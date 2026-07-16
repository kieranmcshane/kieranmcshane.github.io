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

An effect tells us the probability of one outcome. It does not, by itself, tell us the state of the system after that outcome occurs. Describing the state change requires extra information, such as a quantum instrument or Kraus operators.

An effect need not be a projection. If $A&#95;i^2=A&#95;i$, then it is a projection and represents a sharp outcome. A measurement made entirely of projections is called projective or sharp. General effects are not merely defective projections. They also arise naturally after coupling the system to an ancilla or combining several detector outcomes.

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

Commutation is sufficient here, but it is not necessary for general POVMs. For projective measurements, compatibility and commutation are equivalent. For example, the noisy Pauli effects $(I\pm t\sigma&#95;z)/2$ and $(I\pm t\sigma&#95;x)/2$ do not commute when $t>0$, yet they are compatible when $t\leq1/\sqrt2$.

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

This is the two-projection phase-diagram theorem of [Bluhm, Lancien, and Nechita](https://arxiv.org/abs/2507.20600).

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

For two unbiased qubit observables with unit Bloch vectors $m$ and $n$, the qubit compatibility criterion used by [Bluhm, Lancien, and Nechita](https://arxiv.org/abs/2507.20600) gives the white-noise threshold

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

This finite formula also resolves the off-diagonal asymptotic surface. Set

$$
h(\lambda)=\frac1{\sqrt\lambda+\sqrt{1-\lambda}}
$$

and let $\lambda&#95;* = \lambda&#95;*(\alpha,\beta)$ be the point of $[\lambda^-&#95;{\alpha,\beta},\lambda^+&#95;{\alpha,\beta}]$ closest to $1/2$:

$$
\lambda_*=
\begin{cases}
\lambda^+_{\alpha,\beta},&\lambda^+_{\alpha,\beta}<1/2,\\[2mm]
1/2,&\lambda^-_{\alpha,\beta}\leq1/2\leq\lambda^+_{\alpha,\beta},\\[2mm]
\lambda^-_{\alpha,\beta},&\lambda^-_{\alpha,\beta}>1/2.
\end{cases}
$$

Weak convergence supplies principal-angle values throughout the limiting support, while strong convergence rules out spectral outliers. Since $h$ is continuous and has its unique minimum at $1/2$, the exact block formula gives

$$
\tau(\mathsf P_E,\mathsf P_F)
\longrightarrow h(\lambda_*(\alpha,\beta)).
$$

Inside the disk this reduces to $1/\sqrt2$. Outside it selects the nearer spectral endpoint. On the diagonal exterior it reduces to the formula stated in the paper, with $\lambda&#95;\alpha=4\alpha(1-\alpha)$. The paper does not separately state the full off-diagonal formula; the expression above is the direct consequence of its spectral input and the exact reducing-block criterion.

<figure class="post-figure">
  <img src="/assets/images/off-diagonal-phase.svg" alt="A heat map of the limiting compatibility threshold over the full alpha-beta square. The central disk has value one over square root of two, and the threshold rises toward one in the four exterior corners.">
  <figcaption><strong>Figure 1.</strong> The full limiting surface obtained from the principal-angle blocks. The central disk is flat at the universal binary minimum. In each exterior corner, the closest endpoint of $[\lambda^-,\lambda^+]$ determines the threshold.</figcaption>
</figure>

<figure class="post-figure">
  <img src="/assets/images/principal-angle-mechanism.svg" alt="The limiting principal-angle interval contains one half, producing a two-dimensional block at angle pi over four and the Pauli sigma-z and sigma-x witness.">
  <figcaption><strong>Figure 2.</strong> Why the disk gives maximal incompatibility. If the limiting spectrum of squared principal-angle cosines contains $1/2$, a block with $\theta=\pi/4$ appears. On that block, the centered measurements are $\sigma_z$ and $\sigma_x$, forcing $\tau$ down to $1/\sqrt2$.</figcaption>
</figure>

<figure class="post-figure">
  <img src="/assets/images/finite-dimension-check.svg" alt="Seeded Monte Carlo medians and ten-to-ninety percent intervals for finite random projection pairs at an interior point, an off-diagonal boundary point, and an exterior point.">
  <figcaption><strong>Figure 3.</strong> A finite-dimensional check at three parameter choices. Dots are Monte Carlo medians and whiskers show the 10th–90th percentiles. The boundary converges more slowly because $1/2$ sits at a spectral edge. This experiment illustrates finite-size behavior; it is not a proof of a convergence rate.</figcaption>
</figure>

This is not the Clifford mechanism. The random projections do not anticommute on the full space. What survives is a two-dimensional block where they approach the $\sigma&#95;x$ and $\sigma&#95;z$ pair.

The disk concerns tolerance to white noise. It does not separate compatible PVMs from incompatible ones. Apart from trivial ranks, two independent random projections fail to commute with probability one, so their PVMs are incompatible throughout the square. What changes across the circle is the amount of uniform noise needed to erase that incompatibility.

## Many random binary measurements

Fix $g$, take even $d$, and choose $g$ independent random projections of rank $d/2$. Write $A&#95;x=2P&#95;x-I$. The random-measurement theorem gives, almost surely,

$$
\limsup_{d\to\infty}\tau(\mathsf P_1,\ldots,\mathsf P_g)
\leq\frac{2\sqrt{g-1}}{g}
$$

([Bluhm, Lancien, and Nechita, 2025](https://arxiv.org/abs/2507.20600)).

Half the eigenvalues of $A&#95;x$ are $+1$ and half are $-1$. Its spectral law is therefore

$$
b=\frac12(\delta_{-1}+\delta_1).
$$

As $d$ grows, independent Haar conjugates become asymptotically free. More is needed here than convergence of empirical eigenvalue distributions. For every fixed sign vector $\varepsilon$, strong asymptotic freeness ([Collins and Male, 2014](https://arxiv.org/abs/1105.4345)) gives

$$
\left\|\sum_{x=1}^g\varepsilon_xA_x\right\|_\infty
\longrightarrow 2\sqrt{g-1}
$$

almost surely. The limiting law is the Kesten–McKay distribution $b^{\boxplus g}$, whose support has endpoints $\pm2\sqrt{g-1}$. Strong convergence rules out spectral outliers, which ordinary convergence in distribution would not do. Since $g$ is fixed, there are only $2^g$ sign vectors, so the norm convergence holds simultaneously for all of them.

Here is how those signed sums enter the incompatibility test. A tuple of Hermitian operators $W&#95;x$ is normalized as a witness if every compatible tuple of binary difference operators $X&#95;x$ satisfies

$$
\sum_{x=1}^g\operatorname{Tr}(W_xX_x)\leq1.
$$

For the collinear choice $W&#95;x=sA&#95;x/d$, a sufficient normalization condition is

$$
s\left\|\sum_{x=1}^g\varepsilon_xA_x\right\|_\infty\leq1
\qquad\text{for every sign vector }\varepsilon.
$$

This condition bounds every deterministic choice of one sign per measurement, which is exactly what appears when a parent POVM is marginalized.

White noise changes the difference operator $A&#95;x$ to $tA&#95;x$. Because $A&#95;x^2=I$, the witness value on the noisy family is

$$
\sum_{x=1}^g\operatorname{Tr}\!\left(\frac{sA_x}{d}\,tA_x\right)=stg.
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

In the multi-ensemble state-discrimination games with side information studied by [Skrzypczyk, Šupić, and Cavalcanti](https://arxiv.org/abs/1901.00816),

$$
\max_{\mathcal E}
\frac{P_{\rm guess}(\mathcal E,M)}
{P_{\rm guess}^{\rm compatible}(\mathcal E)}
=1+I_R(M).
$$

Thus $I&#95;R$ is the fractional advantage above the compatible benchmark, while $1+I&#95;R$ is the multiplicative advantage. The equality is for this particular class of discrimination games, not for every discrimination task.

The uniform-noise degree asks a narrower question: what fraction of the original measurements can survive depolarization before a joint simulation becomes possible? Another noise model may rank the same measurements differently. The choice of measure therefore matters.

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
- Benoît Collins and Camille Male, [*The strong asymptotic freeness of Haar and deterministic matrices*](https://arxiv.org/abs/1105.4345), 2014.
- Jessica Bavaresco et al., [*Most incompatible measurements for robust steering tests*](https://arxiv.org/abs/1704.02994), 2017.
- Paul Skrzypczyk, Ivan Šupić, and Daniel Cavalcanti, [*All sets of incompatible measurements give an advantage in quantum state discrimination*](https://arxiv.org/abs/1901.00816), 2019.
