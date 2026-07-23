package io.github.kieranmcshane.ratinglab.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import io.github.kieranmcshane.ratinglab.data.RatingLoadState
import io.github.kieranmcshane.ratinglab.data.RatingModel
import io.github.kieranmcshane.ratinglab.data.RatingRepository
import io.github.kieranmcshane.ratinglab.data.Sport
import io.github.kieranmcshane.ratinglab.data.PlayerLoadState
import io.github.kieranmcshane.ratinglab.data.PlayerModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

enum class AppSection(val label: String) {
    RANKINGS("Rankings"),
    COMPARE("A vs B"),
    FORECASTS("Competitions"),
    PLAYERS("Players"),
    METHODS("Methods")
}

data class RatingLabUiState(
    val section: AppSection = AppSection.RANKINGS,
    val sport: Sport = Sport.TENNIS,
    val model: RatingModel = RatingModel.ELO,
    val data: RatingLoadState = RatingLoadState.Loading,
    val competitorA: Int = 0,
    val competitorB: Int = 1,
    val search: String = "",
    val includeProvisional: Boolean = false,
    val competitionId: String? = null,
    val playerData: PlayerLoadState = PlayerLoadState.NotRequested,
    val playerCohortId: String? = null,
    val playerModel: PlayerModel = PlayerModel.LINEUP,
    val playerTeamId: String? = null,
    val playerSearch: String = ""
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
        if (section == AppSection.PLAYERS) loadPlayers()
    }

    fun selectSport(sport: Sport) {
        if (sport == _uiState.value.sport) return
        _uiState.value = _uiState.value.copy(
            sport = sport,
            competitorA = 0,
            competitorB = 1,
            search = "",
            competitionId = null
        )
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

    fun setSearch(value: String) {
        _uiState.value = _uiState.value.copy(search = value)
    }

    fun toggleProvisional() {
        _uiState.value = _uiState.value.copy(
            includeProvisional = !_uiState.value.includeProvisional
        )
    }

    fun selectCompetition(id: String) {
        _uiState.value = _uiState.value.copy(competitionId = id)
    }

    fun selectPlayerCohort(id: String) {
        _uiState.value = _uiState.value.copy(
            playerCohortId = id,
            playerTeamId = null,
            playerSearch = ""
        )
    }

    fun selectPlayerModel(model: PlayerModel) {
        _uiState.value = _uiState.value.copy(playerModel = model, playerTeamId = null)
    }

    fun selectPlayerTeam(id: String) {
        _uiState.value = _uiState.value.copy(playerTeamId = id)
    }

    fun setPlayerSearch(value: String) {
        _uiState.value = _uiState.value.copy(playerSearch = value)
    }

    fun refresh() {
        cache.remove(_uiState.value.sport to _uiState.value.model)
        if (_uiState.value.section == AppSection.PLAYERS) {
            _uiState.value = _uiState.value.copy(playerData = PlayerLoadState.NotRequested)
            loadPlayers()
        }
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
                        val selectedCompetition = _uiState.value.competitionId
                            ?.takeIf { id -> snapshot.competitions.any { it.id == id } }
                            ?: snapshot.competitions.firstOrNull()?.id
                        _uiState.value = _uiState.value.copy(
                            data = ready,
                            competitionId = selectedCompetition
                        )
                    }
                }
                .onFailure { error ->
                    _uiState.value = _uiState.value.copy(
                        data = RatingLoadState.Failed(error.message ?: "Unable to load ratings")
                    )
                }
        }
    }

    private fun loadPlayers() {
        if (_uiState.value.playerData is PlayerLoadState.Loading ||
            _uiState.value.playerData is PlayerLoadState.Ready
        ) return
        _uiState.value = _uiState.value.copy(playerData = PlayerLoadState.Loading)
        viewModelScope.launch {
            runCatching { repository.loadPlayers() }
                .onSuccess { dataset ->
                    val cohort = dataset.cohorts.firstOrNull()
                    _uiState.value = _uiState.value.copy(
                        playerData = PlayerLoadState.Ready(dataset),
                        playerCohortId = cohort?.id
                    )
                }
                .onFailure { error ->
                    _uiState.value = _uiState.value.copy(
                        playerData = PlayerLoadState.Failed(
                            error.message ?: "Unable to load player ratings"
                        )
                    )
                }
        }
    }
}
