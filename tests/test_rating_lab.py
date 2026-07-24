from __future__ import annotations

from datetime import date, timedelta
import hashlib
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from rating_lab.models import EloModel, GaussianSkillModel, Glicko2Model, Match, SurfaceBlendModel
from rating_lab.player_models import LineupTrueSkill
from rating_lab.player_pipeline import (
    API_FOOTBALL_LEAGUE_COHORTS,
    API_FOOTBALL_WORLD_CUP,
    COHORTS,
    _api_football_fixture,
    _build_cohort,
    build_player_payload,
    _fit_pair_ridge,
    _fit_ridge,
    _fit_team_hapm,
    _fit_team_lapm,
    _home_advantage,
    _jaccard,
    _laplacian_solve,
    _lineup_weights,
    _merge_minutes,
    _overlap_minutes,
    player_schema,
    validate_player_payload,
)
from rating_lab.pipeline import (
    FOOTBALL_COMPETITIONS,
    _deduplicate,
    _competition_performance,
    _competition_matches,
    _competition_state,
    _categorical_forecast_score,
    _build_tournament_predictor,
    _finalize_market_comparison,
    _football_data_crest_media,
    _get,
    _kalshi_event_snapshot,
    _market_identity_tokens,
    _metrics,
    _merge_schedule_media,
    _merge_schedule_results,
    _merge_tennis_schedule_results,
    _parse_atp_draw_pages,
    _parse_atp_player_catalog,
    _parse_broadcast_pgn,
    _parse_cup_schedule,
    _parse_football_txt,
    _parse_international_results,
    _parse_open_cup_json,
    _parse_uefa_ucl_qualifying,
    _polymarket_event_snapshot,
    _polymarket_search_query,
    _required_football_seasons,
    _simulate_league,
    _simulate_knockout,
    _simulate_qualifying_round,
    _simulate_tennis_draw,
    _validate_football_coverage,
    _model_candidates,
    build_sport_payload,
    individual_contribution_protocol,
    validate_payload,
    write_outputs,
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
        for model in (EloModel(home=65), Glicko2Model(home=65), GaussianSkillModel(draw_margin=1.35, advantage=1.35), GaussianSkillModel(robust=True, draw_margin=1.35, advantage=1.35)):
            outcomes = model.predict_outcomes(match)
            self.assertAlmostEqual(sum(outcomes), 1.0, places=8)
            self.assertTrue(all(0 <= probability <= 1 for probability in outcomes))

    def test_home_or_white_advantage_increases_entity_a_probability(self):
        neutral = Match(date(2026, 1, 1), "a", "b", 0.5)
        advantaged = Match(date(2026, 1, 1), "a", "b", 0.5, home_advantage=True)
        for model in (
            EloModel(home=35),
            Glicko2Model(home=35),
            GaussianSkillModel(draw_margin=0.75, advantage=0.4),
            GaussianSkillModel(robust=True, draw_margin=0.75, advantage=0.4),
        ):
            self.assertGreater(model.predict(advantaged), model.predict(neutral))

    def test_surface_blend_learns_opposite_surface_strengths(self):
        model = SurfaceBlendModel(lambda: EloModel(k=32), surface_weight=0.8)
        start = date(2026, 1, 1)
        for offset in range(12):
            model.update(Match(start + timedelta(days=offset), "a", "b", 1.0, metadata={"surface": "Clay"}))
            model.update(Match(start + timedelta(days=20 + offset), "a", "b", 0.0, metadata={"surface": "Hard"}))
        clay = model.predict(Match(date(2026, 3, 1), "a", "b", 0.5, metadata={"surface": "Clay"}))
        hard = model.predict(Match(date(2026, 3, 1), "a", "b", 0.5, metadata={"surface": "Hard"}))
        self.assertGreater(clay, 0.5)
        self.assertLess(hard, 0.5)

    def test_glicko2_matches_published_worked_example(self):
        model = Glicko2Model(tau=0.5)
        player = model.state("player")
        player.mean, player.variance, player.volatility = 1500.0, 200.0**2, 0.06
        for entity, rating, rd in (("a", 1400.0, 30.0), ("b", 1550.0, 100.0), ("c", 1700.0, 300.0)):
            state = model.state(entity)
            state.mean, state.variance, state.volatility = rating, rd**2, 0.06
        played = date(2022, 1, 1)
        model.update_period([
            Match(played, "player", "a", 1.0),
            Match(played, "player", "b", 0.0),
            Match(played, "player", "c", 0.0),
        ])
        self.assertAlmostEqual(player.mean, 1464.06, places=1)
        self.assertAlmostEqual(player.sigma, 151.52, places=1)
        self.assertAlmostEqual(player.volatility, 0.059996, places=5)

    def test_glicko2_inactivity_inflates_rd(self):
        recent = Glicko2Model(period_days=7)
        inactive = Glicko2Model(period_days=7)
        first = Match(date(2025, 1, 1), "a", "b", 1.0)
        recent.update(first)
        inactive.update(first)
        recent.update(Match(date(2025, 1, 8), "a", "b", 1.0))
        inactive.update(Match(date(2026, 1, 1), "a", "b", 1.0))
        self.assertGreater(inactive.states["a"].sigma, recent.states["a"].sigma)


class PipelineTests(unittest.TestCase):
    def test_http_credentials_strip_accidental_surrounding_whitespace(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return b'{"errors":{},"response":[]}'

        with patch("rating_lab.pipeline.urlopen", return_value=Response()) as opened:
            _get(
                "https://v3.football.api-sports.io/status?credential-test=1",
                token=" football-data-token\n",
                api_football_key=" api-football-key\n",
                attempts=1,
            )
        request = opened.call_args.args[0]
        headers = {name.casefold(): value for name, value in request.header_items()}
        self.assertEqual(headers["x-auth-token"], "football-data-token")
        self.assertEqual(headers["x-apisports-key"], "api-football-key")

    def test_context_parameters_cover_chess_color_and_tennis_surface(self):
        self.assertTrue(all(candidate["home"] == 35.0 for candidate in _model_candidates("chess", "elo")))
        surface_weights = {candidate["surface_weight"] for candidate in _model_candidates("tennis", "elo")}
        self.assertEqual(surface_weights, {0.4, 0.7, 0.9})

    def test_official_atp_draw_parser_preserves_slots_byes_and_stable_ids(self):
        catalog_text = """code,first_name,last_name,citizenship
a001,Alice,Alpha,FRA
b001,Beth,Beta,GBR
c001,Carla,Gamma,ESP
d001,Dana,Delta,USA
e001,Elena,Epsilon,ITA
f001,Farah,Zeta,TUN
g001,Greta,Eta,GER
h001,Hana,Theta,CZE
"""
        catalog = _parse_atp_player_catalog(catalog_text)
        entries = [
            ("ALPHA, Alice", "FRA"),
            ("Bye", ""),
            ("GAMMA, Carla", "ESP"),
            ("DELTA, Dana", "USA"),
            ("EPSILON, Elena", "ITA"),
            ("ZETA, Farah", "TUN"),
            ("ETA, Greta", "GER"),
            ("THETA, Hana", "CZE"),
        ]
        lines = []
        for index, (name, country) in enumerate(entries, 1):
            base = f" {index}   {name}" + (f"   {country}" if country else "")
            line = base.ljust(52)
            stage_one = {1: "A. Alpha", 3: "C. Gamma", 7: "G. Eta"}.get(index, "")
            stage_two = {2: "A. Alpha"}.get(index, "")
            if stage_one:
                line += stage_one
            line = line.ljust(83)
            if stage_two:
                line += stage_two
            lines.append(line)
        page = "Example Open\nMain Draw Singles\n" + "\n".join(lines) + "\nRound of 8\n"
        draw = _parse_atp_draw_pages([page], catalog)
        self.assertIsNotNone(draw)
        self.assertEqual(draw["slots"][0], "atp:a001")
        self.assertIsNone(draw["slots"][1])
        self.assertEqual(draw["recorded_winners"][0][:2], ["atp:a001", "atp:c001"])
        self.assertIsNone(draw["recorded_winners"][0][2])
        self.assertEqual(draw["recorded_winners"][1][0], "atp:a001")

    def test_tennis_draw_simulation_uses_surface_probability_and_locked_path(self):
        model = SurfaceBlendModel(lambda: EloModel(k=28), surface_weight=0.9)
        start = date(2026, 1, 1)
        for offset in range(12):
            model.update(
                Match(
                    start + timedelta(days=offset),
                    "atp:a",
                    "atp:b",
                    1.0,
                    metadata={"surface": "Clay"},
                )
            )
            model.update(
                Match(
                    start + timedelta(days=20 + offset),
                    "atp:a",
                    "atp:b",
                    0.0,
                    metadata={"surface": "Hard"},
                )
            )
        base = {
            "id": "tennis-test",
            "season": "2026",
            "teams": [
                {"id": "atp:a", "name": "Alice Alpha", "country": "FRA"},
                {"id": "atp:b", "name": "Beth Beta", "country": "GBR"},
            ],
            "draw_slots": ["atp:a", "atp:b"],
            "recorded_winners": [[None]],
            "round_labels": ["Final"],
            "complete": False,
        }
        clay = _simulate_tennis_draw({**base, "surface": "Clay"}, model, "elo", simulations=2000)
        hard = _simulate_tennis_draw({**base, "surface": "Hard"}, model, "elo", simulations=2000)
        clay_a = next(row for row in clay["participants"] if row["id"] == "atp:a")
        hard_a = next(row for row in hard["participants"] if row["id"] == "atp:a")
        self.assertGreater(clay_a["champion"], 0.5)
        self.assertLess(hard_a["champion"], 0.5)
        self.assertAlmostEqual(
            clay["upcoming_matches"][0]["probability_a"]
            + clay["upcoming_matches"][0]["probability_b"],
            1.0,
        )
        self.assertEqual(clay_a["next_match"]["surface"], "Clay")
        self.assertEqual([row["stage"] for row in clay_a["round_probabilities"]], ["Champion"])

    def test_completed_tennis_competition_replay_keeps_surface_metadata(self):
        schedule = {
            "label": "Example Open",
            "season": "2026",
            "cohort": "tennis",
            "surface": "Grass",
            "home_advantage": False,
            "fixtures": [
                {
                    "date": "2026-07-12",
                    "home_id": "atp:a",
                    "away_id": "atp:b",
                    "home_name": "Alice Alpha",
                    "away_name": "Beth Beta",
                    "home_goals": 1.0,
                    "away_goals": 0.0,
                    "is_bye": False,
                }
            ],
        }
        entities = {
            "atp:a": {"name": "Alice Alpha"},
            "atp:b": {"name": "Beth Beta"},
        }
        event_matches = _competition_matches(schedule, entities)
        self.assertEqual(len(event_matches), 1)
        self.assertFalse(event_matches[0].home_advantage)
        self.assertEqual(event_matches[0].metadata["surface"], "Grass")

    def test_individual_contribution_protocol_publishes_only_valid_historical_cohorts(self):
        protocol = individual_contribution_protocol()
        self.assertEqual(protocol["status"], "historical_cohorts_published")
        self.assertEqual(protocol["live_publication_unit"], "club or national team")
        self.assertIn("individual player", protocol["historical_publication_unit"])
        self.assertIn("lineup_trueskill", protocol["methods"])
        self.assertIn("rapm", protocol["methods"])
        self.assertIn("pairwise_chemistry", protocol["methods"])
        self.assertIn("hapm", protocol["methods"])
        self.assertIn("lapm", protocol["methods"])
        self.assertEqual(
            protocol["model_hierarchy"]["primary_baselines"],
            ["lineup_trueskill", "rapm"],
        )
        self.assertEqual(
            protocol["model_hierarchy"]["interaction_extensions"],
            ["pairwise_chemistry"],
        )
        self.assertEqual(
            protocol["model_hierarchy"]["dependency_aware_extensions"],
            ["hapm", "lapm"],
        )
        self.assertIn("chronological", protocol["model_hierarchy"]["promotion_rule"])
        self.assertEqual(protocol["methods"]["pairwise_chemistry"]["status"], "experimental; validation result is published per cohort")
        self.assertIn("within one team", protocol["methods"]["hapm"]["scope"])
        self.assertEqual(protocol["methods"]["lapm"]["scope"], "within one team; values are not compared across teams")
        self.assertEqual(protocol["release_gates"]["starting_lineup_coverage"], ">= 95% of eligible matches")
        self.assertIn("source licence", protocol["release_gates"]["publication_rights"])
        self.assertNotIn("shots", protocol["methods"]["lineup_trueskill"]["input"])

    def test_lineup_trueskill_rewards_winning_players_and_reduces_uncertainty(self):
        model = LineupTrueSkill(draw_probability=0.25)
        team_a = {"a1": 1.0, "a2": 1.0}
        team_b = {"b1": 1.0, "b2": 1.0}
        initial = model.state("a1").sigma
        for _ in range(4):
            model.update(team_a, team_b, 1.0)
        self.assertGreater(model.state("a1").mean, model.state("b1").mean)
        self.assertLess(model.state("a1").sigma, initial)

    def test_lineup_trueskill_probabilities_partition_one(self):
        probabilities = LineupTrueSkill().probabilities({"a": 1.0}, {"b": 1.0})
        self.assertAlmostEqual(sum(probabilities.values()), 1.0, places=9)
        self.assertTrue(all(0 <= value <= 1 for value in probabilities.values()))

    def test_position_segments_merge_without_double_counting_tactical_shifts(self):
        positions = [
            {"from": "00:00", "to": "45:00", "end_reason": "Tactical Shift"},
            {"from": "45:00", "to": None, "end_reason": "Final Whistle", "to_period": None},
        ]
        minutes, started, complete = _merge_minutes(positions, 90.0)
        self.assertAlmostEqual(minutes, 90.0)
        self.assertTrue(started)
        self.assertTrue(complete)

    def test_shared_pitch_overlap_uses_exact_intervals(self):
        left = [(0.0, 60.0), (75.0, 90.0)]
        right = [(30.0, 80.0)]
        self.assertAlmostEqual(_overlap_minutes(left, right), 35.0)

    def test_pair_ridge_identifies_residual_teammate_chemistry(self):
        additive = {
            "home_advantage": 0.0,
            "coefficients": {player: 0.0 for player in ("a", "b", "c", "d")},
        }
        rows = []
        for home_pair, away_pair, goal_difference in (
            (("a", "b"), ("c", "d"), 2.0),
            (("c", "d"), ("a", "b"), -2.0),
            (("a", "b"), ("c", "d"), 1.0),
        ):
            rows.append(
                {
                    "home": {home_pair[0]: 1.0, home_pair[1]: 1.0},
                    "away": {away_pair[0]: 1.0, away_pair[1]: 1.0},
                    "home_pairs": {home_pair: 1.0},
                    "away_pairs": {away_pair: 1.0},
                    "goal_difference": goal_difference,
                    "home_advantage": False,
                }
            )
        fitted = _fit_pair_ridge(rows, additive, 1.0)
        self.assertGreater(fitted["coefficients"][("a", "b")], fitted["coefficients"][("c", "d")])
        self.assertGreaterEqual(fitted["uncertainty"][("a", "b")], 0.0)

    def test_lapm_uses_jaccard_overlap_and_laplacian_smoothing(self):
        self.assertAlmostEqual(_jaccard(("a", "b"), ("b", "c")), 1.0 / 3.0)
        unsmoothed, _, _ = _laplacian_solve([2.0, -2.0], [1.0, 1.0], [(0, 1, 0.5)], 0.0, 0.01)
        smoothed, _, residual = _laplacian_solve([2.0, -2.0], [1.0, 1.0], [(0, 1, 0.5)], 2.0, 0.01)
        self.assertLess(abs(smoothed[0] - smoothed[1]), abs(unsmoothed[0] - unsmoothed[1]))
        self.assertLess(residual, 1e-6)

    def test_team_lapm_publishes_players_and_supported_combinations(self):
        stints = [
            {"match_id": 1, "lineup": ("a", "b", "c"), "minutes": 60.0, "goal_difference": 2.0},
            {"match_id": 2, "lineup": ("a", "b", "d"), "minutes": 30.0, "goal_difference": -1.0},
        ]
        fitted = _fit_team_lapm(
            stints, {"a", "b", "c", "d"}, 20.0, 1, 20.0, 1
        )
        self.assertEqual({row["players"][0] for row in fitted["players"]}, {"a", "b", "c", "d"})
        self.assertTrue(any(row["order"] == 2 for row in fitted["combinations"]))
        self.assertTrue(any(row["order"] == 3 for row in fitted["combinations"]))
        self.assertGreater(fitted["edges"], 0)

    def test_team_lapm_reapplies_eligibility_inside_each_team(self):
        fitted = _fit_team_lapm(
            [
                {
                    "match_id": 1,
                    "lineup": ("established", "transfer"),
                    "minutes": 9.0,
                    "goal_difference": 1.0,
                }
            ],
            {"established", "transfer"},
            20.0,
            1,
            5.0,
            1,
        )
        self.assertEqual(fitted["players"], [])

    def test_team_hapm_fits_players_and_bounded_generalized_lineups(self):
        stints = [
            {"match_id": 1, "lineup": ("a", "b", "c", "d", "e"), "minutes": 60.0, "goal_difference": 2.0},
            {"match_id": 2, "lineup": ("a", "b", "c", "d", "f"), "minutes": 60.0, "goal_difference": 1.0},
            {"match_id": 3, "lineup": ("a", "b", "c", "e", "f"), "minutes": 60.0, "goal_difference": 2.0},
            {"match_id": 4, "lineup": ("a", "b", "d", "e", "f"), "minutes": 60.0, "goal_difference": 1.0},
            {"match_id": 5, "lineup": ("g", "b", "c", "d", "e"), "minutes": 60.0, "goal_difference": -2.0},
            {"match_id": 6, "lineup": ("g", "b", "c", "d", "f"), "minutes": 60.0, "goal_difference": -1.0},
            {"match_id": 7, "lineup": ("g", "b", "c", "e", "f"), "minutes": 60.0, "goal_difference": -2.0},
            {"match_id": 8, "lineup": ("g", "b", "d", "e", "f"), "minutes": 60.0, "goal_difference": -1.0},
        ]
        fitted = _fit_team_hapm(
            stints, {"a", "b", "c", "d", "e", "f", "g"},
            20.0, 1, 20.0, 1,
        )
        player_impacts = {
            row["players"][0]: row["impact"] for row in fitted["players"]
        }
        self.assertGreater(player_impacts["a"], player_impacts["g"])
        self.assertEqual(set(fitted["nodes_by_order"]), {1, 2, 3, 4, 5})
        self.assertEqual(fitted["validation_matches"], 2)
        self.assertIn(fitted["selected_penalty"], (0.1, 1.0, 5.0, 20.0, 50.0))
        self.assertTrue(math.isfinite(fitted["validation_rmse"]))

    def test_rapm_ridge_assigns_positive_impact_to_repeated_winner(self):
        rows = [
            {"home": {"winner": 1.0}, "away": {"loser": 1.0}, "goal_difference": 2.0},
            {"home": {"loser": 1.0}, "away": {"winner": 1.0}, "goal_difference": -1.0},
            {"home": {"winner": 1.0}, "away": {"loser": 1.0}, "goal_difference": 1.0},
        ]
        fitted = _fit_ridge(rows, ["loser", "winner"], 1.0)
        self.assertGreater(fitted["coefficients"]["winner"], fitted["coefficients"]["loser"])
        self.assertGreaterEqual(fitted["uncertainty"]["winner"], 0.0)

    def test_tournament_home_advantage_requires_matching_stadium_country(self):
        definition = {"venue_context": "tournament"}
        hosted = {
            "home_team": {"country": {"name": "Germany"}},
            "stadium": {"country": {"name": "Germany"}},
        }
        neutral = {
            "home_team": {"country": {"name": "Spain"}},
            "stadium": {"country": {"name": "Germany"}},
        }
        self.assertTrue(_home_advantage(hosted, definition))
        self.assertFalse(_home_advantage(neutral, definition))

    def test_api_football_fixture_requires_verified_starters_substitutions_and_minutes(self):
        def team_payload(team_id, offset):
            starters = [offset + index for index in range(1, 12)]
            substitute = offset + 12
            return (
                {
                    "team": {"id": team_id, "name": f"Team {team_id}"},
                    "startXI": [{"player": {"id": player_id, "name": f"P{player_id}"}} for player_id in starters],
                    "substitutes": [{"player": {"id": substitute, "name": f"P{substitute}"}}],
                },
                {
                    "team": {"id": team_id, "name": f"Team {team_id}"},
                    "players": [
                        {
                            "player": {"id": player_id, "name": f"P{player_id}"},
                            "statistics": [{"games": {"minutes": 60 if index == 0 else 90}}],
                        }
                        for index, player_id in enumerate(starters)
                    ]
                    + [{"player": {"id": substitute, "name": f"P{substitute}"}, "statistics": [{"games": {"minutes": 30}}]}],
                },
                starters[0],
                substitute,
            )

        home_lineup, home_players, home_out, home_in = team_payload(10, 100)
        away_lineup, away_players, away_out, away_in = team_payload(20, 200)
        fixture = {
            "fixture": {"id": 999, "date": "2026-07-19T20:00:00+00:00"},
            "league": {"round": "Final"},
            "teams": {"home": {"id": 10, "name": "Home"}, "away": {"id": 20, "name": "Away"}},
            "goals": {"home": 1, "away": 0},
            "lineups": [home_lineup, away_lineup],
            "players": [home_players, away_players],
            "events": [
                {"team": {"id": 10}, "type": "Goal", "player": {"id": home_out}, "time": {"elapsed": 25}},
                {"team": {"id": 10}, "type": "subst", "player": {"id": home_out}, "assist": {"id": home_in}, "time": {"elapsed": 60}},
                {"team": {"id": 20}, "type": "subst", "player": {"id": away_out}, "assist": {"id": away_in}, "time": {"elapsed": 60}},
            ],
        }
        match, lineups, audit = _api_football_fixture(fixture)
        self.assertEqual(match["match_id"], 999)
        self.assertEqual(audit["substitution_players"], 4)
        self.assertEqual(audit["verified_substitution_players"], 4)
        player_meta = {}
        home, away, weights_audit = _lineup_weights(match, lineups, player_meta)
        self.assertAlmostEqual(sum(home.values()), 11.0)
        self.assertAlmostEqual(sum(away.values()), 11.0)
        self.assertTrue(weights_audit["integrity_ok"])
        self.assertEqual(weights_audit["home_intervals"][f"api-football:{home_out}"], [(0.0, 60.0)])
        self.assertEqual(weights_audit["home_intervals"][f"api-football:{home_in}"], [(60.0, 90.0)])

    def test_unavailable_optional_world_cup_does_not_block_public_cohorts(self):
        public_cohort = {
            "id": "verified-public-cohort",
            "source": {"name": "Public source", "url": "https://example.org/data"},
        }
        provider_error = RuntimeError(
            "Free plans do not have access to this season, try from 2022 to 2024."
        )
        with patch("rating_lab.player_pipeline._build_cohort", return_value=(public_cohort, b"snapshot")), patch(
            "rating_lab.player_pipeline._build_api_football_cohort",
            side_effect=provider_error,
        ):
            payload = build_player_payload(lambda *_args, **_kwargs: b"", "secret-key")
        self.assertEqual(payload["cohorts"], [public_cohort] * len(COHORTS))
        status = payload["source"]["statuses"]["api_football_world_cup_2026"]
        self.assertEqual(status["status"], "withheld")
        self.assertEqual(status["reason"], "provider_plan_does_not_include_2026")
        self.assertEqual(status["required_matches"], 104)
        self.assertIn("substitution minute", status["required_fields"])
        self.assertNotIn("2022 to 2024", status["message"])

    def test_recent_mens_league_cohorts_are_complete_and_request_bounded(self):
        self.assertEqual(
            [definition["id"] for definition in API_FOOTBALL_LEAGUE_COHORTS],
            [
                "premier-league-2022-23",
                "premier-league-2023-24",
                "premier-league-2024-25",
                "premier-league-2025-26",
            ],
        )
        for definition in API_FOOTBALL_LEAGUE_COHORTS:
            self.assertEqual(definition["competition_id"], 39)
            self.assertEqual(definition["expected_matches"], 380)
            self.assertEqual(definition["scope_type"], "season")
            self.assertEqual(definition["venue_context"], "home-and-away")
            self.assertEqual(definition["minimum_minutes"], 900.0)
            self.assertEqual(definition["minimum_matches"], 10)
        requests = sum(
            1 + math.ceil(definition["expected_matches"] / 20)
            for definition in (*API_FOOTBALL_LEAGUE_COHORTS, API_FOOTBALL_WORLD_CUP)
        )
        self.assertLessEqual(requests, 100)

    def test_rapm_neutral_matches_do_not_create_home_intercept(self):
        rows = [
            {"home": {"a": 1.0}, "away": {"b": 1.0}, "goal_difference": 2.0, "home_advantage": False},
            {"home": {"b": 1.0}, "away": {"a": 1.0}, "goal_difference": -2.0, "home_advantage": False},
        ]
        fitted = _fit_ridge(rows, ["a", "b"], 1.0)
        self.assertEqual(fitted["home_advantage"], 0.0)

    def test_player_schema_is_versioned_and_closed(self):
        schema = player_schema()
        self.assertEqual(schema["properties"]["schema_version"]["const"], "1.6.0")
        self.assertFalse(schema["additionalProperties"])

    def test_pages_workflow_regenerates_player_data_before_jekyll(self):
        workflow = (
            Path(__file__).resolve().parents[1]
            / ".github/workflows/refresh-and-deploy.yml"
        ).read_text()
        full_refresh = "python scripts/refresh_ratings.py --sports tennis football national-football chess"
        self.assertIn(full_refresh, workflow)
        self.assertEqual(workflow.count(full_refresh), 1)
        self.assertLess(workflow.index(full_refresh), workflow.index("actions/jekyll-build-pages"))
        self.assertIn("rating-lab-public-data-v4-", workflow)
        refresh_script = (
            Path(__file__).resolve().parents[1] / "scripts/refresh_ratings.py"
        ).read_text()
        self.assertIn("write_outputs(args.output, [], chess_months=args.chess_months)", refresh_script)
        self.assertNotIn('(args.output / "player-football.json").write_text', refresh_script)

    def test_player_snapshot_and_manifest_are_published_as_one_contract(self):
        sport_payload = {
            "latest_result": "2026-07-22",
            "generated_at": "2026-07-23T00:00:00+00:00",
            "source": {
                "source": "fixture",
                "stale_after_hours": 24,
                "license": "test",
                "source_url": "https://example.test",
                "snapshot_sha256": "source-hash",
            },
            "parameters": {},
        }
        player_payload = {
            "generated_at": "2026-07-23T01:00:00+00:00",
            "source": {
                "name": "Verified fixture",
                "statuses": {
                    "api_football_world_cup_2026": {
                        "status": "withheld",
                        "reason": "provider_plan_does_not_include_2026",
                    }
                },
            },
            "cohorts": [{"id": "verified-cohort"}],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            for sport in ("tennis", "football", "national-football", "chess"):
                (output / f"{sport}.json").write_text(json.dumps(sport_payload))
            with patch(
                "rating_lab.player_pipeline.build_player_payload",
                return_value=player_payload,
            ), patch(
                "rating_lab.player_pipeline.validate_player_payload"
            ), patch(
                "rating_lab.player_pipeline.player_schema",
                return_value={"type": "object"},
            ):
                manifest = write_outputs(output, [])
            player_bytes = (output / "player-football.json").read_bytes()
            published = json.loads((output / "manifest.json").read_text())
            self.assertEqual(
                manifest["player_football"]["snapshot_sha256"],
                hashlib.sha256(player_bytes).hexdigest(),
            )
            self.assertEqual(published["player_football"], manifest["player_football"])
            self.assertEqual(
                published["player_football"]["source_statuses"][
                    "api_football_world_cup_2026"
                ]["reason"],
                "provider_plan_does_not_include_2026",
            )

    def test_complete_season_rejects_partial_fixture_catalogue(self):
        definition = {
            "id": "partial-season", "competition_id": 2, "season_id": 27,
            "name": "Partial season", "country": "England", "gender": "men",
            "format": "club league season", "venue_context": "home-and-away",
            "expected_matches": 2,
        }
        fetch = lambda *_args, **_kwargs: json.dumps([{"match_id": 1}]).encode()
        with self.assertRaisesRegex(ValueError, "expected 2 matches"):
            _build_cohort(definition, fetch)

    def test_published_player_payload_passes_gates_and_has_contiguous_ranks(self):
        payload = json.loads((Path(__file__).resolve().parents[1] / "assets/data/rating-lab/player-football.json").read_text())
        validate_player_payload(payload)
        self.assertEqual(
            payload["methodology"]["model_hierarchy"]["primary_baselines"],
            ["lineup_trueskill", "rapm"],
        )
        self.assertEqual(
            payload["methodology"]["model_hierarchy"]["interaction_extensions"],
            ["pairwise_chemistry"],
        )
        self.assertEqual(
            payload["methodology"]["model_hierarchy"]["dependency_aware_extensions"],
            ["hapm", "lapm"],
        )
        cohort_ids = {cohort["id"] for cohort in payload["cohorts"]}
        self.assertTrue({"premier-league-2015-16", "euro-2024", "world-cup-2022"}.issubset(cohort_ids))
        self.assertEqual({definition["gender"] for definition in COHORTS}, {"men", "women"})
        premier = next(cohort for cohort in payload["cohorts"] if cohort["id"] == "premier-league-2015-16")
        self.assertEqual(premier["matches"], 380)
        self.assertEqual(premier["coverage"]["fixture_completeness"], 1.0)
        self.assertEqual(premier["eligibility"], {"minimum_minutes": 900.0, "minimum_matches": 10})
        for cohort in payload["cohorts"]:
            self.assertIn(cohort["gender"], {"men", "women"})
            self.assertGreaterEqual(cohort["coverage"]["starting_lineups"], 0.95)
            self.assertGreaterEqual(cohort["coverage"]["player_minutes"], 0.95)
            self.assertGreaterEqual(cohort["coverage"]["event_goal_scores"], 0.95)
            self.assertEqual(cohort["coverage"]["player_match_graph_components"], 1)
            self.assertIn(cohort["models"]["pairwise-chemistry"]["status"], {"supported", "descriptive_only"})
            self.assertIn("baseline_validation_rmse", cohort["models"]["pairwise-chemistry"]["metrics"])
            self.assertEqual(cohort["models"]["hapm"]["scope"], "within_team")
            self.assertEqual(cohort["models"]["hapm"]["status"], "experimental")
            self.assertEqual(
                cohort["models"]["hapm"]["metrics"]["release_status"],
                "experimental",
            )
            self.assertEqual(
                cohort["models"]["hapm"]["metrics"][
                    "teams_beating_full_lineup_baseline"
                ],
                cohort["models"]["hapm"]["metrics"]["supported_teams"],
            )
            self.assertTrue(cohort["models"]["hapm"]["teams"])
            self.assertEqual(cohort["models"]["lapm"]["scope"], "within_team")
            self.assertTrue(cohort["models"]["lapm"]["teams"])
            for model_id in ("lineup-trueskill", "rapm", "pairwise-chemistry"):
                model = cohort["models"][model_id]
                self.assertEqual(
                    [row["rank"] for row in model["rankings"]],
                    list(range(1, len(model["rankings"]) + 1)),
                )
            for model_id in ("hapm", "lapm"):
                for team in cohort["models"][model_id]["teams"]:
                    self.assertEqual(
                        [row["rank"] for row in team["rankings"]],
                        list(range(1, len(team["rankings"]) + 1)),
                    )
                    if model_id == "hapm":
                        self.assertLessEqual(
                            max(map(int, team["diagnostics"]["nodes_by_order"])),
                            11,
                        )
                        self.assertGreaterEqual(
                            team["diagnostics"]["omitted_overcomplete_stints"],
                            0,
                        )

    def test_polymarket_snapshot_matches_entities_and_preserves_raw_overround(self):
        competition = {
            "id": "football-epl",
            "label": "Premier League",
            "season": "2026-27",
            "models": {"elo": {"teams": [
                {"id": "football:name:arsenal-fc", "name": "Arsenal FC", "champion": 0.5},
                {"id": "football:name:chelsea-fc", "name": "Chelsea FC", "champion": 0.3},
                {"id": "football:name:brighton-hove-albion-fc", "name": "Brighton & Hove Albion FC", "champion": 0.2},
            ]}},
        }
        markets = []
        for index, (name, price) in enumerate((("Arsenal", 0.55), ("Chelsea", 0.32), ("Brighton", 0.18)), 1):
            markets.append({
                "id": index,
                "groupItemTitle": name,
                "outcomes": json.dumps(["Yes", "No"]),
                "outcomePrices": json.dumps([str(price), str(1 - price)]),
                "active": True,
                "closed": False,
                "liquidity": "1000",
                "volume": "5000",
                "bestBid": str(price - 0.01),
                "bestAsk": str(price + 0.01),
                "updatedAt": "2026-07-20T12:00:00Z",
            })
        event = {"id": 99, "slug": "epl-2027-champion", "title": "EPL: 2027 Champion", "markets": markets}
        snapshot = _polymarket_event_snapshot(competition, event)
        self.assertIsNotNone(snapshot)
        self.assertAlmostEqual(snapshot["raw_yes_price_sum"], 1.05)
        self.assertEqual(snapshot["matched_participants"], 3)
        self.assertEqual({row["entity_id"] for row in snapshot["outcomes"]}, {
            "football:name:arsenal-fc", "football:name:chelsea-fc", "football:name:brighton-hove-albion-fc"
        })
        self.assertAlmostEqual(sum(row["normalized_probability"] for row in snapshot["outcomes"]), 1.0, places=5)

    def test_polymarket_query_uses_season_end_year(self):
        competition = {"id": "football-epl", "label": "Premier League", "season": "2026-27"}
        self.assertEqual(_polymarket_search_query(competition), "Premier League 2027 champion")

    def test_kalshi_snapshot_uses_midpoints_and_preserves_raw_field_sum(self):
        competition = {
            "id": "premier-league",
            "label": "Premier League",
            "season": "2026-27",
            "models": {"elo": {"teams": [
                {"id": "football:name:arsenal-fc", "name": "Arsenal FC", "champion": 0.5},
                {"id": "football:name:chelsea-fc", "name": "Chelsea FC", "champion": 0.3},
                {"id": "football:name:brighton-hove-albion-fc", "name": "Brighton & Hove Albion FC", "champion": 0.2},
            ]}},
        }
        markets = []
        for name, ticker, bid, ask in (
            ("Arsenal", "ARS", 0.51, 0.53),
            ("Chelsea", "CHE", 0.29, 0.31),
            ("Brighton", "BHA", 0.17, 0.19),
        ):
            markets.append({
                "ticker": f"KXPREMIERLEAGUE-27-{ticker}",
                "yes_sub_title": name,
                "status": "active",
                "yes_bid_dollars": str(bid),
                "yes_ask_dollars": str(ask),
                "last_price_dollars": str(bid),
                "liquidity_dollars": "1000",
                "volume_fp": "5000",
                "updated_time": "2026-07-22T12:00:00Z",
            })
        event = {
            "event_ticker": "KXPREMIERLEAGUE-27",
            "series_ticker": "KXPREMIERLEAGUE",
            "title": "English Premier League Champion",
            "mutually_exclusive": True,
            "markets": markets,
        }
        snapshot = _kalshi_event_snapshot(competition, event, "premier-league")
        self.assertIsNotNone(snapshot)
        self.assertAlmostEqual(snapshot["raw_yes_price_sum"], 1.0)
        self.assertEqual(snapshot["matched_participants"], 3)
        self.assertAlmostEqual(sum(row["normalized_probability"] for row in snapshot["outcomes"]), 1.0)
        self.assertTrue(all(row["quote_method"] == "yes bid-ask midpoint" for row in snapshot["outcomes"]))
        self.assertIn("kalshi.com/markets/kxpremierleague", snapshot["event_url"])

    def test_market_identity_aliases_cover_provider_names(self):
        self.assertEqual(_market_identity_tokens("FC Bayern München"), _market_identity_tokens("Bayern Munich"))
        self.assertEqual(_market_identity_tokens("Paris Saint-Germain FC"), _market_identity_tokens("PSG"))
        self.assertEqual(_market_identity_tokens("FC Internazionale Milano"), _market_identity_tokens("Inter Milan"))

    def test_market_history_freezes_simultaneous_models_and_scores_resolution(self):
        model_probabilities = {
            "elo": (0.7, 0.3),
            "glicko2": (0.65, 0.35),
            "trueskill": (0.6, 0.4),
            "robust": (0.55, 0.45),
        }
        competition = {
            "id": "premier-league",
            "label": "Premier League",
            "season": "2026-27",
            "state": "finished",
            "last_fixture": "2027-05-23",
            "models": {
                model_name: {
                    "teams": [
                        {"id": "arsenal", "name": "Arsenal", "champion": 1.0 if model_name == "elo" else probabilities[0]},
                        {"id": "chelsea", "name": "Chelsea", "champion": 0.0 if model_name == "elo" else probabilities[1]},
                    ]
                }
                for model_name, probabilities in model_probabilities.items()
            },
        }
        current = {
            "status": "current",
            "source": "Polymarket Gamma API",
            "fetched_at": "2026-08-01T12:00:00+00:00",
            "checked_at": "2026-08-01T12:00:00+00:00",
            "competitions": [{
                "competition_id": "premier-league",
                "event_id": "99",
                "event_title": "Premier League Champion",
                "event_url": "https://polymarket.com/event/premier-league",
                "snapshot_sha256": "a" * 64,
                "matched_participants": 2,
                "model_participants": 2,
                "coverage": 1.0,
                "raw_yes_price_sum": 1.0,
                "outcomes": [
                    {"entity_id": "arsenal", "normalized_probability": 0.6},
                    {"entity_id": "chelsea", "normalized_probability": 0.4},
                ],
            }],
            "searches": [{"competition_id": "premier-league", "status": "matched"}],
        }
        benchmark = _finalize_market_comparison(
            current,
            None,
            [competition],
            "Polymarket",
        )
        self.assertEqual(len(benchmark["history"]), 1)
        history = benchmark["history"][0]
        self.assertEqual(history["snapshot_date"], "2026-08-01")
        self.assertEqual(set(history["model_forecasts"]), set(model_probabilities))
        self.assertEqual(history["resolution"]["winner_name"], "Arsenal")
        self.assertAlmostEqual(
            history["resolution"]["scores"]["market"]["log_loss"],
            -math.log(0.6),
            places=6,
        )
        self.assertAlmostEqual(
            history["resolution"]["scores"]["market"]["brier"],
            0.32,
            places=6,
        )
        self.assertEqual(benchmark["benchmark"]["status"], "scored")
        self.assertEqual(
            {row["id"] for row in benchmark["benchmark"]["forecasters"]},
            {"market", "elo", "glicko2", "trueskill", "robust"},
        )
        next_season = json.loads(json.dumps(competition))
        next_season["season"] = "2027-28"
        next_season["state"] = "upcoming"
        retained = _finalize_market_comparison(
            {
                "status": "current",
                "source": "Polymarket Gamma API",
                "fetched_at": "2027-07-20T12:00:00+00:00",
                "checked_at": "2027-07-20T12:00:00+00:00",
                "competitions": [],
                "searches": [],
            },
            benchmark,
            [next_season],
            "Polymarket",
        )
        self.assertEqual(retained["benchmark"]["status"], "scored")
        self.assertEqual(retained["benchmark"]["resolved_competitions"], 1)

    def test_market_history_keeps_one_latest_snapshot_per_utc_day(self):
        competition = {
            "id": "premier-league",
            "label": "Premier League",
            "season": "2026-27",
            "state": "upcoming",
            "models": {
                model_name: {"teams": [
                    {"id": "arsenal", "name": "Arsenal", "champion": 0.6},
                    {"id": "chelsea", "name": "Chelsea", "champion": 0.4},
                ]}
                for model_name in ("elo", "glicko2", "trueskill", "robust")
            },
        }

        def provider(fetched_at, snapshot_hash, arsenal_probability):
            return {
                "status": "current",
                "source": "Kalshi Trade API",
                "fetched_at": fetched_at,
                "checked_at": fetched_at,
                "competitions": [{
                    "competition_id": "premier-league",
                    "event_id": "EPL-27",
                    "event_title": "Premier League Champion",
                    "event_url": "https://kalshi.com/markets/epl",
                    "snapshot_sha256": snapshot_hash,
                    "matched_participants": 2,
                    "model_participants": 2,
                    "coverage": 1.0,
                    "raw_yes_price_sum": 1.0,
                    "outcomes": [
                        {"entity_id": "arsenal", "normalized_probability": arsenal_probability},
                        {"entity_id": "chelsea", "normalized_probability": 1 - arsenal_probability},
                    ],
                }],
                "searches": [{"competition_id": "premier-league", "status": "matched"}],
            }

        first = _finalize_market_comparison(
            provider("2026-08-01T08:00:00+00:00", "a" * 64, 0.55),
            None,
            [competition],
            "Kalshi",
        )
        replacement = _finalize_market_comparison(
            provider("2026-08-01T18:00:00+00:00", "b" * 64, 0.57),
            first,
            [competition],
            "Kalshi",
        )
        second_day = _finalize_market_comparison(
            provider("2026-08-02T18:00:00+00:00", "c" * 64, 0.58),
            replacement,
            [competition],
            "Kalshi",
        )
        self.assertEqual(len(replacement["history"]), 1)
        self.assertEqual(replacement["history"][0]["snapshot_sha256"], "b" * 64)
        self.assertEqual(len(second_day["history"]), 2)
        self.assertEqual(second_day["benchmark"]["status"], "awaiting_resolutions")

    def test_categorical_market_score_uses_explicit_other_bin(self):
        score = _categorical_forecast_score(
            {
                "probabilities": {"arsenal": 0.4, "chelsea": 0.3},
                "other_probability": 0.3,
            },
            "unmatched-winner",
        )
        self.assertAlmostEqual(score["winner_probability"], 0.3)
        self.assertAlmostEqual(score["log_loss"], -math.log(0.3), places=6)
        self.assertAlmostEqual(score["brier"], 0.16 + 0.09 + 0.49, places=6)

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
        self.assertEqual(
            [team["expected_points"] for team in first["teams"]],
            sorted((team["expected_points"] for team in first["teams"]), reverse=True),
        )

    def test_competition_state_machine_is_format_independent(self):
        competition = {
            "format": "round-robin league",
            "last_fixture": "2026-08-09",
        }
        upcoming = {
            "fixtures": [
                {"home_goals": None, "away_goals": None},
                {"home_goals": None, "away_goals": None},
            ]
        }
        live = {
            "fixtures": [
                {"home_goals": 2, "away_goals": 1},
                {"home_goals": None, "away_goals": None},
            ]
        }
        finished = {
            "fixtures": [
                {"home_goals": 2, "away_goals": 1},
                {"home_goals": 0, "away_goals": 0},
            ]
        }
        self.assertEqual(_competition_state(upcoming, competition, {})[0], "upcoming")
        self.assertEqual(_competition_state(live, competition, {})[0], "live")
        self.assertEqual(_competition_state(finished, competition, {})[0], "finished")

        knockout = {
            "format": "knockout cup",
            "last_fixture": "2026-07-19",
        }
        self.assertEqual(
            _competition_state(live, knockout, {"elo": {"current_stage": "Complete"}})[0],
            "finished",
        )
        self.assertEqual(
            _competition_state(upcoming, knockout, {"elo": {"current_stage": "Quarter Finals"}})[0],
            "upcoming",
        )

    def test_completed_competition_performance_replays_from_pre_event_state(self):
        entities = {
            "football:name:alpha": {"name": "Alpha"},
            "football:name:beta": {"name": "Beta"},
        }
        prior = [
            Match(date(2025, 8, 1), "football:name:alpha", "football:name:beta", 0.5, "Old League", "2025-26", True),
            Match(date(2025, 9, 1), "football:name:beta", "football:name:alpha", 0.0, "Old League", "2025-26", True),
        ]
        schedule = {
            "id": "finished-cup",
            "label": "Finished Cup",
            "season": "2025-26",
            "cohort": "football",
            "home_advantage": True,
            "fixtures": [
                {"date": "2026-02-01", "home_name": "Alpha", "away_name": "Beta", "home_goals": 2, "away_goals": 0},
                {"date": "2026-02-08", "home_name": "Beta", "away_name": "Alpha", "home_goals": 1, "away_goals": 1},
            ],
        }
        result = _competition_performance(schedule, EloModel(k=24, home=65), "elo", entities, prior)
        self.assertEqual(result["results"], 2)
        self.assertEqual(len(result["participants"]), 2)
        alpha = next(row for row in result["participants"] if row["name"] == "Alpha")
        self.assertEqual((alpha["wins"], alpha["draws"], alpha["losses"]), (1, 1, 0))
        self.assertGreater(alpha["performance_delta"], 0)
        self.assertGreater(alpha["performance_rating"], alpha["start_rating"])
        self.assertGreaterEqual(alpha["reset_rank"], 1)
        self.assertTrue(math.isfinite(alpha["reset_rating"]))
        self.assertGreater(alpha["score_residual"], 0)
        self.assertGreater(alpha["surprise_index"], 0)
        self.assertAlmostEqual(sum(row["expected_score"] for row in result["participants"]), 2.0, places=3)
        self.assertAlmostEqual(sum(row["score_residual"] for row in result["participants"]), 0.0, places=3)
        self.assertAlmostEqual(sum(row["replay_change"] for row in result["participants"]), 0, places=1)
        self.assertIn("immediately before", result["surprise_method"])

        protocol_models = {
            "glicko2": Glicko2Model(home=65),
            "trueskill": GaussianSkillModel(advantage=1.35, draw_margin=1.35),
            "robust": GaussianSkillModel(robust=True, advantage=1.35, draw_margin=1.35),
        }
        for model_name, reference_model in protocol_models.items():
            with self.subTest(model=model_name):
                protocol_result = _competition_performance(
                    schedule, reference_model, model_name, entities, prior
                )
                self.assertAlmostEqual(
                    sum(row["expected_score"] for row in protocol_result["participants"]),
                    2.0,
                    places=3,
                )
                self.assertAlmostEqual(
                    sum(row["score_residual"] for row in protocol_result["participants"]),
                    0.0,
                    places=3,
                )
                self.assertTrue(
                    all(math.isfinite(row["surprise_index"]) for row in protocol_result["participants"])
                )
                self.assertTrue(
                    all(math.isfinite(row["performance_rating"]) for row in protocol_result["participants"])
                )
                self.assertEqual(
                    sorted(row["reset_rank"] for row in protocol_result["participants"]),
                    list(range(1, len(protocol_result["participants"]) + 1)),
                )

    def test_completed_competition_normalizes_schedule_aliases(self):
        schedule = {
            "label": "World Cup",
            "season": "2026",
            "cohort": "national-football",
            "fixtures": [{
                "date": "2026-07-01",
                "home_name": "USA",
                "away_name": "Spain",
                "home_id": "national-football:usa",
                "away_id": "national-football:spain",
                "home_goals": 1,
                "away_goals": 2,
            }],
        }
        entities = {
            "national-football:united-states": {"name": "United States"},
            "national-football:spain": {"name": "Spain"},
        }
        result = _competition_matches(schedule, entities)
        self.assertEqual(result[0].entity_a, "national-football:united-states")

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
        self.assertEqual(len(first["ties"]), 2)
        self.assertTrue(all(tie["completed_legs"] == 0 for tie in first["ties"]))
        self.assertAlmostEqual(sum(team["champion"] for team in first["participants"]), 1.0, places=3)

    def test_uefa_qualifying_parser_and_current_round_forecast(self):
        article = b"""
<h2><b>First qualifying round</b></h2>
<h3><b>First legs</b></h3><p><b>Tuesday 7 July</b></p><p><b>Champions path</b></p>
<p><a href="https://www.uefa.com/uefachampionsleague/match/1--alpha-vs-beta/">Alpha 2-0 Beta</a></p>
<h3><b>Second legs</b></h3><p><b>Tuesday 14 July</b></p>
<p><a href="https://www.uefa.com/uefachampionsleague/match/2--beta-vs-alpha/">Beta 1-1 <b>Alpha</b> (agg: 1-3)</a></p>
<h2><b>Second qualifying round</b></h2>
<h3><b>First legs</b></h3><p><b>Tuesday 21 July</b></p><p><b>League path</b></p>
<p><a href="https://www.uefa.com/uefachampionsleague/match/3--alpha-vs-gamma/">Alpha vs Gamma</a></p>
<h3><b>Second legs</b></h3><p><b>Tuesday 28 July</b></p>
<p><a href="https://www.uefa.com/uefachampionsleague/match/4--gamma-vs-alpha/">Gamma vs Alpha</a></p>
"""
        competition = _parse_uefa_ucl_qualifying(article)
        self.assertIsNotNone(competition)
        self.assertEqual(competition["active_round"], "SECOND_QUALIFYING")
        self.assertEqual(competition["next_fixture"], "2026-07-21")
        self.assertEqual(len(competition["fixtures"]), 4)
        self.assertEqual(competition["fixtures"][1]["away_name"], "Alpha")
        model = EloModel(home=65)
        model.state("football:name:alpha").mean = 1700
        first = _simulate_qualifying_round(competition, model, "elo", simulations=300)
        second = _simulate_qualifying_round(competition, model, "elo", simulations=300)
        self.assertEqual(first, second)
        self.assertEqual(first["current_stage"], "Second qualifying round")
        self.assertEqual(first["target_label"], "Reach third qualifying round")
        self.assertEqual(first["published_ties_remaining"], 1)
        self.assertEqual(first["ties"][0]["remaining_legs"], 2)
        self.assertEqual(first["ties"][0]["completed_legs"], 0)
        self.assertAlmostEqual(sum(row["reach_next_stage"] for row in first["participants"]), 1.0, places=3)
        between_rounds = _parse_uefa_ucl_qualifying(
            article.replace(b"Alpha vs Gamma", b"Alpha 1-0 Gamma").replace(b"Gamma vs Alpha", b"Gamma 0-0 Alpha")
        )
        self.assertEqual(between_rounds["active_round"], "THIRD_QUALIFYING")
        self.assertFalse(between_rounds["forecast_available"])
        self.assertIn("waiting for UEFA", between_rounds["availability"])

    def test_cup_parser_withholds_title_forecast_before_knockout_field(self):
        payload = {"matches": [{
            "utcDate": "2026-09-01T18:00:00Z",
            "status": "SCHEDULED",
            "stage": "GROUP_STAGE",
            "group": "A",
            "homeTeam": {"id": 1, "name": "Alpha", "crest": "https://crests.football-data.org/1.svg"},
            "awayTeam": {"id": 2, "name": "Beta", "crest": "https://crests.football-data.org/2.png"},
            "score": {"winner": None, "fullTime": {"home": None, "away": None}},
            "season": {"startDate": "2026-08-01"},
        }]}
        body = json.dumps(payload).encode()
        competition = _parse_cup_schedule(payload, "WC", "World Cup", "national-football", "https://example.test", body)
        self.assertIsNotNone(competition)
        self.assertFalse(competition["forecast_available"])
        self.assertIn("no title probability", competition["availability"])
        self.assertEqual(competition["teams"][0]["media"]["kind"], "crest")

    def test_media_hosts_and_schedule_identity_merge_are_explicit(self):
        self.assertIsNotNone(_football_data_crest_media("https://crests.football-data.org/65.png"))
        self.assertIsNone(_football_data_crest_media("http://crests.football-data.org/65.png"))
        self.assertIsNone(_football_data_crest_media("https://example.test/65.png"))
        media = _football_data_crest_media("https://crests.football-data.org/65.png")
        entities = {"national-football:spain": {"name": "Spain"}}
        schedules = [{"teams": [{"id": "different-id", "name": "Spain", "media": media}]}]
        _merge_schedule_media(entities, schedules)
        self.assertEqual(entities["national-football:spain"]["media"]["url"], media["url"])

    def test_flags_are_vendored_svg_assets_not_emoji_glyphs(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / "assets/js/rating-lab.js").read_text()
        self.assertNotIn("flagEmoji", script)
        self.assertNotIn("subdivisionFlag", script)
        self.assertIn("data-flag-image", script)
        for code in ("ar", "ca", "de", "es", "fr", "gb-eng", "it", "rs", "us", "xk"):
            asset = root / "assets/vendor/flag-icons/4x3" / f"{code}.svg"
            self.assertTrue(asset.is_file(), f"Missing vendored flag asset: {code}")
            self.assertIn("<svg", asset.read_text()[:500])
        self.assertIn("MIT License", (root / "assets/vendor/flag-icons/LICENSE").read_text())

    def test_dashboard_trust_guards_are_present(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / "assets/js/rating-lab.js").read_text()
        page = (root / "rating-lab.md").read_text()
        styles = (root / "assets/main.scss").read_text()
        self.assertIn("function signedNumber(value, digits)", script)
        self.assertIn("Object.is(rounded, -0)", script)
        self.assertIn("row.id === selectedId ? ' selected'", script)
        self.assertIn("var isPreseason = isLeague && model.completed_matches === 0;", script)
        self.assertIn("Market gap withheld before play", script)
        self.assertIn("if (!state.includeProvisional)", script)
        self.assertIn("Math.abs(row.change30) >= 0.05", script)
        self.assertIn('competition_state == "finished"', (root / "rating_lab/pipeline.py").read_text())
        self.assertIn("b.champion - a.champion", script)
        self.assertIn("spread reflects starting ratings and schedule priors", script)
        self.assertIn('id="rating-include-provisional"', page)
        self.assertIn("var pageSize = mobile ? 6 : 20;", script)
        self.assertIn("elements.metricsDisclosure.open = false;", script)
        self.assertIn('class="rating-lab-market-detail"', script)
        self.assertIn("view.predictor.kalshi_comparison", script)
        self.assertIn("No eligible market found", script)
        self.assertIn("Benchmark clock:", script)
        self.assertIn("resolvedMarketProviderCard", script)
        self.assertIn("Kalshi Trade API", page)
        self.assertIn(".rating-lab-market-provider", styles)
        self.assertIn('class="rating-lab-title-mobile"', page)
        self.assertIn('aria-label="Competition forecasts"', page)
        self.assertIn("Rating Lab mobile-first interaction pass", styles)
        self.assertNotIn("Colors only identify the outcomes", script)
        self.assertIn('autocomplete="off"', page)

    def test_mobile_audit_guards_keep_core_data_visible(self):
        root = Path(__file__).resolve().parents[1]
        page = (root / "rating-lab.md").read_text()
        player_page = (root / "player-lab.md").read_text()
        script = (root / "assets/js/rating-lab.js").read_text()
        player_script = (root / "assets/js/player-lab.js").read_text()
        styles = (root / "assets/main.scss").read_text()

        self.assertIn("<noscript>This interactive leaderboard requires JavaScript.</noscript>", page)
        self.assertIn("<noscript>This player leaderboard requires JavaScript.</noscript>", player_page)
        self.assertNotIn('<noscript><p class="rating-lab-notice">', page + player_page)
        self.assertIn("Rating Lab mobile audit corrections", styles)
        self.assertIn("overflow-wrap: anywhere", styles)
        self.assertIn(".rating-lab-predictor-table.is-league:not(.is-preseason) .rating-lab-optional", styles)
        self.assertIn(".player-lab-table th:nth-child(n + 4)", styles)
        self.assertIn("font-size: 16px", styles)
        self.assertIn("rating-lab-mobile-change", script)
        self.assertIn('data-label="Candidates tested"', script)
        self.assertIn("elements.scoreHeading.textContent = 'Score';", player_script)
        self.assertIn("Math.floor(elements.chart.clientWidth || 330)", player_script)
        self.assertIn('data-flag-root=', player_page)
        self.assertIn("playerFlag(point.country", player_script)
        self.assertIn("String(row.country || '').toLocaleLowerCase()", player_script)
        self.assertIn("search a country to isolate it", player_script)
        self.assertIn("player-lab-point-card", player_script)
        self.assertIn("var pageSize = isMobile() ? 10 : 30;", player_script)
        self.assertIn("state.detailOpen = !chartPoint", player_script)
        self.assertIn('data-player-model="hapm"', player_page)
        self.assertIn("HAPM · experimental", player_script)
        self.assertIn("HAPM remains experimental.", player_script)
        self.assertIn("teams_beating_full_lineup_baseline", player_script)
        self.assertIn('id="player-filters-return"', player_page)
        self.assertIn('class="rating-lab-local-nav player-lab-local-nav"', player_page)
        self.assertIn('id="player-quick-model-trigger"', player_page)
        self.assertIn('id="player-controls"', player_page)
        self.assertNotIn('id="player-scope" open', player_page)
        self.assertNotIn('id="player-methods" open', player_page)
        self.assertIn("World Cup 2026 data access required.", player_script)
        self.assertIn("Historical Player Lab: compact mobile cards", styles)
        self.assertIn("Historical Player Lab mobile shell", styles)
        self.assertIn(".player-lab-detail.is-active", styles)
        self.assertIn('class="rating-lab-media-policy"', page)
        self.assertIn("Rating Lab mobile redesign", styles)
        self.assertIn("#ranking-table tbody tr", styles)
        self.assertIn(".rating-lab-predictor-table caption", styles)
        self.assertIn('id="rating-mobile-filter-sheet"', page)
        self.assertIn('id="rating-mobile-model-tabs"', page)
        self.assertIn("rating-lab-mobile-row-expansion", script)
        self.assertIn("showModal", script)
        self.assertIn("IntersectionObserver", script)
        self.assertIn("Rating Lab mobile market-pattern pass", styles)
        self.assertIn("position: fixed", styles)
        self.assertIn("env(safe-area-inset-bottom)", styles)
        self.assertIn('id="rating-quick-model"', page)
        self.assertIn('id="player-quick-model"', player_page)
        self.assertIn("function updateQuickModel()", script)
        self.assertIn("function updateQuickModel()", player_script)
        self.assertIn("Compact, context-aware model access", styles)
        self.assertIn("prefers-reduced-motion: reduce", styles)

    def test_open_cup_json_uses_penalties_to_resolve_final(self):
        payload = {"matches": [{
            "round": "Final",
            "date": "2026-07-19",
            "team1": "Alpha",
            "team2": "Beta",
            "score": {"ft": [1, 1], "et": [1, 1], "p": [5, 4]},
        }]}
        competition = _parse_open_cup_json(json.dumps(payload).encode(), "WC", "World Cup", "2026")
        self.assertTrue(competition["forecast_available"])
        final = competition["knockout_fixtures"][0]
        self.assertEqual(final["winner_id"], "national-football:alpha")
        self.assertEqual(final["status"], "FINISHED")

    def test_football_txt_parser_reads_penalty_score_before_suffix(self):
        fixture = """= Cup 2025/26
▪ Finals, Final
  Sat May 30 2026
    18:00  Alpha FC (ENG) v Beta FC (ESP)  4-3 pen. 1-1 a.e.t. (1-1, 0-1)
"""
        competition = _parse_football_txt(fixture, "cup", "Cup", "2025-26")
        self.assertEqual(competition["fixtures"][0]["away_name"], "Beta FC (ESP)")
        self.assertEqual(competition["fixtures"][0]["home_goals"], 4)

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

    def test_football_source_rejects_partial_required_coverage(self):
        seasons = _required_football_seasons(2020, 2026)
        self.assertEqual(seasons, [2023, 2024, 2025])
        counts = {
            (code, year): 1
            for year in seasons
            for code in FOOTBALL_COMPETITIONS
        }
        _validate_football_coverage(counts, seasons)
        counts.pop(("PL", 2025))
        with self.assertRaisesRegex(RuntimeError, "PL:2025"):
            _validate_football_coverage(counts, seasons)

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
        self.assertEqual(set(payload["models"]), {"elo", "glicko2", "trueskill", "robust"})
        self.assertIn("candidate_parameters", payload)
        self.assertFalse(payload["media"]["model_input"])
        self.assertEqual(payload["data_window"]["matches"], len(matches))
        self.assertEqual(payload["outcome_context"]["matches"], len(matches))
        self.assertEqual(payload["outcome_context"]["draw_rate"], 0.0)
        self.assertIn("publication eligibility", payload["outcome_context"]["method"])

    def test_football_elo_separates_small_disconnected_components(self):
        start = date(2026, 1, 1)
        established_pairs = (("a", "b"), ("b", "c"), ("c", "a"))
        matches = [
            Match(
                start + timedelta(days=index),
                *established_pairs[index % len(established_pairs)],
                0.5,
                "Premier League",
                "2025",
                True,
            )
            for index in range(18)
        ]
        matches.extend(
            Match(
                start + timedelta(days=20 + index),
                "new-a",
                "new-b",
                1.0,
                "Champions League qualifying",
                "2025",
                True,
            )
            for index in range(2)
        )
        entities = {
            entity: {
                "name": entity,
                "country": "",
                "competition": "Premier League" if entity in {"a", "b", "c"} else "Champions League qualifying",
                "active": True,
            }
            for entity in ("a", "b", "c", "new-a", "new-b")
        }
        source = {
            "source": "Fixture",
            "source_url": "https://example.test",
            "license": "Test",
            "latest_result": matches[-1].date.isoformat(),
            "stale_after_hours": 48,
        }

        payload = build_sport_payload("football", matches, entities, source)
        elo_rows = {row["id"]: row for row in payload["models"]["elo"]["rankings"]}

        self.assertGreater(elo_rows["new-a"]["rating"], elo_rows["a"]["rating"])
        self.assertTrue(elo_rows["new-a"]["provisional"])
        self.assertIn("not yet connected", elo_rows["new-a"]["provisional_reason"])
        self.assertGreater(
            elo_rows["new-a"]["rank"],
            max(elo_rows[entity]["rank"] for entity in ("a", "b", "c")),
        )
        self.assertFalse(elo_rows["a"]["provisional"])
        self.assertNotIn(
            "provisional",
            next(row for row in payload["models"]["trueskill"]["rankings"] if row["id"] == "new-a"),
        )
        self.assertEqual(payload["eligibility"]["football_elo_established_matches"], 10)

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


class SplitAssetTests(unittest.TestCase):
    @staticmethod
    def _sport_payload(sport: str) -> dict:
        return {
            "schema_version": "1.15.0",
            "sport": sport,
            "generated_at": "2026-07-23T22:01:36+00:00",
            "models": {
                "elo": {
                    "label": "Elo",
                    "metrics": {"brier": 0.2},
                    "rankings": [{"id": "a", "rank": 1}, {"id": "b", "rank": 2}],
                },
                "robust": {
                    "label": "Robust",
                    "metrics": {"brier": 0.19},
                    "rankings": [{"id": "b", "rank": 1}],
                },
            },
            "competitions": [{"id": "league"}],
        }

    @staticmethod
    def _player_payload(cohort_ids: list[str]) -> dict:
        return {
            "schema_version": "3.0.0",
            "generated_at": "2026-07-23T22:01:36+00:00",
            "source": {"name": "Test", "statuses": {}},
            "methodology": {"note": "test"},
            "cohorts": [
                {
                    "id": cohort_id,
                    "name": cohort_id,
                    "gender": "men",
                    "scope_type": "season",
                    "matches": 2,
                    "models": {"lineup-trueskill": {"label": "Lineup", "rankings": [{"id": "p1"}]}},
                }
                for cohort_id in cohort_ids
            ],
        }

    def test_split_assets_mirror_full_payloads(self):
        from rating_lab.pipeline import write_split_assets

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "tennis.json").write_text(json.dumps(self._sport_payload("tennis")))
            (output / "player-football.json").write_text(
                json.dumps(self._player_payload(["euro-2024", "wsl-2023-24"]))
            )
            written = write_split_assets(output)
            split = output / "split"
            core = json.loads((split / "tennis-core.json").read_text())
            self.assertNotIn("rankings", core["models"]["elo"])
            self.assertEqual(core["models"]["elo"]["entity_count"], 2)
            self.assertEqual(core["models"]["elo"]["rankings_url"], "tennis-rankings-elo.json")
            self.assertEqual(core["models"]["elo"]["label"], "Elo")
            self.assertEqual(core["models"]["elo"]["metrics"], {"brier": 0.2})
            self.assertEqual(core["competitions"], [{"id": "league"}])
            for model_name in ("elo", "robust"):
                part = json.loads((split / f"tennis-rankings-{model_name}.json").read_text())
                self.assertEqual(part["generated_at"], "2026-07-23T22:01:36+00:00")
                self.assertEqual(
                    part["rankings"],
                    self._sport_payload("tennis")["models"][model_name]["rankings"],
                )
            index = json.loads((split / "player-index.json").read_text())
            self.assertEqual(len(index["cohorts"]), 2)
            self.assertNotIn("models", index["cohorts"][0])
            self.assertEqual(index["cohorts"][0]["data_url"], "player-cohort-euro-2024.json")
            self.assertEqual(index["source"], {"name": "Test", "statuses": {}})
            cohort = json.loads((split / "player-cohort-euro-2024.json").read_text())
            self.assertEqual(
                cohort["cohort"], self._player_payload(["euro-2024"])["cohorts"][0]
            )
            self.assertEqual(set(written), {path.name for path in split.iterdir()})

    def test_split_assets_remove_stale_parts(self):
        from rating_lab.pipeline import write_split_assets

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "tennis.json").write_text(json.dumps(self._sport_payload("tennis")))
            (output / "player-football.json").write_text(
                json.dumps(self._player_payload(["euro-2024", "wsl-2023-24"]))
            )
            write_split_assets(output)
            self.assertTrue((output / "split/player-cohort-wsl-2023-24.json").exists())
            (output / "player-football.json").write_text(
                json.dumps(self._player_payload(["euro-2024"]))
            )
            write_split_assets(output)
            self.assertFalse((output / "split/player-cohort-wsl-2023-24.json").exists())
            self.assertTrue((output / "split/player-cohort-euro-2024.json").exists())
            self.assertTrue((output / "split/tennis-rankings-elo.json").exists())

    def test_player_default_ranking_is_rapm_with_honest_lineup_framing(self):
        root = Path(__file__).resolve().parents[1]
        page = (root / "player-lab.md").read_text()
        script = (root / "assets/js/player-lab.js").read_text()
        pipeline = (root / "rating_lab/player_pipeline.py").read_text()
        styles = (root / "assets/main.scss").read_text()
        # RAPM is the landing lens: its tab is first and pressed.
        self.assertIn('data-player-model="rapm" aria-pressed="true"', page)
        self.assertIn('data-player-model="lineup-trueskill" aria-pressed="false"', page)
        self.assertIn('id="player-quick-model-label">RAPM<', page)
        self.assertIn("model: 'rapm'", script)
        # The Lineup baseline carries an explicit noise-domination caveat,
        # published in the data and rendered only for that model.
        self.assertIn('"ordering_confidence": "noise-dominated"', pipeline)
        self.assertIn('"ordering_note"', pipeline)
        self.assertIn("function renderOrderingNote()", script)
        self.assertIn("state.model !== 'lineup-trueskill'", script)
        self.assertIn('id="player-ordering-note"', page)
        # The note element cannot fall into the hidden-attribute CSS trap.
        self.assertIn(".player-lab-ordering-note[hidden]", styles)
        self.assertIn("RAPM remains the primary ranking", script)

    def test_player_lab_audit_fixes_are_present(self):
        root = Path(__file__).resolve().parents[1]
        page = (root / "player-lab.md").read_text()
        script = (root / "assets/js/player-lab.js").read_text()
        pipeline = (root / "rating_lab/player_pipeline.py").read_text()
        styles = (root / "assets/main.scss").read_text()
        head = (root / "_includes/head-custom.html").read_text()
        # Lineup log loss ships with chronological reference forecasters.
        self.assertIn('"log_loss_uniform_baseline"', pipeline)
        self.assertIn('"log_loss_home_prior_baseline"', pipeline)
        self.assertIn("uniform guess", script)
        # The hidden attribute wins over the field grid (team selector bug).
        self.assertIn(".rating-lab-field[hidden]", styles)
        # Signed zeros are clamped everywhere impacts are displayed.
        self.assertIn("function signedNumber(value, digits)", script)
        self.assertNotIn(".impact > 0 ? '+' : ''", script)
        # Team-scoped models explain an empty search instead of lying.
        self.assertIn("is fitted within one team", script)
        # Common names from the source, formal name kept for the detail.
        self.assertIn('player.get("player_nickname")', pipeline)
        self.assertIn("full_name", script)
        # Withheld banner renders as a collapsed summary.
        self.assertIn("withheld</strong> — why", script)
        # Scatter overplotting and keyboard controls.
        self.assertIn("FLAG_BUDGET", script)
        self.assertIn("tabindex=\"' + (point.id === tabbableId", script)
        # No render-blocking or hotlinked external dependencies.
        self.assertIn("script async src=\"https://cdn.jsdelivr.net/npm/mathjax@3", head)
        self.assertNotIn("raw.githubusercontent.com", page)
        self.assertIn("assets/images/statsbomb-logo.jpg", page)

    def test_on_demand_loading_contract_is_present(self):
        root = Path(__file__).resolve().parents[1]
        script = (root / "assets/js/rating-lab.js").read_text()
        player_script = (root / "assets/js/player-lab.js").read_text()
        styles = (root / "assets/main.scss").read_text()
        pipeline = (root / "rating_lab/pipeline.py").read_text()
        self.assertIn("function ensureRankings(sport, model)", script)
        self.assertIn("'split/' + sport + '-core.json'", script)
        self.assertIn("'split/' + sport + '-rankings-' + model + '.json'", script)
        self.assertIn("elo.rankings ? elo.rankings.length : elo.entity_count", script)
        self.assertIn("root.setAttribute('aria-busy', 'true')", script)
        self.assertIn("splitUrl('player-index.json')", player_script)
        self.assertIn(".catch(loadFullPayload)", player_script)
        self.assertIn("function ensureCohort(id)", player_script)
        self.assertIn("root.setAttribute('aria-busy', 'true')", player_script)
        self.assertIn(".rating-lab[aria-busy='true']", styles)
        self.assertIn("write_split_assets(output_dir)", pipeline)
        # The canonical full files stay published for downloads and the Android app.
        self.assertIn("player-football.json' | relative_url }}\" download", (root / "player-lab.md").read_text())
        self.assertIn('fetch("${sport.fileName}.json")', (root / "android/app/src/main/java/io/github/kieranmcshane/ratinglab/data/RatingRepository.kt").read_text())


if __name__ == "__main__":
    unittest.main()
