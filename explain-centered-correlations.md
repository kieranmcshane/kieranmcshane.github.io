---
layout: page
title: "Reconstruct the Centered-Correlation Argument"
permalink: /explain/centered-correlations/
description: "A click-based FSRS learning companion to the article on centered correlation tensors and quantum separability."
---

<div class="explain-lab" data-storage-key="centered-correlation-explain-v2">
  <header class="explain-hero">
    <p class="explain-kicker">Interactive companion to the article</p>
    <h1>Can you reconstruct the argument?</h1>
    <p class="explain-deck">No essay box and no speaking to the screen. Rebuild the proof, choose the missing steps, and diagnose plausible mistakes. FSRS then decides which ideas should return and when.</p>
    <div class="explain-hero-actions">
      <a class="explain-primary-link" href="#derivation-order">Start the reconstruction</a>
      <a href="{{ '/2026/07/17/centered-correlation-tensors-separability/' | relative_url }}">Return to the article</a>
    </div>
    <div class="explain-progress" aria-labelledby="explain-progress-label">
      <div class="explain-progress-copy">
        <strong id="explain-progress-label">Your progress</strong>
        <span id="explain-progress-text">0 of 4 stages complete</span>
      </div>
      <div class="explain-progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0" aria-labelledby="explain-progress-label">
        <span id="explain-progress-bar"></span>
      </div>
    </div>
    <p class="explain-privacy">Progress and the FSRS review history stay in this browser. They can be exported and imported without creating an account.</p>
  </header>

  <nav class="explain-local-nav" aria-label="Learning stages">
    <a href="#derivation-order"><strong>1</strong><span>Order</span></a>
    <a href="#scheduled-review"><strong>2</strong><span>Review</span></a>
    <a href="#diagnose"><strong>3</strong><span>Diagnose</span></a>
    <a href="#build-explanation"><strong>4</strong><span>Assemble</span></a>
  </nav>

  <noscript><p class="explain-notice">This learning companion needs JavaScript. The mathematical article remains fully readable without it.</p></noscript>

  <section class="explain-stage" id="derivation-order" aria-labelledby="derivation-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 1</span><h2 id="derivation-heading">Put the proof in order</h2></div>
      <p>Move the statements until each one uses only information established above it.</p>
    </div>

    <ol class="explain-order-list" id="explain-order-list">
      <li data-step="4"><div><span class="explain-order-number">?</span><p>Cauchy–Schwarz bounds the projective sum by the product of the two local standard deviations.</p></div><div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move Cauchy–Schwarz step up">↑</button><button type="button" data-move="down" aria-label="Move Cauchy–Schwarz step down">↓</button></div></li>
      <li data-step="1"><div><span class="explain-order-number">?</span><p>A product state has a rank-one correlation matrix: $T=rs^{\mathsf T}$.</p></div><div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move product-state step up">↑</button><button type="button" data-move="down" aria-label="Move product-state step down">↓</button></div></li>
      <li data-step="5"><div><span class="explain-order-number">?</span><p>The local variances are $R_M^2-\lVert r\rVert_2^2$ and $R_N^2-\lVert s\rVert_2^2$, giving the centered separability bound.</p></div><div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move variance step up">↑</button><button type="button" data-move="down" aria-label="Move variance step down">↓</button></div></li>
      <li data-step="2"><div><span class="explain-order-number">?</span><p>A separable state gives one common convex decomposition: $T=\sum_k p_k r_k s_k^{\mathsf T}$, with $r=\sum_kp_kr_k$ and $s=\sum_kp_ks_k$.</p></div><div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move separable-mixture step up">↑</button><button type="button" data-move="down" aria-label="Move separable-mixture step down">↓</button></div></li>
      <li data-step="3"><div><span class="explain-order-number">?</span><p>Subtracting the means rewrites $C=T-rs^{\mathsf T}$ as $\sum_kp_k(r_k-r)(s_k-s)^{\mathsf T}$.</p></div><div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move centering step up">↑</button><button type="button" data-move="down" aria-label="Move centering step down">↓</button></div></li>
    </ol>
    <div class="explain-stage-actions">
      <button class="explain-button" type="button" id="check-order">Check the order</button>
      <button class="explain-button explain-button-secondary" type="button" id="reset-order">Start again</button>
      <p id="order-feedback" class="explain-feedback" role="status" aria-live="polite"></p>
    </div>
  </section>

  <section class="explain-stage" id="scheduled-review" aria-labelledby="review-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 2 · FSRS-6</span><h2 id="review-heading">Review the ideas when they are due</h2></div>
      <p>Choose an answer. A first-attempt success is recorded as <em>Good</em>; a corrected answer as <em>Hard</em>; revealing the answer as <em>Again</em>. FSRS schedules the next appearance.</p>
    </div>

    <div class="fsrs-summary" aria-live="polite">
      <div><span>Due now</span><strong id="fsrs-due-count">5</strong></div>
      <div><span>Reviewed</span><strong id="fsrs-reviewed-count">0 / 5</strong></div>
      <div><span>Next review</span><strong id="fsrs-next-date">today</strong></div>
    </div>

    <div class="fsrs-review-card" id="fsrs-review-card">
      <div class="fsrs-card-meta"><span id="fsrs-concept-label">Concept 1 of 5</span><strong id="fsrs-card-status">New</strong></div>
      <h3 id="fsrs-question">Which statement best describes the centered matrix?</h3>
      <div class="fsrs-options" id="fsrs-options"></div>
      <button type="button" class="explain-text-button" id="fsrs-reveal">Show the answer</button>
      <div class="fsrs-answer" id="fsrs-answer" hidden></div>
      <button type="button" class="explain-button" id="fsrs-next" hidden>Next concept</button>
    </div>

    <div class="fsrs-empty" id="fsrs-empty" hidden>
      <strong>You are caught up.</strong>
      <p id="fsrs-empty-copy">The next scheduled concept will appear here when it is due.</p>
      <button type="button" class="explain-button explain-button-secondary" id="fsrs-practise-all">Practise all concepts now</button>
    </div>

    <details class="fsrs-schedule">
      <summary>See the five-concept schedule</summary>
      <ol id="fsrs-schedule-list"></ol>
      <p>Scheduling uses the official <a href="https://github.com/open-spaced-repetition/ts-fsrs">ts-fsrs</a> implementation of FSRS-6 with 90% requested retention. No personal parameter optimization is attempted with so little data.</p>
    </details>
  </section>

  <section class="explain-stage" id="diagnose" aria-labelledby="diagnose-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 3</span><h2 id="diagnose-heading">Find what is wrong</h2></div>
      <p>The difficult misconceptions are plausible statements, not absurd ones. Decide whether each claim survives the article’s argument.</p>
    </div>

    <div class="diagnosis-list" id="diagnosis-list">
      <article data-diagnosis="nonlinear" data-correct="false">
        <p>“The map $\rho_{AB}\mapsto C=T-rs^{\mathsf T}$ is linear, so all centered correlation matrices of separable states form one fixed convex body.”</p>
        <div><button type="button" data-answer="true">Sound</button><button type="button" data-answer="false">There is a flaw</button></div>
        <aside hidden>The flaw is the product $rs^{\mathsf T}$: both vectors depend on the state, so centering is nonlinear. For fixed marginals there is a clean norm ball; globally one must qualify the convex-body language.</aside>
      </article>
      <article data-diagnosis="flattening" data-correct="false">
        <p>“For a third-order tensor, the full Euclidean projective norm is just the largest nuclear norm among its matrix unfoldings.”</p>
        <div><button type="button" data-answer="true">Sound</button><button type="button" data-answer="false">There is a flaw</button></div>
        <aside hidden>Every unfolding norm is bounded above by the full projective norm, but equality is not general. A matrix rank-one term across a cut need not factor across every individual party.</aside>
      </article>
      <article data-diagnosis="complete" data-correct="false">
        <p>“Because every entangled pure bipartite state violates the centered bound, the criterion characterizes entanglement for arbitrary mixed states.”</p>
        <div><button type="button" data-answer="true">Sound</button><button type="button" data-answer="false">There is a flaw</button></div>
        <aside hidden>The pure-state statement does not extend to mixed states. The article gives NPT mixed states that still pass the centered test.</aside>
      </article>
      <article data-diagnosis="common" data-correct="true">
        <p>“Bounding every subset tensor separately still does not show that one common separable ensemble generates all tensor orders.”</p>
        <div><button type="button" data-answer="true">Sound</button><button type="button" data-answer="false">There is a flaw</button></div>
        <aside hidden>This is sound. Compatibility across orders is the remaining common-decomposition, or truncated-moment, constraint.</aside>
      </article>
    </div>
    <p class="explain-feedback" id="diagnosis-feedback" role="status" aria-live="polite"></p>
  </section>

  <section class="explain-stage" id="build-explanation" aria-labelledby="builder-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 4</span><h2 id="builder-heading">Assemble a concise explanation</h2></div>
      <p>For each paragraph, choose the sentence that actually advances the argument. The completed version appears only after all four choices are correct.</p>
    </div>

    <div class="explanation-builder" id="explanation-builder">
      <article data-builder="1" data-correct="product"><span>Opening</span><h3>What is the elementary starting point?</h3><div><button type="button" data-choice="commute">Separable states are built from commuting density matrices.</button><button type="button" data-choice="product">A product state factorizes the correlation matrix as $T=rs^{\mathsf T}$.</button><button type="button" data-choice="pure">Every pure state has a rank-one correlation matrix.</button></div><p hidden></p></article>
      <article data-builder="2" data-correct="common"><span>Mixtures</span><h3>What does separability add?</h3><div><button type="button" data-choice="separate">Each marginal and tensor may use an unrelated optimal decomposition.</button><button type="button" data-choice="common">One ensemble gives $r$, $s$, and $T$ simultaneously as first and cross-moments.</button><button type="button" data-choice="orthogonal">The product Bloch vectors can always be chosen orthogonal.</button></div><p hidden></p></article>
      <article data-builder="3" data-correct="covariance"><span>Centering</span><h3>What is gained by subtracting $rs^{\mathsf T}$?</h3><div><button type="button" data-choice="linear">It makes the state-to-tensor map linear.</button><button type="button" data-choice="erase">It erases every classical correlation.</button><button type="button" data-choice="covariance">It turns the remainder into the covariance $\sum_kp_k(r_k-r)(s_k-s)^{\mathsf T}$.</button></div><p hidden></p></article>
      <article data-builder="4" data-correct="bound"><span>Conclusion</span><h3>How does the criterion follow?</h3><div><button type="button" data-choice="bound">Rank-one factorization, the triangle inequality, and Cauchy–Schwarz give a bound controlled by the marginal variance deficits.</button><button type="button" data-choice="ppt">Partial transposition gives the bound in every dimension.</button><button type="button" data-choice="svd">An SVD proves that every mixed state passing the bound is separable.</button></div><p hidden></p></article>
    </div>

    <div class="assembled-explanation" id="assembled-explanation" hidden>
      <p class="explain-kicker">The assembled account</p>
      <p>A product state factorizes the correlation matrix as $T=rs^{\mathsf T}$. For a separable state, one common ensemble gives $r$, $s$, and $T$ simultaneously as first and cross-moments. Subtracting $rs^{\mathsf T}$ therefore turns the remainder into the covariance $C=\sum_kp_k(r_k-r)(s_k-s)^{\mathsf T}$. Rank-one norm factorization, the triangle inequality, and Cauchy–Schwarz then bound $\lVert C\rVert_*$ by the product of the two local standard deviations.</p>
      <p>Bipartitely, the Euclidean projective norm is exactly the matrix nuclear norm, so the uncentered formulation recovers de Vicente. For three or more factors, unfolding nuclear norms can be strictly smaller than the full projective norm. The remaining structural problem is to enforce that all subset tensors and tensor orders come from one common separable ensemble.</p>
    </div>
  </section>

  <section class="explain-readiness" aria-labelledby="readiness-heading">
    <div><p class="explain-kicker">Reconstruction status</p><h2 id="readiness-heading">Understanding means recovering the links.</h2><p id="readiness-copy">Complete all four stages to mark this article as reconstructed.</p></div>
    <div class="readiness-actions">
      <button type="button" class="explain-button" id="mark-ready" disabled>Mark as reconstructed</button>
      <button type="button" class="explain-button explain-button-secondary" id="export-progress">Export progress</button>
      <label class="explain-import-button">Import progress<input type="file" id="import-progress" accept="application/json,.json"></label>
      <button type="button" class="explain-text-button" id="reset-progress">Reset this browser’s progress</button>
    </div>
    <p id="readiness-status" role="status" aria-live="polite"></p>
  </section>

  <p class="explain-source-note">Need to verify a detail? Return to <a href="{{ '/2026/07/17/centered-correlation-tensors-separability/' | relative_url }}">Centered Correlation Tensors and Quantum Separability</a>, then come back to the due queue.</p>
</div>
