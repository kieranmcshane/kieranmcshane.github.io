---
layout: post
title: "Centered Correlation Tensors and Quantum Separability"
subtitle: "The enhanced realignment criterion in Bloch coordinates"
date: 2026-07-17 08:00:00 +0200
categories: [quantum-information]
tags: [entanglement, separability, tensor-norms, Bloch-representation]
excerpt: "How the usual correlation-tensor separability test becomes a marginal-dependent covariance bound after centering."
---

Deciding whether a mixed quantum state is separable is difficult. Even so, a useful necessary test follows from a short piece of linear algebra. Write the state in local operator bases, collect its two-body correlations in a matrix <a class="notation-ref" href="#definition-correlation-matrix" data-definition="Correlation matrix T: the coefficients of traceless observables on both subsystems." aria-describedby="glossary-correlation-desc">$T$</a>, and ask how large that matrix can be if the state is a mixture of product states.

The familiar test controls $T$ itself. A stronger necessary test controls

$$
C=T-rs^{\mathsf T},
$$

where <a class="notation-ref" href="#definition-bloch-vectors" data-definition="Local Bloch vectors r and s: coordinates of the two reduced states." aria-describedby="glossary-bloch-vectors-desc">$r$ and $s$</a> are the local Bloch vectors. The subtraction removes the correlation predicted from the local means alone. What remains is the <a class="notation-ref" href="#definition-centered-correlation" data-definition="Centered correlation matrix C: T with the product of the local means removed." aria-describedby="glossary-centered-desc">centered correlation matrix $C$</a>. The centered test is never weaker than the uncentered one and is sometimes strictly stronger.

This article derives both bounds with one fixed normalization. It then explains why the same language becomes subtler for three or more parties. The centered argument is elementary, but it belongs to a wider line of work on Bloch-representation criteria and covariance matrices; it is not presented here as a new entanglement criterion.

## Reading guide

The article has a complete bipartite core followed by a research-direction appendix.

**Bipartite core**

- [Bloch coordinates](#one-system-bloch-coordinates) fixes the normalization; the [notation glossary](#notation-glossary) gives short reminders.
- [The uncentered test](#from-product-states-to-the-de-vicente-bound) derives the de Vicente nuclear-norm bound.
- [Centering](#subtracting-the-local-means) turns the correlation matrix into a covariance and gives the marginal-dependent bound.
- [Equality and examples](#equality-pure-states-and-two-qubit-checks) identifies equality cases and calibrates both successes and false negatives. Readers interested only in the established bipartite criterion can stop after the [calibrated false negative](#a-calibrated-false-negative).

**Multipartite research directions**

- [More than two parties](#what-changes-for-more-than-two-parties) separates proved necessary bounds from the harder full projective-norm problem.
- [A practical ladder](#a-practical-ladder-of-multipartite-tests) compares computable relaxations; the [moment formulation](#a-possible-moment-problem-formulation) is explicitly a proposal rather than a completed criterion.

## Notation glossary

Only notation that recurs across several sections is linked. Hovering over, or focusing, a linked expression gives a short reminder; activating it moves to the full definition. External papers open in a separate tab.

<div class="notation-glossary">
  <dl>
    <dt><a href="#definition-bloch-vectors">$r,s$</a></dt>
    <dd id="glossary-bloch-vectors-desc">Bloch vectors of the two reduced states.</dd>

    <dt><a href="#definition-correlation-matrix">$T$</a></dt>
    <dd id="glossary-correlation-desc">The matrix of uncentered bipartite correlations.</dd>

    <dt><a href="#definition-centered-correlation">$C$</a></dt>
    <dd id="glossary-centered-desc">The centered matrix $T-rs^{\mathsf T}$.</dd>

    <dt><a href="#definition-bloch-radius">$R&#95;d$</a></dt>
    <dd id="glossary-radius-desc">The largest Euclidean norm of a Bloch vector in dimension $d$.</dd>

    <dt><a href="#definition-nuclear-norm">$\lVert\cdot\rVert&#95;*$</a></dt>
    <dd id="glossary-nuclear-desc">The nuclear norm: the sum of a matrix's singular values.</dd>

    <dt><a href="#definition-projective-norm">$\lVert\cdot\rVert&#95;{\pi,2}$</a></dt>
    <dd id="glossary-projective-desc">The projective tensor norm built from Euclidean local norms.</dd>

    <dt><a href="#definition-realignment">$\mathcal R$</a></dt>
    <dd id="glossary-realignment-desc">The realignment map used by the enhanced realignment and CCNR criteria.</dd>
  </dl>
</div>

## One-system Bloch coordinates

Let $\rho$ be a state on $\mathbb C^d$. Choose traceless Hermitian matrices

$$
\lambda_1,\ldots,\lambda_{d^2-1}
$$

normalized by

$$
\operatorname{Tr}(\lambda_i\lambda_j)=2\delta_{ij}.
$$

Then $\rho$ has a unique expansion

$$
\rho=\frac1d\left(I+\sum_{i=1}^{d^2-1}r_i\lambda_i\right).
$$

The real vector $r=(r_i)$ is the Bloch vector in this convention. Orthogonality gives

$$
\operatorname{Tr}(\rho^2)
=\frac1d+\frac{2}{d^2}\|r\|_2^2,
$$

and therefore

$$
\|r\|_2^2
=\frac{d^2}{2}\left(\operatorname{Tr}(\rho^2)-\frac1d\right).
$$

For a pure state, $\operatorname{Tr}(\rho^2)=1$, so

$$
\boxed{\|r\|_2=R_d:=\sqrt{\frac{d(d-1)}2}.}
$$
{: #definition-bloch-radius .definition-target }

For $d=2$, the generators are the Pauli matrices and $R_2=1$. For $d>2$, not every vector in the outer Euclidean ball is a physical Bloch vector. We will only need the radius bound.

## The bipartite correlation matrix

Consider a state on $\mathbb C^M\otimes\mathbb C^N$. Choose local generators $(\lambda_i)$ and $(\mu_j)$ with the same normalization. The state can be written as

$$
\rho_{AB}=\frac1{MN}\left(
I\otimes I
+\sum_i r_i\lambda_i\otimes I
+\sum_j s_j I\otimes\mu_j
+\sum_{i,j}t_{ij}\lambda_i\otimes\mu_j
\right).
$$

The local vectors $r$ and $s$ determine the reduced states:
{: #definition-bloch-vectors .definition-target }

$$
\rho_A=\frac1M\left(I+\sum_i r_i\lambda_i\right),
\qquad
\rho_B=\frac1N\left(I+\sum_j s_j\mu_j\right).
$$

The coefficients $t_{ij}$ form the correlation matrix $T$. They encode the part of the expansion that uses traceless observables on both sides.
{: #definition-correlation-matrix .definition-target }

Orthogonality gives the coefficient formulas directly:

$$
r_i=\frac M2\operatorname{Tr}(\rho_A\lambda_i),
\qquad
s_j=\frac N2\operatorname{Tr}(\rho_B\mu_j),
$$

and

$$
t_{ij}=\frac{MN}{4}
\operatorname{Tr}\!\left(\rho_{AB}\lambda_i\otimes\mu_j\right).
$$

Consequently, the observable covariance is a scaled entry of the centered matrix:

$$
\langle\lambda_i\otimes\mu_j\rangle
-\langle\lambda_i\rangle\langle\mu_j\rangle
=\frac{4}{MN}C_{ij}.
$$

Changing either orthonormal generator basis rotates $r$ and $s$ orthogonally and sends $C$ to $O_ACO_B^{\mathsf T}$. The Euclidean and nuclear norms used below therefore do not depend on the chosen generators.

If the state is a product,

$$
\rho_{AB}=\rho_A\otimes\rho_B,
$$

then direct multiplication shows that

$$
\boxed{T=rs^{\mathsf T}.}
$$

Thus $T$ has rank at most one. Its only nonzero singular value is

$$
\|r\|_2\|s\|_2,
$$

so

$$
\|rs^{\mathsf T}\|_*
=\|r\|_2\|s\|_2.
$$

The nuclear norm $\lVert X\rVert_*$ is the sum of the singular values of a matrix $X$.
{: #definition-nuclear-norm .definition-target }

This factorization is the basic step behind the separability test.

![Flow from product-state factorization to the centered covariance bound](/assets/images/centered-correlation-flow.svg)

**Figure 1.** The colors have the same meaning in every panel: teal denotes Alice's Bloch vectors and orange denotes Bob's. A product state produces the outer-product matrix $rs^{\mathsf T}$. A separable state produces a convex weighted sum of such rank-one matrices. Subtracting the outer product of the mean vectors moves both local clouds to zero, leaving outer products of the deviations $r_k-r$ and $s_k-s$—the centered covariance.

## From product states to the de Vicente bound

A bipartite state is separable if it admits a decomposition
{: #definition-separable-state .definition-target }

$$
\rho_{AB}=\sum_k p_k\,\rho_A^{(k)}\otimes\rho_B^{(k)},
\qquad
p_k\geq0,
\qquad
\sum_kp_k=1.
$$

We may refine the decomposition so that all local states are pure. If $r_k$ and $s_k$ are their Bloch vectors, then

$$
r=\sum_kp_kr_k,
\qquad
s=\sum_kp_ks_k,
\qquad
T=\sum_kp_k r_ks_k^{\mathsf T}.
$$

The triangle inequality and the rank-one factorization give

$$
\begin{aligned}
\|T\|_*
&\leq\sum_kp_k\|r_ks_k^{\mathsf T}\|_*\\
&=\sum_kp_k\|r_k\|_2\|s_k\|_2\\
&=R_MR_N.
\end{aligned}
$$

Hence every separable state satisfies

$$
\boxed{
\|T\|_*
\leq
\frac12\sqrt{MN(M-1)(N-1)}.
}
$$

This is the necessary condition proved by [de Vicente, Theorem 1](https://arxiv.org/pdf/quant-ph/0607195#page=6). A violation certifies entanglement. Satisfaction does not prove separability in general.

There is a tensor-norm way to read the same calculation. For two Euclidean spaces, the projective tensor norm agrees with the nuclear norm after identifying $r\otimes s$ with the matrix $rs^{\mathsf T}$:
{: #definition-projective-norm .definition-target }

$$
\|T\|_{\pi,2}=\|T\|_*.
$$

In the bipartite setting, “nuclear-norm criterion” and “projective Euclidean tensor-norm criterion” are therefore two descriptions of the same inequality.

## Subtracting the local means

The matrix $T$ contains two contributions at once. It contains correlations between local fluctuations, but it also contains the rank-one term predicted from the local mean vectors. Define

$$
\boxed{C:=T-rs^{\mathsf T}.}
$$
{: #definition-centered-correlation .definition-target }

For the separable decomposition above,

$$
\begin{aligned}
C
&=\sum_kp_kr_ks_k^{\mathsf T}
-\left(\sum_kp_kr_k\right)
 \left(\sum_\ell p_\ell s_\ell\right)^{\mathsf T}\\
&=\sum_kp_k(r_k-r)(s_k-s)^{\mathsf T}.
\end{aligned}
$$

This is exactly a cross-covariance matrix for the classical random vectors $r_k$ and $s_k$ drawn with probabilities $p_k$. The density matrix is quantum; the index $k$ in a chosen <a class="concept-ref" href="#definition-separable-state" data-definition="Separable state: a convex mixture of product states." aria-label="Separable state: a convex mixture of product states.">separable decomposition</a> is classical.

Refining to pure local states makes the variance identities below exact term by term. It is not required for validity: with mixed local states one has $\sum_kp_k\lVert r_k\rVert_2^2\leq R_M^2$ and the same final inequality follows.

The triangle inequality, the rank-one norm formula and then Cauchy–Schwarz give

$$
\begin{aligned}
\|C\|_*
&\leq
\sum_kp_k\|r_k-r\|_2\|s_k-s\|_2\\
&\leq
\sqrt{\sum_kp_k\|r_k-r\|_2^2}
\sqrt{\sum_kp_k\|s_k-s\|_2^2}.
\end{aligned}
$$

For a pure-state refinement,

$$
\begin{aligned}
\sum_kp_k\|r_k-r\|_2^2
&=\sum_kp_k\|r_k\|_2^2
-\left\|\sum_kp_kr_k\right\|_2^2\\
&=R_M^2-\|r\|_2^2\\
&=\frac{M^2}{2}\left(1-\operatorname{Tr}(\rho_A^2)\right).
\end{aligned}
$$

and similarly for Bob. The centered bound can therefore be written in variance-deficit form as

$$
\boxed{
\|C\|_*
\leq
\sqrt{
\left(R_M^2-\|r\|_2^2\right)
\left(R_N^2-\|s\|_2^2\right)
}.
}
$$

Using the purity identity gives the equivalent form

$$
\boxed{
\|T-rs^{\mathsf T}\|_*
\leq
\frac{MN}{2}
\sqrt{
\left(1-\operatorname{Tr}(\rho_A^2)\right)
\left(1-\operatorname{Tr}(\rho_B^2)\right)
}.
}
$$

The right-hand side adapts to the marginal states. If a marginal is nearly pure, its local variance is small and the permitted centered correlation shrinks. Local polarization literally consumes part of the correlation budget. If both marginals are maximally mixed, the centered bound returns to the same constant as the uncentered one.

It is important not to overstate the geometry. The map

$$
\rho_{AB}\longmapsto T-rs^{\mathsf T}
$$

is nonlinear because $r$ and $s$ also depend on the state. For fixed marginals, the inequality defines a clean norm ball. Across all marginals, it should not be described without qualification as one smaller convex body.

### The exact attribution through realignment

The operator and coefficient-matrix versions of centering are related by

$$
\rho_{AB}-\rho_A\otimes\rho_B
=\frac1{MN}\sum_{i,j}C_{ij}\lambda_i\otimes\mu_j.
$$

Realignment sends each tensor product to a rank-one matrix,
{: #definition-realignment .definition-target }

$$
\mathcal R(\lambda_i\otimes\mu_j)
=\operatorname{vec}(\lambda_i)\operatorname{vec}(\mu_j)^{\mathsf T},
$$

and each vectorized generator has Euclidean norm $\sqrt2$. Consequently,

$$
\left\|\mathcal R\!\left(
\rho_{AB}-\rho_A\otimes\rho_B
\right)\right\|_1
=\frac{2}{MN}\|C\|_*.
$$

The boxed centered inequality is therefore exactly [Theorem 1 of Zhang, Zhang, Zhang and Guo](https://arxiv.org/pdf/0709.3766#page=2), rewritten in the present Bloch normalization:

$$
\left\|\mathcal R\!\left(
\rho_{AB}-\rho_A\otimes\rho_B
\right)\right\|_1
\leq
\sqrt{
\left(1-\operatorname{Tr}(\rho_A^2)\right)
\left(1-\operatorname{Tr}(\rho_B^2)\right)
}.
$$

It was also recovered as a consequence of the covariance matrix criterion by [Gittsovich, Gühne, Hyllus and Eisert](https://arxiv.org/abs/0803.0757). The off-diagonal covariance block has entries

$$
\langle A_i\otimes B_j\rangle
-\langle A_i\rangle\langle B_j\rangle.
$$

In Bloch coordinates this is the same centering operation, up to the chosen basis normalization.

### Why the centered criterion is stronger

The implication needs only two lines. Let $a=\lVert r\rVert_2$ and $b=\lVert s\rVert_2$. If the centered inequality holds, then

$$
\begin{aligned}
\|T\|_*
&\leq \|C\|_*+ab\\
&\leq
\sqrt{(R_M^2-a^2)(R_N^2-b^2)}+ab\\
&\leq R_MR_N.
\end{aligned}
$$

The last step is Cauchy–Schwarz applied to the two vectors

$$
\left(\sqrt{R_M^2-a^2},a\right),
\qquad
\left(\sqrt{R_N^2-b^2},b\right).
$$

Thus every state passing the centered test also passes de Vicente. Equivalently, every violation detected by de Vicente is detected by the centered criterion. The converse fails, as the next example shows. This strict strengthening is proved in the Zhang paper and discussed explicitly in the later covariance-matrix treatment.

The computable cross-norm or realignment (CCNR) criterion says that every separable state satisfies $\lVert\mathcal R(\rho)\rVert_1\leq1$. The centered condition implies this bound as well. Writing $P_A=\operatorname{Tr}(\rho_A^2)$ and $P_B=\operatorname{Tr}(\rho_B^2)$,
{: #definition-ccnr .definition-target }

$$
\begin{aligned}
\|\mathcal R(\rho)\|_1
&\leq
\|\mathcal R(\rho-\rho_A\otimes\rho_B)\|_1
+\sqrt{P_AP_B}\\
&\leq
\sqrt{(1-P_A)(1-P_B)}+\sqrt{P_AP_B}\\
&\leq1.
\end{aligned}
$$

Thus a state satisfying the centered condition necessarily satisfies the CCNR bound as well.

Both tests are invariant under local unitaries. In Bloch coordinates these act by orthogonal transformations

$$
r\mapsto O_Ar,
\qquad
s\mapsto O_Bs,
\qquad
T\mapsto O_ATO_B^{\mathsf T},
$$

which preserve the relevant norms and marginal purities. If local filtering brings a state to filter normal form with $r=s=0$, then $C=T$ and the two tests coincide. Centering is not equivalent to filtering, but this explains why its advantage appears when the marginals are polarized.

## Equality, pure states, and two-qubit checks

For qubits, $M=N=2$, so a separable state must satisfy

$$
\|C\|_*
\leq
2\sqrt{
\left(1-\operatorname{Tr}(\rho_A^2)\right)
\left(1-\operatorname{Tr}(\rho_B^2)\right)
}.
$$

### Every two-term pure-product mixture saturates

This is not an isolated equality case. Let

$$
\rho=p\,\rho_A^{(1)}\otimes\rho_B^{(1)}
+q\,\rho_A^{(2)}\otimes\rho_B^{(2)},
\qquad q=1-p,
$$

with all four local states pure. If their Bloch vectors are $r_1,r_2,s_1,s_2$, then

$$
C=pq(r_1-r_2)(s_1-s_2)^{\mathsf T}.
$$

Hence

$$
\|C\|_*=pq\|r_1-r_2\|_2\|s_1-s_2\|_2.
$$

At the same time,

$$
R_M^2-\|r\|_2^2=pq\|r_1-r_2\|_2^2,
$$

and similarly for Bob. Equality therefore holds in the centered bound. In particular,

$$
\rho_p=p|00\rangle\langle00|+(1-p)|11\rangle\langle11|
$$

saturates it for every $p$. This shows that no smaller right-hand side depending only on the two marginal variances can hold for all separable states.

### Every entangled pure state violates

The opposite extreme is also clean. Write a bipartite pure state in Schmidt form,

$$
|\psi\rangle=\sum_i\sqrt{\lambda_i}\,|ii\rangle,
\qquad
P=\sum_i\lambda_i^2.
$$

In the matrix-unit operator basis, the realigned centered operator has off-diagonal singular values $\sqrt{\lambda_i\lambda_j}$ for $i\neq j$. Its diagonal block is

$$
\operatorname{diag}(\lambda)-\lambda\lambda^{\mathsf T}\succeq0,
$$

whose trace is $1-P$. Thus

$$
\left\|\mathcal R\!\left(
|\psi\rangle\langle\psi|-\rho_A\otimes\rho_B
\right)\right\|_1
=(1-P)+\sum_{i\neq j}\sqrt{\lambda_i\lambda_j}.
$$

The separable upper bound is $1-P$. It is therefore violated exactly when at least two Schmidt coefficients are nonzero. The criterion detects every entangled bipartite pure state.

### A family detected only after centering

Let

$$
|\phi_\gamma\rangle
=\cos\gamma\,|00\rangle
+\sin\gamma\,|11\rangle,
$$

and mix it with product noise that polarizes Alice while leaving Bob maximally mixed:

$$
\rho_{p,\gamma}
=p|\phi_\gamma\rangle\langle\phi_\gamma|
+(1-p)|0\rangle\langle0|\otimes\frac I2.
$$

Choose

$$
\sin(2\gamma)=0.6,
\qquad
\cos(2\gamma)=0.8,
\qquad
p=0.45.
$$

Computing the Bloch data directly from the density matrix gives

$$
T=\operatorname{diag}(0.27,-0.27,0.45),
\qquad
\|T\|_*=0.99.
$$

The de Vicente threshold for two qubits is $1$, so that test is silent. The <a class="notation-ref" href="#definition-bloch-vectors" data-definition="Local Bloch vectors r and s: coordinates of the two reduced states." aria-describedby="glossary-bloch-vectors-desc">local vectors</a> and <a class="notation-ref" href="#definition-centered-correlation" data-definition="Centered correlation matrix C: T with the product of the local means removed." aria-describedby="glossary-centered-desc">centered matrix</a> are

$$
r=(0,0,0.91),
\qquad
s=(0,0,0.36),
$$

and

$$
C=\operatorname{diag}(0.27,-0.27,0.1224),
\qquad
\|C\|_*=0.6624.
$$

The marginal purity deficits are

$$
1-\operatorname{Tr}(\rho_A^2)=0.08595,
\qquad
1-\operatorname{Tr}(\rho_B^2)=0.4352,
$$

so the centered budget is

$$
2\sqrt{0.08595\times0.4352}
\approx0.3868.
$$

The centered inequality is violated. This is the missing separation: the centered test detects the state while the uncentered test does not.

| Test | Observed quantity | Separable limit | Verdict |
|---|---:|---:|---|
| de Vicente | $\lVert T\rVert_*=0.99$ | $1$ | silent |
| centered | $\lVert C\rVert_*=0.6624$ | $0.3868$ | entangled |
| partial transpose | $\lambda_{\min}=-0.0552$ | $\lambda_{\min}\geq0$ | entangled |

The state is genuinely entangled. Its partial transpose contains the block

$$
\begin{pmatrix}
0.275 & 0.135\\
0.135 & 0
\end{pmatrix},
$$

whose determinant is negative. More generally, this family is NPT for every $p>0$ and $0<\gamma\leq\pi/4$.

![Detection regions for the polarized-noise family](/assets/images/centered-detection-regions.svg)

**Figure 2.** Every interior point of the $(p,\gamma)$ rectangle is NPT entangled. The grey region is missed by both norm criteria. The light teal region is detected only by the centered criterion, and the dark region is detected by both. The marked state is the numerical example above. The axis $\gamma=0$ is different from its right-hand limit: every state on the axis is separable, whereas for arbitrarily small $\gamma>0$ the centered detection threshold tends to $\sqrt5-2$. Open endpoints and the uncoloured vertical axis mark this discontinuity. Angular ticks are exact radian values.

The [NumPy script](https://github.com/kieranmcshane/kieranmcshane.github.io/blob/main/assets/code/centered_correlation_examples.py) constructs each $4\times4$ density matrix, takes its partial trace and partial transpose, and computes $r$, $s$, $T$, $C$ and both criteria from Pauli expectations. It also generates Figure 2 and its [boundary data](/assets/data/centered-detection-regions.csv). This is an independent numerical consistency check, not a proof.

<details markdown="1">
<summary><strong>Check your own two-qubit density matrix</strong></summary>

Save a Hermitian positive $4\times4$ NumPy array of trace one as `rho.npy`, then run:

```bash
python3 assets/code/centered_correlation_examples.py --matrix rho.npy
```

The program validates the input and prints $r$, $s$, $T$, $C$, both norm tests and the smallest partial-transpose eigenvalue. Only NumPy is required.

</details>

### A calibrated false negative

The criterion is not complete for mixed states. [Zhang and coauthors](https://arxiv.org/abs/0709.3766) consider

$$
\omega_p
=p|\psi^-\rangle\langle\psi^-|
+(1-p)\left(
\frac23|00\rangle\langle00|
+\frac13|01\rangle\langle01|
\right).
$$

Its partial transpose has a negative eigenvalue for every $p>0$, so every nontrivial member is entangled. The centered criterion, however, becomes violated only for

$$
p>0.220937\ldots.
$$

For example, $p=0.1$ is NPT but passes the centered test. The threshold above is recomputed from the density matrix by the linked script. This is a useful calibration: centering strengthens de Vicente and <a class="concept-ref" href="#definition-ccnr" data-definition="CCNR: a separable state must have realignment trace norm at most one." aria-label="CCNR: a separable state must have realignment trace norm at most one.">CCNR</a>, but it is still only a sufficient certificate of entanglement, not a characterization of mixed-state separability.

## What changes for more than two parties

> **Research-direction appendix.** The bipartite criterion, its attribution, equality cases and limitations are complete above. The remaining sections collect proved necessary multipartite bounds, computational relaxations and explicitly labelled proposals. They do not claim a complete multipartite separability criterion.

Suppose a full $g$-party correlation tensor has a separable decomposition

$$
\mathcal T
=\sum_kp_k\,
r_k^{(1)}\otimes\cdots\otimes r_k^{(g)}.
$$

The full projective Euclidean norm immediately obeys

$$
\|\mathcal T\|_{\pi,2}
\leq
\prod_{x=1}^g R_{d_x}.
$$

This is the intrinsic multipartite analogue of the bipartite calculation. Unlike the <a class="notation-ref" href="#definition-nuclear-norm" data-definition="Nuclear norm: the sum of a matrix's singular values." aria-describedby="glossary-nuclear-desc">matrix nuclear norm</a>, the full <a class="notation-ref" href="#definition-projective-norm" data-definition="Projective Euclidean tensor norm: the least weighted sum of products of local Euclidean norms." aria-describedby="glossary-projective-desc">projective tensor norm</a> is computationally hard: weak membership and approximation for third-order tensor nuclear-norm balls are NP-hard [in the sense made precise by Friedland and Lim](https://arxiv.org/abs/1410.6072).

Hassan and Joag take a more tractable route. A matrix unfolding groups some tensor factors into row indices and the rest into column indices. They compute the nuclear norm of each one-versus-the-rest unfolding and keep the largest value. Their [Theorem 1](https://arxiv.org/pdf/0704.3942#page=8) yields the same radius product as a necessary condition for full separability.
{: #definition-unfolding .definition-target }

For every unfolding,

$$
\|\mathcal T_{x\mid\widehat{x}}\|_*
\leq
\|\mathcal T\|_{\pi,2}.
$$

The reason is simple: every fully factorized tensor decomposition is also a valid rank-one matrix decomposition after grouping the remaining factors together. Taking the best matrix decomposition can only lower the infimum.

This distinction disappears for two parties, where the two norms coincide. For three or more parties, replacing the maximum unfolding norm by the full projective norm is generally a strengthening, not a change of notation.

Centering itself is canonical order by order. For three parties, the third central tensor is obtained from the raw subset tensors by

$$
\begin{aligned}
K_{ABC}={}&T_{ABC}
-r_A\otimes T_{BC}
-r_B\otimes T_{AC}
-r_C\otimes T_{AB}\\
&+2r_A\otimes r_B\otimes r_C,
\end{aligned}
$$

with tensor factors restored to $A,B,C$ order. For a fully separable decomposition this becomes

$$
K_{ABC}
=\sum_kp_k
(r_{A,k}-r_A)\otimes
(r_{B,k}-r_B)\otimes
(r_{C,k}-r_C).
$$

What is not canonical is choosing one tensor that captures the whole hierarchy. For example,

$$
|\Phi^+\rangle\langle\Phi^+|_{AB}\otimes\frac{I_C}{2}
$$

is not fully separable, but its traceless three-body tensor and $K_{ABC}$ both vanish. Its entanglement lives in the $AB$ tensor. The natural data are therefore the collection

$$
\{K_S: S\subseteq\{1,\ldots,g\},\ |S|\geq2\},
$$

together with the requirement that every member arise from one common separable ensemble.

There is nevertheless an elementary centered bound at every order. For party $a$, set

$$
V_a=R_{d_a}^2-\|r_a\|_2^2,
\qquad
D_a=R_{d_a}+\|r_a\|_2.
$$

For any subset $S$ with at least two parties, every fully separable state satisfies

$$
\boxed{
\|K_S\|_{\pi,2}
\leq
\min_{\substack{i,j\in S\\i<j}}
\left[
\sqrt{V_iV_j}
\prod_{\ell\in S\setminus\{i,j\}}D_\ell
\right].
}
$$

Indeed, choose $i,j\in S$, bound every other fluctuation by
$\lVert r_{\ell,k}-r_\ell\rVert_2\leq D_\ell$, and apply Cauchy–Schwarz to the remaining two factors. For $|S|=2$, this is exactly the bipartite centered inequality.

This estimate is recorded as a direct extension of the calculation, not as a novelty claim; its relation to existing multipartite covariance bounds would need a dedicated literature comparison.

The full norm is hard, but every bipartition flattening gives a computable lower bound:

$$
\|(K_S)_{P\mid S\setminus P}\|_*
\leq\|K_S\|_{\pi,2}.
$$

Thus exceeding the boxed bound with any flattening certifies failure of full separability. For four or more parties, balanced cuts should be checked alongside one-versus-the-rest cuts.

The tensors $K_S$ are central moments. They agree with connected, or cumulant, tensors through order three, but not from order four onward, where products of lower-order covariances must also be subtracted. A complete multipartite formulation must decide whether central moments or cumulants are the better coordinates and must enforce their common-ensemble compatibility.

## A practical ladder of multipartite tests

There is no single relaxation that turns the full multipartite projective norm into an SVD. It is more accurate to organize the available approaches as a ladder:

| Method | Computation | What it retains |
|---|---|---|
| <a class="concept-ref" href="#definition-unfolding" data-definition="Matrix unfolding: regroup tensor indices into row and column indices across a chosen bipartition." aria-label="Matrix unfolding: regroup tensor indices into row and column indices across a chosen bipartition.">Matrix unfoldings</a> | one SVD per bipartition | correlations visible across each chosen cut |
| Entanglement testers | local contractions followed by an output projective norm | a tunable transformation of the full state |
| Correlation-tensor moments | traces or moment matrices built from tensor singular data | more spectral information than one norm |
| Theta-body or moment relaxations | semidefinite programs of increasing order | progressively tighter outer approximations |

The tester framework of [Jivulescu, Lancien and Nechita](https://arxiv.org/abs/2010.06365) makes the second line precise. A local tester is a contraction

$$
\mathcal E_x:S_1^{d_x}\longrightarrow\ell_2^{n_x},
\qquad
\|\mathcal E_x\|_{S_1\to\ell_2}=1.
$$

For fully separable $\rho$,

$$
\left\|
(\mathcal E_1\otimes\cdots\otimes\mathcal E_g)(\rho)
\right\|_{\pi,2}
\leq1.
$$

<a class="notation-ref" href="#definition-realignment" data-definition="Realignment map: reshuffle bipartite operator indices into a matrix whose trace norm yields a separability test." aria-describedby="glossary-realignment-desc">Realignment</a> and SIC-POVM criteria fit into this language. The important caveat is that, with three or more output factors, evaluating the Euclidean projective norm can itself remain hard. Testers provide a systematic family of valid criteria and can reduce dimensions or exploit structure; they do not automatically make every multipartite instance polynomial-time.

Two other directions complement testers. [Huang and Jing](https://arxiv.org/abs/2402.13162) derive bipartite and multipartite criteria from moments of correlation tensors. [Rauhut and Stojanac](https://arxiv.org/abs/1505.05175) construct theta-body semidefinite relaxations of tensor nuclear-norm balls. The latter work concerns tensor recovery rather than quantum separability, so applying those relaxations to centered Bloch tensors would be a proposed method, not an existing centered criterion.

## A possible moment-problem formulation

There is a useful way to state that difficulty. Let $V_d$ denote the set of pure-state Bloch vectors in dimension $d$. It is a real algebraic set: substituting the Bloch expansion into $\rho^2=\rho$ gives polynomial relations in the Bloch coordinates.

The Euclidean radius condition replaces $V_d$ by its outer sphere. For $d>2$, that loses physical information: $V_d$ is a proper, generally non-centrally-symmetric subset of the sphere. The convex hull of product atoms drawn from the actual sets $V_{d_a}$ is therefore more naturally described by an atomic gauge than by a norm.

A bipartite state is separable exactly when there is a probability measure on $V_M\times V_N$ whose first moments are $r$ and $s$ and whose cross-moment is $T$. In this language, separability is a truncated moment problem.

At order two, introduce the unknown local covariance matrices

$$
K_A=\mathbb E[(R-r)(R-r)^{\mathsf T}],
\qquad
K_B=\mathbb E[(S-s)(S-s)^{\mathsf T}].
$$

They must satisfy

$$
\begin{pmatrix}
K_A & C\\
C^{\mathsf T} & K_B
\end{pmatrix}
\succeq0,
$$

with trace constraints

$$
\operatorname{Tr}K_A=R_M^2-\|r\|_2^2,
\qquad
\operatorname{Tr}K_B=R_N^2-\|s\|_2^2.
$$

Positivity of this block matrix implies

$$
\|C\|_*
\leq
\sqrt{\operatorname{Tr}K_A\,\operatorname{Tr}K_B}.
$$

Substituting only the two trace constraints yields the centered nuclear-norm inequality. Retaining the full matrices $K_A$ and $K_B$ keeps more information and moves toward the covariance matrix criterion.

This suggests a research program rather than a theorem claimed here: impose higher moment and localizing-matrix conditions on the pure-state Bloch varieties, keeping common moments across all correlation orders. Such a hierarchy would be a commutative moment counterpart to operator-side relaxations such as the [Doherty–Parrilo–Spedalieri hierarchy](https://arxiv.org/abs/quant-ph/0308032).

A precise open problem is to develop computable lower bounds on this physical atomic gauge that exploit the nonspherical qudit Bloch body while enforcing compatibility across all subset tensors. Establishing the relationship with existing separability hierarchies, and deciding whether centered moments or cumulants are the better coordinates, remains open.

## What this derivation establishes

The logical chain is short:

1. A product state gives $T=rs^{\mathsf T}$.
2. A separable state gives a convex sum of rank-one correlation matrices.
3. The projective norm factorizes on each rank-one term.
4. Subtracting $rs^{\mathsf T}$ rewrites the remainder as a covariance of local Bloch-vector fluctuations.
5. Cauchy–Schwarz turns the local variances into a bound involving the marginal purities.

The first three steps recover the de Vicente criterion. The final two explain why centered criteria depend naturally on the marginal states.

The equality analysis shows that every mixture of two pure product states saturates the centered bound, while the Schmidt-basis calculation shows that every entangled pure state violates it. The false-negative family records the complementary limitation for mixed states.

The subset bound gives a direct multipartite necessary condition, but it does not settle the compatibility problem. The full projective norm is harder to evaluate than matrix unfolding norms, and a useful multipartite formulation must organize several correlation orders at once. The moment formulation makes the missing common-ensemble constraints explicit; turning them into effective criteria is the research problem.

## References

- Julio I. de Vicente, [*Separability criteria based on the Bloch representation of density matrices*](https://arxiv.org/abs/quant-ph/0607195), *Quantum Information & Computation* **7** (2007), 624–638.
- Cheng-Jie Zhang, Yong-Sheng Zhang, Shun Zhang and Guang-Can Guo, [*Entanglement detection beyond the cross-norm or realignment criterion*](https://arxiv.org/abs/0709.3766), *Physical Review A* **77** (2008), 060301(R).
- Oleg Gittsovich, Otfried Gühne, Philipp Hyllus and Jens Eisert, [*Unifying several separability conditions using the covariance matrix criterion*](https://arxiv.org/abs/0803.0757), *Physical Review A* **78** (2008), 052319.
- Ali Saif M. Hassan and Pramod S. Joag, [*Separability Criterion for multipartite quantum states based on the Bloch representation of density matrices*](https://arxiv.org/abs/0704.3942), *Quantum Information & Computation* **8** (2008), 773–790.
- Otfried Gühne, Philipp Hyllus, Oleg Gittsovich and Jens Eisert, [*Covariance matrices and the separability problem*](https://arxiv.org/abs/quant-ph/0611282), *Physical Review Letters* **99** (2007), 130504.
- Shmuel Friedland and Lek-Heng Lim, [*Nuclear norm of higher-order tensors*](https://arxiv.org/abs/1410.6072), *Mathematics of Computation* **87** (2018), 1255–1281.
- Andrew C. Doherty, Pablo A. Parrilo and Federico M. Spedalieri, [*A complete family of separability criteria*](https://arxiv.org/abs/quant-ph/0308032), *Physical Review A* **69** (2004), 022308.
- Maria Anastasia Jivulescu, Cécilia Lancien and Ion Nechita, [*Multipartite entanglement detection via projective tensor norms*](https://arxiv.org/abs/2010.06365), *Annales Henri Poincaré* **23** (2022), 3791–3838.
- Xiaofen Huang and Naihuan Jing, [*Separability criteria based on the correlation tensor moments for arbitrary dimensional states*](https://arxiv.org/abs/2402.13162), *Quantum Information Processing* **23** (2024), 53.
- Holger Rauhut and Željka Stojanac, [*Tensor theta norms and low rank recovery*](https://arxiv.org/abs/1505.05175), *Numerical Algorithms* **88** (2021), 25–66.
