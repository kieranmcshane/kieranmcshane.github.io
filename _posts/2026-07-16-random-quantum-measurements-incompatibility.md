---
layout: post
title: "Random Binary Projective Measurements and Incompatibility"
subtitle: "From joint measurability to a principal-angle phase diagram"
date: 2026-07-16 09:00:00 +0200
categories: [quantum-information]
tags: [POVMs, incompatibility, random-matrices, free-probability]
excerpt: "A guided introduction to joint measurability and the asymptotic incompatibility of random binary projections."
---

Two quantum measurements are compatible when both can be recovered from a single measurement. If the joint measurement reports a pair of outcomes $(i,j)$, ignoring $j$ should reproduce the statistics of the first measurement, while ignoring $i$ should reproduce those of the second. This must hold for every input state.

Compatibility therefore concerns outcome probabilities. We represent a measurement by a POVM, a collection of positive operators associated with its possible outcomes. A POVM does not specify the state left behind after an outcome; that additional information belongs to a quantum instrument and is not needed for joint measurability.

The article first develops effects, POVMs, compatibility and uniform noise. It then turns to the main subject: random binary projective measurements, their principal-angle geometry and the resulting phase diagram.

## Reading guide

- [The primer](#from-outcomes-to-effects) introduces the notation and the marginal problem.
- [The two-projection argument](#a-phase-diagram-for-two-random-projections) contains the main geometric result and the full off-diagonal limit.
- [The many-measurement section](#many-random-binary-measurements) uses incompatibility witnesses and free probability; the final section explains the operational meaning.

## From outcomes to effects

Imagine that a device has $k$ possible outcomes. We label them

$$
i=1,\ldots,k.
$$

Using the device once returns one label $i$. It names the event “outcome $i$ occurred,” just as “heads” names a coin-toss outcome. Quantum theory associates this outcome with an operator $A&#95;i$, called an **effect**. It satisfies

$$
0\preceq A_i\preceq I.
$$

The first inequality says that $A&#95;i$ is positive. The second says that $I-A&#95;i$ is positive. Equivalently, the eigenvalues of $A&#95;i$ lie between zero and one. If the system is prepared in state $\rho$, the **Born rule** assigns the probability of outcome $i$:

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

so $\operatorname{Tr}(\rho A&#95;i)\leq1$. The assigned probability therefore lies between zero and one for every state. This establishes the allowed range for one outcome. It does not yet show that the probabilities of all outcomes sum to one.

An effect tells us the probability of one outcome. It does not, by itself, tell us the state after that outcome occurs. A quantum instrument supplies this extra information. It is a family of completely positive maps $\mathcal I&#95;i$ whose sum preserves trace. The outcome probability and the conditional state are

$$
\Pr(i\mid\rho)=\operatorname{Tr}\!\bigl(\mathcal I_i(\rho)\bigr),
\qquad
\rho_i=
\frac{\mathcal I_i(\rho)}
{\operatorname{Tr}(\mathcal I_i(\rho))}
$$

whenever the denominator is nonzero. In a Kraus representation,

$$
\mathcal I_i(\rho)=\sum_m K_{i,m}\rho K_{i,m}^{\dagger},
\qquad
A_i=\sum_m K_{i,m}^{\dagger}K_{i,m}.
$$

Different instruments can produce the same effect $A&#95;i$. They agree on the probability of the outcome but can disturb the state differently.

An effect is a projection precisely when

$$
A_i^2=A_i
\quad\Longleftrightarrow\quad
\operatorname{spec}(A_i)\subseteq\{0,1\}.
$$

It then represents a sharp outcome. A measurement made entirely of projections is called projective or sharp. General effects may have eigenvalues strictly between zero and one, but they are not merely defective projections. For example, perform a projective measurement $(P&#95;j)$ and report $i$ with classical probability $p(i\mid j)$. The effective outcome is

$$
A_i=\sum_j p(i\mid j)P_j,
$$

which is generally not a projection. Merely merging mutually orthogonal projective outcomes is different: their sum remains a projection. More generally, a POVM can arise by coupling the system to an ancilla and performing a projective measurement on the larger system.

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

If the measurement is sharp, meaning that its effects are projections, then $D&#95;A^2=I$ and its spectrum is contained in $\{-1,+1\}$. Both values occur when both effects have nonzero range; a trivial sharp measurement may have $D&#95;A=I$ or $D&#95;A=-I$.

## Compatibility is an operator-valued coupling

Let $A=(A&#95;i)&#95;{i=1}^k$ and $B=(B&#95;j)&#95;{j=1}^{\ell}$. They are compatible if positive operators $C&#95;{ij}$ exist such that

$$
\sum_j C_{ij}=A_i,
\qquad
\sum_i C_{ij}=B_j.
$$

Think of $C=(C&#95;{ij})$ as an operator-valued contingency table. Its row totals reproduce $A$ and its column totals reproduce $B$:

$$
\begin{array}{c|ccc|c}
 & B_1 & \cdots & B_\ell & \text{row sum}\\
\hline
A_1 & C_{11} & \cdots & C_{1\ell} & A_1\\
\vdots & \vdots & \ddots & \vdots & \vdots\\
A_k & C_{k1} & \cdots & C_{k\ell} & A_k\\
\hline
\text{column sum} & B_1 & \cdots & B_\ell & I
\end{array}
$$

Each cell contains a positive operator. The labels at the right and bottom are the prescribed operator-valued marginals. Their common grand total is $I$, because both POVMs are complete. For every state $\rho$,

$$
p_\rho(i,j)=\operatorname{Tr}(\rho C_{ij})
$$

is an ordinary joint distribution with the correct marginals.

The pair $(i,j)$ now labels a joint event: measurement $A$ reports $i$ and measurement $B$ reports $j$. The operator $C&#95;{ij}$ is the effect assigned to that joint event.

The words **for every state** carry the quantum content. Two classical distributions can always be coupled. Quantum compatibility asks for one positive operator table that produces the right distributions simultaneously for every input state.

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

Commutation is sufficient here, but it is not necessary for general POVMs. For projective measurements, compatibility and commutation are equivalent. For example, the noisy Pauli effects $(I\pm t\sigma&#95;z)/2$ and $(I\pm t\sigma&#95;x)/2$ do not commute when $t>0$, yet they are compatible when $t\leq1/\sqrt2$.

This is the precise setting behind the familiar slogan that “[noncommuting observables cannot be measured simultaneously](https://ar5iv.labs.arxiv.org/html/2510.13980v2#S1.SS1.SSS1.p2).” For sharp observables, the slogan refers to the failure of simultaneous diagonalization and joint measurability. It should not be extended unchanged to noisy POVMs or to other experimental meanings of simultaneity, such as [continuous weak measurement](https://arxiv.org/abs/2306.06167).

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

Throughout this article, **maximally incompatible** means attaining the smallest possible value of this balanced uniform-white-noise degree within the stated class of measurements. It is not a claim that is independent of the noise model or incompatibility measure.

For a family $A^{(1)},\ldots,A^{(g)}$, a parent POVM is indexed by an outcome string $\mathbf i=(i&#95;1,\ldots,i&#95;g)$. Its $x$-th marginal must satisfy

$$
\sum_{\mathbf i:\,i_x=a}G_{\mathbf i}=A^{(x)}_a.
$$

The compatibility degree of the family is defined by adding the same visibility $t$ to every member and maximizing the values of $t$ for which such a parent exists.

Every pair satisfies $\tau(A,B)\geq1/2$. Indeed,

$$
C_{ij}=\frac{A_i}{2\ell}+\frac{B_j}{2k}
$$

is a parent POVM for the half-noisy measurements. Operationally, flip a fair coin. If it chooses $A$, genuinely measure $A$ and invent a uniform $B$ outcome; if it chooses $B$, do the reverse. Noise gives the apparatus permission to perform one measurement and fabricate the missing answer.

For $g$ arbitrary POVMs, the same time-sharing protocol makes the noisy family compatible at $t=1/g$. Thus every such family satisfies $\tau\geq1/g$.

Binary measurements admit a stronger universal guarantee. For every $g$-tuple of binary POVMs, the noisy family is compatible at visibility $t=1/\sqrt g$, so its compatibility degree satisfies $\tau\geq1/\sqrt g$. Pairwise anticommuting Clifford observables attain equality when the Hilbert-space dimension is large enough ([Bluhm and Nechita, 2018](https://arxiv.org/abs/1807.01508)). Let $\Gamma&#95;x$ be Hermitian unitaries satisfying

$$
\Gamma_x^2=I,
\qquad
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

Assume $d\leq kn$. Draw a Haar-random isometry $V:\mathbb C^d\to\mathbb C^k\otimes\mathbb C^n$ and set

$$
M_i=V^*(|i\rangle\langle i|\otimes I_n)V.
$$

These effects are generally unsharp and describe a system coupled to an environment. All of the constructions use Haar invariance. Their effect spectra and rank profiles differ, and the induced model also depends on the ancillary dimension $n$. They should not be treated as interchangeable models of random measurements.

The rest of this article develops the binary-projective model. The basis and induced models are included here only to make clear that the phrase “random POVM” does not identify a unique ensemble.

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

This is [Corollary 3.6 of Bluhm, Lancien, and Nechita](https://ar5iv.labs.arxiv.org/html/2507.20600#S3.Thmtheorem6).

### Why a circle appears

The squared cosines of the nontrivial principal angles between $E$ and $F$ asymptotically fill an interval with endpoints ([Aubrun, 2021](https://arxiv.org/abs/2109.06535))

$$
\lambda_{\alpha,\beta}^{\pm}
=\alpha+\beta-2\alpha\beta
\pm2\sqrt{\alpha(1-\alpha)\beta(1-\beta)}.
$$

The disk condition is equivalent to

$$
\lambda^-_{\alpha,\beta}\leq\frac12\leq\lambda^+_{\alpha,\beta}.
$$

The principal-angle decomposition organizes the nontrivial parts of $P&#95;E$ and $P&#95;F$ into two-dimensional reducing blocks. On a block with principal angle $\theta$, one may choose a basis in which

$$
P_E=
\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
P_F=
\begin{pmatrix}
\cos^2\theta&\cos\theta\sin\theta\\
\cos\theta\sin\theta&\sin^2\theta
\end{pmatrix}.
$$

The corresponding difference operators are

$$
D_E=\sigma_z,
\qquad
D_F=\cos(2\theta)\sigma_z+\sin(2\theta)\sigma_x.
$$

For two unbiased qubit observables with unit Bloch vectors $m$ and $n$, [Lemma 3.4 of Bluhm, Lancien, and Nechita](https://ar5iv.labs.arxiv.org/html/2507.20600#S3.Thmtheorem4) gives the white-noise threshold

$$
\tau=\frac{2}{\|m+n\|+\|m-n\|}.
$$

On the principal-angle block this becomes

$$
\tau_\theta=\frac{1}{\cos\theta+\sin\theta}.
$$

The function is smallest at $\theta=\pi/4$. Inside the disk, there are blocks whose squared principal-angle cosine tends to $1/2$, so their thresholds tend to $1/\sqrt2$. A parent for the full measurements would restrict to a parent on every reducing block, which gives the asymptotic upper bound. The universal binary theorem supplies the matching lower bound.

Conversely, parents on all reducing blocks can be combined by direct sum. Thus, for a fixed finite pair of projections with nontrivial principal angles $\theta&#95;r$,

$$
\tau(\mathsf P_E,\mathsf P_F)
=\min\left(\{1\}\cup
\left\{\frac{1}{\cos\theta_r+\sin\theta_r}:r\right\}\right).
$$

The value $1$ accounts for the commuting one-dimensional blocks.

There is an equivalent formula that avoids listing the angles. On a nontrivial block, writing $c=\cos\theta$ and $s=\sin\theta$,

$$
[P_E,P_F]
=cs\begin{pmatrix}0&1\\-1&0\end{pmatrix},
\qquad
\|[P_E,P_F]\|_\infty=cs.
$$

Since $(c+s)^2=1+2cs$, taking the worst block gives the exact identity

$$
\boxed{
\tau(\mathsf P_E,\mathsf P_F)
=\frac1{\sqrt{1+2\|[P_E,P_F]\|_\infty}}
}.
$$

This is the visibility form of [Eq. (11) in Heinosaari, Kiukas, and Reitzner](https://ar5iv.labs.arxiv.org/html/1501.04554#S5.E11). The identity is special to two sharp binary measurements under the uniform-noise model. It should not be read as a general commutator formula for arbitrary POVMs.

### The full off-diagonal limit

Set

$$
h(\lambda)=\frac1{\sqrt\lambda+\sqrt{1-\lambda}}
$$

and let $\lambda&#95;{\star}=\lambda&#95;{\star}(\alpha,\beta)$ be the point of $[\lambda^-&#95;{\alpha,\beta},\lambda^+&#95;{\alpha,\beta}]$ closest to $1/2$:

$$
\lambda_{\star}=
\begin{cases}
\lambda^+_{\alpha,\beta},&\lambda^+_{\alpha,\beta}<1/2,\\[2mm]
1/2,&\lambda^-_{\alpha,\beta}\leq1/2\leq\lambda^+_{\alpha,\beta},\\[2mm]
\lambda^-_{\alpha,\beta},&\lambda^-_{\alpha,\beta}>1/2.
\end{cases}
$$

<div class="theorem" markdown="1">

**Proposition.** Let $0<\alpha,\beta<1$, and for each $d$ let $E&#95;d,F&#95;d\subset\mathbb C^d$ be independent Haar-random subspaces of dimensions $\lfloor\alpha d\rfloor$ and $\lfloor\beta d\rfloor$. Then

$$
\tau(\mathsf P_{E_d},\mathsf P_{F_d})
\xrightarrow{\mathbb P}
h(\lambda_{\star}(\alpha,\beta)).
$$

If the pairs are constructed together on the product probability space, using independent Haar draws for every $d$, the convergence holds almost surely.

</div>

**Proof.** Unitary invariance lets us fix $E&#95;d$ as the coordinate subspace of dimension $\lfloor\alpha d\rfloor$. Write

$$
P_{E_d}=P_d,
\qquad
P_{F_d}=U_dQ_dU_d^*,
$$

where $P&#95;d$ and $Q&#95;d$ are deterministic coordinate projections with normalized traces tending to $\alpha$ and $\beta$, and $U&#95;d$ is Haar distributed. These deterministic projection sequences have a strong limit. The strong asymptotic-freeness theorem of [Collins and Male](https://ar5iv.labs.arxiv.org/html/1105.4345#S1.Thmtheorem4) therefore gives, almost surely under the product coupling,

$$
\bigl\|[P_d,U_dQ_dU_d^*]\bigr\|_\infty
\longrightarrow
\|[p,q]\|,
$$

where $p$ and $q$ are free projections of traces $\alpha$ and $\beta$.

[Aubrun’s support computation](https://arxiv.org/abs/2109.06535), combined with the principal-angle block form, shows that the nonzero singular values of $[p,q]$ are obtained by applying

$$
\lambda\longmapsto\sqrt{\lambda(1-\lambda)}
$$

to the interval $[\lambda^-&#95;{\alpha,\beta},\lambda^+&#95;{\alpha,\beta}]$. Equivalently, the nonzero spectrum of the self-adjoint operator $i[p,q]$ is obtained by applying

$$
\lambda\longmapsto\pm\sqrt{\lambda(1-\lambda)}.
$$

Any atoms at $0$ or $1$ come from commuting intersection or kernel blocks; the map sends both to zero. Hence

$$
\|[p,q]\|
=\max_{\lambda\in[\lambda^-_{\alpha,\beta},\lambda^+_{\alpha,\beta}]}
\sqrt{\lambda(1-\lambda)}
=\sqrt{\lambda_{\star}(1-\lambda_{\star})}.
$$

Substituting this norm limit into the exact finite-dimensional identity gives

$$
\tau(\mathsf P_{E_d},\mathsf P_{F_d})
\longrightarrow
\frac1{\sqrt{1+2\sqrt{\lambda_{\star}(1-\lambda_{\star})}}}
=h(\lambda_{\star}).
$$

This is almost-sure convergence under the stated coupling, and therefore convergence in probability for the original sequence of random pairs. $\square$

Inside the disk, $\lambda&#95;{\star}=1/2$ and the proposition gives $1/\sqrt2$. Outside it, $\lambda&#95;{\star}$ is the nearer endpoint. On the diagonal exterior it reduces to the formula stated in the random-measurement paper, with $\lambda&#95;\alpha=4\alpha(1-\alpha)$. That paper does not separately state the full off-diagonal surface; the proposition above is derived from its setup, the exact finite-dimensional identity and the cited strong spectral input.

<figure class="post-figure">
  <img src="/assets/images/off-diagonal-phase.svg" alt="A heat map of the limiting compatibility threshold over the full alpha-beta square. The central disk has value one over square root of two, and the threshold rises toward one in the four exterior corners.">
  <figcaption><strong>Figure 1.</strong> The limiting surface obtained from the principal-angle blocks for interior rank fractions $0<\alpha,\beta<1$. The central disk is flat at the universal binary minimum. A power-stretched colour scale ($\gamma=0.35$) makes the small exterior increases visible, while the ticks retain the true values of $\tau_\infty$. On an exact edge of the square, a rank fraction $0$ or $1$ makes one PVM trivial and gives $\tau=1$; that degenerate boundary value is not the interior limit shown by the colours.</figcaption>
</figure>

<figure class="post-figure">
  <img src="/assets/images/principal-angle-mechanism.svg" alt="The limiting principal-angle interval contains one half, forcing finite-dimensional blocks arbitrarily close to angle pi over four and hence to the Pauli sigma-z and sigma-x obstruction.">
  <figcaption><strong>Figure 2.</strong> Why the disk gives maximal incompatibility. If the limiting spectrum of squared principal-angle cosines contains $1/2$, finite-dimensional blocks occur arbitrarily close to $\theta=\pi/4$ with high probability. Their centered measurements approach the $\sigma_z$ and $\sigma_x$ pair, forcing $\tau$ toward $1/\sqrt2$.</figcaption>
</figure>

<figure class="post-figure">
  <img src="/assets/images/finite-dimension-check.svg" alt="Seeded Monte Carlo medians and ten-to-ninety percent intervals for finite random projection pairs at an interior point, an off-diagonal boundary point, and an exterior point.">
  <figcaption><strong>Figure 3.</strong> A finite-dimensional check at three parameter choices. Dots are Monte Carlo medians and whiskers show the 10th–90th percentiles. The boundary data are consistent with slower, edge-controlled convergence because $1/2$ lies at the endpoint of the limiting spectral interval. This experiment illustrates finite-size behavior; it is not a proof of a convergence rate.</figcaption>
</figure>

**Reproduce Figure 3.** The [Python source](https://github.com/kieranmcshane/kieranmcshane.github.io/blob/main/assets/code/random_projection_compatibility.py) contains the exact finite-dimensional formula, the Haar-subspace sampler, and the seeded Monte Carlo experiment. Its [generated CSV file](/assets/data/finite-dimension-check.csv) records every plotted median and 10th–90th percentile. From the repository root, run:

    python3 -m pip install -r assets/code/requirements.txt
    python3 assets/code/random_projection_compatibility.py

### An independent SDP audit

Figure 3 uses the exact commutator formula, so it tests the random spectral behavior but does not independently validate that formula. A separate [CVXPY audit](https://github.com/kieranmcshane/kieranmcshane.github.io/blob/main/assets/code/validate_projection_compatibility_sdp.py) instead solves the original joint-measurability problem.

For the noisy effects

$$
A_t=tP+(1-t)\frac I2,
\qquad
B_t=tQ+(1-t)\frac I2,
$$

binary compatibility is equivalent to the existence of one Hermitian operator $G$ satisfying

$$
G\succeq0,
\qquad A_t-G\succeq0,
\qquad B_t-G\succeq0,
\qquad I-A_t-B_t+G\succeq0.
$$

The audit maximizes $t$ subject to these constraints and only afterward compares the optimum with $1/\sqrt{1+2\lVert[P,Q]\rVert_\infty}$. Across eight seeded projection pairs in dimensions $2,3,4$ and $6$, the largest absolute discrepancy was $1.035\times10^{-8}$. The [CSV output](/assets/data/sdp-validation.csv) records every comparison. This is a numerical check, not part of the proof above.

To reproduce it:

    python3 -m pip install -r assets/code/sdp-requirements.txt
    python3 assets/code/validate_projection_compatibility_sdp.py

This is not the Clifford mechanism. The random projections do not anticommute on the full space. What survives is a two-dimensional block where they approach the $\sigma&#95;x$ and $\sigma&#95;z$ pair.

The disk concerns tolerance to white noise. It does not separate compatible PVMs from incompatible ones. Apart from trivial ranks, two independent random projections fail to commute with probability one, so their PVMs are incompatible throughout the square. What changes across the circle is the amount of uniform noise needed to erase that incompatibility.

## Many random binary measurements

Fix $g$, take even $d$, and choose $g$ independent random projections of rank $d/2$. Write $D&#95;x=2P&#95;x-I$ for their difference operators. The random-measurement theorem gives, almost surely,

$$
\limsup_{d\to\infty}\tau(\mathsf P_1,\ldots,\mathsf P_g)
\leq\frac{2\sqrt{g-1}}{g}
$$

([Bluhm, Lancien, and Nechita, 2025](https://arxiv.org/abs/2507.20600)).

Half the eigenvalues of $D&#95;x$ are $+1$ and half are $-1$. Its spectral law is therefore

$$
b=\frac12(\delta_{-1}+\delta_1).
$$

As $d$ grows, independent Haar conjugates become asymptotically free. More is needed here than convergence of empirical eigenvalue distributions. For every fixed sign vector $\varepsilon$, strong asymptotic freeness ([Collins and Male, 2014](https://arxiv.org/abs/1105.4345)) gives

$$
\left\|\sum_{x=1}^g\varepsilon_xD_x\right\|_\infty
\longrightarrow 2\sqrt{g-1}
$$

almost surely. The limiting law is the Kesten–McKay distribution $b^{\boxplus g}$, whose support has endpoints $\pm2\sqrt{g-1}$. Strong convergence rules out spectral outliers, which ordinary convergence in distribution would not do. Since $g$ is fixed, there are only $2^g$ sign vectors, so the norm convergence holds simultaneously for all of them.

> **Free-probability intuition.** Free independence determines the limiting bulk spectrum of a large random-matrix sum. Strong convergence adds the fact needed here: no isolated eigenvalue survives beyond that limiting support. Its edge can therefore control the operator norm used to normalize the witness.

Here is how those signed sums enter the incompatibility test. A tuple of Hermitian operators $W&#95;x$ is normalized as a witness if every compatible tuple of binary difference operators $X&#95;x$ satisfies

$$
\sum_{x=1}^g\operatorname{Tr}(W_xX_x)\leq1.
$$

To see the normalization rather than merely quote it, let a compatible tuple $X&#95;1,\ldots,X&#95;g$ have a parent POVM $(G&#95;\varepsilon)&#95;{\varepsilon\in\lbrace-1,+1\rbrace^g}$. Its marginals give

$$
X_x=\sum_{\varepsilon}\varepsilon_xG_\varepsilon.
$$

For the collinear choice $W&#95;x=sD&#95;x/d$,

$$
\begin{aligned}
\sum_{x=1}^g\operatorname{Tr}(W_xX_x)
&=\frac{s}{d}\sum_\varepsilon
\operatorname{Tr}\!\left[
\left(\sum_{x=1}^g\varepsilon_xD_x\right)G_\varepsilon
\right]\\
&\leq\frac{s}{d}
\max_\varepsilon\left\|\sum_{x=1}^g\varepsilon_xD_x\right\|_\infty
\sum_\varepsilon\operatorname{Tr}(G_\varepsilon)\\
&=s\max_\varepsilon
\left\|\sum_{x=1}^g\varepsilon_xD_x\right\|_\infty,
\end{aligned}
$$

because $\sum&#95;\varepsilon G&#95;\varepsilon=I&#95;d$. A sufficient normalization condition is therefore

$$
s\left\|\sum_{x=1}^g\varepsilon_xD_x\right\|_\infty\leq1
\qquad\text{for every sign vector }\varepsilon.
$$

White noise changes $D&#95;x$ to $tD&#95;x$. Because $D&#95;x^2=I$, the witness value on the noisy family is

$$
\sum_{x=1}^g\operatorname{Tr}\!\left(\frac{sD_x}{d}\,tD_x\right)=stg.
$$

Choose $s$ asymptotically as $1/(2\sqrt{g-1})$. The witness detects incompatibility when $stg>1$, yielding the stated upper bound.

After the $d\to\infty$ limit is taken with $g$ fixed, the upper bound behaves as $2/\sqrt g$ when $g$ grows. This is a factor two above the universal lower bound $1/\sqrt g$. The order in $g$ is right, but the constant may not be. The conjecture is

$$
\tau(\mathsf P_1,\ldots,\mathsf P_g)\longrightarrow\frac1{\sqrt g}
$$

for every fixed $g$. When $g=2$, the free-probability estimate gives only the trivial upper bound $1$. The principal-angle argument is what recovers $1/\sqrt2$.

## Operational meaning

A compatible family can be implemented by performing one parent measurement and then relabelling its outcome with classical randomness. In a suitable state-discrimination game, an incompatible family can achieve a higher guessing probability than any compatible family.

The precise operational equality concerns the **generalized robustness of incompatibility**, not the white-noise degree $\tau$. For a measurement family $M=(M&#95;{a\mid x})$, define

$$
I_R(M)=\min\left\{r\geq0:
\frac{M_{a\mid x}+rN_{a\mid x}}{1+r}
\text{ is compatible for some measurement family }N\right\}.
$$

In the multi-ensemble state-discrimination games with side information studied by Skrzypczyk, Šupić, and Cavalcanti, [their Eq. (5)](https://ar5iv.labs.arxiv.org/html/1901.00816#S2.E5) states that

$$
\max_{\mathcal E}
\frac{P_{\rm guess}(\mathcal E,M)}
{P_{\rm guess}^{\rm compatible}(\mathcal E)}
=1+I_R(M).
$$

Thus $I&#95;R$ is the fractional advantage above the compatible benchmark, while $1+I&#95;R$ is the multiplicative advantage. The equality is for this particular class of discrimination games, not for every discrimination task.

The uniform-noise degree asks a narrower question: what fraction of the original measurements can survive depolarization before a joint simulation becomes possible? Another noise model may rank the same measurements differently. The choice of measure therefore matters.

| Quantity | Noise being allowed | What the number means |
|:--|:--|:--|
| $\tau$ | Uniform POVM noise | Largest surviving visibility before compatibility |
| $R&#95;{\rm white}=\tau^{-1}-1$ | The same uniform noise, written as a mixing ratio | Amount of white noise relative to the original measurement |
| $I&#95;R$ | An arbitrary measurement family | Generalized robustness; $1+I&#95;R$ is the optimal discrimination ratio above |

## What remains unresolved

Open questions:

- Do balanced random binary PVMs converge to $1/\sqrt g$ for every fixed $g$?
- How quickly does the two-projection result appear at finite dimension, particularly on the boundary?
- Where is the exact threshold for induced random POVMs?
- Which operational tasks are governed by uniform white noise rather than the generalized measure?

Random measurements can reproduce the same qubit obstruction as an engineered pair, and larger families recover the $1/\sqrt g$ scale. Whether the constant is exactly right is still open.

## References

- Andreas Bluhm and Ion Nechita, [*Joint measurability of quantum effects and the matrix diamond*](https://arxiv.org/abs/1807.01508), 2018.
- Andreas Bluhm, Cécilia Lancien, and Ion Nechita, [*Random measurements are almost maximally incompatible*](https://arxiv.org/abs/2507.20600), 2025.
- Guillaume Aubrun, [*Principal angles between random subspaces and polynomials in two free projections*](https://arxiv.org/abs/2109.06535), 2021.
- Teiko Heinosaari, Jukka Kiukas, and Daniel Reitzner, [*Noise Robustness of the Incompatibility of Quantum Measurements*](https://arxiv.org/abs/1501.04554), 2015.
- Christopher S. Jackson, [*Sequential Quantum Measurements and the Instrumental Group Algebra*](https://arxiv.org/abs/2510.13980), 2025.
- Christopher S. Jackson and Carlton M. Caves, [*Simultaneous Measurements of Noncommuting Observables: Positive Transformations and Instrumental Lie Groups*](https://arxiv.org/abs/2306.06167), 2023.
- Benoît Collins and Camille Male, [*The strong asymptotic freeness of Haar and deterministic matrices*](https://arxiv.org/abs/1105.4345), 2014.
- Jessica Bavaresco et al., [*Most incompatible measurements for robust steering tests*](https://arxiv.org/abs/1704.02994), 2017.
- Paul Skrzypczyk, Ivan Šupić, and Daniel Cavalcanti, [*All sets of incompatible measurements give an advantage in quantum state discrimination*](https://arxiv.org/abs/1901.00816), 2019.
