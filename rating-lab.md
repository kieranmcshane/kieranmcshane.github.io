---
layout: page
title: Rating Lab
permalink: /rating-lab/
description: Live alternative ratings for tennis, club and national-team football, and chess, tested against real match outcomes.
---

<div class="rating-lab" data-data-root="{{ '/assets/data/rating-lab' | relative_url }}" data-flag-root="{{ '/assets/vendor/flag-icons/4x3' | relative_url }}">
  <header class="rating-lab-hero">
    <p class="rating-lab-kicker">Live · reproducible · scored out-of-sample</p>
    <h1><span class="rating-lab-title-desktop">Across sports. Four ways to measure strength.</span><span class="rating-lab-title-mobile">Live ratings across sports.</span></h1>
    <p class="rating-lab-deck"><span class="rating-lab-deck-desktop">Compare Elo, Glicko-2, Gaussian, and robust ratings across tennis, football, and chess. Every forecast is scored before its result updates the model.</span><span class="rating-lab-deck-mobile">Four outcome-tested models for tennis, football, and chess.</span></p>
    <p class="rating-lab-hero-link"><a href="#predictor">Forecast current competitions ↓</a></p>
    <div class="rating-lab-freshness-strip" id="rating-lab-freshness" role="status" aria-live="polite">Loading the latest ratings…</div>
    <p class="rating-lab-generation" id="rating-lab-generation"></p>
  </header>

  <nav class="rating-lab-local-nav" aria-label="Rating Lab sections">
    <a href="#leaderboard-heading" aria-current="location" aria-label="Rankings"><strong>01</strong><span data-mobile-label="Rankings">Rankings</span></a>
    <a href="#matchup" aria-label="A vs B"><strong>02</strong><span data-mobile-label="A vs B">A vs B</span></a>
    <a href="#predictor" aria-label="Competition forecasts"><strong>03</strong><span data-mobile-label="Forecasts">Competitions</span></a>
    <a class="is-external" href="{{ '/rating-lab/players/' | relative_url }}" aria-label="Player ratings"><strong>04</strong><span data-mobile-label="Players">Players ↗</span></a>
    <a href="#research" aria-label="Methods and data"><strong>05</strong><span data-mobile-label="Methods">Methods & data</span></a>
  </nav>

  <noscript>This interactive leaderboard requires JavaScript.</noscript>
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
      <button type="button" class="rating-lab-filter-trigger" id="rating-mobile-filters" aria-haspopup="dialog" aria-controls="rating-mobile-filter-sheet">
        <span><strong id="rating-mobile-model-label">Elo</strong><small>scored out-of-sample</small></span>
        <span>Filters</span>
      </button>
      <div class="rating-lab-control-group rating-lab-desktop-filter" aria-label="Rating model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="model-tabs">
          <button type="button" data-model="elo" aria-pressed="true">Elo</button>
          <button type="button" data-model="glicko2" aria-pressed="false">Glicko-2</button>
          <button type="button" data-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
      <label class="rating-lab-field rating-lab-desktop-filter">
        <span>Competition</span>
        <select id="competition-filter"><option value="">All competitions</option></select>
      </label>
      <label class="rating-lab-field rating-lab-search">
        <span>Search</span>
        <input id="rating-search" type="search" autocomplete="off" placeholder="Player or team">
      </label>
    </div>

    <dialog class="rating-lab-filter-sheet" id="rating-mobile-filter-sheet" aria-labelledby="rating-mobile-filter-title">
      <div class="rating-lab-filter-sheet-handle" aria-hidden="true"></div>
      <div class="rating-lab-filter-sheet-heading">
        <div><p class="rating-lab-kicker">Leaderboard view</p><h3 id="rating-mobile-filter-title">Filters</h3></div>
        <button type="button" id="rating-mobile-filter-close" aria-label="Close filters">×</button>
      </div>
      <div class="rating-lab-control-group" aria-label="Mobile rating model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="rating-mobile-model-tabs">
          <button type="button" data-mobile-model="elo" aria-pressed="true">Elo</button>
          <button type="button" data-mobile-model="glicko2" aria-pressed="false">Glicko-2</button>
          <button type="button" data-mobile-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-mobile-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
      <label class="rating-lab-field">
        <span>Competition</span>
        <select id="rating-mobile-competition"><option value="">All competitions</option></select>
      </label>
      <label class="rating-lab-filter-provisional" id="rating-mobile-provisional-control" hidden>
        <input id="rating-mobile-include-provisional" type="checkbox">
        <span>Include provisional (<strong id="rating-mobile-provisional-count">0</strong>)</span>
      </label>
      <button type="button" class="rating-lab-filter-apply" id="rating-mobile-filter-apply">Apply view</button>
    </dialog>

    <details class="rating-lab-metrics-disclosure" open>
      <summary>Model accuracy</summary>
      <div class="rating-lab-metrics" id="rating-metrics" aria-label="Out-of-sample model accuracy"></div>
    </details>
    <details class="rating-lab-movers-disclosure" open>
      <summary>30-day movers</summary>
      <div class="rating-lab-movers" id="rating-movers" aria-label="Biggest 30-day rating movers"></div>
    </details>

    <div class="rating-lab-provisional-control" id="rating-provisional-control" hidden>
      <label>
        <input id="rating-include-provisional" type="checkbox" aria-describedby="rating-provisional-note">
        <span>Include provisional (<strong id="rating-provisional-count">0</strong>)</span>
      </label>
      <p id="rating-provisional-note">Provisional football Elo entries have too little established-network evidence for the default ranking.</p>
    </div>

    <div class="rating-lab-grid">
      <div class="rating-lab-table-wrap">
        <table class="rating-lab-table" id="ranking-table">
          <caption id="ranking-caption">Current rankings</caption>
          <thead>
            <tr>
              <th scope="col"><button type="button" data-sort="rank">Rank</button></th>
              <th scope="col"><button type="button" data-sort="name">Player or team</button></th>
              <th scope="col" class="rating-lab-trend-column">Trend</th>
              <th scope="col" class="rating-lab-rating-column"><button type="button" data-sort="score">Rating</button></th>
              <th scope="col" class="rating-lab-uncertainty-column"><button type="button" data-sort="sigma">Uncertainty</button></th>
              <th scope="col" class="rating-lab-change-column"><button type="button" data-sort="change30">30-day change</button></th>
              <th scope="col" class="rating-lab-recent-column"><button type="button" data-sort="recent_matches">Recent</button></th>
            </tr>
          </thead>
          <tbody id="ranking-body"></tbody>
        </table>
        <p id="ranking-empty" class="rating-lab-empty" hidden>No eligible competitors match these filters.</p>
        <button type="button" id="ranking-more" class="rating-lab-more" hidden>Show all competitors</button>
      </div>

      <aside class="rating-lab-detail" id="rating-detail" aria-live="polite" hidden></aside>
    </div>
  </section>

  <section class="rating-lab-matchup" id="matchup" aria-labelledby="matchup-heading">
    <p class="rating-lab-kicker">Single-event forecast</p>
    <h2 id="matchup-heading">A vs B probability</h2>
    <p class="rating-lab-matchup-intro">Compare two published competitors with the selected model and relevant tennis surface, football venue, or chess color.</p>

    <div class="rating-lab-matchup-toolbar">
      <label class="rating-lab-field">
        <span>Competitor A</span>
        <select id="matchup-a" aria-label="First competitor" autocomplete="off"></select>
      </label>
      <button type="button" class="rating-lab-matchup-swap" id="matchup-swap" aria-label="Swap competitors">⇄<span>Swap</span></button>
      <label class="rating-lab-field">
        <span>Competitor B</span>
        <select id="matchup-b" aria-label="Second competitor" autocomplete="off"></select>
      </label>
      <label class="rating-lab-field">
        <span id="matchup-venue-label">Venue</span>
        <select id="matchup-venue" aria-labelledby="matchup-venue-label" autocomplete="off"></select>
      </label>
      <div class="rating-lab-control-group" aria-label="Matchup prediction model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="matchup-model-tabs">
          <button type="button" data-matchup-model="elo" aria-pressed="true">Elo</button>
          <button type="button" data-matchup-model="glicko2" aria-pressed="false">Glicko-2</button>
          <button type="button" data-matchup-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-matchup-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
    </div>

    <div class="rating-lab-matchup-result" id="matchup-result" aria-live="polite">
      <p>Loading current rating state…</p>
    </div>
  </section>

  <section class="rating-lab-predictor" id="predictor" aria-labelledby="predictor-heading">
    <p class="rating-lab-kicker">Live forecast · completed performance</p>
    <h2 id="predictor-heading">Competition forecast and performance</h2>
    <p class="rating-lab-predictor-intro">Forecast live and scheduled competitions from current ratings, with confidently matched Polymarket and Kalshi snapshots shown as separate external benchmarks. Completed events switch to protocol performance ratings.</p>
    <details class="rating-lab-coverage-note">
      <summary>Coverage and forecast limits</summary>
      <p class="rating-lab-audit-note">Current forward forecasts cover five club leagues, the live UEFA Champions League qualifying round, public club and national knockout fields, and active elite Lichess round-robin events. Qualifying probabilities stop at the next published stage; they are not mislabeled as title odds. Completed sourced competitions switch to protocol performance ratings. The ATP results source does not publish a usable unauthenticated live draw, so tennis title odds are not reconstructed from completed matches alone.</p>
    </details>

    <div class="rating-lab-predictor-toolbar">
      <label class="rating-lab-field">
        <span>Competition</span>
        <select id="predictor-competition" aria-label="Competition to predict" autocomplete="off"></select>
      </label>
      <div class="rating-lab-control-group" aria-label="Prediction model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="predictor-model-tabs">
          <button type="button" data-predictor-model="elo" aria-pressed="true">Elo</button>
          <button type="button" data-predictor-model="glicko2" aria-pressed="false">Glicko-2</button>
          <button type="button" data-predictor-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-predictor-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
      <div class="rating-lab-predictor-state" id="predictor-state" role="status" aria-live="polite"></div>
    </div>

    <div class="rating-lab-predictor-metrics" id="predictor-metrics" aria-label="Competition simulation state"></div>
    <div class="rating-lab-market" id="predictor-market" aria-live="polite" hidden></div>
    <section class="rating-lab-performance-chart" id="predictor-performance-chart" aria-labelledby="predictor-performance-title" hidden></section>

    <div class="rating-lab-predictor-grid">
      <div class="rating-lab-table-wrap">
        <table class="rating-lab-table rating-lab-predictor-table">
          <caption id="predictor-caption">Projected final table</caption>
          <thead>
            <tr>
              <th scope="col" id="predictor-col-rank" class="rating-lab-rank">Projected</th>
              <th scope="col" id="predictor-col-team" class="rating-lab-predictor-entity">Team</th>
              <th scope="col" id="predictor-col-now" class="rating-lab-predictor-now">Now</th>
              <th scope="col" id="predictor-col-value" class="rating-lab-predictor-value">Expected pts</th>
              <th scope="col" id="predictor-col-title" class="rating-lab-predictor-title">Title</th>
              <th scope="col" id="predictor-col-secondary" class="rating-lab-optional">Top four</th>
              <th scope="col" id="predictor-col-tertiary" class="rating-lab-optional">Bottom three</th>
            </tr>
          </thead>
          <tbody id="predictor-body"></tbody>
        </table>
        <p class="rating-lab-predictor-mobile-hint">Tap a team for title, top-four, relegation, and its full finishing-position distribution.</p>
      </div>
      <aside class="rating-lab-detail rating-lab-predictor-detail" id="predictor-detail" aria-live="polite">
        <p class="rating-lab-detail-placeholder">Choose a team to inspect its full finishing-position distribution.</p>
      </aside>
    </div>

    <details class="rating-lab-predictor-method">
      <summary>How this competition view is calculated</summary>
      <p id="predictor-method-copy"></p>
      <p>Every forecast uses the leaderboard’s chronological rating state. Leagues lock actual points and goal difference, then sample future win/draw/loss outcomes. Cups lock every published result and tie. When a later draw is not yet public, survivors are uniformly re-drawn; the interface states that assumption. If no knockout field is public, the title forecast is withheld.</p>
      <p>For a completed competition, the anchored Performance Rating varies one participant’s rating while every opponent stays fixed at the selected protocol’s pre-event belief, then solves <span class="rating-lab-formula">Σp<sub>m</sub>(R<sub>perf</sub>) = Σs<sub>m</sub></span>. A separate reset rank starts everybody from the neutral prior and replays only the event. Chronological surprise remains <span class="rating-lab-formula">Z = Σ(s<sub>m</sub> − p<sub>m</sub>) / √Σp<sub>m</sub>(1−p<sub>m</sub>)</span>, where a win scores 1, a draw 0.5, and a loss 0.</p>
    </details>
  </section>

  <section class="rating-lab-research" id="research" aria-labelledby="research-heading">
    <p class="rating-lab-kicker">How it works</p>
    <h2 id="research-heading">The details, when you want them.</h2>
    <p class="rating-lab-research-intro">Rating Lab is a side project, but its forecasts should still be inspectable. Open a panel to see the assumptions, parameters, data sources, licences, and exact reproduction steps.</p>
    <details class="rating-lab-media-policy">
      <summary>Identity image and flag policy</summary>
      <p class="rating-lab-explainer"><strong>Identity images are data, too:</strong> club and federation crests are used only when football-data.org supplies them. Tennis and chess portraits are linked through exact ATP or FIDE identifiers to Wikimedia Commons—never guessed from a name—and appear only with a recorded file page, licence, and attribution. Small flags are pinned MIT-licensed SVG assets selected only from the source country or federation code—never operating-system emoji. Unknown codes remain blank rather than being inferred from a name. The inspector exposes image details. Images and flags never enter a rating or forecast; initials remain the final fallback.</p>
    </details>
    <div class="rating-lab-research-links" aria-label="Downloads and code">
      <a href="{{ '/assets/data/rating-lab/manifest.json' | relative_url }}" download>Build manifest</a>
      <a href="{{ '/assets/data/rating-lab/schema.json' | relative_url }}" download>JSON schema</a>
      <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/tree/main/rating_lab">Model source</a>
    </div>

  <details class="rating-lab-disclosure">
    <summary><span>Protocol overview</span><strong>How the four rating models differ</strong></summary>
  <section class="rating-lab-method" id="methodology">
    <p class="rating-lab-kicker">Methodology</p>
    <h2>What changes—and what does not</h2>
    <div class="rating-lab-method-grid">
      <article>
        <h3>Elo</h3>
        <p>A direct online update around a logistic win-probability curve. Football includes home advantage, chess includes White advantage, tennis blends global and surface ratings, club football has seasonal mean reversion, and draws count as half a win. Since Elo has no uncertainty estimate, football clubs with fewer than 10 covered results or no path into the main connected result network remain visibly provisional and are ordered after established clubs; their raw ratings still drive forecasts.</p>
      </article>
      <article>
        <h3>Glicko-2</h3>
        <p>A head-to-head rating with rating deviation and volatility. Calendar-day batches avoid within-day ordering, inactivity increases RD, and rankings use <span class="rating-lab-formula">rating − 2RD</span>.</p>
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
    <p class="rating-lab-explainer"><strong>Why this is not labelled TrueSkill 2:</strong> TrueSkill 2’s published Halo improvement uses experience, squads, kills, quitting, and cross-mode skill. These sports sources do not contain equivalent observations. Calling a result-only replay “TrueSkill 2” would not be reproducible. Core TrueSkill does not need those features: given reliable lineups, it can infer player skill from team outcomes alone.</p>
    <p class="rating-lab-explainer">Turning a Gaussian rating into a log-normal or Pareto-looking published scale can change the histogram without changing anyone’s rank. A genuinely different ranking requires a different performance model or update rule.</p>
  </section>
  </details>

  <details class="rating-lab-disclosure">
    <summary><span>Historical cohorts live</span><strong>Individual footballer contribution</strong></summary>
  <section class="rating-lab-contribution" id="player-contribution" aria-labelledby="contribution-heading">
    <p class="rating-lab-kicker">Team result → player contribution</p>
    <h2 id="contribution-heading">Published where the lineups are complete</h2>
    <p class="rating-lab-contribution-intro">Live club and national-team rankings still treat each team as one competitor. A separate historical player lab now publishes individual estimates for complete declared StatsBomb seasons: Liga F 2023/24 and the FA Women’s Super League 2023/24.</p>
    <p><a class="rating-lab-contribution-cta" href="{{ '/rating-lab/players/' | relative_url }}">Open historical player ratings →</a></p>

    <div class="rating-lab-contribution-methods">
      <article>
        <p class="rating-lab-method-tag">Win, draw or loss</p>
        <h3>Lineup TrueSkill</h3>
        <p>Each player has an uncertain latent skill. A team performance is the minutes-weighted sum of its players’ performances; the observed team result updates every player while accounting for teammates and opponents.</p>
        <p class="rating-lab-equation">team performance = Σ minutes share × player performance</p>
      </article>
      <article>
        <p class="rating-lab-method-tag">Score differential</p>
        <h3>RAPM</h3>
        <p>A regularized regression explains goal difference from who was playing for and against each side. Ridge shrinkage limits unstable estimates when players repeatedly appear in the same combinations.</p>
        <p class="rating-lab-equation">goal difference = player effects + home effect + error</p>
      </article>
    </div>

    <div class="rating-lab-readiness" role="region" aria-labelledby="readiness-heading">
      <div class="rating-lab-readiness-heading">
        <div>
          <p class="rating-lab-method-tag">Publication gate</p>
          <h3 id="readiness-heading">Player leaderboard status</h3>
        </div>
        <span class="rating-lab-status-ready">Historical cohorts live</span>
      </div>
      <p>Every published historical cohort passes the checks below. Men’s club samples and the live five-league feed remain excluded because their open lineup coverage is incomplete.</p>
      <div class="rating-lab-table-wrap">
        <table class="rating-lab-readiness-table">
          <caption>Minimum data and reproducibility requirements for publishing footballer ratings</caption>
          <thead><tr><th scope="col">Gate</th><th scope="col">Required standard</th><th scope="col">Current evidence</th></tr></thead>
          <tbody>
            <tr><th scope="row">Match results</th><td>Complete declared competitions</td><td><span class="is-ready">Ready</span></td></tr>
            <tr><th scope="row">Stable player IDs</th><td>One identity within the declared cohort</td><td><span class="is-ready">Passed</span></td></tr>
            <tr><th scope="row">Starting lineups</th><td>At least 95% of eligible matches</td><td><span class="is-ready">100%</span></td></tr>
            <tr><th scope="row">Player minutes</th><td>At least 95% of players used</td><td><span class="is-ready">100%</span></td></tr>
            <tr><th scope="row">Identification</th><td>Connected player-match graph plus disclosed ridge shrinkage</td><td><span class="is-ready">Passed</span></td></tr>
            <tr><th scope="row">Publication terms</th><td>StatsBomb attribution and declared historical scope</td><td><span class="is-ready">Passed</span></td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <details class="rating-lab-limitations">
      <summary>What these player models do—and do not—claim</summary>
      <ul>
        <li>Inputs are outcomes, lineups, and minutes only: no passes, shots, dribbles, expected goals, or tracking data.</li>
        <li>The estimates would measure net contribution associated with results after controlling for teammates and opponents, not how a player created that contribution.</li>
        <li>Lineup TrueSkill is the natural sequential rating. RAPM is the complementary retrospective impact estimate; they answer related but different questions.</li>
        <li>Minutes are needed to avoid assigning a substitute the same exposure as a full-match player. Score differential by on-field stint is preferable for RAPM when legally reproducible.</li>
        <li>StatsBomb Open Data supports these declared historical seasons, but it is not a complete live feed for the five men’s leagues covered by the team rankings.</li>
      </ul>
    </details>
  </section>
  </details>

  <details class="rating-lab-disclosure">
    <summary><span>Interactive specification</span><strong>Exact protocol explorer</strong></summary>
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
          <button type="button" data-protocol-model="glicko2" aria-pressed="false">Glicko-2</button>
          <button type="button" data-protocol-model="trueskill" aria-pressed="false">Gaussian</button>
          <button type="button" data-protocol-model="robust" aria-pressed="false">Robust</button>
        </div>
      </div>
    </div>

    <div id="rating-protocol" aria-live="polite"></div>

    <details class="rating-lab-limitations">
      <summary>Known limitations and deliberate simplifications</summary>
      <ul>
        <li>Current ratings use the result plus the declared competitive context: tennis surface, football venue, or chess color. Score margin, lineups, injuries, time controls, and player age are not model inputs. The withheld player-contribution protocol would add lineups and minutes, but no event statistics.</li>
        <li>Football Elo values are comparable only inside a connected result network. A new qualifying tie between two unseen clubs forms an isolated component around the arbitrary 1500 prior. Those clubs remain available to forecasts but stay in a provisional tier until they have 10 covered results and connect to the main network.</li>
        <li>Crests, portraits, and source-coded flags are presentational metadata, never model inputs. External images are restricted to the declared football-data.org and Wikimedia hosts and carry source and rights metadata in the public JSON. Flags use a vendored, pinned SVG set rather than operating-system emoji; unavailable assets fall back to initials.</li>
        <li>Draws use an actual score of 0.5. Published log loss and Brier score evaluate expected score, not a separate three-class win/draw/loss forecast.</li>
        <li>Multiple results on the same date are replayed in the published stable identifier order because exact start times are not consistently available.</li>
        <li>Glicko-2 is the exception to within-day ordering: all results on one calendar date form a simultaneous rating period. Seven days define one unit of inactivity inflation.</li>
        <li>The public JSON publishes at most the top 500 eligible entities per model; it is not a complete registry of every entity seen in the source archive.</li>
        <li>Model selection tests a small declared parameter grid. It does not prove that the selected candidate is globally optimal.</li>
        <li>Cup forecasts do not guess unpublished entrants or qualification paths. The live Champions League qualifying view forecasts survival of the current official two-leg tie only. For a fully published knockout field, known ties are fixed; later unpublished draws use a uniform redraw without seeding, association, or country restrictions.</li>
        <li>For two-leg qualifying ties, the selected protocol supplies home/draw/away probabilities. A disclosed independent-Poisson bridge fits those probabilities for each unplayed leg, aggregate goals determine advancement, and a neutral decisive probability is used only if the aggregate remains level.</li>
      </ul>
    </details>
  </section>
  </details>

  <details class="rating-lab-disclosure">
    <summary><span>Reproducibility</span><strong>Equations, parameters, and build audit</strong></summary>
  <section class="rating-lab-audit" id="reproducibility" aria-labelledby="audit-heading">
      <p class="rating-lab-kicker">Full details</p>
    <h2 id="audit-heading">Inspect every assumption. Reproduce every table.</h2>
    <p class="rating-lab-audit-intro">The browser only reads static JSON. All ratings are rebuilt from public results by deterministic, chronological Python replay; there is no private ranking service or hidden model.</p>

    <div class="rating-lab-equations">
      <article>
        <h3>Elo probability and update</h3>
        <p class="rating-lab-equation" aria-label="p A equals one divided by one plus ten to the power negative rating A plus home advantage minus rating B divided by 400">p<sub>A</sub> = 1 / (1 + 10<sup>−(R<sub>A</sub> + H − R<sub>B</sub>)/400</sup>)</p>
        <p class="rating-lab-equation" aria-label="new rating A equals rating A plus K times actual score minus predicted probability">R′<sub>A</sub> = R<sub>A</sub> + K(s<sub>A</sub> − p<sub>A</sub>)</p>
      </article>
      <article>
        <h3>Glicko-2 uncertainty</h3>
        <p>Ratings use <span class="rating-lab-formula">μ=(r−1500)/173.7178</span> and <span class="rating-lab-formula">φ=RD/173.7178</span>. The published iterative volatility update is solved to tolerance <span class="rating-lab-formula">10<sup>−6</sup></span>; rankings use <span class="rating-lab-formula">r−2RD</span>.</p>
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
  </details>

  <details class="rating-lab-disclosure">
    <summary><span>Provenance</span><strong>Sources and licences</strong></summary>
  <section class="rating-lab-sources" aria-labelledby="sources-heading">
    <p class="rating-lab-kicker">Open data</p>
    <h2 id="sources-heading">Sources and licences</h2>
    <ul id="rating-source-list">
      <li><a href="https://github.com/msolonskyi/ManTennisData">ManTennisData</a> — ATP-derived singles results, MIT.</li>
      <li><a href="https://www.football-data.org/">football-data.org</a> — five major European leagues plus published Champions League, FIFA World Cup, and European Championship stages.</li>
      <li><a href="https://www.uefa.com/uefachampionsleague/accesslist/">UEFA</a> — official 2026/27 Champions League qualifying results, published ties, draw dates, and match calendar.</li>
      <li><a href="https://github.com/openfootball">OpenFootball</a> — current league fixtures plus credential-free Champions League, World Cup, and Euro structures, CC0 1.0.</li>
      <li><a href="https://github.com/hudl/open-data">Hudl StatsBomb Open Data</a> — lineups and events for selected historical competitions and seasons; a reproducible player-method research source, not the live five-league feed.</li>
      <li><a href="https://github.com/martj42/international_results">International football results</a> — men’s full internationals, CC0 1.0.</li>
      <li><a href="https://database.lichess.org/#broadcasts">Lichess official broadcasts</a> — elite OTB games, CC BY-SA 4.0.</li>
      <li><a href="https://github.com/lipis/flag-icons/tree/v7.5.0">flag-icons 7.5.0</a> — vendored SVG country and home-nation flags, MIT; selected only from source codes.</li>
      <li><a href="https://www.glicko.net/glicko/glicko2.pdf">Glicko-2 specification and worked example</a> — public-domain head-to-head rating protocol.</li>
      <li><a href="https://www.microsoft.com/en-us/research/publication/trueskill-2-improved-bayesian-skill-rating-system/">Microsoft Research TrueSkill 2 paper</a> — used to delimit features this result-only site does not claim.</li>
      <li><a href="https://docs.polymarket.com/market-data/overview">Polymarket Gamma API</a> — public outcome-price snapshots used only as an external forecast benchmark.</li>
      <li><a href="https://docs.kalshi.com/getting_started/quick_start_market_data">Kalshi Trade API</a> — unauthenticated public bid, ask, and last-trade snapshots used only as a separate external forecast benchmark.</li>
    </ul>
    <p>Rankings are independent statistical estimates, not official tour, league, federation, or Lichess ratings. They are informational and are not betting advice.</p>
  </section>
  </details>

  <aside class="rating-lab-support" aria-labelledby="support-heading">
    <div>
      <p class="rating-lab-kicker">Keep it growing</p>
      <h2 id="support-heading">Enjoying Rating Lab?</h2>
      <p>This is an independent side project. The most useful support right now is to try it, share it, or suggest the next competition or feature.</p>
    </div>
    <div class="rating-lab-support-actions">
      <a class="is-primary" href="https://github.com/kieranmcshane/kieranmcshane.github.io">View the code</a>
      <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues/new">Suggest an idea</a>
    </div>
  </aside>
  </section>
</div>

<script defer src="{{ '/assets/js/rating-lab.js' | relative_url }}?v={{ site.github.build_revision }}"></script>
