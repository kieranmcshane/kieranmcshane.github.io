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
    _merge_schedule_results,
    _parse_broadcast_pgn,
    _parse_cup_schedule,
    _parse_football_txt,
    _parse_international_results,
    _simulate_league,
    _simulate_knockout,
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

    def test_outcome_probabilities_partition_one(self):
        match = Match(date(2026, 1, 1), "a", "b", 0.5, home_advantage=True)
        for model in (EloModel(home=65), GaussianSkillModel(draw_margin=1.35, advantage=1.35), GaussianSkillModel(robust=True, draw_margin=1.35, advantage=1.35)):
            outcomes = model.predict_outcomes(match)
            self.assertAlmostEqual(sum(outcomes), 1.0, places=8)
            self.assertTrue(all(0 <= probability <= 1 for probability in outcomes))


class PipelineTests(unittest.TestCase):
    def test_football_txt_parser_preserves_schedule_and_zero_zero_result(self):
        fixture = """= Test League 2026/27
▪ Matchday 1
  Fri Aug 21 2026
    20:00  Alpha FC               v Beta FC
  Sat Aug 22
    15:00  Gamma FC               v Delta FC               0-0
"""
        competition = _parse_football_txt(fixture, "test", "Test League", "2026-27")
        self.assertEqual(len(competition["fixtures"]), 2)
        self.assertIsNone(competition["fixtures"][0]["home_goals"])
        self.assertEqual(competition["fixtures"][1]["home_goals"], 0)
        self.assertEqual(competition["fixtures"][1]["date"], "2026-08-22")

    def test_league_simulation_is_seeded_and_probabilities_sum(self):
        competition = {
            "id": "test-league",
            "label": "Test League",
            "season": "2026-27",
            "teams": ["Alpha", "Beta", "Gamma", "Delta"],
            "fixtures": [
                {"date": "2026-08-01", "round": "1", "home_name": "Alpha", "away_name": "Beta", "home_goals": None, "away_goals": None},
                {"date": "2026-08-02", "round": "1", "home_name": "Gamma", "away_name": "Delta", "home_goals": None, "away_goals": None},
                {"date": "2026-08-08", "round": "2", "home_name": "Alpha", "away_name": "Gamma", "home_goals": None, "away_goals": None},
                {"date": "2026-08-09", "round": "2", "home_name": "Beta", "away_name": "Delta", "home_goals": None, "away_goals": None},
            ],
        }
        entities = {f"football:name:{name.casefold()}": {"name": name} for name in competition["teams"]}
        model = EloModel(home=65)
        model.state("football:name:alpha").mean = 1700
        first = _simulate_league(competition, model, "elo", entities, 0.25, simulations=250)
        second = _simulate_league(competition, model, "elo", entities, 0.25, simulations=250)
        self.assertEqual(first, second)
        self.assertAlmostEqual(sum(team["champion"] for team in first["teams"]), 1.0, places=3)
        self.assertEqual(first["remaining_matches"], 4)

    def test_knockout_simulation_preserves_published_ties_and_partitions_title_probability(self):
        teams = [
            {"id": "national-football:alpha", "name": "Alpha"},
            {"id": "national-football:beta", "name": "Beta"},
            {"id": "national-football:gamma", "name": "Gamma"},
            {"id": "national-football:delta", "name": "Delta"},
        ]
        competition = {
            "id": "test-cup",
            "season": "2026",
            "cohort": "national-football",
            "teams": teams,
            "knockout_fixtures": [
                {"date": "2026-08-01", "stage": "SEMI_FINALS", "status": "SCHEDULED", "home_id": teams[0]["id"], "away_id": teams[1]["id"], "home_goals": None, "away_goals": None, "winner_id": None},
                {"date": "2026-08-02", "stage": "SEMI_FINALS", "status": "SCHEDULED", "home_id": teams[2]["id"], "away_id": teams[3]["id"], "home_goals": None, "away_goals": None, "winner_id": None},
            ],
        }
        model = EloModel()
        model.state(teams[0]["id"]).mean = 1750
        first = _simulate_knockout(competition, model, "elo", simulations=500)
        second = _simulate_knockout(competition, model, "elo", simulations=500)
        self.assertEqual(first, second)
        self.assertEqual(first["published_ties_remaining"], 2)
        self.assertAlmostEqual(sum(team["champion"] for team in first["participants"]), 1.0, places=3)

    def test_cup_parser_withholds_title_forecast_before_knockout_field(self):
        payload = {"matches": [{
            "utcDate": "2026-09-01T18:00:00Z",
            "status": "SCHEDULED",
            "stage": "GROUP_STAGE",
            "group": "A",
            "homeTeam": {"id": 1, "name": "Alpha"},
            "awayTeam": {"id": 2, "name": "Beta"},
            "score": {"winner": None, "fullTime": {"home": None, "away": None}},
            "season": {"startDate": "2026-08-01"},
        }]}
        body = json.dumps(payload).encode()
        competition = _parse_cup_schedule(payload, "WC", "World Cup", "national-football", "https://example.test", body)
        self.assertIsNotNone(competition)
        self.assertFalse(competition["forecast_available"])
        self.assertIn("no title probability", competition["availability"])

    def test_schedule_results_advance_ratings_feed_and_active_membership(self):
        matches = [Match(date(2025, 1, 1), "football:name:old", "football:name:alpha", 0.0, "Test League", "2025-26", True)]
        entities = {
            "football:name:old": {"name": "Old FC", "competition": "Premier League", "active": True},
            "football:name:alpha": {"name": "Alpha FC", "competition": "Premier League", "active": True},
        }
        schedules = [{
            "label": "Premier League",
            "season": "2026-27",
            "teams": ["Alpha FC", "Beta FC"],
            "fixtures": [{"date": "2026-08-01", "round": "1", "home_name": "Alpha FC", "away_name": "Beta FC", "home_goals": 2, "away_goals": 1}],
        }]
        merged = _merge_schedule_results(matches, entities, schedules)
        self.assertEqual(len(merged), 2)
        self.assertTrue(entities["football:name:alpha"]["active"])
        self.assertTrue(entities["football:name:beta-fc"]["active"])
        self.assertFalse(entities["football:name:old"]["active"])

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
