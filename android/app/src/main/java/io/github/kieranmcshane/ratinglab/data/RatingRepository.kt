package io.github.kieranmcshane.ratinglab.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import kotlin.math.abs

class RatingRepository(
    private val baseUrl: String = "https://kieranmcshane.github.io/assets/data/rating-lab"
) {
    suspend fun load(sport: Sport, model: RatingModel): RatingSnapshot = withContext(Dispatchers.IO) {
        runCatching { parse(fetch("${sport.fileName}.json"), model) }
            .getOrElse { DemoData.snapshot(sport, model) }
    }

    suspend fun loadPlayers(): PlayerDataset = withContext(Dispatchers.IO) {
        parsePlayers(fetch("player-football.json"))
    }

    private fun fetch(fileName: String): String {
        val connection = URL("$baseUrl/$fileName").openConnection() as HttpURLConnection
        connection.connectTimeout = 10_000
        connection.readTimeout = 25_000
        connection.setRequestProperty("Accept", "application/json")
        connection.setRequestProperty("User-Agent", "RatingLab-Android/1.0")
        return try {
            check(connection.responseCode in 200..299) {
                "Data server returned ${connection.responseCode}"
            }
            connection.inputStream.bufferedReader().use { it.readText() }
        } finally {
            connection.disconnect()
        }
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
                            val point = historyArray.optJSONArray(historyIndex) ?: continue
                            add(point.optDouble(1))
                        }
                    }
                }
                val contexts = item.optJSONObject("contexts")
                val contextRatings = buildMap {
                    contexts?.keys()?.forEach { context ->
                        val value = contexts.optJSONObject(context) ?: return@forEach
                        val rating = value.optFiniteDouble("rating") ?: return@forEach
                        put(
                            context,
                            ContextRating(
                                rating = rating,
                                sigma = value.optFiniteDouble("sigma"),
                                matches = value.optInt("matches", 0)
                            )
                        )
                    }
                }
                val change = item.optDouble("change30", 0.0).let {
                    if (abs(it) < 0.05) 0.0 else it
                }
                add(
                    RatingEntry(
                        id = item.getString("id"),
                        name = item.getString("name"),
                        country = item.optNonBlank("country"),
                        competition = item.optString("competition", root.optString("sport", "Current cohort")),
                        rating = item.optDouble("rating", item.optDouble("score")),
                        sigma = item.optFiniteDouble("sigma"),
                        change30 = change,
                        matches = item.optInt("matches", 0),
                        recentMatches = item.optInt("recent_matches", 0),
                        lastPlayed = item.optString("last_played", "—"),
                        history = history,
                        contexts = contextRatings,
                        provisional = item.optBoolean("provisional", false),
                        provisionalReason = item.optNonBlank("provisional_reason"),
                        media = item.optJSONObject("media").toEntityMedia()
                    )
                )
            }
        }
        val parameters = root.optJSONObject("parameters")
            ?.optJSONObject(model.key)
            .numericMap()
        val predictor = root.optJSONObject("tournament_predictor")
        val competitions = predictor?.optJSONArray("competitions")?.let {
            parseCompetitions(it, predictor, model)
        }.orEmpty()
        val source = root.optJSONObject("source") ?: JSONObject()
        val window = root.optJSONObject("data_window") ?: JSONObject()
        val eligibility = root.optJSONObject("eligibility") ?: JSONObject()
        val outcome = root.optJSONObject("outcome_context") ?: JSONObject()
        return RatingSnapshot(
            schemaVersion = root.optString("schema_version", "unknown"),
            generatedAt = root.optString("generated_at", "unknown"),
            modelLabel = modelObject.optString("label", model.label),
            metrics = modelObject.optJSONObject("metrics").numericMap(),
            parameters = parameters,
            drawRate = outcome.optDouble("draw_rate", 0.0),
            entries = entries,
            competitions = competitions,
            evidence = SourceEvidence(
                name = source.optString("source", "Published source"),
                url = source.optString("source_url", ""),
                license = source.optString("license", "Source-specific"),
                latestResult = source.optString("latest_result", root.optString("latest_result", "unknown")),
                staleAfterHours = source.optInt("stale_after_hours", 0),
                firstResult = window.optString("first_result", "unknown"),
                matches = window.optInt("matches", 0),
                entities = window.optInt("entities", 0),
                eligibilityRule = eligibility.optString("rule", "Published eligibility rule"),
                outcomeMethod = outcome.optString("method", "Published outcome model")
            ),
            predictorMethod = predictor?.optString("performance_method")?.takeIf { it.isNotBlank() },
            isFallback = false
        )
    }

    private fun parseCompetitions(
        competitions: JSONArray,
        predictor: JSONObject,
        model: RatingModel
    ): List<CompetitionForecast> {
        val providers = listOf(
            "Polymarket" to predictor.optJSONObject("market_comparison"),
            "Kalshi" to predictor.optJSONObject("kalshi_comparison")
        )
        return buildList {
            for (index in 0 until competitions.length()) {
                val item = competitions.optJSONObject(index) ?: continue
                val id = item.optString("id")
                val modelData = item.optJSONObject("models")?.optJSONObject(model.key)
                val forecastRows = modelData?.optJSONArray("teams")
                    ?: modelData?.optJSONArray("participants")
                val forecast = buildList {
                    if (forecastRows != null) {
                        for (rowIndex in 0 until forecastRows.length()) {
                            val row = forecastRows.optJSONObject(rowIndex) ?: continue
                            add(
                                ForecastEntry(
                                    id = row.optString("id"),
                                    name = row.optString("name", "Unknown"),
                                    currentRank = row.optNullableInt("current_rank"),
                                    played = row.optNullableInt("played"),
                                    currentPoints = row.optFiniteDouble("current_points"),
                                    expectedPoints = row.optFiniteDouble("expected_points"),
                                    expectedPosition = row.optFiniteDouble("expected_position"),
                                    champion = row.optFiniteDouble("champion"),
                                    topFour = row.optFiniteDouble("top_four"),
                                    bottomThree = row.optFiniteDouble("bottom_three"),
                                    reachNextStage = row.optFiniteDouble("reach_next_stage"),
                                    rating = row.optFiniteDouble("rating")
                                )
                            )
                        }
                    }
                }
                val performanceRoot = item.optJSONObject("performance")
                val performanceData = performanceRoot?.optJSONObject("models")
                    ?.optJSONObject(model.key)
                val performanceRows = performanceData?.optJSONArray("participants")
                val performance = buildList {
                    if (performanceRows != null) {
                        for (rowIndex in 0 until performanceRows.length()) {
                            val row = performanceRows.optJSONObject(rowIndex) ?: continue
                            add(
                                PerformanceEntry(
                                    id = row.optString("id"),
                                    name = row.optString("name", "Unknown"),
                                    rank = row.optInt("rank", rowIndex + 1),
                                    performanceRating = row.optDouble("performance_rating", 0.0),
                                    change = row.optDouble("change", 0.0),
                                    matches = row.optInt("matches", 0),
                                    wins = row.optInt("wins", 0),
                                    draws = row.optInt("draws", 0),
                                    losses = row.optInt("losses", 0)
                                )
                            )
                        }
                    }
                }
                add(
                    CompetitionForecast(
                        id = id,
                        label = item.optString("label", id),
                        season = item.optString("season", ""),
                        format = item.optString("format", "competition"),
                        status = item.optString("status", "unknown"),
                        availability = item.optString("availability", ""),
                        firstFixture = item.optNonBlank("first_fixture"),
                        lastFixture = item.optNonBlank("last_fixture"),
                        nextFixture = item.optNonBlank("next_fixture"),
                        forecastType = modelData?.optNonBlank("forecast_type"),
                        simulations = modelData?.optNullableInt("simulations"),
                        completedMatches = modelData?.optNullableInt("completed_matches"),
                        remainingMatches = modelData?.optNullableInt("remaining_matches"),
                        currentStage = modelData?.optNonBlank("current_stage"),
                        forecast = forecast,
                        performanceMethod = performanceRoot?.optNonBlank("method"),
                        performance = performance,
                        markets = providers.mapNotNull { (name, provider) ->
                            parseMarket(name, provider, id)
                        },
                        sourceUrl = item.optNonBlank("source_url"),
                        license = item.optNonBlank("license")
                    )
                )
            }
        }
    }

    private fun parseMarket(
        providerName: String,
        provider: JSONObject?,
        competitionId: String
    ): MarketSnapshot? {
        provider ?: return null
        val snapshots = provider.optJSONArray("competitions") ?: return null
        val snapshot = (0 until snapshots.length())
            .mapNotNull { snapshots.optJSONObject(it) }
            .firstOrNull { it.optString("competition_id") == competitionId }
            ?: return null
        val outcomes = snapshot.optJSONArray("outcomes")
        val rows = buildList {
            if (outcomes != null) {
                for (index in 0 until outcomes.length()) {
                    val item = outcomes.optJSONObject(index) ?: continue
                    add(
                        MarketOutcome(
                            entityId = item.optString("entity_id"),
                            name = item.optString("name", item.optString("market_label", "Unknown")),
                            probability = item.optDouble("normalized_probability", 0.0),
                            rawProbability = item.optFiniteDouble("raw_yes_price")
                                ?: item.optFiniteDouble("midpoint"),
                            bestBid = item.optFiniteDouble("best_bid")
                                ?: item.optFiniteDouble("yes_bid"),
                            bestAsk = item.optFiniteDouble("best_ask")
                                ?: item.optFiniteDouble("yes_ask")
                        )
                    )
                }
            }
        }
        return MarketSnapshot(
            provider = providerName,
            status = provider.optString("status", "unknown"),
            competitionId = competitionId,
            eventTitle = snapshot.optString("event_title", snapshot.optString("title", competitionId)),
            eventUrl = snapshot.optNonBlank("event_url"),
            checkedAt = provider.optNonBlank("checked_at") ?: provider.optNonBlank("fetched_at"),
            rawProbabilitySum = snapshot.optFiniteDouble("raw_yes_price_sum")
                ?: snapshot.optFiniteDouble("raw_probability_sum"),
            coverage = snapshot.optFiniteDouble("coverage"),
            definition = snapshot.optString(
                "normalization",
                provider.optString("probability_definition", "Public market benchmark")
            ),
            outcomes = rows
        )
    }

    internal fun parsePlayers(raw: String): PlayerDataset {
        val root = JSONObject(raw)
        val methodology = root.optJSONObject("methodology") ?: JSONObject()
        val excluded = methodology.optJSONArray("excluded_inputs").stringList()
        val statuses = root.optJSONObject("source")?.optJSONObject("statuses")
        val worldCup = statuses?.optJSONObject("api_football_world_cup_2026")
        val cohortsArray = root.getJSONArray("cohorts")
        val cohorts = buildList {
            for (index in 0 until cohortsArray.length()) {
                val item = cohortsArray.getJSONObject(index)
                val modelsObject = item.getJSONObject("models")
                val models = PlayerModel.entries.associate { playerModel ->
                    playerModel.key to parsePlayerModel(
                        modelsObject.getJSONObject(playerModel.key),
                        playerModel
                    )
                }
                val source = item.optJSONObject("source") ?: JSONObject()
                val eligibility = item.optJSONObject("eligibility") ?: JSONObject()
                val coverage = item.optJSONObject("coverage")
                add(
                    PlayerCohort(
                        id = item.getString("id"),
                        name = item.getString("name"),
                        gender = item.optString("gender", ""),
                        format = item.optString("format", ""),
                        scopeType = item.optString("scope_type", "competition"),
                        firstMatch = item.optString("first_match", ""),
                        lastMatch = item.optString("last_match", ""),
                        matches = item.optInt("matches", 0),
                        eligiblePlayers = item.optInt("eligible_players", 0),
                        minimumMinutes = eligibility.optDouble("minimum_minutes", 0.0),
                        minimumMatches = eligibility.optInt("minimum_matches", 0),
                        sourceName = source.optString("name", "Declared source"),
                        sourceUrl = source.optString("url", ""),
                        license = source.optString("license", "Source-specific"),
                        coverage = coverage.numericMap(),
                        models = models,
                        snapshotSha256 = item.optString("snapshot_sha256", "")
                    )
                )
            }
        }
        return PlayerDataset(
            schemaVersion = root.optString("schema_version", "unknown"),
            generatedAt = root.optString("generated_at", "unknown"),
            cohorts = cohorts,
            inputSummary = methodology.optJSONArray("inputs").stringList().joinToString(", "),
            excludedInputs = excluded,
            interpretation = methodology.optString("interpretation", "Cohort-specific association with team outcomes."),
            worldCupStatus = worldCup?.optNonBlank("status"),
            worldCupMessage = worldCup?.optNonBlank("message")
        )
    }

    private fun parsePlayerModel(
        modelObject: JSONObject,
        playerModel: PlayerModel
    ): PlayerModelSnapshot {
        val teamsArray = modelObject.optJSONArray("teams")
        val teams = buildList {
            if (teamsArray != null) {
                for (index in 0 until teamsArray.length()) {
                    val team = teamsArray.getJSONObject(index)
                    val diagnostics = team.optJSONObject("diagnostics") ?: JSONObject()
                    val combinations = mutableListOf<PlayerCombination>()
                    val combinationRoot = team.optJSONObject("combinations")
                    val byOrder = combinationRoot?.optJSONArray("by_order")
                    if (byOrder != null) {
                        for (orderIndex in 0 until byOrder.length()) {
                            val order = byOrder.getJSONObject(orderIndex)
                            combinations += parseCombinations(order.optJSONArray("outperformers"))
                            combinations += parseCombinations(order.optJSONArray("underperformers"))
                        }
                    } else {
                        combinations += parseCombinations(combinationRoot?.optJSONArray("outperformers"))
                        combinations += parseCombinations(combinationRoot?.optJSONArray("underperformers"))
                    }
                    add(
                        PlayerTeamModel(
                            id = team.optString("id"),
                            name = team.optString("name", "Team"),
                            rankings = parsePlayerRankings(team.optJSONArray("rankings"), diagnostics.optNonBlank("validation_status")),
                            combinations = combinations.distinctBy { "${it.order}:${it.label}" },
                            validationStatus = diagnostics.optNonBlank("validation_status"),
                            validationDelta = diagnostics.optFiniteDouble("validation_delta"),
                            retainedNodes = diagnostics.optNullableInt("retained_nodes"),
                            omittedOvercompleteStints = diagnostics.optNullableInt("omitted_overcomplete_stints")
                        )
                    )
                }
            }
        }
        return PlayerModelSnapshot(
            key = playerModel.key,
            label = modelObject.optString("label", playerModel.label),
            status = modelObject.optNonBlank("status"),
            rankingRule = modelObject.optString("ranking_rule", "Published conservative score"),
            rankings = parsePlayerRankings(modelObject.optJSONArray("rankings"), modelObject.optNonBlank("status")),
            teams = teams,
            metrics = modelObject.optJSONObject("metrics").numericMap()
        )
    }

    private fun parsePlayerRankings(rows: JSONArray?, status: String?): List<PlayerEntry> = buildList {
        if (rows == null) return@buildList
        for (index in 0 until rows.length()) {
            val row = rows.optJSONObject(index) ?: continue
            add(
                PlayerEntry(
                    id = row.optString("id"),
                    name = row.optString("name", "Unknown"),
                    country = row.optNonBlank("country"),
                    team = row.optString("team", ""),
                    rank = row.optInt("rank", index + 1),
                    score = row.optDouble("score", 0.0),
                    impact = row.optFiniteDouble("impact"),
                    mean = row.optFiniteDouble("mean"),
                    uncertainty = row.optDouble("uncertainty", 0.0),
                    minutes = row.optDouble("minutes", row.optDouble("team_minutes", 0.0)),
                    matches = row.optInt("matches", 0),
                    status = status,
                    media = row.optJSONObject("media").toEntityMedia()
                )
            )
        }
    }

    private fun parseCombinations(rows: JSONArray?): List<PlayerCombination> = buildList {
        if (rows == null) return@buildList
        for (index in 0 until rows.length()) {
            val row = rows.optJSONObject(index) ?: continue
            add(
                PlayerCombination(
                    label = row.optString("label", "Observed combination"),
                    order = row.optInt("order", 0),
                    impact = row.optDouble("impact", 0.0),
                    uncertainty = row.optDouble("uncertainty", 0.0),
                    minutes = row.optDouble("minutes", 0.0),
                    stints = row.optInt("stints", 0)
                )
            )
        }
    }
}

private fun JSONObject?.numericMap(): Map<String, Double> = buildMap {
    val source = this@numericMap ?: return@buildMap
    source.keys().forEach { key ->
        source.optFiniteDouble(key)?.let { put(key, it) }
    }
}

private fun JSONObject.optFiniteDouble(key: String): Double? =
    optDouble(key, Double.NaN).takeIf { it.isFinite() }

private fun JSONObject.optNullableInt(key: String): Int? =
    if (has(key) && !isNull(key)) optInt(key) else null

private fun JSONObject.optNonBlank(key: String): String? =
    optString(key).takeIf { it.isNotBlank() && it != "null" }

private fun JSONObject?.toEntityMedia(): EntityMedia? {
    val source = this ?: return null
    val url = source.optNonBlank("url") ?: return null
    return EntityMedia(
        kind = source.optString("kind", "image"),
        url = url,
        sourceUrl = source.optNonBlank("source_url"),
        attribution = source.optNonBlank("attribution") ?: source.optNonBlank("source"),
        license = source.optNonBlank("license")
    )
}

private fun JSONArray?.stringList(): List<String> = buildList {
    val source = this@stringList ?: return@buildList
    for (index in 0 until source.length()) {
        source.optString(index).takeIf { it.isNotBlank() }?.let(::add)
    }
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
            schemaVersion = "offline",
            generatedAt = "bundled fallback",
            modelLabel = model.label,
            metrics = mapOf("log_loss" to 0.612, "brier" to 0.208),
            parameters = if (model == RatingModel.ELO) mapOf("scale" to 400.0, "home" to 35.0) else mapOf("advantage" to 0.8),
            drawRate = if (sport == Sport.TENNIS) 0.0 else 0.25,
            entries = names.getValue(sport).mapIndexed { index, name ->
                RatingEntry(
                    id = "fallback:$index",
                    name = name,
                    country = null,
                    competition = sport.label,
                    rating = base - index * if (model == RatingModel.ELO) 42.0 else 0.8,
                    sigma = if (model.hasUncertainty) 1.1 + index * 0.08 else null,
                    change30 = listOf(17.8, 0.0, 25.0, 19.5, -14.1, 6.2)[index],
                    matches = 40 + index * 7,
                    recentMatches = 12 + index,
                    lastPlayed = "2026-07-20",
                    history = List(10) { point -> base - index * 42.0 - 28 + point * 3.1 },
                    contexts = if (sport == Sport.TENNIS) mapOf(
                        "hard" to ContextRating(base - index * 42.0, null, 12),
                        "clay" to ContextRating(base - index * 38.0 - 25.0, null, 8),
                        "grass" to ContextRating(base - index * 45.0 - 12.0, null, 5)
                    ) else emptyMap()
                )
            },
            competitions = emptyList(),
            evidence = SourceEvidence("Bundled fallback", "", "Local fallback", "2026-07-20", 0, "unknown", 0, 0, "Offline display only", "Offline display only"),
            predictorMethod = null,
            isFallback = true
        )
    }
}
