(function () {
  'use strict';

  var root = document.querySelector('.player-lab');
  if (!root) return;
  var state = { payload: null, cohort: null, cohortData: {}, model: 'rapm', team: null, query: '', visibleCount: 0, selected: null, detailOpen: false };
  var cohortRequests = {};
  var elements = {
    error: document.getElementById('player-lab-error'),
    generated: document.getElementById('player-lab-generated'),
    sourceStatus: document.getElementById('player-source-status'),
    orderingNote: document.getElementById('player-ordering-note'),
    cohort: document.getElementById('player-cohort'),
    team: document.getElementById('player-team'),
    teamField: document.getElementById('player-team-field'),
    teamLabel: document.getElementById('player-team-label'),
    modelTabs: document.getElementById('player-model-tabs'),
    search: document.getElementById('player-search'),
    metrics: document.getElementById('player-metrics'),
    scope: document.getElementById('player-season-scope'),
    hapmStatus: document.getElementById('player-hapm-status'),
    lapmCombinations: document.getElementById('player-lapm-combinations'),
    lapmNote: document.getElementById('player-lapm-note'),
    lapmLists: document.getElementById('player-lapm-lists'),
    chart: document.getElementById('player-comparison-chart'),
    comparisonHeading: document.getElementById('player-comparison-heading'),
    comparisonCopy: document.getElementById('player-comparison-copy'),
    body: document.getElementById('player-ranking-body'),
    caption: document.getElementById('player-ranking-caption'),
    empty: document.getElementById('player-ranking-empty'),
    more: document.getElementById('player-ranking-more'),
    listStatus: document.getElementById('player-list-status'),
    filtersReturn: document.getElementById('player-filters-return'),
    detail: document.getElementById('player-detail'),
    scoreHeading: document.getElementById('player-score-heading'),
    gates: document.getElementById('player-gates'),
    quickModel: document.getElementById('player-quick-model'),
    quickModelMenu: document.getElementById('player-quick-model-menu'),
    quickModelTrigger: document.getElementById('player-quick-model-trigger'),
    quickModelLabel: document.getElementById('player-quick-model-label')
  };

  function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character];
    });
  }

  function number(value, digits) {
    return new Intl.NumberFormat('en', { maximumFractionDigits: digits }).format(value);
  }

  // Signed display that clamps rounded ±0 to a plain 0, matching the main lab.
  function signedNumber(value, digits) {
    if (value === null || value === undefined) return '—';
    var rounded = Math.round(value * Math.pow(10, digits)) / Math.pow(10, digits);
    if (Object.is(rounded, -0) || rounded === 0) return '0';
    return (rounded > 0 ? '+' : '') + number(rounded, digits);
  }

  function percent(value) {
    return new Intl.NumberFormat('en', { style: 'percent', maximumFractionDigits: 1 }).format(value);
  }

  function date(value) {
    return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(value));
  }

  var regionCodesByName = null;

  function normalizedRegionName(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLocaleLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }

  function buildRegionCodes() {
    if (regionCodesByName) return regionCodesByName;
    regionCodesByName = {};
    if (typeof Intl.DisplayNames === 'function') {
      var names = new Intl.DisplayNames(['en'], { type: 'region' });
      for (var first = 65; first <= 90; first += 1) {
        for (var second = 65; second <= 90; second += 1) {
          var code = String.fromCharCode(first, second);
          var name = names.of(code);
          if (name && name !== code) regionCodesByName[normalizedRegionName(name)] = code;
        }
      }
    }
    Object.assign(regionCodesByName, {
      'cote d ivoire': 'CI', 'czech republic': 'CZ', england: 'gb-eng', france: 'FR',
      ireland: 'IE', 'korea south': 'KR', 'macedonia republic of': 'MK',
      'northern ireland': 'gb-nir', scotland: 'gb-sct', serbia: 'RS',
      'united states of america': 'US', 'venezuela bolivarian republic': 'VE',
      wales: 'gb-wls'
    });
    return regionCodesByName;
  }

  function countryFlagCode(country) {
    var code = buildRegionCodes()[normalizedRegionName(country)] || '';
    return /^(?:[A-Z]{2}|gb-(?:eng|nir|sct|wls))$/.test(code) ? code.toLocaleLowerCase() : '';
  }

  function flagAssetUrl(country) {
    var code = countryFlagCode(country);
    var base = String(root.dataset.flagRoot || '').replace(/\/$/, '');
    return code && base ? base + '/' + code + '.svg' : '';
  }

  function playerFlag(country, className, decorative) {
    var url = flagAssetUrl(country);
    if (!url) return '';
    var label = 'Nationality: ' + country;
    return '<span class="player-lab-country-flag' + (className ? ' ' + escapeHtml(className) : '') +
      '"' + (decorative ? ' aria-hidden="true"' : ' role="img" aria-label="' + escapeHtml(label) + '"') +
      ' title="' + escapeHtml(label) + '"><img src="' +
      escapeHtml(url) + '" alt="" loading="lazy" decoding="async"></span>';
  }

  function currentCohort() {
    return state.cohortData[state.cohort];
  }

  function fetchJson(url) {
    return fetch(url).then(function (response) {
      if (!response.ok) throw new Error('The historical player ratings could not be loaded.');
      return response.json();
    });
  }

  function splitUrl(file) {
    return String(root.dataset.playerData).replace(/player-football\.json$/, 'split/' + file);
  }

  function loadFullPayload() {
    return fetchJson(root.dataset.playerData).then(function (payload) {
      (payload.cohorts || []).forEach(function (cohort) { state.cohortData[cohort.id] = cohort; });
      return payload;
    });
  }

  function ensureCohort(id) {
    if (state.cohortData[id]) return Promise.resolve();
    if (cohortRequests[id]) return cohortRequests[id];
    var summary = (state.payload.cohorts || []).find(function (cohort) { return cohort.id === id; });
    var source = summary && summary.data_url
      ? fetchJson(splitUrl(summary.data_url)).then(function (payload) { return payload.cohort; })
      : Promise.reject(new Error('No split cohort file is published.'));
    cohortRequests[id] = source.catch(function () {
      return loadFullPayload().then(function (payload) {
        var full = (payload.cohorts || []).find(function (cohort) { return cohort.id === id; });
        if (!full) throw new Error('The historical player ratings could not be loaded.');
        return full;
      });
    }).then(function (cohort) {
      state.cohortData[id] = cohort;
      delete cohortRequests[id];
    }, function (error) {
      delete cohortRequests[id];
      throw error;
    });
    return cohortRequests[id];
  }

  var syncToken = 0;

  function syncCohort() {
    var token = ++syncToken;
    if (!state.cohortData[state.cohort]) root.setAttribute('aria-busy', 'true');
    return ensureCohort(state.cohort).then(function () {
      if (token !== syncToken) return;
      root.removeAttribute('aria-busy');
      elements.error.hidden = true;
      render();
    }, function (error) {
      if (token !== syncToken) return;
      root.removeAttribute('aria-busy');
      elements.error.hidden = false;
      elements.error.textContent = error.message;
    });
  }

  function isTeamModel(modelId) {
    return modelId === 'hapm' || modelId === 'lapm';
  }

  function currentTeam(modelId) {
    var teams = currentCohort().models[modelId].teams;
    return teams.find(function (team) { return team.id === state.team; }) || teams[0];
  }

  function renderTeamOptions() {
    var modelId = isTeamModel(state.model) ? state.model : 'hapm';
    var teams = currentCohort().models[modelId].teams;
    if (!teams.some(function (team) { return team.id === state.team; })) state.team = teams[0].id;
    elements.team.innerHTML = teams.map(function (team) {
      return '<option value="' + escapeHtml(team.id) + '">' + escapeHtml(team.name) + '</option>';
    }).join('');
    elements.team.value = state.team;
    elements.teamLabel.textContent = 'Team · ' + currentCohort().models[modelId].label + ' is within-team';
    elements.teamField.hidden = !isTeamModel(state.model);
  }

  function currentRows() {
    var query = state.query.trim().toLocaleLowerCase();
    var rows = isTeamModel(state.model)
      ? currentTeam(state.model).rankings
      : currentCohort().models[state.model].rankings;
    return rows.filter(function (row) {
      return !query || row.name.toLocaleLowerCase().indexOf(query) !== -1 ||
        row.team.toLocaleLowerCase().indexOf(query) !== -1 ||
        String(row.country || '').toLocaleLowerCase().indexOf(query) !== -1;
    });
  }

  function isMobile() {
    return window.matchMedia('(max-width: 650px)').matches;
  }

  function resetList() {
    state.visibleCount = 0;
    state.detailOpen = false;
  }

  function renderCohortOptions() {
    var groups = [
      { id: 'men-season', label: "Men's full seasons", matches: function (cohort) { return cohort.gender === 'men' && cohort.scope_type === 'season'; } },
      { id: 'men-event', label: "Men's tournaments", matches: function (cohort) { return cohort.gender === 'men' && cohort.scope_type !== 'season'; } },
      { id: 'women-season', label: "Women's full seasons", matches: function (cohort) { return cohort.gender === 'women' && cohort.scope_type === 'season'; } },
      { id: 'women-event', label: "Women's tournaments", matches: function (cohort) { return cohort.gender === 'women' && cohort.scope_type !== 'season'; } }
    ];
    var known = {};
    var html = groups.map(function (group) {
      var cohorts = state.payload.cohorts.filter(group.matches);
      cohorts.forEach(function (cohort) { known[cohort.id] = true; });
      if (!cohorts.length) return '';
      return '<optgroup label="' + escapeHtml(group.label) + '">' + cohorts.map(function (cohort) {
        return '<option value="' + escapeHtml(cohort.id) + '">' + escapeHtml(cohort.name) + '</option>';
      }).join('') + '</optgroup>';
    }).join('');
    var historical = state.payload.cohorts.filter(function (cohort) { return !known[cohort.id]; });
    if (historical.length) {
      html += '<optgroup label="Historical competitions">' + historical.map(function (cohort) {
        return '<option value="' + escapeHtml(cohort.id) + '">' + escapeHtml(cohort.name) + '</option>';
      }).join('') + '</optgroup>';
    }
    elements.cohort.innerHTML = html;
  }

  function renderSourceStatus() {
    var statuses = state.payload.source && state.payload.source.statuses;
    var unavailable = Object.keys(statuses || {}).map(function (key) {
      return statuses[key];
    }).filter(function (status) {
      return status.status !== 'published';
    });
    if (!unavailable.length) {
      elements.sourceStatus.hidden = true;
      elements.sourceStatus.textContent = '';
      return;
    }
    elements.sourceStatus.hidden = false;
    var worldCup = unavailable.find(function (status) {
      return status.cohort === 'world-cup-2026';
    });
    var summaryParts = [];
    var leagueSeasons = unavailable.filter(function (status) {
      return String(status.cohort || '').indexOf('premier-league-') === 0;
    });
    var parts = [];
    if (leagueSeasons.length) {
      summaryParts.push(leagueSeasons.length + ' recent Premier League season' + (leagueSeasons.length === 1 ? '' : 's'));
      parts.push('<strong>Some recent men’s league seasons remain withheld.</strong> ' +
        leagueSeasons.map(function (status) {
          return escapeHtml(status.cohort.replace('premier-league-', 'Premier League ').replace(/-/g, '/'));
        }).join(', ') +
        ' did not pass source access and completeness gates in this build.');
    }
    if (worldCup) {
      summaryParts.push('World Cup 2026');
      var accessBlocked = worldCup.reason === 'provider_plan_does_not_include_2026';
      parts.push('<strong>' +
        (accessBlocked ? 'World Cup 2026 data access required.' : 'World Cup 2026 withheld.') +
        '</strong> ' +
        escapeHtml(worldCup.message || 'The required complete lineup and event feed has not passed every publication gate.'));
    }
    if (!summaryParts.length) summaryParts.push(unavailable.length + ' cohort' + (unavailable.length === 1 ? '' : 's'));
    parts.push('Nothing is published without every declared fixture, stable player IDs, starting lineups, substitution minutes, player minutes and reproduced results.');
    // One quiet line by default; the full publication-gate explanation on demand.
    elements.sourceStatus.innerHTML = '<details><summary><strong>' +
      escapeHtml(summaryParts.join(' and ')) + ' withheld</strong> — why</summary><div>' +
      parts.join(' ') + '</div></details>';
  }

  function renderMetrics() {
    var cohort = currentCohort();
    var model = cohort.models[state.model];
    var modelMetric;
    if (state.model === 'lineup-trueskill') {
      var uniformBaseline = model.metrics.log_loss_uniform_baseline || 1.099;
      var priorBaseline = model.metrics.log_loss_home_prior_baseline;
      modelMetric = ['Held-out log loss', number(model.metrics.log_loss, 3),
        model.metrics.chronological_predictions + ' predictions recorded before updating · uniform guess ' +
        number(uniformBaseline, 3) + (priorBaseline ? ' · home-frequency prior ' + number(priorBaseline, 3) : '') +
        ' on the same replay'];
    } else if (state.model === 'rapm') {
      modelMetric = ['Validation RMSE', number(model.metrics.validation_rmse, 3), model.metrics.chronological_validation_matches + ' chronological validation matches'];
    } else if (state.model === 'pairwise-chemistry') {
      var delta = model.metrics.validation_delta;
      var deltaLabel = signedNumber(delta, 3) + ' vs RAPM';
      modelMetric = ['Chemistry validation', deltaLabel, model.status === 'supported' ? 'Held-out RMSE is competitive with the additive baseline' : 'Descriptive only: held-out RMSE did not support the interaction layer'];
    } else if (state.model === 'hapm') {
      var hapmTeam = currentTeam('hapm');
      var hapmDelta = hapmTeam.diagnostics.validation_delta;
      var hapmMetrics = model.metrics;
      modelMetric = ['HAPM · experimental',
        number(hapmMetrics.teams_beating_full_lineup_baseline, 0) + '/' +
          number(hapmMetrics.teams_evaluated, 0) + ' teams',
        hapmTeam.name + ': ' + signedNumber(hapmDelta, 3) +
          ' RMSE vs full-lineup APM · ' +
          (hapmTeam.diagnostics.validation_status === 'supported' ? 'beat baseline' : 'descriptive only')];
    } else {
      var team = currentTeam('lapm');
      modelMetric = ['LAPM graph', number(team.diagnostics.retained_nodes, 0) + ' nodes',
        number(team.diagnostics.jaccard_edges, 0) + ' Jaccard links · within ' + team.name];
    }
    var metrics = [
      ['Matches', number(cohort.matches, 0), (cohort.format || 'historical cohort') + ' · ' + cohort.first_match + ' to ' + cohort.last_match],
      ['Eligible players', number(cohort.eligible_players, 0), 'Minimum ' + number(cohort.eligibility.minimum_minutes, 0) + ' minutes and ' + cohort.eligibility.minimum_matches + ' appearances'],
      [modelMetric[0], modelMetric[1], modelMetric[2]],
      ['Lineup coverage', percent(cohort.coverage.starting_lineups), 'Player-match graph: ' + cohort.coverage.player_match_graph_components + ' connected component']
    ];
    elements.metrics.innerHTML = metrics.map(function (metric) {
      return '<div class="rating-lab-metric"><span>' + escapeHtml(metric[0]) + '</span><div class="rating-lab-metric-value"><strong>' +
        escapeHtml(metric[1]) + '</strong></div><small>' + escapeHtml(metric[2]) + '</small></div>';
    }).join('');
  }

  function renderScope() {
    var cohort = currentCohort();
    var included = cohort.included_competitions || [cohort.name];
    var expected = cohort.coverage.expected_matches || cohort.matches;
    var hapmMetrics = cohort.models.hapm.metrics;
    elements.scope.innerHTML = '<strong>' + (cohort.scope_type === 'season' ? 'Season scope' : 'Competition scope') + '</strong>' +
      '<span>Included: ' + escapeHtml(included.join(', ')) + ' · ' + number(cohort.matches, 0) + '/' + number(expected, 0) + ' matches.</span>' +
      (cohort.scope_note ? '<small>' + escapeHtml(cohort.scope_note) + '</small>' : '');
    elements.hapmStatus.innerHTML = '<strong>HAPM remains experimental.</strong> ' +
      number(hapmMetrics.teams_beating_full_lineup_baseline, 0) + ' of ' +
      number(hapmMetrics.teams_evaluated, 0) +
      ' teams beat the simpler full-lineup APM on strictly later held-out stints in this cohort. ' +
      'Team-level results are visible for diagnosis, but ridge-regularized RAPM remains the primary ranking, ' +
      'with Lineup TrueSkill published as the sequential baseline.';
  }

  function renderOrderingNote() {
    var lineupModel = currentCohort().models['lineup-trueskill'];
    var note = lineupModel.ordering_note ||
      'One shared result per match separates teammates who are usually on the pitch together only weakly, ' +
      'so the per-player uncertainties remain comparable to the spread of the means and this conservative ' +
      'ordering is noise-dominated. It is published as the auditable sequential baseline; ridge-regularized ' +
      'RAPM is the default ranking.';
    elements.orderingNote.innerHTML = '<strong>Read this ordering with care.</strong> ' + escapeHtml(note);
    elements.orderingNote.hidden = state.model !== 'lineup-trueskill';
  }

  function renderTeamCombinations() {
    elements.lapmCombinations.hidden = !isTeamModel(state.model);
    if (!isTeamModel(state.model)) return;
    var team = currentTeam(state.model);
    function list(label, rows) {
      return '<article><h4>' + escapeHtml(label) + '</h4><ol>' + rows.slice(0, 5).map(function (row) {
        var readable = row.order > 3 ? row.order + '-player observed lineup' : row.label;
        return '<li><span><b>' + escapeHtml(readable) + '</b><small>' + number(row.minutes, 0) +
          ' minutes · ' + row.stints + ' stints</small></span><strong>' + signedNumber(row.impact, 2) + '</strong></li>';
      }).join('') + '</ol></article>';
    }
    if (state.model === 'hapm') {
      var orders = team.combinations.by_order || [];
      var pairs = orders.find(function (order) { return order.order === 2; }) || { outperformers: [] };
      var trios = orders.find(function (order) { return order.order === 3; }) || { outperformers: [] };
      document.getElementById('player-lapm-combinations-heading').textContent = 'What the extended hypergraph sees';
      elements.lapmNote.textContent = team.name + ' · ' + number(team.diagnostics.retained_nodes, 0) +
        ' retained nodes · orders 1–4 plus full lineups · ridge ' + number(team.diagnostics.selected_ridge_penalty, 1) +
        ' · experimental · ' + (team.diagnostics.validation_status === 'supported' ? 'beat full-lineup APM for this team' : 'descriptive after held-out comparison') +
        ' · ' + number(team.diagnostics.omitted_overcomplete_stints || 0, 0) + ' source-overlap intervals omitted';
      elements.lapmLists.innerHTML = list('Highest-rated pairs', pairs.outperformers || []) +
        list('Highest-rated trios', trios.outperformers || []);
    } else {
      document.getElementById('player-lapm-combinations-heading').textContent = 'What the lineup graph sees';
      elements.lapmNote.textContent = team.name + ' · ' + number(team.diagnostics.retained_nodes, 0) +
        ' retained nodes · ' + number(team.diagnostics.jaccard_edges, 0) +
        ' non-zero Jaccard links. Full-lineup labels collapse to player count on small screens.';
      elements.lapmLists.innerHTML = list('Graph outperformers', team.combinations.outperformers || []) +
        list('Graph underperformers', team.combinations.underperformers || []);
    }
  }

  // Geometry and point lookup from the latest full chart render, so a
  // selection change can update two buttons in place instead of rebuilding
  // all ~324 markers (which made every click feel slow and flicker flags).
  var chartView = null;

  function chartSelectionCard(point) {
    var width = chartView.width, height = chartView.height;
    var cardWidth = Math.min(185, width - 16), cardHeight = 150;
    var preferredCardLeft = point.px > width / 2 ? point.px - cardWidth - 15 : point.px + 15;
    var preferredCardTop = point.py < cardHeight + 14 ? point.py + 14 : point.py - cardHeight - 14;
    var cardLeft = Math.max(8, Math.min(width - cardWidth - 8, preferredCardLeft));
    var cardTop = Math.max(8, Math.min(height - cardHeight - 8, preferredCardTop));
    var pointMeta = point.country && point.country !== point.team
      ? point.country + ' · ' + point.team
      : point.team || point.country || 'Nationality unavailable';
    return '<strong class="player-lab-point-card" style="--card-left:' +
      (cardLeft - point.px).toFixed(1) + 'px;--card-top:' + (cardTop - point.py).toFixed(1) + 'px;--card-width:' + cardWidth + 'px">' +
      '<span class="player-lab-point-card-name">' + playerFlag(point.country, '', true) + '<span>' + escapeHtml(point.name) + '</span></span>' +
      '<span class="player-lab-point-card-meta">' + escapeHtml(pointMeta) + '</span>' +
      '<span class="player-lab-point-card-ranks"><span>Lineup <b>#' + point.trueRank + '</b></span><span>' + chartView.comparisonShort + ' <b>#' + point.comparisonRank + '</b></span></span>' +
      '<span class="player-lab-point-card-scores">Scores ' + number(point.trueScore, 2) + ' · ' + number(point.comparisonScore, 2) + '</span></strong>';
  }

  function updateChartSelection() {
    var frame = elements.chart.querySelector('.player-lab-chart-frame');
    if (!frame || !chartView) return renderChart();
    var previous = frame.querySelector('.player-lab-point.is-selected');
    if (previous) {
      previous.classList.remove('is-selected');
      var oldCard = previous.querySelector('.player-lab-point-card');
      if (oldCard) oldCard.remove();
      // A flag granted only because of the selection goes back to a dot.
      if (chartView.flagged && !chartView.flagged[previous.dataset.playerId]) {
        previous.classList.remove('has-country-flag');
        if (previous.firstElementChild) previous.firstElementChild.innerHTML = '';
      }
    }
    // Exactly one marker stays in the tab order.
    frame.querySelectorAll('.player-lab-point[tabindex="0"]').forEach(function (marker) {
      marker.tabIndex = -1;
    });
    if (!state.selected) {
      var first = frame.querySelector('.player-lab-point');
      if (first) first.tabIndex = 0;
      return;
    }
    var point = chartView.byId[state.selected];
    var button = point && frame.querySelector('.player-lab-point[data-player-id="' + String(state.selected).replace(/"/g, '\\"') + '"]');
    if (!button) return renderChart();
    button.classList.add('is-selected');
    button.tabIndex = 0;
    button.insertAdjacentHTML('beforeend', chartSelectionCard(point));
  }

  function standardized(rows) {
    var values = rows.map(function (row) { return row.score; });
    var mean = values.reduce(function (sum, value) { return sum + value; }, 0) / Math.max(values.length, 1);
    var variance = values.reduce(function (sum, value) { return sum + Math.pow(value - mean, 2); }, 0) / Math.max(values.length, 1);
    var scale = Math.sqrt(variance) || 1;
    var result = {};
    rows.forEach(function (row) { result[row.id] = (row.score - mean) / scale; });
    return result;
  }

  function renderChart() {
    var cohort = currentCohort();
    var trueRows = cohort.models['lineup-trueskill'].rankings;
    var comparisonId = state.model === 'pairwise-chemistry' ? 'pairwise-chemistry' : isTeamModel(state.model) ? state.model : 'rapm';
    var comparisonModel = cohort.models[comparisonId];
    var comparisonRows = isTeamModel(comparisonId) ? currentTeam(comparisonId).rankings : comparisonModel.rankings;
    var comparisonLabel = comparisonId === 'pairwise-chemistry' ? 'Pairwise chemistry' : isTeamModel(comparisonId) ? comparisonModel.label + ' · ' + currentTeam(comparisonId).name : 'RAPM';
    var comparisonShort = comparisonId === 'pairwise-chemistry' ? 'Chemistry' : isTeamModel(comparisonId) ? comparisonModel.label : 'RAPM';
    if (isTeamModel(comparisonId)) {
      var teamIds = comparisonRows.reduce(function (items, row) { items[row.id] = true; return items; }, {});
      trueRows = trueRows.filter(function (row) { return teamIds[row.id]; });
    }
    var trueZ = standardized(trueRows), comparisonZ = standardized(comparisonRows);
    var byId = {};
    trueRows.forEach(function (row) { byId[row.id] = row; });
    var points = comparisonRows.filter(function (row) { return trueZ[row.id] !== undefined; }).map(function (row) {
      return {
        id: row.id, name: row.name, team: row.team, country: row.country,
        x: trueZ[row.id], y: comparisonZ[row.id], trueRank: byId[row.id].rank,
        comparisonRank: row.rank, trueScore: byId[row.id].score, comparisonScore: row.score
      };
    });
    elements.comparisonHeading.textContent = 'Lineup TrueSkill versus ' + comparisonLabel;
    elements.comparisonCopy.textContent = comparisonId === 'pairwise-chemistry'
      ? 'The interaction axis rates residual teammate chemistry after RAPM. Upper-right players rate highly under both lenses; select a marker for exact ranks.'
      : comparisonId === 'hapm'
      ? 'HAPM is team-specific. Its player coefficients are fitted through supported generalized-lineup rows; select a marker for exact ranks and treat unsupported teams as descriptive.'
      : comparisonId === 'lapm'
      ? 'LAPM is team-specific. The graph axis smooths constant-lineup goal impact across overlapping player combinations; select a marker for exact ranks.'
      : 'Each axis is standardized within this competition. Flags show source-listed nationality; upper-right players rate highly under both protocols.';
    var query = state.query.trim().toLocaleLowerCase();
    if (query) {
      points = points.filter(function (point) {
        return point.name.toLocaleLowerCase().indexOf(query) !== -1 ||
          point.team.toLocaleLowerCase().indexOf(query) !== -1 ||
          String(point.country || '').toLocaleLowerCase().indexOf(query) !== -1;
      });
    }
    var mobile = window.matchMedia('(max-width: 650px)').matches;
    var width = mobile ? Math.max(280, Math.floor(elements.chart.clientWidth || 330)) :
      Math.max(480, Math.min(760, Math.floor(elements.chart.clientWidth || 760)));
    var height = mobile ? 300 : 390, pad = mobile ? 34 : 45, extent = 3.2;
    function x(value) { return pad + (Math.max(-extent, Math.min(extent, value)) + extent) / (2 * extent) * (width - 2 * pad); }
    function y(value) { return height - pad - (Math.max(-extent, Math.min(extent, value)) + extent) / (2 * extent) * (height - 2 * pad); }
    points.forEach(function (point) {
      point.px = x(point.x);
      point.py = y(point.y);
    });
    var byExtremity = points.slice().sort(function (a, b) { return Math.max(Math.abs(b.x), Math.abs(b.y)) - Math.max(Math.abs(a.x), Math.abs(a.y)); });
    // Greedy label placement: take the most extreme players whose name text
    // cannot overlap an already placed label, instead of printing names on
    // top of each other when two extremes sit close together.
    var labels = [];
    if (!mobile) {
      byExtremity.some(function (point) {
        var collides = labels.some(function (kept) {
          return Math.abs(kept.px - point.px) < 150 && Math.abs(kept.py - point.py) < 18;
        });
        if (!collides) labels.push(point);
        return labels.length >= 8;
      });
    }
    var labelIds = labels.reduce(function (items, point) { items[point.id] = true; return items; }, {});
    // Overplotting control: with a large cohort, only the most extreme points
    // carry a flag; the dense middle stays as plain dots. Small filtered sets
    // (for example one searched country) keep every flag.
    var FLAG_BUDGET = 100;
    var flaggedIds = null;
    if (points.length > 120) {
      flaggedIds = byExtremity.slice(0, FLAG_BUDGET).reduce(function (items, point) { items[point.id] = true; return items; }, {});
    }
    // Roving tabindex: the chart is one tab stop; arrow keys walk the markers.
    var tabbableId = points.some(function (point) { return point.id === state.selected; })
      ? state.selected
      : points.length ? points[0].id : null;
    chartView = { width: width, height: height, comparisonShort: comparisonShort, flagged: flaggedIds, byId: {} };
    points.forEach(function (point) { chartView.byId[point.id] = point; });
    var circles = points.map(function (point) {
      var selected = point.id === state.selected ? ' is-selected' : '';
      var showFlag = !flaggedIds || flaggedIds[point.id] || point.id === state.selected;
      var flag = showFlag ? playerFlag(point.country, 'is-chart-flag', true) : '';
      var pointX = point.px, pointY = point.py;
      var selectionCard = selected ? chartSelectionCard(point) : '';
      return '<button type="button" class="player-lab-point' + (flag ? ' has-country-flag' : '') + selected + '" data-player-id="' + escapeHtml(point.id) +
        '" tabindex="' + (point.id === tabbableId ? '0' : '-1') + '" style="--point-x:' + pointX.toFixed(1) + 'px;--point-y:' + pointY.toFixed(1) + 'px" aria-label="' +
        escapeHtml(point.name + ', ' + point.country + ', ' + point.team + ', Lineup TrueSkill ' + point.x.toFixed(2) + ' standard deviations, ' + comparisonLabel + ' ' + point.y.toFixed(2) + ' standard deviations') +
        '"><span>' + flag + '</span>' + (labelIds[point.id] ? '<small class="' + (point.px > width - 140 ? 'is-label-left' : '') + '">' + playerFlag(point.country, 'is-label-flag', true) + escapeHtml(point.name) + '</small>' : '') + selectionCard + '</button>';
    }).join('');
    elements.chart.innerHTML = '<p class="player-lab-chart-key">' +
      (flaggedIds ? 'Flags mark the most extreme players; the dense middle stays as dots · ' : 'Source-listed nationality · ') +
      'search a country to isolate it · select a marker for both ranks · arrow keys walk the markers</p><div class="player-lab-chart-frame" style="--chart-width:' + width + 'px;--chart-height:' + height + 'px">' +
      '<svg viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-label="Scatter plot comparing standardized Lineup TrueSkill and ' + escapeHtml(comparisonLabel) + ' scores">' +
      '<line x1="' + x(0) + '" y1="' + pad + '" x2="' + x(0) + '" y2="' + (height - pad) + '"></line>' +
      '<line x1="' + pad + '" y1="' + y(0) + '" x2="' + (width - pad) + '" y2="' + y(0) + '"></line>' +
      '<text x="' + (width / 2) + '" y="' + (height - 8) + '">Lineup TrueSkill score →</text>' +
      '<text class="is-y-label" transform="translate(14 ' + (height / 2) + ') rotate(-90)">' + escapeHtml(comparisonShort) + ' impact →</text></svg>' + circles + '</div>';
  }

  function renderTable() {
    var cohort = currentCohort();
    var rows = currentRows();
    var pageSize = isMobile() ? 10 : 30;
    var visibleCount = state.visibleCount || pageSize;
    var displayed = rows.slice(0, visibleCount);
    var remaining = Math.max(0, rows.length - displayed.length);
    elements.caption.textContent = cohort.models[state.model].label + (isTeamModel(state.model) ? ' · ' + currentTeam(state.model).name : '') + ' · ' + rows.length + ' eligible players' +
      (cohort.source && cohort.source.name ? ' · ' + cohort.source.name : '');
    elements.listStatus.textContent = cohort.models[state.model].label + ' · showing ' + displayed.length + ' of ' + rows.length;
    elements.scoreHeading.textContent = 'Score';
    elements.empty.hidden = rows.length > 0;
    if (isTeamModel(state.model)) {
      // A team-scoped model must say so, or an empty search result reads as
      // "this player was not in the cohort" when they simply play elsewhere.
      elements.empty.innerHTML = 'No eligible player matches this search within <strong>' +
        escapeHtml(currentTeam(state.model).name) + '</strong>. ' +
        escapeHtml(cohort.models[state.model].label) +
        ' is fitted within one team — switch team above, or choose RAPM or Lineup to search the whole cohort.';
    } else {
      elements.empty.textContent = 'No eligible player matches this search.';
    }
    elements.more.hidden = rows.length <= displayed.length;
    elements.more.textContent = remaining ? 'Show next ' + Math.min(pageSize, remaining) + ' · ' + remaining + ' remaining' : '';
    elements.body.innerHTML = displayed.map(function (row) {
      return '<tr data-player-row="' + escapeHtml(row.id) + '"' + (row.id === state.selected ? ' class="is-selected"' : '') + '>' +
        '<td class="rating-lab-rank">' + row.rank + '</td><th scope="row"><button type="button" class="rating-lab-entity" data-player-id="' +
        escapeHtml(row.id) + '"><span class="player-lab-player-name"><span>' + escapeHtml(row.name) + '</span>' + playerFlag(row.country) + '</span><small>' + escapeHtml(row.team) + '</small>' +
        '<span class="player-lab-row-evidence">±' + number(row.uncertainty, 2) + ' · ' + number(row.minutes, 0) + ' min · ' + row.matches + ' matches</span></button></th>' +
        '<td class="player-lab-score"><span>' + (state.model === 'rapm' ? 'RAPM' : state.model === 'pairwise-chemistry' ? 'Chemistry' : state.model === 'hapm' ? 'HAPM' : state.model === 'lapm' ? 'LAPM' : 'Lineup') + '</span><strong>' + number(row.score, 2) + '</strong></td><td>±' + number(row.uncertainty, 2) + '</td>' +
        '<td class="rating-lab-optional">' + number(row.minutes, 0) + '</td><td class="rating-lab-optional">' + row.matches + '</td></tr>';
    }).join('');
  }

  function renderDetail() {
    if (!state.selected) {
      elements.detail.classList.remove('is-active');
      elements.detail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a player to compare the available protocols.</p>';
      return;
    }
    var cohort = currentCohort();
    var trueRow = cohort.models['lineup-trueskill'].rankings.find(function (row) { return row.id === state.selected; });
    var rapmRow = cohort.models.rapm.rankings.find(function (row) { return row.id === state.selected; });
    var chemistryModel = cohort.models['pairwise-chemistry'];
    var chemistryRow = chemistryModel.rankings.find(function (row) { return row.id === state.selected; });
    var hapmTeam = currentTeam('hapm');
    var hapmRow = hapmTeam.rankings.find(function (row) { return row.id === state.selected; });
    var lapmTeam = currentTeam('lapm');
    var lapmRow = lapmTeam.rankings.find(function (row) { return row.id === state.selected; });
    if (!trueRow || !rapmRow) return;
    var identityMeta = trueRow.country && trueRow.country !== trueRow.team
      ? trueRow.country + ' · ' + trueRow.team
      : trueRow.team || trueRow.country || 'Nationality unavailable';
    var partnershipDetails = '';
    if (chemistryRow) {
      function partnershipList(label, rows) {
        return '<div><span>' + escapeHtml(label) + '</span>' + rows.map(function (pair) {
          return '<small><b>' + escapeHtml(pair.partner_name) + '</b><br>' +
            signedNumber(pair.impact, 2) + ' residual goals · ' + number(pair.shared_minutes, 0) + ' min</small>';
        }).join('') + '</div>';
      }
      partnershipDetails = '<div class="player-lab-partnership-detail">' +
        partnershipList('Strongest observed pairs', chemistryRow.strongest_partnerships || []) +
        partnershipList('Weakest observed pairs', chemistryRow.weakest_partnerships || []) + '</div>';
    }
    elements.detail.classList.toggle('is-active', state.detailOpen);
    elements.detail.innerHTML = '<button type="button" class="player-lab-detail-close" data-player-close aria-label="Close player comparison">×</button>' +
      '<p class="rating-lab-kicker">Player comparison</p><h3 class="player-lab-detail-name"><span>' + escapeHtml(trueRow.name) + '</span>' + playerFlag(trueRow.country) + '</h3><p>' +
      escapeHtml(trueRow.full_name && trueRow.full_name !== trueRow.name ? trueRow.full_name + ' · ' : '') +
      escapeHtml(identityMeta) + ' · ' + number(trueRow.minutes, 0) + ' minutes · ' + trueRow.matches + ' matches</p>' +
      '<div class="player-lab-detail-model"><span>Lineup TrueSkill</span><strong>#' + trueRow.rank + '</strong><small>Mean ' + number(trueRow.mean, 2) + ' · uncertainty ±' + number(trueRow.uncertainty, 2) + '</small></div>' +
      '<div class="player-lab-detail-model"><span>RAPM</span><strong>#' + rapmRow.rank + '</strong><small>Goal impact ' + signedNumber(rapmRow.impact, 2) + ' · uncertainty ±' + number(rapmRow.uncertainty, 2) + '</small></div>' +
      (chemistryRow ? '<div class="player-lab-detail-model"><span>Pairwise chemistry · ' + escapeHtml(chemistryModel.status.replace(/_/g, ' ')) + '</span><strong>#' + chemistryRow.rank + '</strong><small>Residual pair impact ' + signedNumber(chemistryRow.impact, 2) + ' · ' + chemistryRow.qualifying_partnerships + ' qualifying partnerships · uncertainty ±' + number(chemistryRow.uncertainty, 2) + '</small></div>' : '') +
      (hapmRow ? '<div class="player-lab-detail-model"><span>HAPM · ' + escapeHtml(hapmTeam.name) + ' · ' + escapeHtml(hapmTeam.diagnostics.validation_status.replace(/_/g, ' ')) + '</span><strong>#' + hapmRow.rank + '</strong><small>Hypergraph-adjusted player coefficient ' + signedNumber(hapmRow.impact, 2) + ' per 90 · uncertainty ±' + number(hapmRow.uncertainty, 2) + '</small></div>' : '') +
      (lapmRow ? '<div class="player-lab-detail-model"><span>LAPM · ' + escapeHtml(lapmTeam.name) + ' · descriptive</span><strong>#' + lapmRow.rank + '</strong><small>Graph-smoothed impact ' + signedNumber(lapmRow.impact, 2) + ' per 90 · uncertainty ±' + number(lapmRow.uncertainty, 2) + '</small></div>' : '') +
      partnershipDetails +
      '<p class="rating-lab-audit-note">Ranks are cohort-specific and use conservative scores, so both estimated contribution and uncertainty matter.</p>';
  }

  function renderGates() {
    var cohort = currentCohort();
    var gates = [
      ['Starting lineups', percent(cohort.coverage.starting_lineups), 'At least 95% required'],
      ['Player minutes', percent(cohort.coverage.player_minutes), 'At least 95% required'],
      ['Event goals', percent(cohort.coverage.event_goal_scores), 'Must reproduce every final score'],
      ['Lineup integrity', percent(cohort.coverage.lineup_integrity), 'At least 95% required'],
      ['Connected graph', cohort.coverage.player_match_graph_components === 1 ? 'Passed' : 'Failed', cohort.coverage.player_match_graph_components + ' component']
    ];
    elements.gates.innerHTML = gates.map(function (gate) {
      return '<article><span>' + escapeHtml(gate[0]) + '</span><strong>' + escapeHtml(gate[1]) + '</strong><small>' + escapeHtml(gate[2]) + '</small></article>';
    }).join('');
  }

  function render() {
    elements.modelTabs.querySelectorAll('button').forEach(function (item) {
      item.setAttribute('aria-pressed', String(item.dataset.playerModel === state.model));
    });
    renderTeamOptions();
    renderMetrics();
    renderScope();
    renderOrderingNote();
    renderTeamCombinations();
    renderChart();
    renderTable();
    renderDetail();
    renderGates();
    updateQuickModel();
  }

  var quickModelFrame = null;

  function updateQuickModel() {
    if (!window.matchMedia('(max-width: 650px)').matches) {
      elements.quickModel.hidden = true;
      elements.quickModel.classList.remove('is-open');
      elements.quickModelTrigger.setAttribute('aria-expanded', 'false');
      return;
    }
    var sectionRect = document.querySelector('.player-lab-explorer').getBoundingClientRect();
    var tabsRect = elements.modelTabs.getBoundingClientRect();
    var withinExplorer = sectionRect.top <= window.innerHeight * 0.36 && sectionRect.bottom > window.innerHeight * 0.36;
    var originalControlsVisible = tabsRect.bottom > 0 && tabsRect.top < window.innerHeight;
    elements.quickModel.hidden = !withinExplorer || originalControlsVisible;
    if (elements.quickModel.hidden) {
      elements.quickModel.classList.remove('is-open');
      elements.quickModelTrigger.setAttribute('aria-expanded', 'false');
    }
    elements.quickModelLabel.textContent = {
      'lineup-trueskill': 'Lineup',
      rapm: 'RAPM',
      'pairwise-chemistry': 'Chemistry',
      hapm: 'HAPM',
      lapm: 'LAPM'
    }[state.model];
    elements.quickModelMenu.querySelectorAll('[data-player-quick-model]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.playerQuickModel === state.model));
    });
  }

  function queueQuickModelUpdate() {
    if (quickModelFrame !== null) return;
    quickModelFrame = window.requestAnimationFrame(function () {
      quickModelFrame = null;
      updateQuickModel();
    });
  }

  elements.cohort.addEventListener('change', function () {
    state.cohort = elements.cohort.value;
    state.selected = null;
    state.team = null;
    resetList();
    syncCohort();
  });
  elements.team.addEventListener('change', function () {
    state.team = elements.team.value;
    state.selected = null;
    resetList();
    render();
  });
  elements.modelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-player-model]');
    if (!button) return;
    state.model = button.dataset.playerModel;
    state.selected = null;
    elements.modelTabs.querySelectorAll('button').forEach(function (item) {
      item.setAttribute('aria-pressed', String(item === button));
    });
    resetList();
    render();
  });
  elements.quickModelMenu.addEventListener('click', function (event) {
    event.stopPropagation();
    var button = event.target.closest('[data-player-quick-model]');
    if (!button) return;
    state.model = button.dataset.playerQuickModel;
    state.selected = null;
    elements.modelTabs.querySelectorAll('button').forEach(function (item) {
      item.setAttribute('aria-pressed', String(item.dataset.playerModel === state.model));
    });
    elements.quickModel.classList.remove('is-open');
    elements.quickModelTrigger.setAttribute('aria-expanded', 'false');
    resetList();
    render();
  });
  elements.quickModelTrigger.addEventListener('click', function (event) {
    event.stopPropagation();
    var open = elements.quickModel.classList.toggle('is-open');
    elements.quickModelTrigger.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('click', function (event) {
    if (elements.quickModel.hidden || elements.quickModel.contains(event.target)) return;
    elements.quickModel.classList.remove('is-open');
    elements.quickModelTrigger.setAttribute('aria-expanded', 'false');
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    elements.quickModel.classList.remove('is-open');
    elements.quickModelTrigger.setAttribute('aria-expanded', 'false');
  });
  var searchDebounce = null;
  elements.search.addEventListener('input', function () {
    state.query = elements.search.value;
    resetList();
    // Debounce so fast typing re-renders the 300-marker chart once, not per key.
    if (searchDebounce) window.clearTimeout(searchDebounce);
    searchDebounce = window.setTimeout(function () {
      searchDebounce = null;
      renderChart();
      renderTable();
    }, 120);
  });
  elements.more.addEventListener('click', function () {
    state.visibleCount = (state.visibleCount || (isMobile() ? 10 : 30)) + (isMobile() ? 10 : 30);
    renderTable();
  });
  elements.filtersReturn.addEventListener('click', function () {
    document.querySelector('.player-lab-toolbar').scrollIntoView({
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
      block: 'start'
    });
  });
  root.addEventListener('click', function (event) {
    if (event.target.closest('[data-player-close]')) {
      state.detailOpen = false;
      renderDetail();
      return;
    }
    var target = event.target.closest('[data-player-id]');
    if (!target) return;
    var chartPoint = target.classList.contains('player-lab-point');
    state.selected = chartPoint && state.selected === target.dataset.playerId ? null : target.dataset.playerId;
    state.detailOpen = !chartPoint && Boolean(state.selected);
    updateChartSelection();
    renderTable();
    renderDetail();
  });
  elements.chart.addEventListener('keydown', function (event) {
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].indexOf(event.key) === -1) return;
    var target = event.target.closest('.player-lab-point');
    if (!target) return;
    event.preventDefault();
    var markers = [].slice.call(elements.chart.querySelectorAll('.player-lab-point'));
    var index = markers.indexOf(target);
    var next = event.key === 'ArrowRight' || event.key === 'ArrowDown' ? index + 1 : index - 1;
    if (next < 0) next = markers.length - 1;
    if (next >= markers.length) next = 0;
    target.tabIndex = -1;
    markers[next].tabIndex = 0;
    markers[next].focus();
  });
  window.addEventListener('scroll', queueQuickModelUpdate, { passive: true });
  window.addEventListener('resize', queueQuickModelUpdate);
  // Re-render the chart when the available width actually changes (window
  // resize or browser zoom), so the fixed-width chart can never overflow.
  var chartResizeDebounce = null;
  window.addEventListener('resize', function () {
    if (chartResizeDebounce) window.clearTimeout(chartResizeDebounce);
    chartResizeDebounce = window.setTimeout(function () {
      chartResizeDebounce = null;
      if (!chartView || !currentCohort()) return;
      var available = Math.max(280, Math.min(760, Math.floor(elements.chart.clientWidth || chartView.width)));
      if (Math.abs(available - chartView.width) > 4) renderChart();
    }, 180);
  });

  fetchJson(splitUrl('player-index.json'))
    .catch(loadFullPayload)
    .then(function (payload) {
      state.payload = payload;
      state.cohort = payload.cohorts[0].id;
      renderCohortOptions();
      renderSourceStatus();
      elements.generated.textContent = 'Verified ' + date(payload.generated_at) + ' · Cohort-specific sources';
      return syncCohort();
    })
    .catch(function (error) {
      elements.error.hidden = false;
      elements.error.textContent = error.message;
    });
}());
