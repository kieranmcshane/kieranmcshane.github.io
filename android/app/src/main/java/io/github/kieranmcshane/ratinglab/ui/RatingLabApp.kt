package io.github.kieranmcshane.ratinglab.ui

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.CompareArrows
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Groups
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Insights
import androidx.compose.material.icons.filled.Leaderboard
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.SwapVert
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledTonalIconButton
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
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
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import io.github.kieranmcshane.ratinglab.data.RatingEntry
import io.github.kieranmcshane.ratinglab.data.RatingLoadState
import io.github.kieranmcshane.ratinglab.data.RatingModel
import io.github.kieranmcshane.ratinglab.data.RatingSnapshot
import io.github.kieranmcshane.ratinglab.data.Sport
import java.text.NumberFormat
import kotlin.math.abs
import kotlin.math.exp
import kotlin.math.pow

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RatingLabApp(viewModel: RatingLabViewModel = viewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    var showModelSheet by rememberSaveable { mutableStateOf(false) }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        containerColor = Canvas,
        topBar = {
            Column(modifier = Modifier.background(Paper).statusBarsPadding()) {
                TopAppBar(
                    title = {
                        Column {
                            Text(
                                text = "Rating Lab",
                                fontFamily = FontFamily.Serif,
                                fontWeight = FontWeight.SemiBold,
                                fontSize = 23.sp
                            )
                            Text(
                                text = "PUBLIC DATA · REPRODUCIBLE REPLAY",
                                color = Muted,
                                fontFamily = FontFamily.Monospace,
                                fontSize = 9.sp,
                                letterSpacing = 0.8.sp
                            )
                        }
                    },
                    actions = {
                        IconButton(onClick = viewModel::refresh) {
                            Icon(Icons.Default.Refresh, contentDescription = "Refresh current ratings")
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = Paper)
                )
                SportSelector(selected = state.sport, onSelect = viewModel::selectSport)
                HorizontalDivider(color = Rule)
            }
        },
        bottomBar = {
            RatingBottomBar(selected = state.section, onSelect = viewModel::selectSection)
        },
        floatingActionButton = {
            if (state.section == AppSection.RANKINGS) {
                FloatingActionButton(
                    onClick = { showModelSheet = true },
                    containerColor = Ink,
                    contentColor = Color.White,
                    modifier = Modifier.semantics { contentDescription = "Choose rating model" }
                ) {
                    Icon(Icons.Default.Tune, contentDescription = null)
                }
            }
        }
    ) { padding ->
        AnimatedContent(
            targetState = state.section,
            label = "section",
            modifier = Modifier.fillMaxSize().padding(padding)
        ) { section ->
            when (section) {
                AppSection.RANKINGS -> RankingsScreen(state.data, state.model)
                AppSection.COMPARE -> CompareScreen(
                    sport = state.sport,
                    model = state.model,
                    data = state.data,
                    competitorA = state.competitorA,
                    competitorB = state.competitorB,
                    onSelectA = viewModel::selectCompetitorA,
                    onSelectB = viewModel::selectCompetitorB,
                    onSwap = viewModel::swapCompetitors,
                    onModelClick = { showModelSheet = true }
                )
                AppSection.FORECASTS -> ForecastScreen(state.sport, state.model, state.data)
                AppSection.PLAYERS -> PlayersScreen()
                AppSection.METHODS -> MethodsScreen()
            }
        }
    }

    if (showModelSheet) {
        ModelSheet(
            selected = state.model,
            onSelect = {
                viewModel.selectModel(it)
                showModelSheet = false
            },
            onDismiss = { showModelSheet = false }
        )
    }
}

@Composable
private fun SportSelector(selected: Sport, onSelect: (Sport) -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Sport.entries.forEach { sport ->
            val active = sport == selected
            Surface(
                onClick = { onSelect(sport) },
                color = if (active) Color.White else Color.Transparent,
                shape = RoundedCornerShape(9.dp),
                border = if (active) androidx.compose.foundation.BorderStroke(1.dp, Rule) else null,
                tonalElevation = if (active) 1.dp else 0.dp,
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    sport.label,
                    modifier = Modifier.padding(vertical = 10.dp),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                    fontSize = 12.sp,
                    fontWeight = if (active) FontWeight.Bold else FontWeight.Medium,
                    color = if (active) Ink else Muted
                )
            }
        }
    }
}

@Composable
private fun RatingBottomBar(selected: AppSection, onSelect: (AppSection) -> Unit) {
    NavigationBar(
        containerColor = Paper,
        tonalElevation = 0.dp,
        modifier = Modifier.navigationBarsPadding().height(68.dp)
    ) {
        AppSection.entries.forEach { section ->
            val icon = when (section) {
                AppSection.RANKINGS -> Icons.Default.Leaderboard
                AppSection.COMPARE -> Icons.AutoMirrored.Filled.CompareArrows
                AppSection.FORECASTS -> Icons.Default.Insights
                AppSection.PLAYERS -> Icons.Default.Groups
                AppSection.METHODS -> Icons.Default.Science
            }
            NavigationBarItem(
                selected = section == selected,
                onClick = { onSelect(section) },
                icon = { Icon(icon, contentDescription = null, modifier = Modifier.size(20.dp)) },
                label = { Text(section.label, fontSize = 9.sp, maxLines = 1) },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = Cobalt,
                    selectedTextColor = Ink,
                    indicatorColor = Color.Transparent,
                    unselectedIconColor = Muted,
                    unselectedTextColor = Muted
                )
            )
        }
    }
}

@Composable
private fun RankingsScreen(data: RatingLoadState, model: RatingModel) {
    when (data) {
        RatingLoadState.Loading -> LoadingPane("Replaying the latest ratings…")
        is RatingLoadState.Failed -> ErrorPane(data.message)
        is RatingLoadState.Ready -> {
            val snapshot = data.snapshot
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(start = 12.dp, top = 14.dp, end = 12.dp, bottom = 92.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item {
                    SectionIntro(
                        eyebrow = "${snapshot.modelLabel.uppercase()} · ${snapshot.entries.size} ELIGIBLE",
                        title = "Leaderboard",
                        body = if (snapshot.isFallback) "Offline snapshot — refresh when connected." else "Current ratings from deterministic chronological replay."
                    )
                }
                item { MetricStrip(snapshot) }
                itemsIndexed(snapshot.entries.take(80), key = { _, item -> item.id }) { index, entry ->
                    RankingCard(rank = index + 1, entry = entry, showSigma = model.hasUncertainty)
                }
                item {
                    Text(
                        "Showing the leading 80. Use the website for the complete downloadable cohort.",
                        color = Muted,
                        fontFamily = FontFamily.Monospace,
                        fontSize = 10.sp,
                        modifier = Modifier.padding(12.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun MetricStrip(snapshot: RatingSnapshot) {
    val logLoss = snapshot.metrics["log_loss"]
    val brier = snapshot.metrics["brier"]
    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
        Credential("OUT-OF-SAMPLE")
        if (logLoss != null) Credential("LOG LOSS ${"%.3f".format(logLoss)}")
        if (brier != null) Credential("BRIER ${"%.3f".format(brier)}")
    }
}

@Composable
private fun Credential(text: String) {
    Surface(color = Color(0xFFE9E7E0), shape = RoundedCornerShape(4.dp)) {
        Text(
            text,
            modifier = Modifier.padding(horizontal = 7.dp, vertical = 4.dp),
            fontFamily = FontFamily.Monospace,
            fontSize = 9.sp,
            color = Muted
        )
    }
}

@Composable
private fun RankingCard(rank: Int, entry: RatingEntry, showSigma: Boolean) {
    var expanded by rememberSaveable(entry.id) { mutableStateOf(false) }
    Card(
        onClick = { expanded = !expanded },
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Paper),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, Rule),
        modifier = Modifier.fillMaxWidth().animateContentSize()
    ) {
        Column(Modifier.padding(horizontal = 12.dp, vertical = 11.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    rank.toString(),
                    color = Muted,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    modifier = Modifier.width(28.dp)
                )
                Monogram(entry.name)
                Spacer(Modifier.width(10.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        entry.name,
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Sparkline(entry.history, Modifier.width(70.dp).height(18.dp))
                        Spacer(Modifier.width(8.dp))
                        ChangePill(entry.change30)
                        if (showSigma && entry.sigma != null) {
                            Text("  σ ${"%.1f".format(entry.sigma)}", color = Muted, fontSize = 10.sp)
                        }
                    }
                }
                Text(
                    NumberFormat.getNumberInstance().apply { maximumFractionDigits = 1 }.format(entry.rating),
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    fontSize = 16.sp
                )
            }
            AnimatedVisibility(expanded) {
                Column(Modifier.padding(start = 66.dp, top = 10.dp)) {
                    HorizontalDivider(color = Rule)
                    Text(entry.competition, fontWeight = FontWeight.SemiBold, fontSize = 12.sp, modifier = Modifier.padding(top = 9.dp))
                    Text("${entry.matches} matches · last activity ${entry.lastPlayed}", color = Muted, fontSize = 11.sp)
                    Text("Tap A vs B below to turn this rating into an outcome probability.", color = Cobalt, fontSize = 11.sp, modifier = Modifier.padding(top = 4.dp))
                }
            }
        }
    }
}

@Composable
private fun Monogram(name: String) {
    val initials = name.split(" ").take(2).mapNotNull { it.firstOrNull()?.toString() }.joinToString("")
    Box(
        modifier = Modifier.size(34.dp).clip(CircleShape).background(Color(0xFFEDEBE5)),
        contentAlignment = Alignment.Center
    ) {
        Text(initials, fontFamily = FontFamily.Monospace, fontSize = 9.sp, color = Muted)
    }
}

@Composable
private fun ChangePill(change: Double) {
    val background = when {
        change > 0.05 -> Color(0xFFDDF1E9)
        change < -0.05 -> Color(0xFFF5DEDC)
        else -> Color.Transparent
    }
    val foreground = when {
        change > 0.05 -> Positive
        change < -0.05 -> Negative
        else -> Muted
    }
    Surface(color = background, shape = RoundedCornerShape(4.dp)) {
        Text(
            when {
                change > 0.05 -> "▲ ${change.toInt()}"
                change < -0.05 -> "▼ ${abs(change).toInt()}"
                else -> "—"
            },
            color = foreground,
            fontFamily = FontFamily.Monospace,
            fontSize = 9.sp,
            modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
        )
    }
}

@Composable
private fun Sparkline(values: List<Double>, modifier: Modifier = Modifier) {
    Canvas(modifier) {
        if (values.size < 2) return@Canvas
        val min = values.min()
        val max = values.max()
        val span = (max - min).takeIf { it > 0 } ?: 1.0
        val path = Path()
        values.forEachIndexed { index, value ->
            val x = index * size.width / (values.size - 1)
            val y = size.height - ((value - min) / span).toFloat() * size.height
            if (index == 0) path.moveTo(x, y) else path.lineTo(x, y)
        }
        drawPath(path, color = Cobalt, style = Stroke(width = 1.7.dp.toPx(), cap = StrokeCap.Round))
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun CompareScreen(
    sport: Sport,
    model: RatingModel,
    data: RatingLoadState,
    competitorA: Int,
    competitorB: Int,
    onSelectA: (Int) -> Unit,
    onSelectB: (Int) -> Unit,
    onSwap: () -> Unit,
    onModelClick: () -> Unit
) {
    if (data !is RatingLoadState.Ready) {
        LoadingPane("Preparing matchup…")
        return
    }
    val entries = data.snapshot.entries
    if (entries.size < 2) {
        ErrorPane("At least two eligible competitors are required.")
        return
    }
    val aIndex = competitorA.coerceIn(entries.indices)
    val bIndex = competitorB.coerceIn(entries.indices)
    val a = entries[aIndex]
    val b = entries[bIndex]
    var pickerForA by remember { mutableStateOf<Boolean?>(null) }
    var contextShift by rememberSaveable(sport) { mutableStateOf(if (sport == Sport.TENNIS) -1 else 0) }
    val surface = when (contextShift) { -1 -> "hard"; 0 -> "clay"; else -> "grass" }
    val effectiveA = if (sport == Sport.TENNIS) a.contextRatings[surface] ?: a.rating else a.rating
    val effectiveB = if (sport == Sport.TENNIS) b.contextRatings[surface] ?: b.rating else b.rating
    val adjustment = if (sport == Sport.TENNIS) 0.0 else contextShift * if (model == RatingModel.ELO) 35.0 else 0.8
    val scale = if (model == RatingModel.ELO) 400.0 else 8.0
    val probabilityA = (1.0 / (1.0 + 10.0.pow(-((effectiveA - effectiveB + adjustment) / scale)))).coerceIn(0.02, 0.98)
    val animatedA by animateFloatAsState(probabilityA.toFloat(), label = "probability")

    LazyColumn(
        contentPadding = PaddingValues(16.dp, 18.dp, 16.dp, 92.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item {
            SectionIntro(
                eyebrow = "HEAD-TO-HEAD · ${model.label.uppercase()}",
                title = "A vs B probability",
                body = "Change any control and the estimate updates immediately. Context is explicit, never hidden."
            )
        }
        item {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                EntityButton(a, "Competitor A", Modifier.weight(1f)) { pickerForA = true }
                FilledTonalIconButton(onClick = onSwap) { Icon(Icons.Default.SwapVert, "Swap competitors") }
                EntityButton(b, "Competitor B", Modifier.weight(1f)) { pickerForA = false }
            }
        }
        item {
            ContextSelector(sport, contextShift, onSelect = { contextShift = it })
        }
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Paper),
                border = androidx.compose.foundation.BorderStroke(1.dp, Rule)
            ) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(a.name, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Text("${(probabilityA * 100).toInt()}%", fontSize = 26.sp, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
                    }
                    ProbabilityBar(animatedA)
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("A ${(probabilityA * 100).toInt()}%", color = Cobalt, fontWeight = FontWeight.Bold)
                        Text("B ${((1 - probabilityA) * 100).toInt()}%", color = Violet, fontWeight = FontWeight.Bold)
                    }
                    HorizontalDivider(color = Rule)
                    val contextNote = if (sport == Sport.TENNIS) "$surface surface ratings" else "${sport.context.lowercase()} ${if (contextShift == 0) "neutral" else if (contextShift > 0) "favours A" else "favours B"}"
                    Text("${formatRating(effectiveA)} vs ${formatRating(effectiveB)} · $contextNote", color = Muted, fontSize = 11.sp)
                }
            }
        }
        item {
            OutlinedButton(onClick = onModelClick, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Default.Tune, null, modifier = Modifier.size(17.dp))
                Spacer(Modifier.width(8.dp))
                Text("Model: ${model.label}")
            }
        }
    }

    pickerForA?.let { selectingA ->
        ModalBottomSheet(onDismissRequest = { pickerForA = null }, containerColor = Paper) {
            Text(
                if (selectingA) "Choose competitor A" else "Choose competitor B",
                fontFamily = FontFamily.Serif,
                fontWeight = FontWeight.Bold,
                fontSize = 22.sp,
                modifier = Modifier.padding(horizontal = 20.dp, vertical = 12.dp)
            )
            LazyColumn(Modifier.fillMaxWidth().heightIn(max = 520.dp)) {
                itemsIndexed(entries.take(50), key = { _, item -> "picker:${item.id}" }) { index, item ->
                    Row(
                        modifier = Modifier.fillMaxWidth().clickable {
                            if (selectingA) onSelectA(index) else onSelectB(index)
                            pickerForA = null
                        }.padding(horizontal = 20.dp, vertical = 12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Monogram(item.name)
                        Spacer(Modifier.width(12.dp))
                        Text(item.name, modifier = Modifier.weight(1f), fontWeight = FontWeight.SemiBold)
                        Text(formatRating(item.rating), fontFamily = FontFamily.Monospace)
                    }
                }
            }
        }
    }
}

@Composable
private fun EntityButton(entry: RatingEntry, label: String, modifier: Modifier, onClick: () -> Unit) {
    Surface(onClick = onClick, modifier = modifier, color = Paper, shape = RoundedCornerShape(12.dp), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
        Column(Modifier.padding(12.dp)) {
            Text(label.uppercase(), fontFamily = FontFamily.Monospace, fontSize = 8.sp, color = Muted)
            Text(entry.name, fontWeight = FontWeight.Bold, fontSize = 13.sp, maxLines = 2, overflow = TextOverflow.Ellipsis)
            Text(formatRating(entry.rating), color = Cobalt, fontFamily = FontFamily.Monospace, fontSize = 11.sp)
        }
    }
}

@Composable
private fun ContextSelector(sport: Sport, selected: Int, onSelect: (Int) -> Unit) {
    val labels = when (sport) {
        Sport.TENNIS -> listOf("Hard", "Clay", "Grass")
        Sport.CLUBS, Sport.NATIONS -> listOf("B home", "Neutral", "A home")
        Sport.CHESS -> listOf("B white", "Random", "A white")
    }
    Column {
        Text(sport.context.uppercase(), fontFamily = FontFamily.Monospace, fontSize = 9.sp, color = Muted, modifier = Modifier.padding(bottom = 6.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            listOf(-1, 0, 1).forEachIndexed { index, value ->
                val active = selected == value
                Surface(
                    onClick = { onSelect(value) },
                    color = if (active) Ink else Paper,
                    contentColor = if (active) Color.White else Ink,
                    shape = RoundedCornerShape(8.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, if (active) Ink else Rule),
                    modifier = Modifier.weight(1f)
                ) {
                    Text(labels[index], textAlign = androidx.compose.ui.text.style.TextAlign.Center, fontSize = 11.sp, modifier = Modifier.padding(vertical = 9.dp))
                }
            }
        }
    }
}

@Composable
private fun ProbabilityBar(probabilityA: Float) {
    Row(Modifier.fillMaxWidth().height(14.dp).clip(RoundedCornerShape(7.dp))) {
        Box(Modifier.weight(probabilityA.coerceAtLeast(0.01f)).fillMaxHeight().background(Cobalt))
        Box(Modifier.weight((1f - probabilityA).coerceAtLeast(0.01f)).fillMaxHeight().background(Violet))
    }
}

@Composable
private fun ForecastScreen(sport: Sport, model: RatingModel, data: RatingLoadState) {
    if (data !is RatingLoadState.Ready) {
        LoadingPane("Preparing competition forecast…")
        return
    }
    val leaders = data.snapshot.entries.take(5)
    val scale = if (model == RatingModel.ELO) 110.0 else 2.7
    val maxRating = leaders.maxOfOrNull { it.rating } ?: 0.0
    val weights = leaders.map { exp((it.rating - maxRating) / scale) }
    val total = weights.sum().takeIf { it > 0 } ?: 1.0
    val title = when (sport) {
        Sport.TENNIS -> "Next published ATP draw"
        Sport.CLUBS -> "Current club competition"
        Sport.NATIONS -> "Current national-team competition"
        Sport.CHESS -> "Next elite tournament"
    }
    LazyColumn(
        contentPadding = PaddingValues(16.dp, 18.dp, 16.dp, 92.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            SectionIntro(
                eyebrow = "CURRENT STATE · ${model.label.uppercase()}",
                title = "Competition forecast",
                body = "A compact live view. Forecasts update from the same ratings; market prices remain a separate benchmark."
            )
        }
        item {
            Card(colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
                Column(Modifier.padding(16.dp)) {
                    Text(title, fontFamily = FontFamily.Serif, fontSize = 19.sp, fontWeight = FontWeight.Bold)
                    Text("MODEL PROBABILITY · NOT MARKET PRICE", color = Muted, fontFamily = FontFamily.Monospace, fontSize = 8.sp)
                    Spacer(Modifier.height(12.dp))
                    leaders.forEachIndexed { index, entry ->
                        ForecastRow(entry, weights[index] / total)
                        if (index != leaders.lastIndex) HorizontalDivider(color = Rule)
                    }
                }
            }
        }
        item {
            Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFE9EEF9))) {
                Row(Modifier.padding(14.dp), verticalAlignment = Alignment.Top) {
                    Icon(Icons.Default.Info, null, tint = Cobalt, modifier = Modifier.size(18.dp))
                    Spacer(Modifier.width(9.dp))
                    Text("This first native build shows a rating-state forecast. Tournament brackets, fixtures, Polymarket and Kalshi comparison are the next data integration milestone.", fontSize = 12.sp, color = Ink)
                }
            }
        }
    }
}

@Composable
private fun ForecastRow(entry: RatingEntry, probability: Double) {
    Row(Modifier.fillMaxWidth().padding(vertical = 11.dp), verticalAlignment = Alignment.CenterVertically) {
        Monogram(entry.name)
        Spacer(Modifier.width(10.dp))
        Column(Modifier.weight(1f)) {
            Text(entry.name, fontWeight = FontWeight.Bold, fontSize = 13.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
            Box(Modifier.fillMaxWidth().padding(top = 5.dp).height(5.dp).clip(CircleShape).background(Rule)) {
                Box(Modifier.fillMaxWidth(probability.toFloat().coerceIn(0f, 1f)).fillMaxHeight().background(Cobalt))
            }
        }
        Spacer(Modifier.width(12.dp))
        Text("${(probability * 100).toInt()}%", fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 16.sp)
    }
}

@Composable
private fun PlayersScreen() {
    val uriHandler = LocalUriHandler.current
    LazyColumn(
        contentPadding = PaddingValues(16.dp, 18.dp, 16.dp, 92.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            SectionIntro(
                eyebrow = "LINEUPS · MINUTES · RESULTS",
                title = "Historical Player Lab",
                body = "Individual football contribution is published only when lineups, substitutions and stable player identifiers pass validation."
            )
        }
        item {
            Card(colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
                Column(Modifier.padding(17.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
                    Text("Men's World Cup 2026", fontFamily = FontFamily.Serif, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    Text("DATA VALIDATION IN PROGRESS", color = Cobalt, fontFamily = FontFamily.Monospace, fontSize = 9.sp)
                    CheckLine("Starting XI for every match")
                    CheckLine("Substitution minutes and minutes played")
                    CheckLine("Stable player and match identifiers")
                    Text("No result-only player ranking will be substituted for lineup evidence.", color = Muted, fontSize = 12.sp)
                    Button(onClick = { uriHandler.openUri("https://kieranmcshane.github.io/player-lab/") }, modifier = Modifier.fillMaxWidth()) {
                        Text("Open the full Player Lab")
                    }
                }
            }
        }
    }
}

@Composable
private fun CheckLine(text: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(Icons.Default.Check, null, tint = Positive, modifier = Modifier.size(17.dp))
        Spacer(Modifier.width(8.dp))
        Text(text, fontSize = 12.sp)
    }
}

@Composable
private fun MethodsScreen() {
    val sections = listOf(
        "Deterministic replay" to "Every rating is rebuilt in chronological order from public results. Browser and app code consume static JSON; credentials never ship to clients.",
        "Context adjustments" to "Home advantage in football, colour in chess, and tennis surface are explicit inputs. The A vs B screen exposes the chosen context.",
        "Model comparison" to "Elo, Glicko-2, Gaussian TrueSkill and robust heavy-tailed TrueSkill are evaluated out of sample. Market probabilities are benchmarks, not training labels.",
        "Reproducibility" to "Generation timestamps, model parameters, source status, licences and validation rules are published in the data manifest."
    )
    LazyColumn(
        contentPadding = PaddingValues(16.dp, 18.dp, 16.dp, 92.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        item { SectionIntro("AUDITABLE BY DESIGN", "Methods & data", "The explanation stays collapsed until you ask for it; the controls remain close.") }
        itemsIndexed(sections) { index, section ->
            var open by rememberSaveable(index) { mutableStateOf(index == 0) }
            Card(onClick = { open = !open }, colors = CardDefaults.cardColors(containerColor = Paper), border = androidx.compose.foundation.BorderStroke(1.dp, Rule)) {
                Column(Modifier.padding(16.dp).animateContentSize()) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(section.first, modifier = Modifier.weight(1f), fontWeight = FontWeight.Bold)
                        Text(if (open) "−" else "+", fontFamily = FontFamily.Monospace, fontSize = 20.sp, color = Cobalt)
                    }
                    AnimatedVisibility(open) {
                        Text(section.second, color = Muted, fontSize = 12.sp, lineHeight = 18.sp, modifier = Modifier.padding(top = 10.dp))
                    }
                }
            }
        }
    }
}

@Composable
private fun SectionIntro(eyebrow: String, title: String, body: String) {
    Column(verticalArrangement = Arrangement.spacedBy(5.dp), modifier = Modifier.padding(bottom = 3.dp)) {
        Text(eyebrow, color = Muted, fontFamily = FontFamily.Monospace, fontSize = 9.sp, letterSpacing = 0.6.sp)
        Text(title, fontFamily = FontFamily.Serif, fontSize = 25.sp, fontWeight = FontWeight.SemiBold)
        Text(body, color = Muted, fontSize = 12.sp, lineHeight = 17.sp)
    }
}

@Composable
private fun LoadingPane(message: String) {
    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(12.dp)) {
            CircularProgressIndicator(modifier = Modifier.size(28.dp), strokeWidth = 2.dp)
            Text(message, color = Muted, fontSize = 12.sp)
        }
    }
}

@Composable
private fun ErrorPane(message: String) {
    Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(Icons.Default.Close, null, tint = Negative)
            Text(message, color = Muted, modifier = Modifier.padding(top = 8.dp))
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ModelSheet(selected: RatingModel, onSelect: (RatingModel) -> Unit, onDismiss: () -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss, containerColor = Paper) {
        Column(Modifier.fillMaxWidth().padding(start = 20.dp, end = 20.dp, bottom = 28.dp)) {
            Text("Rating model", fontFamily = FontFamily.Serif, fontSize = 24.sp, fontWeight = FontWeight.Bold)
            Text("Switch without returning to the top of the leaderboard.", color = Muted, fontSize = 12.sp, modifier = Modifier.padding(top = 3.dp, bottom = 14.dp))
            RatingModel.entries.forEach { model ->
                Surface(
                    onClick = { onSelect(model) },
                    color = if (model == selected) Color(0xFFE9EEF9) else Color.Transparent,
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(model.label, fontWeight = FontWeight.Bold)
                            Text(
                                if (model.hasUncertainty) "Dynamic uncertainty · conservative ranking" else "Transparent baseline · no σ",
                                color = Muted,
                                fontSize = 11.sp
                            )
                        }
                        if (model == selected) Icon(Icons.Default.Check, "Selected", tint = Cobalt)
                    }
                }
            }
        }
    }
}

private fun formatRating(value: Double): String = NumberFormat.getNumberInstance().apply { maximumFractionDigits = 1 }.format(value)
