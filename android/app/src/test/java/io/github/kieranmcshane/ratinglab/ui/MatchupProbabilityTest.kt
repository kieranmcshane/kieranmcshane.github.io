package io.github.kieranmcshane.ratinglab.ui

import io.github.kieranmcshane.ratinglab.data.RatingEntry
import io.github.kieranmcshane.ratinglab.data.RatingModel
import io.github.kieranmcshane.ratinglab.data.RatingSnapshot
import io.github.kieranmcshane.ratinglab.data.SourceEvidence
import io.github.kieranmcshane.ratinglab.data.Sport
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class MatchupProbabilityTest {
    private val alpha = entry("a", 1600.0)
    private val beta = entry("b", 1600.0)

    @Test
    fun threeWayProbabilitiesPartitionTheOutcomeSpace() {
        val result = matchupProbabilities(snapshot(), Sport.CLUBS, RatingModel.ELO, alpha, beta, 0, "hard")
        assertEquals(1.0, result.win + result.draw + result.loss, 1e-9)
        assertTrue(result.draw > 0.0)
    }

    @Test
    fun publishedHomeAdvantageRaisesHomeWinProbability() {
        val neutral = matchupProbabilities(snapshot(), Sport.CLUBS, RatingModel.ELO, alpha, beta, 0, "hard")
        val home = matchupProbabilities(snapshot(), Sport.CLUBS, RatingModel.ELO, alpha, beta, 1, "hard")
        assertTrue(home.win > neutral.win)
    }

    private fun snapshot() = RatingSnapshot(
        schemaVersion = "test",
        generatedAt = "test",
        modelLabel = "Elo",
        metrics = emptyMap(),
        parameters = mapOf("scale" to 400.0, "home" to 40.0),
        drawRate = 0.25,
        entries = listOf(alpha, beta),
        competitions = emptyList(),
        evidence = SourceEvidence("test", "", "", "", 0, "", 0, 0, "", ""),
        predictorMethod = null
    )

    private fun entry(id: String, rating: Double) = RatingEntry(
        id = id,
        name = id,
        country = null,
        competition = "Test",
        rating = rating,
        sigma = null,
        change30 = 0.0,
        matches = 20,
        recentMatches = 5,
        lastPlayed = "2026-07-23",
        history = listOf(rating)
    )
}
