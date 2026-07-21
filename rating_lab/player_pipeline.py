"""Build reproducible historical football-player ratings from StatsBomb lineups."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Callable

from .player_models import LineupTrueSkill, multiclass_brier, multiclass_log_loss


PLAYER_SCHEMA_VERSION = "1.0.0"
STATSBOMB_ROOT = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COHORTS = (
    {
        "id": "liga-f-2023-24",
        "competition_id": 182,
        "season_id": 281,
        "name": "Liga F 2023/24",
        "country": "Spain",
    },
    {
        "id": "wsl-2023-24",
        "competition_id": 37,
        "season_id": 281,
        "name": "FA Women's Super League 2023/24",
        "country": "England",
    },
)
RIDGE_CANDIDATES = (1.0, 5.0, 20.0, 50.0)
MIN_MINUTES = 450.0
MIN_MATCHES = 5


def _clock(value: str | None) -> float | None:
    if not value:
        return None
    parts = value.split(":")
    try:
        return float(parts[0]) + float(parts[1]) / 60.0
    except (IndexError, ValueError):
        return None


def _match_duration(match: dict, lineups: list[dict]) -> float:
    observed = [
        clock
        for team in lineups
        for player in team.get("lineup", [])
        for position in player.get("positions", [])
        for clock in (_clock(position.get("from")), _clock(position.get("to")))
        if clock is not None
    ]
    maximum = max(observed, default=90.0)
    stage = match.get("competition_stage", {}).get("name", "")
    knockout = stage not in {"Regular Season", "Group Stage"}
    if maximum > 100.0 or (knockout and match.get("home_score") == match.get("away_score")):
        return max(120.0, maximum)
    return max(90.0, maximum)


def _merge_minutes(positions: list[dict], duration: float) -> tuple[float, bool, bool]:
    intervals: list[tuple[float, float]] = []
    starts = False
    complete = True
    for position in positions:
        start = _clock(position.get("from"))
        end = _clock(position.get("to"))
        if start is None:
            complete = False
            continue
        if start <= 0.01:
            starts = True
        if end is None:
            if position.get("end_reason") == "Final Whistle" or position.get("to_period") is None:
                end = duration
            else:
                complete = False
                continue
        start = min(max(start, 0.0), duration)
        end = min(max(end, start), duration)
        intervals.append((start, end))
    intervals.sort()
    merged: list[list[float]] = []
    for start, end in intervals:
        if merged and start <= merged[-1][1] + 0.02:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return sum(end - start for start, end in merged), starts, complete and bool(intervals)


def _lineup_weights(
    match: dict, lineups: list[dict], player_meta: dict[str, dict]
) -> tuple[dict[str, float], dict[str, float], dict]:
    duration = _match_duration(match, lineups)
    by_team: dict[int, dict[str, float]] = {}
    starters_ok = 0
    complete_players = 0
    used_players = 0
    team_minutes: dict[int, float] = {}
    for team in lineups:
        raw: dict[str, float] = {}
        starters = 0
        for player in team.get("lineup", []):
            player_id = str(player["player_id"])
            minutes, started, complete = _merge_minutes(player.get("positions", []), duration)
            if minutes <= 0:
                continue
            used_players += 1
            complete_players += int(complete)
            starters += int(started)
            raw[player_id] = minutes / duration
            meta = player_meta.setdefault(
                player_id,
                {
                    "id": player_id,
                    "name": player.get("player_name", player_id),
                    "country": (player.get("country") or {}).get("name", ""),
                    "minutes": 0.0,
                    "matches": 0,
                    "starts": 0,
                    "team_minutes": defaultdict(float),
                },
            )
            meta["minutes"] += minutes
            meta["matches"] += 1
            meta["starts"] += int(started)
            meta["team_minutes"][team["team_name"]] += minutes
        starters_ok += int(starters == 11)
        total = sum(raw.values())
        if total <= 0:
            raise ValueError(f"No usable lineup for match {match['match_id']} team {team.get('team_name')}")
        by_team[team["team_id"]] = {player_id: weight * 11.0 / total for player_id, weight in raw.items()}
        team_minutes[team["team_id"]] = total * duration
    home_id = match["home_team"]["home_team_id"]
    away_id = match["away_team"]["away_team_id"]
    if home_id not in by_team or away_id not in by_team:
        raise ValueError(f"Missing declared team lineup for match {match['match_id']}")
    return by_team[home_id], by_team[away_id], {
        "duration": duration,
        "starter_teams_ok": starters_ok,
        "used_players": used_players,
        "complete_players": complete_players,
        # Source position intervals can overlap by a few stoppage-time minutes around
        # substitutions. The model normalizes each side back to 11 player-equivalents;
        # the gate rejects material gaps but permits that documented timestamp jitter.
        "integrity_ok": starters_ok == 2
        and all(8.5 * duration <= minutes <= 11.6 * duration for minutes in team_minutes.values()),
    }


def _cholesky(matrix: list[list[float]]) -> list[list[float]]:
    size = len(matrix)
    lower = [[0.0] * size for _ in range(size)]
    for row in range(size):
        for column in range(row + 1):
            value = matrix[row][column] - sum(lower[row][k] * lower[column][k] for k in range(column))
            if row == column:
                lower[row][column] = math.sqrt(max(value, 1e-12))
            else:
                lower[row][column] = value / lower[column][column]
    return lower


def _solve(lower: list[list[float]], values: list[float]) -> list[float]:
    size = len(values)
    forward = [0.0] * size
    for row in range(size):
        forward[row] = (values[row] - sum(lower[row][k] * forward[k] for k in range(row))) / lower[row][row]
    result = [0.0] * size
    for row in range(size - 1, -1, -1):
        result[row] = (
            forward[row] - sum(lower[k][row] * result[k] for k in range(row + 1, size))
        ) / lower[row][row]
    return result


def _fit_ridge(rows: list[dict], player_ids: list[str], penalty: float) -> dict:
    if not rows:
        return {"coefficients": {player_id: 0.0 for player_id in player_ids}, "home_advantage": 0.0}
    index = {player_id: position for position, player_id in enumerate(player_ids)}
    design: list[list[float]] = []
    targets: list[float] = []
    for row in rows:
        vector = [0.0] * len(player_ids)
        for player_id, weight in row["home"].items():
            vector[index[player_id]] += weight
        for player_id, weight in row["away"].items():
            vector[index[player_id]] -= weight
        design.append(vector)
        targets.append(row["goal_difference"])
    home_advantage = sum(targets) / len(targets)
    centered = [target - home_advantage for target in targets]
    gram = [
        [sum(left * right for left, right in zip(design[i], design[j])) for j in range(len(rows))]
        for i in range(len(rows))
    ]
    for position in range(len(rows)):
        gram[position][position] += penalty
    lower = _cholesky(gram)
    alpha = _solve(lower, centered)
    coefficients = {
        player_id: sum(design[row][column] * alpha[row] for row in range(len(rows)))
        for column, player_id in enumerate(player_ids)
    }
    predictions = [
        home_advantage + sum(vector[column] * coefficients[player_id] for column, player_id in enumerate(player_ids))
        for vector in design
    ]
    residuals = [target - prediction for target, prediction in zip(targets, predictions)]
    residual_variance = sum(value * value for value in residuals) / max(len(rows) - 1, 1)
    uncertainty: dict[str, float] = {}
    for column, player_id in enumerate(player_ids):
        source = [vector[column] for vector in design]
        projected = _solve(lower, source)
        uncertainty[player_id] = math.sqrt(max(residual_variance * sum(value * value for value in projected), 0.0))
    return {
        "coefficients": coefficients,
        "uncertainty": uncertainty,
        "home_advantage": home_advantage,
        "rmse": math.sqrt(sum(value * value for value in residuals) / len(residuals)),
    }


def _rapm(rows: list[dict], player_ids: list[str]) -> dict:
    split = max(1, int(len(rows) * 0.75))
    training, validation = rows[:split], rows[split:]
    candidates = []
    for penalty in RIDGE_CANDIDATES:
        fitted = _fit_ridge(training, player_ids, penalty)
        errors = []
        for row in validation:
            prediction = fitted["home_advantage"]
            prediction += sum(fitted["coefficients"].get(player_id, 0.0) * weight for player_id, weight in row["home"].items())
            prediction -= sum(fitted["coefficients"].get(player_id, 0.0) * weight for player_id, weight in row["away"].items())
            errors.append((row["goal_difference"] - prediction) ** 2)
        candidates.append({"penalty": penalty, "validation_rmse": math.sqrt(sum(errors) / max(len(errors), 1))})
    selected = min(candidates, key=lambda item: (item["validation_rmse"], item["penalty"]))
    fitted = _fit_ridge(rows, player_ids, selected["penalty"])
    fitted["selected_penalty"] = selected["penalty"]
    fitted["candidates"] = candidates
    fitted["validation_matches"] = len(validation)
    return fitted


def _components(rows: list[dict]) -> int:
    graph: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        players = list(row["home"]) + list(row["away"])
        if not players:
            continue
        anchor = players[0]
        for player_id in players[1:]:
            graph[anchor].add(player_id)
            graph[player_id].add(anchor)
    remaining = set(graph)
    components = 0
    while remaining:
        components += 1
        stack = [remaining.pop()]
        while stack:
            for neighbour in graph[stack.pop()]:
                if neighbour in remaining:
                    remaining.remove(neighbour)
                    stack.append(neighbour)
    return components


def _build_cohort(definition: dict, fetch: Callable[..., bytes]) -> tuple[dict, bytes]:
    match_url = f"{STATSBOMB_ROOT}/matches/{definition['competition_id']}/{definition['season_id']}.json"
    match_bytes = fetch(match_url, cache_ttl=35 * 86_400)
    matches = json.loads(match_bytes)
    matches.sort(key=lambda item: (item["match_date"], item["match_id"]))
    player_meta: dict[str, dict] = {}
    rows: list[dict] = []
    audit = {"starter_teams_ok": 0, "used_players": 0, "complete_players": 0, "integrity_matches": 0}
    snapshot = hashlib.sha256(match_bytes)
    for match in matches:
        lineup_url = f"{STATSBOMB_ROOT}/lineups/{match['match_id']}.json"
        lineup_bytes = fetch(lineup_url, cache_ttl=35 * 86_400)
        snapshot.update(lineup_bytes)
        lineups = json.loads(lineup_bytes)
        home, away, match_audit = _lineup_weights(match, lineups, player_meta)
        audit["starter_teams_ok"] += match_audit["starter_teams_ok"]
        audit["used_players"] += match_audit["used_players"]
        audit["complete_players"] += match_audit["complete_players"]
        audit["integrity_matches"] += int(match_audit["integrity_ok"])
        score_a = 1.0 if match["home_score"] > match["away_score"] else 0.0 if match["home_score"] < match["away_score"] else 0.5
        rows.append(
            {
                "date": match["match_date"],
                "match_id": match["match_id"],
                "home": home,
                "away": away,
                "score_a": score_a,
                "goal_difference": match["home_score"] - match["away_score"],
            }
        )
    lineup_model = LineupTrueSkill()
    log_losses: list[float] = []
    briers: list[float] = []
    for row in rows:
        probabilities = lineup_model.probabilities(row["home"], row["away"])
        log_losses.append(multiclass_log_loss(probabilities, row["score_a"]))
        briers.append(multiclass_brier(probabilities, row["score_a"]))
        lineup_model.update(row["home"], row["away"], row["score_a"])
    player_ids = sorted(player_meta)
    rapm = _rapm(rows, player_ids)
    eligible = [
        player_id
        for player_id, meta in player_meta.items()
        if meta["minutes"] >= MIN_MINUTES and meta["matches"] >= MIN_MATCHES
    ]
    for meta in player_meta.values():
        meta["team"] = max(meta["team_minutes"], key=meta["team_minutes"].get)
        del meta["team_minutes"]

    def common(player_id: str) -> dict:
        meta = player_meta[player_id]
        return {
            "id": player_id,
            "name": meta["name"],
            "team": meta["team"],
            "country": meta["country"],
            "minutes": round(meta["minutes"], 1),
            "matches": meta["matches"],
            "starts": meta["starts"],
        }

    trueskill_rows = []
    for player_id in eligible:
        belief = lineup_model.state(player_id)
        trueskill_rows.append(
            common(player_id)
            | {
                "mean": round(belief.mean, 4),
                "uncertainty": round(belief.sigma, 4),
                "score": round(belief.conservative, 4),
            }
        )
    trueskill_rows.sort(key=lambda item: (-item["score"], item["name"]))
    for rank, item in enumerate(trueskill_rows, 1):
        item["rank"] = rank
    rapm_rows = []
    for player_id in eligible:
        coefficient = rapm["coefficients"][player_id]
        uncertainty = rapm["uncertainty"][player_id]
        rapm_rows.append(
            common(player_id)
            | {
                "impact": round(coefficient, 4),
                "uncertainty": round(uncertainty, 4),
                "score": round(coefficient - 1.96 * uncertainty, 4),
            }
        )
    rapm_rows.sort(key=lambda item: (-item["score"], item["name"]))
    for rank, item in enumerate(rapm_rows, 1):
        item["rank"] = rank
    starter_coverage = audit["starter_teams_ok"] / max(2 * len(rows), 1)
    minute_coverage = audit["complete_players"] / max(audit["used_players"], 1)
    integrity_coverage = audit["integrity_matches"] / max(len(rows), 1)
    gate_passed = starter_coverage >= 0.95 and minute_coverage >= 0.95 and integrity_coverage >= 0.95
    if not gate_passed:
        raise ValueError(
            f"{definition['name']} failed lineup publication gates: "
            f"starters={starter_coverage:.3f}, minutes={minute_coverage:.3f}, integrity={integrity_coverage:.3f}"
        )
    cohort = {
        "id": definition["id"],
        "name": definition["name"],
        "country": definition["country"],
        "first_match": rows[0]["date"],
        "last_match": rows[-1]["date"],
        "matches": len(rows),
        "players_seen": len(player_meta),
        "eligible_players": len(eligible),
        "eligibility": {"minimum_minutes": MIN_MINUTES, "minimum_matches": MIN_MATCHES},
        "coverage": {
            "status": "passed",
            "lineup_files": 1.0,
            "starting_lineups": round(starter_coverage, 4),
            "player_minutes": round(minute_coverage, 4),
            "lineup_integrity": round(integrity_coverage, 4),
            "player_match_graph_components": _components(rows),
        },
        "models": {
            "lineup-trueskill": {
                "label": "Lineup TrueSkill",
                "ranking_rule": "mean − 3 × uncertainty",
                "parameters": {"initial_mean": 25.0, "initial_sigma": round(25.0 / 3.0, 4), "beta": round(25.0 / 6.0, 4), "tau": round(25.0 / 300.0, 4), "draw_probability": 0.25},
                "metrics": {"chronological_predictions": len(rows), "log_loss": round(sum(log_losses) / len(log_losses), 4), "brier": round(sum(briers) / len(briers), 4)},
                "rankings": trueskill_rows,
            },
            "rapm": {
                "label": "RAPM",
                "ranking_rule": "goal impact − 1.96 × uncertainty",
                "parameters": {"selected_ridge_penalty": rapm["selected_penalty"], "candidates": rapm["candidates"], "home_goal_advantage": round(rapm["home_advantage"], 4)},
                "metrics": {"chronological_validation_matches": rapm["validation_matches"], "validation_rmse": min(item["validation_rmse"] for item in rapm["candidates"]), "full_replay_rmse": round(rapm["rmse"], 4)},
                "rankings": rapm_rows,
            },
        },
        "snapshot_sha256": snapshot.hexdigest(),
    }
    return cohort, match_bytes


def build_player_payload(fetch: Callable[..., bytes]) -> dict:
    cohorts = []
    for definition in COHORTS:
        cohort, _ = _build_cohort(definition, fetch)
        cohorts.append(cohort)
    return {
        "schema_version": PLAYER_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": {
            "name": "StatsBomb Open Data",
            "url": "https://github.com/statsbomb/open-data",
            "license": "StatsBomb Open Data terms",
            "attribution": "Data source: StatsBomb. Ratings and analysis are independent.",
            "scope": "Complete declared historical cohorts only; not a live five-league player feed.",
        },
        "methodology": {
            "inputs": ["match outcome", "goal difference", "stable player IDs", "lineups", "minutes played"],
            "excluded_inputs": ["passes", "shots", "dribbles", "expected goals", "tracking data"],
            "lineup_trueskill": "Sequential additive team-skill update using normalized minutes-played weights; every probability is recorded before its match update.",
            "rapm": "Match-level goal-difference ridge regression using normalized minutes weights, home-goal intercept, and a chronological final-quarter penalty selection.",
            "interpretation": "These estimates describe association with team outcomes within one declared season. They do not identify how a player contributed and should not be compared across cohorts.",
        },
        "cohorts": cohorts,
    }


def player_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://kieranmcshane.github.io/rating-lab/player-schema.json",
        "title": "Rating Lab historical football-player payload",
        "type": "object",
        "required": ["schema_version", "generated_at", "source", "methodology", "cohorts"],
        "properties": {
            "schema_version": {"const": PLAYER_SCHEMA_VERSION},
            "generated_at": {"type": "string"},
            "source": {"type": "object"},
            "methodology": {"type": "object"},
            "cohorts": {"type": "array", "minItems": 1},
        },
        "additionalProperties": False,
    }


def validate_player_payload(payload: dict) -> None:
    schema = player_schema()
    missing = set(schema["required"]) - set(payload)
    if missing:
        raise ValueError(f"Player payload missing fields: {sorted(missing)}")
    if payload["schema_version"] != PLAYER_SCHEMA_VERSION:
        raise ValueError("Unexpected player schema version")
    if not payload["cohorts"]:
        raise ValueError("Player payload has no cohorts")
    for cohort in payload["cohorts"]:
        if cohort["coverage"]["status"] != "passed":
            raise ValueError(f"Unpublishable player cohort: {cohort['id']}")
        if not cohort["models"]["lineup-trueskill"]["rankings"] or not cohort["models"]["rapm"]["rankings"]:
            raise ValueError(f"Empty player ranking: {cohort['id']}")
