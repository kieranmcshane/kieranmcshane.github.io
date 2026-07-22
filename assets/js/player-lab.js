(function () {
  'use strict';

  var root = document.querySelector('.player-lab');
  if (!root) return;
  var state = { payload: null, cohort: null, model: 'lineup-trueskill', query: '', expanded: false, selected: null };
  var elements = {
    error: document.getElementById('player-lab-error'),
    generated: document.getElementById('player-lab-generated'),
    cohort: document.getElementById('player-cohort'),
    modelTabs: document.getElementById('player-model-tabs'),
    search: document.getElementById('player-search'),
    metrics: document.getElementById('player-metrics'),
    chart: document.getElementById('player-comparison-chart'),
    body: document.getElementById('player-ranking-body'),
    caption: document.getElementById('player-ranking-caption'),
    empty: document.getElementById('player-ranking-empty'),
    more: document.getElementById('player-ranking-more'),
    detail: document.getElementById('player-detail'),
    scoreHeading: document.getElementById('player-score-heading'),
    gates: document.getElementById('player-gates')
  };

  function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character];
    });
  }

  function number(value, digits) {
    return new Intl.NumberFormat('en', { maximumFractionDigits: digits }).format(value);
  }

  function percent(value) {
    return new Intl.NumberFormat('en', { style: 'percent', maximumFractionDigits: 1 }).format(value);
  }

  function date(value) {
    return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(value));
  }

  function currentCohort() {
    return state.payload.cohorts.find(function (cohort) { return cohort.id === state.cohort; });
  }

  function currentRows() {
    var query = state.query.trim().toLocaleLowerCase();
    return currentCohort().models[state.model].rankings.filter(function (row) {
      return !query || row.name.toLocaleLowerCase().indexOf(query) !== -1 || row.team.toLocaleLowerCase().indexOf(query) !== -1;
    });
  }

  function renderCohortOptions() {
    var groups = [
      { id: 'men', label: "Men's competitions" },
      { id: 'women', label: "Women's competitions" }
    ];
    var known = {};
    var html = groups.map(function (group) {
      var cohorts = state.payload.cohorts.filter(function (cohort) { return cohort.gender === group.id; });
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

  function renderMetrics() {
    var cohort = currentCohort();
    var model = cohort.models[state.model];
    var modelMetric = state.model === 'lineup-trueskill'
      ? ['Held-out log loss', number(model.metrics.log_loss, 3), model.metrics.chronological_predictions + ' predictions recorded before updating']
      : ['Validation RMSE', number(model.metrics.validation_rmse, 3), model.metrics.chronological_validation_matches + ' chronological validation matches'];
    var metrics = [
      ['Matches', number(cohort.matches, 0), (cohort.format || 'historical cohort') + ' · ' + cohort.first_match + ' to ' + cohort.last_match],
      ['Eligible players', number(cohort.eligible_players, 0), 'Minimum 450 minutes and five appearances'],
      [modelMetric[0], modelMetric[1], modelMetric[2]],
      ['Lineup coverage', percent(cohort.coverage.starting_lineups), 'Player-match graph: ' + cohort.coverage.player_match_graph_components + ' connected component']
    ];
    elements.metrics.innerHTML = metrics.map(function (metric) {
      return '<div class="rating-lab-metric"><span>' + escapeHtml(metric[0]) + '</span><div class="rating-lab-metric-value"><strong>' +
        escapeHtml(metric[1]) + '</strong></div><small>' + escapeHtml(metric[2]) + '</small></div>';
    }).join('');
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
    var rapmRows = cohort.models.rapm.rankings;
    var trueZ = standardized(trueRows), rapmZ = standardized(rapmRows);
    var byId = {};
    trueRows.forEach(function (row) { byId[row.id] = row; });
    var points = rapmRows.filter(function (row) { return trueZ[row.id] !== undefined; }).map(function (row) {
      return { id: row.id, name: row.name, team: row.team, x: trueZ[row.id], y: rapmZ[row.id] };
    });
    var mobile = window.matchMedia('(max-width: 650px)').matches;
    var width = mobile ? Math.max(280, Math.floor(elements.chart.clientWidth || 330)) : 760;
    var height = mobile ? 300 : 390, pad = mobile ? 34 : 45, extent = 3.2;
    function x(value) { return pad + (Math.max(-extent, Math.min(extent, value)) + extent) / (2 * extent) * (width - 2 * pad); }
    function y(value) { return height - pad - (Math.max(-extent, Math.min(extent, value)) + extent) / (2 * extent) * (height - 2 * pad); }
    var labels = points.slice().sort(function (a, b) { return Math.max(Math.abs(b.x), Math.abs(b.y)) - Math.max(Math.abs(a.x), Math.abs(a.y)); }).slice(0, mobile ? 4 : 8);
    var labelIds = labels.reduce(function (items, point) { items[point.id] = true; return items; }, {});
    var circles = points.map(function (point) {
      var selected = point.id === state.selected ? ' is-selected' : '';
      return '<button type="button" class="player-lab-point' + selected + '" data-player-id="' + escapeHtml(point.id) +
        '" style="--point-x:' + x(point.x).toFixed(1) + 'px;--point-y:' + y(point.y).toFixed(1) + 'px" aria-label="' +
        escapeHtml(point.name + ', ' + point.team + ', Lineup TrueSkill ' + point.x.toFixed(2) + ' standard deviations, RAPM ' + point.y.toFixed(2) + ' standard deviations') +
        '"><span></span>' + (labelIds[point.id] ? '<small>' + escapeHtml(point.name) + '</small>' : '') + '</button>';
    }).join('');
    elements.chart.innerHTML = '<div class="player-lab-chart-frame" style="--chart-width:' + width + 'px;--chart-height:' + height + 'px">' +
      '<svg viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-label="Scatter plot comparing standardized Lineup TrueSkill and RAPM scores">' +
      '<line x1="' + x(0) + '" y1="' + pad + '" x2="' + x(0) + '" y2="' + (height - pad) + '"></line>' +
      '<line x1="' + pad + '" y1="' + y(0) + '" x2="' + (width - pad) + '" y2="' + y(0) + '"></line>' +
      '<text x="' + (width / 2) + '" y="' + (height - 8) + '">Lineup TrueSkill score →</text>' +
      '<text class="is-y-label" transform="translate(14 ' + (height / 2) + ') rotate(-90)">RAPM impact →</text></svg>' + circles + '</div>';
  }

  function renderTable() {
    var cohort = currentCohort();
    var rows = currentRows();
    var displayed = state.expanded ? rows : rows.slice(0, 30);
    elements.caption.textContent = cohort.models[state.model].label + ' · ' + rows.length + ' eligible players' +
      (cohort.source && cohort.source.name ? ' · ' + cohort.source.name : '');
    elements.scoreHeading.textContent = 'Score';
    elements.empty.hidden = rows.length > 0;
    elements.more.hidden = rows.length <= displayed.length;
    elements.more.textContent = 'Show all ' + rows.length + ' players';
    elements.body.innerHTML = displayed.map(function (row) {
      return '<tr data-player-row="' + escapeHtml(row.id) + '"' + (row.id === state.selected ? ' class="is-selected"' : '') + '>' +
        '<td class="rating-lab-rank">' + row.rank + '</td><th scope="row"><button type="button" class="rating-lab-entity" data-player-id="' +
        escapeHtml(row.id) + '"><span>' + escapeHtml(row.name) + '</span><small>' + escapeHtml(row.team) + ' · ±' +
        number(row.uncertainty, 2) + ' · ' + number(row.minutes, 0) + ' min · ' + row.matches + ' matches</small></button></th>' +
        '<td><strong>' + number(row.score, 2) + '</strong></td><td>±' + number(row.uncertainty, 2) + '</td>' +
        '<td class="rating-lab-optional">' + number(row.minutes, 0) + '</td><td class="rating-lab-optional">' + row.matches + '</td></tr>';
    }).join('');
  }

  function renderDetail() {
    if (!state.selected) {
      elements.detail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a player to compare both protocols.</p>';
      return;
    }
    var cohort = currentCohort();
    var trueRow = cohort.models['lineup-trueskill'].rankings.find(function (row) { return row.id === state.selected; });
    var rapmRow = cohort.models.rapm.rankings.find(function (row) { return row.id === state.selected; });
    if (!trueRow || !rapmRow) return;
    elements.detail.innerHTML = '<p class="rating-lab-kicker">Player comparison</p><h3>' + escapeHtml(trueRow.name) + '</h3><p>' +
      escapeHtml(trueRow.team) + ' · ' + number(trueRow.minutes, 0) + ' minutes · ' + trueRow.matches + ' matches</p>' +
      '<div class="player-lab-detail-model"><span>Lineup TrueSkill</span><strong>#' + trueRow.rank + '</strong><small>Mean ' + number(trueRow.mean, 2) + ' · uncertainty ±' + number(trueRow.uncertainty, 2) + '</small></div>' +
      '<div class="player-lab-detail-model"><span>RAPM</span><strong>#' + rapmRow.rank + '</strong><small>Goal impact ' + (rapmRow.impact > 0 ? '+' : '') + number(rapmRow.impact, 2) + ' · uncertainty ±' + number(rapmRow.uncertainty, 2) + '</small></div>' +
      '<p class="rating-lab-audit-note">Ranks are season-specific and use conservative scores, so both estimated contribution and uncertainty matter.</p>';
  }

  function renderGates() {
    var cohort = currentCohort();
    var gates = [
      ['Starting lineups', percent(cohort.coverage.starting_lineups), 'At least 95% required'],
      ['Player minutes', percent(cohort.coverage.player_minutes), 'At least 95% required'],
      ['Lineup integrity', percent(cohort.coverage.lineup_integrity), 'At least 95% required'],
      ['Connected graph', cohort.coverage.player_match_graph_components === 1 ? 'Passed' : 'Failed', cohort.coverage.player_match_graph_components + ' component']
    ];
    elements.gates.innerHTML = gates.map(function (gate) {
      return '<article><span>' + escapeHtml(gate[0]) + '</span><strong>' + escapeHtml(gate[1]) + '</strong><small>' + escapeHtml(gate[2]) + '</small></article>';
    }).join('');
  }

  function render() {
    renderMetrics();
    renderChart();
    renderTable();
    renderDetail();
    renderGates();
  }

  function revealDetailOnMobile() {
    if (!window.matchMedia('(max-width: 650px)').matches) return;
    window.setTimeout(function () {
      elements.detail.scrollIntoView({
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
        block: 'start'
      });
    }, 0);
  }

  elements.cohort.addEventListener('change', function () {
    state.cohort = elements.cohort.value;
    state.selected = null;
    state.expanded = false;
    render();
  });
  elements.modelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-player-model]');
    if (!button) return;
    state.model = button.dataset.playerModel;
    elements.modelTabs.querySelectorAll('button').forEach(function (item) {
      item.setAttribute('aria-pressed', String(item === button));
    });
    state.expanded = false;
    render();
  });
  elements.search.addEventListener('input', function () {
    state.query = elements.search.value;
    state.expanded = false;
    renderTable();
  });
  elements.more.addEventListener('click', function () { state.expanded = true; renderTable(); });
  root.addEventListener('click', function (event) {
    var target = event.target.closest('[data-player-id]');
    if (!target) return;
    state.selected = target.dataset.playerId;
    renderChart();
    renderTable();
    renderDetail();
    revealDetailOnMobile();
  });

  fetch(root.dataset.playerData)
    .then(function (response) {
      if (!response.ok) throw new Error('The historical player ratings could not be loaded.');
      return response.json();
    })
    .then(function (payload) {
      state.payload = payload;
      state.cohort = payload.cohorts[0].id;
      renderCohortOptions();
      elements.generated.textContent = 'Verified ' + date(payload.generated_at) + ' · Data source: StatsBomb';
      render();
    })
    .catch(function (error) {
      elements.error.hidden = false;
      elements.error.textContent = error.message;
    });
}());
