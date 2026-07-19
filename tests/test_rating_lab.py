from __future__ import annotations

from datetime import date, timedelta
import json
import math
from pathlib import Path
import unittest

from rating_lab.models import EloModel, GaussianSkillModel, Match
from rating_lab.pipeline import (
    _deduplicate,
    _metrics,
    _parse_broadcast_pgn,
    _parse_international_results,
    build_sport_payload,
    validate_payload,
)


class RatingModelTests(unittest.TestCase):
    def test_elo_is_zero_sum_and_symmetric(self):
        model = EloModel(k=24)
        prediction = model.update(Match(date(2026, 1, 1), "a", "b", 1.0))
        self.assertAlmostEqual(prediction, 0.5)
        self.assertAlmostEqual(model.states["a"].mean + model.states["b"].mean, 3000.0)
        self.assertGreater(model.states["a"].mean, 1500)
        self.assertLess(model.states["b"].mean, 1500)

    def test_draw_leaves_equal_players_centered(self):
        for model in (EloModel(), GaussianSkillModel(draw_margin=1.0), GaussianSkillModel(robust=True, draw_margin=1.0)):
            model.update(Match(date(2026, 1, 1), "a", "b", 0.5))
            self.assertAlmostEqual(model.states["a"].mean, model.states["b"].mean, places=7)

    def test_bayesian_uncertainty_reduces_after_evidence(self):
        for robust in (False, True):
            model = GaussianSkillModel(robust=robust)
            initial = model.state("a").variance
            for day in range(8):
                model.update(Match(date(2026, 1, 1) + timedelta(days=day), "a", "b", 1.0))
            self.assertLess(model.states["a"].variance, initial)
            self.assertTrue(math.isfinite(model.states["a"].mean))

    def test_long_inactivity_adds_more_uncertainty(self):
        recent = GaussianSkillModel()
        inactive = GaussianSkillModel()
        first = Match(date(2025, 1, 1), "a", "b", 1.0)
        recent.update(first)
        inactive.update(first)
        recent.update(Match(date(2025, 1, 8), "a", "b", 1.0))
        inactive.update(Match(date(2026, 1, 1), "a", "b", 1.0))
        self.assertGreater(inactive.states["a"].variance, recent.states["a"].variance)

    def test_heavy_tail_limits_a_shock(self):
        gaussian = GaussianSkillModel()
        robust = GaussianSkillModel(robust=True)
        for model in (gaussian, robust):
            model.state("favorite").mean = 45
            model.state("underdog").mean = 10
        before_g = gaussian.state("favorite").mean
        before_r = robust.state("favorite").mean
        upset = Match(date(2026, 1, 1), "favorite", "underdog", 0.0)
        gaussian.update(upset)
        robust.update(upset)
        self.assertLess(abs(before_r - robust.state("favorite").mean), abs(before_g - gaussian.state("favorite").mean))


class PipelineTests(unittest.TestCase):
    def test_international_parser_handles_neutral_venues_and_draws(self):
        fixture = """date,home_team,away_team,home_score,away_score,tournament,city,country,neutral
2026-01-10,France,Spain,1,1,Friendly,Paris,France,FALSE
2026-02-12,Brazil,Argentina,2,1,Friendly,Miami,United States,TRUE
"""
        matches, entities = _parse_international_results(fixture, 2020)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].score_a, 0.5)
        self.assertTrue(matches[0].home_advantage)
        self.assertFalse(matches[1].home_advantage)
        self.assertIn("national-football:brazil", entities)

    def test_pgn_parser_uses_fide_identity_and_draw(self):
        pgn = """[Event \"Open\"]
[Date \"2026.06.20\"]
[White \"Ada Player\"]
[Black \"Bob Player\"]
[WhiteFideId \"123\"]
[BlackFideId \"456\"]
[Result \"1/2-1/2\"]

1. e4 e5 1/2-1/2
"""
        matches, entities = _parse_broadcast_pgn(pgn)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].score_a, 0.5)
        self.assertIn("chess:fide:123", entities)

    def test_deduplication_is_deterministic(self):
        match = Match(date(2026, 1, 1), "a", "b", 1.0, "Test")
        self.assertEqual(_deduplicate([match, match]), [match])

    def test_metrics_are_finite(self):
        rows = [
            {"date": "2026-01-01", "predicted": 0.8, "actual": 1.0},
            {"date": "2026-01-02", "predicted": 0.4, "actual": 0.5},
        ]
        result = _metrics(rows, date(2025, 1, 1))
        self.assertEqual(result["predictions"], 2)
        self.assertGreater(result["log_loss"], 0)

    def test_synthetic_payload_matches_public_contract(self):
        start = date(2023, 1, 1)
        matches = []
        for index in range(36):
            matches.append(Match(start + timedelta(days=index * 35), "p1", "p2", 1.0 if index % 3 else 0.0, "ATP singles", "2025"))
        entities = {
            "p1": {"name": "Player One", "country": "FRA", "competition": "ATP singles"},
            "p2": {"name": "Player Two", "country": "GBR", "competition": "ATP singles"},
        }
        source = {"source": "Fixture", "source_url": "https://example.test", "license": "Test", "latest_result": matches[-1].date.isoformat(), "stale_after_hours": 240}
        payload = build_sport_payload("tennis", matches, entities, source)
        schema = json.loads((Path(__file__).parents[1] / "rating_lab/schema.json").read_text())
        validate_payload(payload, schema)
        self.assertEqual(set(payload["models"]), {"elo", "trueskill", "robust"})
        self.assertIn("candidate_parameters", payload)
        self.assertEqual(payload["data_window"]["matches"], len(matches))

    def test_national_team_eligibility_uses_two_year_window(self):
        start = date(2023, 1, 1)
        matches = [
            Match(start + timedelta(days=index * 120), "n1", "n2", float(index % 2), "Friendly", str(2023 + index // 3), True)
            for index in range(12)
        ]
        entities = {
            "n1": {"name": "Nation One", "country": "", "competition": "Men's national teams"},
            "n2": {"name": "Nation Two", "country": "", "competition": "Men's national teams"},
        }
        source = {"source": "Fixture", "source_url": "https://example.test", "license": "CC0", "latest_result": matches[-1].date.isoformat(), "stale_after_hours": 168}
        payload = build_sport_payload("national-football", matches, entities, source)
        self.assertEqual(payload["eligibility"]["recent_window_days"], 730)
        self.assertEqual(payload["eligibility"]["minimum_recent_matches"], 5)
        self.assertTrue(payload["models"]["elo"]["rankings"])


if __name__ == "__main__":
    unittest.main()
