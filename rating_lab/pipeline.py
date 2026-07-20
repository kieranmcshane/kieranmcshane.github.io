"""Fetch public match data and build the versioned Rating Lab JSON contract."""

from __future__ import annotations

from collections import defaultdict
import csv
from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import random
import re
import subprocess
import tempfile
import time
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import EloModel, GaussianSkillModel, Match


SCHEMA_VERSION = "1.2.0"
METHODOLOGY_VERSION = "2026-07-20.2"
SPORTS = ("tennis", "football", "national-football", "chess")
USER_AGENT = "kieranmcshane-rating-lab/1.2 (+https://kieranmcshane.github.io/rating-lab/)"
FOOTBALL_COMPETITIONS = {
    "PL": "Premier League",
    "PD": "La Liga",
    "BL1": "Bundesliga",
    "SA": "Serie A",
    "FL1": "Ligue 1",
    "CL": "Champions League",
}
OPEN_FOOTBALL_CODES = {
    "en.1": "Premier League",
    "es.1": "La Liga",
    "de.1": "Bundesliga",
    "it.1": "Serie A",
    "fr.1": "Ligue 1",
}
OPEN_FOOTBALL_FIXTURES = {
    "premier-league": (
        "Premier League",
        "https://raw.githubusercontent.com/openfootball/england/master/{season}/1-premierleague.txt",
    ),
    "la-liga": (
        "La Liga",
        "https://raw.githubusercontent.com/openfootball/espana/master/{season}/1-liga.txt",
    ),
    "bundesliga": (
        "Bundesliga",
        "https://raw.githubusercontent.com/openfootball/deutschland/master/{season}/1-bundesliga.txt",
    ),
    "serie-a": (
        "Serie A",
        "https://raw.githubusercontent.com/openfootball/italy/master/{season}/1-seriea.txt",
    ),
    "ligue-1": (
        "Ligue 1",
        "https://raw.githubusercontent.com/openfootball/france/master/france/{season}_fr1.txt",
    ),
}
PREDICTOR_SIMULATIONS = 5_000


def _get(
    url: str,
    *,
    token: str | None = None,
    attempts: int = 3,
    cache_ttl: int = 21_600,
) -> bytes:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json, text/csv, */*"}
    if token:
        headers["X-Auth-Token"] = token
    cache_root = os.environ.get("RATING_LAB_CACHE_DIR")
    cache_file = None
    if cache_root:
        cache_file = Path(cache_root) / hashlib.sha256(url.encode()).hexdigest()
        if cache_file.exists() and time.time() - cache_file.stat().st_mtime < cache_ttl:
            return cache_file.read_bytes()
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urlopen(Request(url, headers=headers), timeout=45) as response:
                body = response.read()
            if cache_file:
                cache_file.parent.mkdir(parents=True, exist_ok=True)
                cache_file.write_bytes(body)
            return body
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"Unable to fetch {url}: {last_error}")


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def _season_label(year: int) -> str:
    return f"{year}-{str(year + 1)[-2:]}"


def fetch_tennis(start_year: int = 2018) -> tuple[list[Match], dict, dict]:
    current_year = datetime.now(timezone.utc).year
    matches: list[Match] = []
    entities: dict[str, dict] = {}
    latest = None
    tournaments_url = (
        "https://raw.githubusercontent.com/msolonskyi/ManTennisData/master/"
        "atp/tournaments.csv"
    )
    tournaments_body = _get(tournaments_url, cache_ttl=21_600).decode("utf-8-sig")
    tournaments = {}
    for tournament in csv.DictReader(io.StringIO(tournaments_body)):
        raw_date = tournament.get("start_dtm", "")
        if not raw_date or not raw_date[:8].isdigit():
            continue
        tournaments[tournament["id"]] = {
            "date": datetime.strptime(raw_date[:8], "%Y%m%d").date(),
            "name": tournament.get("name") or "ATP",
            "surface": tournament.get("surface", ""),
        }
    for year in range(start_year, current_year + 1):
        url = (
            "https://raw.githubusercontent.com/msolonskyi/ManTennisData/master/"
            f"atp/matches_{year}.csv"
        )
        try:
            ttl = 31_536_000 if year < current_year else 21_600
            body = _get(url, cache_ttl=ttl).decode("utf-8-sig")
        except RuntimeError:
            if year == current_year:
                continue
            raise
        for row in csv.DictReader(io.StringIO(body)):
            tournament = tournaments.get(row.get("tournament_id", ""))
            if not row.get("winner_code") or not row.get("loser_code") or not tournament:
                continue
            played = tournament["date"]
            if played > datetime.now(timezone.utc).date():
                continue
            winner = f"atp:{row['winner_code']}"
            loser = f"atp:{row['loser_code']}"
            entities[winner] = {
                "name": row.get("winner_name") or winner,
                "country": row.get("winner_citizenship", ""),
                "competition": "ATP singles",
            }
            entities[loser] = {
                "name": row.get("loser_name") or loser,
                "country": row.get("loser_citizenship", ""),
                "competition": "ATP singles",
            }
            entity_a, entity_b = sorted((winner, loser))
            matches.append(
                Match(
                    played,
                    entity_a,
                    entity_b,
                    1.0 if entity_a == winner else 0.0,
                    tournament["name"],
                    str(year),
                    metadata={"surface": tournament["surface"]},
                )
            )
            latest = max(latest or played, played)
    meta = {
        "source": "ManTennisData (ATP-derived)",
        "source_url": "https://github.com/msolonskyi/ManTennisData",
        "license": "MIT",
        "latest_result": latest.isoformat() if latest else None,
        "stale_after_hours": 240,
    }
    return matches, entities, meta


def fetch_football(token: str | None, start_year: int = 2020) -> tuple[list[Match], dict, dict]:
    if not token:
        return fetch_open_football(start_year)
    current_year = datetime.now(timezone.utc).year
    matches: list[Match] = []
    entities: dict[str, dict] = {}
    latest = None
    successful_sources = 0
    for code, label in FOOTBALL_COMPETITIONS.items():
        for year in range(start_year, current_year + 1):
            url = f"https://api.football-data.org/v4/competitions/{code}/matches?season={year}"
            try:
                ttl = 31_536_000 if year < current_year - 1 else 21_600
                payload = json.loads(_get(url, token=token, cache_ttl=ttl))
            except (RuntimeError, json.JSONDecodeError):
                continue
            successful_sources += 1
            for row in payload.get("matches", []):
                if row.get("status") != "FINISHED":
                    continue
                score = row.get("score", {}).get("fullTime", {})
                home_goals, away_goals = score.get("home"), score.get("away")
                if home_goals is None or away_goals is None:
                    continue
                played = date.fromisoformat(row["utcDate"][:10])
                home = f"football:{row['homeTeam']['id']}"
                away = f"football:{row['awayTeam']['id']}"
                for entity, name in ((home, row["homeTeam"]["name"]), (away, row["awayTeam"]["name"])):
                    previous = entities.get(entity, {})
                    competition = previous.get("competition", "") if label == "Champions League" else label
                    entities[entity] = {"name": name, "country": "", "competition": competition or label}
                result = 1.0 if home_goals > away_goals else 0.0 if home_goals < away_goals else 0.5
                matches.append(Match(played, home, away, result, label, str(year), True))
                latest = max(latest or played, played)
    if not successful_sources or not matches:
        raise RuntimeError("football-data.org returned no usable competitions")
    meta = {
        "source": "football-data.org",
        "source_url": "https://www.football-data.org/",
        "license": "football-data.org terms",
        "latest_result": latest.isoformat() if latest else None,
        "stale_after_hours": 48,
    }
    matches = _deduplicate(matches)
    _mark_active_football(matches, entities)
    return matches, entities, meta


def fetch_open_football(start_year: int = 2020) -> tuple[list[Match], dict, dict]:
    """Keyless development fallback; production uses football-data.org."""
    current_year = datetime.now(timezone.utc).year
    matches: list[Match] = []
    entities: dict[str, dict] = {}
    latest = None
    for year in range(start_year, current_year + 1):
        season = _season_label(year)
        for code, label in OPEN_FOOTBALL_CODES.items():
            url = f"https://raw.githubusercontent.com/openfootball/football.json/master/{season}/{code}.json"
            try:
                ttl = 31_536_000 if year < current_year - 1 else 21_600
                payload = json.loads(_get(url, cache_ttl=ttl))
            except (RuntimeError, json.JSONDecodeError):
                continue
            for row in payload.get("matches", []):
                score = row.get("score", {})
                full_time = score.get("ft") if isinstance(score, dict) else score if isinstance(score, list) else None
                if not full_time or len(full_time) != 2 or None in full_time:
                    continue
                try:
                    played = date.fromisoformat(row["date"][:10])
                except (KeyError, ValueError):
                    continue
                home_name = row.get("team1")
                away_name = row.get("team2")
                if not home_name or not away_name:
                    continue
                home = f"football:name:{_slug(home_name)}"
                away = f"football:name:{_slug(away_name)}"
                entities[home] = {"name": home_name, "country": "", "competition": label}
                entities[away] = {"name": away_name, "country": "", "competition": label}
                result = 1.0 if full_time[0] > full_time[1] else 0.0 if full_time[0] < full_time[1] else 0.5
                matches.append(Match(played, home, away, result, label, season, True))
                latest = max(latest or played, played)
    if not matches:
        raise RuntimeError("OpenFootball fallback returned no usable matches")
    meta = {
        "source": "OpenFootball (development fallback)",
        "source_url": "https://github.com/openfootball/football.json",
        "license": "CC0 1.0",
        "latest_result": latest.isoformat() if latest else None,
        "stale_after_hours": 48,
    }
    matches = _deduplicate(matches)
    _mark_active_football(matches, entities)
    return matches, entities, meta


_FIXTURE_DATE = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
_FIXTURE_SCORE = re.compile(r"\s{2,}(\d+)-(\d+)(?:\s+\([^)]*\))?\s*$")


def _parse_football_txt(text: str, competition_id: str, label: str, season: str) -> dict:
    """Parse an OpenFootball league fixture file with optional full-time scores."""
    fixtures: list[dict] = []
    current_date: date | None = None
    current_year = int(season[:4])
    previous_month = None
    round_name = ""
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("▪"):
            round_name = line.strip().lstrip("▪").strip()
            continue
        date_match = _FIXTURE_DATE.match(line)
        if date_match:
            month_name, day_text, explicit_year = date_match.groups()
            month = datetime.strptime(month_name, "%b").month
            if explicit_year:
                current_year = int(explicit_year)
            elif previous_month is not None and month < previous_month - 6:
                current_year += 1
            current_date = date(current_year, month, int(day_text))
            previous_month = month
            continue
        if current_date is None or " v " not in line:
            continue
        match_text = re.sub(r"^\s*(?:\d{1,2}:\d{2}\s+)?", "", line)
        home_name, right = match_text.split(" v ", 1)
        score_match = _FIXTURE_SCORE.search(right)
        home_goals = away_goals = None
        if score_match:
            home_goals, away_goals = map(int, score_match.groups())
            away_name = right[: score_match.start()].strip()
        else:
            away_name = right.strip()
        home_name = home_name.strip()
        if not home_name or not away_name:
            continue
        fixtures.append(
            {
                "date": current_date.isoformat(),
                "round": round_name,
                "home_name": home_name,
                "away_name": away_name,
                "home_goals": home_goals,
                "away_goals": away_goals,
            }
        )
    if not fixtures:
        raise RuntimeError(f"No fixtures parsed for {label} {season}")
    teams = sorted({fixture[key] for fixture in fixtures for key in ("home_name", "away_name")})
    return {
        "id": competition_id,
        "label": label,
        "season": season,
        "teams": teams,
        "fixtures": fixtures,
    }


def fetch_league_schedules() -> list[dict]:
    today = datetime.now(timezone.utc).date()
    season_start = today.year if today.month >= 7 else today.year - 1
    season = _season_label(season_start)
    competitions = []
    for competition_id, (label, template) in OPEN_FOOTBALL_FIXTURES.items():
        url = template.format(season=season)
        body = _get(url, cache_ttl=21_600)
        competition = _parse_football_txt(body.decode("utf-8-sig"), competition_id, label, season)
        competition["source_url"] = url
        competition["license"] = "CC0 1.0"
        competition["snapshot_sha256"] = hashlib.sha256(body).hexdigest()
        competitions.append(competition)
    return competitions


def _merge_schedule_results(matches: list[Match], entities: dict, schedules: list[dict]) -> list[Match]:
    """Add the fixture source's completed results so ratings and table advance together."""
    entity_by_name = {_slug(info.get("name", "")): entity for entity, info in entities.items()}
    for info in entities.values():
        if info.get("competition") in set(OPEN_FOOTBALL_CODES.values()):
            info["active"] = False
    for competition in schedules:
        team_ids = {}
        for name in competition["teams"]:
            entity = entity_by_name.get(_slug(name), f"football:name:{_slug(name)}")
            entity_by_name[_slug(name)] = entity
            team_ids[name] = entity
            entities[entity] = {
                **entities.get(entity, {}),
                "name": name,
                "country": entities.get(entity, {}).get("country", ""),
                "competition": competition["label"],
                "active": True,
            }
        for fixture in competition["fixtures"]:
            if fixture["home_goals"] is None or fixture["away_goals"] is None:
                continue
            home_goals, away_goals = fixture["home_goals"], fixture["away_goals"]
            result = 1.0 if home_goals > away_goals else 0.0 if home_goals < away_goals else 0.5
            matches.append(
                Match(
                    date.fromisoformat(fixture["date"]),
                    team_ids[fixture["home_name"]],
                    team_ids[fixture["away_name"]],
                    result,
                    competition["label"],
                    competition["season"],
                    True,
                )
            )
    return _deduplicate(matches)


def _parse_international_results(text: str, start_year: int = 2016) -> tuple[list[Match], dict]:
    """Parse Mart Jürisoo's CC0 men's full-international results."""
    matches: list[Match] = []
    entities: dict[str, dict] = {}
    today = datetime.now(timezone.utc).date()
    for row in csv.DictReader(io.StringIO(text)):
        try:
            played = date.fromisoformat(row.get("date", ""))
            home_goals = int(row.get("home_score", ""))
            away_goals = int(row.get("away_score", ""))
        except (TypeError, ValueError):
            continue
        if played.year < start_year or played > today:
            continue
        home_name = (row.get("home_team") or "").strip()
        away_name = (row.get("away_team") or "").strip()
        if not home_name or not away_name or home_name == away_name:
            continue
        home = f"national-football:{_slug(home_name)}"
        away = f"national-football:{_slug(away_name)}"
        entities[home] = {
            "name": home_name,
            "country": "",
            "competition": "Men's national teams",
        }
        entities[away] = {
            "name": away_name,
            "country": "",
            "competition": "Men's national teams",
        }
        result = 1.0 if home_goals > away_goals else 0.0 if home_goals < away_goals else 0.5
        neutral = (row.get("neutral") or "").strip().casefold() == "true"
        competition = (row.get("tournament") or "International").strip()
        matches.append(
            Match(
                played,
                home,
                away,
                result,
                competition,
                str(played.year),
                not neutral,
                {"neutral": str(neutral).lower()},
            )
        )
    return matches, entities


def fetch_national_football(start_year: int = 2016) -> tuple[list[Match], dict, dict]:
    url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
    body = _get(url, cache_ttl=21_600)
    matches, entities = _parse_international_results(body.decode("utf-8-sig"), start_year)
    if not matches:
        raise RuntimeError("International results source returned no usable matches")
    matches = _deduplicate(matches)
    latest = max(match.date for match in matches)
    meta = {
        "source": "International football results by Mart Jürisoo",
        "source_url": "https://github.com/martj42/international_results",
        "license": "CC0 1.0",
        "latest_result": latest.isoformat(),
        "stale_after_hours": 168,
        "snapshot_sha256": hashlib.sha256(body).hexdigest(),
    }
    return matches, entities, meta


def _mark_active_football(matches: list[Match], entities: dict) -> None:
    domestic = set(FOOTBALL_COMPETITIONS.values()) - {"Champions League"}
    latest_season: dict[str, str] = {}
    for match in matches:
        if match.competition not in domestic:
            continue
        current = latest_season.get(match.competition)
        if current is None or match.season > current:
            latest_season[match.competition] = match.season
    for info in entities.values():
        info["active"] = False
    for match in matches:
        if latest_season.get(match.competition) != match.season:
            continue
        entities.get(match.entity_a, {})["active"] = True
        entities.get(match.entity_b, {})["active"] = True


_PGN_HEADER = re.compile(r'^\[([A-Za-z0-9_]+) "(.*)"\]$')


def _chess_id(headers: dict[str, str], color: str) -> tuple[str, str]:
    name = headers.get(color, "Unknown").strip()
    fide_id = headers.get(f"{color}FideId") or headers.get(f"{color}FideID")
    if fide_id and fide_id.isdigit():
        return f"chess:fide:{fide_id}", name
    return f"chess:name:{_slug(name)}", name


def _parse_broadcast_pgn(text: str) -> tuple[list[Match], dict]:
    matches: list[Match] = []
    entities: dict[str, dict] = {}
    headers: dict[str, str] = {}

    def flush() -> None:
        nonlocal headers
        if not headers or headers.get("Result") not in {"1-0", "0-1", "1/2-1/2"}:
            headers = {}
            return
        raw_date = headers.get("UTCDate") or headers.get("Date", "")
        try:
            played = date.fromisoformat(raw_date.replace(".", "-")[:10])
        except ValueError:
            headers = {}
            return
        white, white_name = _chess_id(headers, "White")
        black, black_name = _chess_id(headers, "Black")
        if white == black or "unknown" in {white_name.casefold(), black_name.casefold()}:
            headers = {}
            return
        # Broadcast archives also include engine events. FIDE IDs provide a
        # stable identity boundary for the intended elite human OTB cohort.
        if not white.startswith("chess:fide:") or not black.startswith("chess:fide:"):
            headers = {}
            return
        white_rating = int(headers.get("WhiteElo", "0")) if headers.get("WhiteElo", "").isdigit() else 0
        black_rating = int(headers.get("BlackElo", "0")) if headers.get("BlackElo", "").isdigit() else 0
        entities[white] = {"name": white_name, "country": headers.get("WhiteFederation", ""), "competition": "Elite OTB", "official_rating": max(white_rating, entities.get(white, {}).get("official_rating", 0))}
        entities[black] = {"name": black_name, "country": headers.get("BlackFederation", ""), "competition": "Elite OTB", "official_rating": max(black_rating, entities.get(black, {}).get("official_rating", 0))}
        result = {"1-0": 1.0, "0-1": 0.0, "1/2-1/2": 0.5}[headers["Result"]]
        matches.append(Match(played, white, black, result, headers.get("Event", "Lichess broadcast"), str(played.year), True, {"rating_a": str(white_rating), "rating_b": str(black_rating)}))
        headers = {}

    for line in text.splitlines():
        line = line.strip()
        match = _PGN_HEADER.match(line)
        if match:
            if match.group(1) == "Event" and headers:
                flush()
            headers[match.group(1)] = match.group(2)
    flush()
    return matches, entities


def _fetch_current_broadcasts(limit: int = 40) -> tuple[list[Match], dict]:
    """Fetch recent high-tier broadcast rounds not yet in monthly archives."""
    body = _get("https://lichess.org/api/broadcast", cache_ttl=10_800).decode("utf-8", "replace")
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    recent_ms = now_ms - 45 * 86_400_000
    round_ids: list[tuple[str, bool]] = []
    for line in body.splitlines():
        try:
            broadcast = json.loads(line)
        except json.JSONDecodeError:
            continue
        if broadcast.get("tour", {}).get("tier", 0) < 3:
            continue
        for round_info in broadcast.get("rounds", []):
            starts = round_info.get("startsAt", 0)
            if recent_ms <= starts <= now_ms:
                round_ids.append((round_info["id"], bool(round_info.get("finished"))))
        if len(round_ids) >= limit:
            break
    matches: list[Match] = []
    entities: dict[str, dict] = {}
    for round_id, finished in round_ids[:limit]:
        url = f"https://lichess.org/api/broadcast/round/{round_id}.pgn"
        try:
            ttl = 31_536_000 if finished else 10_800
            pgn = _get(url, cache_ttl=ttl).decode("utf-8", "replace")
        except RuntimeError:
            continue
        batch, batch_entities = _parse_broadcast_pgn(pgn)
        matches.extend(batch)
        entities.update(batch_entities)
    return matches, entities


def fetch_chess(months: int = 36) -> tuple[list[Match], dict, dict]:
    if not shutil_which("zstd"):
        raise RuntimeError("zstd is required to read official Lichess broadcast archives")
    today = datetime.now(timezone.utc).date().replace(day=1)
    matches: list[Match] = []
    entities: dict[str, dict] = {}
    successful = 0
    cursor = today
    for _ in range(months + 2):
        cursor = (cursor - timedelta(days=1)).replace(day=1)
        url = f"https://database.lichess.org/broadcast/lichess_db_broadcast_{cursor:%Y-%m}.pgn.zst"
        try:
            compressed = _get(url, attempts=2, cache_ttl=31_536_000)
        except RuntimeError:
            continue
        with tempfile.NamedTemporaryFile(suffix=".pgn.zst") as archive:
            archive.write(compressed)
            archive.flush()
            process = subprocess.run(
                ["zstd", "-dc", archive.name], capture_output=True, check=True
            )
        batch, batch_entities = _parse_broadcast_pgn(process.stdout.decode("utf-8", "replace"))
        matches.extend(batch)
        entities.update(batch_entities)
        successful += 1
        if successful >= months:
            break
    current_matches, current_entities = _fetch_current_broadcasts()
    matches.extend(current_matches)
    entities.update(current_entities)
    if not matches:
        raise RuntimeError("Lichess broadcast archives returned no usable games")
    matches = _deduplicate(matches)
    latest = max(match.date for match in matches)
    meta = {
        "source": "Lichess official broadcasts",
        "source_url": "https://database.lichess.org/#broadcasts",
        "license": "CC BY-SA 4.0",
        "latest_result": latest.isoformat(),
        "stale_after_hours": 840,
    }
    return matches, entities, meta


def shutil_which(command: str) -> str | None:
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / command
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def _deduplicate(matches: Iterable[Match]) -> list[Match]:
    unique: dict[str, Match] = {}
    for match in matches:
        signature = "|".join(
            [match.date.isoformat(), match.entity_a, match.entity_b, str(match.score_a), match.competition]
        )
        unique[hashlib.sha1(signature.encode()).hexdigest()] = match
    return list(unique.values())


def _match_sort_key(match: Match) -> tuple:
    return (
        match.date,
        match.entity_a,
        match.entity_b,
        match.competition,
        match.score_a,
    )


def _metrics(predictions: list[dict], cutoff: date) -> dict:
    sample = [row for row in predictions if date.fromisoformat(row["date"]) >= cutoff]
    if not sample:
        return {"log_loss": None, "brier": None, "calibration": None, "predictions": 0}
    log_loss = brier = 0.0
    bins = defaultdict(lambda: [0.0, 0.0, 0])
    for row in sample:
        probability = min(max(row["predicted"], 1e-9), 1 - 1e-9)
        actual = row["actual"]
        log_loss -= actual * math.log(probability) + (1 - actual) * math.log(1 - probability)
        brier += (probability - actual) ** 2
        bucket = min(int(probability * 10), 9)
        bins[bucket][0] += probability
        bins[bucket][1] += actual
        bins[bucket][2] += 1
    count = len(sample)
    calibration = sum(
        abs(total_p / size - total_y / size) * size / count
        for total_p, total_y, size in bins.values()
    )
    return {
        "log_loss": round(log_loss / count, 4),
        "brier": round(brier / count, 4),
        "calibration": round(calibration, 4),
        "predictions": count,
    }


def _model_candidates(sport: str, model_name: str) -> list[dict]:
    football_like = sport in {"football", "national-football"}
    advantage = 65.0 if football_like else 0.0
    bayes_advantage = 1.35 if football_like else 0.4 if sport == "chess" else 0.0
    draw_margin = 1.35 if football_like else 0.75 if sport == "chess" else 0.0
    if model_name == "elo":
        return [{"k": k, "scale": 400.0, "home": advantage} for k in (16.0, 24.0, 32.0)]
    robust = model_name == "robust"
    return [
        {"robust": robust, "beta": beta, "draw_margin": draw_margin, "advantage": bayes_advantage}
        for beta in (3.5, 25.0 / 6.0, 5.0)
    ]


def _new_model(model_name: str, params: dict):
    return EloModel(**params) if model_name == "elo" else GaussianSkillModel(**params)


def _run_model(
    matches: list[Match],
    model,
    sport: str,
    *,
    history_entities: set[str] | None = None,
) -> tuple[dict, list[dict], dict[str, list]]:
    predictions: list[dict] = []
    histories: dict[str, list] = defaultdict(list)
    previous_season = None
    for match in sorted(matches, key=_match_sort_key):
        if sport == "chess":
            for entity, key in ((match.entity_a, "rating_a"), (match.entity_b, "rating_b")):
                if entity in model.states:
                    continue
                raw_rating = match.metadata.get(key, "")
                if not raw_rating.isdigit() or int(raw_rating) < 1000:
                    continue
                state = model.state(entity)
                if isinstance(model, EloModel):
                    state.mean = float(raw_rating)
                else:
                    state.mean = 25.0 + (float(raw_rating) - 2000.0) / 80.0
                    state.variance = 9.0
        if (
            sport == "football"
            and isinstance(model, EloModel)
            and previous_season is not None
            and match.season != previous_season
        ):
            model.regress(0.25)
        probability = model.update(match)
        predictions.append({"date": match.date.isoformat(), "predicted": probability, "actual": match.score_a})
        for entity in (match.entity_a, match.entity_b):
            if history_entities is not None and entity not in history_entities:
                continue
            state = model.states[entity]
            rating = state.mean if isinstance(model, EloModel) else state.mean - 3 * state.sigma
            series = histories[entity]
            point = [match.date.isoformat(), round(rating, 2)]
            if series and series[-1][0] == point[0]:
                series[-1] = point
            else:
                series.append(point)
        previous_season = match.season or previous_season
    return model.states, predictions, histories


def _choose_parameters(matches: list[Match], sport: str, model_name: str, validation_start: date, evaluation_start: date) -> dict:
    best_params = None
    best_loss = float("inf")
    # Ratings are warmed up on all older results, then parameters are chosen
    # strictly on the 24-to-12-month validation interval.
    tuning_matches = [match for match in matches if match.date < evaluation_start]
    for params in _model_candidates(sport, model_name):
        _, predictions, _ = _run_model(
            tuning_matches,
            _new_model(model_name, params),
            sport,
            history_entities=set(),
        )
        validation = [
            row for row in predictions
            if validation_start <= date.fromisoformat(row["date"]) < evaluation_start
        ]
        score = _metrics(validation, validation_start)["log_loss"] if validation else None
        if score is not None and score < best_loss:
            best_loss = score
            best_params = params
    return best_params or _model_candidates(sport, model_name)[1]


def _compress_history(points: list[list], limit: int = 24) -> list[list]:
    if len(points) <= limit:
        return points
    step = max(len(points) // (limit - 1), 1)
    sampled = points[::step]
    if sampled[-1] != points[-1]:
        sampled.append(points[-1])
    return sampled[-limit:]


def _simulate_league(
    competition: dict,
    model,
    model_name: str,
    entities: dict,
    historical_draw_rate: float,
    simulations: int = PREDICTOR_SIMULATIONS,
) -> dict:
    """Simulate a league from its actual table and remaining fixture list."""
    names = competition["teams"]
    team_count = len(names)
    index_by_name = {name: index for index, name in enumerate(names)}
    entity_by_name = {_slug(info.get("name", "")): entity for entity, info in entities.items()}
    entity_ids = [entity_by_name.get(_slug(name), f"football:name:{_slug(name)}") for name in names]
    strengths = []
    for entity in entity_ids:
        state = model.state(entity)
        strengths.append(state.mean)

    base_points = [0] * team_count
    base_goal_difference = [0] * team_count
    base_games = [0] * team_count
    remaining = []
    completed = 0
    latest_completed = None
    for fixture in competition["fixtures"]:
        home_index = index_by_name[fixture["home_name"]]
        away_index = index_by_name[fixture["away_name"]]
        if fixture["home_goals"] is not None and fixture["away_goals"] is not None:
            home_goals, away_goals = fixture["home_goals"], fixture["away_goals"]
            base_games[home_index] += 1
            base_games[away_index] += 1
            base_goal_difference[home_index] += home_goals - away_goals
            base_goal_difference[away_index] += away_goals - home_goals
            if home_goals > away_goals:
                base_points[home_index] += 3
            elif home_goals < away_goals:
                base_points[away_index] += 3
            else:
                base_points[home_index] += 1
                base_points[away_index] += 1
            completed += 1
            latest_completed = max(latest_completed or fixture["date"], fixture["date"])
            continue
        future_match = Match(
            date.fromisoformat(fixture["date"]),
            entity_ids[home_index],
            entity_ids[away_index],
            0.5,
            competition["label"],
            competition["season"],
            True,
        )
        if isinstance(model, EloModel):
            probabilities = model.predict_outcomes(future_match, historical_draw_rate)
        else:
            probabilities = model.predict_outcomes(future_match)
        remaining.append((home_index, away_index, probabilities))

    def order(points: list[int], goal_difference: list[int]) -> list[int]:
        return sorted(
            range(team_count),
            key=lambda index: (-points[index], -goal_difference[index], -strengths[index], names[index]),
        )

    current_order = order(base_points, base_goal_difference)
    current_rank = [0] * team_count
    for rank, index in enumerate(current_order, 1):
        current_rank[index] = rank

    finish_counts = [[0] * team_count for _ in range(team_count)]
    point_sums = [0] * team_count
    seed_material = f"{METHODOLOGY_VERSION}|{competition['id']}|{competition['season']}|{model_name}"
    seed = int.from_bytes(hashlib.sha256(seed_material.encode()).digest()[:8], "big")
    generator = random.Random(seed)
    for _ in range(simulations):
        points = base_points.copy()
        goal_difference = base_goal_difference.copy()
        for home_index, away_index, probabilities in remaining:
            home_win, draw, _away_win = probabilities
            outcome = generator.random()
            if outcome < home_win:
                points[home_index] += 3
                margin_roll = generator.random()
                margin = 1 if margin_roll < 0.64 else 2 if margin_roll < 0.92 else 3
                goal_difference[home_index] += margin
                goal_difference[away_index] -= margin
            elif outcome < home_win + draw:
                points[home_index] += 1
                points[away_index] += 1
            else:
                points[away_index] += 3
                margin_roll = generator.random()
                margin = 1 if margin_roll < 0.64 else 2 if margin_roll < 0.92 else 3
                goal_difference[away_index] += margin
                goal_difference[home_index] -= margin
        for position, index in enumerate(order(points, goal_difference)):
            finish_counts[index][position] += 1
            point_sums[index] += points[index]

    teams = []
    for index, name in enumerate(names):
        position_probabilities = [count / simulations for count in finish_counts[index]]
        teams.append(
            {
                "id": entity_ids[index],
                "name": name,
                "current_rank": current_rank[index],
                "played": base_games[index],
                "current_points": base_points[index],
                "expected_points": round(point_sums[index] / simulations, 1),
                "expected_position": round(
                    sum((position + 1) * probability for position, probability in enumerate(position_probabilities)),
                    2,
                ),
                "champion": round(position_probabilities[0], 4),
                "top_four": round(sum(position_probabilities[:4]), 4),
                "bottom_three": round(sum(position_probabilities[-3:]), 4),
                "positions": [round(probability, 4) for probability in position_probabilities],
            }
        )
    teams.sort(key=lambda team: (team["expected_position"], team["name"]))
    return {
        "seed": f"{seed:016x}",
        "simulations": simulations,
        "completed_matches": completed,
        "remaining_matches": len(remaining),
        "latest_completed": latest_completed,
        "teams": teams,
    }


def _build_tournament_predictor(
    schedules: list[dict],
    models: dict,
    entities: dict,
    matches: list[Match],
) -> dict:
    draw_rate = sum(match.score_a == 0.5 for match in matches) / len(matches)
    competitions = []
    for schedule in schedules:
        competition = {
            key: schedule[key]
            for key in ("id", "label", "season", "source_url", "license", "snapshot_sha256")
        }
        competition["total_matches"] = len(schedule["fixtures"])
        competition["first_fixture"] = min(row["date"] for row in schedule["fixtures"])
        competition["last_fixture"] = max(row["date"] for row in schedule["fixtures"])
        unplayed_dates = [
            row["date"] for row in schedule["fixtures"] if row["home_goals"] is None
        ]
        competition["next_fixture"] = min(unplayed_dates) if unplayed_dates else None
        competition["models"] = {
            model_name: _simulate_league(
                schedule,
                model,
                model_name,
                entities,
                draw_rate,
            )
            for model_name, model in models.items()
        }
        completed = competition["models"]["elo"]["completed_matches"]
        competition["status"] = (
            "scheduled" if completed == 0 else "complete" if completed == competition["total_matches"] else "live"
        )
        competitions.append(competition)
    return {
        "format": "round-robin league",
        "simulations_per_model": PREDICTOR_SIMULATIONS,
        "draw_model": "Model draw likelihood; Elo uses the historical football draw rate scaled by matchup closeness.",
        "tie_break": "Points, simulated goal difference, then current model strength.",
        "strengths": "Fixed at the generation-time rating state; completed results change both the table and the next refresh's ratings.",
        "competitions": competitions,
    }


def build_sport_payload(
    sport: str,
    matches: list[Match],
    entities: dict,
    source_meta: dict,
    predictor_schedules: list[dict] | None = None,
) -> dict:
    matches = sorted(_deduplicate(matches), key=_match_sort_key)
    latest = max(match.date for match in matches)
    evaluation_start = latest - timedelta(days=365)
    validation_start = latest - timedelta(days=730)
    active_window_days = 730 if sport == "national-football" else 365
    active_cutoff = latest - timedelta(days=active_window_days)
    recent_counts = defaultdict(int)
    for match in matches:
        if match.date >= active_cutoff:
            recent_counts[match.entity_a] += 1
            recent_counts[match.entity_b] += 1
    minimum = (
        10 if sport == "tennis"
        else 20 if sport == "chess"
        else 5 if sport == "national-football"
        else 0
    )
    history_entities = {
        entity
        for entity in entities
        if recent_counts[entity] >= minimum
        and (sport != "football" or entities[entity].get("active", False))
        and (
            sport != "chess"
            or (
                entity.startswith("chess:fide:")
                and entities[entity].get("official_rating", 0) >= 2200
            )
        )
    }
    model_payloads = {}
    selected_parameters = {}
    fitted_models = {}
    for model_name in ("elo", "trueskill", "robust"):
        params = _choose_parameters(matches, sport, model_name, validation_start, evaluation_start)
        selected_parameters[model_name] = params
        fitted_model = _new_model(model_name, params)
        states, predictions, histories = _run_model(
            matches,
            fitted_model,
            sport,
            history_entities=history_entities,
        )
        fitted_models[model_name] = fitted_model
        rows = []
        for entity, state in states.items():
            if entity not in entities or recent_counts[entity] < minimum:
                continue
            if sport == "football" and not entities[entity].get("active", False):
                continue
            if sport == "chess" and (
                not entity.startswith("chess:fide:")
                or entities[entity].get("official_rating", 0) < 2200
            ):
                continue
            conservative = state.mean if model_name == "elo" else state.mean - 3 * state.sigma
            full_history = histories.get(entity, [])
            cutoff_point = next((point[1] for point in reversed(full_history) if date.fromisoformat(point[0]) <= latest - timedelta(days=30)), full_history[0][1] if full_history else conservative)
            history = _compress_history(full_history)
            rows.append(
                {
                    "id": entity,
                    "name": entities[entity]["name"],
                    "country": entities[entity].get("country", ""),
                    "competition": entities[entity].get("competition", ""),
                    "rating": round(state.mean, 2),
                    "sigma": round(state.sigma, 2) if model_name != "elo" else None,
                    "score": round(conservative, 2),
                    "change30": round(conservative - cutoff_point, 2),
                    "matches": state.matches,
                    "recent_matches": recent_counts[entity],
                    "last_played": state.last_played.isoformat() if state.last_played else None,
                    "history": history,
                }
            )
        rows.sort(key=lambda row: (-row["score"], row["name"]))
        rows = rows[:500]
        for rank, row in enumerate(rows, 1):
            row["rank"] = rank
        model_payloads[model_name] = {
            "label": {"elo": "Elo", "trueskill": "Gaussian TrueSkill", "robust": "Robust TrueSkill"}[model_name],
            "metrics": _metrics(predictions, evaluation_start),
            "rankings": rows,
        }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "sport": sport,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "latest_result": latest.isoformat(),
        "source": source_meta,
        "data_window": {
            "first_result": matches[0].date.isoformat(),
            "last_result": latest.isoformat(),
            "matches": len(matches),
            "entities": len(entities),
        },
        "eligibility": {
            "minimum_recent_matches": minimum,
            "recent_window_days": active_window_days,
            "rule": {
                "tennis": "At least 10 ATP matches in the latest 52 weeks.",
                "football": "Member of a covered current-season domestic competition.",
                "national-football": "At least 5 men's full internationals in the latest 24 months.",
                "chess": "FIDE-identified, official rating at least 2200, and 20 games in the latest 12 months.",
            }[sport],
        },
        "competitions": sorted({info.get("competition", "") for info in entities.values() if info.get("competition")}),
        "candidate_parameters": {
            name: _model_candidates(sport, name) for name in ("elo", "trueskill", "robust")
        },
        "parameters": selected_parameters,
        "models": model_payloads,
    }
    if sport == "football" and predictor_schedules:
        payload["tournament_predictor"] = _build_tournament_predictor(
            predictor_schedules, fitted_models, entities, matches
        )
    return payload


def validate_payload(payload: dict, schema: dict) -> None:
    required = schema["required"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"Missing payload keys: {', '.join(missing)}")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unexpected schema version")
    if payload["sport"] not in SPORTS:
        raise ValueError("Unexpected sport")
    allowed = set(schema["properties"])
    unexpected = sorted(set(payload) - allowed)
    if unexpected:
        raise ValueError(f"Unexpected payload keys: {', '.join(unexpected)}")
    window = payload["data_window"]
    if not isinstance(window.get("matches"), int) or window["matches"] < 1:
        raise ValueError("Invalid data window match count")
    if not isinstance(window.get("entities"), int) or window["entities"] < 2:
        raise ValueError("Invalid data window entity count")
    eligibility = payload["eligibility"]
    if not isinstance(eligibility.get("minimum_recent_matches"), int):
        raise ValueError("Invalid eligibility minimum")
    if not isinstance(eligibility.get("recent_window_days"), int):
        raise ValueError("Invalid eligibility window")
    if payload["sport"] == "football":
        predictor = payload.get("tournament_predictor")
        if not predictor or not predictor.get("competitions"):
            raise ValueError("Missing football tournament predictor")
        for competition in predictor["competitions"]:
            if set(competition.get("models", {})) != {"elo", "trueskill", "robust"}:
                raise ValueError("Incomplete tournament prediction models")
    for name in ("elo", "trueskill", "robust"):
        if name not in payload["models"]:
            raise ValueError(f"Missing model {name}")
        ranks = [row["rank"] for row in payload["models"][name]["rankings"]]
        if ranks != list(range(1, len(ranks) + 1)):
            raise ValueError(f"Non-contiguous {name} ranks")
        for row in payload["models"][name]["rankings"]:
            required_row = {"id", "name", "rank", "score", "rating", "sigma", "matches", "recent_matches", "last_played", "history"}
            if not required_row.issubset(row):
                raise ValueError(f"Incomplete {name} ranking row")


def write_outputs(output_dir: Path, requested: list[str], *, chess_months: int = 36) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    schema = json.loads((Path(__file__).with_name("schema.json")).read_text())
    token = os.environ.get("FOOTBALL_DATA_TOKEN")
    loaders = {
        "tennis": lambda: fetch_tennis(),
        "football": lambda: fetch_football(token),
        "national-football": lambda: fetch_national_football(),
        "chess": lambda: fetch_chess(chess_months),
    }
    statuses = {}
    for sport in SPORTS:
        existing = output_dir / f"{sport}.json"
        if sport in requested or not existing.exists():
            continue
        previous = json.loads(existing.read_text())
        statuses[sport] = {
            "status": "current",
            "latest_result": previous.get("latest_result"),
            "source": previous.get("source", {}).get("source", "Unknown"),
            "stale_after_hours": previous.get("source", {}).get("stale_after_hours", 0),
            "checked_at": previous.get("generated_at"),
            "license": previous.get("source", {}).get("license", "Unknown"),
            "source_url": previous.get("source", {}).get("source_url"),
            "snapshot_sha256": previous.get("source", {}).get("snapshot_sha256"),
            "parameters": previous.get("parameters", {}),
        }
    with tempfile.TemporaryDirectory(prefix="rating-lab-") as temporary:
        temporary_path = Path(temporary)
        for sport in requested:
            try:
                matches, entities, source_meta = loaders[sport]()
                predictor_schedules = fetch_league_schedules() if sport == "football" else None
                if predictor_schedules:
                    matches = _merge_schedule_results(matches, entities, predictor_schedules)
                payload = build_sport_payload(
                    sport,
                    matches,
                    entities,
                    source_meta,
                    predictor_schedules=predictor_schedules,
                )
                validate_payload(payload, schema)
                staged = temporary_path / f"{sport}.json"
                staged.write_text(json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n")
                staged.replace(output_dir / staged.name)
                statuses[sport] = {
                    "status": "current",
                    "latest_result": payload["latest_result"],
                    "source": source_meta["source"],
                    "stale_after_hours": source_meta["stale_after_hours"],
                    "checked_at": payload["generated_at"],
                    "license": source_meta.get("license", "Unknown"),
                    "source_url": source_meta.get("source_url"),
                    "snapshot_sha256": source_meta.get("snapshot_sha256"),
                    "parameters": payload["parameters"],
                }
            except Exception as error:
                existing = output_dir / f"{sport}.json"
                if not existing.exists():
                    raise
                previous = json.loads(existing.read_text())
                statuses[sport] = {
                    "status": "retained",
                    "latest_result": previous.get("latest_result"),
                    "source": previous.get("source", {}).get("source", "Unknown"),
                    "stale_after_hours": previous.get("source", {}).get("stale_after_hours", 0),
                    "checked_at": previous.get("generated_at"),
                    "message": str(error)[:240],
                    "license": previous.get("source", {}).get("license", "Unknown"),
                    "source_url": previous.get("source", {}).get("source_url"),
                    "snapshot_sha256": previous.get("source", {}).get("snapshot_sha256"),
                    "parameters": previous.get("parameters", {}),
                }
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "methodology_version": METHODOLOGY_VERSION,
        "code_revision": os.environ.get("GITHUB_SHA") or _git_revision(),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sports": statuses,
        "models": ["elo", "trueskill", "robust"],
        "replay": {
            "order": ["date", "entity_a", "entity_b", "competition", "score_a"],
            "validation_days": 365,
            "evaluation_days": 365,
            "quadrature_nodes": 20,
            "robust_student_t_degrees_of_freedom": 1,
        },
        "tournament_predictor": {
            "simulations_per_competition_model": PREDICTOR_SIMULATIONS,
            "seed": "SHA-256(methodology version, competition, season, model), first 64 bits as hexadecimal",
            "refresh": "daily",
        },
        "methodology_url": "/rating-lab/#methodology",
    }
    (output_dir / "schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def _git_revision() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).resolve().parents[1],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
