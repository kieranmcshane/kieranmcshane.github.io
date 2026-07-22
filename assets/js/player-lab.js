(function () {
  'use strict';

  var root = document.querySelector('.player-lab');
  if (!root) return;
  var state = { payload: null, cohort: null, model: 'lineup-trueskill', query: '', visibleCount: 0, selected: null, detailOpen: false };
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
    listStatus: document.getElementById('player-list-status'),
    filtersReturn: document.getElementById('player-filters-return'),
    detail: document.getElementById('player-detail'),
    scoreHeading: document.getElementById('player-score-heading'),
    gates: document.getElementById('player-gates'),
    quickModel: document.getElementById('player-quick-model'),
    quickModelMenu: document.getElementById('player-quick-model-menu')
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
    return state.payload.cohorts.find(function (cohort) { return cohort.id === state.cohort; });
  }

  function currentRows() {
    var query = state.query.trim().toLocaleLowerCase();
    return currentCohort().models[state.model].rankings.filter(function (row) {
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
      return {
        id: row.id, name: row.name, team: row.team, country: row.country,
        x: trueZ[row.id], y: rapmZ[row.id], trueRank: byId[row.id].rank,
        rapmRank: row.rank, trueScore: byId[row.id].score, rapmScore: row.score
      };
    });
    var query = state.query.trim().toLocaleLowerCase();
    if (query) {
      points = points.filter(function (point) {
        return point.name.toLocaleLowerCase().indexOf(query) !== -1 ||
          point.team.toLocaleLowerCase().indexOf(query) !== -1 ||
          String(point.country || '').toLocaleLowerCase().indexOf(query) !== -1;
      });
    }
    var mobile = window.matchMedia('(max-width: 650px)').matches;
    var width = mobile ? Math.max(280, Math.floor(elements.chart.clientWidth || 330)) : 760;
    var height = mobile ? 300 : 390, pad = mobile ? 34 : 45, extent = 3.2;
    function x(value) { return pad + (Math.max(-extent, Math.min(extent, value)) + extent) / (2 * extent) * (width - 2 * pad); }
    function y(value) { return height - pad - (Math.max(-extent, Math.min(extent, value)) + extent) / (2 * extent) * (height - 2 * pad); }
    var labels = points.slice().sort(function (a, b) { return Math.max(Math.abs(b.x), Math.abs(b.y)) - Math.max(Math.abs(a.x), Math.abs(a.y)); }).slice(0, mobile ? 0 : 8);
    var labelIds = labels.reduce(function (items, point) { items[point.id] = true; return items; }, {});
    var circles = points.map(function (point) {
      var selected = point.id === state.selected ? ' is-selected' : '';
      var flag = playerFlag(point.country, 'is-chart-flag', true);
      var pointX = x(point.x), pointY = y(point.y);
      var cardWidth = Math.min(185, width - 16), cardHeight = 112;
      var preferredCardLeft = pointX > width / 2 ? pointX - cardWidth - 15 : pointX + 15;
      var preferredCardTop = pointY < cardHeight + 14 ? pointY + 14 : pointY - cardHeight - 14;
      var cardLeft = Math.max(8, Math.min(width - cardWidth - 8, preferredCardLeft));
      var cardTop = Math.max(8, Math.min(height - cardHeight - 8, preferredCardTop));
      var pointMeta = point.country && point.country !== point.team
        ? point.country + ' · ' + point.team
        : point.team || point.country || 'Nationality unavailable';
      var selectionCard = selected ? '<strong class="player-lab-point-card" style="--card-left:' +
        (cardLeft - pointX).toFixed(1) + 'px;--card-top:' + (cardTop - pointY).toFixed(1) + 'px;--card-width:' + cardWidth + 'px">' +
        '<span class="player-lab-point-card-name">' + playerFlag(point.country, '', true) + '<span>' + escapeHtml(point.name) + '</span></span>' +
        '<span class="player-lab-point-card-meta">' + escapeHtml(pointMeta) + '</span>' +
        '<span class="player-lab-point-card-ranks"><span>Lineup <b>#' + point.trueRank + '</b></span><span>RAPM <b>#' + point.rapmRank + '</b></span></span>' +
        '<span class="player-lab-point-card-scores">Scores ' + number(point.trueScore, 2) + ' · ' + number(point.rapmScore, 2) + '</span></strong>' : '';
      return '<button type="button" class="player-lab-point' + (flag ? ' has-country-flag' : '') + selected + '" data-player-id="' + escapeHtml(point.id) +
        '" style="--point-x:' + pointX.toFixed(1) + 'px;--point-y:' + pointY.toFixed(1) + 'px" aria-label="' +
        escapeHtml(point.name + ', ' + point.country + ', ' + point.team + ', Lineup TrueSkill ' + point.x.toFixed(2) + ' standard deviations, RAPM ' + point.y.toFixed(2) + ' standard deviations') +
        '"><span>' + flag + '</span>' + (labelIds[point.id] ? '<small>' + playerFlag(point.country, 'is-label-flag', true) + escapeHtml(point.name) + '</small>' : '') + selectionCard + '</button>';
    }).join('');
    elements.chart.innerHTML = '<p class="player-lab-chart-key">Source-listed nationality · search a country to isolate it · select a marker for both ranks</p><div class="player-lab-chart-frame" style="--chart-width:' + width + 'px;--chart-height:' + height + 'px">' +
      '<svg viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-label="Scatter plot comparing standardized Lineup TrueSkill and RAPM scores">' +
      '<line x1="' + x(0) + '" y1="' + pad + '" x2="' + x(0) + '" y2="' + (height - pad) + '"></line>' +
      '<line x1="' + pad + '" y1="' + y(0) + '" x2="' + (width - pad) + '" y2="' + y(0) + '"></line>' +
      '<text x="' + (width / 2) + '" y="' + (height - 8) + '">Lineup TrueSkill score →</text>' +
      '<text class="is-y-label" transform="translate(14 ' + (height / 2) + ') rotate(-90)">RAPM impact →</text></svg>' + circles + '</div>';
  }

  function renderTable() {
    var cohort = currentCohort();
    var rows = currentRows();
    var pageSize = isMobile() ? 10 : 30;
    var visibleCount = state.visibleCount || pageSize;
    var displayed = rows.slice(0, visibleCount);
    var remaining = Math.max(0, rows.length - displayed.length);
    elements.caption.textContent = cohort.models[state.model].label + ' · ' + rows.length + ' eligible players' +
      (cohort.source && cohort.source.name ? ' · ' + cohort.source.name : '');
    elements.listStatus.textContent = cohort.models[state.model].label + ' · showing ' + displayed.length + ' of ' + rows.length;
    elements.scoreHeading.textContent = 'Score';
    elements.empty.hidden = rows.length > 0;
    elements.more.hidden = rows.length <= displayed.length;
    elements.more.textContent = remaining ? 'Show next ' + Math.min(pageSize, remaining) + ' · ' + remaining + ' remaining' : '';
    elements.body.innerHTML = displayed.map(function (row) {
      return '<tr data-player-row="' + escapeHtml(row.id) + '"' + (row.id === state.selected ? ' class="is-selected"' : '') + '>' +
        '<td class="rating-lab-rank">' + row.rank + '</td><th scope="row"><button type="button" class="rating-lab-entity" data-player-id="' +
        escapeHtml(row.id) + '"><span class="player-lab-player-name"><span>' + escapeHtml(row.name) + '</span>' + playerFlag(row.country) + '</span><small>' + escapeHtml(row.team) + '</small>' +
        '<span class="player-lab-row-evidence">±' + number(row.uncertainty, 2) + ' · ' + number(row.minutes, 0) + ' min · ' + row.matches + ' matches</span></button></th>' +
        '<td class="player-lab-score"><span>' + (state.model === 'rapm' ? 'RAPM' : 'Lineup') + '</span><strong>' + number(row.score, 2) + '</strong></td><td>±' + number(row.uncertainty, 2) + '</td>' +
        '<td class="rating-lab-optional">' + number(row.minutes, 0) + '</td><td class="rating-lab-optional">' + row.matches + '</td></tr>';
    }).join('');
  }

  function renderDetail() {
    if (!state.selected) {
      elements.detail.classList.remove('is-active');
      elements.detail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a player to compare both protocols.</p>';
      return;
    }
    var cohort = currentCohort();
    var trueRow = cohort.models['lineup-trueskill'].rankings.find(function (row) { return row.id === state.selected; });
    var rapmRow = cohort.models.rapm.rankings.find(function (row) { return row.id === state.selected; });
    if (!trueRow || !rapmRow) return;
    var identityMeta = trueRow.country && trueRow.country !== trueRow.team
      ? trueRow.country + ' · ' + trueRow.team
      : trueRow.team || trueRow.country || 'Nationality unavailable';
    elements.detail.classList.toggle('is-active', state.detailOpen);
    elements.detail.innerHTML = '<button type="button" class="player-lab-detail-close" data-player-close aria-label="Close player comparison">×</button>' +
      '<p class="rating-lab-kicker">Player comparison</p><h3 class="player-lab-detail-name"><span>' + escapeHtml(trueRow.name) + '</span>' + playerFlag(trueRow.country) + '</h3><p>' +
      escapeHtml(identityMeta) + ' · ' + number(trueRow.minutes, 0) + ' minutes · ' + trueRow.matches + ' matches</p>' +
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
    updateQuickModel();
  }

  var quickModelFrame = null;

  function updateQuickModel() {
    if (!window.matchMedia('(max-width: 650px)').matches) {
      elements.quickModel.hidden = true;
      return;
    }
    var sectionRect = document.querySelector('.player-lab-explorer').getBoundingClientRect();
    var tabsRect = elements.modelTabs.getBoundingClientRect();
    var withinExplorer = sectionRect.top <= window.innerHeight * 0.36 && sectionRect.bottom > window.innerHeight * 0.36;
    var originalControlsVisible = tabsRect.bottom > 0 && tabsRect.top < window.innerHeight;
    elements.quickModel.hidden = !withinExplorer || originalControlsVisible;
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
    resetList();
    render();
  });
  elements.modelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-player-model]');
    if (!button) return;
    state.model = button.dataset.playerModel;
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
    elements.modelTabs.querySelectorAll('button').forEach(function (item) {
      item.setAttribute('aria-pressed', String(item.dataset.playerModel === state.model));
    });
    resetList();
    render();
  });
  elements.search.addEventListener('input', function () {
    state.query = elements.search.value;
    resetList();
    renderChart();
    renderTable();
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
    renderChart();
    renderTable();
    renderDetail();
  });
  window.addEventListener('scroll', queueQuickModelUpdate, { passive: true });
  window.addEventListener('resize', queueQuickModelUpdate);

  fetch(root.dataset.playerData)
    .then(function (response) {
      if (!response.ok) throw new Error('The historical player ratings could not be loaded.');
      return response.json();
    })
    .then(function (payload) {
      state.payload = payload;
      state.cohort = payload.cohorts[0].id;
      if (isMobile()) {
        document.getElementById('player-scope').open = false;
        document.getElementById('player-methods').open = false;
      }
      renderCohortOptions();
      elements.generated.textContent = 'Verified ' + date(payload.generated_at) + ' · Data source: StatsBomb';
      render();
    })
    .catch(function (error) {
      elements.error.hidden = false;
      elements.error.textContent = error.message;
    });
}());
