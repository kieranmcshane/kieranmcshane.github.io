(function () {
  'use strict';

  var root = document.querySelector('.rating-lab');
  if (!root) return;
  var sports = ['tennis', 'football', 'national-football', 'chess'];
  var modelKeys = ['elo', 'glicko2', 'trueskill', 'robust'];
  var ghNodes = [
    -5.387480890011233, -4.603682449550744, -3.944764040115625, -3.347854567383216,
    -2.788806058428130, -2.254974002089276, -1.738537712116586, -1.234076215395323,
    -0.737473728545394, -0.245340708300901, 0.245340708300901, 0.737473728545394,
    1.234076215395323, 1.738537712116586, 2.254974002089276, 2.788806058428130,
    3.347854567383216, 3.944764040115625, 4.603682449550744, 5.387480890011233
  ];
  var ghWeights = [
    2.229393645534151e-13, 4.399340992273181e-10, 1.086069370769281e-7,
    7.802556478532064e-6, 2.283386360163540e-4, 0.003243773342238,
    0.024810520887464, 0.109017206020023, 0.286675505362834, 0.462243669600610,
    0.462243669600610, 0.286675505362834, 0.109017206020023, 0.024810520887464,
    0.003243773342238, 2.283386360163540e-4, 7.802556478532064e-6,
    1.086069370769281e-7, 4.399340992273181e-10, 2.229393645534151e-13
  ];

  var state = {
    sport: 'tennis',
    model: 'elo',
    competition: '',
    query: '',
    sort: 'rank',
    direction: 1,
    selected: null,
    pinned: [],
    expanded: false,
    matchupA: null,
    matchupB: null,
    matchupVenue: 'neutral',
    predictorCompetition: null,
    predictorModel: 'elo',
    predictorTeam: null,
    manifest: null,
    datasets: {}
  };

  var elements = {
    freshness: document.getElementById('rating-lab-freshness'),
    generation: document.getElementById('rating-lab-generation'),
    error: document.getElementById('rating-lab-error'),
    sportTabs: document.getElementById('sport-tabs'),
    modelTabs: document.getElementById('model-tabs'),
    protocolSportTabs: document.getElementById('protocol-sport-tabs'),
    protocolModelTabs: document.getElementById('protocol-model-tabs'),
    protocol: document.getElementById('rating-protocol'),
    competition: document.getElementById('competition-filter'),
    search: document.getElementById('rating-search'),
    metrics: document.getElementById('rating-metrics'),
    movers: document.getElementById('rating-movers'),
    context: document.getElementById('leaderboard-context'),
    body: document.getElementById('ranking-body'),
    empty: document.getElementById('ranking-empty'),
    more: document.getElementById('ranking-more'),
    caption: document.getElementById('ranking-caption'),
    detail: document.getElementById('rating-detail'),
    eligibility: document.getElementById('rating-eligibility'),
    parameterBody: document.getElementById('rating-parameter-body'),
    auditRecord: document.getElementById('rating-audit-record'),
    dataDownload: document.getElementById('rating-data-download'),
    matchupA: document.getElementById('matchup-a'),
    matchupB: document.getElementById('matchup-b'),
    matchupSwap: document.getElementById('matchup-swap'),
    matchupVenue: document.getElementById('matchup-venue'),
    matchupVenueLabel: document.getElementById('matchup-venue-label'),
    matchupModelTabs: document.getElementById('matchup-model-tabs'),
    matchupResult: document.getElementById('matchup-result'),
    predictorCompetition: document.getElementById('predictor-competition'),
    predictorModelTabs: document.getElementById('predictor-model-tabs'),
    predictorState: document.getElementById('predictor-state'),
    predictorMetrics: document.getElementById('predictor-metrics'),
    predictorMarket: document.getElementById('predictor-market'),
    predictorPerformanceChart: document.getElementById('predictor-performance-chart'),
    predictorCaption: document.getElementById('predictor-caption'),
    predictorBody: document.getElementById('predictor-body'),
    predictorDetail: document.getElementById('predictor-detail'),
    predictorMethod: document.getElementById('predictor-method-copy'),
    predictorColumns: {
      rank: document.getElementById('predictor-col-rank'),
      team: document.getElementById('predictor-col-team'),
      now: document.getElementById('predictor-col-now'),
      value: document.getElementById('predictor-col-value'),
      title: document.getElementById('predictor-col-title'),
      secondary: document.getElementById('predictor-col-secondary'),
      tertiary: document.getElementById('predictor-col-tertiary')
    }
  };

  function dataUrl(file) {
    return root.dataset.dataRoot.replace(/\/$/, '') + '/' + file;
  }

  function formatDate(value) {
    if (!value) return 'Unknown';
    return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' })
      .format(new Date(value + (value.length === 10 ? 'T12:00:00Z' : '')));
  }

  function number(value, digits) {
    if (value === null || value === undefined) return '—';
    return new Intl.NumberFormat('en', { maximumFractionDigits: digits }).format(value);
  }

  function percent(value) {
    if (value === null || value === undefined) return '—';
    return new Intl.NumberFormat('en', {
      style: 'percent',
      maximumFractionDigits: value < 0.1 ? 1 : 0
    }).format(value);
  }

  function competitionTitle(competition) {
    var season = String(competition.season || '');
    return season && competition.label.indexOf(season) === -1 ? competition.label + ' ' + season : competition.label;
  }

  function isStale(status) {
    if (!status || !status.checked_at || !status.stale_after_hours) return false;
    return Date.now() - new Date(status.checked_at).getTime() > status.stale_after_hours * 3600000;
  }

  function updateFreshness() {
    var statuses = state.manifest.sports;
    var labels = { tennis: 'Tennis', football: 'Clubs', 'national-football': 'Nations', chess: 'Chess' };
    var stale = sports.filter(function (sport) {
      return statuses[sport].status !== 'current' || isStale(statuses[sport]);
    });
    elements.freshness.classList.toggle('is-stale', stale.length > 0);
    elements.freshness.innerHTML = sports.map(function (sport) {
      var delayed = statuses[sport].status !== 'current' || isStale(statuses[sport]);
      return '<span class="rating-lab-freshness-chip' + (delayed ? ' is-stale' : '') + '"><i aria-hidden="true"></i>' +
        escapeHtml(labels[sport]) + ' · ' + escapeHtml(formatDate(statuses[sport].latest_result)) + '</span>';
    }).join('');
    var total = sports.reduce(function (sum, sport) {
      return sum + state.datasets[sport].models.elo.rankings.length;
    }, 0);
    elements.generation.textContent = number(total, 0) + ' published rankings · generated ' +
      formatDate(state.manifest.generated_at) + (stale.length ? ' · delayed sources retain their last valid snapshot' : '');
  }

  function setPressed(container, key, value) {
    container.querySelectorAll('button').forEach(function (button) {
      button.setAttribute('aria-pressed', button.dataset[key] === value ? 'true' : 'false');
    });
  }

  function populateCompetitions() {
    var data = state.datasets[state.sport];
    var options = ['<option value="">All competitions</option>'];
    data.competitions.forEach(function (competition) {
      options.push('<option value="' + escapeHtml(competition) + '">' + escapeHtml(competition) + '</option>');
    });
    elements.competition.innerHTML = options.join('');
    state.competition = '';
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character];
    });
  }

  function currentRows() {
    var rows = state.datasets[state.sport].models[state.model].rankings.slice();
    var query = state.query.trim().toLocaleLowerCase();
    rows = rows.filter(function (row) {
      return (!state.competition || row.competition === state.competition) &&
        (!query || row.name.toLocaleLowerCase().indexOf(query) !== -1 || row.country.toLocaleLowerCase().indexOf(query) !== -1);
    });
    rows.sort(function (a, b) {
      var left = a[state.sort];
      var right = b[state.sort];
      if (left === null || left === undefined) return 1;
      if (right === null || right === undefined) return -1;
      if (typeof left === 'string') return left.localeCompare(right) * state.direction;
      return (left - right) * state.direction;
    });
    return rows;
  }

  function renderMetrics() {
    var models = state.datasets[state.sport].models;
    var selected = models[state.model].metrics;
    var definitions = [
      ['Brier score', 'brier', 4],
      ['Log loss', 'log_loss', 4],
      ['Calibration gap', 'calibration', 4]
    ];
    elements.metrics.innerHTML = definitions.map(function (definition) {
      var values = modelKeys.map(function (key) { return models[key].metrics[definition[1]]; });
      var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
      var bars = modelKeys.map(function (key, index) {
        var relative = max === min ? 100 : 26 + (values[index] - min) / (max - min) * 74;
        return '<span class="rating-lab-metric-bar' + (key === state.model ? ' is-active' : '') +
          '" style="--metric-height:' + relative.toFixed(1) + '%" title="' + escapeHtml(models[key].label) +
          ': ' + number(values[index], definition[2]) + '"></span>';
      }).join('');
      return '<div class="rating-lab-metric"><span>' + definition[0] + '</span><div class="rating-lab-metric-value"><strong>' +
        number(selected[definition[1]], definition[2]) + '</strong><span class="rating-lab-metric-bars" aria-label="' +
        escapeHtml(definition[0]) + ' comparison: ' + escapeHtml(modelKeys.map(function (key, index) {
          return models[key].label + ' ' + number(values[index], definition[2]);
        }).join(', ')) + '">' + bars +
        '</span></div><small>Lower is better · all four protocols</small></div>';
    }).concat(['<div class="rating-lab-metric"><span>Held-out predictions</span><div class="rating-lab-metric-value"><strong>' +
      number(selected.predictions, 0) + '</strong></div><small>Scored before each result updates the model</small></div>']).join('');
    elements.context.textContent = models[state.model].label + ' · ' +
      (state.competition || 'all competitions') + ' · ' + currentRows().length + ' published competitors';
  }

  function renderMovers() {
    var rows = currentRows().filter(function (row) { return Number.isFinite(row.change30); });
    var risers = rows.slice().sort(function (a, b) { return b.change30 - a.change30; }).slice(0, 3);
    var fallers = rows.slice().sort(function (a, b) { return a.change30 - b.change30; }).slice(0, 3);
    function group(label, items, positive) {
      return '<div><p>' + label + '</p><div>' + items.map(function (row) {
        var value = (positive && row.change30 > 0 ? '+' : '') + number(row.change30, 1);
        return '<button type="button" data-select="' + escapeHtml(row.id) + '"><span>' + escapeHtml(row.name) +
          '</span><strong class="' + (positive ? 'is-positive' : 'is-negative') + '">' + value + '</strong></button>';
      }).join('') + '</div></div>';
    }
    elements.movers.innerHTML = group('▲ Biggest risers · 30 days', risers, true) +
      group('▼ Biggest fallers · 30 days', fallers, false);
  }

  function miniSparkline(points, label) {
    if (!points || points.length < 2) return '<span class="rating-lab-mini-empty">—</span>';
    var recent = points.slice(-14), width = 94, height = 28, pad = 2;
    var values = recent.map(function (point) { return point[1]; });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    if (max === min) max += 1;
    var coordinates = recent.map(function (point, index) {
      return (pad + index / (recent.length - 1) * (width - 2 * pad)).toFixed(1) + ',' +
        (height - pad - (point[1] - min) / (max - min) * (height - 2 * pad)).toFixed(1);
    }).join(' ');
    return '<svg class="rating-lab-mini-chart" viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-label="' +
      escapeHtml(label) + ' recent range ' + number(min, 1) + ' to ' + number(max, 1) + '"><polyline points="' +
      coordinates + '"></polyline><title>Last ' + recent.length + ' updates · ' + number(min, 1) + ' to ' + number(max, 1) + '</title></svg>';
  }

  function renderTable() {
    var rows = currentRows();
    var displayed = state.expanded ? rows : rows.slice(0, 20);
    var model = state.datasets[state.sport].models[state.model];
    elements.caption.textContent = model.label + ' · ' + rows.length + ' published competitors';
    elements.empty.hidden = rows.length > 0;
    elements.more.hidden = rows.length <= displayed.length;
    elements.more.textContent = 'Show all ' + number(rows.length, 0) + ' competitors';
    elements.body.innerHTML = displayed.map(function (row) {
      var deltaClass = row.change30 > 0 ? 'is-positive' : row.change30 < 0 ? 'is-negative' : '';
      var delta = row.change30 > 0 ? '+' + number(row.change30, 1) : number(row.change30, 1);
      return '<tr data-id="' + escapeHtml(row.id) + '" data-row-select="' + escapeHtml(row.id) + '" aria-selected="' +
        (row.id === state.selected ? 'true' : 'false') + '"' + (row.id === state.selected ? ' class="is-selected"' : '') + '>' +
        '<td class="rating-lab-rank">' + row.rank + '</td>' +
        '<th scope="row"><button type="button" class="rating-lab-entity" data-select="' + escapeHtml(row.id) + '"><span>' + escapeHtml(row.name) + '</span><small>' + escapeHtml(row.competition || row.country) + '</small></button></th>' +
        '<td class="rating-lab-trend-column">' + miniSparkline(row.history, row.name) + '</td>' +
        '<td><strong>' + number(row.score, 1) + '</strong></td>' +
        '<td class="rating-lab-optional">' + (row.sigma === null ? '—' : '±' + number(row.sigma, 1)) + '</td>' +
        '<td class="' + deltaClass + '">' + delta + '</td>' +
        '<td class="rating-lab-optional">' + number(row.recent_matches, 0) + '</td>' +
        '</tr>';
    }).join('');
  }

  function historyChart(series, label) {
    var usable = series.filter(function (item) { return item.points && item.points.length > 1; });
    if (!usable.length) return '<p class="rating-lab-detail-placeholder">Not enough history to chart yet.</p>';
    var width = 380, height = 178, left = 43, right = 8, top = 10, bottom = 28;
    var all = usable.reduce(function (items, item) { return items.concat(item.points); }, []);
    var values = all.map(function (point) { return point[1]; });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    var range = max - min || 1;
    min -= range * 0.06;
    max += range * 0.06;
    var firstDate = Math.min.apply(null, all.map(function (point) { return new Date(point[0]).getTime(); }));
    var lastDate = Math.max.apply(null, all.map(function (point) { return new Date(point[0]).getTime(); }));
    if (lastDate === firstDate) lastDate += 86400000;
    function x(date) { return left + (new Date(date).getTime() - firstDate) / (lastDate - firstDate) * (width - left - right); }
    function y(value) { return top + (max - value) / (max - min) * (height - top - bottom); }
    var grid = [0, 1, 2, 3].map(function (index) {
      var value = min + (max - min) * index / 3;
      var yPos = y(value);
      return '<line class="rating-lab-gridline" x1="' + left + '" y1="' + yPos.toFixed(1) + '" x2="' +
        (width - right) + '" y2="' + yPos.toFixed(1) + '"></line><text x="' + (left - 6) + '" y="' +
        (yPos + 3).toFixed(1) + '" text-anchor="end">' + number(value, 0) + '</text>';
    }).join('');
    var paths = usable.map(function (item, seriesIndex) {
      var coordinates = item.points.map(function (point) { return x(point[0]).toFixed(1) + ',' + y(point[1]).toFixed(1); });
      var area = 'M' + coordinates.join(' L') + ' L' + coordinates[coordinates.length - 1].split(',')[0] +
        ',' + (height - bottom) + ' L' + coordinates[0].split(',')[0] + ',' + (height - bottom) + ' Z';
      var points = item.points.map(function (point) {
        return '<circle class="rating-lab-chart-hit" cx="' + x(point[0]).toFixed(1) + '" cy="' + y(point[1]).toFixed(1) +
          '" r="3" data-chart-point data-series-index="' + seriesIndex + '" data-series="' + escapeHtml(item.name) + '" data-date="' + escapeHtml(point[0]) +
          '" data-value="' + point[1] + '"><title>' + escapeHtml(item.name) + ' · ' + escapeHtml(formatDate(point[0])) +
          ' · ' + number(point[1], 1) + '</title></circle>';
      }).join('');
      var last = item.points[item.points.length - 1];
      return (usable.length === 1 ? '<path class="rating-lab-chart-area" d="' + area + '"></path>' : '') +
        '<polyline class="rating-lab-series-' + (seriesIndex + 1) + '" points="' + coordinates.join(' ') +
        '"></polyline>' + points + '<circle class="rating-lab-chart-endpoint rating-lab-series-' + (seriesIndex + 1) +
        '" cx="' + x(last[0]).toFixed(1) + '" cy="' + y(last[1]).toFixed(1) + '" r="3.5"></circle>';
    }).join('');
    var middleDate = new Date((firstDate + lastDate) / 2).toISOString().slice(0, 10);
    var dateLabels = [new Date(firstDate).toISOString().slice(0, 10), middleDate, new Date(lastDate).toISOString().slice(0, 10)];
    var axis = dateLabels.map(function (date, index) {
      return '<text x="' + (left + index * (width - left - right) / 2).toFixed(1) + '" y="' + (height - 6) +
        '" text-anchor="' + (index === 0 ? 'start' : index === 2 ? 'end' : 'middle') + '">' +
        escapeHtml(new Intl.DateTimeFormat('en', { month: 'short', year: '2-digit' }).format(new Date(date + 'T12:00:00Z'))) + '</text>';
    }).join('');
    var legend = usable.length > 1 ? '<div class="rating-lab-chart-legend">' + usable.map(function (item, index) {
      return '<span><i class="rating-lab-series-' + (index + 1) + '"></i>' + escapeHtml(item.name) + '</span>';
    }).join('') + '</div>' : '';
    return '<div class="rating-lab-chart-wrap"><div class="rating-lab-chart-stage"><svg class="rating-lab-chart" viewBox="0 0 ' + width + ' ' + height +
      '" role="img" aria-label="' + escapeHtml(label) + ' with labelled date and rating axes">' + grid + paths + axis +
      '<line class="rating-lab-crosshair" x1="0" y1="' + top + '" x2="0" y2="' + (height - bottom) + '"></line>' +
      '<rect class="rating-lab-chart-surface" x="' + left + '" y="' + top + '" width="' + (width - left - right) +
      '" height="' + (height - top - bottom) + '" tabindex="0" data-chart-surface aria-label="Inspect ' +
      escapeHtml(label) + '. Move across the chart, tap, or use the left and right arrow keys."></rect></svg>' +
      '<div class="rating-lab-chart-tooltip" role="presentation" hidden></div></div>' +
      '<p class="rating-lab-chart-readout" aria-live="polite">Move across the chart, tap, or use ← → to inspect each update.</p>' + legend + '</div>';
  }

  function chartEntries(chartWrap) {
    return Array.prototype.map.call(chartWrap.querySelectorAll('[data-chart-point]'), function (point) {
      return {
        element: point,
        x: Number(point.getAttribute('cx')),
        y: Number(point.getAttribute('cy')),
        date: point.dataset.date,
        series: point.dataset.series,
        seriesIndex: Number(point.dataset.seriesIndex),
        value: Number(point.dataset.value)
      };
    });
  }

  function selectChartX(chartWrap, requestedX, explicitDate) {
    var entries = chartEntries(chartWrap);
    if (!entries.length) return;
    var minimumX = Math.min.apply(null, entries.map(function (entry) { return entry.x; }));
    var maximumX = Math.max.apply(null, entries.map(function (entry) { return entry.x; }));
    var x = Math.max(minimumX, Math.min(maximumX, requestedX));
    var series = entries.reduce(function (groups, entry) {
      if (!groups[entry.seriesIndex]) groups[entry.seriesIndex] = [];
      groups[entry.seriesIndex].push(entry);
      return groups;
    }, {});
    var selected = Object.keys(series).map(function (key) {
      return series[key].reduce(function (best, entry) {
        return !best || Math.abs(entry.x - x) < Math.abs(best.x - x) ? entry : best;
      }, null);
    });
    entries.forEach(function (entry) {
      var active = selected.some(function (candidate) { return candidate.element === entry.element; });
      entry.element.classList.toggle('is-active', active);
      entry.element.setAttribute('r', active ? '5' : '3');
    });
    var crosshairX = selected.length > 1 ? x : selected[0].x;
    var crosshair = chartWrap.querySelector('.rating-lab-crosshair');
    crosshair.setAttribute('x1', crosshairX);
    crosshair.setAttribute('x2', crosshairX);
    crosshair.classList.add('is-visible');
    var minimumTime = Math.min.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var maximumTime = Math.max.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var date = explicitDate || new Date(minimumTime + (x - minimumX) / (maximumX - minimumX || 1) *
      (maximumTime - minimumTime)).toISOString().slice(0, 10);
    var detail = formatDate(date) + ' · ' + selected.map(function (entry) {
      return entry.series + ' ' + number(entry.value, 1);
    }).join(' · ');
    chartWrap.querySelector('.rating-lab-chart-readout').textContent = detail;
    var surface = chartWrap.querySelector('[data-chart-surface]');
    surface.dataset.activeDate = date;
    surface.setAttribute('aria-valuetext', detail);
    var tooltip = chartWrap.querySelector('.rating-lab-chart-tooltip');
    tooltip.textContent = detail;
    tooltip.hidden = false;
    tooltip.style.setProperty('--chart-x', (crosshairX / 380 * 100).toFixed(2) + '%');
  }

  function selectChartDate(chartWrap, date) {
    var entries = chartEntries(chartWrap);
    if (!entries.length) return;
    var minimumX = Math.min.apply(null, entries.map(function (entry) { return entry.x; }));
    var maximumX = Math.max.apply(null, entries.map(function (entry) { return entry.x; }));
    var minimumTime = Math.min.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var maximumTime = Math.max.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var time = new Date(date).getTime();
    selectChartX(chartWrap, minimumX + (time - minimumTime) / (maximumTime - minimumTime || 1) * (maximumX - minimumX), date);
  }

  function scrubChart(event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface) return;
    var chartWrap = surface.closest('.rating-lab-chart-wrap');
    var svg = surface.closest('svg');
    var bounds = svg.getBoundingClientRect();
    var viewBox = svg.viewBox.baseVal;
    var pointerX = viewBox.x + (event.clientX - bounds.left) / bounds.width * viewBox.width;
    selectChartX(chartWrap, pointerX);
  }

  function distribution(row, rows) {
    var values = rows.map(function (item) { return item.score; });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values), bins = 12;
    var width = (max - min || 1) / bins;
    var counts = Array(bins).fill(0);
    values.forEach(function (value) { counts[Math.min(bins - 1, Math.floor((value - min) / width))] += 1; });
    var tallest = Math.max.apply(null, counts) || 1;
    var selectedBin = Math.min(bins - 1, Math.floor((row.score - min) / width));
    var bars = counts.map(function (count, index) {
      var start = min + index * width, end = start + width;
      return '<button type="button" class="rating-lab-histogram-bar' + (index === selectedBin ? ' is-selected' : '') +
        '" style="--histogram-height:' + Math.max(4, count / tallest * 100).toFixed(1) + '%" data-histogram="' +
        number(start, 0) + '–' + number(end, 0) + ' · ' + count + ' competitors" aria-label="Ratings ' +
        number(start, 0) + ' to ' + number(end, 0) + ': ' + count + ' competitors"></button>';
    }).join('');
    return '<div class="rating-lab-distribution"><p class="rating-lab-inspector-label">Rating distribution</p><div class="rating-lab-histogram">' +
      bars + '</div><div class="rating-lab-histogram-axis"><span>' + number(min, 0) + '</span><span>' + number(max, 0) +
      '</span></div><p class="rating-lab-histogram-readout">Selected: ' + number(row.score, 1) + '</p></div>';
  }

  function renderDetail() {
    var dataset = state.datasets[state.sport];
    var rows = dataset.models[state.model].rankings;
    var row = rows.find(function (candidate) { return candidate.id === state.selected; });
    if (!row) {
      elements.detail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a row to inspect history, compare models, and pin competitors.</p>';
      return;
    }
    var crossModel = modelKeys.map(function (key) {
      var modelRow = dataset.models[key].rankings.find(function (candidate) { return candidate.id === row.id; });
      return '<tr><th scope="row">' + escapeHtml(dataset.models[key].label) + '</th><td>' +
        (modelRow ? '#' + modelRow.rank : '—') + '</td><td>' + (modelRow ? number(modelRow.score, 1) : '—') +
        '</td><td>' + (modelRow && modelRow.sigma !== null ? '±' + number(modelRow.sigma, 1) : '—') + '</td></tr>';
    }).join('');
    var isPinned = state.pinned.indexOf(row.id) !== -1;
    var pinnedRows = state.pinned.map(function (id) {
      return rows.find(function (candidate) { return candidate.id === id; });
    }).filter(Boolean);
    var compare = '';
    if (pinnedRows.length) {
      compare = '<div class="rating-lab-compare"><div class="rating-lab-compare-heading"><p class="rating-lab-inspector-label">Pinned comparison</p><div>' +
        pinnedRows.map(function (item) { return '<button type="button" data-unpin="' + escapeHtml(item.id) + '">' +
          escapeHtml(item.name) + ' ×</button>'; }).join('') + '</div></div>' +
        (pinnedRows.length === 2 ? historyChart(pinnedRows.map(function (item) { return { name: item.name, points: item.history }; }),
          pinnedRows[0].name + ' and ' + pinnedRows[1].name + ' rating comparison') :
          '<p class="rating-lab-detail-placeholder">Pin one more competitor to overlay both histories.</p>') + '</div>';
    }
    elements.detail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Rank ' + row.rank +
      '</p><h3>' + escapeHtml(row.name) + '</h3></div><strong>' + number(row.score, 1) + '</strong></div>' +
      '<button type="button" class="rating-lab-pin" data-pin="' + escapeHtml(row.id) + '" aria-pressed="' +
      (isPinned ? 'true' : 'false') + '">' + (isPinned ? 'Pinned for comparison' : 'Pin for comparison') + '</button>' +
      historyChart([{ name: row.name, points: row.history }], row.name + ' rating history') +
      '<p class="rating-lab-inspector-label">Across all four models</p><table class="rating-lab-model-compare"><thead><tr><th>Model</th><th>Rank</th><th>Score</th><th>Uncertainty</th></tr></thead><tbody>' +
      crossModel + '</tbody></table>' + distribution(row, rows) +
      '<dl><div><dt>Last played</dt><dd>' + formatDate(row.last_played) + '</dd></div><div><dt>Recent matches</dt><dd>' + row.recent_matches + '</dd></div><div><dt>All matches</dt><dd>' + row.matches + '</dd></div>' +
      (row.sigma === null ? '' : '<div><dt>Uncertainty σ</dt><dd>' + number(row.sigma, 2) + '</dd></div>') + '</dl>' + compare;
  }

  function parameterText(parameters) {
    return Object.keys(parameters).sort().map(function (key) {
      var value = parameters[key];
      return key + '=' + (typeof value === 'number' ? number(value, 4) : String(value));
    }).join(', ');
  }

  function renderAudit() {
    var data = state.datasets[state.sport];
    var status = state.manifest.sports[state.sport];
    var modelNames = modelKeys;
    elements.eligibility.textContent = data.eligibility.rule + ' “Recent” covers ' +
      number(data.eligibility.recent_window_days, 0) + ' days for this cohort.';
    elements.parameterBody.innerHTML = modelNames.map(function (model) {
      var candidates = data.candidate_parameters[model].map(parameterText).join(' · ');
      return '<tr><th scope="row">' + escapeHtml(data.models[model].label) + '</th>' +
        '<td><code>' + escapeHtml(parameterText(data.parameters[model])) + '</code></td>' +
        '<td><code>' + escapeHtml(candidates) + '</code></td></tr>';
    }).join('');
    var revision = state.manifest.code_revision || 'unknown';
    var snapshot = data.source.snapshot_sha256 || 'Published through source API/archive';
    elements.auditRecord.innerHTML = [
      ['Schema', data.schema_version],
      ['Method', state.manifest.methodology_version || '—'],
      ['Code revision', revision.substring(0, 12)],
      ['Generated', formatDate(data.generated_at)],
      ['Data window', formatDate(data.data_window.first_result) + ' – ' + formatDate(data.data_window.last_result)],
      ['Input size', number(data.data_window.matches, 0) + ' results · ' + number(data.data_window.entities, 0) + ' entities'],
      ['Source state', status.status],
      ['Snapshot SHA-256', snapshot]
    ].map(function (item) {
      return '<div><dt>' + escapeHtml(item[0]) + '</dt><dd>' + escapeHtml(item[1]) + '</dd></div>';
    }).join('');
    elements.dataDownload.href = dataUrl(state.sport + '.json');
  }

  function dateBefore(value, days) {
    var shifted = new Date(value + 'T12:00:00Z');
    shifted.setUTCDate(shifted.getUTCDate() - days);
    return shifted.toISOString().slice(0, 10);
  }

  function protocolSportRules(sport) {
    var rules = {
      tennis: {
        label: 'ATP singles',
        input: 'Completed tour-level singles results. Player identity uses the source player code; tournament start date is the available chronological date. Surface is normalized to hard, clay, grass, carpet, or unknown.',
        venue: 'Each prediction blends the global belief with the selected surface belief; the surface weight grows with surface evidence. Draws are not valid tennis outcomes.',
        initialization: 'Every player starts at Elo/Glicko-2 rating 1500 (Glicko-2 RD 350, volatility 0.06) or Gaussian μ=25, σ=8.333.',
        special: 'Every result updates both the global model and its surface-specific model. No seasonal regression.'
      },
      football: {
        label: 'European club football',
        input: 'Full-time results from the five covered domestic leagues and Champions League. Club identity uses the source ID, with normalized names only for the documented OpenFootball fallback.',
        venue: 'The listed home team receives the selected home advantage. A draw is y=0.5.',
        initialization: 'Every club starts at Elo/Glicko-2 rating 1500 (Glicko-2 RD 350, volatility 0.06) or Gaussian μ=25, σ=8.333.',
        special: 'Only club Elo regresses 25% toward 1500 when the season label changes. Glicko-2 instead responds through RD and volatility; Gaussian models do not receive seasonal mean reversion.'
      },
      'national-football': {
        label: "Men's national teams",
        input: 'Completed men’s full internationals since 2016. Country identity is a normalized team name from the CC0 source.',
        venue: 'Home advantage applies only when the source does not mark the match neutral. A draw is y=0.5.',
        initialization: 'Every national team starts at Elo/Glicko-2 rating 1500 (Glicko-2 RD 350, volatility 0.06) or Gaussian μ=25, σ=8.333.',
        special: 'No seasonal regression; all recorded tournament and friendly results receive the same update weight.'
      },
      chess: {
        label: 'Elite over-the-board chess',
        input: 'Decisive games and draws from official Lichess broadcast PGNs. Both players must have numeric FIDE IDs; online games and engine identities are excluded.',
        venue: 'White receives the selected color advantage. A draw is y=0.5.',
        initialization: 'At first appearance, Elo and Glicko-2 use the PGN FIDE rating when it is at least 1000 (Glicko-2 RD 100). Gaussian μ=25+(FIDE−2000)/80 with σ=3; otherwise the generic prior is retained.',
        special: 'All valid FIDE-identified broadcast games update ratings; the 2200 official-rating threshold applies to publication eligibility.'
      }
    };
    return rules[sport];
  }

  function protocolModelRules(model, parameters) {
    if (model === 'elo') {
      return {
        prediction: 'Compute expected score p = 1 / (1 + 10^−((Rₐ + advantage − Rᵦ) / scale)).',
        update: 'After recording p, update both sides symmetrically: R′ₐ = Rₐ + K(y−p) and R′ᵦ = Rᵦ − K(y−p).',
        publication: 'Publish and rank the raw Elo rating. Elo has no uncertainty estimate.',
        constants: 'Initial rating 1500. Selected K=' + number(parameters.k, 4) + ', scale=' + number(parameters.scale, 4) + ', advantage=' + number(parameters.home, 4) + '.'
      };
    }
    if (model === 'glicko2') {
      return {
        prediction: 'Compute the official Glicko-2 expected score after damping the rating gap by the opponent’s rating deviation; apply the declared home/White offset when relevant.',
        update: 'Batch every calendar date as one simultaneous rating period. Inflate RD for elapsed seven-day periods, solve the published iterative volatility equation, then update rating and RD from all results in that date.',
        publication: 'Publish rating, RD, and volatility; rank by the conservative score rating−2×RD, approximately the lower end of the documented 95% interval.',
        constants: 'Initial rating=' + number(parameters.initial_rating, 1) + ', RD=' + number(parameters.initial_rd, 1) +
          ', volatility=' + number(parameters.initial_volatility, 4) + ', selected τ=' + number(parameters.tau, 4) +
          ', period scale=' + number(parameters.period_days, 1) + ' days, advantage=' + number(parameters.home, 2) + '.'
      };
    }
    var robust = model === 'robust';
    return {
      prediction: 'Integrate win, draw, and loss likelihoods over the Gaussian belief for the skill difference using the fixed 20-node Gauss–Hermite rule. Expected score is p(win)+0.5p(draw).',
      update: 'Before prediction, add τ² × max(days inactive / 7, 1) to each variance. Condition on the observed result, numerically compute the posterior moments, then moment-match back to independent Gaussian beliefs.',
      publication: 'Publish μ and σ, but rank by the conservative score μ−3σ. More uncertainty therefore lowers the published rank.',
      constants: 'Initial μ=25 and σ=8.333; τ=0.08333; performance noise ' + (robust ? 'Student-t ν=1 (Cauchy)' : 'Gaussian') +
        '; β=' + number(parameters.beta, 4) + '; draw margin=' + number(parameters.draw_margin, 4) + '; advantage=' + number(parameters.advantage, 4) + '.'
    };
  }

  function protocolParameterMeaning(key) {
    return {
      k: 'Maximum Elo response scale for one result',
      scale: 'Rating-gap width in the Elo logistic curve',
      home: 'Rating points added only when the home/White advantage flag is true',
      surface_weight: 'Maximum weight assigned to the independently replayed tennis-surface belief; actual weight grows from zero over the first 20 combined surface matches',
      tau: 'Glicko-2 constraint on how quickly volatility may change',
      initial_rating: 'Glicko-2 initial rating',
      initial_rd: 'Glicko-2 initial rating deviation',
      initial_volatility: 'Glicko-2 initial volatility',
      period_days: 'Calendar days represented by one inactivity period',
      beta: 'Performance-noise scale; larger values expect more upsets',
      draw_margin: 'Skill-difference interval treated as a draw',
      advantage: 'Bayesian skill units added when home/White advantage is active',
      robust: 'Whether performance noise uses Student-t ν=1 rather than Gaussian'
    }[key] || key;
  }

  function renderProtocol() {
    var data = state.datasets[state.sport];
    var model = data.models[state.model];
    var parameters = data.parameters[state.model];
    var sportRules = protocolSportRules(state.sport);
    var modelRules = protocolModelRules(state.model, parameters);
    var latest = data.data_window.last_result;
    var validationStart = dateBefore(latest, 730);
    var evaluationStart = dateBefore(latest, 365);
    var parameterRows = Object.keys(parameters).sort().map(function (key) {
      var value = parameters[key];
      return '<div><dt><code>' + escapeHtml(key) + '</code></dt><dd><strong>' +
        escapeHtml(typeof value === 'number' ? number(value, 4) : String(value)) + '</strong><span>' +
        escapeHtml(protocolParameterMeaning(key)) + '</span></dd></div>';
    }).join('');
    var candidates = data.candidate_parameters[state.model].map(parameterText).join(' · ');
    var metric = model.metrics;
    elements.protocol.innerHTML = '<p class="rating-lab-protocol-status"><strong>' + escapeHtml(sportRules.label) +
      ' · ' + escapeHtml(model.label) + '</strong><span>Source window ' + escapeHtml(formatDate(data.data_window.first_result)) +
      '–' + escapeHtml(formatDate(latest)) + ' · ' + number(data.data_window.matches, 0) + ' deduplicated results</span></p>' +
      '<ol class="rating-lab-protocol-flow">' +
      '<li><span>1</span><div><h3>Accept and identify</h3><p>' + escapeHtml(sportRules.input) + '</p></div></li>' +
      '<li><span>2</span><div><h3>Order deterministically</h3><p>Deduplicate exact date/entity/score/competition signatures, then sort by date, entity A ID, entity B ID, competition, and score. ' + escapeHtml(sportRules.initialization) + '</p></div></li>' +
      '<li><span>3</span><div><h3>Predict before learning</h3><p>' + escapeHtml(modelRules.prediction + ' ' + sportRules.venue) + '</p></div></li>' +
      '<li><span>4</span><div><h3>Apply the result</h3><p>' + escapeHtml(modelRules.update + ' ' + sportRules.special) + '</p></div></li>' +
      '<li><span>5</span><div><h3>Evaluate and publish</h3><p>' + escapeHtml(modelRules.publication) + ' Histories are display-downsampled to at most 24 points; rating replay itself is not downsampled.</p></div></li>' +
      '</ol><div class="rating-lab-protocol-grid"><article><h3>Selected parameters</h3><dl class="rating-lab-protocol-parameters">' +
      parameterRows + '</dl><p class="rating-lab-protocol-fixed"><strong>Fixed constants:</strong> ' + escapeHtml(modelRules.constants) +
      '</p></article><article><h3>Eligibility and publication</h3><p>' + escapeHtml(data.eligibility.rule) + '</p><p>“Recent” counts the latest ' +
      number(data.eligibility.recent_window_days, 0) + ' days. After eligibility, the public file retains at most the top 500 entities for each model.</p>' +
      '<h3>Candidate grid actually tested</h3><p><code>' + escapeHtml(candidates) + '</code></p></article></div>' +
      '<div class="rating-lab-protocol-evaluation"><h3>Chronological tuning and untouched evaluation</h3><div><p><strong>Warm-up</strong><span>Before ' +
      escapeHtml(formatDate(validationStart)) + '</span></p><p><strong>Validation</strong><span>' + escapeHtml(formatDate(validationStart)) +
      '–' + escapeHtml(formatDate(evaluationStart)) + '</span></p><p><strong>Evaluation</strong><span>' + escapeHtml(formatDate(evaluationStart)) +
      '–' + escapeHtml(formatDate(latest)) + '</span></p></div><p>Choose the declared candidate with the lowest validation log loss. Then score ' +
      number(metric.predictions, 0) + ' one-step-ahead evaluation predictions: log loss ' + number(metric.log_loss, 4) +
      ', Brier ' + number(metric.brier, 4) + ', calibration gap ' + number(metric.calibration, 4) +
      '. Calibration uses 10 equal-width probability bins and a count-weighted absolute predicted-versus-observed gap.</p></div>';
    setPressed(elements.protocolSportTabs, 'protocolSport', state.sport);
    setPressed(elements.protocolModelTabs, 'protocolModel', state.model);
  }

  function predictorCompetitions() {
    var rows = ['football', 'national-football', 'chess'].reduce(function (items, sport) {
      var predictor = state.datasets[sport].tournament_predictor;
      if (!predictor) return items;
      predictor.competitions.forEach(function (competition) {
        items.push({ sport: sport, predictor: predictor, competition: competition });
      });
      return items;
    }, []);
    var priority = { live: 0, scheduled: 1, 'waiting for draw': 2, complete: 3 };
    return rows.sort(function (a, b) {
      var priorityA = Object.prototype.hasOwnProperty.call(priority, a.competition.status) ? priority[a.competition.status] : 9;
      var priorityB = Object.prototype.hasOwnProperty.call(priority, b.competition.status) ? priority[b.competition.status] : 9;
      return priorityA - priorityB ||
        a.competition.label.localeCompare(b.competition.label);
    });
  }

  function predictorData() {
    var view = predictorCompetitions().find(function (item) {
      return item.competition.id === state.predictorCompetition;
    });
    if (!view) return null;
    view.model = view.competition.models[state.predictorModel] || null;
    return view;
  }

  function probabilityCell(value) {
    return '<span class="rating-lab-probability" style="--probability:' +
      (value * 100).toFixed(1) + '%"><span>' + percent(value) + '</span></span>';
  }

  function renderMarketComparison(view, modelRows) {
    var benchmark = view.predictor.market_comparison;
    elements.predictorMarket.hidden = false;
    if (!benchmark) {
      elements.predictorMarket.innerHTML = '<p><strong>Market comparison not in this snapshot.</strong> Refresh the published dataset to check for a confidently matched public market.</p>';
      return;
    }
    var snapshot = (benchmark.competitions || []).find(function (item) {
      return item.competition_id === view.competition.id;
    });
    if (!snapshot) {
      var search = (benchmark.searches || []).find(function (item) {
        return item.competition_id === view.competition.id;
      });
      var reason = search && search.status === 'source_error' ?
        'The market source could not be checked.' :
        'No active event passed the participant-coverage and identity checks.';
      elements.predictorMarket.innerHTML = '<div class="rating-lab-market-heading"><div><p class="rating-lab-kicker">External benchmark</p><h3>No confident Polymarket match</h3></div></div><p>' +
        escapeHtml(reason) + ' Our forecast remains available and independent; no market is guessed or attached by title alone.</p>';
      return;
    }
    var rowsById = {};
    (modelRows || []).forEach(function (row) { rowsById[row.id] = row; });
    var comparisons = snapshot.outcomes.reduce(function (items, outcome) {
      var modelRow = rowsById[outcome.entity_id];
      if (!modelRow || !Number.isFinite(modelRow.champion)) return items;
      items.push({
        name: outcome.name,
        model: modelRow.champion,
        market: outcome.normalized_probability,
        gap: modelRow.champion - outcome.normalized_probability,
        bid: outcome.best_bid,
        ask: outcome.best_ask,
        liquidity: outcome.liquidity_usd,
        raw: outcome.raw_yes_price
      });
      return items;
    }, []);
    comparisons.sort(function (a, b) { return Math.abs(b.gap) - Math.abs(a.gap) || a.name.localeCompare(b.name); });
    var meanGap = comparisons.length ? comparisons.reduce(function (sum, row) {
      return sum + Math.abs(row.gap);
    }, 0) / comparisons.length : null;
    var retained = benchmark.status !== 'current' || isStale(benchmark);
    var freshness = retained ? ' · retained or delayed snapshot' : '';
    var table = comparisons.length ? '<div class="rating-lab-market-table-wrap"><table><caption>Largest model–market differences first</caption><thead><tr><th scope="col">Participant</th><th scope="col">Our model</th><th scope="col">Market</th><th scope="col">Gap</th><th scope="col">Raw quote</th><th scope="col">Bid–ask</th></tr></thead><tbody>' +
      comparisons.map(function (row) {
        var gapClass = row.gap > 0 ? 'is-positive' : row.gap < 0 ? 'is-negative' : '';
        var gap = (row.gap > 0 ? '+' : '') + number(row.gap * 100, 1) + ' pp';
        var spread = row.bid > 0 && row.ask > 0 ? number(row.bid * 100, 1) + '–' + number(row.ask * 100, 1) + '%' : '—';
        return '<tr><th scope="row">' + escapeHtml(row.name) + '</th><td>' + percent(row.model) + '</td><td>' +
          percent(row.market) + '</td><td class="' + gapClass + '">' + escapeHtml(gap) + '</td><td>' +
          percent(row.raw) + '</td><td>' + escapeHtml(spread) + '</td></tr>';
      }).join('') + '</tbody></table></div>' :
      '<p><strong>A market was matched, but no participant IDs overlap this model output.</strong> The comparison is withheld.</p>';
    elements.predictorMarket.classList.toggle('is-stale', retained);
    elements.predictorMarket.innerHTML = '<div class="rating-lab-market-heading"><div><p class="rating-lab-kicker">External benchmark</p><h3>Our protocol vs Polymarket</h3></div><a href="' +
      escapeHtml(snapshot.event_url) + '" target="_blank" rel="noopener">Open market ↗</a></div><div class="rating-lab-market-metrics"><div><span>Field coverage</span><strong>' +
      snapshot.matched_participants + ' / ' + snapshot.model_participants + '</strong></div><div><span>Raw Yes total</span><strong>' +
      number(snapshot.raw_yes_price_sum * 100, 1) + '%</strong></div><div><span>Mean absolute gap</span><strong>' +
      (meanGap === null ? '—' : number(meanGap * 100, 1) + ' pp') + '</strong></div></div><p class="rating-lab-market-note">Snapshot ' +
      escapeHtml(formatDate(benchmark.fetched_at)) + freshness + '. “Market” divides each public Yes quote by the raw Yes total across all active liquid winner outcomes. The raw total and quote remain visible. Positive gap means our selected protocol gives a higher title probability. Market prices are an external benchmark only—never a rating or simulation input.</p>' + table;
  }

  function errorFunction(value) {
    var sign = value < 0 ? -1 : 1;
    var x = Math.abs(value);
    var t = 1 / (1 + 0.3275911 * x);
    var approximation = 1 - (((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t -
      0.284496736) * t + 0.254829592) * t * Math.exp(-x * x));
    return sign * approximation;
  }

  function normalCdf(value) {
    return 0.5 * (1 + errorFunction(value / Math.sqrt(2)));
  }

  function performanceCdf(value, robust) {
    return robust ? 0.5 + Math.atan(value) / Math.PI : normalCdf(value);
  }

  function bayesianLikelihood(difference, score, parameters, robust) {
    var cdf = function (value) { return performanceCdf(value, robust); };
    if (score === 0.5) {
      return Math.max(cdf((parameters.draw_margin - difference) / parameters.beta) -
        cdf((-parameters.draw_margin - difference) / parameters.beta), 1e-12);
    }
    var signed = score === 1 ? difference : -difference;
    return Math.max(cdf((signed - parameters.draw_margin) / parameters.beta), 1e-12);
  }

  function beliefOutcomes(rowA, rowB, dataset, advantage) {
    var parameters = dataset.parameters[state.model];
    var meanDifference = rowA.rating - rowB.rating + advantage;
    if (state.model === 'elo' || state.model === 'glicko2') {
      var expected;
      if (state.model === 'elo') {
        expected = 1 / (1 + Math.pow(10, -meanDifference / parameters.scale));
      } else {
        var opponentPhi = rowB.sigma / 173.7178;
        var glickoDamping = 1 / Math.sqrt(1 + 3 * opponentPhi * opponentPhi / (Math.PI * Math.PI));
        expected = 1 / (1 + Math.exp(-glickoDamping * meanDifference / 173.7178));
      }
      var context = dataset.outcome_context || {};
      var empiricalDrawRate = Number.isFinite(context.draw_rate) ? context.draw_rate : state.sport === 'tennis' ? 0 : 0.25;
      var draw = Math.min(empiricalDrawRate * 4 * expected * (1 - expected), 2 * Math.min(expected, 1 - expected));
      return {
        win: expected - 0.5 * draw,
        draw: draw,
        loss: 1 - expected - 0.5 * draw,
        expected: expected,
        difference: meanDifference,
        empiricalDrawRate: empiricalDrawRate,
        parameters: parameters
      };
    }
    var variance = rowA.sigma * rowA.sigma + rowB.sigma * rowB.sigma;
    var totals = [0, 0, 0];
    ghNodes.forEach(function (node, index) {
      var difference = meanDifference + Math.sqrt(2 * variance) * node;
      totals[0] += ghWeights[index] * bayesianLikelihood(difference, 1, parameters, state.model === 'robust');
      totals[1] += ghWeights[index] * bayesianLikelihood(difference, 0.5, parameters, state.model === 'robust');
      totals[2] += ghWeights[index] * bayesianLikelihood(difference, 0, parameters, state.model === 'robust');
    });
    var total = Math.max((totals[0] + totals[1] + totals[2]) / Math.sqrt(Math.PI), 1e-12);
    return {
      win: totals[0] / Math.sqrt(Math.PI) / total,
      draw: totals[1] / Math.sqrt(Math.PI) / total,
      loss: totals[2] / Math.sqrt(Math.PI) / total,
      expected: (totals[0] + 0.5 * totals[1]) / Math.sqrt(Math.PI) / total,
      difference: meanDifference,
      variance: variance,
      parameters: parameters
    };
  }

  function matchupOutcomes(rowA, rowB, dataset) {
    var parameters = dataset.parameters[state.model];
    if (state.sport === 'tennis') {
      var surface = state.matchupVenue;
      var contextA = rowA.contexts && rowA.contexts[surface];
      var contextB = rowB.contexts && rowB.contexts[surface];
      var globalOutcome = beliefOutcomes(rowA, rowB, dataset, 0);
      if (!contextA || !contextB) {
        globalOutcome.surface = surface;
        globalOutcome.surfaceWeight = 0;
        globalOutcome.globalExpected = globalOutcome.expected;
        globalOutcome.surfaceExpected = null;
        return globalOutcome;
      }
      var surfaceOutcome = beliefOutcomes(contextA, contextB, dataset, 0);
      var evidence = Math.min((contextA.matches + contextB.matches) / 20, 1);
      var weight = parameters.surface_weight * evidence;
      return {
        win: (1 - weight) * globalOutcome.win + weight * surfaceOutcome.win,
        draw: (1 - weight) * globalOutcome.draw + weight * surfaceOutcome.draw,
        loss: (1 - weight) * globalOutcome.loss + weight * surfaceOutcome.loss,
        expected: (1 - weight) * globalOutcome.expected + weight * surfaceOutcome.expected,
        difference: (1 - weight) * globalOutcome.difference + weight * surfaceOutcome.difference,
        variance: Number.isFinite(globalOutcome.variance) && Number.isFinite(surfaceOutcome.variance) ?
          (1 - weight) * globalOutcome.variance + weight * surfaceOutcome.variance : null,
        empiricalDrawRate: globalOutcome.empiricalDrawRate,
        parameters: parameters,
        surface: surface,
        surfaceWeight: weight,
        globalExpected: globalOutcome.expected,
        surfaceExpected: surfaceOutcome.expected,
        contextA: contextA,
        contextB: contextB
      };
    }
    var advantageDirection = state.matchupVenue === 'a' ? 1 : state.matchupVenue === 'b' ? -1 : 0;
    var advantage = advantageDirection * (state.model === 'elo' || state.model === 'glicko2' ? parameters.home : parameters.advantage);
    return beliefOutcomes(rowA, rowB, dataset, advantage);
  }

  function matchupVenueOptions(rowA, rowB) {
    var nameA = rowA ? rowA.name : 'Competitor A';
    var nameB = rowB ? rowB.name : 'Competitor B';
    if (state.sport === 'tennis') {
      var contexts = state.datasets.tennis.prediction_contexts;
      return contexts.values.map(function (surface) {
        return { value: surface.id, label: surface.label + ' court' };
      });
    }
    if (state.sport === 'chess') return [
      { value: 'a', label: nameA + ' plays White' },
      { value: 'b', label: nameB + ' plays White' },
      { value: 'neutral', label: 'White not assigned · neutral assumption' }
    ];
    return [
      { value: 'a', label: nameA + ' at home' },
      { value: 'neutral', label: 'Neutral venue' },
      { value: 'b', label: nameB + ' at home' }
    ];
  }

  function populateMatchupControls() {
    var rows = state.datasets[state.sport].models[state.model].rankings;
    if (!rows.some(function (row) { return row.id === state.matchupA; })) state.matchupA = rows[0] ? rows[0].id : null;
    if (!rows.some(function (row) { return row.id === state.matchupB; }) || state.matchupB === state.matchupA) {
      state.matchupB = rows.find(function (row) { return row.id !== state.matchupA; });
      state.matchupB = state.matchupB ? state.matchupB.id : null;
    }
    var options = rows.map(function (row) {
      return '<option value="' + escapeHtml(row.id) + '">#' + row.rank + ' · ' + escapeHtml(row.name) + '</option>';
    }).join('');
    elements.matchupA.innerHTML = options;
    elements.matchupB.innerHTML = options;
    elements.matchupA.value = state.matchupA || '';
    elements.matchupB.value = state.matchupB || '';
    var rowA = rows.find(function (row) { return row.id === state.matchupA; });
    var rowB = rows.find(function (row) { return row.id === state.matchupB; });
    var venues = matchupVenueOptions(rowA, rowB);
    if (!venues.some(function (venue) { return venue.value === state.matchupVenue; })) state.matchupVenue = venues[0].value;
    elements.matchupVenue.innerHTML = venues.map(function (venue) {
      return '<option value="' + venue.value + '">' + escapeHtml(venue.label) + '</option>';
    }).join('');
    elements.matchupVenue.value = state.matchupVenue;
    elements.matchupVenue.disabled = venues.length === 1;
    elements.matchupVenueLabel.textContent = state.sport === 'chess' ? 'Who plays White?' : state.sport === 'tennis' ? 'Surface' : 'Venue';
    setPressed(elements.matchupModelTabs, 'matchupModel', state.model);
  }

  function renderMatchup() {
    var dataset = state.datasets[state.sport];
    var rows = dataset.models[state.model].rankings;
    populateMatchupControls();
    var rowA = rows.find(function (row) { return row.id === state.matchupA; });
    var rowB = rows.find(function (row) { return row.id === state.matchupB; });
    if (!rowA || !rowB) {
      elements.matchupResult.innerHTML = '<p>Two published competitors are required for a matchup forecast.</p>';
      return;
    }
    var outcome = matchupOutcomes(rowA, rowB, dataset);
    var includesDraw = state.sport !== 'tennis';
    var outcomes = [
      { label: rowA.name + ' wins', short: 'A win', value: outcome.win, className: 'is-a' }
    ];
    if (includesDraw) outcomes.push({ label: 'Draw', short: 'Draw', value: outcome.draw, className: 'is-draw' });
    outcomes.push({ label: rowB.name + ' wins', short: 'B win', value: outcome.loss, className: 'is-b' });
    var strip = outcomes.map(function (item) {
      return '<span class="' + item.className + '" style="--outcome-width:' + (item.value * 100).toFixed(4) +
        '%" aria-hidden="true"></span>';
    }).join('');
    var cards = outcomes.map(function (item) {
      return '<div class="' + item.className + '"><span><i aria-hidden="true"></i>' + escapeHtml(item.label) +
        '</span><strong>' + percent(item.value) +
        '</strong><small>' + number(item.value * 100, 2) + '%</small></div>';
    }).join('');
    var venue = matchupVenueOptions(rowA, rowB).find(function (item) { return item.value === state.matchupVenue; });
    var parameters = outcome.parameters;
    var context = dataset.outcome_context || {
      draw_rate: state.sport === 'tennis' ? 0 : 0.25,
      draws: 0,
      matches: dataset.data_window.matches,
      method: 'Legacy snapshot fallback; refresh to schema 1.4.0 for cohort draw context.'
    };
    var beliefLabel = function (row) {
      return state.model === 'elo' ? number(row.rating, 1) : state.model === 'glicko2' ?
        'rating ' + number(row.rating, 2) + ', RD ' + number(row.sigma, 2) + ', volatility ' + number(row.volatility, 5) :
        'μ ' + number(row.rating, 2) + ', σ ' + number(row.sigma, 2);
    };
    var ratingA = beliefLabel(rowA);
    var ratingB = beliefLabel(rowB);
    if (outcome.contextA && outcome.contextB) {
      ratingA += '; ' + venue.label + ' ' + beliefLabel(outcome.contextA) + ' from ' + outcome.contextA.matches + ' matches';
      ratingB += '; ' + venue.label + ' ' + beliefLabel(outcome.contextB) + ' from ' + outcome.contextB.matches + ' matches';
    }
    var calculation;
    if (state.model === 'elo') {
      calculation = 'Expected score uses 1 / (1 + 10^(−Δ/' + number(parameters.scale, 0) + ')), where Δ includes ' +
        number(parameters.home, 2) + ' rating points when home advantage applies. The three-way split allocates draws as d = min(q × 4p(1−p), 2min(p,1−p)), using empirical q=' +
        number(outcome.empiricalDrawRate, 4) + ' from ' + number(context.draws, 0) + ' draws in ' +
        number(context.matches, 0) + ' replay results; win probabilities are p−d/2 and 1−p−d/2.';
    } else if (state.model === 'glicko2') {
      calculation = 'Expected score uses 1 / (1 + exp(−g(RDᵦ/173.7178) × Δ/173.7178)), with g(φ)=1/√(1+3φ²/π²). Δ includes ' +
        number(parameters.home, 2) + ' rating points when the selected home/White advantage applies. The result-only three-way display uses the same declared empirical-draw allocation as Elo; the Glicko-2 rating update itself records a draw as score 0.5.';
    } else {
      calculation = 'The published Gaussian skill beliefs are combined into Δ ~ N(' + number(outcome.difference, 3) + ', ' +
        number(outcome.variance, 3) + '). Win, draw, and loss likelihoods use ' +
        (state.model === 'robust' ? 'Student-t ν=1 performance noise' : 'Gaussian performance noise') +
        ' with β=' + number(parameters.beta, 4) + ' and draw margin=' + number(parameters.draw_margin, 4) +
        ', integrated with the same fixed 20-node Gauss–Hermite rule as the rating replay. The eligible cohort’s observed draw rate is ' +
        number(context.draw_rate * 100, 2) + '% (' + number(context.draws, 0) + ' of ' + number(context.matches, 0) +
        '); the Bayesian likelihood is not forced to equal that baseline.';
    }
    if (state.sport === 'tennis') {
      var surfaceDetail = outcome.surfaceExpected === null ?
        'One or both players have no published belief for this surface, so this matchup uses the global belief only.' :
        'Global expected score ' + number(outcome.globalExpected, 4) + ' and surface expected score ' +
        number(outcome.surfaceExpected, 4) + ' are blended with actual surface weight ' +
        number(outcome.surfaceWeight, 4) + '. The maximum selected surface weight is ' +
        number(parameters.surface_weight, 4) + '; evidence scales it over the first 20 combined surface matches.';
      calculation = surfaceDetail + ' ' + calculation;
    }
    var eventContext = state.sport === 'tennis' ? 'surface' : state.sport === 'chess' ? 'color' : 'venue';
    var unusedContext = state.sport === 'tennis' ?
      'It does not use score margin, injuries, player age, or bookmaker information' :
      'It does not use score margin, line-ups, injuries, time control, player age, or bookmaker information';
    elements.matchupResult.innerHTML = '<div class="rating-lab-matchup-context"><strong>' +
      escapeHtml(dataset.models[state.model].label) + '</strong><span>' + escapeHtml(venue.label) + ' · rating snapshot ' +
      escapeHtml(formatDate(dataset.latest_result)) + '</span></div><div class="rating-lab-outcome-strip" role="img" aria-label="' +
      escapeHtml(outcomes.map(function (item) { return item.label + ' ' + number(item.value * 100, 2) + ' percent'; }).join(', ')) + '">' +
      strip + '</div><div class="rating-lab-outcome-cards">' + cards + '</div><p class="rating-lab-outcome-explainer">Colors only identify the outcomes shown above; they do not mean good, bad, certain, or uncertain.</p><dl class="rating-lab-matchup-inputs"><div><dt>' +
      escapeHtml(rowA.name) + '</dt><dd>' + escapeHtml(ratingA) + '</dd></div><div><dt>Expected score A</dt><dd>' +
      number(outcome.expected, 4) + '</dd></div><div><dt>' + escapeHtml(rowB.name) + '</dt><dd>' + escapeHtml(ratingB) +
      '</dd></div></dl><details class="rating-lab-matchup-method"><summary>Exact calculation and assumptions</summary><p>' +
      escapeHtml(calculation) + '</p><p><strong>Published inputs:</strong> A ' + escapeHtml(ratingA) + '; B ' +
      escapeHtml(ratingB) + '; adjusted difference ' + number(outcome.difference, 3) + '. ' + escapeHtml(context.method) +
      '</p><p>This is a result-and-context probability for one event at the selected ' + eventContext + '. The published evaluation scores expected score, not a separately calibrated three-class forecast. ' + unusedContext + ', and it contains no betting margin. <a href="#protocol">Inspect the full protocol</a> or <a href="' +
      escapeHtml(dataset.source.source_url) + '">open the source data</a>.</p></details>';
  }

  function renderLeaguePredictorDetail(team) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a team to inspect its full finishing-position distribution.</p>';
      return;
    }
    var bars = team.positions.map(function (probability, index) {
      var relegation = index >= team.positions.length - 3 ? ' is-relegation' : '';
      return '<span class="rating-lab-position-bar' + relegation + '" style="--height:' +
        Math.max(probability * 100, 1).toFixed(1) + '%" aria-label="Position ' + (index + 1) + ': ' +
        escapeHtml(percent(probability)) + '"></span>';
    }).join('');
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Expected position ' +
      number(team.expected_position, 2) + '</p><h3>' + escapeHtml(team.name) + '</h3></div><strong>' +
      number(team.expected_points, 1) + ' pts</strong></div>' +
      '<div class="rating-lab-position-chart" role="img" aria-label="Finishing-position probabilities for ' +
      escapeHtml(team.name) + '">' + bars + '</div><div class="rating-lab-position-axis"><span>Champion</span><span>Position ' +
      team.positions.length + '</span></div><dl><div><dt>Title</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>Top four</dt><dd>' + percent(team.top_four) +
      '</dd></div><div><dt>Bottom three</dt><dd>' + percent(team.bottom_three) +
      '</dd></div><div><dt>Current points</dt><dd>' + team.current_points + '</dd></div></dl>';
  }

  function renderStandingsPredictorDetail(team) {
    if (!team) return renderLeaguePredictorDetail(team);
    var bars = team.positions.map(function (probability, index) {
      return '<span class="rating-lab-position-bar" style="--height:' + Math.max(probability * 100, 1).toFixed(1) +
        '%" aria-label="Position ' + (index + 1) + ': ' + escapeHtml(percent(probability)) + '"></span>';
    }).join('');
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Expected position ' +
      number(team.expected_position, 2) + '</p><h3>' + escapeHtml(team.name) + '</h3></div><strong>' +
      number(team.expected_points, 1) + ' pts</strong></div><div class="rating-lab-position-chart" role="img" aria-label="Final-position probabilities for ' +
      escapeHtml(team.name) + '">' + bars + '</div><div class="rating-lab-position-axis"><span>Winner</span><span>Position ' +
      team.positions.length + '</span></div><dl><div><dt>Win event</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>Podium</dt><dd>' + percent(team.podium) + '</dd></div><div><dt>Last place</dt><dd>' +
      percent(team.last_place) + '</dd></div><div><dt>Current points</dt><dd>' + number(team.current_points, 1) + '</dd></div></dl>';
  }

  function renderKnockoutPredictorDetail(team, model) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a participant to inspect its advancement probabilities.</p>';
      return;
    }
    var nextLabel = model.current_stage === 'Complete' ? 'Recorded champion' : 'Survive published stage';
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">' +
      escapeHtml(model.current_stage) + '</p><h3>' + escapeHtml(team.name) + '</h3></div><strong>' +
      percent(team.champion) + '</strong></div><dl><div><dt>Win competition</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>' + escapeHtml(nextLabel) + '</dt><dd>' + percent(team.reach_next_stage) +
      '</dd></div><div><dt>Model rating</dt><dd>' + number(team.rating, 1) + '</dd></div></dl>';
  }

  function setPredictorColumns(type) {
    var knockout = type === 'knockout';
    var standings = type === 'standings';
    elements.predictorColumns.rank.textContent = knockout ? 'Forecast' : 'Projected';
    elements.predictorColumns.team.textContent = knockout ? 'Participant' : standings ? 'Player' : 'Team';
    elements.predictorColumns.now.textContent = knockout ? 'Rating' : 'Now';
    elements.predictorColumns.value.textContent = knockout ? 'Next stage' : 'Expected pts';
    elements.predictorColumns.title.textContent = standings ? 'Win event' : 'Title';
    elements.predictorColumns.secondary.textContent = standings ? 'Podium' : 'Top four';
    elements.predictorColumns.tertiary.textContent = standings ? 'Last place' : 'Bottom three';
    elements.predictorColumns.secondary.hidden = knockout;
    elements.predictorColumns.tertiary.hidden = knockout;
  }

  function setPerformanceColumns() {
    elements.predictorColumns.rank.textContent = 'Performance';
    elements.predictorColumns.team.textContent = 'Participant';
    elements.predictorColumns.now.textContent = 'W–D–L';
    elements.predictorColumns.value.textContent = 'Start';
    elements.predictorColumns.title.textContent = 'Final rating';
    elements.predictorColumns.secondary.textContent = 'Change';
    elements.predictorColumns.tertiary.textContent = 'Score';
    elements.predictorColumns.secondary.hidden = false;
    elements.predictorColumns.tertiary.hidden = false;
  }

  function renderPerformanceDetail(team, model) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a participant to inspect its completed-event performance.</p>';
      return;
    }
    var changeClass = team.change > 0 ? 'is-positive' : team.change < 0 ? 'is-negative' : '';
    var surpriseClass = team.score_residual > 0 ? 'is-positive' : team.score_residual < 0 ? 'is-negative' : '';
    var change = (team.change > 0 ? '+' : '') + number(team.change, 2);
    var isGlicko = model.rating_type === 'glicko2_conservative_r_minus_2rd';
    var startBelief = model.rating_type === 'elo' ? number(team.start_rating, 2) : isGlicko ?
      'rating ' + number(team.start_rating, 2) + ' · RD ' + number(team.start_sigma, 2) + ' · volatility ' + number(team.start_volatility, 5) :
      'μ ' + number(team.start_rating, 2) + ' · σ ' + number(team.start_sigma, 2);
    var endBelief = model.rating_type === 'elo' ? number(team.end_rating, 2) : isGlicko ?
      'rating ' + number(team.end_rating, 2) + ' · RD ' + number(team.end_sigma, 2) + ' · volatility ' + number(team.end_volatility, 5) :
      'μ ' + number(team.end_rating, 2) + ' · σ ' + number(team.end_sigma, 2);
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Protocol performance #' +
      team.rank + '</p><h3>' + escapeHtml(team.name) + '</h3></div><strong>' + number(team.performance_rating, 2) +
      '</strong></div><dl><div><dt>Event record</dt><dd>' + team.wins + '–' + team.draws + '–' + team.losses +
      '</dd></div><div><dt>Result score</dt><dd>' + number(team.points, 2) + ' / ' + number(team.matches, 0) +
      '</dd></div><div><dt>Protocol expectation</dt><dd>' + number(team.expected_score, 2) + ' / ' + number(team.matches, 0) +
      '</dd></div><div><dt>Score residual</dt><dd class="' + surpriseClass + '">' +
      (team.score_residual > 0 ? '+' : '') + number(team.score_residual, 2) +
      '</dd></div><div><dt>Standardized surprise</dt><dd class="' + surpriseClass + '">' +
      (team.surprise_index > 0 ? '+' : '') + number(team.surprise_index, 2) + ' σ' +
      '</dd></div><div><dt>Starting belief</dt><dd>' + escapeHtml(startBelief) + '</dd></div><div><dt>Final belief</dt><dd>' +
      escapeHtml(endBelief) + '</dd></div><div><dt>Published start</dt><dd>' + number(team.start_score, 2) +
      '</dd></div><div><dt>Performance change</dt><dd class="' + changeClass + '">' + change +
      '</dd></div></dl><p class="rating-lab-performance-note">The final published score is Elo, Glicko-2 rating−2RD, or Gaussian μ−3σ after replaying only this competition from the strictly pre-event state. It is not the official competition table or a conventional bookmaker rating.</p>';
  }

  function renderPerformanceChart(rows, model, competition, sport) {
    var rankedRows = rows.filter(function (team) {
      return Number.isFinite(team.surprise_index) && Number.isFinite(team.expected_score);
    }).slice().sort(function (a, b) {
      return b.surprise_index - a.surprise_index || a.name.localeCompare(b.name);
    });
    if (!rankedRows.length) {
      elements.predictorPerformanceChart.hidden = true;
      elements.predictorPerformanceChart.innerHTML = '';
      return;
    }
    var chartRows = rankedRows.filter(function (team) { return team.surprise_index >= 0; }).slice(0, 6)
      .concat(rankedRows.filter(function (team) { return team.surprise_index < 0; }).slice(-6))
      .sort(function (a, b) { return b.surprise_index - a.surprise_index || a.name.localeCompare(b.name); });
    var maxAbs = Math.max(1, Math.max.apply(null, chartRows.map(function (team) {
      return Math.abs(team.surprise_index);
    })));
    var modelLabel = state.datasets[sport].models[state.predictorModel].label;
    elements.predictorPerformanceChart.hidden = false;
    elements.predictorPerformanceChart.innerHTML =
      '<div class="rating-lab-performance-heading"><div><p class="rating-lab-kicker">Actual versus expected</p>' +
      '<h3 id="predictor-performance-title">Largest completed-event surprises</h3></div>' +
      '<p>Selected protocol: <strong>' + escapeHtml(modelLabel) + '</strong></p></div>' +
      '<p class="rating-lab-performance-subtitle">The six largest outperformers and underperformers by signed standardized result-score residual. Solid dark bars point right; outlined light bars point left, so color is not the only cue. The complete participant table remains below.</p>' +
      '<div class="rating-lab-performance-scroll"><div class="rating-lab-performance-plot" role="group" aria-label="' +
      escapeHtml(competitionTitle(competition) + ' actual result score versus ' + modelLabel + ' expectation') + '">' +
      '<div class="rating-lab-performance-axis" aria-hidden="true"><span>Underperformed</span><span>As expected</span><span>Outperformed</span></div>' +
      chartRows.map(function (team) {
        var positive = team.surprise_index >= 0;
        var signedSurprise = (team.surprise_index > 0 ? '+' : '') + number(team.surprise_index, 2) + ' σ';
        var signedResidual = (team.score_residual > 0 ? '+' : '') + number(team.score_residual, 2);
        var size = Math.min(Math.abs(team.surprise_index) / maxAbs * 50, 50).toFixed(3) + '%';
        var label = team.name + ': actual ' + number(team.points, 2) + ', expected ' + number(team.expected_score, 2) +
          ', residual ' + signedResidual + ', standardized surprise ' + signedSurprise + ', ' + team.matches + ' matches';
        return '<button type="button" class="rating-lab-performance-row' +
          (team.id === state.predictorTeam ? ' is-selected' : '') + '" data-predictor-team="' + escapeHtml(team.id) +
          '" aria-label="' + escapeHtml(label) + '"><span class="rating-lab-performance-name">' + escapeHtml(team.name) +
          '<small>' + team.matches + ' match' + (team.matches === 1 ? '' : 'es') + ' · ' + number(team.points, 2) +
          ' actual / ' + number(team.expected_score, 2) + ' expected</small></span><span class="rating-lab-performance-track" aria-hidden="true">' +
          '<span class="rating-lab-performance-zero"></span><span class="rating-lab-performance-bar ' +
          (positive ? 'is-outperformer' : 'is-underperformer') + '" style="--bar-size:' + size + '"></span></span>' +
          '<strong>' + escapeHtml(signedSurprise) + '</strong></button>';
      }).join('') + '</div></div><p class="rating-lab-performance-footnote">' + escapeHtml(model.surprise_method) + '</p>';
  }

  function renderCompletedPerformance(view) {
    elements.predictorMarket.hidden = true;
    elements.predictorMarket.innerHTML = '';
    var competition = view.competition;
    var model = competition.performance.models[state.predictorModel];
    var rows = model.participants;
    if (!state.predictorTeam || !rows.some(function (team) { return team.id === state.predictorTeam; })) {
      state.predictorTeam = rows[0].id;
    }
    setPerformanceColumns();
    elements.predictorState.textContent = 'Completed · performance replay ' + formatDate(model.first_result) + '–' +
      formatDate(model.last_result);
    elements.predictorMetrics.innerHTML = [
      ['Recorded results', number(model.results, 0)],
      ['Participants', number(rows.length, 0)],
      ['Published rating', model.rating_type === 'elo' ? 'Final Elo' : model.rating_type === 'glicko2_conservative_r_minus_2rd' ? 'Final rating−2RD' : 'Final μ−3σ']
    ].map(function (item) {
      return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
    }).join('');
    elements.predictorCaption.textContent = competitionTitle(competition) + ' · completed performance by ' +
      state.datasets[view.sport].models[state.predictorModel].label;
    renderPerformanceChart(rows, model, competition, view.sport);
    elements.predictorBody.innerHTML = rows.map(function (team) {
      var changeClass = team.change > 0 ? 'is-positive' : team.change < 0 ? 'is-negative' : '';
      var change = (team.change > 0 ? '+' : '') + number(team.change, 2);
      return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
        team.rank + '</td><th scope="row"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
        escapeHtml(team.id) + '">' + escapeHtml(team.name) + '</button></th><td>' + team.wins + '–' + team.draws + '–' +
        team.losses + '</td><td>' + number(team.start_score, 2) + '</td><td><strong>' + number(team.performance_rating, 2) +
        '</strong></td><td class="rating-lab-optional ' + changeClass + '">' + change +
        '</td><td class="rating-lab-optional">' + percent(team.score_rate) + '</td></tr>';
    }).join('');
    renderPerformanceDetail(rows.find(function (team) { return team.id === state.predictorTeam; }), model);
    elements.predictorMethod.innerHTML = escapeHtml(competition.performance.method) + ' Selected model parameters are the same ones shown in the protocol section. Snapshot: <code>' +
      escapeHtml(competition.snapshot_sha256.substring(0, 12)) + '</code>. <a href="' +
      escapeHtml(competition.source_url) + '">Open completed competition source</a>.';
  }

  function renderPredictor() {
    var view = predictorData();
    if (!view) return;
    elements.predictorPerformanceChart.hidden = true;
    elements.predictorPerformanceChart.innerHTML = '';
    var competition = view.competition;
    var model = view.model;
    var competitionFormat = competition.format || (model && model.teams ? 'round-robin league' : 'knockout cup');
    elements.predictorState.textContent = competition.status.charAt(0).toUpperCase() + competition.status.slice(1) +
      ' · ' + competitionFormat + ' · fixtures through ' + formatDate(competition.last_fixture);
    if (competition.status === 'complete' && competition.performance && competition.performance.models[state.predictorModel]) {
      renderCompletedPerformance(view);
      return;
    }
    if (competition.forecast_available === false || !model) {
      setPredictorColumns('knockout');
      elements.predictorMetrics.innerHTML = [
        ['Competition state', competition.status],
        ['Published fixtures', number(competition.total_matches, 0)],
        ['Title forecast', 'Withheld']
      ].map(function (item) {
        return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
      }).join('');
      elements.predictorCaption.textContent = competitionTitle(competition) + ' · waiting for forecastable structure';
      elements.predictorBody.innerHTML = '<tr><td colspan="5"><strong>Waiting for the knockout field.</strong><br>' +
        escapeHtml(competition.availability) + '</td></tr>';
      elements.predictorDetail.innerHTML = '<p>' + escapeHtml(competition.availability) + '</p>';
      elements.predictorMethod.innerHTML = escapeHtml(view.predictor.availability_rule) + ' <a href="' +
        escapeHtml(competition.source_url) + '">Open competition source</a>.';
      renderMarketComparison(view, []);
      return;
    }
    var isLeague = model.forecast_type === 'league' || Boolean(model.teams);
    var isStandings = model.forecast_type === 'standings';
    var rows = isLeague ? model.teams : model.participants;
    if (!state.predictorTeam || !rows.some(function (team) { return team.id === state.predictorTeam; })) {
      state.predictorTeam = rows[0].id;
    }
    setPredictorColumns(isStandings ? 'standings' : isLeague ? 'league' : 'knockout');
    if (!isLeague) {
      elements.predictorMetrics.innerHTML = [
        ['Competition state', model.current_stage],
        ['Published ties left', number(model.published_ties_remaining, 0)],
        ['Forecast sample', number(model.simulations, 0) + ' deterministic brackets']
      ].map(function (item) {
        return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
      }).join('');
      elements.predictorCaption.textContent = competitionTitle(competition) + ' · title forecast by ' +
        state.datasets[view.sport].models[state.predictorModel].label;
      elements.predictorBody.innerHTML = rows.map(function (team, index) {
        return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
          (index + 1) + '</td><th scope="row"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
          escapeHtml(team.id) + '">' + escapeHtml(team.name) + '</button></th><td>' + number(team.rating, 1) +
          '</td><td>' + probabilityCell(team.reach_next_stage) + '</td><td>' + probabilityCell(team.champion) + '</td></tr>';
      }).join('');
      renderKnockoutPredictorDetail(rows.find(function (team) { return team.id === state.predictorTeam; }), model);
      renderMarketComparison(view, rows);
      elements.predictorMethod.innerHTML = number(model.simulations, 0) + ' simulations. Published ties are locked. ' +
        escapeHtml(view.predictor.knockout_draw) + ' Fixed seed: <code>' + escapeHtml(String(model.seed)) +
        '</code>. Snapshot: <code>' + escapeHtml(competition.snapshot_sha256.substring(0, 12)) +
        '</code>. <a href="' + escapeHtml(competition.source_url) + '">Open competition source</a>.';
      return;
    }
    elements.predictorMetrics.innerHTML = [
      ['Competition state', model.completed_matches + ' of ' + competition.total_matches + ' played'],
      ['Next fixture', competition.next_fixture ? formatDate(competition.next_fixture) : 'Competition complete'],
      ['Forecast sample', number(model.simulations, 0) + (isStandings ? ' deterministic tournaments' : ' deterministic seasons')]
    ].map(function (item) {
      return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
    }).join('');
    elements.predictorCaption.textContent = competitionTitle(competition) + ' · projected by ' +
      state.datasets[view.sport].models[state.predictorModel].label;
    elements.predictorBody.innerHTML = model.teams.map(function (team, index) {
      return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
        (index + 1) + '</td><th scope="row"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
        escapeHtml(team.id) + '">' + escapeHtml(team.name) + '</button></th><td>' +
        (team.played ? team.current_rank : '—') + '</td><td><strong>' + number(team.expected_points, 1) +
        '</strong></td><td>' + probabilityCell(team.champion) + '</td><td class="rating-lab-optional">' +
        probabilityCell(isStandings ? team.podium : team.top_four) + '</td><td class="rating-lab-optional">' +
        probabilityCell(isStandings ? team.last_place : team.bottom_three) + '</td></tr>';
    }).join('');
    var selectedTeam = model.teams.find(function (team) { return team.id === state.predictorTeam; });
    if (isStandings) renderStandingsPredictorDetail(selectedTeam);
    else renderLeaguePredictorDetail(selectedTeam);
    renderMarketComparison(view, model.teams);
    elements.predictorMethod.innerHTML = escapeHtml(view.predictor.simulations_per_model) +
      ' simulations per model and competition. Fixed seed: <code>' + escapeHtml(String(model.seed)) +
      '</code>. Fixture snapshot: <code>' + escapeHtml(competition.snapshot_sha256.substring(0, 12)) +
      '</code>. ' + escapeHtml(competition.availability || '') + (competition.tie_break ? ' ' + escapeHtml(competition.tie_break) : '') +
      ' <a href="' + escapeHtml(competition.source_url) + '">Open fixture source</a>.';
  }

  function render() {
    updateFreshness();
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
    renderMatchup();
    renderProtocol();
    renderAudit();
    renderPredictor();
  }

  elements.sportTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-sport]');
    if (!button || button.dataset.sport === state.sport) return;
    state.sport = button.dataset.sport;
    state.selected = null;
    state.pinned = [];
    state.expanded = false;
    state.matchupA = null;
    state.matchupB = null;
    state.matchupVenue = 'neutral';
    setPressed(elements.sportTabs, 'sport', state.sport);
    populateCompetitions();
    render();
  });

  elements.modelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-model]');
    if (!button || button.dataset.model === state.model) return;
    state.model = button.dataset.model;
    state.expanded = false;
    setPressed(elements.modelTabs, 'model', state.model);
    render();
  });

  elements.matchupModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-matchup-model]');
    if (!button || button.dataset.matchupModel === state.model) return;
    state.model = button.dataset.matchupModel;
    state.expanded = false;
    setPressed(elements.modelTabs, 'model', state.model);
    render();
  });

  elements.matchupA.addEventListener('change', function () {
    var previous = state.matchupA;
    state.matchupA = elements.matchupA.value;
    if (state.matchupA === state.matchupB) state.matchupB = previous;
    renderMatchup();
  });

  elements.matchupB.addEventListener('change', function () {
    var previous = state.matchupB;
    state.matchupB = elements.matchupB.value;
    if (state.matchupA === state.matchupB) state.matchupA = previous;
    renderMatchup();
  });

  elements.matchupSwap.addEventListener('click', function () {
    var first = state.matchupA;
    state.matchupA = state.matchupB;
    state.matchupB = first;
    if (state.matchupVenue === 'a') state.matchupVenue = 'b';
    else if (state.matchupVenue === 'b') state.matchupVenue = 'a';
    renderMatchup();
  });

  elements.matchupVenue.addEventListener('change', function () {
    state.matchupVenue = elements.matchupVenue.value;
    renderMatchup();
  });

  elements.protocolSportTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-protocol-sport]');
    if (!button || button.dataset.protocolSport === state.sport) return;
    state.sport = button.dataset.protocolSport;
    state.selected = null;
    state.pinned = [];
    state.expanded = false;
    state.matchupA = null;
    state.matchupB = null;
    state.matchupVenue = 'neutral';
    setPressed(elements.sportTabs, 'sport', state.sport);
    populateCompetitions();
    render();
  });

  elements.protocolModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-protocol-model]');
    if (!button || button.dataset.protocolModel === state.model) return;
    state.model = button.dataset.protocolModel;
    state.expanded = false;
    setPressed(elements.modelTabs, 'model', state.model);
    render();
  });

  elements.competition.addEventListener('change', function () {
    state.competition = elements.competition.value;
    state.expanded = false;
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
  });

  elements.search.addEventListener('input', function () {
    state.query = elements.search.value;
    state.expanded = false;
    renderMetrics();
    renderMovers();
    renderTable();
  });

  elements.more.addEventListener('click', function () {
    state.expanded = true;
    renderTable();
  });

  elements.body.addEventListener('click', function (event) {
    var target = event.target.closest('[data-select], [data-row-select]');
    if (!target) return;
    state.selected = target.dataset.select || target.dataset.rowSelect;
    renderTable();
    renderDetail();
  });

  elements.movers.addEventListener('click', function (event) {
    var button = event.target.closest('[data-select]');
    if (!button) return;
    state.selected = button.dataset.select;
    renderTable();
    renderDetail();
  });

  elements.detail.addEventListener('click', function (event) {
    var pin = event.target.closest('[data-pin]');
    var unpin = event.target.closest('[data-unpin]');
    if (pin) {
      var index = state.pinned.indexOf(pin.dataset.pin);
      if (index === -1) {
        if (state.pinned.length === 2) state.pinned.shift();
        state.pinned.push(pin.dataset.pin);
      } else state.pinned.splice(index, 1);
      renderDetail();
    } else if (unpin) {
      state.pinned = state.pinned.filter(function (id) { return id !== unpin.dataset.unpin; });
      renderDetail();
    }
  });

  elements.detail.addEventListener('mouseover', function (event) {
    var histogram = event.target.closest('[data-histogram]');
    if (histogram) histogram.closest('.rating-lab-distribution').querySelector('.rating-lab-histogram-readout').textContent = histogram.dataset.histogram;
  });

  elements.detail.addEventListener('pointerdown', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface) return;
    surface.dataset.scrubbing = 'true';
    if (surface.setPointerCapture) surface.setPointerCapture(event.pointerId);
    surface.focus();
    scrubChart(event);
  });

  elements.detail.addEventListener('pointermove', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface) return;
    if (event.pointerType === 'mouse' || surface.dataset.scrubbing === 'true') scrubChart(event);
  });

  elements.detail.addEventListener('pointerup', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (surface) delete surface.dataset.scrubbing;
  });

  elements.detail.addEventListener('pointercancel', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (surface) delete surface.dataset.scrubbing;
  });

  elements.detail.addEventListener('keydown', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface || ['ArrowLeft', 'ArrowRight', 'Home', 'End'].indexOf(event.key) === -1) return;
    event.preventDefault();
    var chartWrap = surface.closest('.rating-lab-chart-wrap');
    var dates = chartEntries(chartWrap).map(function (entry) { return entry.date; }).filter(function (date, index, items) {
      return items.indexOf(date) === index;
    }).sort();
    var current = dates.indexOf(surface.dataset.activeDate);
    if (current < 0 && surface.dataset.activeDate) {
      var activeTime = new Date(surface.dataset.activeDate).getTime();
      current = dates.reduce(function (nearest, date, index) {
        return Math.abs(new Date(date).getTime() - activeTime) < Math.abs(new Date(dates[nearest]).getTime() - activeTime) ? index : nearest;
      }, 0);
    }
    if (event.key === 'Home') current = 0;
    else if (event.key === 'End') current = dates.length - 1;
    else if (event.key === 'ArrowLeft') current = current < 0 ? dates.length - 1 : Math.max(0, current - 1);
    else current = current < 0 ? 0 : Math.min(dates.length - 1, current + 1);
    selectChartDate(chartWrap, dates[current]);
  });

  elements.detail.addEventListener('focusin', function (event) {
    var histogram = event.target.closest('[data-histogram]');
    if (histogram) histogram.closest('.rating-lab-distribution').querySelector('.rating-lab-histogram-readout').textContent = histogram.dataset.histogram;
  });

  elements.predictorCompetition.addEventListener('change', function () {
    state.predictorCompetition = elements.predictorCompetition.value;
    state.predictorTeam = null;
    renderPredictor();
  });

  elements.predictorModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-predictor-model]');
    if (!button || button.dataset.predictorModel === state.predictorModel) return;
    state.predictorModel = button.dataset.predictorModel;
    state.predictorTeam = null;
    setPressed(elements.predictorModelTabs, 'predictorModel', state.predictorModel);
    renderPredictor();
  });

  elements.predictorBody.addEventListener('click', function (event) {
    var button = event.target.closest('[data-predictor-team]');
    if (!button) return;
    state.predictorTeam = button.dataset.predictorTeam;
    renderPredictor();
  });

  elements.predictorPerformanceChart.addEventListener('click', function (event) {
    var button = event.target.closest('[data-predictor-team]');
    if (!button) return;
    state.predictorTeam = button.dataset.predictorTeam;
    renderPredictor();
  });

  document.querySelector('.rating-lab-table thead').addEventListener('click', function (event) {
    var button = event.target.closest('[data-sort]');
    if (!button) return;
    if (state.sort === button.dataset.sort) state.direction *= -1;
    else {
      state.sort = button.dataset.sort;
      state.direction = button.dataset.sort === 'name' ? 1 : -1;
    }
    renderTable();
  });

  function revealLinkedMethod() {
    if (!window.location.hash) return;
    var target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
    var disclosure = target && target.closest('.rating-lab-disclosure');
    if (disclosure) disclosure.open = true;
  }

  window.addEventListener('hashchange', revealLinkedMethod);
  revealLinkedMethod();

  fetch(dataUrl('manifest.json'))
    .then(function (response) {
      if (!response.ok) throw new Error('The ratings manifest could not be loaded.');
      return response.json();
    })
    .then(function (manifest) {
      state.manifest = manifest;
      return Promise.all(sports.map(function (sport) {
        return fetch(dataUrl(sport + '.json')).then(function (response) {
          if (!response.ok) throw new Error(sport + ' ratings could not be loaded.');
          return response.json();
        }).then(function (payload) { state.datasets[sport] = payload; });
      }));
    })
    .then(function () {
      var competitions = predictorCompetitions();
      elements.predictorCompetition.innerHTML = competitions.map(function (view) {
        var competition = view.competition;
        var stateLabel = {
          live: 'Live forecast',
          scheduled: 'Upcoming forecast',
          complete: 'Completed performance',
          'waiting for draw': 'Waiting for field'
        }[competition.status] || competition.status;
        var kind = view.sport === 'chess' ? 'Chess tournament' :
          (competition.format === 'round-robin league' || (competition.models.elo && competition.models.elo.forecast_type === 'league')) ? 'League' :
          view.sport === 'national-football' ? 'National tournament' : 'Club cup';
        return '<option value="' + escapeHtml(competition.id) + '">' +
          escapeHtml(stateLabel + ' · ' + kind + ' · ' + competitionTitle(competition)) + '</option>';
      }).join('');
      state.predictorCompetition = competitions[0].competition.id;
      populateCompetitions();
      render();
    })
    .catch(function (error) {
      elements.freshness.hidden = true;
      elements.error.hidden = false;
      elements.error.textContent = error.message + ' Please try again later.';
    });
}());
