---
layout: post
title: "Centered Correlation Tensors and Quantum Separability"
subtitle: "From Bloch vectors to a covariance bound"
date: 2026-07-17 08:00:00 +0200
categories: [quantum-information]
tags: [entanglement, separability, tensor-norms, Bloch-representation]
excerpt: "How the usual correlation-tensor separability test becomes a marginal-dependent covariance bound after centering."
---

Deciding whether a mixed quantum state is separable is difficult. Even so, a useful necessary test follows from a short piece of linear algebra. Write the state in local operator bases, collect its two-body correlations in a matrix $T$, and ask how large that matrix can be if the state is a mixture of product states.

The familiar test controls $T$ itself. A stronger necessary test controls

$$
C=T-rs^{\mathsf T},
$$

where $r$ and $s$ are the local Bloch vectors. The subtraction removes the correlation predicted from the local means alone. What remains is a covariance matrix. The centered test is never weaker than the uncentered one and is sometimes strictly stronger.

This article derives both bounds with one fixed normalization. It then explains why the same language becomes subtler for three or more parties. The centered argument is elementary, but it belongs to a wider line of work on Bloch-representation criteria and covariance matrices; it is not presented here as a new entanglement criterion.

## Reading guide

- [Bloch coordinates](#one-system-bloch-coordinates) fixes the normalization.
- [The uncentered test](#from-product-states-to-the-de-vicente-bound) derives the bipartite nuclear-norm bound.
- [Centering](#subtracting-the-local-means) turns the correlation matrix into a covariance and gives the marginal-dependent bound.
- [Two qubits](#two-qubit-checks) gives a separating example where centering detects entanglement and the uncentered test does not.
- [More than two parties](#what-changes-for-more-than-two-parties) separates matrix unfoldings from the full projective tensor norm.
- [Moment formulation](#a-possible-moment-problem-formulation) sketches a possible hierarchy and labels clearly what remains open.

## Notation at a glance

| Symbol | Meaning |
|---|---|
| $r,s$ | Bloch vectors of the two reduced states |
| $T$ | Matrix of uncentered bipartite correlations |
| $C=T-rs^{\mathsf T}$ | Centered correlation matrix |
| $\lVert T\rVert_*$ | Nuclear norm: the sum of the singular values |
| $\lVert T\rVert_{\pi,2}$ | Projective tensor norm built from Euclidean local norms |

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

$$
\rho_A=\frac1M\left(I+\sum_i r_i\lambda_i\right),
\qquad
\rho_B=\frac1N\left(I+\sum_j s_j\mu_j\right).
$$

The coefficients $t_{ij}$ form the correlation matrix $T$. They encode the part of the expansion that uses traceless observables on both sides.

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

This factorization is the basic step behind the separability test.

![Flow from product-state factorization to the centered covariance bound](/assets/images/centered-correlation-flow.svg)

**Figure 1.** A product state gives one rank-one tensor. A separable state gives a convex mixture of such tensors. Subtracting the product of the mean Bloch vectors rewrites the remainder as a covariance of local fluctuations.

## From product states to the de Vicente bound

A bipartite state is separable if it admits a decomposition

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

$$
\|T\|_{\pi,2}=\|T\|_*.
$$

In the bipartite setting, “nuclear-norm criterion” and “projective Euclidean tensor-norm criterion” are therefore two descriptions of the same inequality.

## Subtracting the local means

The matrix $T$ contains two contributions at once. It contains correlations between local fluctuations, but it also contains the rank-one term predicted from the local mean vectors. Define

$$
\boxed{C:=T-rs^{\mathsf T}.}
$$

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

This is exactly a cross-covariance matrix for the classical random vectors $r_k$ and $s_k$ drawn with probabilities $p_k$. The density matrix is quantum; the index $k$ in a chosen separable decomposition is classical.

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
\sum_kp_k\|r_k-r\|_2^2
=R_M^2-\|r\|_2^2
=\frac{M^2}{2}\left(1-\operatorname{Tr}(\rho_A^2)\right),
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

Both tests are invariant under local unitaries. In Bloch coordinates these act by orthogonal transformations

$$
r\mapsto O_Ar,
\qquad
s\mapsto O_Bs,
\qquad
T\mapsto O_ATO_B^{\mathsf T},
$$

which preserve the relevant norms and marginal purities. If local filtering brings a state to filter normal form with $r=s=0$, then $C=T$ and the two tests coincide. Centering is not equivalent to filtering, but this explains why its advantage appears when the marginals are polarized.

## Two-qubit checks

For qubits, $M=N=2$, so a separable state must satisfy

$$
\|C\|_*
\leq
2\sqrt{
\left(1-\operatorname{Tr}(\rho_A^2)\right)
\left(1-\operatorname{Tr}(\rho_B^2)\right)
}.
$$

### A separable family that saturates the bound

Consider

$$
\rho_p=p|00\rangle\langle00|+(1-p)|11\rangle\langle11|.
$$

Here

$$
r=s=(0,0,2p-1),
\qquad
T=\operatorname{diag}(0,0,1).
$$

Therefore

$$
C=\operatorname{diag}\bigl(0,0,4p(1-p)\bigr)
$$

and

$$
\|C\|_*=4p(1-p).
$$

The reduced-state purity is $p^2+(1-p)^2$, so the right-hand side of the centered inequality is also $4p(1-p)$. The family saturates the bound for every $p$.

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

The de Vicente threshold for two qubits is $1$, so that test is silent. The local vectors and centered matrix are

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

The state is genuinely entangled. Its partial transpose contains the block

$$
\begin{pmatrix}
0.275 & 0.135\\
0.135 & 0
\end{pmatrix},
$$

whose determinant is negative. More generally, this family is NPT for every $p>0$ and $0<\gamma\leq\pi/4$.

![Detection regions for the polarized-noise family](/assets/images/centered-detection-regions.svg)

**Figure 2.** Every interior point of the $(p,\gamma)$ rectangle is NPT entangled. The grey region is missed by both norm criteria. The light teal region is detected only by the centered criterion, and the dark region is detected by both. The marked state is the numerical example above. The axes $p=0$ and $\gamma=0$ are separable.

The [NumPy script](https://github.com/kieranmcshane/kieranmcshane.github.io/blob/main/assets/code/centered_correlation_examples.py) constructs each $4\times4$ density matrix, takes its partial trace and partial transpose, and computes $r$, $s$, $T$, $C$ and both criteria from Pauli expectations. It also generates Figure 2 and its [boundary data](/assets/data/centered-detection-regions.csv). This is an independent numerical consistency check, not a proof.

## What changes for more than two parties

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

This is the intrinsic multipartite analogue of the bipartite calculation. Unlike the matrix nuclear norm, it is computationally hard: weak membership and approximation for third-order tensor nuclear-norm balls are NP-hard [in the sense made precise by Friedland and Lim](https://arxiv.org/abs/1410.6072).

Hassan and Joag take a more tractable route. They unfold the tensor into a matrix across each one-versus-the-rest split, compute the nuclear norm of each unfolding, and keep the largest value. Their [Theorem 1](https://arxiv.org/pdf/0704.3942#page=8) yields the same radius product as a necessary condition for full separability.

For every unfolding,

$$
\|\mathcal T_{x\mid\widehat{x}}\|_*
\leq
\|\mathcal T\|_{\pi,2}.
$$

The reason is simple: every fully factorized tensor decomposition is also a valid rank-one matrix decomposition after grouping the remaining factors together. Taking the best matrix decomposition can only lower the infimum.

This distinction disappears for two parties, where the two norms coincide. For three or more parties, replacing the maximum unfolding norm by the full projective norm is generally a strengthening, not a change of notation.

Centering is also less automatic in the multipartite case. The third central moment

$$
\sum_kp_k
(r_k-r)\otimes(s_k-s)\otimes(t_k-t)
$$

is a natural object, but it does not by itself encode every lower-order centered tensor or the requirement that all of them arise from one common separable decomposition. Those compatibility conditions are part of the real difficulty.

## A possible moment-problem formulation

There is a useful way to state that difficulty. Let $V_d$ denote the set of pure-state Bloch vectors in dimension $d$. It is a real algebraic set: substituting the Bloch expansion into $\rho^2=\rho$ gives polynomial relations in the Bloch coordinates.

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

This suggests a research program rather than a theorem claimed here: impose higher moment and localizing-matrix conditions on the pure-state Bloch varieties, keeping common moments across all correlation orders. Such a hierarchy would be a commutative moment counterpart to operator-side relaxations such as the [Doherty–Parrilo–Spedalieri hierarchy](https://arxiv.org/abs/quant-ph/0308032). Establishing the exact relationship, and deciding which centered tensors or cumulants are the right coordinates, remains open.

## What this derivation establishes

The logical chain is short:

1. A product state gives $T=rs^{\mathsf T}$.
2. A separable state gives a convex sum of rank-one correlation matrices.
3. The projective norm factorizes on each rank-one term.
4. Subtracting $rs^{\mathsf T}$ rewrites the remainder as a covariance of local Bloch-vector fluctuations.
5. Cauchy–Schwarz turns the local variances into a bound involving the marginal purities.

The first three steps recover the de Vicente criterion. The final two explain why centered criteria depend naturally on the marginal states.

This does not yet settle the multipartite program. The full projective norm is harder to evaluate than matrix unfolding norms, and a useful multipartite centering must organize several correlation orders at once. The moment formulation makes the missing compatibility conditions explicit; turning it into effective criteria is the research problem.

## References

- Julio I. de Vicente, [*Separability criteria based on the Bloch representation of density matrices*](https://arxiv.org/abs/quant-ph/0607195), *Quantum Information & Computation* **7** (2007), 624–638.
- Chang-Jiang Zhang, Yong-Sheng Zhang, Shun Zhang and Guang-Can Guo, [*Entanglement detection beyond the computable cross-norm or realignment criterion*](https://arxiv.org/abs/0709.3766), *Physical Review A* **77** (2008), 060301(R).
- Oleg Gittsovich, Otfried Gühne, Philipp Hyllus and Jens Eisert, [*Unifying several separability conditions using the covariance matrix criterion*](https://arxiv.org/abs/0803.0757), *Physical Review A* **78** (2008), 052319.
- Ali Saif M. Hassan and Pramod S. Joag, [*Separability Criterion for multipartite quantum states based on the Bloch representation of density matrices*](https://arxiv.org/abs/0704.3942), *Quantum Information & Computation* **8** (2008), 773–790.
- Otfried Gühne, Philipp Hyllus, Oleg Gittsovich and Jens Eisert, [*Covariance matrices and the separability problem*](https://arxiv.org/abs/quant-ph/0611282), *Physical Review Letters* **99** (2007), 130504.
- Shmuel Friedland and Lek-Heng Lim, [*Nuclear norm of higher-order tensors*](https://arxiv.org/abs/1410.6072), *Mathematics of Computation* **87** (2018), 1255–1281.
- Andrew C. Doherty, Pablo A. Parrilo and Federico M. Spedalieri, [*A complete family of separability criteria*](https://arxiv.org/abs/quant-ph/0308032), *Physical Review A* **69** (2004), 022308.
