"""Deterministic online rating models used by the public dashboard.

The Bayesian models use assumed-density filtering.  Outcome likelihoods are
integrated over a Gaussian skill-difference prior with Gauss-Hermite
quadrature, then moment-matched back to independent Gaussian player beliefs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
import math
from typing import Callable, Iterable


# 20-point Gauss-Hermite rule (weight exp(-x^2)).  Keeping the nodes here makes
# production refreshes reproducible without a compiled numerical dependency.
_GH_X = (
    -5.387480890011233, -4.603682449550744, -3.944764040115625,
    -3.347854567383216, -2.788806058428130, -2.254974002089276,
    -1.738537712116586, -1.234076215395323, -0.737473728545394,
    -0.245340708300901, 0.245340708300901, 0.737473728545394,
    1.234076215395323, 1.738537712116586, 2.254974002089276,
    2.788806058428130, 3.347854567383216, 3.944764040115625,
    4.603682449550744, 5.387480890011233,
)
_GH_W = (
    2.229393645534151e-13, 4.399340992273181e-10, 1.086069370769281e-7,
    7.802556478532064e-6, 2.283386360163540e-4, 0.003243773342238,
    0.024810520887464, 0.109017206020023, 0.286675505362834,
    0.462243669600610, 0.462243669600610, 0.286675505362834,
    0.109017206020023, 0.024810520887464, 0.003243773342238,
    2.283386360163540e-4, 7.802556478532064e-6, 1.086069370769281e-7,
    4.399340992273181e-10, 2.229393645534151e-13,
)
_SQRT_PI = math.sqrt(math.pi)


@dataclass(frozen=True, slots=True)
class Match:
    date: date
    entity_a: str
    entity_b: str
    score_a: float
    competition: str = ""
    season: str = ""
    home_advantage: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, row: dict) -> "Match":
        raw_date = row["date"]
        parsed = raw_date if isinstance(raw_date, date) else date.fromisoformat(str(raw_date)[:10])
        return cls(
            date=parsed,
            entity_a=str(row["entity_a"]),
            entity_b=str(row["entity_b"]),
            score_a=float(row["score_a"]),
            competition=str(row.get("competition", "")),
            season=str(row.get("season", "")),
            home_advantage=bool(row.get("home_advantage", False)),
            metadata=dict(row.get("metadata", {})),
        )


@dataclass(slots=True)
class RatingState:
    mean: float
    variance: float = 0.0
    matches: int = 0
    last_played: date | None = None

    @property
    def sigma(self) -> float:
        return math.sqrt(max(self.variance, 0.0))


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def _cauchy_cdf(value: float) -> float:
    # Student-t with one degree of freedom: deliberately heavy-tailed.
    return 0.5 + math.atan(value) / math.pi


class EloModel:
    name = "elo"

    def __init__(self, k: float = 24.0, scale: float = 400.0, home: float = 0.0):
        self.k = k
        self.scale = scale
        self.home = home
        self.states: dict[str, RatingState] = {}

    def state(self, entity: str) -> RatingState:
        return self.states.setdefault(entity, RatingState(1500.0))

    def predict(self, match: Match) -> float:
        a, b = self.state(match.entity_a), self.state(match.entity_b)
        advantage = self.home if match.home_advantage else 0.0
        return 1.0 / (1.0 + 10.0 ** (-(a.mean + advantage - b.mean) / self.scale))

    def update(self, match: Match) -> float:
        probability = self.predict(match)
        delta = self.k * (match.score_a - probability)
        a, b = self.state(match.entity_a), self.state(match.entity_b)
        a.mean += delta
        b.mean -= delta
        for state in (a, b):
            state.matches += 1
            state.last_played = match.date
        return probability

    def regress(self, fraction: float = 0.25) -> None:
        for state in self.states.values():
            state.mean += fraction * (1500.0 - state.mean)


class GaussianSkillModel:
    """TrueSkill-like Gaussian beliefs with Gaussian or heavy-tail performance."""

    def __init__(
        self,
        *,
        robust: bool = False,
        initial_mean: float = 25.0,
        initial_sigma: float = 25.0 / 3.0,
        beta: float = 25.0 / 6.0,
        tau: float = 25.0 / 300.0,
        draw_margin: float = 0.0,
        advantage: float = 0.0,
    ):
        self.name = "robust" if robust else "trueskill"
        self.robust = robust
        self.initial_mean = initial_mean
        self.initial_variance = initial_sigma**2
        self.beta = beta
        self.tau = tau
        self.draw_margin = draw_margin
        self.advantage = advantage
        self.states: dict[str, RatingState] = {}

    def state(self, entity: str) -> RatingState:
        return self.states.setdefault(
            entity, RatingState(self.initial_mean, self.initial_variance)
        )

    def _outcome_probability(self, difference: float, score_a: float) -> float:
        cdf: Callable[[float], float] = _cauchy_cdf if self.robust else _normal_cdf
        if score_a == 0.5:
            upper = cdf((self.draw_margin - difference) / self.beta)
            lower = cdf((-self.draw_margin - difference) / self.beta)
            return max(upper - lower, 1e-12)
        signed = difference if score_a == 1.0 else -difference
        return max(cdf((signed - self.draw_margin) / self.beta), 1e-12)

    def predict(self, match: Match) -> float:
        a, b = self.state(match.entity_a), self.state(match.entity_b)
        mean = a.mean - b.mean + (self.advantage if match.home_advantage else 0.0)
        variance = a.variance + b.variance
        win = draw = 0.0
        for node, weight in zip(_GH_X, _GH_W):
            difference = mean + math.sqrt(2.0 * variance) * node
            win += weight * self._outcome_probability(difference, 1.0)
            draw += weight * self._outcome_probability(difference, 0.5)
        win /= _SQRT_PI
        draw /= _SQRT_PI
        # Expected score is the quantity comparable with Elo and Brier scoring.
        return min(max(win + 0.5 * draw, 1e-9), 1.0 - 1e-9)

    def update(self, match: Match) -> float:
        a, b = self.state(match.entity_a), self.state(match.entity_b)
        for state in (a, b):
            elapsed_days = max((match.date - state.last_played).days, 1) if state.last_played else 1
            state.variance += self.tau**2 * max(elapsed_days / 7.0, 1.0)
        prediction = self.predict(match)
        advantage = self.advantage if match.home_advantage else 0.0
        mean = a.mean - b.mean + advantage
        variance = max(a.variance + b.variance, 1e-9)

        z = first = second = 0.0
        for node, weight in zip(_GH_X, _GH_W):
            difference = mean + math.sqrt(2.0 * variance) * node
            likelihood = self._outcome_probability(difference, match.score_a)
            weighted = weight * likelihood
            z += weighted
            first += weighted * difference
            second += weighted * difference * difference
        z = max(z, 1e-15)
        posterior_mean = first / z
        posterior_variance = max(second / z - posterior_mean**2, 1e-8)

        shift = posterior_mean - mean
        a_variance, b_variance = a.variance, b.variance
        a.mean += a_variance / variance * shift
        b.mean -= b_variance / variance * shift
        a.variance = max(
            a_variance + (a_variance / variance) ** 2 * (posterior_variance - variance),
            1e-6,
        )
        b.variance = max(
            b_variance + (b_variance / variance) ** 2 * (posterior_variance - variance),
            1e-6,
        )
        for state in (a, b):
            state.matches += 1
            state.last_played = match.date
        return prediction


def replay(
    matches: Iterable[Match],
    model,
    *,
    season_regression: float = 0.0,
) -> tuple[dict[str, RatingState], list[dict]]:
    """Replay sorted matches and return states plus pre-match predictions."""
    predictions: list[dict] = []
    previous_season = None
    for match in sorted(matches, key=lambda item: (item.date, item.entity_a, item.entity_b)):
        if (
            season_regression
            and previous_season is not None
            and match.season
            and match.season != previous_season
            and isinstance(model, EloModel)
        ):
            model.regress(season_regression)
        probability = model.update(match)
        predictions.append(
            {"date": match.date.isoformat(), "predicted": probability, "actual": match.score_a}
        )
        previous_season = match.season or previous_season
    return model.states, predictions


def utc_now_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
