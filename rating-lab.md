---
layout: page
title: Rating Lab
permalink: /rating-lab/
description: Live alternative ratings for tennis, club and national-team football, and chess, tested against real match outcomes.
---

<div class="rating-lab" data-data-root="{{ '/assets/data/rating-lab' | relative_url }}">
  <header class="rating-lab-hero">
    <p class="rating-lab-kicker">Live, reproducible sports ratings</p>
    <h1>Across sports. Three ways to measure strength.</h1>
    <p class="rating-lab-deck">Explore current Elo, Gaussian TrueSkill, and robust heavy-tail rankings built from real match results. Every prediction is scored before its result is used to update the model.</p>
    <p class="rating-lab-hero-link"><a href="#predictor">Forecast the 2026–27 competitions ↓</a></p>
    <div class="rating-lab-freshness-strip" id="rating-lab-freshness" role="status" aria-live="polite">Loading the latest ratings…</div>
    <p class="rating-lab-generation" id="rating-lab-generation"></p>
  </header>

  <noscript><p class="rating-lab-notice">This interactive leaderboard requires JavaScript.</p></noscript>
  <div id="rating-lab-error" class="rating-lab-notice rating-lab-notice-error" role="alert" hidden></div>

  <section class="rating-lab-explorer" aria-labelledby="leaderboard-heading">
    <div class="rating-lab-section-heading">
      <h2 id="leaderboard-heading">Leaderboard</h2>
      <p id="leaderboard-context">Current ratings and one-step-ahead evidence</p>
    </div>
    <div class="rating-lab-toolbar">
      <div class="rating-lab-control-group" aria-label="Sport">
        <span class="rating-lab-control-label">Sport</span>
        <div class="rating-lab-segmented" id="sport-tabs">
          <button type="button" data-sport="tennis" aria-pressed="true">Tennis</button>
          <button type="button" data-sport="football" aria-pressed="false">Clubs</button>
          <button type="button" data-sport="national-football" aria-pressed="false">Nations</button>
          <button type="button" data-sport="chess" aria-pressed="false">Chess</button>
        </div>
      </div>
      <div class="rating-lab-control-group" aria-label="Rating model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="model-tabs">
          <button type="button" data-model="elo" aria-pressed="true">Elo</button>
          <button type="button" data-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
      <label class="rating-lab-field">
        <span>Competition</span>
        <select id="competition-filter"><option value="">All competitions</option></select>
      </label>
      <label class="rating-lab-field rating-lab-search">
        <span>Search</span>
        <input id="rating-search" type="search" autocomplete="off" placeholder="Player or team">
      </label>
    </div>

    <div class="rating-lab-metrics" id="rating-metrics" aria-label="Out-of-sample model accuracy"></div>
    <div class="rating-lab-movers" id="rating-movers" aria-label="Biggest 30-day rating movers"></div>

    <div class="rating-lab-grid">
      <div class="rating-lab-table-wrap">
        <table class="rating-lab-table">
          <caption id="ranking-caption">Current rankings</caption>
          <thead>
            <tr>
              <th scope="col"><button type="button" data-sort="rank">Rank</button></th>
              <th scope="col"><button type="button" data-sort="name">Player or team</button></th>
              <th scope="col" class="rating-lab-trend-column">Trend</th>
              <th scope="col"><button type="button" data-sort="score">Rating</button></th>
              <th scope="col" class="rating-lab-optional"><button type="button" data-sort="sigma">Uncertainty</button></th>
              <th scope="col"><button type="button" data-sort="change30">30-day change</button></th>
              <th scope="col" class="rating-lab-optional"><button type="button" data-sort="recent_matches">Recent</button></th>
            </tr>
          </thead>
          <tbody id="ranking-body"></tbody>
        </table>
        <p id="ranking-empty" class="rating-lab-empty" hidden>No eligible competitors match these filters.</p>
        <button type="button" id="ranking-more" class="rating-lab-more" hidden>Show all competitors</button>
      </div>

      <aside class="rating-lab-detail" id="rating-detail" aria-live="polite">
        <p class="rating-lab-detail-placeholder">Choose a row to inspect history, compare models, and pin competitors.</p>
      </aside>
    </div>
  </section>

  <section class="rating-lab-predictor" id="predictor" aria-labelledby="predictor-heading">
    <p class="rating-lab-kicker">Live competition forecast</p>
    <h2 id="predictor-heading">Tournament predictor</h2>
    <p class="rating-lab-predictor-intro">Predict leagues, club cups, and national-team tournaments from their actual published state. League tables keep played results and simulate the remaining calendar; knockout forecasts preserve published ties and never invent a title probability before the field exists.</p>
    <p class="rating-lab-audit-note">Current forecastable structures: five club leagues, football-data.org club and national knockout fields, and active elite Lichess round-robin events. The ATP results source does not publish a usable unauthenticated live draw, so tennis title odds are not reconstructed from completed matches alone.</p>

    <div class="rating-lab-predictor-toolbar">
      <label class="rating-lab-field">
        <span>Competition</span>
        <select id="predictor-competition" aria-label="Competition to predict"></select>
      </label>
      <div class="rating-lab-control-group" aria-label="Prediction model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="predictor-model-tabs">
          <button type="button" data-predictor-model="elo" aria-pressed="true">Elo</button>
          <button type="button" data-predictor-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-predictor-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
      <div class="rating-lab-predictor-state" id="predictor-state" role="status" aria-live="polite"></div>
    </div>

    <div class="rating-lab-predictor-metrics" id="predictor-metrics" aria-label="Competition simulation state"></div>

    <div class="rating-lab-predictor-grid">
      <div class="rating-lab-table-wrap">
        <table class="rating-lab-table rating-lab-predictor-table">
          <caption id="predictor-caption">Projected final table</caption>
          <thead>
            <tr>
              <th scope="col" id="predictor-col-rank">Projected</th>
              <th scope="col" id="predictor-col-team">Team</th>
              <th scope="col" id="predictor-col-now">Now</th>
              <th scope="col" id="predictor-col-value">Expected pts</th>
              <th scope="col" id="predictor-col-title">Title</th>
              <th scope="col" id="predictor-col-secondary" class="rating-lab-optional">Top four</th>
              <th scope="col" id="predictor-col-tertiary" class="rating-lab-optional">Bottom three</th>
            </tr>
          </thead>
          <tbody id="predictor-body"></tbody>
        </table>
      </div>
      <aside class="rating-lab-detail rating-lab-predictor-detail" id="predictor-detail" aria-live="polite">
        <p class="rating-lab-detail-placeholder">Choose a team to inspect its full finishing-position distribution.</p>
      </aside>
    </div>

    <details class="rating-lab-predictor-method">
      <summary>How the forecast works</summary>
      <p id="predictor-method-copy"></p>
      <p>Every forecast uses the leaderboard’s chronological rating state. Leagues lock actual points and goal difference, then sample future win/draw/loss outcomes. Cups lock every published result and tie. When a later draw is not yet public, survivors are uniformly re-drawn; the interface states that assumption. If no knockout field is public, the title forecast is withheld.</p>
    </details>
  </section>

  <section class="rating-lab-method" id="methodology">
    <p class="rating-lab-kicker">Methodology</p>
    <h2>What changes—and what does not</h2>
    <div class="rating-lab-method-grid">
      <article>
        <h3>Elo</h3>
        <p>A direct online update around a logistic win-probability curve. Football includes home advantage, club football has seasonal mean reversion, and draws count as half a win.</p>
      </article>
      <article>
        <h3>Gaussian TrueSkill</h3>
        <p>Each competitor has a skill mean and uncertainty. Rankings use the conservative score <span class="rating-lab-formula">μ − 3σ</span>, rewarding evidence as well as estimated strength.</p>
      </article>
      <article>
        <h3>Robust TrueSkill</h3>
        <p>The same uncertain-skill framework uses Student-t performance noise. Its heavy tails expect more upsets, so one surprising result moves the ranking less.</p>
      </article>
    </div>
    <p class="rating-lab-explainer">Turning a Gaussian rating into a log-normal or Pareto-looking published scale can change the histogram without changing anyone’s rank. A genuinely different ranking requires a different performance model or update rule.</p>
  </section>

  <section class="rating-lab-protocol" id="protocol" aria-labelledby="protocol-heading">
    <p class="rating-lab-kicker">Protocol transparency</p>
    <h2 id="protocol-heading">From one public result to one published rank</h2>
    <p class="rating-lab-protocol-intro">Choose a cohort and model to see the exact operational rules. These are descriptions of the running code—not a simplified alternative methodology.</p>

    <div class="rating-lab-protocol-toolbar">
      <div class="rating-lab-control-group" aria-label="Protocol sport">
        <span class="rating-lab-control-label">Cohort</span>
        <div class="rating-lab-segmented" id="protocol-sport-tabs">
          <button type="button" data-protocol-sport="tennis" aria-pressed="true">Tennis</button>
          <button type="button" data-protocol-sport="football" aria-pressed="false">Clubs</button>
          <button type="button" data-protocol-sport="national-football" aria-pressed="false">Nations</button>
          <button type="button" data-protocol-sport="chess" aria-pressed="false">Chess</button>
        </div>
      </div>
      <div class="rating-lab-control-group" aria-label="Protocol model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="protocol-model-tabs">
          <button type="button" data-protocol-model="elo" aria-pressed="true">Elo</button>
          <button type="button" data-protocol-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-protocol-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
    </div>

    <div id="rating-protocol" aria-live="polite"></div>

    <details class="rating-lab-limitations">
      <summary>Known limitations and deliberate simplifications</summary>
      <ul>
        <li>Ratings are result-only: score margin, tennis surface, line-ups, injuries, time controls, and player age are not model inputs.</li>
        <li>Draws use an actual score of 0.5. Published log loss and Brier score evaluate expected score, not a separate three-class win/draw/loss forecast.</li>
        <li>Multiple results on the same date are replayed in the published stable identifier order because exact start times are not consistently available.</li>
        <li>The public JSON publishes at most the top 500 eligible entities per model; it is not a complete registry of every entity seen in the source archive.</li>
        <li>Model selection tests a small declared parameter grid. It does not prove that the selected candidate is globally optimal.</li>
        <li>Cup forecasts do not guess unpublished entrants or qualification paths. Once a knockout field exists, published ties are fixed; later unpublished draws use a uniform redraw without seeding, association, or country restrictions.</li>
      </ul>
    </details>
  </section>

  <section class="rating-lab-audit" id="reproducibility" aria-labelledby="audit-heading">
    <p class="rating-lab-kicker">Open methodology</p>
    <h2 id="audit-heading">Inspect every assumption. Reproduce every table.</h2>
    <p class="rating-lab-audit-intro">The browser only reads static JSON. All ratings are rebuilt from public results by deterministic, chronological Python replay; there is no private ranking service or hidden model.</p>

    <div class="rating-lab-equations">
      <article>
        <h3>Elo probability and update</h3>
        <p class="rating-lab-equation" aria-label="p A equals one divided by one plus ten to the power negative rating A plus home advantage minus rating B divided by 400">p<sub>A</sub> = 1 / (1 + 10<sup>−(R<sub>A</sub> + H − R<sub>B</sub>)/400</sup>)</p>
        <p class="rating-lab-equation" aria-label="new rating A equals rating A plus K times actual score minus predicted probability">R′<sub>A</sub> = R<sub>A</sub> + K(s<sub>A</sub> − p<sub>A</sub>)</p>
      </article>
      <article>
        <h3>Uncertain skill</h3>
        <p class="rating-lab-equation">s<sub>i</sub> ∼ N(μ<sub>i</sub>, σ<sub>i</sub><sup>2</sup>)</p>
        <p>Gaussian performance noise uses <span class="rating-lab-formula">ε ∼ N(0, β²)</span>. Robust performance uses <span class="rating-lab-formula">ε ∼ t<sub>ν=1</sub>(0, β)</span>, the Cauchy case. Both publish <span class="rating-lab-formula">μ − 3σ</span>.</p>
      </article>
      <article>
        <h3>Numerical update</h3>
        <p>The result likelihood—including the draw interval <span class="rating-lab-formula">± margin</span>—is integrated over the skill-difference belief with a fixed 20-node Gauss–Hermite rule, then moment-matched back to Gaussian competitor beliefs.</p>
      </article>
    </div>

    <div class="rating-lab-split">
      <h3>No look-ahead parameter tuning</h3>
      <ol>
        <li><strong>Warm-up:</strong> results older than 24 months establish prior rating state.</li>
        <li><strong>Validation:</strong> months 24–12 choose the candidate with lowest chronological log loss.</li>
        <li><strong>Evaluation:</strong> the latest 12 months remain untouched until one-step-ahead scoring.</li>
        <li><strong>Publication:</strong> the selected parameters replay the complete declared data window in the stable sort order.</li>
      </ol>
    </div>

    <div class="rating-lab-audit-grid">
      <article>
        <h3>Selected parameters</h3>
        <p id="rating-eligibility">Loading cohort rules…</p>
        <div class="rating-lab-table-wrap">
          <table class="rating-lab-parameter-table">
            <caption>Parameters selected for the current cohort</caption>
            <thead><tr><th scope="col">Model</th><th scope="col">Selected values</th><th scope="col">Candidates tested</th></tr></thead>
            <tbody id="rating-parameter-body"></tbody>
          </table>
        </div>
      </article>
      <article>
        <h3>Build audit record</h3>
        <dl id="rating-audit-record"><div><dt>Status</dt><dd>Loading…</dd></div></dl>
        <div class="rating-lab-downloads">
          <a id="rating-data-download" href="{{ '/assets/data/rating-lab/tennis.json' | relative_url }}" download>Current cohort JSON</a>
          <a href="{{ '/assets/data/rating-lab/manifest.json' | relative_url }}" download>Build manifest</a>
          <a href="{{ '/assets/data/rating-lab/schema.json' | relative_url }}" download>JSON schema</a>
          <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/tree/main/rating_lab">Model source</a>
        </div>
      </article>
    </div>

    <h3>Exact local reproduction</h3>
    <pre class="rating-lab-code"><code>git clone https://github.com/kieranmcshane/kieranmcshane.github.io.git
cd kieranmcshane.github.io
RATING_LAB_CACHE_DIR=.cache/rating-lab python3 scripts/refresh_ratings.py
python3 -m unittest discover -s tests -v</code></pre>
    <p class="rating-lab-audit-note">A <code>FOOTBALL_DATA_TOKEN</code> enables the primary club feed; without it, the documented CC0 OpenFootball fallback is used. Results are deduplicated and sorted by date, competitor IDs, competition, and score. The source snapshot hash is published when the source is a single file. Generated files contain no credentials.</p>
  </section>

  <section class="rating-lab-sources" aria-labelledby="sources-heading">
    <p class="rating-lab-kicker">Open data</p>
    <h2 id="sources-heading">Sources and licences</h2>
    <ul id="rating-source-list">
      <li><a href="https://github.com/msolonskyi/ManTennisData">ManTennisData</a> — ATP-derived singles results, MIT.</li>
      <li><a href="https://www.football-data.org/">football-data.org</a> — five major European leagues plus published Champions League, FIFA World Cup, and European Championship stages.</li>
      <li><a href="https://github.com/openfootball">OpenFootball</a> — current league fixtures plus credential-free Champions League, World Cup, and Euro structures, CC0 1.0.</li>
      <li><a href="https://github.com/martj42/international_results">International football results</a> — men’s full internationals, CC0 1.0.</li>
      <li><a href="https://database.lichess.org/#broadcasts">Lichess official broadcasts</a> — elite OTB games, CC BY-SA 4.0.</li>
    </ul>
    <p>Rankings are independent statistical estimates, not official tour, league, federation, or Lichess ratings. They are informational and are not betting advice.</p>
  </section>
</div>

<script defer src="{{ '/assets/js/rating-lab.js' | relative_url }}?v={{ site.github.build_revision }}"></script>
