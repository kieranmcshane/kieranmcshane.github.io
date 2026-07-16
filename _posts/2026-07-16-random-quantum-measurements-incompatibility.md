---
layout: post
title: "When Quantum Measurements Refuse to Share a Table"
subtitle: "Compatibility, noise robustness, and why randomness can be nearly extremal"
date: 2026-07-16 09:00:00 +0200
categories: [quantum-information]
tags: [POVMs, incompatibility, random-matrices, free-probability]
excerpt: "Quantum incompatibility is an operator-valued marginal problem. That viewpoint leads from Pauli measurements to a sharp phase diagram for random projections."
---

Quantum incompatibility is often introduced with a slogan: noncommuting observables cannot be measured simultaneously. The slogan is useful, but it hides a more general—and more visual—question:

> Can the statistics of several measurements arise as the marginals of one larger measurement?

This turns incompatibility into an operator-valued marginal problem. It also suggests a quantitative question: how much random noise must be added before a joint measurement becomes possible? From there, a surprising landscape appears. Two Pauli measurements have a clean geometric obstruction. Large families of anticommuting observables attain universal bounds. In high dimension, random measurements can approach those bounds without being designed to do so.

## Measurements as positive operator partitions

A quantum measurement with $k$ outcomes on $\mathbb C^d$ is described by a positive operator-valued measure (POVM)

$$
A=(A_1,\ldots,A_k),
\qquad A_i\succeq0,
\qquad \sum_{i=1}^k A_i=I_d.
$$

If the system is in state $\rho$, the Born rule gives

$$
\Pr(i\mid\rho)=\operatorname{Tr}(\rho A_i).
$$

For a binary measurement, only one effect is independent:

$$
A=(A_+,A_-)=(A_+,I-A_+).
$$

It is convenient to recenter it as

$$
X=A_+-A_-=2A_+-I.
$$

Then $X=X^*$ and $-I\preceq X\preceq I$. Conversely, $A_\pm=(I\pm X)/2$. A projective binary measurement has $X^2=I$ and eigenvalues $\pm1$.

## Compatibility is an operator-valued coupling

Let $A=(A_i)_{i=1}^k$ and $B=(B_j)_{j=1}^{\ell}$. They are compatible if positive operators $C_{ij}$ exist such that

$$
\sum_j C_{ij}=A_i,
\qquad
\sum_i C_{ij}=B_j.
$$

Think of $C=(C_{ij})$ as an operator-valued contingency table. Its row totals reproduce $A$ and its column totals reproduce $B$. For every state $\rho$,

$$
p_\rho(i,j)=\operatorname{Tr}(\rho C_{ij})
$$

is an ordinary joint distribution with the correct marginals.

The words **for every state** carry the quantum content. Two classical distributions can always be coupled. Quantum compatibility asks for one positive operator table that produces the right distributions simultaneously for every input state.

This is why Sudoku is only a loose analogy. Sudoku has discrete symbols and fixed clues. Here every cell is an unknown positive matrix constrained by operator-valued row and column totals. “Positive coupling problem” is closer to the mathematics.

## Commutation gives a joint measurement

Suppose every $A_i$ commutes with every $B_j$. Set

$$
C_{ij}=A_iB_j.
$$

The marginal equations follow immediately. Positivity is the only subtle point: products of positive matrices are not generally positive, or even Hermitian. Under commutation,

$$
A_iB_j=B_j^{1/2}A_iB_j^{1/2}\succeq0.
$$

This embeds the familiar statement about commuting sharp observables inside the more general POVM framework.

## The simplest obstruction: Pauli $X$ and $Z$

Consider the qubit measurements

$$
A=(|0\rangle\langle0|,|1\rangle\langle1|),
\qquad
B=(|+\rangle\langle+|,|-\rangle\langle-|).
$$

Their centered observables are $Z$ and $X$. If a joint table existed, its upper-left entry would satisfy

$$
0\preceq C_{++}\preceq|0\rangle\langle0|,
\qquad
0\preceq C_{++}\preceq|+\rangle\langle+|.
$$

A positive operator dominated by a rank-one projection must be supported on that projection’s range. Thus $C_{++}$ would have to live simultaneously in $\operatorname{span}\{|0\rangle\}$ and $\operatorname{span}\{|+\rangle\}$. Those distinct one-dimensional subspaces intersect only at zero, so $C_{++}=0$. The same argument kills every cell, contradicting $\sum_{a,b}C_{ab}=I$.

Geometrically, every joint cell must live inside both its row subspace and its column subspace. For sharp $X$ and $Z$, there is nowhere nonzero for it to live.

## Noise buys compatibility by time-sharing

For a $k$-outcome POVM $A$, add uniform white noise:

$$
A_i^{(t)}=tA_i+(1-t)\frac{I}{k},
\qquad 0\leq t\leq1.
$$

With probability $t$, one performs $A$; with probability $1-t$, one ignores the state and reports a uniformly random outcome. Define

$$
\tau(A,B)=\max\{t:A^{(t)}\text{ and }B^{(t)}\text{ are compatible}\}.
$$

Every pair satisfies $\tau(A,B)\geq1/2$. Indeed,

$$
C_{ij}=\frac{A_i}{2\ell}+\frac{B_j}{2k}
$$

is a parent POVM for the half-noisy measurements. Operationally, flip a fair coin. If it chooses $A$, genuinely measure $A$ and invent a uniform $B$ outcome; if it chooses $B$, do the reverse. Noise gives the apparatus permission to perform one measurement and fabricate the missing answer.

For $g$ arbitrary POVMs, the same time-sharing protocol gives the universal bound $t=1/g$.

Binary measurements do better. Every $g$-tuple of binary POVMs becomes compatible by $t=1/\sqrt g$. Pairwise anticommuting Clifford observables show this can be sharp when the Hilbert-space dimension is large enough. If

$$
\Gamma_x\Gamma_y+\Gamma_y\Gamma_x=0\quad(x\neq y),
$$

then

$$
\left(\sum_x s_x\Gamma_x\right)^2
=\left(\sum_xs_x^2\right)I.
$$

They behave like exactly perpendicular directions in operator space.

## Three ways to randomize a measurement

There is no unique “uniform random POVM.” Three natural ensembles answer different questions.

1. **Random binary projective measurements.** Choose a Haar-random subspace $E\subset\mathbb C^d$ of prescribed dimension and measure $(P_E,I-P_E)$.
2. **Random basis measurements.** Draw a Haar-random unitary $U$ and measure the rank-one projections onto its columns.
3. **Random induced POVMs.** Draw a Haar-random isometry $V:\mathbb C^d\to\mathbb C^k\otimes\mathbb C^n$ and set

   $$
   M_i=V^*(|i\rangle\langle i|\otimes I_n)V.
   $$

The first model gives sharp yes/no questions. The second gives a complete $d$-outcome basis readout. The third produces generally unsharp effects and models a system interacting with an environment. Haar invariance is shared; the compatibility thresholds are not.

## A phase diagram for two random projections

Let $E,F\subset\mathbb C^d$ be independent uniformly random subspaces with

$$
\dim E=\lfloor\alpha d\rfloor,
\qquad
\dim F=\lfloor\beta d\rfloor,
$$

and let $\mathsf P_E=(P_E,I-P_E)$ and $\mathsf P_F=(P_F,I-P_F)$. If

$$
\left(\alpha-\frac12\right)^2+
\left(\beta-\frac12\right)^2\leq\frac14,
$$

then, in probability as $d\to\infty$,

$$
\tau(\mathsf P_E,\mathsf P_F)\longrightarrow\frac1{\sqrt2}.
$$

Because $1/\sqrt2$ is the universal minimum for a binary pair, these random measurements are asymptotically maximally incompatible throughout the disk—not only at the balanced point $(1/2,1/2)$.

### Why a circle appears

The squared cosines of the nontrivial principal angles between $E$ and $F$ asymptotically fill an interval with endpoints

$$
\lambda_{\alpha,\beta}^{\pm}
=\alpha+\beta-2\alpha\beta
\pm2\sqrt{\alpha(1-\alpha)\beta(1-\beta)}.
$$

The disk condition is equivalent to

$$
\lambda^-_{\alpha,\beta}\leq\frac12\leq\lambda^+_{\alpha,\beta}.
$$

In other words, the limiting principal-angle spectrum reaches $\pi/4$. One can then find a two-dimensional compression on which $A=2P_E-I$ is exactly Pauli $Z$ and $B=2P_F-I$ approaches Pauli $X$.

Compatibility cannot be improved by compression: a parent measurement upstairs would compress to a parent measurement downstairs. The embedded Pauli pair therefore gives the upper bound $1/\sqrt2$; the universal binary theorem gives the matching lower bound.

This mechanism differs from Clifford anticommutation. Random projections almost surely do not anticommute globally. They instead contain a small, asymptotically Pauli-like witness.

The circle marks a robustness transition, not a transition between compatible and incompatible sharp measurements. Nontrivial independent random projections are generically noncommuting—and hence incompatible—on both sides. Outside the disk they are simply less resistant to white noise. Along $\alpha=\beta$, the exterior limit is known explicitly; the full off-diagonal exterior remains open.

## Many random binary measurements

Now take $g$ independent balanced random projections, $\operatorname{rank}P_x=d/2$, and let $A_x=2P_x-I$. For fixed $g$, free probability yields

$$
\limsup_{d\to\infty}\tau(\mathsf P_1,\ldots,\mathsf P_g)
\leq\frac{2\sqrt{g-1}}{g}
\sim\frac2{\sqrt g}
$$

almost surely.

Each $A_x$ has the symmetric Bernoulli spectral law

$$
b=\frac12(\delta_{-1}+\delta_1).
$$

Independent Haar conjugates become asymptotically free. For fixed signs $\varepsilon_x$, the signed sum $\sum_x\varepsilon_xA_x$ therefore has limiting law $b^{\boxplus g}$, the Kesten–McKay distribution, whose support ends at $2\sqrt{g-1}$.

That spectral edge normalizes an incompatibility witness. Taking $s=1/(2\sqrt{g-1})$, its pairing with the visibility-$t$ measurements is $stg$. Incompatibility is certified once $stg>1$, producing the bound above.

The result is within a factor two of the universal lower bound $1/\sqrt g$. It proves the optimal scale, not the sharp constant. The conjecture is that balanced Haar-random binary PVMs actually converge to $1/\sqrt g$ for every fixed $g$. For $g=2$, the free-probability bound is trivial; the principal-angle compression is what recovers the exact $1/\sqrt2$.

## What incompatibility buys operationally

Compatible measurements are simulations of one parent measurement followed by classical post-processing. Incompatible measurements can outperform every compatible strategy in suitable state-discrimination and communication tasks. Generalized incompatibility robustness has an exact interpretation as an optimal discrimination advantage.

The uniform-noise degree used here answers a particularly concrete experimental question: what fraction of the original measurement can survive depolarization before a joint simulation becomes possible? Its operational ordering need not coincide with every other noise model, which is one reason the choice of robustness measure matters.

## What remains unresolved

Several clean questions survive the asymptotic results:

- Is the conjectured polar-plus-equatorial configuration optimal for four binary qubit measurements?
- Do $g$ balanced random binary PVMs reach the exact value $1/\sqrt g$ for every fixed $g$?
- What is the limiting function $\tau(\alpha,\beta)$ throughout the off-diagonal exterior of the central disk?
- Can the two-projection convergence be made quantitatively useful at moderate dimension, especially on the boundary?
- Can the gap between compatibility and incompatibility thresholds for induced random POVMs be closed?
- Which operational tasks are controlled specifically by uniform white-noise robustness rather than generalized robustness?

The larger lesson is already visible. Carefully engineered Pauli strings are not the only route to extreme quantum behavior. In high dimension, randomness can place a maximally incompatible qubit witness inside a much larger measurement—or reproduce the optimal many-measurement scale through free spectral geometry.

## References

- Andreas Bluhm and Ion Nechita, [*Joint measurability of quantum effects and the matrix diamond*](https://arxiv.org/abs/1807.01508), 2018.
- Andreas Bluhm, Cécilia Lancien, and Ion Nechita, [*Random measurements are almost maximally incompatible*](https://arxiv.org/abs/2507.20600), 2025.
- Jessica Bavaresco et al., [*Most incompatible measurements for robust steering tests*](https://arxiv.org/abs/1704.02994), 2017.
- Paul Skrzypczyk, Ivan Šupić, and Daniel Cavalcanti, [*All sets of incompatible measurements give an advantage in quantum state discrimination*](https://arxiv.org/abs/1901.00816), 2019.
