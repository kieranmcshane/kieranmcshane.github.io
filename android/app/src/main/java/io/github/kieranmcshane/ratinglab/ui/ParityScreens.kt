package io.github.kieranmcshane.ratinglab.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.OpenInNew
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import io.github.kieranmcshane.ratinglab.data.CompetitionForecast
import io.github.kieranmcshane.ratinglab.data.EntityMedia
import io.github.kieranmcshane.ratinglab.data.ForecastEntry
import io.github.kieranmcshane.ratinglab.data.MarketSnapshot
import io.github.kieranmcshane.ratinglab.data.PerformanceEntry
import io.github.kieranmcshane.ratinglab.data.PlayerCohort
import io.github.kieranmcshane.ratinglab.data.PlayerEntry
import io.github.kieranmcshane.ratinglab.data.PlayerLoadState
import io.github.kieranmcshane.ratinglab.data.PlayerModel
import io.github.kieranmcshane.ratinglab.data.PlayerModelSnapshot
import io.github.kieranmcshane.ratinglab.data.PlayerTeamModel
import io.github.kieranmcshane.ratinglab.data.RatingEntry
import io.github.kieranmcshane.ratinglab.data.RatingLoadState
import io.github.kieranmcshane.ratinglab.data.RatingModel
import io.github.kieranmcshane.ratinglab.data.RatingSnapshot
import io.github.kieranmcshane.ratinglab.data.Sport
import java.text.NumberFormat
import java.net.URI
import java.util.Locale
import coil3.compose.SubcomposeAsyncImage
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.atan
import kotlin.math.exp
import kotlin.math.ln
import kotlin.math.pow
import kotlin.math.sqrt

data class OutcomeProbabilities(val win: Double, val draw: Double, val loss: Double)

fun formatPercent(value: Double): String = "%.1f%%".format(value.coerceIn(0.0, 1.0) * 100)

fun matchupProbabilities(
    snapshot: RatingSnapshot,
    sport: Sport,
    model: RatingModel,
    a: RatingEntry,
    b: RatingEntry,
    contextShift: Int,
    surface: String
): OutcomeProbabilities {
    val parameters = snapshot.parameters
    if (sport == Sport.TENNIS) {
        val global = baseOutcomes(snapshot, model, a.rating, a.sigma, b.rating, b.sigma, 0.0)
        val contextA = a.contexts[surface]
        val contextB = b.contexts[surface]
        if (contextA == null || contextB == null) return global
        val contextual = baseOutcomes(
            snapshot,
            model,
            contextA.rating,
            contextA.sigma,
            contextB.rating,
            contextB.sigma,
            0.0
        )
        val evidence = ((contextA.matches + contextB.matches) / 20.0).coerceIn(0.0, 1.0)
        val weight = (parameters["surface_weight"] ?: 0.0) * evidence
        return OutcomeProbabilities(
            win = (1 - weight) * global.win + weight * contextual.win,
            draw = (1 - weight) * global.draw + weight * contextual.draw,
            loss = (1 - weight) * global.loss + weight * contextual.loss
        ).normalized()
    }
    val advantage = contextShift * when (model) {
        RatingModel.ELO, RatingModel.GLICKO2 -> parameters["home"] ?: 0.0
        else -> parameters["advantage"] ?: 0.0
    }
    return baseOutcomes(snapshot, model, a.rating, a.sigma, b.rating, b.sigma, advantage)
}

private fun baseOutcomes(
    snapshot: RatingSnapshot,
    model: RatingModel,
    ratingA: Double,
    sigmaA: Double?,
    ratingB: Double,
    sigmaB: Double?,
    advantage: Double
): OutcomeProbabilities {
    val difference = ratingA - ratingB + advantage
    val parameters = snapshot.parameters
    if (model == RatingModel.ELO || model == RatingModel.GLICKO2) {
        val expected = if (model == RatingModel.ELO) {
            1.0 / (1.0 + 10.0.pow(-difference / (parameters["scale"] ?: 400.0)))
        } else {
            val opponentPhi = (sigmaB ?: 350.0) / 173.7178
            val damping = 1.0 / sqrt(1.0 + 3.0 * opponentPhi * opponentPhi / (PI * PI))
            1.0 / (1.0 + exp(-damping * difference / 173.7178))
        }
        val draw = minOf(
            snapshot.drawRate * 4.0 * expected * (1.0 - expected),
            2.0 * minOf(expected, 1.0 - expected)
        )
        return OutcomeProbabilities(
            expected - 0.5 * draw,
            draw,
            1.0 - expected - 0.5 * draw
        ).normalized()
    }
    val beta = parameters["beta"] ?: 4.1667
    val margin = parameters["draw_margin"] ?: 0.0
    val uncertainty = sqrt((sigmaA ?: 0.0).pow(2) + (sigmaB ?: 0.0).pow(2))
    val scale = sqrt(beta * beta + uncertainty * uncertainty)
    val cdf: (Double) -> Double = if (model == RatingModel.ROBUST) {
        { value -> 0.5 + atan(value) / PI }
    } else {
        { value -> normalCdf(value) }
    }
    val win = 1.0 - cdf((margin - difference) / scale)
    val loss = cdf((-margin - difference) / scale)
    val draw = (1.0 - win - loss).coerceAtLeast(0.0)
    return OutcomeProbabilities(win, draw, loss).normalized()
}

private fun OutcomeProbabilities.normalized(): OutcomeProbabilities {
    val total = (win + draw + loss).coerceAtLeast(1e-12)
    return OutcomeProbabilities(win / total, draw / total, loss / total)
}

private fun normalCdf(value: Double): Double {
    val sign = if (value < 0) -1 else 1
    val x = abs(value) / sqrt(2.0)
    val t = 1.0 / (1.0 + 0.3275911 * x)
    val erf = sign * (1.0 - (((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t -
        0.284496736) * t + 0.254829592) * t * exp(-x * x)))
    return 0.5 * (1.0 + erf)
}

@Composable
fun ParityRankingsScreen(
    state: RatingLabUiState,
    onSearch: (String) -> Unit,
    onToggleProvisional: () -> Unit
) {
    val ready = state.data as? RatingLoadState.Ready
    if (ready == null) {
        ParityLoading("Loading the published rankings…")
        return
    }
    val snapshot = ready.snapshot
    val query = state.search.trim().lowercase()
    val provisionalCount = snapshot.entries.count { it.provisional }
    val rows = snapshot.entries.filter { entry ->
        (state.includeProvisional || !entry.provisional) &&
            (query.isBlank() || listOf(entry.name, entry.country, entry.competition)
                .any { it.orEmpty().lowercase().contains(query) })
    }
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(12.dp, 14.dp, 12.dp, 92.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            ParityIntro(
                "${snapshot.modelLabel.uppercase()} · ${rows.size} SHOWN",
                "Leaderboard",
                "Search, inspect history, and switch models without returning to the top."
            )
        }
        item {
            OutlinedTextField(
                value = state.search,
                onValueChange = onSearch,
                leadingIcon = { Icon(Icons.Default.Search, null) },
                label = { Text("Player, team, country or competition") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
        }
        if (provisionalCount > 0) {
            item {
                FilterChip(
                    selected = state.includeProvisional,
                    onClick = onToggleProvisional,
                    label = { Text("Include provisional ($provisionalCount)") },
                    leadingIcon = if (state.includeProvisional) {
                        { Icon(Icons.Default.Check, null, Modifier.size(16.dp)) }
                    } else null
                )
            }
        }
        if (snapshot.isFallback) {
            item {
                NoticeCard(
                    "Offline fallback",
                    "The live public snapshot could not be loaded. These bundled rows are clearly separated from the published rankings; refresh when connected."
                )
            }
        }
        item { RatingEvidenceStrip(snapshot) }
        itemsIndexed(rows, key = { _, entry -> entry.id }) { index, entry ->
            ParityRatingRow(index + 1, entry, state.model, state.sport)
        }
        if (rows.isEmpty()) item { EmptyCard("No eligible competitor matches this search.") }
    }
}

@Composable
private fun RatingEvidenceStrip(snapshot: RatingSnapshot) {
    LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        item { EvidencePill("Generated ${snapshot.generatedAt.take(10)}") }
        snapshot.metrics["log_loss"]?.let { item { EvidencePill("Log loss ${"%.3f".format(it)}") } }
        snapshot.metrics["brier"]?.let { item { EvidencePill("Brier ${"%.3f".format(it)}") } }
        item { EvidencePill("${snapshot.evidence.matches} source matches") }
    }
}

@Composable
private fun EvidencePill(text: String) {
    Surface(color = Color(0xFFE9E7E0), shape = RoundedCornerShape(5.dp)) {
        Text(text, Modifier.padding(horizontal = 8.dp, vertical = 5.dp), fontSize = 10.sp, color = Muted, fontFamily = FontFamily.Monospace)
    }
}

@Composable
private fun ParityRatingRow(rank: Int, entry: RatingEntry, model: RatingModel, sport: Sport) {
    var expanded by rememberSaveable(entry.id) { mutableStateOf(false) }
    Card(
        onClick = { expanded = !expanded },
        colors = CardDefaults.cardColors(containerColor = Paper),
        border = androidx.compose.foundation.BorderStroke(1.dp, Rule),
        modifier = Modifier.fillMaxWidth().animateContentSize()
    ) {
        Column(Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("#$rank", color = Muted, fontFamily = FontFamily.Monospace, fontSize = 11.sp, modifier = Modifier.width(34.dp))
                IdentityMark(entry.country, entry.media, if (sport == Sport.NATIONS) entry.name else null)
                Spacer(Modifier.width(9.dp))
                Column(Modifier.weight(1f)) {
                    Text(entry.name, fontWeight = FontWeight.Bold, fontSize = 14.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text(entry.competition, color = Muted, fontSize = 11.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                Column(horizontalAlignment = Alignment.End) {
                    Text(formatRatingValue(entry.rating), fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text(
                        when {
                            entry.change30 > 0.05 -> "+${"%.1f".format(entry.change30)}"
                            entry.change30 < -0.05 -> "${"%.1f".format(entry.change30)}"
                            else -> "0.0"
                        },
                        color = if (entry.change30 > 0.05) Positive else if (entry.change30 < -0.05) Negative else Muted,
                        fontSize = 10.sp,
                        fontFamily = FontFamily.Monospace
                    )
                }
            }
            AnimatedVisibility(expanded) {
                Column(Modifier.padding(top = 10.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
                    HorizontalDivider(color = Rule)
                    HistoryChart(entry.history)
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("${entry.matches} total · ${entry.recentMatches} recent", color = Muted, fontSize = 11.sp)
                        Text("Last ${entry.lastPlayed}", color = Muted, fontSize = 11.sp)
                    }
                    if (model.hasUncertainty && entry.sigma != null) {
                        Text("Published uncertainty ±${"%.2f".format(entry.sigma)}", color = Cobalt, fontSize = 11.sp)
                    }
                    entry.provisionalReason?.let { Text("Provisional: $it", color = Negative, fontSize = 11.sp) }
                    entry.media?.let { media ->
                        Text(
                            listOfNotNull(media.attribution, media.license).joinToString(" · "),
                            color = Muted,
                            fontSize = 9.sp
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun HistoryChart(values: List<Double>) {
    Canvas(Modifier.fillMaxWidth().height(72.dp)) {
        if (values.size < 2) return@Canvas
        val minimum = values.min()
        val span = (values.max() - minimum).takeIf { it > 0 } ?: 1.0
        val path = Path()
        values.forEachIndexed { index, value ->
            val x = index * size.width / (values.size - 1)
            val y = size.height - ((value - minimum) / span).toFloat() * size.height
            if (index == 0) path.moveTo(x, y) else path.lineTo(x, y)
        }
        drawPath(path, Cobalt, style = Stroke(2.dp.toPx(), cap = StrokeCap.Round))
    }
}

@Composable
fun ParityCompetitionScreen(
    state: RatingLabUiState,
    onSelectCompetition: (String) -> Unit,
    onModelClick: () -> Unit
) {
    val ready = state.data as? RatingLoadState.Ready
    if (ready == null) {
        ParityLoading("Loading published competitions…")
        return
    }
    val competitions = ready.snapshot.competitions
    if (competitions.isEmpty()) {
        LazyColumn(contentPadding = PaddingValues(16.dp, 18.dp, 16.dp, 92.dp)) {
            item { ParityIntro("CURRENT AND COMPLETED EVENTS", "Competitions", "No forecastable competition is published for this sport in the current source snapshot.") }
            item { EmptyCard("The app does not invent a draw, field, or title probability when the website data withholds it.") }
        }
        return
    }
    val competition = competitions.firstOrNull { it.id == state.competitionId } ?: competitions.first()
    LazyColumn(
        contentPadding = PaddingValues(12.dp, 14.dp, 12.dp, 92.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        item { ParityIntro("LIVE FORECAST OR FINISHED PERFORMANCE", "Competitions", "The current competition state, protocol forecast, and independent market benchmarks use the same public snapshot as the website.") }
        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                items(competitions, key = { it.id }) { item ->
                    FilterChip(
                        selected = item.id == competition.id,
                        onClick = { onSelectCompetition(item.id) },
                        label = { Text(item.label, maxLines = 1) }
                    )
                }
            }
        }
        item { CompetitionHeader(competition, state.model, onModelClick) }
        if (competition.performance.isNotEmpty()) {
            item { SectionLabel("Finished competition · protocol performance") }
            items(competition.performance.take(30), key = { "perf:${it.id}" }) { row ->
                PerformanceRow(row)
            }
        } else if (competition.forecast.isNotEmpty()) {
            item { SectionLabel("Current forecast · ${competition.forecastType.orEmpty()}") }
            items(competition.forecast.take(40), key = { "forecast:${it.id}" }) { row ->
                ForecastCard(row)
            }
        } else {
            item { EmptyCard(competition.availability.ifBlank { "Forecast withheld until the public competition state is complete." }) }
        }
        competition.markets.forEach { market ->
            item { MarketCard(market, competition.forecast) }
        }
        item { ReproductionCard(competition) }
    }
}

@Composable
private fun CompetitionHeader(competition: CompetitionForecast, model: RatingModel, onModelClick: () -> Unit) {
    Card(colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
            Text(competition.label, fontFamily = FontFamily.Serif, fontWeight = FontWeight.Bold, fontSize = 21.sp)
            Text(listOf(competition.season, competition.format, competition.status).filter { it.isNotBlank() }.joinToString(" · "), color = Muted, fontSize = 11.sp)
            Text(competition.availability, color = Muted, fontSize = 12.sp)
            LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                competition.completedMatches?.let { item { EvidencePill("$it played") } }
                competition.remainingMatches?.let { item { EvidencePill("$it remaining") } }
                competition.simulations?.let { item { EvidencePill("$it simulations") } }
            }
            OutlinedButton(onClick = onModelClick, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Default.Tune, null, Modifier.size(16.dp))
                Spacer(Modifier.width(7.dp))
                Text("Protocol: ${model.label}")
            }
        }
    }
}

@Composable
private fun ForecastCard(row: ForecastEntry) {
    Card(colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(row.currentRank?.let { "#$it" } ?: "•", color = Muted, fontFamily = FontFamily.Monospace, modifier = Modifier.width(32.dp))
                Text(row.name, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                val primary = row.champion ?: row.reachNextStage
                primary?.let { Text(formatPercent(it), fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace, color = Cobalt) }
            }
            row.champion?.let { ProbabilityStrip(it) }
            LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                row.expectedPoints?.let { item { Text("Expected ${"%.1f".format(it)} pts", color = Muted, fontSize = 10.sp) } }
                row.expectedPosition?.let { item { Text("Position ${"%.1f".format(it)}", color = Muted, fontSize = 10.sp) } }
                row.topFour?.let { item { Text("Top four ${formatPercent(it)}", color = Muted, fontSize = 10.sp) } }
                row.bottomThree?.let { item { Text("Bottom three ${formatPercent(it)}", color = Muted, fontSize = 10.sp) } }
            }
        }
    }
}

@Composable
private fun PerformanceRow(row: PerformanceEntry) {
    Card(colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
            Text("#${row.rank}", color = Muted, fontFamily = FontFamily.Monospace, modifier = Modifier.width(38.dp))
            Column(Modifier.weight(1f)) {
                Text(row.name, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text("${row.matches} matches · ${row.wins}W ${row.draws}D ${row.losses}L", color = Muted, fontSize = 10.sp)
            }
            Column(horizontalAlignment = Alignment.End) {
                Text(formatNumber(row.performanceRating), fontWeight = FontWeight.Bold, fontFamily = FontFamily.Monospace)
                Text((if (row.change > 0) "+" else "") + "%.1f".format(row.change), color = if (row.change >= 0) Positive else Negative, fontSize = 10.sp)
            }
        }
    }
}

@Composable
private fun MarketCard(market: MarketSnapshot, forecasts: List<ForecastEntry>) {
    val uriHandler = LocalUriHandler.current
    val modelById = forecasts.associateBy { it.id }
    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFF7F4EC)), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(15.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text("${market.provider} benchmark", fontWeight = FontWeight.Bold)
                    Text("${market.status} · coverage ${market.coverage?.let(::formatPercent) ?: "unknown"}", color = Muted, fontSize = 10.sp)
                }
                market.eventUrl?.let { url ->
                    TextButton(onClick = { uriHandler.openUri(url) }) {
                        Icon(Icons.AutoMirrored.Filled.OpenInNew, null, Modifier.size(15.dp))
                        Text("Market")
                    }
                }
            }
            market.outcomes.take(12).forEach { outcome ->
                val model = modelById[outcome.entityId]?.champion
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Text(outcome.name, Modifier.weight(1f), fontSize = 11.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("Mkt ${formatPercent(outcome.probability)}", fontFamily = FontFamily.Monospace, fontSize = 10.sp)
                    if (model != null) {
                        Spacer(Modifier.width(8.dp))
                        val gap = model - outcome.probability
                        Text("Δ ${(if (gap > 0) "+" else "")}${"%.1f".format(gap * 100)}pp", color = if (gap >= 0) Positive else Negative, fontFamily = FontFamily.Monospace, fontSize = 10.sp)
                    }
                }
            }
            Text("Raw Yes total ${market.rawProbabilitySum?.let { "%.1f%%".format(it * 100) } ?: "—"}. Market data are displayed beside, never inside, the rating model.", color = Muted, fontSize = 10.sp)
        }
    }
}

@Composable
private fun ReproductionCard(competition: CompetitionForecast) {
    val uriHandler = LocalUriHandler.current
    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFE9EEF9))) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text("Reproducibility", fontWeight = FontWeight.Bold)
            Text("${competition.sourceUrl.orEmpty()} · ${competition.license.orEmpty()}", color = Muted, fontSize = 10.sp)
            competition.sourceUrl?.let { url ->
                TextButton(onClick = { uriHandler.openUri(url) }) {
                    Icon(Icons.AutoMirrored.Filled.OpenInNew, null, Modifier.size(15.dp))
                    Text("Open competition source")
                }
            }
        }
    }
}

@Composable
fun ParityPlayersScreen(
    state: RatingLabUiState,
    onSelectCohort: (String) -> Unit,
    onSelectModel: (PlayerModel) -> Unit,
    onSelectTeam: (String) -> Unit,
    onSearch: (String) -> Unit
) {
    val ready = state.playerData as? PlayerLoadState.Ready
    if (ready == null) {
        when (val data = state.playerData) {
            is PlayerLoadState.Failed -> EmptyCard(data.message)
            else -> ParityLoading("Loading verified lineups and player models…")
        }
        return
    }
    val dataset = ready.dataset
    val cohort = dataset.cohorts.firstOrNull { it.id == state.playerCohortId } ?: dataset.cohorts.first()
    val model = cohort.models.getValue(state.playerModel.key)
    val team = if (state.playerModel.teamScoped) {
        model.teams.firstOrNull { it.id == state.playerTeamId } ?: model.teams.firstOrNull()
    } else null
    val query = state.playerSearch.trim().lowercase()
    val rows = (team?.rankings ?: model.rankings).filter {
        query.isBlank() || listOf(it.name, it.team, it.country).any { value -> value.orEmpty().lowercase().contains(query) }
    }
    LazyColumn(
        contentPadding = PaddingValues(12.dp, 14.dp, 12.dp, 92.dp),
        verticalArrangement = Arrangement.spacedBy(9.dp)
    ) {
        item { ParityIntro("RESULTS + LINEUPS + MINUTES ONLY", "Historical Player Lab", "Five lenses, identical publication gates for men's and women's complete tournaments and seasons.") }
        dataset.worldCupMessage?.let { message -> item { NoticeCard("World Cup 2026 · ${dataset.worldCupStatus.orEmpty()}", message) } }
        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                items(dataset.cohorts, key = { it.id }) { item ->
                    FilterChip(selected = item.id == cohort.id, onClick = { onSelectCohort(item.id) }, label = { Text(item.name, maxLines = 1) })
                }
            }
        }
        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                items(PlayerModel.entries) { item ->
                    FilterChip(selected = item == state.playerModel, onClick = { onSelectModel(item) }, label = { Text(item.label) })
                }
            }
        }
        if (state.playerModel.teamScoped && model.teams.isNotEmpty()) {
            item {
                LazyRow(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                    items(model.teams, key = { it.id }) { item ->
                        FilterChip(selected = item.id == team?.id, onClick = { onSelectTeam(item.id) }, label = { Text(item.name, maxLines = 1) })
                    }
                }
            }
        }
        item {
            OutlinedTextField(
                value = state.playerSearch,
                onValueChange = onSearch,
                leadingIcon = { Icon(Icons.Default.Search, null) },
                label = { Text("Player, team or nationality") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
        }
        item { PlayerEvidence(cohort, model, team) }
        item { PlayerComparisonPlot(cohort, state.playerModel, model, team) }
        if (team != null && team.combinations.isNotEmpty()) {
            item { CombinationPanel(team) }
        }
        item { SectionLabel("${model.label} leaderboard · ${rows.size} eligible") }
        items(rows.take(120), key = { "player:${state.playerModel.key}:${team?.id}:${it.id}" }) { row ->
            PlayerRow(row)
        }
        item { PlayerMethodCard(dataset.inputSummary, dataset.excludedInputs, dataset.interpretation, model, team) }
    }
}

@Composable
private fun PlayerEvidence(cohort: PlayerCohort, model: PlayerModelSnapshot, team: PlayerTeamModel?) {
    Card(colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(cohort.name, fontFamily = FontFamily.Serif, fontWeight = FontWeight.Bold, fontSize = 19.sp)
            Text("${cohort.gender} · ${cohort.format} · ${cohort.firstMatch} to ${cohort.lastMatch}", color = Muted, fontSize = 10.sp)
            Text("${cohort.matches} matches · ${cohort.eligiblePlayers} eligible · minimum ${cohort.minimumMinutes.toInt()} minutes / ${cohort.minimumMatches} matches", fontSize = 11.sp)
            Text(model.rankingRule, color = Cobalt, fontSize = 11.sp)
            if (team != null) {
                Text("${team.name} · ${team.validationStatus.orEmpty().replace('_', ' ')} · ${team.retainedNodes ?: 0} retained nodes", fontSize = 11.sp)
                team.validationDelta?.let { Text("Held-out RMSE delta vs APM ${(if (it > 0) "+" else "")}${"%.3f".format(it)}", color = if (it < 0) Positive else Negative, fontSize = 11.sp) }
                Text("${team.omittedOvercompleteStints ?: 0} over-complete source intervals omitted", color = Muted, fontSize = 10.sp)
            }
        }
    }
}

@Composable
private fun PlayerComparisonPlot(
    cohort: PlayerCohort,
    selectedModel: PlayerModel,
    model: PlayerModelSnapshot,
    team: PlayerTeamModel?
) {
    val lineupRows = cohort.models.getValue(PlayerModel.LINEUP.key).rankings
    val comparisonRows = team?.rankings ?: model.rankings
    if (selectedModel == PlayerModel.LINEUP || comparisonRows.size < 3) return
    val comparisonById = comparisonRows.associateBy { it.id }
    val points = lineupRows.mapNotNull { left -> comparisonById[left.id]?.let { right -> Triple(left, right, left.id) } }
    if (points.size < 3) return
    val xValues = points.map { it.first.score }
    val yValues = points.map { it.second.score }
    val xMean = xValues.average()
    val yMean = yValues.average()
    val xScale = sqrt(xValues.sumOf { (it - xMean).pow(2) } / points.size).takeIf { it > 0 } ?: 1.0
    val yScale = sqrt(yValues.sumOf { (it - yMean).pow(2) } / points.size).takeIf { it > 0 } ?: 1.0
    val standardized = points.map { Triple((it.first.score - xMean) / xScale, (it.second.score - yMean) / yScale, it) }
    var selectedId by rememberSaveable(cohort.id, selectedModel.key, team?.id) { mutableStateOf<String?>(null) }
    val selected = points.firstOrNull { it.third == selectedId }
    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFFBFAF6)), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(13.dp)) {
            Text("Lineup versus ${model.label}", fontWeight = FontWeight.Bold)
            Text("Tap a dot for player, nationality and both ranks.", color = Muted, fontSize = 10.sp)
            Canvas(
                Modifier.fillMaxWidth().height(260.dp).padding(top = 8.dp).pointerInput(standardized) {
                    detectTapGestures { tap ->
                        val extent = 3.0
                        val nearest = standardized.minByOrNull { point ->
                            val x = ((point.first + extent) / (2 * extent)).toFloat() * size.width
                            val y = (1f - ((point.second + extent) / (2 * extent)).toFloat()) * size.height
                            (Offset(x, y) - tap).getDistance()
                        }
                        selectedId = nearest?.third?.third
                    }
                }
            ) {
                drawLine(Rule, Offset(size.width / 2, 0f), Offset(size.width / 2, size.height), 1.dp.toPx())
                drawLine(Rule, Offset(0f, size.height / 2), Offset(size.width, size.height / 2), 1.dp.toPx())
                val extent = 3.0
                standardized.forEach { point ->
                    val x = ((point.first + extent) / (2 * extent)).toFloat().coerceIn(0f, 1f) * size.width
                    val y = (1f - ((point.second + extent) / (2 * extent)).toFloat().coerceIn(0f, 1f)) * size.height
                    drawCircle(if (point.third.third == selectedId) Violet else Cobalt.copy(alpha = 0.62f), if (point.third.third == selectedId) 7.dp.toPx() else 4.dp.toPx(), Offset(x, y))
                }
            }
            selected?.let { point ->
                Row(Modifier.fillMaxWidth().background(Paper, RoundedCornerShape(8.dp)).padding(10.dp), verticalAlignment = Alignment.CenterVertically) {
                    IdentityMark(point.first.country, point.first.media, null)
                    Spacer(Modifier.width(8.dp))
                    Column(Modifier.weight(1f)) {
                        Text(point.first.name, fontWeight = FontWeight.Bold)
                        Text("${point.first.country.orEmpty()} · ${point.first.team}", color = Muted, fontSize = 10.sp)
                    }
                    Text("Lineup #${point.first.rank}\n${model.label} #${point.second.rank}", fontFamily = FontFamily.Monospace, fontSize = 10.sp)
                }
            }
        }
    }
}

@Composable
private fun CombinationPanel(team: PlayerTeamModel) {
    var expanded by rememberSaveable(team.id) { mutableStateOf(false) }
    Card(onClick = { expanded = !expanded }, colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F7FA)), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(14.dp).animateContentSize()) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text("Observed combinations", fontWeight = FontWeight.Bold)
                    Text("Pairs, trios and higher-order evidence", color = Muted, fontSize = 10.sp)
                }
                Text(if (expanded) "−" else "+", color = Cobalt, fontSize = 20.sp)
            }
            AnimatedVisibility(expanded) {
                Column(Modifier.padding(top = 8.dp)) {
                    team.combinations.sortedByDescending { it.impact }.take(14).forEach { row ->
                        Row(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                            Column(Modifier.weight(1f)) {
                                Text(if (row.order > 4) "${row.order}-player observed lineup" else row.label, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                                Text("${row.minutes.toInt()} min · ${row.stints} stints · order ${row.order}", color = Muted, fontSize = 9.sp)
                            }
                            Text((if (row.impact > 0) "+" else "") + "%.2f".format(row.impact), fontFamily = FontFamily.Monospace, fontSize = 11.sp)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun PlayerRow(row: PlayerEntry) {
    var expanded by rememberSaveable(row.id) { mutableStateOf(false) }
    Card(onClick = { expanded = !expanded }, colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule), modifier = Modifier.animateContentSize()) {
        Column(Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("#${row.rank}", color = Muted, fontFamily = FontFamily.Monospace, modifier = Modifier.width(38.dp))
                IdentityMark(row.country, row.media, null)
                Spacer(Modifier.width(8.dp))
                Column(Modifier.weight(1f)) {
                    Text(row.name, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text("${row.country.orEmpty()} · ${row.team}", color = Muted, fontSize = 10.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                Text("%.2f".format(row.score), fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
            }
            AnimatedVisibility(expanded) {
                Row(Modifier.fillMaxWidth().padding(start = 38.dp, top = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("±${"%.2f".format(row.uncertainty)}", color = Muted, fontSize = 10.sp)
                    Text("${row.minutes.toInt()} minutes", color = Muted, fontSize = 10.sp)
                    Text("${row.matches} matches", color = Muted, fontSize = 10.sp)
                    row.impact?.let { Text("impact ${(if (it > 0) "+" else "")}${"%.2f".format(it)}", color = Cobalt, fontSize = 10.sp) }
                }
            }
        }
    }
}

@Composable
private fun PlayerMethodCard(
    inputs: String,
    excluded: List<String>,
    interpretation: String,
    model: PlayerModelSnapshot,
    team: PlayerTeamModel?
) {
    var expanded by rememberSaveable("player-method:${model.key}") { mutableStateOf(false) }
    Card(onClick = { expanded = !expanded }, colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(15.dp).animateContentSize()) {
            Row {
                Text("Exact player protocol", Modifier.weight(1f), fontWeight = FontWeight.Bold)
                Text(if (expanded) "−" else "+", color = Cobalt, fontSize = 20.sp)
            }
            AnimatedVisibility(expanded) {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(top = 8.dp)) {
                    Text("Inputs: $inputs", fontSize = 11.sp)
                    Text("Excluded: ${excluded.joinToString(", ")}", fontSize = 11.sp)
                    Text(interpretation, color = Muted, fontSize = 11.sp)
                    Text("Rule: ${model.rankingRule}", color = Cobalt, fontSize = 11.sp)
                    team?.validationStatus?.let { Text("Team validation: ${it.replace('_', ' ')}", fontSize = 11.sp) }
                }
            }
        }
    }
}

@Composable
fun ParityMethodsScreen(state: RatingLabUiState) {
    val ready = state.data as? RatingLoadState.Ready
    if (ready == null) {
        ParityLoading("Loading methods and source evidence…")
        return
    }
    val snapshot = ready.snapshot
    val uriHandler = LocalUriHandler.current
    val sections = listOf(
        "Source and freshness" to "${snapshot.evidence.name} · latest result ${snapshot.evidence.latestResult} · stale threshold ${snapshot.evidence.staleAfterHours} hours · ${snapshot.evidence.license}",
        "Eligibility" to snapshot.evidence.eligibilityRule,
        "Outcome protocol" to snapshot.evidence.outcomeMethod,
        "Selected parameters" to snapshot.parameters.entries.sortedBy { it.key }.joinToString(" · ") { "${it.key}=${formatNumber(it.value)}" },
        "Evaluation" to snapshot.metrics.entries.sortedBy { it.key }.joinToString(" · ") { "${it.key.replace('_', ' ')}=${formatNumber(it.value)}" },
        "Competition replay" to (snapshot.predictorMethod ?: "No format-aware predictor is published for this sport snapshot."),
        "Client boundary" to "The app reads versioned static JSON. API credentials, raw commercial responses, tuning, and rating replay remain server-side."
    )
    LazyColumn(contentPadding = PaddingValues(12.dp, 14.dp, 12.dp, 92.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
        item { ParityIntro("AUDITABLE BY DESIGN", "Methods & data", "Exact live parameters, source status, licensing, evaluation, and reproduction links—not a simplified app-only explanation.") }
        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                item { EvidencePill("Schema ${snapshot.schemaVersion}") }
                item { EvidencePill("${snapshot.evidence.matches} matches") }
                item { EvidencePill("${snapshot.evidence.entities} entities") }
            }
        }
        itemsIndexed(sections) { index, section -> MethodAccordion(index, section.first, section.second) }
        item {
            Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFE9EEF9))) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                    Text("Public reproduction", fontWeight = FontWeight.Bold)
                    Text("Generated ${snapshot.generatedAt} · window begins ${snapshot.evidence.firstResult}", color = Muted, fontSize = 10.sp)
                    TextButton(onClick = { uriHandler.openUri("https://github.com/kieranmcshane/kieranmcshane.github.io/tree/main/rating_lab") }) {
                        Icon(Icons.AutoMirrored.Filled.OpenInNew, null, Modifier.size(15.dp)); Text("Pipeline and model source")
                    }
                    TextButton(onClick = { uriHandler.openUri("https://kieranmcshane.github.io/assets/data/rating-lab/${state.sport.fileName}.json") }) {
                        Icon(Icons.AutoMirrored.Filled.OpenInNew, null, Modifier.size(15.dp)); Text("Current ${state.sport.label} JSON")
                    }
                    if (snapshot.evidence.url.isNotBlank()) {
                        TextButton(onClick = { uriHandler.openUri(snapshot.evidence.url) }) {
                            Icon(Icons.AutoMirrored.Filled.OpenInNew, null, Modifier.size(15.dp)); Text("Primary data source")
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun MethodAccordion(index: Int, title: String, body: String) {
    var open by rememberSaveable("method:$index") { mutableStateOf(index == 0) }
    Card(onClick = { open = !open }, colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(15.dp).animateContentSize()) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(title, Modifier.weight(1f), fontWeight = FontWeight.Bold)
                Text(if (open) "−" else "+", color = Cobalt, fontSize = 20.sp)
            }
            AnimatedVisibility(open) { Text(body, color = Muted, fontSize = 12.sp, lineHeight = 18.sp, modifier = Modifier.padding(top = 8.dp)) }
        }
    }
}

@Composable
private fun ProbabilityStrip(probability: Double) {
    Box(Modifier.fillMaxWidth().height(6.dp).clip(CircleShape).background(Rule)) {
        Box(Modifier.fillMaxWidth(probability.toFloat().coerceIn(0f, 1f)).fillMaxHeight().background(Cobalt))
    }
}

@Composable
private fun CountryMark(country: String?) {
    val label = country.orEmpty().split(" ").mapNotNull { it.firstOrNull() }.take(3).joinToString("").uppercase().ifBlank { "—" }
    Box(Modifier.size(34.dp).clip(RoundedCornerShape(8.dp)).background(Color(0xFFEDEBE5)).border(1.dp, Rule, RoundedCornerShape(8.dp)), contentAlignment = Alignment.Center) {
        Text(label, fontFamily = FontFamily.Monospace, color = Muted, fontSize = 9.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun IdentityMark(country: String?, media: EntityMedia?, nationalName: String?) {
    val mediaUrl = media?.url?.takeIf(::isTrustedImageUrl)
    val flagCode = countryCode(nationalName ?: country)
    val flagUrl = flagCode?.let { "https://kieranmcshane.github.io/assets/vendor/flag-icons/4x3/$it.svg" }
    val imageUrl = mediaUrl ?: flagUrl
    if (imageUrl == null) {
        CountryMark(country ?: nationalName)
        return
    }
    SubcomposeAsyncImage(
        model = imageUrl,
        contentDescription = when {
            mediaUrl != null -> null
            nationalName != null -> "Flag of $nationalName"
            else -> country?.let { "Nationality: $it" }
        },
        contentScale = if (mediaUrl != null) ContentScale.Crop else ContentScale.Fit,
        modifier = Modifier.size(34.dp).clip(RoundedCornerShape(8.dp)).background(Color.White).border(1.dp, Rule, RoundedCornerShape(8.dp)),
        loading = { CountryMark(country ?: nationalName) },
        error = { CountryMark(country ?: nationalName) }
    )
}

private fun isTrustedImageUrl(value: String): Boolean = runCatching {
    val uri = URI(value)
    uri.scheme == "https" && uri.host in setOf("crests.football-data.org", "upload.wikimedia.org")
}.getOrDefault(false)

private val countryCodesByName: Map<String, String> by lazy {
    buildMap {
        Locale.getISOCountries().forEach { code ->
            val locale = Locale.Builder().setRegion(code).build()
            put(locale.getDisplayCountry(Locale.ENGLISH).lowercase(Locale.ENGLISH), code.lowercase(Locale.ENGLISH))
            runCatching { put(locale.isO3Country.lowercase(Locale.ENGLISH), code.lowercase(Locale.ENGLISH)) }
        }
        putAll(
            mapOf(
                "england" to "gb-eng", "scotland" to "gb-sct", "wales" to "gb-wls",
                "northern ireland" to "gb-nir", "usa" to "us", "united states of america" to "us",
                "korea republic" to "kr", "south korea" to "kr", "cote d ivoire" to "ci",
                "côte d'ivoire" to "ci", "turkiye" to "tr", "türkiye" to "tr",
                "iran" to "ir", "russia" to "ru", "czech republic" to "cz"
            )
        )
    }
}

private fun countryCode(value: String?): String? {
    val normalized = value.orEmpty().trim().lowercase(Locale.ENGLISH)
    if (normalized.isBlank()) return null
    if (normalized.matches(Regex("[a-z]{2}"))) return normalized
    return countryCodesByName[normalized]
}

@Composable
private fun SectionLabel(text: String) {
    Text(text.uppercase(), color = Muted, fontFamily = FontFamily.Monospace, fontSize = 9.sp, letterSpacing = 0.5.sp, modifier = Modifier.padding(top = 4.dp))
}

@Composable
private fun ParityIntro(eyebrow: String, title: String, body: String) {
    Column(verticalArrangement = Arrangement.spacedBy(5.dp), modifier = Modifier.padding(bottom = 3.dp)) {
        Text(eyebrow, color = Muted, fontFamily = FontFamily.Monospace, fontSize = 9.sp, letterSpacing = 0.6.sp)
        Text(title, fontFamily = FontFamily.Serif, fontSize = 25.sp, fontWeight = FontWeight.SemiBold)
        Text(body, color = Muted, fontSize = 12.sp, lineHeight = 17.sp)
    }
}

@Composable
private fun EmptyCard(message: String) {
    Card(colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule), modifier = Modifier.fillMaxWidth()) {
        Text(message, color = Muted, fontSize = 12.sp, modifier = Modifier.padding(16.dp))
    }
}

@Composable
private fun NoticeCard(title: String, message: String) {
    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFE9EEF9))) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.Top) {
            Icon(Icons.Default.Info, null, tint = Cobalt, modifier = Modifier.size(18.dp))
            Spacer(Modifier.width(8.dp))
            Column { Text(title, fontWeight = FontWeight.Bold, fontSize = 12.sp); Text(message, color = Muted, fontSize = 11.sp) }
        }
    }
}

@Composable
private fun ParityLoading(message: String) {
    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(10.dp)) {
            CircularProgressIndicator(Modifier.size(27.dp), strokeWidth = 2.dp)
            Text(message, color = Muted, fontSize = 12.sp)
        }
    }
}

private fun formatNumber(value: Double): String = NumberFormat.getNumberInstance().apply { maximumFractionDigits = 2 }.format(value)

private fun formatRatingValue(value: Double): String = NumberFormat.getNumberInstance().apply {
    minimumFractionDigits = 1
    maximumFractionDigits = 1
}.format(value)
