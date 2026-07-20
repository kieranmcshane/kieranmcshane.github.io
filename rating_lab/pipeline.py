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
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .models import EloModel, GaussianSkillModel, Glicko2Model, Match, SurfaceBlendModel


SCHEMA_VERSION = "1.9.0"
METHODOLOGY_VERSION = "2026-07-20.10"
SPORTS = ("tennis", "football", "national-football", "chess")
MODEL_NAMES = ("elo", "glicko2", "trueskill", "robust")
SCHEDULE_ENTITY_ALIASES = {
    "national-football": {
        "usa": "united-states",
        "bosnia-herzegovina": "bosnia-and-herzegovina",
    },
}
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
PUBLIC_CUP_COMPETITIONS = {
    "football": {
        "CL": ("UEFA Champions League", "club cup"),
    },
    "national-football": {
        "WC": ("FIFA World Cup", "national cup"),
        "EC": ("UEFA European Championship", "national cup"),
    },
}
KNOCKOUT_STAGES = {
    "LAST_64": 1,
    "ROUND_OF_64": 1,
    "LAST_32": 2,
    "ROUND_OF_32": 2,
    "PLAYOFFS": 2,
    "LAST_16": 3,
    "ROUND_OF_16": 3,
    "QUARTER_FINALS": 4,
    "SEMI_FINALS": 5,
    "FINAL": 6,
}
PREDICTOR_SIMULATIONS = 5_000


def individual_contribution_protocol() -> dict:
    """Publish the exact release gate for outcome-only player contribution ratings."""
    return {
        "status": "withheld_pending_lineup_source",
        "scope": "football players",
        "current_publication_unit": "club or national team",
        "methods": {
            "lineup_trueskill": {
                "input": "match outcome plus the players and minutes on each side",
                "team_performance": "sum(minutes_share * player_performance)",
                "uncertainty": "posterior mean and standard deviation per player",
            },
            "rapm": {
                "input": "score differential plus the players and minutes on each side",
                "estimator": "minutes-weighted ridge regression with chronological validation",
                "uncertainty": "block bootstrap intervals by match",
            },
        },
        "excluded_inputs": [
            "passes",
            "shots",
            "dribbles",
            "expected goals",
            "tracking data",
        ],
        "release_gates": {
            "stable_player_identifiers": "required",
            "starting_lineup_coverage": ">= 95% of eligible matches",
            "substitution_minute_coverage": ">= 95% of eligible matches",
            "lineup_integrity": "11 starters per side and minutes bounded to the match",
            "identifiability": "connected player-opponent graph and published collinearity diagnostics",
            "chronology": "no future lineups or outcomes may enter a past update or evaluation prediction",
            "publication_rights": "source licence must permit derived public ratings and audit metadata",
        },
        "source_assessment": {
            "statsbomb_open_data": "Reproducible historical research archive with selected competitions and seasons; not a complete live five-league feed.",
            "football_data_org": "Potential live source because the API schema includes lineups and substitutions; completeness must be measured with the configured token.",
            "openfootball_fallback": "Results and fixtures only; cannot support player attribution.",
        },
        "publication_rule": "Do not publish player ranks until every release gate passes for the declared cohort.",
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
_FIXTURE_SCORE = re.compile(r"\s{2,}(\d+)-(\d+)(?=\s|$)")


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


def _parse_cup_schedule(payload: dict, code: str, label: str, cohort: str, source_url: str, body: bytes) -> dict | None:
    """Keep the published knockout field; never manufacture unpublished teams or fixtures."""
    fixtures = []
    teams: dict[str, str] = {}
    season = None
    for row in payload.get("matches", []):
        stage = row.get("stage") or "UNKNOWN"
        home_info = row.get("homeTeam") or {}
        away_info = row.get("awayTeam") or {}
        home_name = home_info.get("name")
        away_name = away_info.get("name")
        if not home_name or not away_name:
            continue
        if cohort == "national-football":
            home_id = f"national-football:{_slug(home_name)}"
            away_id = f"national-football:{_slug(away_name)}"
        else:
            home_id = f"football:{home_info.get('id')}" if home_info.get("id") else f"football:name:{_slug(home_name)}"
            away_id = f"football:{away_info.get('id')}" if away_info.get("id") else f"football:name:{_slug(away_name)}"
        teams[home_id] = home_name
        teams[away_id] = away_name
        score = row.get("score") or {}
        full_time = score.get("fullTime") or {}
        winner_code = score.get("winner")
        winner_id = home_id if winner_code == "HOME_TEAM" else away_id if winner_code == "AWAY_TEAM" else None
        season_info = row.get("season") or payload.get("competition", {}).get("currentSeason") or {}
        start_date = season_info.get("startDate")
        if start_date:
            season = str(start_date)[:4]
        fixtures.append(
            {
                "date": str(row.get("utcDate", ""))[:10],
                "stage": stage,
                "group": row.get("group"),
                "status": row.get("status", "SCHEDULED"),
                "home_id": home_id,
                "home_name": home_name,
                "away_id": away_id,
                "away_name": away_name,
                "home_goals": full_time.get("home"),
                "away_goals": full_time.get("away"),
                "winner_id": winner_id,
            }
        )
    if len(teams) < 2 or not fixtures:
        return None
    knockout_fixtures = [row for row in fixtures if row["stage"] in KNOCKOUT_STAGES]
    final = next((row for row in knockout_fixtures if row["stage"] == "FINAL" and row["winner_id"]), None)
    forecast_available = bool(knockout_fixtures)
    if final:
        availability = "Final result published; the completed forecast resolves to the recorded champion."
    elif forecast_available:
        availability = "A knockout field is published. Known ties are preserved; later unpublished draws are sampled."
    else:
        availability = "Waiting for the source to publish a knockout field; no title probability is fabricated from group or qualifying matches alone."
    dates = [row["date"] for row in fixtures if row["date"]]
    return {
        "id": f"{cohort}-{_slug(code)}",
        "label": label,
        "season": season or "current",
        "format": "group + knockout" if code in {"CL", "WC", "EC"} else "knockout cup",
        "cohort": cohort,
        "source_url": source_url,
        "license": "football-data.org terms",
        "snapshot_sha256": hashlib.sha256(body).hexdigest(),
        "teams": [{"id": entity, "name": name} for entity, name in sorted(teams.items(), key=lambda item: item[1])],
        "fixtures": fixtures,
        "knockout_fixtures": knockout_fixtures,
        "forecast_available": forecast_available,
        "availability": availability,
        "first_fixture": min(dates) if dates else None,
        "last_fixture": max(dates) if dates else None,
    }


def fetch_cup_schedules(token: str | None, cohort: str, results: list[Match] | None = None) -> list[dict]:
    """Prefer football-data.org; retain keyless CC0 coverage when no token is configured."""
    competitions = []
    if token:
        for code, (label, _kind) in PUBLIC_CUP_COMPETITIONS[cohort].items():
            url = f"https://api.football-data.org/v4/competitions/{code}/matches"
            try:
                body = _get(url, token=token, cache_ttl=21_600)
                payload = json.loads(body)
            except (RuntimeError, json.JSONDecodeError):
                continue
            schedule = _parse_cup_schedule(payload, code, label, cohort, url, body)
            if schedule:
                competitions.append(schedule)
    schedules = competitions or fetch_open_cup_schedules(cohort)
    return _merge_cup_results(schedules, results or [])


def _merge_cup_results(schedules: list[dict], results: list[Match]) -> list[dict]:
    """Fill a slower fixture snapshot from the already-declared chronological result feed."""
    lookup = {
        (match.date.isoformat(), frozenset((match.entity_a, match.entity_b))): match
        for match in results
    }
    for competition in schedules:
        merged_signatures = []
        for fixture in competition["fixtures"]:
            if fixture["status"] == "FINISHED":
                continue
            match = lookup.get((fixture["date"], frozenset((fixture["home_id"], fixture["away_id"]))))
            if not match or match.score_a == 0.5:
                continue
            home_won = (match.entity_a == fixture["home_id"] and match.score_a == 1.0) or (
                match.entity_b == fixture["home_id"] and match.score_a == 0.0
            )
            fixture["home_goals"], fixture["away_goals"] = (1, 0) if home_won else (0, 1)
            fixture["winner_id"] = fixture["home_id"] if home_won else fixture["away_id"]
            fixture["status"] = "FINISHED"
            merged_signatures.append(f"{fixture['date']}|{fixture['winner_id']}")
        if merged_signatures:
            material = competition["snapshot_sha256"] + "|" + "|".join(sorted(merged_signatures))
            competition["snapshot_sha256"] = hashlib.sha256(material.encode()).hexdigest()
            final = next((row for row in competition["knockout_fixtures"] if row["stage"] == "FINAL" and row["winner_id"]), None)
            if final:
                competition["availability"] = "Final result merged from the ranking's declared result feed; the completed forecast resolves to the recorded champion."
    return schedules


def _cup_stage(label: str) -> str | None:
    value = label.casefold().replace("-", " ")
    if "round of 64" in value or "last 64" in value:
        return "ROUND_OF_64"
    if "round of 32" in value or "last 32" in value:
        return "ROUND_OF_32"
    if "round of 16" in value or "last 16" in value:
        return "ROUND_OF_16"
    if "quarter" in value:
        return "QUARTER_FINALS"
    if "semi" in value:
        return "SEMI_FINALS"
    if "playoff" in value:
        return "PLAYOFFS"
    if value.strip() == "final" or value.rstrip().endswith(", final"):
        return "FINAL"
    return None


def _open_cup_payload(
    *,
    code: str,
    label: str,
    season: str,
    cohort: str,
    source_url: str,
    body: bytes,
    fixtures: list[dict],
) -> dict | None:
    if not fixtures:
        return None
    teams = {
        entity: name
        for row in fixtures
        for entity, name in ((row["home_id"], row["home_name"]), (row["away_id"], row["away_name"]))
    }
    knockout = [row for row in fixtures if row["stage"] in KNOCKOUT_STAGES]
    final = next((row for row in knockout if row["stage"] == "FINAL" and row["winner_id"]), None)
    forecast_available = bool(knockout)
    availability = (
        "Final result published; the completed forecast resolves to the recorded champion."
        if final
        else "A CC0 knockout field is published. Known ties are preserved; later unpublished draws are sampled."
        if forecast_available
        else "Waiting for the CC0 source to publish a knockout field; no title probability is fabricated."
    )
    dates = [row["date"] for row in fixtures if row["date"]]
    return {
        "id": f"{cohort}-{_slug(code)}",
        "label": label,
        "season": season,
        "format": "group + knockout",
        "cohort": cohort,
        "source_url": source_url,
        "license": "CC0 1.0",
        "snapshot_sha256": hashlib.sha256(body).hexdigest(),
        "teams": [{"id": entity, "name": name} for entity, name in sorted(teams.items(), key=lambda item: item[1])],
        "fixtures": fixtures,
        "knockout_fixtures": knockout,
        "forecast_available": forecast_available,
        "availability": availability,
        "first_fixture": min(dates) if dates else None,
        "last_fixture": max(dates) if dates else None,
    }


def _parse_open_cup_json(body: bytes, code: str, label: str, season: str) -> dict | None:
    payload = json.loads(body)
    fixtures = []
    placeholder = re.compile(r"^[WLR]\d+$")
    for row in payload.get("matches", []):
        home_name = str(row.get("team1") or "").strip()
        away_name = str(row.get("team2") or "").strip()
        if not home_name or not away_name or placeholder.match(home_name) or placeholder.match(away_name):
            continue
        stage = _cup_stage(str(row.get("round", ""))) or "GROUP_STAGE"
        score = row.get("score") or {}
        full_time = score.get("ft")
        deciding = score.get("p") or score.get("et") or full_time
        home_id = f"national-football:{_slug(home_name)}"
        away_id = f"national-football:{_slug(away_name)}"
        winner_id = None
        if isinstance(deciding, list) and len(deciding) == 2 and deciding[0] != deciding[1]:
            winner_id = home_id if deciding[0] > deciding[1] else away_id
        fixtures.append(
            {
                "date": str(row.get("date", ""))[:10],
                "stage": stage,
                "group": row.get("group"),
                "status": "FINISHED" if winner_id or (full_time and full_time[0] == full_time[1]) else "SCHEDULED",
                "home_id": home_id,
                "home_name": home_name,
                "away_id": away_id,
                "away_name": away_name,
                "home_goals": full_time[0] if full_time else None,
                "away_goals": full_time[1] if full_time else None,
                "winner_id": winner_id,
            }
        )
    url = {
        "WC": "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json",
        "EC": "https://raw.githubusercontent.com/openfootball/euro.json/master/2024/euro.json",
    }[code]
    return _open_cup_payload(code=code, label=label, season=season, cohort="national-football", source_url=url, body=body, fixtures=fixtures)


def _parse_open_champions_league(body: bytes, season: str, source_url: str) -> dict | None:
    parsed = _parse_football_txt(body.decode("utf-8-sig"), "open-cl", "UEFA Champions League", season)
    fixtures = []
    for row in parsed["fixtures"]:
        stage = _cup_stage(row["round"])
        if not stage:
            continue
        home_name = re.sub(r"\s+\([A-Z]{3}\)$", "", row["home_name"]).strip()
        away_name = re.sub(r"\s+\([A-Z]{3}\)$", "", row["away_name"]).strip()
        home_id = f"football:name:{_slug(home_name)}"
        away_id = f"football:name:{_slug(away_name)}"
        home_goals, away_goals = row["home_goals"], row["away_goals"]
        winner_id = None
        if home_goals is not None and home_goals != away_goals:
            winner_id = home_id if home_goals > away_goals else away_id
        fixtures.append(
            {
                "date": row["date"],
                "stage": stage,
                "group": None,
                "status": "FINISHED" if home_goals is not None else "SCHEDULED",
                "home_id": home_id,
                "home_name": home_name,
                "away_id": away_id,
                "away_name": away_name,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "winner_id": winner_id,
            }
        )
    return _open_cup_payload(code="CL", label="UEFA Champions League", season=season, cohort="football", source_url=source_url, body=body, fixtures=fixtures)


def fetch_open_cup_schedules(cohort: str) -> list[dict]:
    """Credential-free CC0 cup snapshots used when football-data.org is unavailable."""
    if cohort == "national-football":
        rows = []
        for code, label, season, url in (
            ("WC", "FIFA World Cup", "2026", "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"),
            ("EC", "UEFA European Championship", "2024", "https://raw.githubusercontent.com/openfootball/euro.json/master/2024/euro.json"),
        ):
            try:
                body = _get(url, cache_ttl=21_600)
                schedule = _parse_open_cup_json(body, code, label, season)
            except (RuntimeError, json.JSONDecodeError):
                continue
            if schedule:
                rows.append(schedule)
        return rows
    today = datetime.now(timezone.utc).date()
    start_year = today.year if today.month >= 7 else today.year - 1
    for year in (start_year, start_year - 1):
        season = _season_label(year)
        url = f"https://raw.githubusercontent.com/openfootball/champions-league/master/{season}/cl.txt"
        try:
            body = _get(url, cache_ttl=21_600)
            schedule = _parse_open_champions_league(body, season, url)
        except RuntimeError:
            continue
        if schedule:
            return [schedule]
    return []


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


def fetch_chess_tournament_schedules(limit: int = 3) -> list[dict]:
    """Build live elite round-robin tables from official Lichess broadcasts."""
    body = _get("https://lichess.org/api/broadcast", cache_ttl=10_800)
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    schedules = []
    for line in body.decode("utf-8", "replace").splitlines():
        try:
            broadcast = json.loads(line)
        except json.JSONDecodeError:
            continue
        tour = broadcast.get("tour") or {}
        info = tour.get("info") or {}
        raw_format = str(info.get("format", ""))
        dates = tour.get("dates") or []
        if tour.get("tier", 0) < 4 or "round-robin" not in raw_format.casefold() or len(dates) != 2:
            continue
        if not dates[0] - 2 * 86_400_000 <= now_ms <= dates[1] + 2 * 86_400_000:
            continue
        event_matches: list[Match] = []
        event_entities: dict[str, dict] = {}
        snapshot = hashlib.sha256(line.encode())
        for round_info in broadcast.get("rounds", []):
            try:
                pgn = _get(
                    f"https://lichess.org/api/broadcast/round/{round_info['id']}.pgn",
                    cache_ttl=31_536_000 if round_info.get("finished") else 10_800,
                )
            except RuntimeError:
                continue
            snapshot.update(pgn)
            batch, batch_entities = _parse_broadcast_pgn(pgn.decode("utf-8", "replace"))
            event_matches.extend(batch)
            event_entities.update(batch_entities)
        event_matches = _deduplicate(event_matches)
        if len(event_entities) < 4 or not event_matches:
            continue
        name_by_id = {entity: row["name"] for entity, row in event_entities.items()}
        completed_by_pair = {frozenset((match.entity_a, match.entity_b)): match for match in event_matches}
        entity_ids = sorted(event_entities, key=lambda entity: name_by_id[entity])
        fixtures = []
        end_date = datetime.fromtimestamp(dates[1] / 1000, timezone.utc).date().isoformat()
        for index, entity_a in enumerate(entity_ids):
            for entity_b in entity_ids[index + 1:]:
                played = completed_by_pair.get(frozenset((entity_a, entity_b)))
                if played:
                    if played.entity_a == entity_a:
                        score_a = played.score_a
                    else:
                        score_a = 1.0 - played.score_a
                    fixture_date = played.date.isoformat()
                    round_name = "Played"
                else:
                    score_a = None
                    fixture_date = end_date
                    round_name = "Remaining pairing (round-robin inference)"
                fixtures.append(
                    {
                        "date": fixture_date,
                        "round": round_name,
                        "home_name": name_by_id[entity_a],
                        "away_name": name_by_id[entity_b],
                        "home_goals": score_a,
                        "away_goals": None if score_a is None else 1.0 - score_a,
                    }
                )
        schedules.append(
            {
                "id": f"chess-{tour['id']}",
                "label": tour.get("name", "Elite chess broadcast"),
                "season": str(datetime.fromtimestamp(dates[0] / 1000, timezone.utc).year),
                "format": "round-robin tournament",
                "forecast_type": "standings",
                "cohort": "chess",
                "teams": [name_by_id[entity] for entity in entity_ids],
                "fixtures": fixtures,
                "win_points": 1.0,
                "draw_points": 0.5,
                "home_advantage": False,
                "source_url": tour.get("url", "https://lichess.org/broadcast"),
                "license": "CC BY-SA 4.0",
                "snapshot_sha256": snapshot.hexdigest(),
                "forecast_available": True,
                "availability": "All unplayed pairings are inferred from the published round-robin field; future colours are treated as neutral until published.",
                "tie_break": "Points, simulated win-loss differential, then generation-time model strength; event-specific official tie-breaks are not available in the broadcast feed.",
            }
        )
        if len(schedules) >= limit:
            break
    return schedules


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
    advantage = 65.0 if football_like else 35.0 if sport == "chess" else 0.0
    bayes_advantage = 1.35 if football_like else 0.4 if sport == "chess" else 0.0
    draw_margin = 1.35 if football_like else 0.75 if sport == "chess" else 0.0
    if model_name == "elo":
        candidates = [{"k": k, "scale": 400.0, "home": advantage} for k in (16.0, 24.0, 32.0)]
    elif model_name == "glicko2":
        candidates = [
            {
                "tau": tau,
                "home": advantage,
                "period_days": 7.0,
                "initial_rating": 1500.0,
                "initial_rd": 350.0,
                "initial_volatility": 0.06,
            }
            for tau in (0.3, 0.5, 0.8)
        ]
    else:
        robust = model_name == "robust"
        candidates = [
            {"robust": robust, "beta": beta, "draw_margin": draw_margin, "advantage": bayes_advantage}
            for beta in (3.5, 25.0 / 6.0, 5.0)
        ]
    if sport == "tennis":
        return [
            {**candidate, "surface_weight": surface_weight}
            for candidate in candidates
            for surface_weight in (0.4, 0.7, 0.9)
        ]
    return candidates


def _new_model(model_name: str, params: dict, sport: str | None = None):
    parameters = dict(params)
    surface_weight = parameters.pop("surface_weight", None)
    def factory():
        if model_name == "elo":
            return EloModel(**parameters)
        if model_name == "glicko2":
            return Glicko2Model(**parameters)
        return GaussianSkillModel(**parameters)
    if sport == "tennis" and surface_weight is not None:
        return SurfaceBlendModel(factory, surface_weight)
    return factory()


def _published_score(model_name: str, state) -> float:
    if model_name == "elo":
        return state.mean
    if model_name == "glicko2":
        return state.mean - 2.0 * state.sigma
    return state.mean - 3.0 * state.sigma


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
    ordered = sorted(matches, key=_match_sort_key)
    index = 0
    while index < len(ordered):
        match = ordered[index]
        period_end = index + 1
        if isinstance(model, Glicko2Model) or getattr(model, "uses_rating_period", False):
            while period_end < len(ordered) and ordered[period_end].date == match.date:
                period_end += 1
        period = ordered[index:period_end]
        for period_match in period:
            if sport != "chess":
                continue
            for entity, key in ((period_match.entity_a, "rating_a"), (period_match.entity_b, "rating_b")):
                if entity in model.states:
                    continue
                raw_rating = period_match.metadata.get(key, "")
                if not raw_rating.isdigit() or int(raw_rating) < 1000:
                    continue
                state = model.state(entity)
                if isinstance(model, (EloModel, Glicko2Model)):
                    state.mean = float(raw_rating)
                    if isinstance(model, Glicko2Model):
                        state.variance = 100.0**2
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
        if isinstance(model, Glicko2Model) or getattr(model, "uses_rating_period", False):
            period_predictions = model.update_period(period)
        else:
            period_predictions = [model.update(match)]
        for period_match, probability in zip(period, period_predictions):
            predictions.append({"date": period_match.date.isoformat(), "predicted": probability, "actual": period_match.score_a})
        for entity in {entity for item in period for entity in (item.entity_a, item.entity_b)}:
            if history_entities is not None and entity not in history_entities:
                continue
            state = model.states[entity]
            rating = _published_score(model.name, state)
            series = histories[entity]
            point = [match.date.isoformat(), round(rating, 2)]
            if series and series[-1][0] == point[0]:
                series[-1] = point
            else:
                series.append(point)
        previous_season = period[-1].season or previous_season
        index = period_end
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
            _new_model(model_name, params, sport),
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
    win_points = float(competition.get("win_points", 3.0))
    draw_points = float(competition.get("draw_points", 1.0))
    use_home_advantage = bool(competition.get("home_advantage", True))
    index_by_name = {name: index for index, name in enumerate(names)}
    entity_by_name = {_slug(info.get("name", "")): entity for entity, info in entities.items()}
    entity_ids = [entity_by_name.get(_slug(name), f"football:name:{_slug(name)}") for name in names]
    strengths = []
    for entity in entity_ids:
        state = model.state(entity)
        strengths.append(state.mean)

    base_points = [0.0] * team_count
    base_goal_difference = [0.0] * team_count
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
                base_points[home_index] += win_points
            elif home_goals < away_goals:
                base_points[away_index] += win_points
            else:
                base_points[home_index] += draw_points
                base_points[away_index] += draw_points
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
            use_home_advantage,
        )
        if isinstance(model, (EloModel, Glicko2Model)):
            probabilities = model.predict_outcomes(future_match, historical_draw_rate)
        else:
            probabilities = model.predict_outcomes(future_match)
        remaining.append((home_index, away_index, probabilities))

    def order(points: list[float], goal_difference: list[float]) -> list[int]:
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
                points[home_index] += win_points
                margin_roll = generator.random()
                margin = 1 if win_points == 1.0 else 1 if margin_roll < 0.64 else 2 if margin_roll < 0.92 else 3
                goal_difference[home_index] += margin
                goal_difference[away_index] -= margin
            elif outcome < home_win + draw:
                points[home_index] += draw_points
                points[away_index] += draw_points
            else:
                points[away_index] += win_points
                margin_roll = generator.random()
                margin = 1 if win_points == 1.0 else 1 if margin_roll < 0.64 else 2 if margin_roll < 0.92 else 3
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
                "podium": round(sum(position_probabilities[:3]), 4),
                "last_place": round(position_probabilities[-1], 4),
                "positions": [round(probability, 4) for probability in position_probabilities],
            }
        )
    teams.sort(key=lambda team: (team["expected_position"], team["name"]))
    return {
        "forecast_type": competition.get("forecast_type", "league"),
        "seed": f"{seed:016x}",
        "simulations": simulations,
        "completed_matches": completed,
        "remaining_matches": len(remaining),
        "latest_completed": latest_completed,
        "teams": teams,
    }


def _decisive_probability(model, entity_a: str, entity_b: str) -> float:
    """Convert a neutral 90-minute W/D/L forecast into a decisive tie probability."""
    match = Match(date.today(), entity_a, entity_b, 0.5, home_advantage=False)
    home_win, _draw, away_win = model.predict_outcomes(match)
    decisive = home_win + away_win
    return home_win / decisive if decisive else 0.5


def _resolved_knockout_ties(competition: dict) -> tuple[set[str], dict[tuple[int, tuple[str, str]], list[dict]]]:
    grouped: dict[tuple[int, tuple[str, str]], list[dict]] = defaultdict(list)
    for fixture in competition["knockout_fixtures"]:
        stage_rank = KNOCKOUT_STAGES[fixture["stage"]]
        pair = tuple(sorted((fixture["home_id"], fixture["away_id"])))
        grouped[(stage_rank, pair)].append(fixture)
    eliminated: set[str] = set()
    cohort = competition.get("cohort")
    for (_stage_rank, pair), fixtures in grouped.items():
        finished = [row for row in fixtures if row["status"] == "FINISHED" and row["winner_id"]]
        if len(finished) != len(fixtures):
            continue
        winner = None
        if cohort == "national-football" or fixtures[0]["stage"] == "FINAL":
            winner = finished[-1]["winner_id"] if finished else None
        elif len(fixtures) >= 2:
            goals = {pair[0]: 0, pair[1]: 0}
            for row in finished:
                goals[row["home_id"]] += row["home_goals"] or 0
                goals[row["away_id"]] += row["away_goals"] or 0
            if goals[pair[0]] != goals[pair[1]]:
                winner = pair[0] if goals[pair[0]] > goals[pair[1]] else pair[1]
            else:
                winner = finished[-1]["winner_id"]
        if winner:
            eliminated.add(pair[1] if winner == pair[0] else pair[0])
    return eliminated, grouped


def _simulate_knockout(competition: dict, model, model_name: str, simulations: int = PREDICTOR_SIMULATIONS) -> dict:
    """Forecast a published knockout field and explicitly sample later unpublished draws."""
    names = {team["id"]: team["name"] for team in competition["teams"]}
    eliminated, grouped = _resolved_knockout_ties(competition)
    participants = {
        entity
        for fixture in competition["knockout_fixtures"]
        for entity in (fixture["home_id"], fixture["away_id"])
    }
    survivors = sorted(participants - eliminated)
    final = next(
        (row for row in competition["knockout_fixtures"] if row["stage"] == "FINAL" and row["status"] == "FINISHED" and row["winner_id"]),
        None,
    )
    seed_material = f"{METHODOLOGY_VERSION}|{competition['id']}|{competition['season']}|{model_name}|knockout"
    seed = int.from_bytes(hashlib.sha256(seed_material.encode()).digest()[:8], "big")
    if final:
        champion_counts = {entity: simulations if entity == final["winner_id"] else 0 for entity in participants}
        next_counts = {entity: simulations if entity == final["winner_id"] else 0 for entity in participants}
        current_stage = "complete"
        unresolved_pairs: list[tuple[str, str]] = []
    else:
        unresolved_by_stage: dict[int, list[tuple[str, str]]] = defaultdict(list)
        for (stage_rank, pair), fixtures in grouped.items():
            tie_eliminated = set(pair) & eliminated
            if not tie_eliminated and any(row["status"] != "FINISHED" for row in fixtures):
                unresolved_by_stage[stage_rank].append(pair)
        active_rank = min(unresolved_by_stage) if unresolved_by_stage else None
        unresolved_pairs = sorted(set(unresolved_by_stage.get(active_rank, [])))
        current_stage = next(
            (stage for stage, rank in KNOCKOUT_STAGES.items() if rank == active_rank),
            "draw pending",
        )
        champion_counts = {entity: 0 for entity in participants}
        next_counts = {entity: 0 for entity in participants}
        generator = random.Random(seed)
        for _ in range(simulations):
            field = set(survivors)
            advanced: list[str] = []
            paired: set[str] = set()
            for entity_a, entity_b in unresolved_pairs:
                if entity_a not in field or entity_b not in field:
                    continue
                paired.update((entity_a, entity_b))
                probability = _decisive_probability(model, entity_a, entity_b)
                winner = entity_a if generator.random() < probability else entity_b
                advanced.append(winner)
                next_counts[winner] += 1
            for entity in sorted(field - paired):
                advanced.append(entity)
                next_counts[entity] += 1
            while len(advanced) > 1:
                generator.shuffle(advanced)
                next_round = []
                if len(advanced) % 2:
                    next_round.append(advanced.pop())
                for index in range(0, len(advanced), 2):
                    entity_a, entity_b = advanced[index], advanced[index + 1]
                    probability = _decisive_probability(model, entity_a, entity_b)
                    next_round.append(entity_a if generator.random() < probability else entity_b)
                advanced = next_round
            if advanced:
                champion_counts[advanced[0]] += 1
    rows = []
    for entity in participants:
        state = model.state(entity)
        rows.append(
            {
                "id": entity,
                "name": names.get(entity, entity),
                "rating": round(state.mean, 2),
                "champion": round(champion_counts[entity] / simulations, 4),
                "reach_next_stage": round(next_counts[entity] / simulations, 4),
            }
        )
    rows.sort(key=lambda row: (-row["champion"], -row["rating"], row["name"]))
    return {
        "forecast_type": "knockout",
        "seed": f"{seed:016x}",
        "simulations": simulations,
        "current_stage": current_stage.replace("_", " ").title(),
        "published_ties_remaining": len(unresolved_pairs),
        "participants": rows,
    }


def _model_parameters(model) -> dict:
    if isinstance(model, SurfaceBlendModel):
        return {
            **_model_parameters(model.global_model),
            "surface_weight": model.surface_weight,
        }
    if isinstance(model, EloModel):
        return {"k": model.k, "scale": model.scale, "home": model.home}
    if isinstance(model, Glicko2Model):
        return {
            "tau": model.tau,
            "initial_rating": model.initial_rating,
            "initial_rd": model.initial_rd,
            "initial_volatility": model.initial_volatility,
            "home": model.home,
            "period_days": model.period_days,
        }
    return {
        "robust": model.robust,
        "beta": model.beta,
        "draw_margin": model.draw_margin,
        "advantage": model.advantage,
    }


def _competition_matches(schedule: dict, entities: dict) -> list[Match]:
    """Convert completed schedule rows into protocol-ready event results."""
    cohort = schedule.get("cohort", "football")
    entity_by_name = {_slug(info.get("name", "")): entity for entity, info in entities.items()}
    use_advantage = bool(schedule.get("home_advantage", cohort == "football"))
    results = []
    for fixture in schedule["fixtures"]:
        if fixture.get("home_goals") is None or fixture.get("away_goals") is None or not fixture.get("date"):
            continue
        home_slug = _slug(fixture["home_name"])
        away_slug = _slug(fixture["away_name"])
        aliases = SCHEDULE_ENTITY_ALIASES.get(cohort, {})
        home = entity_by_name.get(home_slug) or entity_by_name.get(aliases.get(home_slug, "")) or fixture.get("home_id")
        away = entity_by_name.get(away_slug) or entity_by_name.get(aliases.get(away_slug, "")) or fixture.get("away_id")
        if not home or not away or home == away:
            continue
        home_score, away_score = fixture["home_goals"], fixture["away_goals"]
        result = 1.0 if home_score > away_score else 0.0 if home_score < away_score else 0.5
        results.append(
            Match(
                date.fromisoformat(fixture["date"]),
                home,
                away,
                result,
                schedule["label"],
                schedule["season"],
                use_advantage,
            )
        )
    return sorted(_deduplicate(results), key=_match_sort_key)


def _competition_performance(
    schedule: dict,
    reference_model,
    model_name: str,
    entities: dict,
    matches: list[Match],
) -> dict | None:
    """Replay a completed event from its strictly pre-event rating state."""
    event_matches = _competition_matches(schedule, entities)
    if not event_matches:
        return None
    sport = schedule.get("cohort", "football")
    first_result = event_matches[0].date
    prior_matches = [match for match in matches if match.date < first_result]
    parameters = _model_parameters(reference_model)
    prior_model = _new_model(model_name, parameters, sport)
    _run_model(prior_matches, prior_model, sport, history_entities=set())
    event_model = _new_model(model_name, parameters, sport)
    participants = sorted({entity for match in event_matches for entity in (match.entity_a, match.entity_b)})
    event_names = {}
    entity_by_name = {_slug(info.get("name", "")): entity for entity, info in entities.items()}
    aliases = SCHEDULE_ENTITY_ALIASES.get(sport, {})
    for fixture in schedule["fixtures"]:
        for side in ("home", "away"):
            name = fixture.get(f"{side}_name", "")
            slug = _slug(name)
            entity = entity_by_name.get(slug) or entity_by_name.get(aliases.get(slug, "")) or fixture.get(f"{side}_id")
            if entity and name:
                event_names[entity] = name
    for entity in participants:
        source = prior_model.state(entity)
        target = event_model.state(entity)
        target.mean = source.mean
        target.variance = source.variance
        target.matches = source.matches
        target.last_played = source.last_played
        target.volatility = source.volatility
    previous_season = next((match.season for match in reversed(prior_matches) if match.season), None)
    if sport == "football" and isinstance(event_model, EloModel) and previous_season and previous_season != schedule["season"]:
        event_model.regress(0.25)
    starts = {
        entity: (event_model.state(entity).mean, event_model.state(entity).sigma, event_model.state(entity).volatility)
        for entity in participants
    }
    records = defaultdict(
        lambda: {
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "points": 0.0,
            "expected_score": 0.0,
            "expectation_variance": 0.0,
            "matches": 0,
        }
    )
    event_index = 0
    while event_index < len(event_matches):
        match = event_matches[event_index]
        event_period_end = event_index + 1
        period_matches = event_matches[event_index:event_period_end]
        if isinstance(event_model, Glicko2Model):
            while event_period_end < len(event_matches) and event_matches[event_period_end].date == match.date:
                event_period_end += 1
            period_matches = event_matches[event_index:event_period_end]
            predictions = event_model.update_period(period_matches)
        else:
            predictions = [event_model.update(match)]
        for match, prediction_a in zip(period_matches, predictions):
            # This common score-scale variance reference makes surprise
            # comparable across protocols while completed draws keep score 0.5.
            variance_reference = max(prediction_a * (1.0 - prediction_a), 1e-9)
            for entity, score, expected in (
                (match.entity_a, match.score_a, prediction_a),
                (match.entity_b, 1.0 - match.score_a, 1.0 - prediction_a),
            ):
                record = records[entity]
                record["matches"] += 1
                record["points"] += score
                record["expected_score"] += expected
                record["expectation_variance"] += variance_reference
                if score == 1.0:
                    record["wins"] += 1
                elif score == 0.5:
                    record["draws"] += 1
                else:
                    record["losses"] += 1
        event_index = event_period_end
    rows = []
    for entity in participants:
        start_mean, start_sigma, start_volatility = starts[entity]
        end = event_model.state(entity)
        start_score = (
            start_mean if model_name == "elo"
            else start_mean - 2.0 * start_sigma if model_name == "glicko2"
            else start_mean - 3.0 * start_sigma
        )
        end_score = _published_score(model_name, end)
        record = records[entity]
        score_residual = record["points"] - record["expected_score"]
        surprise_index = score_residual / math.sqrt(record["expectation_variance"])
        rows.append(
            {
                "id": entity,
                "name": entities.get(entity, {}).get("name") or event_names.get(entity, entity),
                "start_rating": round(start_mean, 2),
                "start_sigma": round(start_sigma, 2) if model_name != "elo" else None,
                "start_volatility": round(start_volatility, 6) if model_name == "glicko2" else None,
                "start_score": round(start_score, 2),
                "end_rating": round(end.mean, 2),
                "end_sigma": round(end.sigma, 2) if model_name != "elo" else None,
                "end_volatility": round(end.volatility, 6) if model_name == "glicko2" else None,
                "performance_rating": round(end_score, 2),
                "change": round(end_score - start_score, 2),
                "matches": record["matches"],
                "wins": record["wins"],
                "draws": record["draws"],
                "losses": record["losses"],
                "points": round(record["points"], 2),
                "expected_score": round(record["expected_score"], 4),
                "score_residual": round(score_residual, 4),
                "residual_per_match": round(score_residual / record["matches"], 4),
                "expectation_variance": round(record["expectation_variance"], 6),
                "surprise_index": round(surprise_index, 4),
                "score_rate": round(record["points"] / record["matches"], 4),
            }
        )
    rows.sort(key=lambda row: (-row["performance_rating"], -row["change"], row["name"]))
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
    return {
        "rating_type": "elo" if model_name == "elo" else "glicko2_conservative_r_minus_2rd" if model_name == "glicko2" else "conservative_mu_minus_3_sigma",
        "results": len(event_matches),
        "first_result": event_matches[0].date.isoformat(),
        "last_result": event_matches[-1].date.isoformat(),
        "surprise_method": "For every result, record the selected protocol's expected score immediately before its update. Actual score minus expected score is the signed residual. Divide the cumulative residual by sqrt(sum p(1-p)) to obtain the displayed standardized surprise; draws keep score 0.5, and p(1-p) is the disclosed common Bernoulli-score variance reference.",
        "participants": rows,
    }


def _as_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _json_array(value) -> list:
    if isinstance(value, list):
        return value
    if not isinstance(value, str):
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def _market_identity_tokens(name: str) -> frozenset[str]:
    ignored = {"fc", "cf", "afc", "sc", "ac", "club"}
    return frozenset(token for token in _slug(name).split("-") if token and token not in ignored)


def _competition_participants(competition: dict) -> list[dict]:
    model = competition.get("models", {}).get("elo", {})
    return model.get("teams") or model.get("participants") or []


def _polymarket_event_snapshot(competition: dict, event: dict) -> dict | None:
    participants = _competition_participants(competition)
    if len(participants) < 2 or not event.get("markets"):
        return None
    participant_tokens = [(_market_identity_tokens(row["name"]), row) for row in participants]
    valid_markets = []
    for market in event["markets"]:
        outcomes = _json_array(market.get("outcomes"))
        prices = _json_array(market.get("outcomePrices"))
        yes_index = next((index for index, outcome in enumerate(outcomes) if str(outcome).casefold() == "yes"), None)
        if yes_index is None or yes_index >= len(prices) or market.get("closed") is True or market.get("active") is False:
            continue
        liquidity = _as_float(market.get("liquidity"))
        volume = _as_float(market.get("volume"))
        if liquidity <= 0 and volume <= 0:
            continue
        price = _as_float(prices[yes_index], -1)
        if not 0 <= price <= 1:
            continue
        title = str(market.get("groupItemTitle") or market.get("question") or "").strip()
        tokens = _market_identity_tokens(title)
        if not tokens:
            continue
        valid_markets.append((market, title, tokens, price, liquidity, volume))
    raw_sum = sum(item[3] for item in valid_markets)
    if raw_sum <= 0:
        return None
    matched = []
    used_entities = set()
    for market, market_title, tokens, price, liquidity, volume in valid_markets:
        exact = [row for candidate, row in participant_tokens if candidate == tokens]
        candidates = exact or [
            row for candidate, row in participant_tokens
            if tokens.issubset(candidate) or candidate.issubset(tokens)
        ]
        candidates = [row for row in candidates if row["id"] not in used_entities]
        if len(candidates) != 1:
            continue
        participant = candidates[0]
        used_entities.add(participant["id"])
        matched.append(
            {
                "entity_id": participant["id"],
                "name": participant["name"],
                "market_id": str(market.get("id", "")),
                "market_slug": market.get("slug"),
                "market_label": market_title,
                "raw_yes_price": round(price, 6),
                "normalized_probability": round(price / raw_sum, 6),
                "best_bid": round(_as_float(market.get("bestBid")), 6),
                "best_ask": round(_as_float(market.get("bestAsk")), 6),
                "liquidity_usd": round(liquidity, 2),
                "volume_usd": round(volume, 2),
                "updated_at": market.get("updatedAt"),
            }
        )
    coverage = len(matched) / len(participants)
    if len(matched) < 2 or coverage < 0.5:
        return None
    matched.sort(key=lambda row: (-row["normalized_probability"], row["name"]))
    snapshot_material = json.dumps(
        [(row["market_id"], row["raw_yes_price"], row["updated_at"]) for row in matched],
        separators=(",", ":"),
    )
    return {
        "competition_id": competition["id"],
        "event_id": str(event.get("id", "")),
        "event_title": event.get("title"),
        "event_slug": event.get("slug"),
        "event_url": f"https://polymarket.com/event/{event.get('slug')}",
        "event_updated_at": event.get("updatedAt"),
        "event_liquidity_usd": round(_as_float(event.get("liquidity")), 2),
        "event_volume_usd": round(_as_float(event.get("volume")), 2),
        "raw_yes_price_sum": round(raw_sum, 6),
        "normalization": "Each active liquid binary winner market's Yes price divided by the sum of Yes prices across all active liquid outcomes in the matched event.",
        "matched_participants": len(matched),
        "model_participants": len(participants),
        "market_outcomes": len(valid_markets),
        "coverage": round(coverage, 4),
        "snapshot_sha256": hashlib.sha256(snapshot_material.encode()).hexdigest(),
        "outcomes": matched,
    }


def _polymarket_search_query(competition: dict) -> str:
    season = str(competition.get("season", ""))
    if "-" in season and len(season.rsplit("-", 1)[-1]) == 2:
        century = season.split("-", 1)[0][:2]
        year = century + season.rsplit("-", 1)[-1]
    else:
        year = season
    suffix = "winner" if "chess" in competition["id"] else "champion"
    return " ".join(part for part in (competition["label"], year, suffix) if part)


def fetch_polymarket_comparison(competitions: list[dict]) -> dict:
    """Fetch public winner markets and match them conservatively to our fields."""
    eligible = [competition for competition in competitions if competition.get("status") in {"live", "scheduled"}]
    fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    snapshots = []
    searches = []
    failures = 0
    for competition in eligible:
        query = _polymarket_search_query(competition)
        api_url = "https://gamma-api.polymarket.com/public-search?" + urlencode(
            {
                "q": query,
                "events_status": "active",
                "limit_per_type": 10,
                "search_profiles": "false",
            }
        )
        try:
            payload = json.loads(_get(api_url, attempts=3, cache_ttl=1800).decode("utf-8"))
        except (RuntimeError, json.JSONDecodeError):
            failures += 1
            searches.append({"competition_id": competition["id"], "query": query, "status": "source_error"})
            continue
        candidates = []
        for event in payload.get("events") or []:
            if event.get("closed") is True or event.get("active") is False:
                continue
            snapshot = _polymarket_event_snapshot(competition, event)
            if snapshot:
                candidates.append(snapshot)
        if candidates:
            candidates.sort(key=lambda row: (-row["matched_participants"], -row["coverage"], -row["event_liquidity_usd"]))
            snapshots.append(candidates[0])
            searches.append({"competition_id": competition["id"], "query": query, "status": "matched", "event_id": candidates[0]["event_id"]})
        else:
            searches.append({"competition_id": competition["id"], "query": query, "status": "no_confident_match"})
    if eligible and failures == len(eligible):
        raise RuntimeError("Polymarket Gamma API was unavailable for every eligible competition")
    return {
        "status": "current",
        "source": "Polymarket Gamma API",
        "source_url": "https://docs.polymarket.com/market-data/overview",
        "api_base": "https://gamma-api.polymarket.com",
        "fetched_at": fetched_at,
        "checked_at": fetched_at,
        "stale_after_hours": 48,
        "probability_definition": "Public Gamma outcomePrices Yes values, normalized across active liquid mutually exclusive winner markets; these are a market benchmark and never a rating-model input.",
        "competitions": snapshots,
        "searches": searches,
    }


def _attach_polymarket_comparison(payload: dict, previous: dict | None) -> None:
    predictor = payload.get("tournament_predictor")
    if not predictor:
        return
    try:
        predictor["market_comparison"] = fetch_polymarket_comparison(predictor["competitions"])
    except RuntimeError as error:
        retained = (previous or {}).get("tournament_predictor", {}).get("market_comparison")
        if retained:
            retained = json.loads(json.dumps(retained))
            retained["status"] = "retained"
            retained["checked_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            retained["message"] = str(error)[:240]
            predictor["market_comparison"] = retained
        else:
            checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            predictor["market_comparison"] = {
                "status": "unavailable",
                "source": "Polymarket Gamma API",
                "source_url": "https://docs.polymarket.com/market-data/overview",
                "api_base": "https://gamma-api.polymarket.com",
                "fetched_at": None,
                "checked_at": checked_at,
                "stale_after_hours": 48,
                "probability_definition": "No market snapshot was available; rating forecasts remain independent.",
                "competitions": [],
                "searches": [],
                "message": str(error)[:240],
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
        competition = {key: schedule[key] for key in ("id", "label", "season", "source_url", "license", "snapshot_sha256")}
        competition["format"] = schedule.get("format", "round-robin league")
        competition["forecast_available"] = schedule.get("forecast_available", True)
        competition["availability"] = schedule.get(
            "availability",
            "The complete round-robin fixture list is published and forecastable.",
        )
        competition["tie_break"] = schedule.get("tie_break")
        competition["total_matches"] = len(schedule["fixtures"])
        competition["first_fixture"] = schedule.get("first_fixture") or min(row["date"] for row in schedule["fixtures"])
        competition["last_fixture"] = schedule.get("last_fixture") or max(row["date"] for row in schedule["fixtures"])
        unplayed_dates = [row["date"] for row in schedule["fixtures"] if row["home_goals"] is None and row["date"]]
        competition["next_fixture"] = min(unplayed_dates) if unplayed_dates else None
        if competition["format"] in {"round-robin league", "round-robin tournament"}:
            competition["models"] = {
                model_name: _simulate_league(schedule, model, model_name, entities, draw_rate)
                for model_name, model in models.items()
            }
            completed = competition["models"]["elo"]["completed_matches"]
            competition["status"] = "scheduled" if completed == 0 else "complete" if completed == competition["total_matches"] else "live"
        elif competition["forecast_available"]:
            competition["models"] = {
                model_name: _simulate_knockout(schedule, model, model_name)
                for model_name, model in models.items()
            }
            competition["status"] = "complete" if competition["models"]["elo"]["current_stage"] == "Complete" else "live"
        else:
            competition["models"] = {}
            competition["status"] = "waiting for draw"
        if competition["status"] == "complete":
            performance_models = {
                model_name: _competition_performance(schedule, model, model_name, entities, matches)
                for model_name, model in models.items()
            }
            if all(performance_models.values()):
                competition["performance"] = {
                    "method": "Initialize every participant from the global rating state after all source results strictly before the first event date, replay only completed event results in deterministic protocol order, record each selected protocol's pre-update expectation, and publish final Elo, Glicko-2 rating−2RD, or Gaussian μ−3σ with its change from the event start.",
                    "models": performance_models,
                }
        competitions.append(competition)
    return {
        "format": "format-aware competition forecast",
        "simulations_per_model": PREDICTOR_SIMULATIONS,
        "draw_model": "Gaussian models use their fitted draw likelihood; Elo and Glicko-2 allocate the historical draw rate by matchup closeness while preserving expected score.",
        "tie_break": "Points, simulated goal difference, then current model strength.",
        "strengths": "Fixed at the generation-time rating state; completed results change both the table and the next refresh's ratings.",
        "knockout_draw": "Published ties are preserved. If a later cup draw is not published, surviving teams are uniformly re-drawn in each simulation; known byes are preserved. Draw constraints are not invented.",
        "availability_rule": "Title probabilities are withheld until a public knockout field exists.",
        "performance_method": "Completed competitions publish protocol performance ratings instead of retrospective title probabilities.",
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
    outcome_matches = [
        match for match in matches
        if match.entity_a in history_entities and match.entity_b in history_entities
    ] or matches
    model_payloads = {}
    selected_parameters = {}
    fitted_models = {}
    for model_name in MODEL_NAMES:
        params = _choose_parameters(matches, sport, model_name, validation_start, evaluation_start)
        selected_parameters[model_name] = params
        fitted_model = _new_model(model_name, params, sport)
        states, predictions, histories = _run_model(
            matches,
            fitted_model,
            sport,
            history_entities=history_entities,
        )
        if isinstance(fitted_model, Glicko2Model) or getattr(fitted_model, "uses_rating_period", False):
            fitted_model.age_to(latest)
            for entity in history_entities:
                if entity not in states:
                    continue
                point = [latest.isoformat(), round(_published_score(model_name, states[entity]), 2)]
                series = histories[entity]
                if series and series[-1][0] == point[0]:
                    series[-1] = point
                else:
                    series.append(point)
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
            conservative = _published_score(model_name, state)
            full_history = histories.get(entity, [])
            cutoff_point = next((point[1] for point in reversed(full_history) if date.fromisoformat(point[0]) <= latest - timedelta(days=30)), full_history[0][1] if full_history else conservative)
            history = _compress_history(full_history)
            row = {
                    "id": entity,
                    "name": entities[entity]["name"],
                    "country": entities[entity].get("country", ""),
                    "competition": entities[entity].get("competition", ""),
                    "rating": round(state.mean, 2),
                    "sigma": round(state.sigma, 2) if model_name != "elo" else None,
                    "volatility": round(state.volatility, 6) if model_name == "glicko2" else None,
                    "score": round(conservative, 2),
                    "change30": round(conservative - cutoff_point, 2),
                    "matches": state.matches,
                    "recent_matches": recent_counts[entity],
                    "last_played": state.last_played.isoformat() if state.last_played else None,
                    "history": history,
                }
            if isinstance(fitted_model, SurfaceBlendModel):
                row["contexts"] = {}
                for surface, surface_model in sorted(fitted_model.surface_models.items()):
                    surface_state = surface_model.states.get(entity)
                    if not surface_state or not surface_state.matches:
                        continue
                    row["contexts"][surface] = {
                        "rating": round(surface_state.mean, 2),
                        "sigma": round(surface_state.sigma, 2) if model_name != "elo" else None,
                        "volatility": round(surface_state.volatility, 6) if model_name == "glicko2" else None,
                        "score": round(_published_score(model_name, surface_state), 2),
                        "matches": surface_state.matches,
                        "last_played": surface_state.last_played.isoformat() if surface_state.last_played else None,
                    }
            rows.append(row)
        rows.sort(key=lambda row: (-row["score"], row["name"]))
        rows = rows[:500]
        for rank, row in enumerate(rows, 1):
            row["rank"] = rank
        model_payloads[model_name] = {
            "label": {"elo": "Elo", "glicko2": "Glicko-2", "trueskill": "Gaussian TrueSkill", "robust": "Robust TrueSkill"}[model_name],
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
        "outcome_context": {
            "draw_rate": round(sum(match.score_a == 0.5 for match in outcome_matches) / len(outcome_matches), 6),
            "draws": sum(match.score_a == 0.5 for match in outcome_matches),
            "matches": len(outcome_matches),
            "method": "Completed draws divided by deduplicated replay results where both competitors satisfy the current publication eligibility rules.",
        },
        "prediction_contexts": {
            "tennis": {
                "type": "surface",
                "values": [
                    {"id": surface, "label": surface.title()}
                    for surface in ("hard", "clay", "grass", "carpet")
                    if any(SurfaceBlendModel.surface(match) == surface for match in matches)
                ],
                "method": "Blend the global player belief with an independently replayed surface belief. The selected validation weight is multiplied by min((surface matches A + surface matches B) / 20, 1).",
            },
            "football": {
                "type": "venue",
                "values": [{"id": "a", "label": "A at home"}, {"id": "neutral", "label": "Neutral"}, {"id": "b", "label": "B at home"}],
                "method": "Apply the selected home offset to the listed home side before predicting and updating.",
            },
            "national-football": {
                "type": "venue",
                "values": [{"id": "a", "label": "A at home"}, {"id": "neutral", "label": "Neutral"}, {"id": "b", "label": "B at home"}],
                "method": "Apply the selected home offset only when the source does not mark the match neutral.",
            },
            "chess": {
                "type": "color",
                "values": [{"id": "a", "label": "A is White"}, {"id": "b", "label": "B is White"}, {"id": "neutral", "label": "Color unassigned"}],
                "method": "PGN games are White-first. Apply the declared White offset before predicting and updating.",
            },
        }[sport],
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
            name: _model_candidates(sport, name) for name in MODEL_NAMES
        },
        "parameters": selected_parameters,
        "models": model_payloads,
    }
    if sport in {"football", "national-football", "chess"} and predictor_schedules:
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
    context = payload["outcome_context"]
    if not isinstance(context.get("matches"), int) or not 1 <= context["matches"] <= window["matches"]:
        raise ValueError("Outcome context sample is outside the data window")
    if not 0 <= context.get("draw_rate", -1) <= 1:
        raise ValueError("Invalid empirical draw rate")
    eligibility = payload["eligibility"]
    if not isinstance(eligibility.get("minimum_recent_matches"), int):
        raise ValueError("Invalid eligibility minimum")
    if not isinstance(eligibility.get("recent_window_days"), int):
        raise ValueError("Invalid eligibility window")
    if payload["sport"] == "football":
        predictor = payload.get("tournament_predictor")
        if not predictor or not predictor.get("competitions"):
            raise ValueError("Missing football tournament predictor")
    predictor = payload.get("tournament_predictor")
    if predictor:
        for competition in predictor["competitions"]:
            if competition.get("forecast_available") and set(competition.get("models", {})) != set(MODEL_NAMES):
                raise ValueError("Incomplete tournament prediction models")
            if competition.get("status") == "complete":
                performance = competition.get("performance", {}).get("models", {})
                if set(performance) != set(MODEL_NAMES):
                    raise ValueError("Completed competition is missing protocol performance ratings")
        market = predictor.get("market_comparison")
        if market:
            if market.get("status") not in {"current", "retained", "unavailable"}:
                raise ValueError("Invalid market comparison status")
            for competition in market.get("competitions", []):
                if competition.get("raw_yes_price_sum", 0) <= 0:
                    raise ValueError("Invalid Polymarket outcome-price sum")
                entity_ids = [row.get("entity_id") for row in competition.get("outcomes", [])]
                if len(entity_ids) != len(set(entity_ids)):
                    raise ValueError("Duplicate Polymarket participant match")
                if any(not 0 <= row.get("normalized_probability", -1) <= 1 for row in competition.get("outcomes", [])):
                    raise ValueError("Invalid normalized Polymarket probability")
    for name in MODEL_NAMES:
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
                existing = output_dir / f"{sport}.json"
                previous_payload = json.loads(existing.read_text()) if existing.exists() else None
                matches, entities, source_meta = loaders[sport]()
                predictor_schedules = None
                if sport == "football":
                    league_schedules = fetch_league_schedules()
                    predictor_schedules = league_schedules + fetch_cup_schedules(token, sport, matches)
                    matches = _merge_schedule_results(matches, entities, league_schedules)
                elif sport == "national-football":
                    predictor_schedules = fetch_cup_schedules(token, sport, matches)
                elif sport == "chess":
                    predictor_schedules = fetch_chess_tournament_schedules()
                payload = build_sport_payload(
                    sport,
                    matches,
                    entities,
                    source_meta,
                    predictor_schedules=predictor_schedules,
                )
                _attach_polymarket_comparison(payload, previous_payload)
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
        "models": list(MODEL_NAMES),
        "replay": {
            "order": ["date", "entity_a", "entity_b", "competition", "score_a"],
            "validation_days": 365,
            "evaluation_days": 365,
            "quadrature_nodes": 20,
            "robust_student_t_degrees_of_freedom": 1,
            "glicko2_rating_period": "All results on one UTC calendar date are updated simultaneously.",
            "glicko2_inactivity_period_days": 7,
            "glicko2_publication_score": "rating - 2 * rating deviation",
            "trueskill2_claim": "Not used: the public sports sources do not provide the experience, squad, individual-performance, quitting, or cross-mode observations required by the published TrueSkill 2 model.",
            "competitive_context": {
                "tennis": "Global and surface-specific beliefs are replayed together. Prediction weight = selected surface_weight * min((surface matches A + surface matches B) / 20, 1).",
                "football": "The listed home side receives the model's declared home offset; source-marked neutral national matches do not.",
                "chess": "PGN entity A is White and receives the declared White offset before every prediction and update.",
            },
        },
        "tournament_predictor": {
            "simulations_per_competition_model": PREDICTOR_SIMULATIONS,
            "seed": "SHA-256(methodology version, competition, season, model), first 64 bits as hexadecimal",
            "formats": ["round-robin league", "round-robin tournament", "group + knockout", "knockout cup"],
            "unpublished_draws": "Uniform random redraw among surviving teams; published ties and byes are locked.",
            "availability": "Withhold title probabilities until the public source identifies a knockout field.",
            "completed_competitions": "Replace retrospective title odds with competition-only protocol performance ratings initialized from the strictly pre-event state.",
            "market_benchmark": "Polymarket Gamma Yes outcomePrices, normalized across active liquid mutually exclusive winner markets; comparison only and never a model input.",
            "market_quality_fields": ["raw_yes_price_sum", "coverage", "best_bid", "best_ask", "liquidity_usd", "volume_usd", "updated_at"],
            "refresh": "daily",
        },
        "individual_contribution": individual_contribution_protocol(),
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
