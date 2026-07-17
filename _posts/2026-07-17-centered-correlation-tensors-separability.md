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

The familiar test controls $T$ itself. A more informative object is often

$$
C=T-rs^{\mathsf T},
$$

where $r$ and $s$ are the local Bloch vectors. The subtraction removes the correlation predicted from the local means alone. What remains is a covariance matrix.

This article derives both bounds with one fixed normalization. It then explains why the same language becomes subtler for three or more parties. The centered argument is elementary, but it belongs to a wider line of work on Bloch-representation criteria and covariance matrices; it is not presented here as a new entanglement criterion.

## Reading guide

- [Bloch coordinates](#one-system-bloch-coordinates) fixes the normalization.
- [The uncentered test](#from-product-states-to-the-de-vicente-bound) derives the bipartite nuclear-norm bound.
- [Centering](#subtracting-the-local-means) turns the correlation matrix into a covariance and gives the marginal-dependent bound.
- [Two qubits](#two-qubit-checks) gives one separable and one entangled example.
- [More than two parties](#what-changes-for-more-than-two-parties) separates matrix unfoldings from the full projective tensor norm.

## Notation at a glance

| Symbol | Meaning |
|---|---|
| $r,s$ | Bloch vectors of the two reduced states |
| $T$ | Matrix of uncentered bipartite correlations |
| $C=T-rs^{\mathsf T}$ | Centered correlation matrix |
| $\|T\|_*$ | Nuclear norm: the sum of the singular values |
| $\|T\|_{\pi,2}$ | Projective tensor norm built from Euclidean local norms |

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

Applying the projective norm and Cauchy–Schwarz gives

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

Because the local states in the decomposition are pure,

$$
\sum_kp_k\|r_k-r\|_2^2
=R_M^2-\|r\|_2^2
=\frac{M^2}{2}\left(1-\operatorname{Tr}(\rho_A^2)\right),
$$

and similarly for Bob. We obtain the centered bound

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

The right-hand side adapts to the marginal states. If a marginal is nearly pure, its local variance is small and the permitted centered correlation shrinks. If both marginals are maximally mixed, the centered bound returns to the same constant as the uncentered one.

It is important not to overstate the geometry. The map

$$
\rho_{AB}\longmapsto T-rs^{\mathsf T}
$$

is nonlinear because $r$ and $s$ also depend on the state. For fixed marginals, the inequality defines a clean norm ball. Across all marginals, it should not be described without qualification as one smaller convex body.

The off-diagonal block of the covariance matrix in [Gühne, Hyllus, Gittsovich and Eisert](https://arxiv.org/pdf/quant-ph/0611282#page=2) has entries

$$
\langle A_i\otimes B_j\rangle
-\langle A_i\rangle\langle B_j\rangle.
$$

In Bloch coordinates this is the same centering operation, up to the chosen basis normalization. The calculation above is best viewed as the tensor-norm face of that covariance idea.

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

### A pure entangled family

Now take

$$
|\psi_\gamma\rangle
=\cos\gamma\,|00\rangle
+\sin\gamma\,|11\rangle,
\qquad
0<\gamma\leq\frac\pi4.
$$

Write $u=\sin(2\gamma)$. A direct Pauli calculation gives

$$
C=\operatorname{diag}(u,-u,u^2).
$$

Hence

$$
\|C\|_*=2u+u^2,
$$

while the separable upper bound equals $u^2$. Every entangled member of this pure-state family violates the centered inequality.

The short calculations above can be reproduced with [this NumPy script](https://github.com/kieranmcshane/kieranmcshane.github.io/blob/main/assets/code/centered_correlation_examples.py). The script checks both examples over a small numerical grid; it is a consistency check, not a proof.

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

This is the intrinsic multipartite analogue of the bipartite calculation. It is also difficult to compute in general.

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

## What this derivation establishes

The logical chain is short:

1. A product state gives $T=rs^{\mathsf T}$.
2. A separable state gives a convex sum of rank-one correlation matrices.
3. The projective norm factorizes on each rank-one term.
4. Subtracting $rs^{\mathsf T}$ rewrites the remainder as a covariance of local Bloch-vector fluctuations.
5. Cauchy–Schwarz turns the local variances into a bound involving the marginal purities.

The first three steps recover the de Vicente criterion. The final two explain why centered criteria depend naturally on the marginal states.

This does not yet settle the multipartite program. The full projective norm is harder to evaluate than matrix unfolding norms, and a useful multipartite centering must organize several correlation orders at once. That gap is precisely where the tensor-norm formulation becomes a research question rather than a notational rewrite.

## References

- Julio I. de Vicente, [*Separability criteria based on the Bloch representation of density matrices*](https://arxiv.org/abs/quant-ph/0607195), *Quantum Information & Computation* **7** (2007), 624–638.
- Ali Saif M. Hassan and Pramod S. Joag, [*Separability Criterion for multipartite quantum states based on the Bloch representation of density matrices*](https://arxiv.org/abs/0704.3942), 2007.
- Otfried Gühne, Philipp Hyllus, Oleg Gittsovich and Jens Eisert, [*Covariance matrices and the separability problem*](https://arxiv.org/abs/quant-ph/0611282), *Physical Review Letters* **99** (2007), 130504.
