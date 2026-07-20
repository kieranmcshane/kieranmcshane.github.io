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
    volatility: float = 0.0

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

    def predict_outcomes(self, match: Match, draw_rate: float = 0.25) -> tuple[float, float, float]:
        """Return home-win, draw, away-win probabilities preserving expected score."""
        expected = self.predict(match)
        draw = min(draw_rate * 4.0 * expected * (1.0 - expected), 2.0 * min(expected, 1.0 - expected))
        return expected - 0.5 * draw, draw, 1.0 - expected - 0.5 * draw

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

    def predict_outcomes(self, match: Match) -> tuple[float, float, float]:
        a, b = self.state(match.entity_a), self.state(match.entity_b)
        mean = a.mean - b.mean + (self.advantage if match.home_advantage else 0.0)
        variance = a.variance + b.variance
        win = draw = loss = 0.0
        for node, weight in zip(_GH_X, _GH_W):
            difference = mean + math.sqrt(2.0 * variance) * node
            win += weight * self._outcome_probability(difference, 1.0)
            draw += weight * self._outcome_probability(difference, 0.5)
            loss += weight * self._outcome_probability(difference, 0.0)
        total = max((win + draw + loss) / _SQRT_PI, 1e-12)
        return win / _SQRT_PI / total, draw / _SQRT_PI / total, loss / _SQRT_PI / total

    def predict(self, match: Match) -> float:
        win, draw, _ = self.predict_outcomes(match)
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


class Glicko2Model:
    """Public-domain Glicko-2 with deterministic calendar-day rating periods."""

    name = "glicko2"
    scale = 173.7178

    def __init__(
        self,
        *,
        tau: float = 0.5,
        initial_rating: float = 1500.0,
        initial_rd: float = 350.0,
        initial_volatility: float = 0.06,
        home: float = 0.0,
        period_days: float = 7.0,
        epsilon: float = 1e-6,
    ):
        self.tau = tau
        self.initial_rating = initial_rating
        self.initial_rd = initial_rd
        self.initial_volatility = initial_volatility
        self.home = home
        self.period_days = period_days
        self.epsilon = epsilon
        self.states: dict[str, RatingState] = {}

    def state(self, entity: str) -> RatingState:
        return self.states.setdefault(
            entity,
            RatingState(
                self.initial_rating,
                self.initial_rd**2,
                volatility=self.initial_volatility,
            ),
        )

    @staticmethod
    def _g(phi: float) -> float:
        return 1.0 / math.sqrt(1.0 + 3.0 * phi * phi / math.pi**2)

    def _inflate(self, state: RatingState, played: date) -> None:
        if state.last_played:
            periods = max((played - state.last_played).days / self.period_days, 1.0)
            phi = state.sigma / self.scale
            phi = math.sqrt(phi * phi + state.volatility**2 * periods)
            state.variance = min((phi * self.scale) ** 2, self.initial_rd**2)

    def age_to(self, played: date) -> None:
        """Inflate every published RD to a common snapshot date without adding games."""
        for state in self.states.values():
            self._inflate(state, played)

    def _expected(self, a: RatingState, b: RatingState, advantage: float = 0.0) -> float:
        mu_difference = (a.mean + advantage - b.mean) / self.scale
        opponent_phi = b.sigma / self.scale
        return 1.0 / (1.0 + math.exp(-self._g(opponent_phi) * mu_difference))

    def predict(self, match: Match) -> float:
        return min(
            max(
                self._expected(
                    self.state(match.entity_a),
                    self.state(match.entity_b),
                    self.home if match.home_advantage else 0.0,
                ),
                1e-9,
            ),
            1.0 - 1e-9,
        )

    def predict_outcomes(self, match: Match, draw_rate: float = 0.25) -> tuple[float, float, float]:
        expected = self.predict(match)
        draw = min(draw_rate * 4.0 * expected * (1.0 - expected), 2.0 * min(expected, 1.0 - expected))
        return expected - 0.5 * draw, draw, 1.0 - expected - 0.5 * draw

    def _new_volatility(self, phi: float, volatility: float, variance: float, delta: float) -> float:
        a = math.log(volatility * volatility)

        def objective(x: float) -> float:
            exponential = math.exp(x)
            numerator = exponential * (delta * delta - phi * phi - variance - exponential)
            denominator = 2.0 * (phi * phi + variance + exponential) ** 2
            return numerator / denominator - (x - a) / (self.tau * self.tau)

        lower = a
        if delta * delta > phi * phi + variance:
            upper = math.log(delta * delta - phi * phi - variance)
        else:
            step = 1
            upper = a - step * self.tau
            while objective(upper) < 0.0:
                step += 1
                upper = a - step * self.tau
        f_lower, f_upper = objective(lower), objective(upper)
        while abs(upper - lower) > self.epsilon:
            candidate = lower + (lower - upper) * f_lower / (f_upper - f_lower)
            f_candidate = objective(candidate)
            if f_candidate * f_upper <= 0.0:
                lower, f_lower = upper, f_upper
            else:
                f_lower /= 2.0
            upper, f_upper = candidate, f_candidate
        return math.exp(lower / 2.0)

    def update_period(self, matches: Iterable[Match]) -> list[float]:
        period = list(matches)
        if not period:
            return []
        played = period[0].date
        if any(match.date != played for match in period):
            raise ValueError("A Glicko-2 rating period must contain one calendar date")
        participants = {entity for match in period for entity in (match.entity_a, match.entity_b)}
        for entity in participants:
            self._inflate(self.state(entity), played)
        predictions = [self.predict(match) for match in period]
        snapshots = {
            entity: (
                self.state(entity).mean,
                self.state(entity).sigma,
                self.state(entity).volatility,
            )
            for entity in participants
        }
        results: dict[str, list[tuple[str, float, float]]] = {entity: [] for entity in participants}
        for match in period:
            advantage = self.home if match.home_advantage else 0.0
            results[match.entity_a].append((match.entity_b, match.score_a, advantage))
            results[match.entity_b].append((match.entity_a, 1.0 - match.score_a, -advantage))
        updates = {}
        for entity, games in results.items():
            rating, rd, volatility = snapshots[entity]
            mu, phi = (rating - 1500.0) / self.scale, rd / self.scale
            terms = []
            for opponent, score, advantage in games:
                opponent_rating, opponent_rd, _ = snapshots[opponent]
                opponent_mu = (opponent_rating - 1500.0) / self.scale
                opponent_phi = opponent_rd / self.scale
                g_value = self._g(opponent_phi)
                expected = 1.0 / (
                    1.0 + math.exp(-g_value * (mu + advantage / self.scale - opponent_mu))
                )
                terms.append((g_value, expected, score))
            variance = 1.0 / sum(g_value * g_value * expected * (1.0 - expected) for g_value, expected, _ in terms)
            delta = variance * sum(g_value * (score - expected) for g_value, expected, score in terms)
            new_volatility = self._new_volatility(phi, volatility, variance, delta)
            phi_star = math.sqrt(phi * phi + new_volatility * new_volatility)
            new_phi = 1.0 / math.sqrt(1.0 / (phi_star * phi_star) + 1.0 / variance)
            new_mu = mu + new_phi * new_phi * sum(
                g_value * (score - expected) for g_value, expected, score in terms
            )
            updates[entity] = (
                1500.0 + self.scale * new_mu,
                (self.scale * new_phi) ** 2,
                new_volatility,
                len(games),
            )
        for entity, (rating, variance, volatility, games) in updates.items():
            state = self.state(entity)
            state.mean = rating
            state.variance = variance
            state.volatility = volatility
            state.matches += games
            state.last_played = played
        return predictions

    def update(self, match: Match) -> float:
        return self.update_period([match])[0]


class SurfaceBlendModel:
    """Blend a global rating with an independently replayed surface rating.

    The global component keeps evidence connected across surfaces.  The
    surface component captures repeatable clay/grass/hard-court differences;
    its influence grows only as both players accumulate surface evidence.
    """

    def __init__(self, model_factory: Callable[[], object], surface_weight: float = 0.7):
        if not 0.0 <= surface_weight <= 1.0:
            raise ValueError("surface_weight must be between zero and one")
        self.model_factory = model_factory
        self.surface_weight = surface_weight
        self.global_model = model_factory()
        self.surface_models: dict[str, object] = {}
        self.name = self.global_model.name
        self.states = self.global_model.states
        self.uses_rating_period = isinstance(self.global_model, Glicko2Model)

    @staticmethod
    def surface(match: Match) -> str:
        raw = str(match.metadata.get("surface", "unknown")).strip().casefold()
        if "clay" in raw:
            return "clay"
        if "grass" in raw:
            return "grass"
        if "hard" in raw:
            return "hard"
        if "carpet" in raw:
            return "carpet"
        return "unknown"

    def surface_model(self, surface: str):
        return self.surface_models.setdefault(surface, self.model_factory())

    def state(self, entity: str) -> RatingState:
        return self.global_model.state(entity)

    def _weight(self, match: Match) -> float:
        surface_model = self.surface_model(self.surface(match))
        matches_a = surface_model.state(match.entity_a).matches
        matches_b = surface_model.state(match.entity_b).matches
        evidence = min((matches_a + matches_b) / 20.0, 1.0)
        return self.surface_weight * evidence

    def predict(self, match: Match) -> float:
        weight = self._weight(match)
        global_probability = self.global_model.predict(match)
        surface_probability = self.surface_model(self.surface(match)).predict(match)
        return (1.0 - weight) * global_probability + weight * surface_probability

    def predict_outcomes(self, match: Match, draw_rate: float = 0.25) -> tuple[float, float, float]:
        weight = self._weight(match)
        surface_model = self.surface_model(self.surface(match))
        if isinstance(self.global_model, (EloModel, Glicko2Model)):
            global_outcomes = self.global_model.predict_outcomes(match, draw_rate)
            surface_outcomes = surface_model.predict_outcomes(match, draw_rate)
        else:
            global_outcomes = self.global_model.predict_outcomes(match)
            surface_outcomes = surface_model.predict_outcomes(match)
        return tuple(
            (1.0 - weight) * global_value + weight * surface_value
            for global_value, surface_value in zip(global_outcomes, surface_outcomes)
        )

    def update(self, match: Match) -> float:
        probability = self.predict(match)
        self.global_model.update(match)
        self.surface_model(self.surface(match)).update(match)
        return probability

    def update_period(self, matches: Iterable[Match]) -> list[float]:
        period = list(matches)
        predictions = [self.predict(match) for match in period]
        self.global_model.update_period(period)
        by_surface: dict[str, list[Match]] = {}
        for match in period:
            by_surface.setdefault(self.surface(match), []).append(match)
        for surface, surface_matches in by_surface.items():
            self.surface_model(surface).update_period(surface_matches)
        return predictions

    def age_to(self, played: date) -> None:
        if hasattr(self.global_model, "age_to"):
            self.global_model.age_to(played)
        for model in self.surface_models.values():
            if hasattr(model, "age_to"):
                model.age_to(played)


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
