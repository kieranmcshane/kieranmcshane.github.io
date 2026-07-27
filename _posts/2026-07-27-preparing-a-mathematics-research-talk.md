---
layout: post
math: true
title: "How I Prepare a Mathematics Research Talk"
subtitle: "A nine-stage workshop from raw notes to expert questions"
date: 2026-07-27 10:00:00 +0200
categories: [research-practice]
tags: [mathematics, research-talks, exposition, proof-writing, seminars]
excerpt: "A complete, exercise-based method for turning mathematical research notes into a precise, resilient and speakable seminar."
---

A mathematics talk is not a paper read aloud. It is a controlled sequence of mathematical decisions: what the audience must see first, which hypotheses have to remain visible, where an example should calibrate the abstraction, and what can safely move to backup.

The method below is the one I use to turn conversations, calculations and incomplete notes into a research presentation. It is deliberately stricter than “make some slides.” The talk is not ready merely when every theorem has a frame. It is ready when the main line can be reconstructed, challenged and spoken without the slides doing the reasoning on my behalf.

The workshop has nine stages and thirty exercises. The first twenty-seven build the talk; the last three test the whole object. Each stage ends with a concrete deliverable and a stopping rule.

## The governing principles

Five choices shape the entire method.

1. **Calibration before abstraction.** A small case tells the audience what the general objects are meant to do.
2. **Claims before decoration.** Every slide must earn its place through a mathematical move.
3. **Counterexamples before confidence.** A failed converse or missing hypothesis should be made explicit, not left for the seminar to discover.
4. **Bottom lines before transitions.** Each section ends with the exact fact the next section is allowed to use.
5. **Backups instead of digressions.** Technical branches remain available without breaking the main proof line.

The scope is mathematical. Travel, administration, software setup and other logistical matters belong in a separate checklist.

## How to use the workshop

For a new talk, work through the stages in order. For a revision, begin at the first stage whose stopping rule is not satisfied. Do not repair a weak mathematical spine by polishing later slides.

Keep four documents open:

- a **claim ledger** for statements, hypotheses and proof status;
- a **spine** containing only the main mathematical line;
- a **parking lot** for material removed from that line;
- a **question bank** for objections and expert follow-ups.

<nav class="talk-workshop-map" aria-label="Nine stages of the research talk workshop">
  <a href="#stage-1-clean-the-raw-material"><span>1</span> Clean</a>
  <a href="#stage-2-fix-the-target"><span>2</span> Target</a>
  <a href="#stage-3-build-the-conceptual-spine"><span>3</span> Spine</a>
  <a href="#stage-4-secure-every-claim"><span>4</span> Secure</a>
  <a href="#stage-5-red-team-the-mathematics"><span>5</span> Attack</a>
  <a href="#stage-6-stabilize-notation"><span>6</span> Notation</a>
  <a href="#stage-7-design-the-slides"><span>7</span> Slides</a>
  <a href="#stage-8-write-the-spoken-talk"><span>8</span> Script</a>
  <a href="#stage-9-rehearse-for-the-room"><span>9</span> Rehearse</a>
</nav>

<section class="talk-stage" id="stage-1-clean-the-raw-material" markdown="1">

## Stage 1 — Clean the raw material

Research notes preserve discovery, not exposition. They mix settled facts, guesses, failed routes, literature reminders and private shorthand. The first task is classification, not rewriting.

<div class="talk-exercise" markdown="1">

### Exercise 1 — The signal/noise pass

Read the source material once without editing it. Mark each item as one of:

- **result**: a statement the talk may use;
- **mechanism**: the idea explaining why the result should be true;
- **example**: a case that calibrates or tests the statement;
- **open**: a conjecture, question or unresolved calculation;
- **context**: literature or motivation;
- **discard**: repetition, logistics or an abandoned route.

**Done when:** every paragraph, board fragment or message has exactly one primary label.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 2 — The claim ledger

Turn every mathematical assertion into one row with five fields:

| Claim | Exact hypotheses | Status | Evidence | Role in talk |
|---|---|---|---|---|
| What is being asserted? | Under precisely what conditions? | proved / cited / computed / conjectural | proof, reference or calculation | main line / example / backup |

Split any row containing “and” into separate claims. Replace “clearly,” “usually” and “it follows” by the actual implication they hide.

**Done when:** no claim in the source material exists only as prose.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 3 — The five-minute reconstruction

Close the source material. On a blank page, reconstruct:

1. the problem;
2. the smallest useful example;
3. the main result;
4. the mechanism;
5. the remaining obstruction.

Compare this page with the claim ledger. Anything important that you could not reconstruct is either poorly understood or poorly organized.

**Done when:** the reconstruction and the ledger tell the same mathematical story.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> a classified source packet and a claim ledger with no unlabelled assertions.</p>

</section>

<section class="talk-stage" id="stage-2-fix-the-target" markdown="1">

## Stage 2 — Fix the target

A talk needs a promise: one mathematical gain the audience can reasonably obtain in the available time. “I will discuss my work on…” is a topic, not a promise.

<div class="talk-exercise" markdown="1">

### Exercise 4 — The one-sentence promise

Complete this sentence:

> By the end of the talk, the audience will understand why **[precise phenomenon or theorem]** follows from **[central mechanism]**, and where **[one honest limitation]** remains.

Remove every clause that introduces a second talk.

**Done when:** the sentence names an outcome, a mechanism and a boundary.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 5 — Audience subtraction

Write three lists for the actual audience:

- facts almost everyone may be assumed to know;
- facts some specialists know but must still be recalled;
- facts that are specific to this talk and must be taught.

Now remove one assumed prerequisite at a time. Ask what single calibration example or definition would repair the loss.

**Done when:** every prerequisite is either genuinely assumed or explicitly supplied.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 6 — The stopping rule

Write the last mathematical sentence of the talk before writing the first slide. It may be a theorem, a sharp obstruction or a well-posed open problem. Then list everything the audience must know for that sentence to be meaningful.

**Done when:** the endpoint determines the necessary content, rather than the notes determining how long the talk becomes.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> one promise, one audience model and one final mathematical sentence.</p>

</section>

<section class="talk-stage" id="stage-3-build-the-conceptual-spine" markdown="1">

## Stage 3 — Build the conceptual spine

The spine is the shortest sequence of mathematical moves that fulfills the promise. It is not yet a slide deck.

<div class="talk-exercise" markdown="1">

### Exercise 7 — Calibration before abstraction

Find the smallest case in which the central mechanism is visible. Work it out completely: compute the relevant objects, state what succeeds, and identify what the example cannot show.

Then write the general definition only after the example.

**Done when:** every symbol in the abstract definition has already performed a job in the calibration case.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 8 — The dependency spine

Put the endpoint at the bottom of a page. Above it, write only the statements it directly depends on. Continue upward until reaching standard background or the calibration example.

Delete branches that do not feed the endpoint. Move them to the parking lot.

**Done when:** the main line forms one connected dependency graph with no ornamental theorem.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 9 — Section bottom lines

For each block of the spine, write a boxed sentence of the form:

> **Bottom line:** from now on, we may use ______.

The sentence must contain a mathematical object, property or implication—not “we have gained intuition.”

**Done when:** concatenating the bottom lines reconstructs the entire talk at high speed.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> a calibration case, a dependency graph and a chain of mathematical bottom lines.</p>

</section>

<section class="talk-stage" id="stage-4-secure-every-claim" markdown="1">

## Stage 4 — Secure every claim

This stage converts plausible exposition into a talk that survives careful listening. The standard is not a fully written paper proof; it is that every displayed implication has a known source and legal hypotheses.

<div class="talk-exercise" markdown="1">

### Exercise 10 — The quantifier audit

Circle every quantifier in the main theorem and its supporting lemmas. For each one, ask:

- Is the statement uniform or pointwise?
- Does a constant depend on the dimension, parameter or chosen object?
- Is the order of limits fixed?
- Is an existence claim constructive, measurable or merely set-theoretic?

Read the statement aloud with all dependencies restored.

**Done when:** no parameter changes status silently between two slides.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 11 — The implication audit

For every arrow \(A\Rightarrow B\), try to write the converse. Classify it as:

- true;
- false with a known counterexample;
- true under an extra hypothesis;
- unknown.

Put the classification in the claim ledger, even if the converse never appears on a main slide.

**Done when:** the direction of every implication can be defended without relying on verbal emphasis.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 12 — Proof-status tagging

Assign each claim one visible internal tag:

- **P** — proved in the talk;
- **S** — sketched, with the missing step named;
- **C** — cited, with a precise source;
- **E** — supported by an explicit computation;
- **O** — open or conjectural.

Anything tagged **O** must never be spoken with theorem grammar.

**Done when:** every main-line claim has a status and every citation has a location.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> an audited claim ledger with explicit dependencies, directions and proof status.</p>

</section>

<section class="talk-stage" id="stage-5-red-team-the-mathematics" markdown="1">

## Stage 5 — Red-team the mathematics

Before a seminar audience attacks the argument, construct a more systematic adversary.

<div class="talk-exercise" markdown="1">

### Exercise 13 — The hypothesis deletion game

Remove the hypotheses of each main result one at a time. Search first in the smallest dimension, shortest time scale or simplest algebraic class. Record:

- the first hypothesis whose deletion breaks the result;
- the smallest counterexample you can exhibit;
- the exact line of the proof that fails.

**Done when:** every non-cosmetic hypothesis has either a failure witness or a structural justification.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 14 — The false-converse slide

Choose the converse most likely to be inferred by a listener. Build one compact backup slide containing:

1. the tempting false statement;
2. an explicit counterexample;
3. the corrected statement.

If the false inference is central, promote this slide into the main talk.

**Done when:** the audience cannot leave with the most dangerous wrong theorem.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 15 — The hostile seminar

For ten minutes, interrupt the talk after every mathematical sentence with one of:

- “Under which hypothesis?”
- “Why is that map well defined?”
- “Is this invariant under the natural equivalence?”
- “What happens in the smallest nontrivial case?”
- “Is that implication reversible?”
- “Where exactly is this proved?”

Add every answer longer than thirty seconds to the question bank or a backup slide.

**Done when:** objections improve navigation rather than reveal a missing mathematical dependency.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> a hypothesis-failure table, at least one explicit counterexample and a first expert question bank.</p>

</section>

<section class="talk-stage" id="stage-6-stabilize-notation" markdown="1">

## Stage 6 — Stabilize notation and separate side threads

Notation is part of the proof interface. A symbol that changes meaning forces the audience to recompute the argument.

<div class="talk-exercise" markdown="1">

### Exercise 16 — The symbol census

List every symbol that appears on a main slide. For each, record:

- its type or ambient space;
- the slide where it is introduced;
- its spoken name;
- whether it changes with an index, parameter or choice.

Delete one-use notation unless it shortens a genuinely repeated expression.

**Done when:** no symbol appears before its introduction or survives after its purpose.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 17 — The collision test

Search for symbols that differ only by typography: \(X\) and \(\mathcal X\), \(l\) and \(1\), \(O\) and \(0\), subscripts that disappear when spoken. Replace them or make the distinction semantic and audible.

Then test the notation in grayscale and from the back of a room.

**Done when:** every important distinction survives both speech and imperfect projection.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 18 — Main line, parking lot, backup

Assign every item outside the spine to one of:

- **delete** — not needed for this talk;
- **parking lot** — valuable for another exposition;
- **backup** — likely to answer a concrete question.

A backup slide needs a trigger: write the question that would cause you to open it.

**Done when:** no side thread remains in the main talk merely because it was difficult to derive.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> a notation sheet and a backup deck indexed by actual questions.</p>

</section>

<section class="talk-stage" id="stage-7-design-the-slides" markdown="1">

## Stage 7 — Design the slides

Only now does the spine become a visual sequence. Slide design is a mathematical compression problem.

<div class="talk-exercise" markdown="1">

### Exercise 19 — One intellectual move per slide

Give each planned slide a verb: **define**, **compute**, **compare**, **bound**, **contradict**, **conclude**. If a slide needs two unrelated verbs, split it. If two consecutive slides have the same verb and object, consider merging them.

**Done when:** the sequence of slide verbs matches the dependency spine.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 20 — The headline test

Replace topic headings such as “Main theorem” or “Examples” with the mathematical point:

- “Centering removes the product of the means.”
- “The converse already fails in dimension three.”
- “One common decomposition must explain every order.”

Hide the slide body. The headlines alone should still tell a correct story.

**Done when:** the title of every content slide is a claim or an action, not a filing label.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 21 — The equation budget

For each displayed equation, identify the one part the audience must look at. Remove algebra that will not be discussed. Reveal a derivation in stages only when the order of transformations is itself the point.

Check that every equation can be read from the back of the room and does not require simultaneous narration of three lines.

**Done when:** each display has one visual task and one spoken interpretation.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> a complete slide sequence whose headlines and displays reproduce the mathematical spine.</p>

</section>

<section class="talk-stage" id="stage-8-write-the-spoken-talk" markdown="1">

## Stage 8 — Write the spoken talk

Slides expose objects; speech supplies causality. A usable script records transitions and emphasis, not every word that happens to be visible.

<div class="talk-exercise" markdown="1">

### Exercise 22 — The transition script

For every slide change, write two sentences:

1. what the previous slide established;
2. why the next mathematical move is necessary.

Avoid “Now we move on to…” The transition must carry a dependency.

**Done when:** the talk remains logically continuous during a blank screen.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 23 — Explain it without the frame

Choose the three densest slides. Hide each one and explain its point in sixty seconds using only the objects already introduced. Then show the slide and remove anything your explanation did not need.

**Done when:** the slide supports the explanation but is not the sole place where the reasoning exists.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 24 — The compression ladder

Explain the main theorem in three durations:

- **15 seconds:** the bottom line;
- **60 seconds:** mechanism plus limitation;
- **3 minutes:** definitions, mechanism and proof architecture.

The three versions must be consistent, not different stories.

**Done when:** an interruption can shorten the talk without changing its claims.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> a spoken script for every transition, emphasis point and planned compression.</p>

</section>

<section class="talk-stage" id="stage-9-rehearse-for-the-room" markdown="1">

## Stage 9 — Rehearse for the room

Rehearsal is where the mathematical object meets time, memory and interruption.

<div class="talk-exercise" markdown="1">

### Exercise 25 — Three timed passes

Run the talk at:

- **full length**, with the intended explanations;
- **85% length**, using planned compressions;
- **60% length**, preserving only calibration, mechanism, theorem and limitation.

Record the actual time of every section. Do not solve overruns by speaking faster.

**Done when:** you know exactly which complete mathematical units can be removed.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 26 — The interruption drill

Ask someone to interrupt at three unpredictable points. After answering, resume by stating:

1. the last established bottom line;
2. the current goal;
3. the next move.

Repeat alone by drawing random slide numbers if no partner is available.

**Done when:** an interruption changes the clock, not the logical state of the talk.

</div>

<div class="talk-exercise" markdown="1">

### Exercise 27 — The expert question bank

Prepare concise answers under five headings:

- normalization and conventions;
- edge cases and counterexamples;
- relation to the nearest literature;
- proof bottlenecks;
- strongest honest next result.

For each answer, decide whether it is spoken, written on a backup slide, or deferred with a precise reason.

**Done when:** the ten most likely expert questions have answers that do not overstate the mathematics.

</div>

<p class="talk-deliverable"><strong>Stage deliverable:</strong> a timed talk with planned cuts, interruption recovery and an indexed question bank.</p>

</section>

## Capstone exercises

These exercises test the finished talk as a single mathematical object.

<div class="talk-exercise talk-exercise-capstone" markdown="1">

### Exercise 28 — The ninety-minute rebuild

Starting from the claim ledger rather than the existing slides, rebuild the talk in ninety minutes:

1. write the promise;
2. select one calibration case;
3. draw the dependency spine;
4. retain only the indispensable bottom lines;
5. assign one slide to each intellectual move.

Compare the rebuilt version with the original. Any slide that disappears twice is probably not part of the talk.

</div>

<div class="talk-exercise talk-exercise-capstone" markdown="1">

### Exercise 29 — The contradiction audit

Give the slides, script and claim ledger to a skeptical reader. Ask them to find only:

- claims stronger than their evidence;
- silent changes of notation;
- hidden hypotheses;
- false converses encouraged by the exposition;
- open statements that sound proved.

Do not ask whether the talk is “clear” until these five searches are complete.

</div>

<div class="talk-exercise talk-exercise-capstone" markdown="1">

### Exercise 30 — The post-talk update

Within twenty-four hours of the seminar, record:

- the first point where the audience became lost;
- every question not answered cleanly;
- every slide that was skipped or rushed;
- every counterexample or reference supplied by the audience;
- one change to the reusable method.

Update the claim ledger and question bank before editing the slides. The next talk should inherit the mathematics learned in the room, not merely its typography.

</div>

## Compact worksheet

Copy this block at the start of a new presentation.

<div class="talk-template" markdown="1">

### Talk brief

- **Audience:**
- **Duration:**
- **Promise:**
- **Calibration case:**
- **Main mechanism:**
- **Final mathematical sentence:**
- **Honest limitation:**

### Spine

1. We begin from:
2. The first obstruction is:
3. The mechanism is:
4. The main result says:
5. The counterexample prevents:
6. The bottom line is:

### Integrity check

- [ ] Every main claim has exact hypotheses.
- [ ] Every implication direction has been audited.
- [ ] At least one tempting false converse has been tested.
- [ ] Notation is stable and speakable.
- [ ] Every section ends with a mathematical bottom line.
- [ ] Technical branches have question-indexed backup slides.
- [ ] The talk works at 100%, 85% and 60% length.
- [ ] The expert question bank is current.

</div>

## When the talk is ready

The talk is ready when four representations agree:

1. the **claim ledger** says what is true;
2. the **dependency spine** says what is necessary;
3. the **slides** make those necessities visible;
4. the **spoken script** makes the implications audible.

If these disagree, return to the earliest broken stage. If they agree, polishing becomes useful: it clarifies an already sound mathematical object instead of disguising an unstable one.
