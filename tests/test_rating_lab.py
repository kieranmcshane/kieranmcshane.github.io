from __future__ import annotations

from datetime import date, timedelta
import json
import math
from pathlib import Path
import unittest

from rating_lab.models import EloModel, GaussianSkillModel, Glicko2Model, Match, SurfaceBlendModel
from rating_lab.player_models import LineupTrueSkill
from rating_lab.player_pipeline import _fit_ridge, _merge_minutes, player_schema, validate_player_payload
from rating_lab.pipeline import (
    FOOTBALL_COMPETITIONS,
    _deduplicate,
    _competition_performance,
    _competition_matches,
    _football_data_crest_media,
    _metrics,
    _merge_schedule_media,
    _merge_schedule_results,
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
    _validate_football_coverage,
    _model_candidates,
    build_sport_payload,
    individual_contribution_protocol,
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
    def test_context_parameters_cover_chess_color_and_tennis_surface(self):
        self.assertTrue(all(candidate["home"] == 35.0 for candidate in _model_candidates("chess", "elo")))
        surface_weights = {candidate["surface_weight"] for candidate in _model_candidates("tennis", "elo")}
        self.assertEqual(surface_weights, {0.4, 0.7, 0.9})

    def test_individual_contribution_protocol_publishes_only_valid_historical_cohorts(self):
        protocol = individual_contribution_protocol()
        self.assertEqual(protocol["status"], "historical_cohorts_published")
        self.assertEqual(protocol["live_publication_unit"], "club or national team")
        self.assertIn("individual player", protocol["historical_publication_unit"])
        self.assertIn("lineup_trueskill", protocol["methods"])
        self.assertIn("rapm", protocol["methods"])
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

    def test_rapm_ridge_assigns_positive_impact_to_repeated_winner(self):
        rows = [
            {"home": {"winner": 1.0}, "away": {"loser": 1.0}, "goal_difference": 2.0},
            {"home": {"loser": 1.0}, "away": {"winner": 1.0}, "goal_difference": -1.0},
            {"home": {"winner": 1.0}, "away": {"loser": 1.0}, "goal_difference": 1.0},
        ]
        fitted = _fit_ridge(rows, ["loser", "winner"], 1.0)
        self.assertGreater(fitted["coefficients"]["winner"], fitted["coefficients"]["loser"])
        self.assertGreaterEqual(fitted["uncertainty"]["winner"], 0.0)

    def test_player_schema_is_versioned_and_closed(self):
        schema = player_schema()
        self.assertEqual(schema["properties"]["schema_version"]["const"], "1.0.0")
        self.assertFalse(schema["additionalProperties"])

    def test_published_player_payload_passes_gates_and_has_contiguous_ranks(self):
        payload = json.loads((Path(__file__).resolve().parents[1] / "assets/data/rating-lab/player-football.json").read_text())
        validate_player_payload(payload)
        for cohort in payload["cohorts"]:
            self.assertGreaterEqual(cohort["coverage"]["starting_lineups"], 0.95)
            self.assertGreaterEqual(cohort["coverage"]["player_minutes"], 0.95)
            self.assertEqual(cohort["coverage"]["player_match_graph_components"], 1)
            for model in cohort["models"].values():
                self.assertEqual(
                    [row["rank"] for row in model["rankings"]],
                    list(range(1, len(model["rankings"]) + 1)),
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
        self.assertIn("b.champion - a.champion", script)
        self.assertIn("spread reflects starting ratings and schedule priors", script)
        self.assertIn('id="rating-include-provisional"', page)
        self.assertIn("var pageSize = mobile ? 12 : 20;", script)
        self.assertIn("elements.metricsDisclosure.open = false;", script)
        self.assertIn('class="rating-lab-market-detail"', script)
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


if __name__ == "__main__":
    unittest.main()
