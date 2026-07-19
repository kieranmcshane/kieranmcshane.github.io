---
layout: page
title: Rating Lab
permalink: /rating-lab/
description: Live alternative ratings for tennis, football, and chess, tested against real match outcomes.
---

<div class="rating-lab" data-data-root="{{ '/assets/data/rating-lab' | relative_url }}">
  <header class="rating-lab-hero">
    <p class="rating-lab-kicker">Live, reproducible sports ratings</p>
    <h1>Three sports. Three ways to measure strength.</h1>
    <p class="rating-lab-deck">Explore current Elo, Gaussian TrueSkill, and robust heavy-tail rankings built from real match results. Every prediction is scored before its result is used to update the model.</p>
    <div class="rating-lab-freshness" id="rating-lab-freshness" role="status" aria-live="polite">Loading the latest ratings…</div>
  </header>

  <noscript><p class="rating-lab-notice">This interactive leaderboard requires JavaScript.</p></noscript>
  <div id="rating-lab-error" class="rating-lab-notice rating-lab-notice-error" role="alert" hidden></div>

  <section class="rating-lab-explorer" aria-labelledby="leaderboard-heading">
    <h2 id="leaderboard-heading">Leaderboard</h2>
    <div class="rating-lab-toolbar">
      <div class="rating-lab-control-group" aria-label="Sport">
        <span class="rating-lab-control-label">Sport</span>
        <div class="rating-lab-segmented" id="sport-tabs">
          <button type="button" data-sport="tennis" aria-pressed="true">Tennis</button>
          <button type="button" data-sport="football" aria-pressed="false">Football</button>
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

    <div class="rating-lab-grid">
      <div class="rating-lab-table-wrap">
        <table class="rating-lab-table">
          <caption id="ranking-caption">Current rankings</caption>
          <thead>
            <tr>
              <th scope="col"><button type="button" data-sort="rank">Rank</button></th>
              <th scope="col"><button type="button" data-sort="name">Player or team</button></th>
              <th scope="col"><button type="button" data-sort="score">Rating</button></th>
              <th scope="col" class="rating-lab-optional"><button type="button" data-sort="sigma">Uncertainty</button></th>
              <th scope="col"><button type="button" data-sort="change30">30-day change</button></th>
              <th scope="col" class="rating-lab-optional"><button type="button" data-sort="recent_matches">Recent</button></th>
            </tr>
          </thead>
          <tbody id="ranking-body"></tbody>
        </table>
        <p id="ranking-empty" class="rating-lab-empty" hidden>No eligible competitors match these filters.</p>
      </div>

      <aside class="rating-lab-detail" id="rating-detail" aria-live="polite">
        <p class="rating-lab-detail-placeholder">Choose a row to inspect its recent rating history.</p>
      </aside>
    </div>
  </section>

  <section class="rating-lab-method" id="methodology">
    <p class="rating-lab-kicker">Methodology</p>
    <h2>What changes—and what does not</h2>
    <div class="rating-lab-method-grid">
      <article>
        <h3>Elo</h3>
        <p>A direct online update around a logistic win-probability curve. Football includes home advantage and seasonal mean reversion; draws count as half a win.</p>
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

  <section class="rating-lab-sources" aria-labelledby="sources-heading">
    <p class="rating-lab-kicker">Open data</p>
    <h2 id="sources-heading">Sources and licences</h2>
    <ul id="rating-source-list">
      <li><a href="https://github.com/msolonskyi/ManTennisData">ManTennisData</a> — ATP-derived singles results, MIT.</li>
      <li><a href="https://www.football-data.org/">football-data.org</a> — five major European leagues and the Champions League.</li>
      <li><a href="https://database.lichess.org/#broadcasts">Lichess official broadcasts</a> — elite OTB games, CC BY-SA 4.0.</li>
    </ul>
    <p>Rankings are independent statistical estimates, not official tour, league, federation, or Lichess ratings. They are informational and are not betting advice.</p>
  </section>
</div>

<script defer src="{{ '/assets/js/rating-lab.js' | relative_url }}?v={{ site.github.build_revision }}"></script>
