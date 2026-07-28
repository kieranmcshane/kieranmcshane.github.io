---
layout: post
math: true
title: "Galois Theory Without Detours"
subtitle: "Fields, symmetries, fixed points, and the fundamental correspondence"
date: 2026-07-27 11:00:00 +0200
last_modified_at: 2026-07-28 02:15:00 +0200
categories: [mathematics]
tags: [algebra, field-theory, group-theory, Galois-theory]
excerpt: "A self-contained route from undergraduate algebra to the fundamental theorem of Galois theory, with a rigorous proof and complete V4 and A4 correspondence diagrams."
---

<div class="longform-post galois-post" markdown="1">

Galois theory is often summarized by a picture: a lattice of fields beside an upside-down lattice of groups. The slogan is that intermediate fields correspond to subgroups. That summary is correct, but compressed enough to hide almost every reason it is true.

This article unpacks the picture directly. We will begin with one field in which every calculation can be done by hand,

$$
L=\mathbb Q(\sqrt2,\sqrt3),
$$

and discover its four symmetries. We will see that the three nontrivial proper subgroups fix exactly the three quadratic fields

$$
\mathbb Q(\sqrt2),\qquad
\mathbb Q(\sqrt3),\qquad
\mathbb Q(\sqrt6).
$$

Only after that concrete calculation will we introduce the general definitions needed to state and prove the theorem. The proof is complete: it includes the linear independence of distinct field homomorphisms, Artin's fixed-field theorem, the degree formulas, and the normal-subgroup quotient statement. The final section uses the subgroup structure of $A_4$ to reconstruct a much larger field lattice.

The intended reader knows undergraduate linear algebra, basic polynomial algebra, and the definitions of a group and a subgroup. Nothing from ring theory beyond polynomial division is assumed.

<div class="longform-reading-layout" markdown="1">

<nav class="longform-toc" aria-label="Article navigation" data-section-navigation>
  <details class="longform-toc-details" open>
    <summary>Contents</summary>
    <div class="toc-section-links">
      <a href="#the-destination">The destination</a>
      <a href="#start-with-the-diamond">1. The diamond</a>
      <a href="#field-extensions-and-degree">2. Extensions and degree</a>
      <a href="#why-automorphisms-permute-roots">3. Automorphisms and roots</a>
      <a href="#splitting-fields-separability-and-normality">4. Splitting fields</a>
      <a href="#fixed-fields-and-inclusion-reversal">5. Fixed fields</a>
      <a href="#the-fundamental-theorem">6. Fundamental theorem</a>
      <a href="#proof-core-i-independence-of-homomorphisms">7–10. Proof core</a>
      <a href="#re-reading-the-biquadratic-example">11–13. Worked examples</a>
      <a href="#decoding-an-a4-lattice">The \(A_4\) lattice</a>
      <a href="#how-to-use-the-theorem-in-practice">14. Using the theorem</a>
      <a href="#common-mistakes">15. Common mistakes</a>
      <a href="#what-the-theorem-is-really-saying">16. The big picture</a>
      <a href="#a-compact-checklist">Checklist</a>
      <a href="#comprehension-checks-with-solutions">Exercises</a>
      <a href="#further-reading">Further reading</a>
    </div>
  </details>
</nav>

<div class="longform-main" markdown="1">

## The destination

Let $L/K$ be a finite Galois extension and set

$$
G=\operatorname{Gal}(L/K).
$$

The fundamental theorem of Galois theory gives mutually inverse maps

$$
\left\{
\begin{array}{c}
\text{intermediate fields }E\\
K\subseteq E\subseteq L
\end{array}
\right\}
\longleftrightarrow
\left\{
\begin{array}{c}
\text{subgroups }H\\
H\leq G
\end{array}
\right\},
$$

defined by

$$
E\longmapsto\operatorname{Gal}(L/E),
\qquad
H\longmapsto L^H.
$$

Here $L^H$ is the set of elements fixed by every member of $H$. The correspondence reverses inclusions:

$$
E_1\subseteq E_2
\quad\Longleftrightarrow\quad
\operatorname{Gal}(L/E_2)
\subseteq
\operatorname{Gal}(L/E_1).
$$

It also turns orders and indices into field degrees:

$$
[L:L^H]=|H|,
\qquad
[L^H:K]=[G:H].
$$

Finally,

$$
L^H/K\text{ is Galois}
\quad\Longleftrightarrow\quad
H\trianglelefteq G,
$$

and in that case

$$
\operatorname{Gal}(L^H/K)\cong G/H.
$$

This is the target. The rest of the article explains what every symbol means and why every assertion holds.

## 1. Start with the diamond

Consider

$$
L=\mathbb Q(\sqrt2,\sqrt3).
$$

This is the smallest example that displays the full shape of the correspondence. A single quadratic extension has only a top and a bottom. A biquadratic extension has three genuinely different intermediate fields, so the lattice becomes visible.

### Writing every element

Adjoining $\sqrt2$ first gives

$$
\mathbb Q\subseteq\mathbb Q(\sqrt2).
$$

Every element of $\mathbb Q(\sqrt2)$ is $a+b\sqrt2$ with $a,b\in\mathbb Q$. Now adjoin $\sqrt3$. Every element of $L$ can be written

$$
x=(a+b\sqrt2)+(c+d\sqrt2)\sqrt3,
$$

or equivalently

$$
x=a+b\sqrt2+c\sqrt3+d\sqrt6,
\qquad a,b,c,d\in\mathbb Q.
$$

The four displayed basis elements are linearly independent over $\mathbb Q$. To see the only non-obvious point, suppose that $\sqrt3$ belonged to $\mathbb Q(\sqrt2)$. Then

$$
\sqrt3=a+b\sqrt2
$$

for some rational $a,b$. Squaring gives

$$
3=a^2+2b^2+2ab\sqrt2.
$$

Thus $ab=0$. If $a=0$, then $b^2=3/2$, impossible for rational $b$; if $b=0$, then $a^2=3$, impossible for rational $a$. Hence $\sqrt3\notin\mathbb Q(\sqrt2)$, and

$$
[L:\mathbb Q]=4.
$$

### Finding the automorphisms

A $\mathbb Q$-automorphism of $L$ is a bijection $\sigma:L\to L$ that preserves addition and multiplication and fixes every rational number. It is not merely an invertible map of sets or vector spaces.

Because

$$
(\sqrt2)^2=2,
$$

we must have

$$
\sigma(\sqrt2)^2=\sigma(2)=2.
$$

Inside $L$, this forces $\sigma(\sqrt2)=\sqrt2$ or $-\sqrt2$. Similarly,

$$
\sigma(\sqrt3)=\sqrt3
\quad\text{or}\quad
\sigma(\sqrt3)=-\sqrt3.
$$

All four choices are compatible with the field operations. They give

$$
\begin{array}{c|cc}
&\sqrt2&\sqrt3\\
\hline
1&\sqrt2&\sqrt3\\
\sigma&-\sqrt2&\sqrt3\\
\tau&\sqrt2&-\sqrt3\\
\sigma\tau&-\sqrt2&-\sqrt3.
\end{array}
$$

Once the images of $\sqrt2$ and $\sqrt3$ are known, the image of every element is known. For instance,

$$
\sigma(a+b\sqrt2+c\sqrt3+d\sqrt6)
=a-b\sqrt2+c\sqrt3-d\sqrt6.
$$

Composition gives

$$
\sigma^2=\tau^2=1,
\qquad
\sigma\tau=\tau\sigma.
$$

Therefore

$$
G=\operatorname{Gal}(L/\mathbb Q)
=\{1,\sigma,\tau,\sigma\tau\}
\cong C_2\times C_2.
$$

This group is the Klein four-group, denoted $V_4$.

### Computing the fixed fields

The subgroup $\langle\sigma\rangle=\{1,\sigma\}$ fixes $x$ precisely when $\sigma(x)=x$. Comparing coefficients in

$$
a-b\sqrt2+c\sqrt3-d\sqrt6
=
a+b\sqrt2+c\sqrt3+d\sqrt6
$$

gives $b=d=0$. Thus

$$
L^{\langle\sigma\rangle}
=\mathbb Q(\sqrt3).
$$

Similarly,

$$
L^{\langle\tau\rangle}
=\mathbb Q(\sqrt2),
$$

and because $\sigma\tau$ changes both signs but leaves their product fixed,

$$
L^{\langle\sigma\tau\rangle}
=\mathbb Q(\sqrt6).
$$

The identity fixes all of $L$, while the whole group fixes only $\mathbb Q$. We have already found the entire correspondence:

| Subgroup $H\leq G$ | Order $\lvert H\rvert$ | Fixed field $L^H$ | Degree $[L^H:\mathbb Q]$ |
|---|---:|---|---:|
| $\lbrace 1\rbrace$ | $1$ | $\mathbb Q(\sqrt2,\sqrt3)$ | $4$ |
| $\langle\sigma\rangle$ | $2$ | $\mathbb Q(\sqrt3)$ | $2$ |
| $\langle\tau\rangle$ | $2$ | $\mathbb Q(\sqrt2)$ | $2$ |
| $\langle\sigma\tau\rangle$ | $2$ | $\mathbb Q(\sqrt6)$ | $2$ |
| $G$ | $4$ | $\mathbb Q$ | $1$ |

<figure class="post-figure" id="biquadratic-lattice-diagram">
  <div class="post-figure-media post-figure-media-wide">
    <img src="{{ '/assets/images/galois-v4-correspondence.svg' | relative_url }}" alt="The subgroup diamond of the Klein four-group beside the reversed intermediate-field diamond for Q square root 2 square root 3.">
  </div>
  <figcaption>The biquadratic correspondence. Moving upward on the field side means moving downward on the group side.</figcaption>
</figure>

The reversal has a simple meaning:

> More symmetries impose more fixed-point conditions, so a larger subgroup fixes a smaller field.

Everything in the general theorem is already present in this diamond. What remains is to identify the hypotheses that make the phenomenon reliable and to prove that no fields or subgroups are missing.

## 2. Field extensions and degree

A field extension $L/K$ means that $K$ is a subfield of $L$. The notation remembers which field supplies the scalars. Because $L$ is a vector space over $K$, its degree is

$$
[L:K]=\dim_K L.
$$

If this dimension is finite, $L/K$ is called a finite extension.

### The tower formula

Suppose

$$
K\subseteq E\subseteq L,
$$

with $[E:K]=m$ and $[L:E]=n$. Choose a $K$-basis

$$
e_1,\ldots,e_m
$$

of $E$ and an $E$-basis

$$
\ell_1,\ldots,\ell_n
$$

of $L$. Then the $mn$ products

$$
e_i\ell_j
$$

form a $K$-basis of $L$.

They span because any $x\in L$ can first be written as

$$
x=\sum_j a_j\ell_j,
\qquad a_j\in E,
$$

and each $a_j$ can then be expanded in the $e_i$. For independence, if

$$
\sum_{i,j}c_{ij}e_i\ell_j=0,
\qquad c_{ij}\in K,
$$

then

$$
\sum_j\left(\sum_i c_{ij}e_i\right)\ell_j=0.
$$

The $E$-independence of the $\ell_j$ makes every inner sum zero, and the $K$-independence of the $e_i$ makes every $c_{ij}$ zero. Therefore

$$
\boxed{[L:K]=[L:E][E:K].}
$$

For the running example,

$$
[L:\mathbb Q]
=
[L:\mathbb Q(\sqrt2)]
[\mathbb Q(\sqrt2):\mathbb Q]
=2\cdot2.
$$

The same multiplication will later become

$$
|G|=|H|[G:H].
$$

The numerical part of Galois theory works because the tower formula for fields and Lagrange's formula for finite groups have exactly the same shape.

### Algebraic elements and minimal polynomials

An element $\alpha$ in an extension of $K$ is algebraic over $K$ if some nonzero polynomial in $K[X]$ vanishes at $\alpha$. Among all such polynomials there is a unique monic polynomial of smallest degree. It is the minimal polynomial of $\alpha$ over $K$, written $m_{\alpha,K}$.

The minimal polynomial is irreducible. If

$$
m_{\alpha,K}=fg
$$

with $f,g\in K[X]$ of smaller positive degree, then

$$
0=m_{\alpha,K}(\alpha)=f(\alpha)g(\alpha).
$$

A field has no zero divisors, so one factor vanishes at $\alpha$, contradicting minimality.

The simple extension $K(\alpha)$ consists of rational expressions in $\alpha$ with coefficients in $K$. Division by the minimal polynomial reduces every expression to

$$
a_0+a_1\alpha+\cdots+a_{d-1}\alpha^{d-1},
$$

where $d=\deg m_{\alpha,K}$. These $d$ powers are linearly independent, since a dependence would produce a polynomial of degree below $d$ that vanishes at $\alpha$. Hence

$$
\boxed{[K(\alpha):K]=\deg m_{\alpha,K}.}
$$

Equivalently,

$$
K(\alpha)\cong K[X]/(m_{\alpha,K}).
$$

For example, $X^2-2$ is irreducible over $\mathbb Q$, so

$$
[\mathbb Q(\sqrt2):\mathbb Q]=2.
$$

This vector-space viewpoint is all the field construction machinery we need.

## 3. Why automorphisms permute roots

Let $\varphi:L\to M$ be a field homomorphism that fixes $K$. If

$$
f(X)=a_0+a_1X+\cdots+a_nX^n\in K[X],
$$

then

$$
\varphi(f(\alpha))
=
a_0+a_1\varphi(\alpha)+\cdots+a_n\varphi(\alpha)^n
=
f(\varphi(\alpha)).
$$

Consequently,

$$
f(\alpha)=0
\quad\Longrightarrow\quad
f(\varphi(\alpha))=0.
$$

A $K$-homomorphism can send an algebraic element only to another root of its minimal polynomial.

This elementary calculation explains the link between fields and permutations. If a field is generated by roots of polynomials, an automorphism must permute those roots in a way compatible with every algebraic relation among them.

### Generators determine homomorphisms

If

$$
L=K(\alpha_1,\ldots,\alpha_r),
$$

then a $K$-homomorphism out of $L$ is completely determined by the images of the generators. The images cannot be chosen arbitrarily: each $\alpha_i$ must go to a suitable conjugate, and all relations among the generators must remain true.

For $L=\mathbb Q(\sqrt2,\sqrt3)$, choosing signs independently preserves all relations, so all four possibilities work. In a less separable presentation, a plausible permutation of roots may fail because it does not preserve a relation among them. “The Galois group permutes the roots” is therefore only the beginning: it acts as a particular subgroup of the full permutation group.

### An upper bound on the number of embeddings

Suppose $L=K(\alpha)$ and the minimal polynomial of $\alpha$ has degree $d$. A $K$-homomorphism $L\to\Omega$ into a larger field is determined by $\alpha$, and $\alpha$ has at most $d$ possible images. Therefore there are at most $d=[L:K]$ such homomorphisms.

For a general finite extension, adjoining generators one at a time and applying the tower formula gives the same conclusion:

$$
\#\operatorname{Hom}_K(L,\Omega)\leq[L:K].
$$

In particular,

$$
|\operatorname{Aut}(L/K)|\leq[L:K].
$$

Galois extensions are precisely the finite extensions for which the right number of automorphisms is available.

## 4. Splitting fields, separability, and normality

The correspondence cannot work for every finite extension. The simplest warning is

$$
L=\mathbb Q(\sqrt[3]{2}).
$$

The minimal polynomial $X^3-2$ has three complex roots:

$$
\sqrt[3]{2},\qquad
\omega\sqrt[3]{2},\qquad
\omega^2\sqrt[3]{2},
$$

where $\omega=e^{2\pi i/3}$. Only the real root belongs to $L$. A $\mathbb Q$-automorphism of $L$ must send $\sqrt[3]{2}$ to a root that still lies in $L$, so it has no choice:

$$
\operatorname{Aut}(L/\mathbb Q)=\{1\},
$$

even though

$$
[L:\mathbb Q]=3.
$$

The automorphism group is too small to recover the intermediate-field structure. The missing complex roots indicate the missing hypothesis.

### Splitting fields

Let $f\in K[X]$. A splitting field of $f$ over $K$ is a smallest extension $L/K$ in which

$$
f(X)=c\prod_{i=1}^n(X-\alpha_i)
$$

for roots $\alpha_i\in L$. Equivalently,

$$
L=K(\alpha_1,\ldots,\alpha_n).
$$

For example, the splitting field of

$$
(X^2-2)(X^2-3)
$$

over $\mathbb Q$ is $\mathbb Q(\sqrt2,\sqrt3)$.

The splitting field of $X^3-2$ is

$$
\mathbb Q(\sqrt[3]{2},\omega),
$$

which has degree $6$ over $\mathbb Q$. It has enough automorphisms to permute all three roots, and its Galois group is isomorphic to $S_3$.

### Separable polynomials

A polynomial is separable if it has no repeated root in a splitting field. An irreducible polynomial $f$ has a repeated root precisely when $f$ and its formal derivative $f'$ have a common factor. In characteristic zero, an irreducible nonconstant polynomial cannot divide its derivative because the derivative has smaller degree. Thus every algebraic extension of $\mathbb Q$ is separable.

The word matters in positive characteristic. Over $\mathbb F_p(t)$, the polynomial

$$
X^p-t
$$

has derivative zero. In an extension containing a $p$th root $\alpha$ of $t$,

$$
X^p-t=(X-\alpha)^p.
$$

There is only one distinct root, repeated $p$ times. Counting conjugates no longer behaves as it does over $\mathbb Q$.

An algebraic extension $L/K$ is separable if every element of $L$ has a separable minimal polynomial over $K$.

### Normal extensions

An algebraic extension $L/K$ is normal if every irreducible polynomial in $K[X]$ that has one root in $L$ splits completely over $L$.

For finite extensions, normality is equivalent to being a splitting field of some family of polynomials over $K$. It prevents the defect seen in $\mathbb Q(\sqrt[3]{2})$: if one conjugate appears, all conjugates appear.

### Galois extensions

A finite extension is Galois if it is both normal and separable:

$$
\boxed{
L/K\text{ finite Galois}
\quad\Longleftrightarrow\quad
L/K\text{ finite, normal, and separable}.
}
$$

Equivalently, $L$ is the splitting field over $K$ of a separable polynomial.

Another equivalent condition, to be proved below, is

$$
|\operatorname{Aut}(L/K)|=[L:K].
$$

The running extension $\mathbb Q(\sqrt2,\sqrt3)/\mathbb Q$ is the splitting field of the separable polynomial

$$
(X^2-2)(X^2-3),
$$

so it is Galois.

The theorem in this article is initially and deliberately finite. For an infinite Galois extension, intermediate fields correspond to **closed** subgroups under the Krull topology, not to arbitrary subgroups. That is a genuine additional layer of theory, not a harmless omission of the word “finite.”

## A bridge: embeddings, normality, and the automorphism count

We have used three descriptions of a finite Galois extension:

1. finite, normal, and separable;
2. the splitting field of a separable polynomial;
3. an extension with as many automorphisms as its degree.

It is worth proving why these descriptions agree. This also supplies the embedding count used later in the proof of the correspondence.

### Extending an embedding by one algebraic element

Suppose $E$ is a field, $\alpha$ is algebraic over $E$, and

$$
\varphi:E\longrightarrow\Omega
$$

is a field embedding into an algebraically closed field $\Omega$. Let

$$
m_{\alpha,E}(X)
=a_0+a_1X+\cdots+a_dX^d
$$

be the minimal polynomial of $\alpha$ over $E$. Apply $\varphi$ to the coefficients:

$$
\varphi(m_{\alpha,E})(X)
=
\varphi(a_0)+\varphi(a_1)X+\cdots+\varphi(a_d)X^d.
$$

Because $\Omega$ is algebraically closed, this transformed polynomial has a root $\beta\in\Omega$. The assignment

$$
\alpha\longmapsto\beta
$$

extends $\varphi$ uniquely to an embedding

$$
\widetilde\varphi:E(\alpha)\longrightarrow\Omega.
$$

To see why it is well-defined, use

$$
E(\alpha)\cong E[X]/(m_{\alpha,E}).
$$

Evaluating the transformed coefficients at $\beta$ annihilates exactly the relation used in the quotient. Conversely, every extension of $\varphi$ must send $\alpha$ to a root of $\varphi(m_{\alpha,E})$.

Thus the number of extensions of $\varphi$ is the number of distinct roots of the transformed minimal polynomial. It is at most

$$
d=[E(\alpha):E],
$$

and it equals $d$ when the polynomial is separable.

### Counting embeddings in a finite separable extension

Let $L/K$ be finite. Choose finitely many algebraic generators and form a tower

$$
K=K_0\subseteq K_1\subseteq\cdots\subseteq K_r=L,
$$

where

$$
K_i=K_{i-1}(\alpha_i).
$$

Fix an algebraic closure $\overline K$. Start with the identity embedding of $K$. At the $i$th stage, each embedding of $K_{i-1}$ has at most

$$
[K_i:K_{i-1}]
$$

extensions to $K_i$. Multiplying the bounds and using the tower formula gives

$$
\#\operatorname{Hom}_K(L,\overline K)
\leq
\prod_{i=1}^r[K_i:K_{i-1}]
=
[L:K].
$$

If $L/K$ is separable, every minimal polynomial encountered in the tower is separable. Each stage then attains its bound, so

$$
\boxed{
\#\operatorname{Hom}_K(L,\overline K)=[L:K].
}
$$

This is the precise meaning of “separability supplies all conjugate embeddings.” Without separability, repeated roots cause some of the possible branches to collapse.

### What normality adds

An embedding

$$
\sigma:L\longrightarrow\overline K
$$

need not have image inside $L$. That is exactly what happens to the embeddings of $\mathbb Q(\sqrt[3]{2})$: two send the real cube root to nonreal roots outside the original field.

If $L/K$ is normal, every minimal polynomial over $K$ with one root in $L$ splits in $L$. For any $\alpha\in L$, the element $\sigma(\alpha)$ is another root of $m_{\alpha,K}$, so

$$
\sigma(\alpha)\in L.
$$

Hence every $K$-embedding $L\to\overline K$ has image in $L$. Since $L/K$ is finite, an injective map $L\to L$ is also surjective as a $K$-linear map. Every embedding is therefore an automorphism.

If $L/K$ is both normal and separable, we conclude that

$$
|\operatorname{Aut}(L/K)|
=
\#\operatorname{Hom}_K(L,\overline K)
=
[L:K].
$$

Conversely, suppose

$$
|\operatorname{Aut}(L/K)|=[L:K].
$$

The general embedding bound shows that $L/K$ must have the maximum possible number of distinct embeddings, which forces separability. All of those embeddings already appear as automorphisms of $L$, so every $K$-embedding into an algebraic closure maps $L$ back to itself.

Now take an irreducible $f\in K[X]$ with a root $\alpha\in L$, and let $\beta$ be any other root in $\overline K$. The map

$$
K(\alpha)\longrightarrow\overline K,
\qquad
\alpha\longmapsto\beta,
$$

is a $K$-embedding. By repeatedly applying the one-element extension argument, it extends to a $K$-embedding of $L$ into $\overline K$. By our hypothesis its image is $L$, so $\beta\in L$. Thus every conjugate of every element of $L$ lies in $L$, and $L/K$ is normal.

We have proved

$$
\boxed{
L/K\text{ finite Galois}
\quad\Longleftrightarrow\quad
|\operatorname{Aut}(L/K)|=[L:K].
}
$$

This equivalence is not a competing definition. It is the numerical form of the two structural requirements: separability creates the full set of embeddings, and normality keeps their images inside the field.

## 5. Fixed fields and inclusion reversal

Let $L/K$ be finite Galois and write

$$
G=\operatorname{Gal}(L/K).
$$

There are two natural constructions.

### From a field to a subgroup

Given an intermediate field

$$
K\subseteq E\subseteq L,
$$

define

$$
\operatorname{Gal}(L/E)
=
\{\sigma\in G:\sigma(x)=x\text{ for every }x\in E\}.
$$

This is a subgroup: the identity fixes $E$, a composition of maps fixing $E$ again fixes $E$, and the inverse of a map fixing $E$ fixes $E$.

If

$$
E_1\subseteq E_2,
$$

then fixing every element of $E_2$ is a stronger requirement than fixing every element of $E_1$. Therefore

$$
\operatorname{Gal}(L/E_2)
\subseteq
\operatorname{Gal}(L/E_1).
$$

### From a subgroup to a field

Given $H\leq G$, define the fixed field

$$
L^H
=
\{x\in L:\sigma(x)=x\text{ for every }\sigma\in H\}.
$$

It is a field. If $x,y\in L^H$ and $\sigma\in H$, then

$$
\sigma(x+y)=\sigma(x)+\sigma(y)=x+y,
$$

$$
\sigma(xy)=\sigma(x)\sigma(y)=xy,
$$

and, for $x\neq0$,

$$
\sigma(x^{-1})=\sigma(x)^{-1}=x^{-1}.
$$

Every element of $K$ is fixed by all of $G$, hence by $H$, so

$$
K\subseteq L^H\subseteq L.
$$

If

$$
H_1\subseteq H_2,
$$

then being fixed by every member of $H_2$ imposes at least as many conditions as being fixed by every member of $H_1$. Hence

$$
L^{H_2}\subseteq L^{H_1}.
$$

### The easy inclusions

The two operations almost look inverse before any serious theorem is used.

Every element of $E$ is fixed by $\operatorname{Gal}(L/E)$, so

$$
E\subseteq L^{\operatorname{Gal}(L/E)}.
$$

Every element of $H$ fixes $L^H$, so

$$
H\subseteq\operatorname{Gal}(L/L^H).
$$

The difficult point is equality. Why can the field on the right not be larger? Why can the group on the right not contain extra automorphisms? The answer comes from degree counting, and the key degree count is Artin's theorem.

## 6. The fundamental theorem

We can now state the result precisely.

> **Fundamental theorem of finite Galois theory.**  
> Let $L/K$ be a finite Galois extension and let $G=\operatorname{Gal}(L/K)$. The maps
>
> $$
> E\longmapsto\operatorname{Gal}(L/E),
> \qquad
> H\longmapsto L^H
> $$
>
> are mutually inverse, inclusion-reversing bijections between the intermediate fields $K\subseteq E\subseteq L$ and the subgroups $H\leq G$.
>
> If $E=L^H$, then
>
> $$
> [L:E]=|H|,
> \qquad
> [E:K]=[G:H].
> $$
>
> Moreover,
>
> $$
> E/K\text{ is Galois}
> \quad\Longleftrightarrow\quad
> H\trianglelefteq G.
> $$
>
> When these equivalent conditions hold, restriction of automorphisms induces
>
> $$
> \operatorname{Gal}(E/K)\cong G/H.
> $$

This formulation agrees with the [Stacks Project statement of the fundamental theorem](https://stacks.math.columbia.edu/tag/09DW). We will prove it from the ground up.

## 7. Proof core I: independence of homomorphisms

The first lemma says that distinct field homomorphisms behave like linearly independent vectors, even though they are functions.

> **Dedekind independence lemma.**  
> Let $L$ and $\Omega$ be fields, and let
>
> $$
> \sigma_1,\ldots,\sigma_n:L\to\Omega
> $$
>
> be distinct field homomorphisms. If $a_1,\ldots,a_n\in\Omega$ satisfy
>
> $$
> a_1\sigma_1(x)+\cdots+a_n\sigma_n(x)=0
> $$
>
> for every $x\in L$, then
>
> $$
> a_1=\cdots=a_n=0.
> $$

In other words, the functions $\sigma_i$ are linearly independent over $\Omega$.

### Proof

Assume the conclusion is false. Among all nontrivial relations, choose one with the smallest possible number of nonzero coefficients. After discarding zero terms and renumbering, write it as

$$
a_1\sigma_1(x)+\cdots+a_r\sigma_r(x)=0
\qquad\text{for all }x\in L,
$$

where every $a_i$ is nonzero and $r$ is minimal.

There cannot be only one term, because a field homomorphism sends $1$ to $1$, so

$$
a_1\sigma_1(1)=a_1\neq0.
$$

Thus $r\geq2$. Since $\sigma_1$ and $\sigma_r$ are distinct, there exists $y\in L$ such that

$$
\sigma_1(y)\neq\sigma_r(y).
$$

Apply the relation to $xy$:

$$
a_1\sigma_1(x)\sigma_1(y)
+\cdots+
a_r\sigma_r(x)\sigma_r(y)=0.
$$

Multiply the original relation by $\sigma_r(y)$:

$$
a_1\sigma_1(x)\sigma_r(y)
+\cdots+
a_r\sigma_r(x)\sigma_r(y)=0.
$$

Subtracting eliminates the last term:

$$
\sum_{i=1}^{r-1}
a_i\bigl(\sigma_i(y)-\sigma_r(y)\bigr)\sigma_i(x)=0
\qquad\text{for all }x\in L.
$$

The coefficient of $\sigma_1$ is nonzero because both factors are nonzero. We have produced a nontrivial relation with fewer than $r$ terms, contradicting minimality. Therefore no nontrivial relation exists. $\square$

### Why this lemma is the right tool

Suppose $L/F$ is finite of degree $d$. The set of $F$-linear maps $L\to L$ is a vector space over $L$: multiply a map pointwise by an element of $L$. Once an $F$-basis of $L$ is fixed, a linear map is determined by its values on the $d$ basis elements. Therefore

$$
\dim_L\operatorname{Hom}_F(L,L)=d.
$$

Distinct $F$-automorphisms are linearly independent by Dedekind's lemma. Consequently,

$$
|\operatorname{Aut}(L/F)|\leq[L:F].
$$

This recovers the automorphism bound without assuming that the extension is simple.

## 8. Proof core II: Artin's fixed-field theorem

The central engine is the following result.

> **Artin's fixed-field theorem.**  
> Let $H$ be a finite group of automorphisms of a field $L$, and let
>
> $$
> F=L^H.
> $$
>
> Then
>
> $$
> [L:F]=|H|.
> $$
>
> In particular, $L/F$ is a finite Galois extension and
>
> $$
> \operatorname{Gal}(L/F)=H.
> $$

The striking point is that finiteness of $L/F$ is a conclusion, not a hypothesis.

Write

$$
H=\{\sigma_1,\ldots,\sigma_n\},
\qquad n=|H|.
$$

We prove the two inequalities

$$
[L:F]\leq n
\qquad\text{and}\qquad
n\leq[L:F].
$$

### First inequality: no more than $n$ independent elements

Take any $m>n$ elements

$$
x_1,\ldots,x_m\in L.
$$

Form the $n\times m$ matrix

$$
A=(\sigma_i(x_j)).
$$

Because there are more columns than rows, the homogeneous system

$$
A
\begin{pmatrix}
c_1\\ \vdots\\ c_m
\end{pmatrix}
=0
$$

has a nonzero solution with coefficients $c_j\in L$. Among all nonzero solutions, choose one with the smallest possible number of nonzero coordinates. Relabel the $x_j$ if necessary and rescale the solution so that

$$
c_1=1.
$$

Thus, for every $\sigma\in H$,

$$
\sum_{j=1}^m c_j\sigma(x_j)=0.
$$

Let $\tau\in H$. Apply $\tau$ to the equation:

$$
\sum_{j=1}^m \tau(c_j)(\tau\sigma)(x_j)=0.
$$

As $\sigma$ runs through $H$, so does $\tau\sigma$. Therefore the vector

$$
\bigl(\tau(c_1),\ldots,\tau(c_m)\bigr)
$$

is another solution of the same matrix equation. Its first coordinate is

$$
\tau(c_1)=\tau(1)=1.
$$

Subtract the original solution. The difference is again a solution, but its first coordinate is zero. All its nonzero coordinates lie among the nonzero coordinates of the original minimal solution. If the difference were nonzero, it would have strictly smaller support, contradicting minimality. Hence

$$
\tau(c_j)=c_j
$$

for every $j$ and every $\tau\in H$. Thus every coefficient $c_j$ belongs to $F=L^H$.

We have proved that any $m>n$ elements of $L$ are linearly dependent over $F$. Therefore

$$
[L:F]\leq n.
$$

In particular, $L/F$ is finite.

### Second inequality: the automorphisms are independent

Every member of $H$ fixes $F$, so the elements of $H$ are distinct $F$-linear maps $L\to L$. Dedekind's lemma makes them linearly independent over $L$. But

$$
\dim_L\operatorname{Hom}_F(L,L)=[L:F].
$$

Therefore

$$
n\leq[L:F].
$$

Combining both inequalities gives

$$
\boxed{[L:L^H]=|H|.}
$$

### Why the extension is Galois

For any $\alpha\in L$, consider the orbit polynomial

$$
p_\alpha(T)
=
\prod_{\beta\in H\cdot\alpha}(T-\beta),
$$

where $H\cdot\alpha=\{\sigma(\alpha):\sigma\in H\}$ is written without repetitions. Every $\tau\in H$ permutes the orbit, so it fixes every coefficient of $p_\alpha$. Hence

$$
p_\alpha(T)\in F[T].
$$

The roots are distinct by construction, and $\alpha$ is one of them. The minimal polynomial of $\alpha$ over $F$ divides $p_\alpha$, so it splits in $L$ and has no repeated root. Thus $L/F$ is normal and separable, hence Galois.

We already know that $H\subseteq\operatorname{Gal}(L/F)$. The general automorphism bound and the degree equality give

$$
|\operatorname{Gal}(L/F)|
\leq[L:F]
=|H|.
$$

Therefore

$$
\operatorname{Gal}(L/F)=H.
$$

This completes the proof of Artin's theorem. $\square$

## 9. Proof core III: the correspondence

Let $L/K$ be finite Galois and let

$$
G=\operatorname{Gal}(L/K).
$$

We use two facts:

1. If $K\subseteq E\subseteq L$, then $L/E$ is finite Galois.
2. If $M/N$ is finite Galois, then
   $|\operatorname{Gal}(M/N)|=[M:N]$.

For the first fact, write $L$ as the splitting field over $K$ of a separable polynomial $f\in K[X]$. The same $f$ lies in $E[X]$, and $L$ is still generated over $E$ by all of its roots. Thus $L/E$ is again a splitting field of a separable polynomial.

The second fact follows from the usual embedding count: separability supplies $[M:N]$ distinct $N$-embeddings into an algebraic closure, while normality ensures that every image lies back in $M$, making each embedding an automorphism.

### A field returns to itself

Take an intermediate field $E$ and set

$$
H=\operatorname{Gal}(L/E).
$$

We already have

$$
E\subseteq L^H.
$$

Because $L/E$ is finite Galois,

$$
|H|=[L:E].
$$

Artin's theorem gives

$$
[L:L^H]=|H|.
$$

Therefore

$$
[L:L^H]=[L:E].
$$

Apply the tower formula to

$$
E\subseteq L^H\subseteq L:
$$

$$
[L:E]=[L:L^H][L^H:E].
$$

Equality of the first two factors forces

$$
[L^H:E]=1,
$$

so

$$
\boxed{L^{\operatorname{Gal}(L/E)}=E.}
$$

### A subgroup returns to itself

Take $H\leq G$ and set

$$
E=L^H.
$$

We already have

$$
H\subseteq\operatorname{Gal}(L/E).
$$

Artin's theorem says directly that

$$
[L:E]=|H|
$$

and that the full automorphism group of $L/E$ is $H$. Therefore

$$
\boxed{\operatorname{Gal}(L/L^H)=H.}
$$

The two constructions are inverse. Since both reverse inclusions, they give an inclusion-reversing bijection.

### Degree and index

If $E=L^H$, Artin's theorem already gives

$$
[L:E]=|H|.
$$

The tower formula gives

$$
[L:K]=[L:E][E:K].
$$

Because $L/K$ is Galois,

$$
[L:K]=|G|.
$$

Therefore

$$
|G|=|H|[E:K],
$$

and hence

$$
\boxed{[E:K]=\frac{|G|}{|H|}=[G:H].}
$$

This proves the bijection and both numerical formulas.

## 10. Proof core IV: normal subgroups and quotient groups

It remains to determine when the intermediate extension $E/K$ is itself Galois.

Let $E=L^H$. For $g\in G$,

$$
g(E)=g(L^H)=L^{gHg^{-1}}.
$$

To verify this formula, take $x\in L^H$. For $h\in H$,

$$
(ghg^{-1})(g(x))=g(h(x))=g(x),
$$

so $g(x)$ is fixed by $gHg^{-1}$. Applying the same argument to $g^{-1}$ gives equality.

By the correspondence,

$$
g(E)=E
\quad\Longleftrightarrow\quad
gHg^{-1}=H.
$$

Thus $E$ is stable under every element of $G$ precisely when $H$ is normal in $G$.

### From normal subgroup to Galois subextension

Assume $H\trianglelefteq G$. Then every $g\in G$ preserves $E$, so restriction defines a homomorphism

$$
\rho:G\longrightarrow\operatorname{Aut}(E/K),
\qquad
g\longmapsto g|_E.
$$

Its kernel consists of the automorphisms fixing $E$ pointwise:

$$
\ker\rho=\operatorname{Gal}(L/E)=H.
$$

The first isomorphism theorem gives

$$
\operatorname{im}\rho\cong G/H.
$$

Now

$$
|\operatorname{im}\rho|
=
|G/H|
=
[G:H]
=
[E:K].
$$

But a finite extension has at most its degree many automorphisms. We have already found $[E:K]$ of them, so

$$
|\operatorname{Aut}(E/K)|=[E:K].
$$

Hence $E/K$ is Galois and

$$
\boxed{\operatorname{Gal}(E/K)\cong G/H.}
$$

### From Galois subextension to normal subgroup

Conversely, assume $E/K$ is Galois. Because it is normal, every $K$-embedding of $E$ into an algebraic closure maps $E$ onto itself. In particular, for every $g\in G$,

$$
g(E)=E.
$$

The conjugation formula then gives

$$
L^{gHg^{-1}}
=g(L^H)
=g(E)
=E
=L^H.
$$

The subgroup-to-field map is injective, so

$$
gHg^{-1}=H
$$

for every $g\in G$. Thus $H\trianglelefteq G$.

The normal-subgroup and quotient portions of the theorem are proved. $\square$

## 11. Re-reading the biquadratic example

Return to

$$
L=\mathbb Q(\sqrt2,\sqrt3),
\qquad
G\cong V_4.
$$

The subgroup lattice of $V_4$ has five elements:

$$
\{1\},\quad
\langle\sigma\rangle,\quad
\langle\tau\rangle,\quad
\langle\sigma\tau\rangle,\quad
G.
$$

The theorem says there can be no other intermediate fields. Our direct coefficient calculations found one field for every subgroup, and the theorem proves completeness.

Each order-$2$ subgroup has index $2$. Its fixed field therefore has degree $2$ over $\mathbb Q$:

$$
[L^{\langle\sigma\rangle}:\mathbb Q]
=[G:\langle\sigma\rangle]
=2,
$$

and similarly for the other two.

Every subgroup of an abelian group is normal. Hence each intermediate field is Galois over $\mathbb Q$. For example,

$$
\operatorname{Gal}(\mathbb Q(\sqrt3)/\mathbb Q)
\cong
G/\langle\sigma\rangle
\cong C_2.
$$

There is a useful generalization. If $a,b\in K^\times$ represent distinct nontrivial square classes—meaning that none of $a,b,ab$ is a square in $K$—then

$$
K(\sqrt a,\sqrt b)/K
$$

is a $V_4$-extension, and its three quadratic intermediate fields are

$$
K(\sqrt a),\qquad
K(\sqrt b),\qquad
K(\sqrt{ab}).
$$

The third field is not an accident of $2$ and $3$. It is forced by the third order-$2$ subgroup.

## 12. A nonabelian checkpoint: the splitting field of $X^3-2$

Before approaching $A_4$, it helps to see what changes when the Galois group is nonabelian.

Let

$$
L=\mathbb Q(\alpha,\omega),
\qquad
\alpha=\sqrt[3]{2},
\qquad
\omega=e^{2\pi i/3}.
$$

This is the splitting field of $X^3-2$. Its three roots are

$$
\alpha,\qquad\omega\alpha,\qquad\omega^2\alpha.
$$

The polynomial is irreducible over $\mathbb Q$ by Eisenstein's criterion at $2$, so

$$
[\mathbb Q(\alpha):\mathbb Q]=3.
$$

The field $\mathbb Q(\alpha)$ is real and does not contain $\omega$, whose minimal polynomial is

$$
X^2+X+1.
$$

Therefore

$$
[L:\mathbb Q]=6.
$$

The automorphisms permute the three roots faithfully, and two automorphisms generate the group:

$$
r(\alpha)=\omega\alpha,\qquad r(\omega)=\omega,
$$

$$
s(\alpha)=\alpha,\qquad s(\omega)=\omega^2.
$$

They satisfy

$$
r^3=s^2=1,
\qquad
srs=r^{-1},
$$

so

$$
\operatorname{Gal}(L/\mathbb Q)\cong S_3.
$$

The subgroup $\langle r\rangle\cong C_3$ is normal and has index $2$. Its fixed field is

$$
L^{\langle r\rangle}=\mathbb Q(\omega),
$$

a quadratic Galois extension of $\mathbb Q$. The three subgroups generated by transpositions have order $2$ and index $3$. Their fixed fields are three cubic fields. One is

$$
L^{\langle s\rangle}=\mathbb Q(\alpha).
$$

Because a transposition subgroup is not normal in $S_3$, $\mathbb Q(\alpha)/\mathbb Q$ is not Galois. This recovers exactly what we observed earlier: the other two roots of $X^3-2$ are missing.

This example separates two facts that coincide in the $V_4$ example:

- every subgroup still corresponds to an intermediate field;
- only normal subgroups correspond to intermediate fields that are Galois over the base.

## Lattice arithmetic: intersections and composita

The phrase “lattice correspondence” means more than drawing the same graph upside down. It also tells us how the two natural ways of combining fields translate into operations on subgroups.

Let $E_1,E_2$ be intermediate fields, with corresponding subgroups

$$
H_1=\operatorname{Gal}(L/E_1),
\qquad
H_2=\operatorname{Gal}(L/E_2).
$$

There are two fields to construct:

- the intersection $E_1\cap E_2$;
- the compositum $E_1E_2$, the smallest subfield of $L$ containing both $E_1$ and $E_2$.

There are likewise two subgroups:

- the intersection $H_1\cap H_2$;
- the generated subgroup $\langle H_1,H_2\rangle$, the smallest subgroup containing both.

Because the correspondence reverses inclusions, intersections and generated objects exchange roles.

### The compositum corresponds to subgroup intersection

An automorphism fixes $E_1E_2$ pointwise exactly when it fixes both $E_1$ and $E_2$ pointwise. Therefore

$$
\operatorname{Gal}(L/E_1E_2)
=
\operatorname{Gal}(L/E_1)
\cap
\operatorname{Gal}(L/E_2),
$$

or

$$
\boxed{
\operatorname{Gal}(L/E_1E_2)=H_1\cap H_2.
}
$$

Applying the fixed-field operation gives the equivalent formula

$$
\boxed{
L^{H_1\cap H_2}=E_1E_2.
}
$$

In the biquadratic example,

$$
\mathbb Q(\sqrt2)\mathbb Q(\sqrt3)
=
\mathbb Q(\sqrt2,\sqrt3)=L.
$$

The corresponding order-$2$ subgroups intersect trivially:

$$
\langle\tau\rangle\cap\langle\sigma\rangle=\{1\}.
$$

The fixed field of the trivial subgroup is indeed all of $L$.

### The field intersection corresponds to generated subgroup

An element lies in both $E_1=L^{H_1}$ and $E_2=L^{H_2}$ exactly when it is fixed by every member of $H_1$ and every member of $H_2$. That is equivalent to being fixed by every finite product of such elements, hence by the generated subgroup. Therefore

$$
\boxed{
E_1\cap E_2=L^{\langle H_1,H_2\rangle}.
}
$$

Equivalently,

$$
\boxed{
\operatorname{Gal}(L/E_1\cap E_2)
=
\langle H_1,H_2\rangle.
}
$$

For example,

$$
\mathbb Q(\sqrt2)\cap\mathbb Q(\sqrt3)=\mathbb Q.
$$

On the group side,

$$
\langle\langle\tau\rangle,\langle\sigma\rangle\rangle
=
G,
$$

and the full group fixes $\mathbb Q$.

### A degree consequence

When $H_1$ and $H_2$ are finite subgroups, group theory relates their sizes:

$$
|H_1H_2|
=
\frac{|H_1||H_2|}{|H_1\cap H_2|}.
$$

If at least one subgroup is normal, $H_1H_2$ is a subgroup and equals $\langle H_1,H_2\rangle$. Translating every order through Artin's formula gives field-degree identities. For instance, when one of $E_1/K$ or $E_2/K$ is Galois,

$$
[E_1E_2:K]\,[E_1\cap E_2:K]
=
[E_1:K]\,[E_2:K].
$$

Without a normality or linear-disjointness hypothesis, one should not use that product formula blindly. The lattice identities themselves remain valid; it is the simple cardinality formula for the generated subgroup that can fail.

These operations clarify why the theorem is an anti-isomorphism of lattices, not merely a bijection of sets.

## 13. Decoding an $A_4$-lattice

Now suppose $L/K$ is a finite Galois extension with

$$
\operatorname{Gal}(L/K)\cong A_4.
$$

The existence of such extensions is not needed for the lattice calculation; we are asking what the intermediate fields must look like once the Galois group is known.

The alternating group $A_4$ consists of the even permutations of four letters. It has $12$ elements:

- the identity;
- eight $3$-cycles;
- three double transpositions,

  $$
  (12)(34),\qquad(13)(24),\qquad(14)(23).
  $$

### Listing the subgroups

Each double transposition generates a distinct order-$2$ subgroup:

$$
H_1=\langle(12)(34)\rangle,
$$

$$
H_2=\langle(13)(24)\rangle,
$$

$$
H_3=\langle(14)(23)\rangle.
$$

Together with the identity, the double transpositions form

$$
V=
\{1,(12)(34),(13)(24),(14)(23)\}
\cong V_4.
$$

This is a subgroup because the product of any two distinct double transpositions is the third. It is normal because conjugation preserves cycle type: the three double transpositions are permuted among themselves.

Each subgroup of order $3$ contains two nonidentity $3$-cycles, a cycle and its inverse. Since $A_4$ has eight $3$-cycles, there are

$$
\frac82=4
$$

distinct order-$3$ subgroups. We may take

$$
C_1=\langle(123)\rangle,\quad
C_2=\langle(124)\rangle,\quad
C_3=\langle(134)\rangle,\quad
C_4=\langle(234)\rangle.
$$

There are no subgroups of order $6$. One quick proof is that an index-$2$ subgroup would be normal. If $N\leq A_4$ had order $6$, then the quotient $A_4/N$ would have order $2$, giving a nontrivial homomorphism

$$
A_4\to C_2.
$$

Every $3$-cycle would map to the identity because $C_2$ has no element of order $3$. But the $3$-cycles generate $A_4$, so the homomorphism would be trivial, a contradiction.

There are also no other order-$4$ subgroups. By Lagrange's theorem, a group of order $4$ is $C_4$ or $V_4$. The group $A_4$ has no element of order $4$, so an order-$4$ subgroup would have to contain all three elements of order $2$, hence would be exactly $V$.

Thus the complete list is:

| Subgroup type | Number | Order |
|---|---:|---:|
| $\lbrace 1\rbrace$ | $1$ | $1$ |
| $C_2$ | $3$ | $2$ |
| $C_3$ | $4$ | $3$ |
| $V_4$ | $1$ | $4$ |
| $A_4$ | $1$ | $12$ |

### Turning subgroup orders into field degrees

For each subgroup $H$,

$$
[L:L^H]=|H|
$$

and

$$
[L^H:K]=[A_4:H]=\frac{12}{|H|}.
$$

Therefore:

| Subgroup $H$ | Number of such fields | $[L:L^H]$ | $[L^H:K]$ |
|---|---:|---:|---:|
| $\lbrace 1\rbrace$ | $1$ | $1$ | $12$ |
| $C_2$ | $3$ | $2$ | $6$ |
| $C_3$ | $4$ | $3$ | $4$ |
| $V_4$ | $1$ | $4$ | $3$ |
| $A_4$ | $1$ | $12$ | $1$ |

The three order-$2$ subgroups lie inside $V$. Inclusion reverses, so

$$
H_i\subseteq V
\quad\Longrightarrow\quad
L^V\subseteq L^{H_i}.
$$

Thus the unique cubic field $L^V$ lies inside each of the three degree-$6$ fields $L^{H_i}$.

None of the order-$3$ subgroups is contained in $V$, and no $C_3$ contains a nontrivial proper subgroup. The four degree-$4$ fields $L^{C_i}$ therefore sit on separate branches directly between $K$ and $L$.

<figure class="post-figure" id="a4-lattice-diagram">
  <div class="post-figure-media post-figure-media-wide">
    <img src="{{ '/assets/images/galois-a4-correspondence.svg' | relative_url }}" alt="The subgroup lattice of A4 beside the reversed lattice of intermediate fields labelled by their degrees over K.">
  </div>
  <figcaption>An abstract $A_4$-extension. The three $C_2$ subgroups sit inside $V_4$, so the cubic fixed field of $V_4$ sits inside the three degree-$6$ fixed fields.</figcaption>
</figure>

### Which intermediate fields are Galois over $K$?

The normal subgroups of $A_4$ are

$$
\{1\},\qquad V,\qquad A_4.
$$

The four $C_3$ subgroups are conjugate to one another, so none is normal. The three $C_2$ subgroups are also conjugate to one another, so none is normal.

Therefore the only corresponding fields that are Galois over $K$ are

$$
L,\qquad L^V,\qquad K.
$$

For the nontrivial proper one,

$$
\operatorname{Gal}(L^V/K)
\cong
A_4/V
\cong C_3.
$$

This explains the special role of the unique cubic field in the diagram: it is not merely unique at its degree; it is the only proper nontrivial intermediate field that is Galois over the base.

### A useful warning about a tempting polynomial

The polynomial

$$
X^4+8X^2+12
$$

does **not** provide an $A_4$ example. It factors:

$$
X^4+8X^2+12
=(X^2+2)(X^2+6).
$$

Its roots are

$$
\pm i\sqrt2,\qquad\pm i\sqrt6,
$$

and its splitting field is

$$
\mathbb Q(i\sqrt2,i\sqrt6)
=
\mathbb Q(i\sqrt2,\sqrt3).
$$

That extension has degree $4$ and Galois group $V_4$, not $A_4$. A correct field lattice cannot be recovered from an incorrect Galois-group label. The $A_4$ discussion above is intentionally stated for an abstract extension whose group is known to be $A_4$.

## 14. How to use the theorem in practice

When faced with a concrete finite Galois extension, the following order of work is reliable.

### Step 1: identify the splitting field

Start with the polynomial or family of polynomials and determine the field containing all roots. Do not confuse $K(\alpha)$, generated by one root, with the full splitting field.

For $X^3-2$,

$$
\mathbb Q(\sqrt[3]{2})
$$

is not the splitting field, while

$$
\mathbb Q(\sqrt[3]{2},\omega)
$$

is.

### Step 2: compute the degree

Use minimal polynomials and the tower formula. The degree is both a check and a target:

$$
|\operatorname{Gal}(L/K)|=[L:K]
$$

when the extension is Galois.

If you have found only four automorphisms of a degree-$8$ Galois extension, your list is incomplete. If you claim eight distinct automorphisms of a degree-$4$ extension, some of them are not well-defined.

### Step 3: describe automorphisms on generators

Determine where each generator may go. Images must be roots of the same minimal polynomial and must preserve all relations.

Write automorphisms by their action on generators, not by a vague root-permutation slogan. In the biquadratic case, the sign table makes the group law transparent.

### Step 4: identify the abstract group

Use orders, relations, and the action on roots. The order alone rarely determines the group. At order $4$, $C_4$ and $V_4$ have different subgroup lattices and therefore predict different intermediate-field lattices.

### Step 5: draw the subgroup lattice first

Group theory is usually the easier side. List all subgroups, their orders, containments, and normality. Then reverse the diagram.

For every subgroup $H$, label the corresponding field by

$$
[L:L^H]=|H|
$$

and

$$
[L^H:K]=[G:H].
$$

These two numbers catch many inverted labels.

### Step 6: find explicit generators for fixed fields

The theorem guarantees that the fields exist and gives their degrees, but it does not automatically hand you convenient generators.

To find $L^H$, look for expressions invariant under $H$: sums, products, traces, and symmetric combinations of conjugates. Then use the predicted degree to prove that the candidate is the entire fixed field.

In the running example, $\sigma\tau$ changes the signs of both $\sqrt2$ and $\sqrt3$, so it fixes their product $\sqrt6$. The theorem predicts a quadratic fixed field; since $\mathbb Q(\sqrt6)$ is already quadratic, it must be the whole fixed field.

### Step 7: read normality on either side

If $H$ is normal, the field $L^H$ is Galois over $K$, and the quotient $G/H$ is its Galois group. If $H$ is not normal, its conjugates correspond to the conjugate intermediate fields.

This is one of the theorem's most useful efficiencies. It turns a potentially difficult field-normality calculation into a subgroup-normality calculation.

## Computing fixed fields: orbits, traces, and norms

The correspondence proves that $L^H$ exists and predicts its degree, but concrete problems usually ask for a generator. Three related constructions are especially useful.

### Orbit polynomials

For $\alpha\in L$, let

$$
H\cdot\alpha=\{\sigma(\alpha):\sigma\in H\}
$$

be its orbit. The polynomial

$$
p_{\alpha,H}(T)
=
\prod_{\beta\in H\cdot\alpha}(T-\beta)
$$

has coefficients in $L^H$, because every member of $H$ merely permutes its roots.

If the stabilizer

$$
H_\alpha=\{\sigma\in H:\sigma(\alpha)=\alpha\}
$$

is known, the orbit-stabilizer theorem gives

$$
|H\cdot\alpha|=[H:H_\alpha].
$$

This number is the degree one expects for $\alpha$ over $L^H$ when the orbit polynomial is its minimal polynomial.

For the full Galois group $G$, the coefficients of

$$
\prod_{\sigma\in G}(T-\sigma(\alpha))
$$

lie in $K$. Repeated roots appear if some automorphisms fix $\alpha$; removing repetitions gives the minimal polynomial when $\alpha$ generates the appropriate orbit.

### Relative trace

Define

$$
\operatorname{Tr}_{L/L^H}(\alpha)
=
\sum_{\sigma\in H}\sigma(\alpha).
$$

For $\tau\in H$,

$$
\tau\left(\sum_{\sigma\in H}\sigma(\alpha)\right)
=
\sum_{\sigma\in H}(\tau\sigma)(\alpha).
$$

Left multiplication by $\tau$ permutes $H$, so the sum is unchanged. Therefore

$$
\operatorname{Tr}_{L/L^H}(\alpha)\in L^H.
$$

The trace is additive and $L^H$-linear. It is often an efficient way to manufacture invariant linear combinations.

In the biquadratic example, take $H=\langle\sigma\rangle$. Then

$$
\operatorname{Tr}_{L/L^H}(\sqrt2+\sqrt3)
=
(\sqrt2+\sqrt3)+(-\sqrt2+\sqrt3)
=
2\sqrt3.
$$

This immediately reveals $\sqrt3$ as an element of the fixed field.

### Relative norm

Define

$$
\operatorname{N}_{L/L^H}(\alpha)
=
\prod_{\sigma\in H}\sigma(\alpha).
$$

The same permutation argument shows that

$$
\operatorname{N}_{L/L^H}(\alpha)\in L^H.
$$

The norm is multiplicative rather than additive.

With the same subgroup and element,

$$
\operatorname{N}_{L/L^H}(\sqrt2+\sqrt3)
=
(\sqrt2+\sqrt3)(-\sqrt2+\sqrt3)
=1.
$$

That particular norm is uninformative, which is a useful reminder: invariants are candidates, not guaranteed generators.

For $H=\langle\sigma\tau\rangle$,

$$
\operatorname{Tr}_{L/L^H}(\sqrt2+\sqrt3)=0,
$$

but

$$
\operatorname{N}_{L/L^H}(\sqrt2+\sqrt3)
=
(\sqrt2+\sqrt3)(-\sqrt2-\sqrt3)
=
-5-2\sqrt6.
$$

This element generates $\mathbb Q(\sqrt6)$.

### Proving that a candidate is the whole field

Suppose an invariant $\theta$ has been found. The inclusion

$$
K(\theta)\subseteq L^H
$$

is immediate. To prove equality, compare degrees.

If the theorem predicts

$$
[L^H:K]=d
$$

and the minimal polynomial of $\theta$ over $K$ has degree $d$, then

$$
[K(\theta):K]=[L^H:K].
$$

An inclusion between two finite extensions of the same degree is equality:

$$
K(\theta)=L^H.
$$

This two-step method—construct an invariant, then certify it by degree—is usually cleaner than solving the fixed-point equations for a completely general element.

## Stabilizers recover minimal polynomials

There is a particularly clean meeting point between the elementary theory of minimal polynomials and the group action.

Let $L/K$ be finite Galois, let $G=\operatorname{Gal}(L/K)$, and choose $\alpha\in L$. The stabilizer of $\alpha$ is

$$
G_\alpha
=
\{\sigma\in G:\sigma(\alpha)=\alpha\}.
$$

Fixing $\alpha$ is equivalent to fixing every rational expression in $\alpha$ with coefficients in $K$. Therefore

$$
G_\alpha
=
\operatorname{Gal}(L/K(\alpha)).
$$

The fundamental theorem now gives

$$
[K(\alpha):K]
=
[G:G_\alpha].
$$

The orbit-stabilizer theorem gives the same index as the size of the orbit:

$$
|G\cdot\alpha|
=
[G:G_\alpha].
$$

Consequently,

$$
\boxed{
[K(\alpha):K]=|G\cdot\alpha|.
}
$$

But the left side is the degree of the minimal polynomial $m_{\alpha,K}$. The orbit elements are all roots of that polynomial, and separability says they are distinct. Since their number already equals the degree, they are exactly all of its roots:

$$
\boxed{
m_{\alpha,K}(T)
=
\prod_{\beta\in G\cdot\alpha}(T-\beta).
}
$$

This formula is often introduced before the correspondence as an observation about conjugates. The theorem reveals its group-theoretic content: the degree of an element is the index of its stabilizer.

### Example: $\sqrt2+\sqrt3$

Take

$$
\alpha=\sqrt2+\sqrt3
$$

in the biquadratic field. Its four images are

$$
\sqrt2+\sqrt3,\quad
-\sqrt2+\sqrt3,\quad
\sqrt2-\sqrt3,\quad
-\sqrt2-\sqrt3.
$$

They are distinct, so the stabilizer is trivial. Hence

$$
[\mathbb Q(\alpha):\mathbb Q]=[G:\{1\}]=4.
$$

Since $L$ also has degree $4$, this proves

$$
\mathbb Q(\sqrt2+\sqrt3)=\mathbb Q(\sqrt2,\sqrt3).
$$

Multiplying the four linear factors gives the minimal polynomial without guessing:

$$
\begin{aligned}
m_{\alpha,\mathbb Q}(T)
&=
\bigl(T-(\sqrt2+\sqrt3)\bigr)
\bigl(T-(-\sqrt2-\sqrt3)\bigr)\\
&\quad\cdot
\bigl(T-(-\sqrt2+\sqrt3)\bigr)
\bigl(T-(\sqrt2-\sqrt3)\bigr)\\
&=
\bigl(T^2-(5+2\sqrt6)\bigr)
\bigl(T^2-(5-2\sqrt6)\bigr)\\
&=
T^4-10T^2+1.
\end{aligned}
$$

The apparent irrationalities cancel because the coefficients are fixed by all of $G$ and therefore lie in $\mathbb Q$.

### Example: one cube root inside the $S_3$-extension

In the splitting field of $X^3-2$, the element

$$
\alpha=\sqrt[3]{2}
$$

is fixed by the order-$2$ subgroup generated by complex conjugation. Its orbit has size

$$
[S_3:C_2]=3,
$$

and consists of

$$
\alpha,\qquad\omega\alpha,\qquad\omega^2\alpha.
$$

The orbit polynomial is

$$
(T-\alpha)(T-\omega\alpha)(T-\omega^2\alpha)
=T^3-2.
$$

The field $K(\alpha)$ has degree $3$, but its stabilizer is not normal. This expresses in one calculation both the minimal-polynomial degree and the failure of $K(\alpha)/K$ to be Galois.

### When does one element generate the whole extension?

The same reasoning gives a useful test:

$$
K(\alpha)=L
\quad\Longleftrightarrow\quad
G_\alpha=\{1\}.
$$

An element generates the Galois extension precisely when no nonidentity automorphism fixes it. The primitive element theorem guarantees that a finite separable extension has such an element, but the stabilizer criterion tells us how to recognize one inside a given Galois extension.

This is also why a “generic” linear combination of field generators tends to work: each nonidentity automorphism imposes one proper linear condition for being fixed, and only finitely many automorphisms must be avoided.

## 15. Common mistakes

### Mistake 1: treating an automorphism as an arbitrary bijection

A field automorphism preserves

$$
\sigma(x+y)=\sigma(x)+\sigma(y),
\qquad
\sigma(xy)=\sigma(x)\sigma(y),
\qquad
\sigma(1)=1.
$$

An arbitrary invertible linear transformation is almost never a field automorphism.

### Mistake 2: forgetting which field is fixed

The notation

$$
\operatorname{Gal}(L/K)
$$

means automorphisms of $L$ that fix $K$ **pointwise**. It does not mean automorphisms that merely send $K$ to itself as a set.

### Mistake 3: reversing the degree formulas

For $E=L^H$,

$$
[L:E]=|H|
$$

while

$$
[E:K]=[G:H].
$$

The order measures the distance from the fixed field up to $L$; the index measures the distance from $K$ up to the fixed field.

### Mistake 4: assuming every intermediate extension is Galois

The top extension $L/K$ is Galois, and $L/E$ is Galois for every intermediate $E$. But $E/K$ need not be Galois. It is Galois exactly when the corresponding subgroup is normal.

The splitting field of $X^3-2$ displays all three possibilities:

$$
L/\mathbb Q\text{ is Galois},
$$

$$
L/\mathbb Q(\sqrt[3]{2})\text{ is Galois},
$$

but

$$
\mathbb Q(\sqrt[3]{2})/\mathbb Q\text{ is not Galois}.
$$

### Mistake 5: applying the finite theorem unchanged to infinite extensions

Infinite Galois theory introduces a topology on the Galois group. The corresponding subgroups must be closed. The [Stacks Project's infinite theorem](https://stacks.math.columbia.edu/tag/0BML) states this explicitly.

### Mistake 6: drawing a field lattice from subgroup orders alone

Orders determine degrees, but containments determine edges. In $A_4$, the $C_2$ subgroups lie inside $V_4$, while the $C_3$ subgroups do not. That difference is exactly why the degree-$6$ branches pass through the cubic field and the degree-$4$ branches do not.

## 16. What the theorem is really saying

The theorem does more than match two finite lists. It says that the internal structure of a finite Galois extension is completely encoded by the subgroup structure of its automorphism group.

The field side and the group side use opposite notions of size:

$$
\text{larger field}
\quad\longleftrightarrow\quad
\text{smaller fixing group}.
$$

The reason is logical before it is algebraic. A larger field contains more elements that an automorphism is required to fix, so fewer automorphisms survive. A larger subgroup contains more tests of invariance, so fewer field elements survive.

Artin's theorem turns that qualitative reversal into an exact numerical identity:

$$
[L:L^H]=|H|.
$$

Once this equality is known, the rest of the correspondence becomes almost forced. The easy inclusions cannot be strict because a strict inclusion would change a degree. Normality then appears through conjugation:

$$
g(L^H)=L^{gHg^{-1}}.
$$

An intermediate field is stable under every symmetry of $L/K$ exactly when its subgroup is stable under conjugation.

For the biquadratic field, the entire theory can be seen by changing signs. For an $A_4$-extension, the same mechanism organizes nine proper nontrivial subgroups and eight proper nontrivial intermediate fields into a single reversed diagram. The abstraction has not replaced the calculation; it has explained why the calculation has the shape it does.

## What has deliberately been left for later

Galois theory is famous for its application to solving polynomial equations by radicals, but that application requires another substantial bridge: solvable groups, towers of radical extensions, roots of unity, and the theorem connecting them. None of those ideas is needed to understand the correspondence itself. Introducing them here would replace one direct argument with two partially developed theories.

The same is true of ruler-and-compass constructions, finite fields, cyclotomic extensions, and explicit algorithms for computing the Galois group of a general polynomial. Each is a natural next subject, but each asks a different central question. This article has kept one promise: given a finite Galois extension and its automorphism group, explain exactly why subgroups classify all intermediate fields.

Infinite Galois theory has also appeared only as a warning. Its closed-subgroup condition is not a technical footnote that can be proved by repeating the finite argument with larger cardinalities. It depends on the profinite topology of the Galois group and on recovering infinite extensions from their finite Galois subextensions.

Finally, the abstract $A_4$ section decodes a lattice from a known group; it does not present an algorithm for proving that a particular quartic polynomial has Galois group $A_4$. Such a proof normally combines irreducibility, the discriminant, resolvent polynomials, and information about how primes factor. Keeping those questions separate prevents a common pedagogical confusion: computing a Galois group and using a known Galois group are different tasks.

With this boundary in place, every theorem used in the central correspondence has been stated and proved, while the examples remain calculations the reader can reproduce directly.

## A compact checklist

At the end of the route, the essential facts are these:

1. A finite extension has at most its degree many automorphisms.
2. A finite Galois extension has exactly its degree many automorphisms.
3. A subgroup $H$ fixes a field $L^H$.
4. Artin's theorem gives $[L:L^H]=|H|$.
5. Intermediate fields and subgroups are therefore mutually recoverable.
6. The correspondence reverses inclusion.
7. Subgroup order becomes upper field degree; subgroup index becomes lower field degree.
8. Normal subgroups correspond to intermediate fields Galois over the base.
9. The quotient group is the Galois group of that subextension.
10. In an infinite Galois extension, “subgroup” must be replaced by “closed subgroup.”

That is enough to reconstruct both the $V_4$ diamond and the $A_4$ lattice—and, more importantly, to know why the reconstruction is complete.

## Comprehension checks with solutions

These short problems test the correspondence itself rather than unrelated polynomial techniques.

### 1. A quadratic extension

Let $L=\mathbb Q(\sqrt5)$. Find $\operatorname{Gal}(L/\mathbb Q)$ and list all intermediate fields.

**Solution.** Any automorphism sends $\sqrt5$ to another root of $X^2-5$, so there are at most two:

$$
1(\sqrt5)=\sqrt5,
\qquad
\sigma(\sqrt5)=-\sqrt5.
$$

Both exist, so

$$
\operatorname{Gal}(L/\mathbb Q)\cong C_2.
$$

The only subgroups of $C_2$ are $\{1\}$ and $C_2$. Their fixed fields are $L$ and $\mathbb Q$. There is no proper nontrivial intermediate field. The same conclusion follows from the tower formula: an intermediate degree would have to divide the prime number $2$.

### 2. Identifying a fixed field by one invariant

In $L=\mathbb Q(\sqrt2,\sqrt3)$, let

$$
H=\langle\sigma\tau\rangle.
$$

Show without solving four coefficient equations that

$$
L^H=\mathbb Q(\sqrt6).
$$

**Solution.** The product $\sqrt6=\sqrt2\sqrt3$ is fixed because $\sigma\tau$ changes both signs. Hence

$$
\mathbb Q(\sqrt6)\subseteq L^H.
$$

The subgroup $H$ has order $2$, so

$$
[L^H:\mathbb Q]=[G:H]=2.
$$

The field $\mathbb Q(\sqrt6)$ also has degree $2$ over $\mathbb Q$. The inclusion between fields of equal finite degree is equality.

### 3. A subgroup of prime index

Let $L/K$ be finite Galois, and suppose $H\leq G$ has index $p$, where $p$ is prime. Can $L^H$ contain a field strictly between $K$ and $L^H$?

**Solution.** We have

$$
[L^H:K]=[G:H]=p.
$$

If

$$
K\subsetneq E\subsetneq L^H,
$$

the tower formula would write the prime $p$ as

$$
p=[L^H:E][E:K]
$$

with both factors larger than $1$, impossible. Thus there is no such $E$.

Notice that $L^H/K$ need not be Galois. Prime degree rules out internal fields; normality is a separate question.

### 4. Conjugate subgroups and conjugate fields

Let $H\leq G$ and $g\in G$. What field corresponds to $gHg^{-1}$?

**Solution.** The conjugation formula proved above gives

$$
L^{gHg^{-1}}=g(L^H).
$$

Thus conjugate subgroups correspond to fields carried into one another by automorphisms of $L/K$. A subgroup is normal exactly when every conjugate field is the same field.

In the $S_3$ splitting field of $X^3-2$, the three order-$2$ subgroups are conjugate. Their three cubic fixed fields are therefore conjugate copies, generated by the three roots

$$
\alpha,\qquad\omega\alpha,\qquad\omega^2\alpha.
$$

### 5. Intersections in the biquadratic field

Compute

$$
\mathbb Q(\sqrt2)\cap\mathbb Q(\sqrt6)
$$

inside $L=\mathbb Q(\sqrt2,\sqrt3)$.

**Solution.** The fields correspond respectively to

$$
\langle\tau\rangle
\quad\text{and}\quad
\langle\sigma\tau\rangle.
$$

These two subgroups generate all of $V_4$, because their product contains $\sigma$. Therefore

$$
\mathbb Q(\sqrt2)\cap\mathbb Q(\sqrt6)
=
L^{\langle\langle\tau\rangle,\langle\sigma\tau\rangle\rangle}
=
L^G
=
\mathbb Q.
$$

### 6. The cubic field in an $A_4$-extension

Suppose $\operatorname{Gal}(L/K)\cong A_4$, and let $V\cong V_4$ be its normal Klein four-subgroup. Determine the degree and Galois group of $L^V/K$.

**Solution.** Since $|A_4|=12$ and $|V|=4$,

$$
[L^V:K]=[A_4:V]=3.
$$

Because $V$ is normal, the extension is Galois and

$$
\operatorname{Gal}(L^V/K)
\cong
A_4/V.
$$

The quotient has order $3$, so it is cyclic:

$$
\operatorname{Gal}(L^V/K)\cong C_3.
$$

### 7. Why the degree-$4$ fields in the $A_4$ lattice are not Galois

Each degree-$4$ field is fixed by an order-$3$ subgroup $C_i$. Explain why it is not Galois over $K$.

**Solution.** The four order-$3$ subgroups are conjugate. A normal subgroup is equal to all of its conjugates, so no individual $C_i$ is normal. The normal-subgroup criterion gives

$$
L^{C_i}/K\text{ is not Galois}.
$$

Its normal closure inside $L$ is all of $L$, because the conjugates of $C_i$ have trivial intersection. Equivalently, the compositum of the four conjugate degree-$4$ fields is $L$.

### 8. Recovering a subgroup order from two degrees

Let $K\subseteq E\subseteq L$, where $L/K$ is finite Galois of degree $60$, and suppose $[E:K]=12$. What is the order of $\operatorname{Gal}(L/E)$?

**Solution.** The tower formula gives

$$
[L:E]=\frac{[L:K]}{[E:K]}=\frac{60}{12}=5.
$$

Since $L/E$ is Galois,

$$
|\operatorname{Gal}(L/E)|=[L:E]=5.
$$

On the group side this is the same calculation as

$$
|H|=\frac{|G|}{[G:H]}.
$$

## Further reading

- J. S. Milne, [*Fields and Galois Theory*, version 5.10](https://www.jmilne.org/math/CourseNotes/FT.pdf), especially Chapters 1–4. Milne's [course page](https://www.jmilne.org/math/CourseNotes/ft.html) also provides source files and exercises.
- The Stacks Project, [Section 9.21: Galois theory](https://stacks.math.columbia.edu/tag/09DU), including the [fundamental theorem](https://stacks.math.columbia.edu/tag/09DW) and its finite fixed-field lemma.
- Emil Artin, *Galois Theory*, for the automorphism-first route that motivates the proof used here.
- Ian Stewart, *Galois Theory*, for further worked examples and applications to polynomial equations.

</div>

</div>

</div>
