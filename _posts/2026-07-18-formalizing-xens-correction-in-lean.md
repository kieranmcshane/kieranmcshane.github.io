---
layout: post
title: "Formalizing an X/ENS Correction in Lean"
subtitle: "What changed when the proof had to compile"
date: 2026-07-18 10:00:00 +0200
categories: [formalization]
tags: [Lean, mathlib, random-matrices, semicircle-law, concours]
excerpt: "A field report from turning an X/ENS 2026 Mathematics B correction into a no-sorry Lean project."
---

I have been working on a Lean formalization of an X/ENS 2026 Mathematics B correction. The project began as a scaffold: a way of translating a long written solution into named definitions, lemmas and theorem targets. It has now become something more useful. Large parts of the argument compile, the remaining assumptions are explicit, and the last Wigner-model probability suppliers have been moved from informal labels to Mathlib-usable hypotheses.

That is the interesting part. Lean did not merely check that the final line was plausible. It forced the proof to say what kind of mathematical object each sentence was using.

Was a statement a direct theorem? Was it an analytic theorem still imported through an interface? Was an independence assumption just a `Prop`-shaped label, or was it in a form that Mathlib's probability library could actually use? These distinctions are easy to blur in prose. They are much harder to blur in a file that has to build.

## Reading guide

- [The shape of the correction](#the-shape-of-the-correction) explains the four mathematical blocks.
- [What Lean forced into the open](#what-lean-forced-into-the-open) describes the main modelling lesson.
- [The Wigner gap](#the-wigner-gap) gives the concrete probability case study.
- [What is actually verified](#what-is-actually-verified) separates compiled proof from explicit assumptions.
- [What remains useful](#what-remains-useful) explains why this matters beyond this single exam correction.

## Small glossary

These are the terms I will use in a precise way.

<div class="notation-glossary">
  <dl>
    <dt id="definition-proof-obligation" class="definition-target">Proof obligation</dt>
    <dd>A mathematical fact that Lean still needs before a theorem can compile.</dd>

    <dt id="definition-api-boundary" class="definition-target">API boundary</dt>
    <dd>An explicit local interface collecting assumptions that are not yet proved directly in the current file.</dd>

    <dt id="definition-supplier" class="definition-target">Supplier theorem</dt>
    <dd>A theorem that fills such an interface from more concrete hypotheses.</dd>

    <dt id="definition-no-sorry" class="definition-target">No-sorry</dt>
    <dd>A Lean file or project with no `sorry` placeholders, no `admit`, and no project-specific axioms.</dd>

    <dt id="definition-wigner-input" class="definition-target">Wigner input</dt>
    <dd>The probabilistic data describing the entries of the random matrix.</dd>
  </dl>
</div>

## The shape of the correction

The correction has four large mathematical layers.

The first layer is deterministic analysis. It includes Riemann sums, the arcsine density and the cosine-grid parametrization

$$
x = 2\cos\theta.
$$

This is the analytic backbone of the early questions. It turns discrete averages over eigenvalue grids into integrals against the arcsine law.

The second layer is linear algebra. The tridiagonal path matrix and the more general Toeplitz matrix have explicit eigenvalue grids. In prose, this is where one writes down sine eigenvectors and recognizes the characteristic polynomial. In Lean, it means proving that the matrix action really reduces to left and right neighbors, that the proposed eigenvectors are nonzero, that the eigenvalues are distinct, and that the list is complete.

The third layer is approximation. The correction uses a constructive route rather than appealing directly to a black-box Weierstrass theorem. The basic polynomial gadget is

$$
Q_n(X) = (1-X^n)^{2^n},
$$

then a shifted version is used to approximate step functions. That is not the shortest possible written proof, but it is excellent for formalization: the approximants are explicit and the error estimates have named locations.

The fourth layer is probabilistic. It is the route from Wigner matrices to the semicircle law. The spectral average of a test function is reduced to normalized traces of powers, monomial concentration is proved by variance estimates, and polynomial approximation bridges from monomials to compactly supported continuous functions.

The high-level endpoint has the familiar shape:

$$
\Pr\left(\left|S_n(f)-\Sigma(f)\right|\geq\varepsilon\right)\longrightarrow 0.
$$

Here $S_n(f)$ is the empirical spectral average and $\Sigma(f)$ is the semicircle functional. But the real formalization work lies in the sentence before this one: which hypotheses make the moment and concentration arguments legal?

## What Lean forced into the open

The first version of the Wigner model had fields such as independence, identical distribution, mean zero, variance one and finite moments. Mathematically, that sounds reasonable. Formally, it was too weak.

The issue is not philosophical. It is type-theoretic and practical. A field saying

```lean
independent_upper : Prop
```

does not by itself give Lean a theorem of type `iIndepFun`. A field saying that all moments are finite does not give Lean an `Integrable` term for the particular finite product of entries appearing in a normalized trace. A field saying variance one does not automatically produce the exact integral identity needed for an expectation calculation.

So the important move was to separate two objects.

The abstract model, called `WignerInput`, is still useful for the conditional proof graph. It lets the later theorems say: if the moment hypotheses and integrability suppliers are available, then the concentration and semicircle arguments go through.

The concrete model, called `WignerInputConcrete`, is stricter. Schematically, it records hypotheses in the language Mathlib can consume:

```lean
structure WignerInputConcrete
    (Omega : Type*) [MeasurableSpace Omega] (mu : Measure Omega) where
  Wz : Nat -> Nat -> Omega -> Int
  entry_measurable :
    forall i j, Measurable (fun omega => (Wz i j omega : Real))
  entry_integrable_abs_pow :
    forall i j k, Integrable (fun omega => |(Wz i j omega : Real)| ^ k) mu
  entry_mean_zero :
    forall i j, i <= j -> integral mu (fun omega => (Wz i j omega : Real)) = 0
  entry_second_moment_one :
    forall i j, i <= j ->
      integral mu (fun omega => ((Wz i j omega : Real) ^ 2)) = 1
  upper_independent :
    ProbabilityTheory.iIndepFun (fun p : UpperPair => upperRealOf Wz p) mu
  upper_identDistrib :
    forall p q : UpperPair,
      ProbabilityTheory.IdentDistrib (upperRealOf Wz p) (upperRealOf Wz q) mu mu
  entry_fourth_moment_bound :
    exists C : Real, 0 <= C
      /\ forall i j, i <= j ->
        integral mu (fun omega => |(Wz i j omega : Real)| ^ 4) <= C
```

This is less elegant than the informal sentence "take independent centered entries with variance one and bounded fourth moment." It is also much more useful. Each field is now shaped so that a later theorem can actually apply it.

That is the role of an <a class="concept-ref" href="#definition-api-boundary" data-definition="API boundary: an explicit local interface collecting assumptions that have not yet been proved directly here.">API boundary</a>. It is not a hidden proof. It is a labelled border between what has already been reduced and what still needs to be supplied.

## The Wigner gap

The recent improvement closed two specific suppliers.

The first one is

```lean
theorem lowDegreeMomentAPI
    (W : WignerInputConcrete Omega mu) :
    LowDegreeMomentAPI W.toWignerInput
```

This packages the low-degree moment information needed downstream. The delicate part is the degree-two second moment:

$$
\mathbb E\left[\left(\frac{\operatorname{Tr}(X_n^2)}{n}\right)^2\right]
\longrightarrow 1.
$$

In prose, one often waves at independence and says the variance vanishes. Lean wanted the actual random variable.

For the symmetric Wigner matrix, the normalized quadratic trace can be rewritten as a weighted sum over upper-triangular entries:

$$
\frac{\operatorname{Tr}(X_n^2)}{n}
=
\frac{1}{n^2}\sum_{i\leq j} c_{ij} W_{ij}^2,
$$

where diagonal and off-diagonal terms have different weights. Once the expression has this form, Mathlib's independence API can be used to prove that the variance of the sum is the sum of the variances. The bounded fourth moment controls each summand. The number of upper-triangular entries is $O(n^2)$, while the normalization contributes $n^{-4}$, so the variance is $O(n^{-2})$.

That proves concentration of the quadratic trace around its expectation. The expectation itself is one. Therefore the second moment tends to one.

The second supplier is

```lean
theorem snMonomialIntegrability
    (W : WignerInputConcrete Omega mu) :
    SnMonomialIntegrability W.toWignerInput
```

This may sound minor, but it is exactly the sort of fact that informal proofs tend to spend without naming. A normalized trace of a power of a random matrix is a finite sum of finite products of entries. Its square is another finite sum of such products. To integrate them, Lean needs moment integrability for those products. The proof uses the concrete entry moment fields and Holder-style product estimates to produce the required integrability statements.

Together, these two <a class="concept-ref" href="#definition-supplier" data-definition="Supplier theorem: a theorem that fills an explicit interface from more concrete hypotheses.">supplier theorems</a> turn the final Wigner part from "morally available" into something the probability layer can consume.

## What is actually verified

The current project builds against Lean 4.29.1 and Mathlib 4.29.1. The relevant status snapshot is:

```text
lake build
Build completed successfully

grep audit over XENS2026MB:
no sorry, no admit, no project-specific axiom, no unsafe

axiom audit for the new Wigner suppliers:
propext, Classical.choice, Quot.sound
```

The last line is the usual foundational footprint inherited from Lean and Mathlib. It is not a project-specific mathematical axiom.

That said, "<a class="concept-ref" href="#definition-no-sorry" data-definition="No-sorry: no Lean placeholder proofs such as sorry/admit and no project-specific axioms.">no-sorry</a>" does not mean "every theorem in the written correction has been reproved from first principles in one file." Some analytic parts remain behind explicit interfaces. For instance, parts of the arcsine integral and cosine-grid distribution story are recorded as named APIs. The point is that these assumptions are not invisible. They occur as theorem parameters or typeclass assumptions, and the manifest records where they enter.

This is the difference between a fake completion and an auditable one. A fake completion hides the missing theorem behind a placeholder. An auditable completion says:

> This theorem is proved, conditional on these exact mathematical inputs.

Then one can choose the next target intelligently.

## Why the architecture matters

The project has a ticket ledger rather than only a collection of files. The tickets distinguish several statuses:

- `done`: proved directly or fully supplied in the canonical repository.
- `api-done`: available through an explicit local interface.
- `model-gap`: not derivable from the current model fields without strengthening the model.
- `frontier`: mathematically intended, not yet a theorem.

This may look bureaucratic, but it is how a large formalization stays legible. A concours solution is not a single theorem. It is a dependency graph. The ledger says which leaves of the graph are closed, which are abstracted, and which were modelling mistakes.

The most useful example was the <a class="concept-ref" href="#definition-wigner-input" data-definition="Wigner input: the probabilistic entry data used to build the random matrix model.">Wigner input</a>. The initial model described the mathematics in ordinary language. The concrete model described it in a way Lean could use. That change did not alter the intended theorem; it changed the proof object enough for the theorem to become checkable.

Another example is the constructive polynomial approximation in Part III. The project deliberately avoids using Weierstrass as a black box. It constructs step approximations, then replaces jumps by the explicit polynomials $P_n$. This makes the proof longer, but it also makes it more diagnostic. If a bound fails, it fails at a named interval, a named jump, or a named coefficient estimate.

The linear algebra layer has the same flavor. Saying "the sine vectors are eigenvectors" is short. Proving it in Lean means naming the neighbor-action reduction, the boundary sine identities, the nonzero vector proof, the injectivity of eigenvalues and the characteristic-polynomial completeness argument.

## What changed in the written correction

The formalization also fed back into the PDF correction. Several prose passages became more precise because Lean had forced a sharper dependency.

The Wigner section now separates:

1. low-degree moment computations;
2. monomial concentration;
3. polynomial concentration;
4. tail estimates outside a compact interval;
5. final compact-supported semicircle convergence.

That order matters. Polynomial concentration is not magic. It is a finite linear combination of monomial concentration statements. Compact-supported convergence is not only polynomial approximation. It also needs the tail term and the semicircle functional to be controlled on the chosen compact interval.

The Lean theorem `q17a_reduction` makes this budget visible. It chooses a polynomial $P$ and an index $N$, then reduces the final probability estimate to two events: one tail event and one centered polynomial event. The written correction can now follow that same structure instead of compressing the whole argument into a paragraph.

## A small philosophical lesson

There is a common misunderstanding about formalization: that the main benefit is catching arithmetic mistakes or forcing every proof to become unreadably low-level. That is not the experience here.

The main benefit was calibration.

Lean asked whether the hypotheses were strong enough to apply the theorem I wanted to apply. It asked whether an average at $n=0$ had accidentally been confused with a normalized spectral average for $n>0$. It asked whether "independent" meant a sentence in a human proof or a term of the right Mathlib type. It asked whether integrability of entries automatically implied integrability of traces, and refused to pretend that it did until the product argument was written.

Those questions are not clerical. They are mathematical hygiene.

## What remains useful

The project is now useful in three ways.

First, it is a checked map of the correction. Even where an analytic input is still abstracted, the boundary is explicit.

Second, it is a source of better prose. The proof dependencies discovered by Lean are exactly the dependencies a careful written solution should make visible.

Third, it gives a practical workflow for formalizing long exam solutions: begin with a scaffold, remove placeholders, replace informal model fields by usable hypotheses, and keep a public manifest of what is direct, conditional and still frontier.

The most recent Wigner work is a good example of that workflow. The final theorem did not change its mathematical meaning. What changed is that two assumptions that used to live in the fog now have concrete suppliers:

```lean
WignerInputConcrete.lowDegreeMomentAPI
WignerInputConcrete.snMonomialIntegrability
```

That is not glamorous. It is better than glamorous: it is the kind of progress that makes the next proof possible.
