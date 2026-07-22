package io.github.kieranmcshane.ratinglab.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class RatingRepository(
    private val baseUrl: String = "https://kieranmcshane.github.io/assets/data/rating-lab"
) {
    suspend fun load(sport: Sport, model: RatingModel): RatingSnapshot = withContext(Dispatchers.IO) {
        runCatching {
            val connection = URL("$baseUrl/${sport.fileName}.json").openConnection() as HttpURLConnection
            connection.connectTimeout = 8_000
            connection.readTimeout = 12_000
            connection.setRequestProperty("Accept", "application/json")
            connection.setRequestProperty("User-Agent", "RatingLab-Android/0.1")
            try {
                check(connection.responseCode in 200..299) { "Data server returned ${connection.responseCode}" }
                parse(connection.inputStream.bufferedReader().use { it.readText() }, model)
            } finally {
                connection.disconnect()
            }
        }.getOrElse { DemoData.snapshot(sport, model) }
    }

    internal fun parse(raw: String, model: RatingModel): RatingSnapshot {
        val root = JSONObject(raw)
        val modelObject = root.getJSONObject("models").getJSONObject(model.key)
        val rankings = modelObject.getJSONArray("rankings")
        val entries = buildList {
            for (index in 0 until rankings.length()) {
                val item = rankings.getJSONObject(index)
                val historyArray = item.optJSONArray("history")
                val history = buildList {
                    if (historyArray != null) {
                        for (historyIndex in 0 until historyArray.length()) {
                            add(historyArray.getJSONArray(historyIndex).optDouble(1))
                        }
                    }
                }
                val contexts = item.optJSONObject("contexts")
                val contextRatings = buildMap {
                    contexts?.keys()?.forEach { context ->
                        val contextRating = contexts.optJSONObject(context)?.optDouble("rating")
                        if (contextRating != null && !contextRating.isNaN()) put(context, contextRating)
                    }
                }
                add(
                    RatingEntry(
                        id = item.getString("id"),
                        name = item.getString("name"),
                        country = item.optString("country").takeIf { it.isNotBlank() },
                        competition = item.optString("competition", sportLabel(root)),
                        rating = item.optDouble("rating", item.optDouble("score")),
                        sigma = item.optDouble("sigma").takeUnless { it.isNaN() },
                        change30 = item.optDouble("change30", 0.0).let { if (kotlin.math.abs(it) < 0.05) 0.0 else it },
                        matches = item.optInt("matches", 0),
                        lastPlayed = item.optString("last_played", "—"),
                        history = history,
                        contextRatings = contextRatings
                    )
                )
            }
        }
        val metricObject = modelObject.optJSONObject("metrics")
        val metrics = buildMap {
            metricObject?.keys()?.forEach { key ->
                val value = metricObject.optDouble(key)
                if (!value.isNaN()) put(key, value)
            }
        }
        return RatingSnapshot(
            generatedAt = root.optString("generated_at", "unknown"),
            modelLabel = modelObject.optString("label", model.label),
            metrics = metrics,
            entries = entries
        )
    }

    private fun sportLabel(root: JSONObject): String = root.optString("sport", "Current cohort")
}

private object DemoData {
    private val names = mapOf(
        Sport.TENNIS to listOf("Jannik Sinner", "Carlos Alcaraz", "Alexander Zverev", "Novak Djokovic", "Arthur Fils", "Taylor Fritz"),
        Sport.CLUBS to listOf("Paris Saint-Germain", "Real Madrid", "Liverpool", "Bayern München", "Arsenal", "Barcelona"),
        Sport.NATIONS to listOf("Argentina", "Spain", "France", "Brazil", "Colombia", "Portugal"),
        Sport.CHESS to listOf("Magnus Carlsen", "Hikaru Nakamura", "Fabiano Caruana", "Arjun Erigaisi", "Alireza Firouzja", "Gukesh D")
    )

    fun snapshot(sport: Sport, model: RatingModel): RatingSnapshot {
        val base = if (model == RatingModel.ELO) 2420.0 else 35.0
        return RatingSnapshot(
            generatedAt = "bundled fallback",
            modelLabel = model.label,
            metrics = mapOf("log_loss" to 0.612, "brier" to 0.208),
            entries = names.getValue(sport).mapIndexed { index, name ->
                RatingEntry(
                    id = "fallback:$index",
                    name = name,
                    country = null,
                    competition = when (sport) {
                        Sport.TENNIS -> "ATP singles"
                        Sport.CLUBS -> "European clubs"
                        Sport.NATIONS -> "Men's national teams"
                        Sport.CHESS -> "Elite OTB"
                    },
                    rating = base - index * if (model == RatingModel.ELO) 42.0 else 0.8,
                    sigma = if (model.hasUncertainty) 1.1 + index * 0.08 else null,
                    change30 = listOf(17.8, 0.0, 25.0, 19.5, -14.1, 6.2)[index],
                    matches = 40 + index * 7,
                    lastPlayed = "2026-07-20",
                    history = List(10) { point -> base - index * 42.0 - 28 + point * 3.1 + (index % 3) * 2 },
                    contextRatings = if (sport == Sport.TENNIS) mapOf(
                        "hard" to base - index * 42.0,
                        "clay" to base - index * 38.0 - 25.0,
                        "grass" to base - index * 45.0 - 12.0
                    ) else emptyMap()
                )
            },
            isFallback = true
        )
    }
}
