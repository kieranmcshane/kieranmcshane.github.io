package io.github.kieranmcshane.ratinglab.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import io.github.kieranmcshane.ratinglab.data.RatingLoadState
import io.github.kieranmcshane.ratinglab.data.RatingModel
import io.github.kieranmcshane.ratinglab.data.RatingRepository
import io.github.kieranmcshane.ratinglab.data.Sport
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

enum class AppSection(val label: String) {
    RANKINGS("Rankings"),
    COMPARE("A vs B"),
    FORECASTS("Forecasts"),
    PLAYERS("Players"),
    METHODS("Methods")
}

data class RatingLabUiState(
    val section: AppSection = AppSection.RANKINGS,
    val sport: Sport = Sport.TENNIS,
    val model: RatingModel = RatingModel.ELO,
    val data: RatingLoadState = RatingLoadState.Loading,
    val competitorA: Int = 0,
    val competitorB: Int = 1
)

class RatingLabViewModel(
    private val repository: RatingRepository = RatingRepository()
) : ViewModel() {
    private val _uiState = MutableStateFlow(RatingLabUiState())
    val uiState: StateFlow<RatingLabUiState> = _uiState.asStateFlow()

    private val cache = mutableMapOf<Pair<Sport, RatingModel>, RatingLoadState.Ready>()

    init {
        refresh()
    }

    fun selectSection(section: AppSection) {
        _uiState.value = _uiState.value.copy(section = section)
    }

    fun selectSport(sport: Sport) {
        if (sport == _uiState.value.sport) return
        _uiState.value = _uiState.value.copy(sport = sport, competitorA = 0, competitorB = 1)
        loadCurrent()
    }

    fun selectModel(model: RatingModel) {
        if (model == _uiState.value.model) return
        _uiState.value = _uiState.value.copy(model = model, competitorA = 0, competitorB = 1)
        loadCurrent()
    }

    fun selectCompetitorA(index: Int) {
        _uiState.value = _uiState.value.copy(competitorA = index)
    }

    fun selectCompetitorB(index: Int) {
        _uiState.value = _uiState.value.copy(competitorB = index)
    }

    fun swapCompetitors() {
        val current = _uiState.value
        _uiState.value = current.copy(competitorA = current.competitorB, competitorB = current.competitorA)
    }

    fun refresh() {
        cache.remove(_uiState.value.sport to _uiState.value.model)
        loadCurrent()
    }

    private fun loadCurrent() {
        val sport = _uiState.value.sport
        val model = _uiState.value.model
        val cached = cache[sport to model]
        if (cached != null) {
            _uiState.value = _uiState.value.copy(data = cached)
            return
        }
        _uiState.value = _uiState.value.copy(data = RatingLoadState.Loading)
        viewModelScope.launch {
            runCatching { repository.load(sport, model) }
                .onSuccess { snapshot ->
                    val ready = RatingLoadState.Ready(snapshot)
                    cache[sport to model] = ready
                    if (_uiState.value.sport == sport && _uiState.value.model == model) {
                        _uiState.value = _uiState.value.copy(data = ready)
                    }
                }
                .onFailure { error ->
                    _uiState.value = _uiState.value.copy(
                        data = RatingLoadState.Failed(error.message ?: "Unable to load ratings")
                    )
                }
        }
    }
}
