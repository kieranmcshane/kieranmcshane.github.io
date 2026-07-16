---
layout: post
title: "Quantum Measurement Incompatibility, Step by Step"
subtitle: "From detector outcomes to random projections"
date: 2026-07-16 09:00:00 +0200
categories: [quantum-information]
tags: [POVMs, incompatibility, random-matrices, free-probability]
excerpt: "A guided introduction to quantum measurement incompatibility, from detector outcomes and effects to random projections and their asymptotic phase diagram."
---

Suppose a quantum measuring device has several possible readouts. Can we build one larger device whose output contains the readouts of two different measurements at once? This is the question of **measurement compatibility**.

The familiar slogan says that noncommuting observables cannot be measured simultaneously. The more general question is:

> Can the statistics of several measurements arise as the marginals of one larger measurement?

Notation often blurs the distinction between a measurement and one of its possible outcomes. The operator attached to that outcome adds another layer. We will introduce each piece separately.

## From outcomes to effects

Imagine that a device has $k$ possible outcomes. We label them

$$
i=1,\ldots,k.
$$

Using the device once returns one label $i$. It names the event “outcome $i$ occurred,” just as “heads” names a coin-toss outcome. Quantum theory associates this outcome with an operator $A&#95;i$, called an **effect**. It satisfies

$$
0\preceq A_i\preceq I.
$$

The first inequality says that $A&#95;i$ is positive. The second says that $I-A&#95;i$ is positive. Equivalently, the eigenvalues of $A&#95;i$ lie between zero and one. If the system is prepared in state $\rho$, then the probability of outcome $i$ is

$$
\Pr(i\mid\rho)=\operatorname{Tr}(\rho A_i).
$$

Here $\rho$ is a density matrix, meaning a positive operator with trace one. It is fixed in this setup; the measurement outcome $i$ is random. Positivity gives

$$
\operatorname{Tr}(\rho A_i)
=\operatorname{Tr}(\rho^{1/2}A_i\rho^{1/2})\geq0.
$$

Applying the same argument to $I-A&#95;i$ gives

$$
0\leq\operatorname{Tr}\!\bigl(\rho(I-A_i)\bigr)
=1-\operatorname{Tr}(\rho A_i),
$$

so $\operatorname{Tr}(\rho A&#95;i)\leq1$. The Born-rule expression therefore lies between zero and one for every state. This establishes the allowed range for one outcome. It does not yet show that the probabilities of all outcomes sum to one.

An effect tells us the probability of one outcome. It does not, by itself, tell us the state of the system after that outcome occurs. Describing the state change requires extra information, such as a quantum instrument or Kraus operators.

An effect need not be a projection. If $A&#95;i^2=A&#95;i$, then it is a projection and represents a sharp outcome. A measurement made entirely of projections is called projective or sharp. General effects also describe imperfect or deliberately noisy readouts.

The entire measurement is the collection of its effects:

$$
A=(A_1,\ldots,A_k),
\qquad A_i\succeq0,
\qquad \sum_{i=1}^k A_i=I_d.
$$

The condition $\sum&#95;i A&#95;i=I$ is called **completeness**. It supplies the missing normalization:

$$
\sum_{i=1}^k \Pr(i\mid\rho)
=\sum_{i=1}^k\operatorname{Tr}(\rho A_i)
=\operatorname{Tr}\!\left(\rho\sum_{i=1}^k A_i\right)
=\operatorname{Tr}(\rho I)=1.
$$

The individual bounds make each Born-rule value lie in $[0,1]$; completeness makes the collection a probability distribution. A collection of effects satisfying completeness is called a positive operator-valued measure, or POVM. In this notation, $A$ names the whole measurement, while $A&#95;i$ is the effect associated with outcome $i$.

For example, the standard computational-basis measurement of a qubit has two effects:

$$
A_0=|0\rangle\langle0|,
\qquad
A_1=|1\rangle\langle1|.
$$

If the qubit is in the pure state $\lvert\psi\rangle=a\lvert0\rangle+b\lvert1\rangle$, the two outcome probabilities are $\lvert a\rvert^2$ and $\lvert b\rvert^2$.

## Binary measurements and the difference operator

A binary measurement has only two outcomes. We may call them $+$ and $-$, or “yes” and “no”:

$$
A=(A_+,A_-)=(A_+,I-A_+).
$$

The effect $A&#95;+$ corresponds to the $+$ outcome and $A&#95;-$ to the $-$ outcome. Because their sum must be $I$, choosing $A&#95;+$ fixes $A&#95;-=I-A&#95;+$. This is why only one of the two effects is independent.

It is often useful to replace the pair by one **difference operator**:

$$
D_A=A_+-A_-=2A_+-I.
$$

This amounts to assigning the numerical value $+1$ to one outcome and $-1$ to the other. The operator $D&#95;A$ is Hermitian and satisfies $-I\preceq D&#95;A\preceq I$. Conversely,

$$
A_\pm=\frac{I\pm D_A}{2}.
$$

If the measurement is sharp, meaning that its effects are projections, then $D&#95;A^2=I$ and its eigenvalues are exactly $\pm1$.

## Compatibility is an operator-valued coupling

Let $A=(A&#95;i)&#95;{i=1}^k$ and $B=(B&#95;j)&#95;{j=1}^{\ell}$. They are compatible if positive operators $C&#95;{ij}$ exist such that

$$
\sum_j C_{ij}=A_i,
\qquad
\sum_i C_{ij}=B_j.
$$

Think of $C=(C&#95;{ij})$ as an operator-valued contingency table. Its row totals reproduce $A$ and its column totals reproduce $B$. For every state $\rho$,

$$
p_\rho(i,j)=\operatorname{Tr}(\rho C_{ij})
$$

is an ordinary joint distribution with the correct marginals.

The pair $(i,j)$ now labels a joint event: measurement $A$ reports $i$ and measurement $B$ reports $j$. The operator $C&#95;{ij}$ is the effect assigned to that joint event.

The words **for every state** carry the quantum content. Two classical distributions can always be coupled. Quantum compatibility asks for one positive operator table that produces the right distributions simultaneously for every input state.

This is why Sudoku is only a loose analogy. Sudoku has discrete symbols and fixed clues. Here every cell is an unknown positive matrix constrained by operator-valued row and column totals. “Positive coupling problem” is closer to the mathematics.

## Commutation gives a joint measurement

Suppose every $A&#95;i$ commutes with every $B&#95;j$. Set

$$
C_{ij}=A_iB_j.
$$

The marginal equations follow immediately. Positivity is the only subtle point: products of positive matrices are not generally positive, or even Hermitian. Under commutation,

$$
A_iB_j=B_j^{1/2}A_iB_j^{1/2}\succeq0.
$$

This embeds the familiar statement about commuting sharp observables inside the more general POVM framework.

## The simplest obstruction: two Pauli measurements

Consider the qubit measurements

$$
A=(|0\rangle\langle0|,|1\rangle\langle1|),
\qquad
B=(|+\rangle\langle+|,|-\rangle\langle-|).
$$

Here

$$
|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},
\qquad
|-\rangle=\frac{|0\rangle-|1\rangle}{\sqrt2}.
$$

Their difference operators are the Pauli matrices

$$
D_A=\sigma_z=
\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\qquad
D_B=\sigma_x=
\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$

The subscript in $\sigma&#95;x$ is a name for this particular Pauli matrix. It is not the generic binary operator from the previous section.

If a joint table existed, the cell associated with outcomes $0$ and $+$ would satisfy

$$
0\preceq C_{0,+}\preceq|0\rangle\langle0|,
\qquad
0\preceq C_{0,+}\preceq|+\rangle\langle+|.
$$

A positive operator dominated by a rank-one projection must be supported on that projection’s range. Thus $C&#95;{0,+}$ would have to live in both $\operatorname{span}\{\lvert0\rangle\}$ and $\operatorname{span}\{\lvert+\rangle\}$. These one-dimensional subspaces intersect only at zero, so $C&#95;{0,+}=0$. Repeating the argument for the other entries makes every cell zero, contradicting $\sum&#95;{a,b}C&#95;{ab}=I$.

Geometrically, every joint cell must live inside both its row subspace and its column subspace. For the sharp $\sigma&#95;x$ and $\sigma&#95;z$ measurements, there is nowhere nonzero for it to live.

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

For $g$ arbitrary POVMs, the same time-sharing protocol makes the noisy family compatible at $t=1/g$. Thus every such family satisfies $\tau\geq1/g$.

Binary measurements admit a stronger universal guarantee. For every $g$-tuple of binary POVMs, the noisy family is compatible at visibility $t=1/\sqrt g$, so its compatibility degree satisfies $\tau\geq1/\sqrt g$. Pairwise anticommuting Clifford observables attain equality when the Hilbert-space dimension is large enough. If

$$
\Gamma_x\Gamma_y+\Gamma_y\Gamma_x=0\quad(x\neq y),
$$

then

$$
\left(\sum_x s_x\Gamma_x\right)^2
=\left(\sum_xs_x^2\right)I.
$$

They behave like exactly perpendicular directions in operator space.

## Random measurement models

“Random POVM” does not specify a probability distribution. The ensemble determines the number of outcomes and whether the effects are sharp.

### Binary projective measurements

Choose a Haar-random subspace $E\subset\mathbb C^d$ of prescribed dimension and measure $(P&#95;E,I-P&#95;E)$. This gives a sharp yes/no test.

### Basis measurements

Draw a Haar-random unitary $U$ and measure the rank-one projections onto its columns. The result is a complete $d$-outcome basis readout.

### Induced POVMs

Draw a Haar-random isometry $V:\mathbb C^d\to\mathbb C^k\otimes\mathbb C^n$ and set

$$
M_i=V^*(|i\rangle\langle i|\otimes I_n)V.
$$

These effects are generally unsharp and describe a system coupled to an environment. All of the constructions use Haar invariance. Their outcome structures differ, so they should not be treated as interchangeable models of random measurements.

## A phase diagram for two random projections

Let $E,F\subset\mathbb C^d$ be independent uniformly random subspaces with

$$
\dim E=\lfloor\alpha d\rfloor,
\qquad
\dim F=\lfloor\beta d\rfloor,
$$

and let $\mathsf P&#95;E=(P&#95;E,I-P&#95;E)$ and $\mathsf P&#95;F=(P&#95;F,I-P&#95;F)$. If

$$
\left(\alpha-\frac12\right)^2+
\left(\beta-\frac12\right)^2\leq\frac14,
$$

then, in probability as $d\to\infty$,

$$
\tau(\mathsf P_E,\mathsf P_F)\longrightarrow\frac1{\sqrt2}.
$$

Because $1/\sqrt2$ is the universal minimum for a binary pair, these random measurements are asymptotically maximally incompatible throughout the disk. The result is not restricted to the balanced point $(1/2,1/2)$.

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

The principal-angle decomposition organizes the nontrivial parts of $P&#95;E$ and $P&#95;F$ into two-dimensional blocks. Inside the disk, one can choose a sequence of blocks whose squared principal-angle cosine tends to $1/2$. After choosing a basis in each block, the compression of $2P&#95;E-I$ equals $\sigma&#95;z$, while the compression of $2P&#95;F-I$ tends to $\sigma&#95;x$.

This limiting Pauli pair gives the upper bound $1/\sqrt2$. If the original measurements had a parent POVM, compressing it to the same block would give a parent POVM there as well. The general theorem for binary measurements supplies the reverse inequality, so the two bounds meet.

This is not the Clifford mechanism. The random projections do not anticommute on the full space. What survives is a two-dimensional subspace where they look like $\sigma&#95;x$ and $\sigma&#95;z$.

The disk concerns tolerance to white noise. It does not separate compatible PVMs from incompatible ones. Apart from the trivial ranks, two independent random projections fail to commute with probability one, so their PVMs are incompatible throughout the square. Outside the disk, that incompatibility is easier to erase with noise. The exterior limit is known along $\alpha=\beta$; for general $\alpha\neq\beta$, it remains open.

## Many random binary measurements

Take $g$ independent random projections of rank $d/2$ and let $d$ tend to infinity. Write $A&#95;x=2P&#95;x-I$. Free probability gives

$$
\limsup_{d\to\infty}\tau(\mathsf P_1,\ldots,\mathsf P_g)
\leq\frac{2\sqrt{g-1}}{g}
\sim\frac2{\sqrt g}
$$

almost surely.

Half the eigenvalues of $A&#95;x$ are $+1$ and half are $-1$. Its spectral law is therefore

$$
b=\frac12(\delta_{-1}+\delta_1).
$$

As $d$ grows, independent Haar conjugates become asymptotically free. For any fixed signs $\varepsilon&#95;x$, the sum $\sum&#95;x\varepsilon&#95;xA&#95;x$ converges in distribution to $b^{\boxplus g}$. This is the Kesten–McKay law, and the right endpoint of its support is $2\sqrt{g-1}$.

The endpoint tells us how far the incompatibility witness can be scaled. Set $s=1/(2\sqrt{g-1})$. On the measurements with visibility $t$, the witness has value $stg$. It detects incompatibility as soon as $stg>1$, which gives the bound above.

For large $g$, this is a factor two above the universal lower bound $1/\sqrt g$. The order in $g$ is right, but the constant may not be. The conjecture is

$$
\tau(\mathsf P_1,\ldots,\mathsf P_g)\longrightarrow\frac1{\sqrt g}
$$

for every fixed $g$. When $g=2$, the free-probability estimate gives only the trivial upper bound $1$. The principal-angle argument is what recovers $1/\sqrt2$.

## Operational meaning

A compatible family can be implemented by performing one parent measurement and then relabelling its outcome with classical randomness. In a suitable state-discrimination game, an incompatible family can achieve a higher guessing probability than any compatible family. For the generalized measure, the value is exactly the best possible multiplicative advantage.

The uniform-noise degree asks a narrower question: what fraction of the original measurements can survive depolarization before a joint simulation becomes possible? Another noise model may rank the same measurements differently. The choice of measure therefore matters.

## What remains unresolved

Open questions:

- Is the polar-plus-equatorial configuration optimal for four binary qubit measurements?
- Do balanced random binary PVMs converge to $1/\sqrt g$ for every fixed $g$?
- What is $\tau(\alpha,\beta)$ outside the disk when $\alpha\neq\beta$?
- How quickly does the two-projection result appear at finite dimension, particularly on the boundary?
- Where is the exact threshold for induced random POVMs?
- Which operational tasks are governed by uniform white noise rather than the generalized measure?

Random measurements can reproduce the same qubit obstruction as an engineered pair, and larger families recover the $1/\sqrt g$ scale. Whether the constant is exactly right is still open.

## References

- Andreas Bluhm and Ion Nechita, [*Joint measurability of quantum effects and the matrix diamond*](https://arxiv.org/abs/1807.01508), 2018.
- Andreas Bluhm, Cécilia Lancien, and Ion Nechita, [*Random measurements are almost maximally incompatible*](https://arxiv.org/abs/2507.20600), 2025.
- Jessica Bavaresco et al., [study of maximally incompatible measurements in steering tests](https://arxiv.org/abs/1704.02994), 2017.
- Paul Skrzypczyk, Ivan Šupić, and Daniel Cavalcanti, [*All sets of incompatible measurements give an advantage in quantum state discrimination*](https://arxiv.org/abs/1901.00816), 2019.
