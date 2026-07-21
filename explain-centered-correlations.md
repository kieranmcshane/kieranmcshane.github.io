---
layout: page
title: "Explain Centered Correlation Tensors"
permalink: /explain/centered-correlations/
description: "An active-recall and oral-rehearsal companion to the article on centered correlation tensors and quantum separability."
---

<div class="explain-lab" data-storage-key="centered-correlation-explain-v1">
  <header class="explain-hero">
    <p class="explain-kicker">Active companion to the article</p>
    <h1>Can you explain the argument without looking?</h1>
    <p class="explain-deck">Reading the derivation is not the same as being able to reconstruct it. This page asks you to put the proof back together, explain its hinges, and rehearse a short oral account.</p>
    <div class="explain-hero-actions">
      <a class="explain-primary-link" href="#derivation-order">Start with the proof</a>
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
    <p class="explain-privacy">No account is required. Your profile and progress stay in this browser. Audio is never uploaded.</p>
  </header>

  <nav class="explain-local-nav" aria-label="Oral trainer stages">
    <a href="#derivation-order"><strong>1</strong><span>Rebuild</span></a>
    <a href="#teach-back"><strong>2</strong><span>Explain</span></a>
    <a href="#viva"><strong>3</strong><span>Defend</span></a>
    <a href="#oral-rehearsal"><strong>4</strong><span>Rehearse</span></a>
  </nav>

  <noscript><p class="explain-notice">This oral trainer needs JavaScript. The mathematical article itself remains fully readable without it.</p></noscript>

  <section class="explain-stage" id="derivation-order" aria-labelledby="derivation-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 1</span><h2 id="derivation-heading">Rebuild the proof</h2></div>
      <p>Put the five statements in logical order. Do not consult the article until you have made a first attempt.</p>
    </div>

    <ol class="explain-order-list" id="explain-order-list">
      <li data-step="4">
        <div><span class="explain-order-number">?</span><p>Cauchy–Schwarz bounds the projective sum by the product of the two local standard deviations.</p></div>
        <div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move Cauchy–Schwarz step up">↑</button><button type="button" data-move="down" aria-label="Move Cauchy–Schwarz step down">↓</button></div>
      </li>
      <li data-step="1">
        <div><span class="explain-order-number">?</span><p>A product state has a rank-one correlation matrix: $T=rs^{\mathsf T}$.</p></div>
        <div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move product-state step up">↑</button><button type="button" data-move="down" aria-label="Move product-state step down">↓</button></div>
      </li>
      <li data-step="5">
        <div><span class="explain-order-number">?</span><p>The local variances are $R_M^2-\lVert r\rVert_2^2$ and $R_N^2-\lVert s\rVert_2^2$, giving the centered separability bound.</p></div>
        <div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move variance step up">↑</button><button type="button" data-move="down" aria-label="Move variance step down">↓</button></div>
      </li>
      <li data-step="2">
        <div><span class="explain-order-number">?</span><p>A separable state gives one common convex decomposition: $T=\sum_k p_k r_k s_k^{\mathsf T}$, with $r=\sum_kp_kr_k$ and $s=\sum_kp_ks_k$.</p></div>
        <div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move separable-mixture step up">↑</button><button type="button" data-move="down" aria-label="Move separable-mixture step down">↓</button></div>
      </li>
      <li data-step="3">
        <div><span class="explain-order-number">?</span><p>Subtracting the means rewrites $C=T-rs^{\mathsf T}$ as $\sum_kp_k(r_k-r)(s_k-s)^{\mathsf T}$.</p></div>
        <div class="explain-order-controls"><button type="button" data-move="up" aria-label="Move centering step up">↑</button><button type="button" data-move="down" aria-label="Move centering step down">↓</button></div>
      </li>
    </ol>
    <div class="explain-stage-actions">
      <button class="explain-button" type="button" id="check-order">Check the order</button>
      <button class="explain-button explain-button-secondary" type="button" id="reset-order">Start again</button>
      <p id="order-feedback" class="explain-feedback" role="status" aria-live="polite"></p>
    </div>
  </section>

  <section class="explain-stage" id="teach-back" aria-labelledby="teach-back-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 2</span><h2 id="teach-back-heading">Explain the five hinges</h2></div>
      <p>Write a short answer from memory. The comparison grid appears only after you have committed to an explanation.</p>
    </div>

    <div class="teach-back-list" id="teach-back-list">
      <article class="teach-back-card" data-card="coordinates">
        <header><span>01</span><h3>What are $r$, $s$, $T$, and $C$?</h3><em data-card-state>Not attempted</em></header>
        <label><span>Your explanation</span><textarea rows="4" placeholder="Explain the four objects and what centering removes."></textarea></label>
        <button type="button" class="explain-button reveal-rubric" disabled>Compare with the essentials</button>
        <div class="teach-back-rubric" hidden>
          <p>A sound answer should make all three points:</p>
          <label><input type="checkbox"> $r$ and $s$ are the Bloch coordinates of the reduced states.</label>
          <label><input type="checkbox"> $T$ contains the coefficients of traceless observables on both subsystems.</label>
          <label><input type="checkbox"> $C=T-rs^{\mathsf T}$ removes the product of the local means, leaving connected correlations.</label>
          <div class="teach-back-confidence"><button type="button" data-confidence="review">I need another pass</button><button type="button" data-confidence="mastered">I can explain this aloud</button></div>
        </div>
      </article>

      <article class="teach-back-card" data-card="identity">
        <header><span>02</span><h3>Why is $C$ a covariance for a separable state?</h3><em data-card-state>Not attempted</em></header>
        <label><span>Your explanation</span><textarea rows="4" placeholder="Start from a common separable decomposition and do the algebra."></textarea></label>
        <button type="button" class="explain-button reveal-rubric" disabled>Compare with the essentials</button>
        <div class="teach-back-rubric" hidden>
          <p>A sound answer should make all three points:</p>
          <label><input type="checkbox"> Use the same probabilities $p_k$ for $r$, $s$, and $T$.</label>
          <label><input type="checkbox"> State $T=\sum_kp_kr_ks_k^{\mathsf T}$, $r=\sum_kp_kr_k$, and $s=\sum_kp_ks_k$.</label>
          <label><input type="checkbox"> Expand to obtain $C=\sum_kp_k(r_k-r)(s_k-s)^{\mathsf T}$.</label>
          <div class="teach-back-confidence"><button type="button" data-confidence="review">I need another pass</button><button type="button" data-confidence="mastered">I can explain this aloud</button></div>
        </div>
      </article>

      <article class="teach-back-card" data-card="bound">
        <header><span>03</span><h3>How does the separability bound follow?</h3><em data-card-state>Not attempted</em></header>
        <label><span>Your explanation</span><textarea rows="5" placeholder="Name the rank-one norm identity, the two inequalities, and the variance calculation."></textarea></label>
        <button type="button" class="explain-button reveal-rubric" disabled>Compare with the essentials</button>
        <div class="teach-back-rubric" hidden>
          <p>A sound answer should make all four points:</p>
          <label><input type="checkbox"> Use $\lVert uv^{\mathsf T}\rVert_*=\lVert u\rVert_2\lVert v\rVert_2$ and the triangle inequality.</label>
          <label><input type="checkbox"> Apply Cauchy–Schwarz to the weighted sum of the two fluctuation norms.</label>
          <label><input type="checkbox"> Identify the variance deficits $R_M^2-\lVert r\rVert_2^2$ and $R_N^2-\lVert s\rVert_2^2$.</label>
          <label><input type="checkbox"> Conclude $\lVert C\rVert_*\leq\sqrt{(R_M^2-\lVert r\rVert_2^2)(R_N^2-\lVert s\rVert_2^2)}$.</label>
          <div class="teach-back-confidence"><button type="button" data-confidence="review">I need another pass</button><button type="button" data-confidence="mastered">I can explain this aloud</button></div>
        </div>
      </article>

      <article class="teach-back-card" data-card="norms">
        <header><span>04</span><h3>What is equivalent to de Vicente, and what is stronger multipartitely?</h3><em data-card-state>Not attempted</em></header>
        <label><span>Your explanation</span><textarea rows="5" placeholder="Separate the bipartite matrix statement from the higher-order tensor statement."></textarea></label>
        <button type="button" class="explain-button reveal-rubric" disabled>Compare with the essentials</button>
        <div class="teach-back-rubric" hidden>
          <p>A sound answer should make all three points:</p>
          <label><input type="checkbox"> For two Euclidean factors, the projective tensor norm equals the matrix nuclear norm.</label>
          <label><input type="checkbox"> Thus the uncentered bipartite projective-norm statement is exactly de Vicente in different language.</label>
          <label><input type="checkbox"> For three or more factors, each unfolding nuclear norm is only a lower bound on the full projective norm, so replacing unfoldings by the full norm can strengthen the test.</label>
          <div class="teach-back-confidence"><button type="button" data-confidence="review">I need another pass</button><button type="button" data-confidence="mastered">I can explain this aloud</button></div>
        </div>
      </article>

      <article class="teach-back-card" data-card="compatibility">
        <header><span>05</span><h3>What remains unresolved beyond the bipartite bound?</h3><em data-card-state>Not attempted</em></header>
        <label><span>Your explanation</span><textarea rows="5" placeholder="Explain why separate bounds at each tensor order are not enough."></textarea></label>
        <button type="button" class="explain-button reveal-rubric" disabled>Compare with the essentials</button>
        <div class="teach-back-rubric" hidden>
          <p>A sound answer should make all three points:</p>
          <label><input type="checkbox"> A multipartite state carries a family of subset tensors, not only the top-order tensor.</label>
          <label><input type="checkbox"> Separate decompositions for different orders do not prove that one separable ensemble generates them all.</label>
          <label><input type="checkbox"> The remaining problem is a common-moment or common-decomposition constraint across tensor orders.</label>
          <div class="teach-back-confidence"><button type="button" data-confidence="review">I need another pass</button><button type="button" data-confidence="mastered">I can explain this aloud</button></div>
        </div>
      </article>
    </div>
  </section>

  <section class="explain-stage" id="viva" aria-labelledby="viva-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 3</span><h2 id="viva-heading">Defend it in a mini-viva</h2></div>
      <p>Answer aloud before revealing the model answer. The next question is chosen from the conceptual points readers most often blur.</p>
    </div>

    <div class="viva-card">
      <p class="viva-count" id="viva-count">Question 1</p>
      <h3 id="viva-question">Why does a product state give a rank-one correlation matrix?</h3>
      <button type="button" class="explain-button" id="reveal-viva">Reveal the answer</button>
      <div class="viva-answer" id="viva-answer" hidden></div>
      <div class="viva-rating" id="viva-rating" hidden>
        <span>How did your answer compare?</span>
        <button type="button" data-viva-rating="missed">Missed</button>
        <button type="button" data-viva-rating="partial">Partial</button>
        <button type="button" data-viva-rating="correct">Correct</button>
      </div>
    </div>
    <div class="viva-score" aria-live="polite"><strong id="viva-score">0</strong><span>answers rated correct</span></div>
  </section>

  <section class="explain-stage" id="oral-rehearsal" aria-labelledby="rehearsal-heading">
    <div class="explain-stage-heading">
      <div><span>Stage 4</span><h2 id="rehearsal-heading">Give the explanation</h2></div>
      <p>Choose a length, speak without notes, then inspect the outline. You can record yourself, but the audio remains on this device and disappears when the page is closed.</p>
    </div>

    <div class="rehearsal-grid">
      <div class="rehearsal-controls">
        <fieldset>
          <legend>Length</legend>
          <label><input type="radio" name="rehearsal-length" value="90" checked> 90 seconds</label>
          <label><input type="radio" name="rehearsal-length" value="180"> 3 minutes</label>
          <label><input type="radio" name="rehearsal-length" value="300"> 5 minutes</label>
        </fieldset>
        <label class="local-profile-field"><span>Name for this local profile <small>(optional)</small></span><input type="text" id="learner-name" autocomplete="name" maxlength="80" placeholder="Your name"></label>
        <div class="rehearsal-buttons">
          <button type="button" class="explain-button" id="start-rehearsal">Start timer</button>
          <button type="button" class="explain-button explain-button-secondary" id="record-rehearsal">Record audio</button>
          <button type="button" class="explain-button explain-button-secondary" id="finish-rehearsal" disabled>Finish</button>
        </div>
        <p id="recording-status" class="explain-feedback" role="status" aria-live="polite"></p>
      </div>
      <div class="rehearsal-timer">
        <span>Time remaining</span>
        <strong id="rehearsal-clock" role="timer">01:30</strong>
        <p>Explain the result to a colleague who knows density matrices but has not read the article.</p>
      </div>
    </div>
    <audio id="rehearsal-audio" controls hidden></audio>

    <details class="rehearsal-outline" id="rehearsal-outline">
      <summary>Open the comparison outline after speaking</summary>
      <ol>
        <li><strong>Set up:</strong> define the Bloch vectors $r,s$, correlation matrix $T$, and centered matrix $C$.</li>
        <li><strong>Product and mixture:</strong> explain $T=rs^{\mathsf T}$ for a product state and the common convex decomposition for a separable state.</li>
        <li><strong>Center:</strong> derive $C=\sum_kp_k(r_k-r)(s_k-s)^{\mathsf T}$.</li>
        <li><strong>Bound:</strong> use the rank-one norm identity, triangle inequality, Cauchy–Schwarz, and the local variance deficits.</li>
        <li><strong>Locate the result:</strong> bipartitely, the projective norm is the nuclear norm; multipartitely, the full projective norm can be stronger than unfoldings.</li>
        <li><strong>State the open point:</strong> several tensor orders must come from one common separable ensemble.</li>
      </ol>
    </details>
  </section>

  <section class="explain-readiness" aria-labelledby="readiness-heading">
    <div>
      <p class="explain-kicker">Self-assessed readiness</p>
      <h2 id="readiness-heading">Ready means you can reconstruct, not recognize.</h2>
      <p id="readiness-copy">Complete all four stages to mark this article as ready to explain.</p>
    </div>
    <div class="readiness-actions">
      <button type="button" class="explain-button" id="mark-ready" disabled>Mark as ready to explain</button>
      <button type="button" class="explain-button explain-button-secondary" id="export-progress">Export progress</button>
      <label class="explain-import-button">Import progress<input type="file" id="import-progress" accept="application/json,.json"></label>
      <button type="button" class="explain-text-button" id="reset-progress">Reset this browser’s progress</button>
    </div>
    <p id="readiness-status" role="status" aria-live="polite"></p>
  </section>

  <p class="explain-source-note">Need to check a detail? Every stage corresponds to a passage in <a href="{{ '/2026/07/17/centered-correlation-tensors-separability/' | relative_url }}">Centered Correlation Tensors and Quantum Separability</a>. Use the article after attempting the prompt, not before.</p>
</div>
