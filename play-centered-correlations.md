---
layout: page
title: "Centered Correlations: Proof Campaign"
permalink: /play/centered-correlations/
description: "A no-typing mathematical strategy game for reconstructing the centered-correlation separability argument, with FSRS return missions."
---

<div class="proof-game" data-storage-key="centered-correlation-game-v1">
  <header class="game-hero">
    <div>
      <p class="game-kicker">Proof campaign · no typing or speaking</p>
      <h1>Recover the centered-correlation argument</h1>
      <p>You are given mathematical facts, a target, and a small set of legal moves. Choose what to transform, keep the proof intact, and reconstruct the entire argument. Fragile ideas return later through FSRS.</p>
    </div>
    <div class="game-hero-status" aria-label="Campaign status">
      <span>Campaign</span>
      <strong id="game-campaign-count">0 / 7</strong>
      <span id="game-save-status">Saved on this device</span>
    </div>
  </header>

  <noscript><p class="game-notice">The proof campaign needs JavaScript. The <a href="{{ '/2026/07/17/centered-correlation-tensors-separability/' | relative_url }}">mathematical article</a> remains fully readable without it.</p></noscript>

  <nav class="game-tabs" aria-label="Game views">
    <button type="button" aria-pressed="true" data-game-view="campaign"><span class="game-tab-icon" aria-hidden="true">⌂</span><span class="game-tab-long">Campaign map</span><span class="game-tab-short">Map</span></button>
    <button type="button" aria-pressed="false" data-game-view="mission"><span class="game-tab-icon" aria-hidden="true">◇</span><span class="game-tab-long">Current mission</span><span class="game-tab-short">Mission</span></button>
    <button type="button" aria-pressed="false" data-game-view="returns"><span class="game-tab-icon" aria-hidden="true">↻</span><span class="game-tab-long">Return missions</span><span class="game-tab-short">Returns</span> <span class="game-due-badge" id="game-due-badge">0</span></button>
  </nav>

  <main>
    <section class="game-view" id="game-campaign" data-game-panel="campaign" aria-labelledby="campaign-heading">
      <div class="game-section-heading">
        <div><p class="game-kicker">The argument as a territory</p><h2 id="campaign-heading">Campaign map</h2></div>
        <p>Each mission isolates one mathematical decision. Finish a mission to open the next route.</p>
      </div>
      <ol class="game-map" id="game-map" aria-label="Seven proof missions"></ol>
      <aside class="game-map-key">
        <span><i class="game-key-dot is-open"></i> available</span>
        <span><i class="game-key-dot is-complete"></i> recovered</span>
        <span><i class="game-key-dot is-locked"></i> locked</span>
      </aside>
    </section>

    <section class="game-view" id="game-mission" data-game-panel="mission" aria-labelledby="mission-title" hidden>
      <header class="mission-header">
        <button type="button" class="game-quiet-button" id="game-leave-mission">← Campaign map</button>
        <div class="mission-meta"><span id="mission-number">Mission 1 of 7</span><strong id="mission-title">Coordinates</strong></div>
        <div class="mission-integrity" aria-labelledby="integrity-label">
          <span id="integrity-label">Proof integrity</span>
          <div id="integrity-meter" role="img" aria-label="3 of 3 integrity remaining"></div>
        </div>
      </header>

      <div class="mission-brief">
        <p class="game-kicker">Objective</p>
        <p id="mission-objective"></p>
      </div>

      <div class="mission-board">
        <details class="mission-facts" id="mission-facts-drawer" open>
          <summary id="mission-facts-heading"><span>Available facts</span><small>Reference</small></summary>
          <ul id="mission-facts"></ul>
          <p class="mission-rules">A productive move advances the proof. A valid detour can be undone. A false implication damages proof integrity. At zero integrity, this mission returns to its checkpoint.</p>
        </details>

        <div class="mission-workspace">
          <div class="mission-turn">
            <span id="mission-step-label">Decision 1 of 3</span>
            <span id="mission-rating">Clean run</span>
          </div>
          <div class="mission-goal">
            <span>Target</span>
            <strong id="mission-target"></strong>
          </div>
          <article class="proof-state" id="proof-state" aria-live="polite">
            <p class="proof-state-label">Current proof state</p>
            <div id="proof-state-formula"></div>
            <p id="proof-state-copy"></p>
          </article>

          <div class="proof-tools" aria-labelledby="proof-tools-heading">
            <div><span id="proof-tools-heading">Choose a move</span><p id="proof-prompt"></p></div>
            <div id="proof-tool-buttons"></div>
          </div>
          <p class="mission-feedback" id="mission-feedback" role="status" aria-live="polite"></p>
          <ol class="mission-log" id="mission-log" aria-label="Moves made in this mission"></ol>
          <div class="mission-controls">
            <button type="button" class="game-button game-button-secondary" id="game-undo" disabled>Undo detour</button>
            <button type="button" class="game-quiet-button" id="game-restart">Restart mission</button>
          </div>
        </div>
      </div>

      <div class="mission-complete" id="mission-complete" hidden>
        <p class="game-kicker">Route recovered</p>
        <h2 id="mission-complete-title">Mission complete</h2>
        <p id="mission-complete-copy"></p>
        <div class="mission-complete-actions">
          <button type="button" class="game-button" id="game-next-mission">Continue to the next mission</button>
          <button type="button" class="game-button game-button-secondary" id="game-return-map">Return to the map</button>
        </div>
      </div>
    </section>

    <section class="game-view" id="game-returns" data-game-panel="returns" aria-labelledby="returns-heading" hidden>
      <div class="game-section-heading">
        <div><p class="game-kicker">FSRS-6</p><h2 id="returns-heading">Return missions</h2></div>
        <p>Completed ideas return as short encounters when FSRS predicts that retrieval is becoming useful.</p>
      </div>
      <div class="return-summary">
        <div><span>Due now</span><strong id="return-due-count">0</strong></div>
        <div><span>Next return</span><strong id="return-next-date">—</strong></div>
        <div><span>Retention target</span><strong>90%</strong></div>
      </div>
      <article class="return-encounter" id="return-encounter">
        <p class="game-kicker" id="return-mission-label">No mission due</p>
        <h3 id="return-question">Finish campaign missions to open return encounters.</h3>
        <div id="return-options"></div>
        <p id="return-feedback" role="status" aria-live="polite"></p>
        <button type="button" class="game-button" id="return-next" hidden>Next return mission</button>
      </article>
      <details class="return-method">
        <summary>How the return system works</summary>
        <p>The official <a href="https://github.com/open-spaced-repetition/ts-fsrs">ts-fsrs</a> implementation schedules each mathematical idea. A clean recovery is recorded as <em>Good</em>, a recovered run as <em>Hard</em>, and a failed encounter as <em>Again</em>. The schedule and campaign save remain in this browser.</p>
      </details>
    </section>
  </main>

  <footer class="game-footer">
    <div>
      <strong>Need the full exposition?</strong>
      <a href="{{ '/2026/07/17/centered-correlation-tensors-separability/' | relative_url }}">Read the article</a>
      <span aria-hidden="true">·</span>
      <a href="{{ '/explain/centered-correlations/' | relative_url }}">Open the study companion</a>
    </div>
    <button type="button" class="game-quiet-button" id="game-reset-save">Reset campaign save</button>
  </footer>
</div>
