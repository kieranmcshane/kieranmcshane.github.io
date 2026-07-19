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
import re
import subprocess
import tempfile
import time
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import EloModel, GaussianSkillModel, Match


SCHEMA_VERSION = "1.0.0"
USER_AGENT = "kieranmcshane-rating-lab/1.0 (+https://kieranmcshane.github.io/rating-lab/)"
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
                full_time = score.get("ft") if isinstance(score, dict) else None
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
    advantage = 65.0 if sport == "football" else 0.0
    bayes_advantage = 1.35 if sport == "football" else 0.4 if sport == "chess" else 0.0
    draw_margin = 1.35 if sport == "football" else 0.75 if sport == "chess" else 0.0
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
    for match in sorted(matches, key=lambda item: (item.date, item.entity_a, item.entity_b)):
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


def build_sport_payload(sport: str, matches: list[Match], entities: dict, source_meta: dict) -> dict:
    matches = sorted(_deduplicate(matches), key=lambda item: (item.date, item.entity_a, item.entity_b))
    latest = max(match.date for match in matches)
    evaluation_start = latest - timedelta(days=365)
    validation_start = latest - timedelta(days=730)
    active_cutoff = latest - timedelta(days=365)
    recent_counts = defaultdict(int)
    for match in matches:
        if match.date >= active_cutoff:
            recent_counts[match.entity_a] += 1
            recent_counts[match.entity_b] += 1
    minimum = 10 if sport == "tennis" else 20 if sport == "chess" else 0
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
    for model_name in ("elo", "trueskill", "robust"):
        params = _choose_parameters(matches, sport, model_name, validation_start, evaluation_start)
        selected_parameters[model_name] = params
        states, predictions, histories = _run_model(
            matches,
            _new_model(model_name, params),
            sport,
            history_entities=history_entities,
        )
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
    return {
        "schema_version": SCHEMA_VERSION,
        "sport": sport,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "latest_result": latest.isoformat(),
        "source": source_meta,
        "competitions": sorted({info.get("competition", "") for info in entities.values() if info.get("competition")}),
        "parameters": selected_parameters,
        "models": model_payloads,
    }


def validate_payload(payload: dict, schema: dict) -> None:
    required = schema["required"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"Missing payload keys: {', '.join(missing)}")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unexpected schema version")
    for name in ("elo", "trueskill", "robust"):
        if name not in payload["models"]:
            raise ValueError(f"Missing model {name}")
        ranks = [row["rank"] for row in payload["models"][name]["rankings"]]
        if ranks != list(range(1, len(ranks) + 1)):
            raise ValueError(f"Non-contiguous {name} ranks")


def write_outputs(output_dir: Path, requested: list[str], *, chess_months: int = 36) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    schema = json.loads((Path(__file__).with_name("schema.json")).read_text())
    token = os.environ.get("FOOTBALL_DATA_TOKEN")
    loaders = {
        "tennis": lambda: fetch_tennis(),
        "football": lambda: fetch_football(token),
        "chess": lambda: fetch_chess(chess_months),
    }
    statuses = {}
    for sport in ("tennis", "football", "chess"):
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
        }
    with tempfile.TemporaryDirectory(prefix="rating-lab-") as temporary:
        temporary_path = Path(temporary)
        for sport in requested:
            try:
                matches, entities, source_meta = loaders[sport]()
                payload = build_sport_payload(sport, matches, entities, source_meta)
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
                }
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sports": statuses,
        "models": ["elo", "trueskill", "robust"],
        "methodology_url": "/rating-lab/#methodology",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest
