"""Outcome-only football player models for complete historical lineup cohorts."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi, sqrt
from statistics import NormalDist


_NORMAL = NormalDist()


@dataclass
class PlayerBelief:
    mean: float = 25.0
    variance: float = (25.0 / 3.0) ** 2

    @property
    def sigma(self) -> float:
        return sqrt(max(self.variance, 1e-12))

    @property
    def conservative(self) -> float:
        return self.mean - 3.0 * self.sigma


class LineupTrueSkill:
    """Two-team TrueSkill update with normalized minutes-played weights."""

    def __init__(
        self,
        *,
        initial_mean: float = 25.0,
        initial_sigma: float = 25.0 / 3.0,
        beta: float = 25.0 / 6.0,
        tau: float = 25.0 / 300.0,
        draw_probability: float = 0.25,
    ) -> None:
        self.initial_mean = initial_mean
        self.initial_variance = initial_sigma**2
        self.beta = beta
        self.tau = tau
        self.draw_probability = draw_probability
        self.beliefs: dict[str, PlayerBelief] = {}

    def state(self, player_id: str) -> PlayerBelief:
        if player_id not in self.beliefs:
            self.beliefs[player_id] = PlayerBelief(self.initial_mean, self.initial_variance)
        return self.beliefs[player_id]

    def _terms(
        self, team_a: dict[str, float], team_b: dict[str, float]
    ) -> tuple[float, float, float]:
        mean = 0.0
        variance = 0.0
        weight_square_sum = 0.0
        for side, team in ((1.0, team_a), (-1.0, team_b)):
            for player_id, weight in team.items():
                belief = self.state(player_id)
                mean += side * weight * belief.mean
                variance += weight * weight * belief.variance
                weight_square_sum += weight * weight
        performance_variance = self.beta * self.beta * weight_square_sum
        c = sqrt(max(variance + performance_variance, 1e-12))
        margin = _NORMAL.inv_cdf((self.draw_probability + 1.0) / 2.0) * sqrt(
            max(performance_variance, 1e-12)
        )
        return mean, c, margin

    def probabilities(
        self, team_a: dict[str, float], team_b: dict[str, float]
    ) -> dict[str, float]:
        mean, c, margin = self._terms(team_a, team_b)
        loss = _NORMAL.cdf((-margin - mean) / c)
        win = 1.0 - _NORMAL.cdf((margin - mean) / c)
        draw = max(0.0, 1.0 - win - loss)
        total = max(win + draw + loss, 1e-12)
        return {"win": win / total, "draw": draw / total, "loss": loss / total}

    def update(
        self, team_a: dict[str, float], team_b: dict[str, float], outcome_a: float
    ) -> None:
        for player_id in set(team_a) | set(team_b):
            belief = self.state(player_id)
            belief.variance += self.tau * self.tau
        mean, c, margin = self._terms(team_a, team_b)
        if outcome_a == 0.5:
            lower = (-margin - mean) / c
            upper = (margin - mean) / c
            denominator = max(_NORMAL.cdf(upper) - _NORMAL.cdf(lower), 1e-12)
            phi_lower = exp(-0.5 * lower * lower) / sqrt(2.0 * pi)
            phi_upper = exp(-0.5 * upper * upper) / sqrt(2.0 * pi)
            v = (phi_lower - phi_upper) / denominator
            w = v * v + (upper * phi_upper - lower * phi_lower) / denominator
        else:
            side = 1.0 if outcome_a > 0.5 else -1.0
            t = (side * mean - margin) / c
            denominator = max(_NORMAL.cdf(t), 1e-12)
            v = side * exp(-0.5 * t * t) / sqrt(2.0 * pi) / denominator
            signed_v = v
            unsigned_v = abs(v)
            w = unsigned_v * (unsigned_v + t)
            v = signed_v
        snapshots = {
            player_id: (self.state(player_id).mean, self.state(player_id).variance)
            for player_id in set(team_a) | set(team_b)
        }
        for side, team in ((1.0, team_a), (-1.0, team_b)):
            for player_id, weight in team.items():
                belief = self.state(player_id)
                old_mean, old_variance = snapshots[player_id]
                belief.mean = old_mean + side * old_variance * weight / c * v
                shrink = old_variance * weight * weight / (c * c) * max(w, 0.0)
                belief.variance = old_variance * max(1.0 - shrink, 1e-6)


def multiclass_log_loss(probabilities: dict[str, float], outcome_a: float) -> float:
    key = "win" if outcome_a > 0.5 else "loss" if outcome_a < 0.5 else "draw"
    return -log(max(probabilities[key], 1e-12))


def multiclass_brier(probabilities: dict[str, float], outcome_a: float) -> float:
    key = "win" if outcome_a > 0.5 else "loss" if outcome_a < 0.5 else "draw"
    return sum((probability - (1.0 if label == key else 0.0)) ** 2 for label, probability in probabilities.items())

