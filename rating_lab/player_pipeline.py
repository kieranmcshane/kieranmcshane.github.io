"""Build reproducible historical football-player ratings from StatsBomb lineups."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Callable

from .player_models import LineupTrueSkill, multiclass_brier, multiclass_log_loss


PLAYER_SCHEMA_VERSION = "1.3.0"
STATSBOMB_ROOT = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
API_FOOTBALL_ROOT = "https://v3.football.api-sports.io"
API_FOOTBALL_WORLD_CUP = {
    "id": "world-cup-2026",
    "competition_id": 1,
    "season_id": 2026,
    "name": "FIFA World Cup 2026",
    "country": "International",
    "gender": "men",
    "format": "international tournament",
    "venue_context": "tournament",
    "expected_matches": 104,
}
COHORTS = (
    {
        "id": "premier-league-2015-16",
        "competition_id": 2,
        "season_id": 27,
        "season_name": "2015/16",
        "name": "Premier League 2015/16",
        "country": "England",
        "gender": "men",
        "format": "club league season",
        "scope_type": "season",
        "venue_context": "home-and-away",
        "expected_matches": 380,
        "minimum_minutes": 900.0,
        "minimum_matches": 10,
        "included_competitions": ["Premier League"],
        "scope_note": "Complete 380-match league season. FA Cup, EFL Cup and UEFA fixtures are withheld because the open source does not provide complete lineup-minute coverage for those competitions.",
    },
    {
        "id": "euro-2024",
        "competition_id": 55,
        "season_id": 282,
        "name": "UEFA Euro 2024",
        "country": "Europe",
        "gender": "men",
        "format": "international tournament",
        "venue_context": "tournament",
        "expected_matches": 51,
        "included_competitions": ["UEFA Euro 2024"],
    },
    {
        "id": "world-cup-2022",
        "competition_id": 43,
        "season_id": 106,
        "name": "FIFA World Cup 2022",
        "country": "International",
        "gender": "men",
        "format": "international tournament",
        "venue_context": "tournament",
        "expected_matches": 64,
        "included_competitions": ["FIFA World Cup 2022"],
    },
    {
        "id": "liga-f-2023-24",
        "competition_id": 182,
        "season_id": 281,
        "season_name": "2023/24",
        "name": "Liga F 2023/24",
        "country": "Spain",
        "gender": "women",
        "format": "club league season",
        "scope_type": "season",
        "venue_context": "home-and-away",
        "expected_matches": 240,
        "included_competitions": ["Liga F"],
        "scope_note": "Complete 240-match league season. Copa de la Reina and UEFA fixtures are not included because equivalent complete lineup-minute coverage is unavailable in the open source.",
    },
    {
        "id": "wsl-2023-24",
        "competition_id": 37,
        "season_id": 281,
        "season_name": "2023/24",
        "name": "FA Women's Super League 2023/24",
        "country": "England",
        "gender": "women",
        "format": "club league season",
        "scope_type": "season",
        "venue_context": "home-and-away",
        "expected_matches": 132,
        "included_competitions": ["Women's Super League"],
        "scope_note": "Complete 132-match league season. FA Cup, League Cup and UEFA fixtures are not included because equivalent complete lineup-minute coverage is unavailable in the open source.",
    },
)
RIDGE_CANDIDATES = (1.0, 5.0, 20.0, 50.0)
CHEMISTRY_RIDGE_CANDIDATES = (1.0, 5.0, 20.0, 50.0)
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


def _merge_intervals(
    positions: list[dict], duration: float
) -> tuple[list[tuple[float, float]], bool, bool]:
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
    return [(start, end) for start, end in merged], starts, complete and bool(intervals)


def _merge_minutes(positions: list[dict], duration: float) -> tuple[float, bool, bool]:
    intervals, starts, complete = _merge_intervals(positions, duration)
    return sum(end - start for start, end in intervals), starts, complete


def _overlap_minutes(
    left: list[tuple[float, float]], right: list[tuple[float, float]]
) -> float:
    total = 0.0
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        left_start, left_end = left[left_index]
        right_start, right_end = right[right_index]
        total += max(0.0, min(left_end, right_end) - max(left_start, right_start))
        if left_end <= right_end:
            left_index += 1
        else:
            right_index += 1
    return total


def _lineup_weights(
    match: dict, lineups: list[dict], player_meta: dict[str, dict]
) -> tuple[dict[str, float], dict[str, float], dict]:
    duration = _match_duration(match, lineups)
    by_team: dict[int, dict[str, float]] = {}
    pair_by_team: dict[int, dict[tuple[str, str], float]] = {}
    starters_ok = 0
    complete_players = 0
    used_players = 0
    team_minutes: dict[int, float] = {}
    for team in lineups:
        raw: dict[str, float] = {}
        intervals_by_player: dict[str, list[tuple[float, float]]] = {}
        starters = 0
        for player in team.get("lineup", []):
            player_id = str(player["player_id"])
            intervals, started, complete = _merge_intervals(
                player.get("positions", []), duration
            )
            minutes = sum(end - start for start, end in intervals)
            if minutes <= 0:
                continue
            used_players += 1
            complete_players += int(complete)
            starters += int(started)
            raw[player_id] = minutes / duration
            intervals_by_player[player_id] = intervals
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
        pair_by_team[team["team_id"]] = {
            (left, right): overlap / duration
            for position, left in enumerate(sorted(intervals_by_player))
            for right in sorted(intervals_by_player)[position + 1 :]
            for overlap in (
                _overlap_minutes(intervals_by_player[left], intervals_by_player[right]),
            )
            if overlap > 0.0
        }
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
        "home_pairs": pair_by_team[home_id],
        "away_pairs": pair_by_team[away_id],
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
    home_exposure = [1.0 if row.get("home_advantage", True) else 0.0 for row in rows]
    exposed_targets = [target for target, exposure in zip(targets, home_exposure) if exposure]
    home_advantage = sum(exposed_targets) / len(exposed_targets) if exposed_targets else 0.0
    centered = [
        target - home_advantage * exposure
        for target, exposure in zip(targets, home_exposure)
    ]
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
        home_advantage * home_exposure[row]
        + sum(vector[column] * coefficients[player_id] for column, player_id in enumerate(player_ids))
        for row, vector in enumerate(design)
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
            prediction = fitted["home_advantage"] if row.get("home_advantage", True) else 0.0
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


def _predict_ridge(row: dict, fitted: dict) -> float:
    prediction = fitted["home_advantage"] if row.get("home_advantage", True) else 0.0
    prediction += sum(
        fitted["coefficients"].get(player_id, 0.0) * weight
        for player_id, weight in row["home"].items()
    )
    prediction -= sum(
        fitted["coefficients"].get(player_id, 0.0) * weight
        for player_id, weight in row["away"].items()
    )
    return prediction


def _pair_design(row: dict) -> dict[tuple[str, str], float]:
    """Give each side one unit of chemistry exposure, split by shared-pitch time."""
    result: dict[tuple[str, str], float] = {}
    home_total = sum(row.get("home_pairs", {}).values())
    away_total = sum(row.get("away_pairs", {}).values())
    if home_total:
        for pair, exposure in row["home_pairs"].items():
            result[pair] = result.get(pair, 0.0) + exposure / home_total
    if away_total:
        for pair, exposure in row["away_pairs"].items():
            result[pair] = result.get(pair, 0.0) - exposure / away_total
    return result


def _sparse_dot(left: dict, right: dict) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(key, 0.0) for key, value in left.items())


def _fit_pair_ridge(rows: list[dict], additive: dict, penalty: float) -> dict:
    """Fit teammate-pair effects to goal difference left unexplained by RAPM."""
    if not rows:
        return {"coefficients": {}, "uncertainty": {}, "rmse": 0.0}
    design = [_pair_design(row) for row in rows]
    targets = [row["goal_difference"] - _predict_ridge(row, additive) for row in rows]
    gram = [
        [
            _sparse_dot(design[left], design[right])
            + (penalty if left == right else 0.0)
            for right in range(len(rows))
        ]
        for left in range(len(rows))
    ]
    lower = _cholesky(gram)
    alpha = _solve(lower, targets)
    features = sorted({pair for vector in design for pair in vector})
    coefficients = {
        pair: sum(vector.get(pair, 0.0) * alpha[row] for row, vector in enumerate(design))
        for pair in features
    }
    predictions = [
        sum(coefficients[pair] * value for pair, value in vector.items())
        for vector in design
    ]
    residuals = [target - prediction for target, prediction in zip(targets, predictions)]
    residual_variance = sum(value * value for value in residuals) / max(len(rows) - 1, 1)
    uncertainty: dict[tuple[str, str], float] = {}
    for pair in features:
        source = [vector.get(pair, 0.0) for vector in design]
        projected = _solve(lower, source)
        leverage = sum(value * fitted for value, fitted in zip(source, projected))
        posterior_variance = residual_variance / penalty * max(1.0 - leverage, 0.0)
        uncertainty[pair] = math.sqrt(posterior_variance)
    return {
        "coefficients": coefficients,
        "uncertainty": uncertainty,
        "rmse": math.sqrt(sum(value * value for value in residuals) / len(residuals)),
    }


def _predict_pair_component(row: dict, fitted: dict) -> float:
    return sum(
        fitted["coefficients"].get(pair, 0.0) * value
        for pair, value in _pair_design(row).items()
    )


def _pair_chemistry(rows: list[dict], player_ids: list[str], additive: dict) -> dict:
    """Select residual pair shrinkage chronologically, then replay the full cohort."""
    split = max(1, int(len(rows) * 0.75))
    training, validation = rows[:split], rows[split:]
    training_additive = _rapm(training, player_ids)
    baseline_errors = [
        (row["goal_difference"] - _predict_ridge(row, training_additive)) ** 2
        for row in validation
    ]
    baseline_rmse = math.sqrt(sum(baseline_errors) / max(len(baseline_errors), 1))
    candidates = []
    for penalty in CHEMISTRY_RIDGE_CANDIDATES:
        fitted = _fit_pair_ridge(training, training_additive, penalty)
        errors = [
            (
                row["goal_difference"]
                - _predict_ridge(row, training_additive)
                - _predict_pair_component(row, fitted)
            )
            ** 2
            for row in validation
        ]
        candidates.append(
            {
                "penalty": penalty,
                "validation_rmse": math.sqrt(sum(errors) / max(len(errors), 1)),
            }
        )
    selected = min(candidates, key=lambda item: (item["validation_rmse"], item["penalty"]))
    fitted = _fit_pair_ridge(rows, additive, selected["penalty"])
    fitted["selected_penalty"] = selected["penalty"]
    fitted["candidates"] = candidates
    fitted["validation_matches"] = len(validation)
    fitted["baseline_validation_rmse"] = baseline_rmse
    fitted["validation_rmse"] = selected["validation_rmse"]
    fitted["validation_status"] = (
        "supported"
        if selected["validation_rmse"] < baseline_rmse - 0.0001
        else "descriptive_only"
    )
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


def _home_advantage(match: dict, definition: dict) -> bool:
    """Use venue evidence for tournaments; league home designations are authoritative."""
    if definition.get("venue_context") != "tournament":
        return True
    home_country = (match.get("home_team", {}).get("country") or {}).get("name")
    stadium_country = (match.get("stadium", {}).get("country") or {}).get("name")
    return bool(home_country and stadium_country and home_country == stadium_country)


def _rate_cohort(
    definition: dict,
    rows: list[dict],
    player_meta: dict[str, dict],
    audit: dict,
    snapshot_sha256: str,
    source: dict,
) -> dict:
    if not rows:
        raise ValueError(f"{definition['name']} has no completed matches")
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
    chemistry = _pair_chemistry(rows, player_ids, rapm)
    minimum_minutes = float(definition.get("minimum_minutes", MIN_MINUTES))
    minimum_matches = int(definition.get("minimum_matches", MIN_MATCHES))
    eligible = [
        player_id
        for player_id, meta in player_meta.items()
        if meta["minutes"] >= minimum_minutes and meta["matches"] >= minimum_matches
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

    pair_minimum_minutes = float(
        definition.get(
            "pair_minimum_minutes", 450.0 if definition.get("scope_type") == "season" else 120.0
        )
    )
    pair_minimum_matches = int(
        definition.get(
            "pair_minimum_matches", 5 if definition.get("scope_type") == "season" else 2
        )
    )
    pair_support: dict[tuple[str, str], dict[str, float | int]] = defaultdict(
        lambda: {"minutes": 0.0, "matches": 0}
    )
    for row in rows:
        for pairs in (row.get("home_pairs", {}), row.get("away_pairs", {})):
            for pair, exposure in pairs.items():
                pair_support[pair]["minutes"] += exposure * row["duration"]
                pair_support[pair]["matches"] += 1
    published_pairs = {
        pair
        for pair, support in pair_support.items()
        if support["minutes"] >= pair_minimum_minutes
        and support["matches"] >= pair_minimum_matches
        and pair in chemistry["coefficients"]
    }
    chemistry_rows = []
    for player_id in eligible:
        partnerships = [pair for pair in published_pairs if player_id in pair]
        total_minutes = sum(float(pair_support[pair]["minutes"]) for pair in partnerships)
        if total_minutes <= 0.0:
            continue
        weights = {
            pair: float(pair_support[pair]["minutes"]) / total_minutes
            for pair in partnerships
        }
        impact = sum(weights[pair] * chemistry["coefficients"][pair] for pair in partnerships)
        uncertainty = math.sqrt(
            sum(
                (weights[pair] * chemistry["uncertainty"][pair]) ** 2
                for pair in partnerships
            )
        )
        ordered_partnerships = sorted(
            partnerships,
            key=lambda pair: (chemistry["coefficients"][pair], pair),
            reverse=True,
        )

        def partnership_summary(pair: tuple[str, str]) -> dict:
            partner_id = pair[1] if pair[0] == player_id else pair[0]
            return {
                "partner_id": partner_id,
                "partner_name": player_meta[partner_id]["name"],
                "impact": round(chemistry["coefficients"][pair], 4),
                "shared_minutes": round(float(pair_support[pair]["minutes"]), 1),
            }

        chemistry_rows.append(
            common(player_id)
            | {
                "impact": round(impact, 4),
                "uncertainty": round(uncertainty, 4),
                "score": round(impact - 1.96 * uncertainty, 4),
                "qualifying_partnerships": len(partnerships),
                "strongest_partnerships": [
                    partnership_summary(pair) for pair in ordered_partnerships[:2]
                ],
                "weakest_partnerships": [
                    partnership_summary(pair) for pair in reversed(ordered_partnerships[-2:])
                ],
            }
        )
    chemistry_rows.sort(key=lambda item: (-item["score"], item["name"]))
    for rank, item in enumerate(chemistry_rows, 1):
        item["rank"] = rank

    partnership_rows = []
    for pair in published_pairs:
        left, right = pair
        if left not in player_meta or right not in player_meta:
            continue
        impact = chemistry["coefficients"][pair]
        uncertainty = chemistry["uncertainty"][pair]
        left_team = player_meta[left]["team"]
        right_team = player_meta[right]["team"]
        partnership_rows.append(
            {
                "id": f"{left}:{right}",
                "players": [
                    {"id": left, "name": player_meta[left]["name"]},
                    {"id": right, "name": player_meta[right]["name"]},
                ],
                "team": left_team if left_team == right_team else "Multiple teams",
                "shared_minutes": round(float(pair_support[pair]["minutes"]), 1),
                "matches": int(pair_support[pair]["matches"]),
                "impact": round(impact, 4),
                "uncertainty": round(uncertainty, 4),
                "score": round(impact - 1.96 * uncertainty, 4),
            }
        )
    partnership_rows.sort(key=lambda item: (-item["score"], item["id"]))
    starter_coverage = audit["starter_teams_ok"] / max(2 * len(rows), 1)
    minute_coverage = audit["complete_players"] / max(audit["used_players"], 1)
    integrity_coverage = audit["integrity_matches"] / max(len(rows), 1)
    substitution_coverage = audit.get("verified_substitution_players", 0) / max(
        audit.get("substitution_players", 0), 1
    ) if "substitution_players" in audit else 1.0
    source_fixture_coverage = audit.get("source_fixtures", len(rows)) / max(len(rows), 1)
    gate_passed = (
        starter_coverage >= 0.95
        and minute_coverage >= 0.95
        and integrity_coverage >= 0.95
        and substitution_coverage >= 0.95
        and source_fixture_coverage >= 0.95
    )
    if not gate_passed:
        raise ValueError(
            f"{definition['name']} failed lineup publication gates: "
            f"starters={starter_coverage:.3f}, minutes={minute_coverage:.3f}, "
            f"integrity={integrity_coverage:.3f}, substitutions={substitution_coverage:.3f}, "
            f"fixtures={source_fixture_coverage:.3f}"
        )
    return {
        "id": definition["id"],
        "name": definition["name"],
        "country": definition["country"],
        "gender": definition["gender"],
        "format": definition["format"],
        "scope_type": definition.get("scope_type", "competition"),
        "season_name": definition.get("season_name"),
        "included_competitions": definition.get("included_competitions", [definition["name"]]),
        "scope_note": definition.get("scope_note"),
        "source": source,
        "first_match": rows[0]["date"],
        "last_match": rows[-1]["date"],
        "matches": len(rows),
        "players_seen": len(player_meta),
        "eligible_players": len(eligible),
        "eligibility": {"minimum_minutes": minimum_minutes, "minimum_matches": minimum_matches},
        "coverage": {
            "status": "passed",
            "lineup_files": round(source_fixture_coverage, 4),
            "starting_lineups": round(starter_coverage, 4),
            "player_minutes": round(minute_coverage, 4),
            "substitution_minutes": round(substitution_coverage, 4),
            "lineup_integrity": round(integrity_coverage, 4),
            "player_match_graph_components": _components(rows),
            "expected_matches": definition.get("expected_matches", len(rows)),
            "fixture_completeness": round(
                len(rows) / max(definition.get("expected_matches", len(rows)), 1), 4
            ),
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
                "parameters": {
                    "selected_ridge_penalty": rapm["selected_penalty"],
                    "candidates": rapm["candidates"],
                    "home_goal_advantage": round(rapm["home_advantage"], 4),
                    "home_advantage_evidence": "Declared home team for league seasons; stadium country equals home-team country for international tournaments.",
                },
                "metrics": {"chronological_validation_matches": rapm["validation_matches"], "validation_rmse": min(item["validation_rmse"] for item in rapm["candidates"]), "full_replay_rmse": round(rapm["rmse"], 4)},
                "rankings": rapm_rows,
            },
            "pairwise-chemistry": {
                "label": "Pairwise chemistry",
                "status": chemistry["validation_status"],
                "ranking_rule": "residual pair impact − 1.96 × approximate uncertainty",
                "parameters": {
                    "selected_ridge_penalty": chemistry["selected_penalty"],
                    "candidates": chemistry["candidates"],
                    "pair_minimum_minutes": pair_minimum_minutes,
                    "pair_minimum_matches": pair_minimum_matches,
                    "team_pair_normalization": "Each side contributes one unit of total pair exposure per match, divided according to exact shared-pitch time.",
                    "additive_baseline": "Chronologically tuned RAPM",
                },
                "metrics": {
                    "chronological_validation_matches": chemistry["validation_matches"],
                    "baseline_validation_rmse": round(chemistry["baseline_validation_rmse"], 4),
                    "validation_rmse": round(chemistry["validation_rmse"], 4),
                    "validation_delta": round(
                        chemistry["validation_rmse"] - chemistry["baseline_validation_rmse"], 4
                    ),
                    "full_replay_residual_rmse": round(chemistry["rmse"], 4),
                    "qualifying_partnerships": len(partnership_rows),
                },
                "rankings": chemistry_rows,
                "partnerships": {
                    "outperformers": partnership_rows[:15],
                    "underperformers": list(reversed(partnership_rows[-15:])),
                },
            },
        },
        "snapshot_sha256": snapshot_sha256,
    }


def _build_cohort(definition: dict, fetch: Callable[..., bytes]) -> tuple[dict, bytes]:
    match_url = f"{STATSBOMB_ROOT}/matches/{definition['competition_id']}/{definition['season_id']}.json"
    match_bytes = fetch(match_url, cache_ttl=35 * 86_400)
    matches = json.loads(match_bytes)
    expected_matches = definition.get("expected_matches")
    if expected_matches is not None and len(matches) != expected_matches:
        raise ValueError(
            f"{definition['name']} expected {expected_matches} matches; "
            f"StatsBomb published {len(matches)}"
        )
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
                "home_pairs": match_audit["home_pairs"],
                "away_pairs": match_audit["away_pairs"],
                "duration": match_audit["duration"],
                "score_a": score_a,
                "goal_difference": match["home_score"] - match["away_score"],
                "home_advantage": _home_advantage(match, definition),
            }
        )
    cohort = _rate_cohort(
        definition,
        rows,
        player_meta,
        audit,
        snapshot.hexdigest(),
        {
            "name": "StatsBomb Open Data",
            "url": "https://github.com/statsbomb/open-data",
            "license": "StatsBomb Open Data terms",
            "raw_responses_published": True,
        },
    )
    return cohort, match_bytes


def _api_football_json(
    fetch: Callable[..., bytes], url: str, api_key: str, snapshot
) -> dict:
    body = fetch(url, api_football_key=api_key, cache_ttl=35 * 86_400)
    snapshot.update(body)
    payload = json.loads(body)
    errors = payload.get("errors")
    if errors:
        raise ValueError(f"API-Football rejected {url.split('?')[0]}: {errors}")
    if "response" not in payload:
        raise ValueError(f"API-Football response missing data for {url.split('?')[0]}")
    return payload


def _api_football_fixture(
    fixture_row: dict,
) -> tuple[dict, list[dict], dict]:
    fixture = fixture_row.get("fixture") or {}
    fixture_id = fixture.get("id")
    teams = fixture_row.get("teams") or {}
    home_team = teams.get("home") or {}
    away_team = teams.get("away") or {}
    if not fixture_id or not home_team.get("id") or not away_team.get("id"):
        raise ValueError("API-Football fixture is missing stable fixture or team identifiers")
    lineups_by_team = {
        (item.get("team") or {}).get("id"): item for item in fixture_row.get("lineups") or []
    }
    players_by_team = {
        (item.get("team") or {}).get("id"): item for item in fixture_row.get("players") or []
    }
    incoming: dict[int, set[int]] = defaultdict(set)
    outgoing: dict[int, set[int]] = defaultdict(set)
    dismissed: dict[int, set[int]] = defaultdict(set)
    for event in fixture_row.get("events") or []:
        team_id = (event.get("team") or {}).get("id")
        event_type = str(event.get("type") or "").casefold()
        if not team_id:
            continue
        if event_type == "subst":
            player_out = (event.get("player") or {}).get("id")
            player_in = (event.get("assist") or {}).get("id")
            if player_out:
                outgoing[team_id].add(player_out)
            if player_in:
                incoming[team_id].add(player_in)
        elif event_type == "card" and "red" in str(event.get("detail") or "").casefold():
            player_id = (event.get("player") or {}).get("id")
            if player_id:
                dismissed[team_id].add(player_id)
    lineups: list[dict] = []
    substitution_players = 0
    verified_substitution_players = 0
    maximum_minutes = 90.0
    for team in (home_team, away_team):
        team_id = team["id"]
        lineup = lineups_by_team.get(team_id)
        player_block = players_by_team.get(team_id)
        if not lineup or not player_block:
            raise ValueError(f"API-Football fixture {fixture_id} is missing lineup/player data for team {team_id}")
        starter_ids = {
            (item.get("player") or {}).get("id") for item in lineup.get("startXI") or []
        }
        starter_ids.discard(None)
        if len(starter_ids) != 11:
            raise ValueError(f"API-Football fixture {fixture_id} team {team_id} has {len(starter_ids)} starters")
        players: list[dict] = []
        for entry in player_block.get("players") or []:
            player = entry.get("player") or {}
            player_id = player.get("id")
            statistics = (entry.get("statistics") or [{}])[0]
            games = statistics.get("games") or {}
            minutes = games.get("minutes")
            if not player_id or minutes in (None, ""):
                continue
            minutes = float(minutes)
            if minutes <= 0:
                continue
            maximum_minutes = max(maximum_minutes, minutes)
            started = player_id in starter_ids
            if not started:
                substitution_players += 1
                verified_substitution_players += int(player_id in incoming[team_id])
            elif minutes < 89.5:
                substitution_players += 1
                verified_substitution_players += int(
                    player_id in outgoing[team_id] or player_id in dismissed[team_id]
                )
            players.append(
                {
                    "player_id": f"api-football:{player_id}",
                    "player_name": player.get("name") or str(player_id),
                    "country": {"name": ""},
                    "positions": [
                        {
                            "from": "00:00" if started else f"{max(0.0, 90.0 - minutes):.2f}:00",
                            "to": f"{minutes:.2f}:00" if started else "90:00",
                            "end_reason": "Final Whistle" if minutes >= 89.5 else "Substitution",
                        }
                    ],
                }
            )
        missing_starters = starter_ids - {
            int(player["player_id"].split(":", 1)[1]) for player in players
        }
        if missing_starters:
            raise ValueError(
                f"API-Football fixture {fixture_id} team {team_id} lacks minutes for starters {sorted(missing_starters)}"
            )
        lineups.append({"team_id": team_id, "team_name": team.get("name") or str(team_id), "lineup": players})
    duration = 120.0 if maximum_minutes > 100.0 else 90.0
    for team in lineups:
        for player in team["lineup"]:
            position = player["positions"][0]
            minutes = float(position["to"].split(":", 1)[0]) if position["from"] == "00:00" else 90.0 - float(position["from"].split(":", 1)[0])
            if position["from"] != "00:00":
                position["from"] = f"{duration - minutes:.2f}:00"
                position["to"] = f"{duration:.2f}:00"
    goals = fixture_row.get("goals") or {}
    if goals.get("home") is None or goals.get("away") is None:
        raise ValueError(f"API-Football fixture {fixture_id} is missing the result")
    match = {
        "match_id": fixture_id,
        "match_date": str(fixture.get("date") or "")[:10],
        "home_team": {"home_team_id": home_team["id"], "home_team_name": home_team.get("name")},
        "away_team": {"away_team_id": away_team["id"], "away_team_name": away_team.get("name")},
        "home_score": int(goals["home"]),
        "away_score": int(goals["away"]),
        "competition_stage": {"name": (fixture_row.get("league") or {}).get("round", "")},
    }
    return match, lineups, {
        "substitution_players": substitution_players,
        "verified_substitution_players": verified_substitution_players,
    }


def _build_api_football_cohort(
    definition: dict, fetch: Callable[..., bytes], api_key: str
) -> dict:
    snapshot = hashlib.sha256()
    fixture_list_url = (
        f"{API_FOOTBALL_ROOT}/fixtures?league={definition['competition_id']}"
        f"&season={definition['season_id']}"
    )
    fixture_list = _api_football_json(fetch, fixture_list_url, api_key, snapshot)
    fixture_ids = sorted(
        {
            int(item["fixture"]["id"])
            for item in fixture_list["response"]
            if (item.get("fixture") or {}).get("status", {}).get("short") in {"FT", "AET", "PEN"}
        }
    )
    if len(fixture_ids) != definition["expected_matches"]:
        raise ValueError(
            f"{definition['name']} expected {definition['expected_matches']} completed fixtures; "
            f"API-Football returned {len(fixture_ids)}"
        )
    detailed: list[dict] = []
    for offset in range(0, len(fixture_ids), 20):
        ids = "-".join(str(value) for value in fixture_ids[offset : offset + 20])
        payload = _api_football_json(
            fetch, f"{API_FOOTBALL_ROOT}/fixtures?ids={ids}", api_key, snapshot
        )
        detailed.extend(payload["response"])
    by_id = {(item.get("fixture") or {}).get("id"): item for item in detailed}
    if set(by_id) != set(fixture_ids):
        raise ValueError(f"{definition['name']} detailed fixture batches are incomplete")
    player_meta: dict[str, dict] = {}
    rows: list[dict] = []
    audit = {
        "starter_teams_ok": 0,
        "used_players": 0,
        "complete_players": 0,
        "integrity_matches": 0,
        "source_fixtures": 0,
        "substitution_players": 0,
        "verified_substitution_players": 0,
    }
    for fixture_id in fixture_ids:
        match, lineups, source_audit = _api_football_fixture(by_id[fixture_id])
        home, away, match_audit = _lineup_weights(match, lineups, player_meta)
        audit["starter_teams_ok"] += match_audit["starter_teams_ok"]
        audit["used_players"] += match_audit["used_players"]
        audit["complete_players"] += match_audit["complete_players"]
        audit["integrity_matches"] += int(match_audit["integrity_ok"])
        audit["source_fixtures"] += 1
        audit["substitution_players"] += source_audit["substitution_players"]
        audit["verified_substitution_players"] += source_audit["verified_substitution_players"]
        score_a = 1.0 if match["home_score"] > match["away_score"] else 0.0 if match["home_score"] < match["away_score"] else 0.5
        rows.append(
            {
                "date": match["match_date"],
                "match_id": match["match_id"],
                "home": home,
                "away": away,
                "home_pairs": match_audit["home_pairs"],
                "away_pairs": match_audit["away_pairs"],
                "duration": match_audit["duration"],
                "score_a": score_a,
                "goal_difference": match["home_score"] - match["away_score"],
                "home_advantage": False,
            }
        )
    rows.sort(key=lambda item: (item["date"], item["match_id"]))
    return _rate_cohort(
        definition,
        rows,
        player_meta,
        audit,
        snapshot.hexdigest(),
        {
            "name": "API-Football by API-SPORTS",
            "url": "https://www.api-football.com/",
            "terms": "https://api-sports.io/terms",
            "retrieval": "One league-season fixture list plus batches of at most 20 fixture IDs; raw responses remain in the private build cache.",
            "raw_responses_published": False,
        },
    )


def build_player_payload(
    fetch: Callable[..., bytes], api_football_key: str | None = None
) -> dict:
    cohorts = []
    for definition in COHORTS:
        cohort, _ = _build_cohort(definition, fetch)
        cohorts.append(cohort)
    if api_football_key:
        cohorts.append(
            _build_api_football_cohort(API_FOOTBALL_WORLD_CUP, fetch, api_football_key)
        )
    sources = {
        cohort["source"]["name"]: {
            "name": cohort["source"]["name"],
            "url": cohort["source"]["url"],
        }
        for cohort in cohorts
    }
    return {
        "schema_version": PLAYER_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": {
            "name": "Cohort-specific verified sources",
            "url": "https://kieranmcshane.github.io/rating-lab/players/",
            "sources": list(sources.values()),
            "license": "Source-specific terms recorded on each cohort",
            "attribution": "Ratings and analysis are independent of the data providers.",
            "scope": "Complete declared men's and women's tournaments and league seasons only; each cohort records its included competitions, source, and snapshot hash.",
        },
        "methodology": {
            "inputs": ["match outcome", "goal difference", "stable player IDs", "lineups", "minutes played"],
            "excluded_inputs": ["passes", "shots", "dribbles", "expected goals", "tracking data"],
            "lineup_trueskill": "Sequential additive team-skill update using normalized minutes-played weights; every probability is recorded before its match update.",
            "rapm": "Match-level goal-difference ridge regression using normalized minutes weights, home-goal intercept, and a chronological final-quarter penalty selection.",
            "pairwise_chemistry": "Experimental non-additive residual model: exact teammate overlap minutes define pair features, ridge shrinkage is selected on the chronological final quarter, and effects are fitted only to goal difference left unexplained by RAPM.",
            "interpretation": "These estimates describe association with team outcomes within one declared complete tournament or season. They do not identify how a player contributed and should not be compared across cohorts.",
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
        if any(
            not cohort["models"][model]["rankings"]
            for model in ("lineup-trueskill", "rapm", "pairwise-chemistry")
        ):
            raise ValueError(f"Empty player ranking: {cohort['id']}")
