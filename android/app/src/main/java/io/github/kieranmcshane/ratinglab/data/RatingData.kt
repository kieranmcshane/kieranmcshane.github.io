package io.github.kieranmcshane.ratinglab.data

enum class Sport(val label: String, val fileName: String, val context: String) {
    TENNIS("Tennis", "tennis", "Surface"),
    CLUBS("Clubs", "football", "Venue"),
    NATIONS("Nations", "national-football", "Venue"),
    CHESS("Chess", "chess", "Colour")
}

enum class RatingModel(val key: String, val label: String, val hasUncertainty: Boolean) {
    ELO("elo", "Elo", false),
    GLICKO2("glicko2", "Glicko-2", true),
    TRUESKILL("trueskill", "TrueSkill", true),
    ROBUST("robust", "Robust", true)
}

data class ContextRating(
    val rating: Double,
    val sigma: Double?,
    val matches: Int
)

data class EntityMedia(
    val kind: String,
    val url: String,
    val sourceUrl: String?,
    val attribution: String?,
    val license: String?
)

data class RatingEntry(
    val id: String,
    val name: String,
    val country: String?,
    val competition: String,
    val rating: Double,
    val sigma: Double?,
    val change30: Double,
    val matches: Int,
    val recentMatches: Int,
    val lastPlayed: String,
    val history: List<Double>,
    val contexts: Map<String, ContextRating> = emptyMap(),
    val provisional: Boolean = false,
    val provisionalReason: String? = null,
    val media: EntityMedia? = null
)

data class ForecastEntry(
    val id: String,
    val name: String,
    val currentRank: Int?,
    val played: Int?,
    val currentPoints: Double?,
    val expectedPoints: Double?,
    val expectedPosition: Double?,
    val champion: Double?,
    val topFour: Double?,
    val bottomThree: Double?,
    val reachNextStage: Double?,
    val rating: Double?
)

data class PerformanceEntry(
    val id: String,
    val name: String,
    val rank: Int,
    val performanceRating: Double,
    val change: Double,
    val matches: Int,
    val wins: Int,
    val draws: Int,
    val losses: Int
)

data class MarketOutcome(
    val entityId: String,
    val name: String,
    val probability: Double,
    val rawProbability: Double?,
    val bestBid: Double?,
    val bestAsk: Double?
)

data class MarketSnapshot(
    val provider: String,
    val status: String,
    val competitionId: String,
    val eventTitle: String,
    val eventUrl: String?,
    val checkedAt: String?,
    val rawProbabilitySum: Double?,
    val coverage: Double?,
    val definition: String,
    val outcomes: List<MarketOutcome>
)

data class CompetitionForecast(
    val id: String,
    val label: String,
    val season: String,
    val format: String,
    val status: String,
    val availability: String,
    val firstFixture: String?,
    val lastFixture: String?,
    val nextFixture: String?,
    val forecastType: String?,
    val simulations: Int?,
    val completedMatches: Int?,
    val remainingMatches: Int?,
    val currentStage: String?,
    val forecast: List<ForecastEntry>,
    val performanceMethod: String?,
    val performance: List<PerformanceEntry>,
    val markets: List<MarketSnapshot>,
    val sourceUrl: String?,
    val license: String?
)

data class SourceEvidence(
    val name: String,
    val url: String,
    val license: String,
    val latestResult: String,
    val staleAfterHours: Int,
    val firstResult: String,
    val matches: Int,
    val entities: Int,
    val eligibilityRule: String,
    val outcomeMethod: String
)

data class RatingSnapshot(
    val schemaVersion: String,
    val generatedAt: String,
    val modelLabel: String,
    val metrics: Map<String, Double>,
    val parameters: Map<String, Double>,
    val drawRate: Double,
    val entries: List<RatingEntry>,
    val competitions: List<CompetitionForecast>,
    val evidence: SourceEvidence,
    val predictorMethod: String?,
    val isFallback: Boolean = false
)

enum class PlayerModel(
    val key: String,
    val label: String,
    val teamScoped: Boolean = false
) {
    LINEUP("lineup-trueskill", "Lineup"),
    RAPM("rapm", "RAPM"),
    CHEMISTRY("pairwise-chemistry", "Chemistry"),
    HAPM("hapm", "HAPM", true),
    LAPM("lapm", "LAPM", true)
}

data class PlayerEntry(
    val id: String,
    val name: String,
    val country: String?,
    val team: String,
    val rank: Int,
    val score: Double,
    val impact: Double?,
    val mean: Double?,
    val uncertainty: Double,
    val minutes: Double,
    val matches: Int,
    val status: String? = null,
    val media: EntityMedia? = null
)

data class PlayerCombination(
    val label: String,
    val order: Int,
    val impact: Double,
    val uncertainty: Double,
    val minutes: Double,
    val stints: Int
)

data class PlayerTeamModel(
    val id: String,
    val name: String,
    val rankings: List<PlayerEntry>,
    val combinations: List<PlayerCombination>,
    val validationStatus: String?,
    val validationDelta: Double?,
    val retainedNodes: Int?,
    val omittedOvercompleteStints: Int?
)

data class PlayerModelSnapshot(
    val key: String,
    val label: String,
    val status: String?,
    val rankingRule: String,
    val rankings: List<PlayerEntry>,
    val teams: List<PlayerTeamModel>,
    val metrics: Map<String, Double>
)

data class PlayerCohort(
    val id: String,
    val name: String,
    val gender: String,
    val format: String,
    val scopeType: String,
    val firstMatch: String,
    val lastMatch: String,
    val matches: Int,
    val eligiblePlayers: Int,
    val minimumMinutes: Double,
    val minimumMatches: Int,
    val sourceName: String,
    val sourceUrl: String,
    val license: String,
    val coverage: Map<String, Double>,
    val models: Map<String, PlayerModelSnapshot>,
    val snapshotSha256: String
)

data class PlayerDataset(
    val schemaVersion: String,
    val generatedAt: String,
    val cohorts: List<PlayerCohort>,
    val inputSummary: String,
    val excludedInputs: List<String>,
    val interpretation: String,
    val worldCupStatus: String?,
    val worldCupMessage: String?
)

sealed interface RatingLoadState {
    data object Loading : RatingLoadState
    data class Ready(val snapshot: RatingSnapshot) : RatingLoadState
    data class Failed(val message: String) : RatingLoadState
}

sealed interface PlayerLoadState {
    data object NotRequested : PlayerLoadState
    data object Loading : PlayerLoadState
    data class Ready(val dataset: PlayerDataset) : PlayerLoadState
    data class Failed(val message: String) : PlayerLoadState
}
