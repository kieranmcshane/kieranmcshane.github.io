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

data class RatingEntry(
    val id: String,
    val name: String,
    val country: String?,
    val competition: String,
    val rating: Double,
    val sigma: Double?,
    val change30: Double,
    val matches: Int,
    val lastPlayed: String,
    val history: List<Double>,
    val contextRatings: Map<String, Double> = emptyMap()
)

data class RatingSnapshot(
    val generatedAt: String,
    val modelLabel: String,
    val metrics: Map<String, Double>,
    val entries: List<RatingEntry>,
    val isFallback: Boolean = false
)

sealed interface RatingLoadState {
    data object Loading : RatingLoadState
    data class Ready(val snapshot: RatingSnapshot) : RatingLoadState
    data class Failed(val message: String) : RatingLoadState
}
