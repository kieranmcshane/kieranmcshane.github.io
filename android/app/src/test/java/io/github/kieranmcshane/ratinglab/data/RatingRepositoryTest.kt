package io.github.kieranmcshane.ratinglab.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

class RatingRepositoryTest {
    private val repository = RatingRepository("https://example.invalid")

    @Test
    fun parsesPublishedRankingCompetitionAndMarketContracts() {
        val snapshot = repository.parse(SPORT_FIXTURE, RatingModel.ELO)

        assertEquals("3.0", snapshot.schemaVersion)
        assertEquals(2, snapshot.entries.size)
        assertEquals(0.0, snapshot.entries[0].change30, 0.0)
        assertEquals(1640.0, snapshot.entries[0].contexts.getValue("clay").rating, 0.0)
        assertEquals(1, snapshot.competitions.size)
        assertEquals(0.42, snapshot.competitions[0].forecast[0].champion!!, 0.0)
        assertEquals(2, snapshot.competitions[0].markets.size)
        assertEquals("Polymarket", snapshot.competitions[0].markets[0].provider)
        assertEquals(0.40, snapshot.competitions[0].markets[0].outcomes[0].probability, 0.0)
        assertTrue(snapshot.parameters.containsKey("home"))
    }

    @Test
    fun parsesEveryPublishedPlayerProtocolIncludingTeamScopedModels() {
        val dataset = repository.parsePlayers(PLAYER_FIXTURE)
        val cohort = dataset.cohorts.single()

        assertEquals("season", cohort.scopeType)
        assertEquals(PlayerModel.entries.map { it.key }.toSet(), cohort.models.keys)
        assertEquals("Player One", cohort.models.getValue("lineup-trueskill").rankings.single().name)
        val hapm = cohort.models.getValue("hapm").teams.single()
        assertEquals("validated", hapm.validationStatus)
        assertEquals(1, hapm.combinations.size)
        assertEquals("One + Two", hapm.combinations.single().label)
        assertNotNull(dataset.worldCupMessage)
    }

    @Test
    fun checkedInPublicSnapshotsRemainAndroidCompatible() {
        val repositoryRoot = File(requireNotNull(System.getProperty("ratingLabRepositoryRoot")))
        val dataDirectory = File(repositoryRoot, "assets/data/rating-lab")
        assertTrue("Missing checked-in Rating Lab snapshots", dataDirectory.isDirectory)

        Sport.entries.forEach { sport ->
            val raw = File(dataDirectory, "${sport.fileName}.json").readText()
            RatingModel.entries.forEach { model ->
                val snapshot = repository.parse(raw, model)
                assertTrue("${sport.label}/${model.label} has no rankings", snapshot.entries.isNotEmpty())
            }
        }
        val players = repository.parsePlayers(File(dataDirectory, "player-football.json").readText())
        assertTrue(players.cohorts.isNotEmpty())
        assertTrue(players.cohorts.all { cohort -> PlayerModel.entries.all { it.key in cohort.models } })
    }

    companion object {
        private val SPORT_FIXTURE = """
            {
              "schema_version":"3.0","generated_at":"2026-07-23T12:00:00Z","sport":"football",
              "source":{"source":"Open results","source_url":"https://example.org","license":"CC0","latest_result":"2026-07-22","stale_after_hours":48},
              "data_window":{"first_result":"2024-01-01","matches":40,"entities":4},
              "eligibility":{"rule":"Ten matches"},
              "outcome_context":{"draw_rate":0.25,"method":"Home advantage before outcome likelihood"},
              "parameters":{"elo":{"scale":400,"home":35,"surface_weight":0.4}},
              "models":{"elo":{"label":"Elo","metrics":{"log_loss":0.61,"brier":0.20},"rankings":[
                {"id":"a","name":"Alpha","country":"FR","competition":"League","rating":1650,"change30":-0.01,"matches":30,"recent_matches":8,"last_played":"2026-07-22","history":[["2026-01-01",1600],["2026-07-22",1650]],"contexts":{"clay":{"rating":1640,"matches":12}}},
                {"id":"b","name":"Beta","country":"ES","competition":"League","rating":1600,"change30":2.5,"matches":28,"recent_matches":7,"last_played":"2026-07-21","history":[["2026-01-01",1580],["2026-07-21",1600]]}
              ]}},
              "tournament_predictor":{"performance_method":"Chronological Monte Carlo","competitions":[{
                "id":"league","label":"Example League","season":"2026","format":"league","status":"live","availability":"Live forecast","source_url":"https://example.org/league","license":"CC0",
                "models":{"elo":{"forecast_type":"league","simulations":10000,"completed_matches":8,"remaining_matches":12,"teams":[{"id":"a","name":"Alpha","current_rank":1,"played":4,"current_points":10,"expected_points":31.2,"expected_position":1.8,"champion":0.42,"top_four":0.91,"bottom_three":0.01}]}}
              }],
              "market_comparison":{"status":"ok","checked_at":"2026-07-23","competitions":[{"competition_id":"league","event_title":"Winner","raw_yes_price_sum":1.05,"coverage":0.9,"outcomes":[{"entity_id":"a","name":"Alpha","normalized_probability":0.40,"raw_yes_price":0.42,"best_bid":0.41,"best_ask":0.43}]}]},
              "kalshi_comparison":{"status":"ok","checked_at":"2026-07-23","competitions":[{"competition_id":"league","event_title":"Winner","raw_probability_sum":1.0,"coverage":0.8,"outcomes":[{"entity_id":"a","name":"Alpha","normalized_probability":0.38,"midpoint":0.38,"yes_bid":0.37,"yes_ask":0.39}]}]}
              }
            }
        """.trimIndent()

        private val PLAYER_FIXTURE = """
            {
              "schema_version":"2.0","generated_at":"2026-07-23T12:00:00Z",
              "source":{"statuses":{"api_football_world_cup_2026":{"status":"ready","message":"Validated 104-match coverage"}}},
              "methodology":{"inputs":["results","lineups","minutes"],"excluded_inputs":["goals","passes"],"interpretation":"Association with team outcomes."},
              "cohorts":[{
                "id":"men-season","name":"Men's full season","gender":"men","format":"league","scope_type":"season","first_match":"2025-08-01","last_match":"2026-05-31","matches":380,"eligible_players":1,
                "source":{"name":"Verified lineups","url":"https://example.org","license":"CC0"},
                "coverage":{"lineups":1.0,"minutes":1.0},"eligibility":{"minimum_minutes":900,"minimum_matches":10},"snapshot_sha256":"abc",
                "models":{
                  "lineup-trueskill":{"label":"Lineup TrueSkill","ranking_rule":"mean minus uncertainty","rankings":[{"id":"p1","name":"Player One","country":"FR","team":"Alpha","rank":1,"score":3.2,"mean":4.0,"uncertainty":0.2,"minutes":1200,"matches":20}]},
                  "rapm":{"label":"RAPM","ranking_rule":"impact","rankings":[]},
                  "pairwise-chemistry":{"label":"Chemistry","ranking_rule":"interaction residual","rankings":[]},
                  "hapm":{"label":"HAPM","ranking_rule":"impact","teams":[{"id":"a","name":"Alpha","diagnostics":{"validation_status":"validated","validation_delta":0.01,"retained_nodes":12},"rankings":[],"combinations":{"outperformers":[{"label":"One + Two","order":2,"impact":0.3,"uncertainty":0.1,"minutes":600,"stints":12}]}}]},
                  "lapm":{"label":"LAPM","ranking_rule":"smoothed impact","teams":[]}
                }
              }]
            }
        """.trimIndent()
    }
}
