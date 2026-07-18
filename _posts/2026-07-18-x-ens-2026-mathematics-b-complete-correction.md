---
layout: post
title: "Ecole Polytechnique-ESPCI 2026 Mathematics B: Complete Correction"
subtitle: "From tridiagonal spectra to the semicircle law"
date: 2026-07-18 12:00:00 +0200
categories: [mathematics]
tags: [concours, linear-algebra, approximation, probability, random-matrices]
excerpt: "A detailed question-by-question correction of the X/ENS 2026 Mathematics B paper, including endpoint cases, multiplicities, constructive Weierstrass approximation and the final semicircle-law argument."
---

<div class="correction-post" markdown="1">

<p class="correction-deck">From tridiagonal spectra to the semicircle law</p>

This paper has an unusually coherent mathematical arc. It starts with a second-order recurrence, turns that recurrence into the characteristic polynomial of a tridiagonal matrix, reads off an exact cosine grid of eigenvalues, and then uses the same approximation ideas to reach a probabilistic spectral limit for Wigner matrices.

This post is the complete mathematical correction. It is written question by question and includes the details that matter in a concours solution: endpoint cases, algebraic multiplicities, normalizing factors, tail estimates, and the variance computation in the low-degree Wigner case. A separate companion post, [Formalizing an X/ENS Correction in Lean](/2026/07/18/formalizing-xens-correction-in-lean/), explains what changed when this correction was made to compile.

<div class="correction-downloads">
  <span>Complete files</span>
  <a href="/assets/files/X_ENS_2026_MP_MB_correction_V2_concours_grade.pdf">Typeset PDF</a>
  <a href="/assets/files/X_ENS_2026_MP_MB_correction_V2_concours_grade.tex">LaTeX source</a>
</div>

<div class="correction-route" role="img" aria-label="The proof route goes from a recurrence, to exact tridiagonal spectra, to constructive polynomial approximation, and finally to the semicircle law.">
  <div><span>01</span><strong>Recurrence</strong><small>closed forms</small></div>
  <div><span>02</span><strong>Spectra</strong><small>cosine grids</small></div>
  <div><span>03</span><strong>Approximation</strong><small>explicit polynomials</small></div>
  <div><span>04</span><strong>Semicircle law</strong><small>moments and tails</small></div>
</div>

<nav class="correction-toc" aria-label="Correction sections">
  <span>Jump to</span>
  <a href="#preliminary-question">Recurrence</a>
  <a href="#part-i">Arcsine law</a>
  <a href="#part-ii">Toeplitz spectra</a>
  <a href="#part-iii-constructive-weierstrass-approximation">Approximation</a>
  <a href="#part-iv">Random matrices</a>
</nav>

The paper uses two different limiting measures. They should not be confused.

<div class="law-comparison" markdown="1">
<div class="law-panel" markdown="1">
<p class="law-stage">Parts I-II</p>
<p class="law-name">Arcsine law</p>
$$
\frac{1}{\pi\sqrt{4-x^2}}\,\mathbf 1_{(-2,2)}(x)\,dx,
$$
</div>
<div class="law-panel" markdown="1">
<p class="law-stage">Part IV</p>
<p class="law-name">Semicircle law</p>
$$
\frac{1}{2\pi}\sqrt{4-x^2}\,\mathbf 1_{[-2,2]}(x)\,dx.
$$
</div>
</div>

## General conventions

All spectra below are counted with algebraic multiplicity, as in the
statement. For a real symmetric matrix $M\in M_n(\mathbb{R})$ and a
function $f$ defined on the spectrum,
$$S_f(M)=\frac1n\sum_{(\lambda,m_\lambda)\in\operatorname{Sp}(M)}m_\lambda f(\lambda).$$
In Part IV we write $S_n(f)=S_f(X_n)$. The function $f_k$ is always
$x\mapsto x^k$.

All limits are taken as $n\to\infty$ unless stated otherwise. Endpoint
cases are handled separately whenever an asymptotic equivalent would
otherwise hide a zero term.

## Preliminary question

### Question 1.

The recurrence
$$u_0=0,\qquad u_1=1,\qquad u_n=\alpha u_{n-1}-u_{n-2}\quad(n\ge2)$$
determines the sequence uniquely: if two sequences have the same first
two terms and satisfy the same recurrence, they are equal by induction
on $n$. Thus, in each case below, it is enough to exhibit a sequence
with the announced formula and to check its first two values and the
recurrence.

**Case $|\alpha|>2$.** Put $$r_+=\frac{\alpha+\sqrt{\alpha^2-4}}2,\qquad
  r_-=\frac{\alpha-\sqrt{\alpha^2-4}}2.$$ Since $|\alpha|>2$, we have
$\alpha^2-4>0$, so $r_+\ne r_-$ and $r_+-r_-=\sqrt{\alpha^2-4}$.
Moreover $r_+$ and $r_-$ are the two roots of $r^2-\alpha r+1=0$, hence
$$r_\pm^{\,n+2}=\alpha r_\pm^{\,n+1}-r_\pm^{\,n}\qquad(n\ge0).$$
Therefore the sequence $$v_n=\frac{r_+^n-r_-^n}{r_+-r_-}$$ satisfies the
same recurrence. Also $v_0=0$ and $v_1=1$. By uniqueness,
$$\boxed{u_n=\frac{r_+^n-r_-^n}{r_+-r_-}
  =\frac{r_+^n-r_-^n}{\sqrt{\alpha^2-4}}\qquad(n\ge0).}$$

**Case $|\alpha|<2$.** There is a unique $\theta\in(0,\pi)$ such that
$\alpha=2\cos\theta$. Here $\sin\theta>0$. Define
$$v_n=\frac{\sin(n\theta)}{\sin\theta}.$$ Then $v_0=0$ and $v_1=1$. The
addition formula gives, for every $n\ge0$, $$\sin((n+2)\theta)
  =2\cos\theta\,\sin((n+1)\theta)-\sin(n\theta).$$ Dividing by
$\sin\theta$ and using $\alpha=2\cos\theta$ shows that
$v_{n+2}=\alpha v_{n+1}-v_n$. Thus, by uniqueness, $$\boxed{
  \begin{gathered}
    u_n=\dfrac{\sin(n\theta)}{\sin\theta},\\
    \alpha=2\cos\theta,\qquad 0<\theta<\pi.
  \end{gathered}}$$

**Case $\alpha=2$.** Let $v_n=n$. Then $v_0=0$, $v_1=1$, and
$$2v_{n+1}-v_n=2(n+1)-n=n+2=v_{n+2}.$$ Hence $$\boxed{u_n=n.}$$

**Case $\alpha=-2$.** Let $v_n=(-1)^{n+1}n$. Again $v_0=0$ and $v_1=1$.
Moreover $$-2v_{n+1}-v_n
  =-2(-1)^{n+2}(n+1)-(-1)^{n+1}n
  =(-1)^{n+3}(n+2)=v_{n+2}.$$ Therefore $$\boxed{u_n=(-1)^{n+1}n.}$$

## Part I

The first step is analytic. We identify two discrete averages as Riemann
sums, then transport the uniform measure on an angle interval through
$x=2\cos\theta$. This produces the arcsine density.

### Question 2.

All estimates below are written for $n\ge1$; changing finitely many
initial terms has no effect on the limit. Let $f$ be continuous on
$[0,1]$. The two averages in the question are

$$
v_n=\frac1n\sum_{k=1}^n f\left(\frac{k}{n+1}\right),
\qquad
w_n=\frac1n\sum_{k=1}^n f\left(\frac{2k}{2n+1}\right).
$$

Since $[0,1]$ is compact, $f$ is uniformly continuous and
bounded. Set $$M=\sup_{[0,1]}|f|.$$ We shall use the following
elementary Riemann-sum estimate, with the omitted right endpoint treated
explicitly. Let $m\ge1$, let $h>0$ satisfy $mh\le1$, and define
$$R(m,h)=h\sum_{k=1}^m f(kh).$$ Then $$\begin{aligned}
\left|R(m,h)-\int_0^1 f(t)\,dt\right|
&\le
  \sum_{k=1}^m
  \int_{(k-1)h}^{kh}|f(kh)-f(t)|\,dt
  +\int_{mh}^1 |f(t)|\,dt .
\end{aligned}$$ For $t\in[(k-1)h,kh]$, both $t$ and $kh$ belong to
$[0,1]$ and their distance is at most $h$. If $$\omega(\delta)
  =
  \sup\{|f(x)-f(y)|:\ x,y\in[0,1],\ |x-y|\le\delta\},$$ then
$\omega(\delta)\to0$ as $\delta\to0$, and the previous bound gives
$$\left|R(m,h)-\int_0^1 f(t)\,dt\right|
  \le mh\,\omega(h)+M(1-mh).$$ The last term is exactly the contribution
of the short interval $[mh,1]$, whose length tends to $0$ in the
applications. Consequently, whenever $h_n\to0$ and $m_nh_n\to1$ with
$m_nh_n\le1$, one has $$h_n\sum_{k=1}^{m_n} f(kh_n)
  \longrightarrow
  \int_0^1 f(t)\,dt. \tag{2.1}$$

For the first sequence, take $$h_n=\frac1{n+1},\qquad m_n=n.$$ Then
$h_n\to0$, $m_nh_n=n/(n+1)\to1$, and (2.1) yields
$$\frac1{n+1}\sum_{k=1}^n f\left(\frac{k}{n+1}\right)
  \longrightarrow
  \int_0^1 f(t)\,dt.$$ Since $$v_n
  =
  \frac{n+1}{n}
  \left(
    \frac1{n+1}\sum_{k=1}^n f\left(\frac{k}{n+1}\right)
  \right)$$ and $(n+1)/n\to1$, we get
$$v_n\longrightarrow\int_0^1 f(t)\,dt.$$

For the second sequence, take $$h_n=\frac2{2n+1},\qquad m_n=n.$$ Again
$h_n\to0$, $m_nh_n=2n/(2n+1)\to1$, and (2.1) gives $$\frac2{2n+1}
  \sum_{k=1}^n
  f\left(\frac{2k}{2n+1}\right)
  \longrightarrow
  \int_0^1 f(t)\,dt.$$ But $$w_n
  =
  \frac{2n+1}{2n}
  \left(
    \frac2{2n+1}
    \sum_{k=1}^n
    f\left(\frac{2k}{2n+1}\right)
  \right),$$ and $(2n+1)/(2n)\to1$. Therefore
$$w_n\longrightarrow\int_0^1 f(t)\,dt.$$ Finally,
$$\boxed{\lim_{n\to\infty}v_n=\lim_{n\to\infty}w_n=\int_0^1 f(t)\,dt.}$$

### Question 3a.

Let $f$ be continuous on $[-2,2]$ and let $M=\sup_{[-2,2]}|f|$. The only
possible singularities of $$\frac{f(x)}{\sqrt{4-x^2}}$$ are at $x=-2$
and $x=2$. Near $2$, for $x\in[0,2)$, $$4-x^2=(2-x)(2+x)\ge 2(2-x),$$ so
$$\frac{|f(x)|}{\sqrt{4-x^2}}\le \frac{M}{\sqrt{2}\sqrt{2-x}},$$ and
$1/\sqrt{2-x}$ is integrable near $2$. The endpoint $-2$ is treated
similarly, using $$4-x^2=(2-x)(2+x)\ge 2(x+2)\qquad(x\in(-2,0]).$$ Thus
the improper integral
$$I(f)=\frac1\pi\int_{-2}^2\frac{f(x)}{\sqrt{4-x^2}}\,dx$$ is
convergent.

On $[-2+\varepsilon,2-\varepsilon]$ we may use the substitution
$x=2\cos\theta$. Then $$dx=-2\sin\theta\,d\theta,
  \qquad
  \sqrt{4-x^2}=2\sin\theta\quad(0<\theta<\pi).$$ Letting
$\varepsilon\downarrow0$, justified by the convergence just proved,
gives $$\boxed{I(f)=\frac1\pi\int_0^\pi f(2\cos\theta)\,d\theta.}$$

### Question 3b.

For $f_0(x)=1$, $$I(f_0)=\frac1\pi\int_0^\pi1\,d\theta=1.$$ For
$f_1(x)=x$, $$I(f_1)=\frac1\pi\int_0^\pi2\cos\theta\,d\theta=0.$$ For
$f_2(x)=x^2$, $$I(f_2)=\frac1\pi\int_0^\pi4\cos^2\theta\,d\theta
        =\frac4\pi\cdot\frac\pi2=2.$$ Hence
$$\boxed{I(f_0)=1,\qquad I(f_1)=0,\qquad I(f_2)=2.}$$

### Question 3c.

If $n$ is odd, the function $x^n/\sqrt{4-x^2}$ is odd on $[-2,2]$, so
$$\boxed{I(f_n)=0\qquad(n\text{ odd}).}$$ Let $n=2p$. Then
$$I(f_{2p})=\frac1\pi\int_0^\pi (2\cos\theta)^{2p}\,d\theta.$$ It
remains to compute $\int_0^\pi\cos^{2p}\theta\,d\theta$. Since
$\cos^{2p}$ has period $\pi$, $$\int_0^\pi \cos^{2p}\theta\,d\theta
  =\frac12\int_0^{2\pi}\cos^{2p}\theta\,d\theta.$$ Using
$$\cos\theta=\frac{e^{i\theta}+e^{-i\theta}}2,$$ we get
$$\cos^{2p}\theta
  =2^{-2p}\sum_{j=0}^{2p}\binom{2p}{j}e^{i(2p-2j)\theta}.$$ The integral
over $[0,2\pi]$ kills every nonconstant exponential term. The constant
term corresponds to $j=p$. Hence $$\int_0^{2\pi}\cos^{2p}\theta\,d\theta
  =2\pi\,2^{-2p}\binom{2p}{p},$$ and therefore
$$\int_0^\pi\cos^{2p}\theta\,d\theta
  =\pi\,2^{-2p}\binom{2p}{p}.$$ Consequently
$$I(f_{2p})=\frac{2^{2p}}\pi\cdot \pi\,2^{-2p}\binom{2p}{p}
  =\binom{2p}{p}.$$ Thus $$\boxed{
  I(f_n)=
  \begin{cases}
  0,& n\text{ odd},\\[1mm]
  \displaystyle \binom{2p}{p},& n=2p.
  \end{cases}}$$

### Question 4a.

Let $f$ be continuous on $[-2,2]$ and define
$$g(t)=f(2\cos(\pi t)),\qquad t\in[0,1].$$ Then $g$ is continuous on
$[0,1]$. Since $U_n$ is uniform on $\{1,\dots,n\}$, $$\begin{aligned}
 \mathbb{E}\left(f\left(2\cos\left(\frac{\pi U_n}{n+1}\right)\right)\right)
 &=\frac1n\sum_{k=1}^n f\left(2\cos\left(\frac{\pi k}{n+1}\right)\right)\\
 &=\frac1n\sum_{k=1}^n g\left(\frac{k}{n+1}\right).
\end{aligned}$$ By Question 2 this converges to $$\int_0^1 g(t)\,dt
  =\frac1\pi\int_0^\pi f(2\cos\theta)\,d\theta
  =\frac1\pi\int_{-2}^2\frac{f(x)}{\sqrt{4-x^2}}\,dx.$$ Therefore
$$\boxed{
  \mathbb{E}\left(f\left(2\cos\left(\frac{\pi U_n}{n+1}\right)\right)\right)
  \longrightarrow I(f).}$$

### Question 4b.

Fix $y\in[-2,2]$ and define
$$\theta_y=\arccos\left(\frac y2\right)\in[0,\pi].$$ The function $\cos$
is strictly decreasing on $[0,\pi]$. Thus, for $1\le k\le n$,
$$2\cos\left(\frac{\pi k}{n+1}\right)<y
  \iff
  \frac{\pi k}{n+1}>\theta_y.$$ If $y=-2$, then $\theta_y=\pi$ and the
inequality is impossible, so the probability is $0$ for every $n$. The
right-hand integral is also $0$. If $y=2$, then $\theta_y=0$ and the
inequality is true for every $k=1,\dots,n$, so the probability is $1$
for every $n$. The right-hand integral is also $1$.

Assume now $-2<y<2$. Put $a_n=(n+1)\theta_y/\pi$. The number of integers
$k\in\{1,\dots,n\}$ with $k>a_n$ is $n-\lfloor a_n\rfloor$. Hence
$$\mathbb{P}\left(2\cos\left(\frac{\pi U_n}{n+1}\right)<y\right)
  =\frac{n-\lfloor a_n\rfloor}{n}
  \longrightarrow 1-\frac{\theta_y}{\pi}.$$ Finally, with
$x=2\cos\theta$, $$\frac1\pi\int_{-2}^y\frac{dx}{\sqrt{4-x^2}}
  =\frac1\pi\int_{\theta_y}^{\pi}d\theta
  =1-\frac{\theta_y}{\pi}.$$ Therefore, for every $y\in[-2,2]$,
$$\boxed{
  \mathbb{P}\left(2\cos\left(\frac{\pi U_n}{n+1}\right)<y\right)
  \longrightarrow
  \frac1\pi\int_{-2}^y\frac{dx}{\sqrt{4-x^2}}.}$$

## Part II

Let $T_n$ be the adjacency matrix of the path with $n$ vertices: it has
zeros on the diagonal and ones immediately above and below it. More
generally, $T_n(a,b,c)$ denotes the tridiagonal Toeplitz matrix with
diagonal entry $a$, superdiagonal entry $b$, and subdiagonal entry $c$.
The recurrence from Question 1 now reappears as a determinant recurrence.

### Question 5a.

For $n=2$, $$T_2=\begin{pmatrix}0&1\\1&0\end{pmatrix},
  \qquad
  \chi_2(X)=\det\begin{pmatrix}X&-1\\-1&X\end{pmatrix}=X^2-1.$$ Thus
$$\boxed{\operatorname{Sp}(T_2)=\{-1,1\}.}$$ For $n=3$,
$$XI_3-T_3=\begin{pmatrix}
  X&-1&0\\
  -1&X&-1\\
  0&-1&X
  \end{pmatrix}.$$ Expanding the determinant gives
$$\chi_3(X)=X(X^2-1)-X=X^3-2X=X(X^2-2).$$ Hence
$$\boxed{\operatorname{Sp}(T_3)=\{-\sqrt2,0,\sqrt2\}.}$$

### Question 5b.

It is convenient to set $\chi_0(X)=1$ and $\chi_1(X)=X$. For $n\ge2$,
expand $$\chi_n(X)=\det(XI_n-T_n)$$ along the first row. The first
contribution is $X\chi_{n-1}(X)$. The only other nonzero entry in the
first row is $-1$ in column $2$; its cofactor has determinant
$-\chi_{n-2}(X)$. Therefore
$$\boxed{\chi_n(X)=X\chi_{n-1}(X)-\chi_{n-2}(X)\qquad(n\ge2).}$$ In
particular this proves the requested recurrence for all $n\ge4$.

### Question 5c.

Let $\alpha\in\mathbb{C}$ with $|\alpha|<2$, and choose a square root
$\Delta$ of $4-\alpha^2$. Since $|\alpha|<2$, one has $\alpha\ne\pm2$,
so $\Delta\ne0$. Put $$r_+=\frac{\alpha+i\Delta}{2},\qquad
  r_-=\frac{\alpha-i\Delta}{2}.$$ Then $$r_++r_-=\alpha,
  \qquad
  r_+r_-=\frac{\alpha^2+\Delta^2}{4}=1.$$ Thus $r_+$ and $r_-$ are the
two distinct roots of $r^2-\alpha r+1=0$.

For fixed $\alpha$, the numbers $\chi_n(\alpha)$ satisfy
$$\chi_n(\alpha)=\alpha\chi_{n-1}(\alpha)-\chi_{n-2}(\alpha),
  \qquad \chi_0(\alpha)=1,
  \qquad \chi_1(\alpha)=\alpha.$$ The sequence
$$q_n=\frac{r_+^{n+1}-r_-^{n+1}}{r_+-r_-}$$ has the same two initial
values and satisfies the same recurrence. Therefore $\chi_n(\alpha)=q_n$
for all $n\ge0$. Since $r_+-r_-=i\Delta$, we obtain, for every $n\ge2$,
$$\boxed{
  \chi_n(\alpha)=\frac{1}{i\sqrt{4-\alpha^2}}
  \left[
  \left(\frac{\alpha+i\sqrt{4-\alpha^2}}2\right)^{n+1}
  -
  \left(\frac{\alpha-i\sqrt{4-\alpha^2}}2\right)^{n+1}
  \right].}$$ Changing the sign of the chosen square root exchanges the
two terms and changes the sign of the denominator, so the value is
independent of this choice.

### Question 5d.

From the formula of Question 5c, expanded formally with $D^2=4-X^2$, one
obtains $$\begin{aligned}
  \chi_n(X)
  &=\frac{(X+iD)^{n+1}-(X-iD)^{n+1}}{iD\,2^{n+1}}\\
  &=\frac1{2^n}\sum_{s=0}^{\lfloor n/2\rfloor}
      (-1)^s\binom{n+1}{2s+1}X^{n-2s}(4-X^2)^s.
\end{aligned}$$ Thus the coefficient of $X^{n-2p}$, for
$0\le p\le\lfloor n/2\rfloor$, may be written as $$\frac{(-1)^p4^p}{2^n}
  \sum_{s=p}^{\lfloor n/2\rfloor}
  \binom{n+1}{2s+1}\binom{s}{p}.$$ This is already an exact expression
as a sum of products of binomial coefficients.

It simplifies to the following standard closed form:
$$\boxed{\chi_n(X)=\sum_{p=0}^{\lfloor n/2\rfloor}
  (-1)^p\binom{n-p}{p}X^{n-2p}.}$$ For completeness, we verify the
simplification by induction. The formula is true for $\chi_0=1$ and
$\chi_1=X$. If it holds for $\chi_{n-1}$ and $\chi_{n-2}$, the
coefficient of $X^{n-2p}$ in $$X\chi_{n-1}(X)-\chi_{n-2}(X)$$ is
$$(-1)^p\binom{n-1-p}{p}
  -(-1)^{p-1}\binom{n-p-1}{p-1}
  =(-1)^p\binom{n-p}{p},$$ by Pascal's identity. The induction follows.

### Question 6.

Let $\theta\in(0,\pi)$ and set $\alpha=2\cos\theta$. By Question 1 or by
Question 5c,
$$\chi_n(2\cos\theta)=\frac{\sin((n+1)\theta)}{\sin\theta}.$$ For
$$\theta_k=\frac{k\pi}{n+1},\qquad k=1,\dots,n,$$ we have
$\sin\theta_k\ne0$ and $\sin((n+1)\theta_k)=\sin(k\pi)=0$. Therefore
$$2\cos\left(\frac{k\pi}{n+1}\right)$$ is a root of $\chi_n$. These $n$
numbers are distinct because $\cos$ is strictly decreasing on $[0,\pi]$.
Since $\chi_n$ has degree $n$, they are all the roots. Hence
$$\boxed{\operatorname{Sp}(T_n)=\left\{2\cos\left(\frac{k\pi}{n+1}\right):1\le k\le n\right\},}$$
each eigenvalue having multiplicity $1$.

### Question 7.

By Question 6, $$S_f(T_n)=\frac1n\sum_{k=1}^n
  f\left(2\cos\left(\frac{k\pi}{n+1}\right)\right).$$ This is exactly
the expectation in Question 4a with $U_n$ uniform on $\{1,\dots,n\}$.
Therefore, for every continuous $f$ on $[-2,2]$, $$\boxed{
  \lim_{n\to\infty}S_f(T_n)
  =\frac1\pi\int_{-2}^2\frac{f(x)}{\sqrt{4-x^2}}\,dx.}$$

### Question 8a.

We have $$T_n(a,b,c)=aI_n+T_n(0,b,c).$$ If $\mu$ is an eigenvalue of
$T_n(0,b,c)$, then $a+\mu$ is an eigenvalue of $T_n(a,b,c)$ with the
same algebraic multiplicity. Equivalently,
$$\chi_{T_n(a,b,c)}(X)=\chi_{T_n(0,b,c)}(X-a).$$ Thus
$$\boxed{\operatorname{Sp}(T_n(a,b,c))=a+\operatorname{Sp}(T_n(0,b,c)),}$$
with multiplicities preserved.

### Question 8b.

Let $$D_n(X)=\det(XI_n-T_n(0,b,c)).$$ The matrix $XI_n-T_n(0,b,c)$ has
diagonal entries $X$, superdiagonal entries $-b$, and subdiagonal
entries $-c$. Expanding as in Question 5b gives
$$D_n(X)=X D_{n-1}(X)-bc\,D_{n-2}(X),
  \qquad D_0=1,
  \qquad D_1=X.$$ The same recurrence and the same initial values are
obtained for $$\det(XI_n-T_n(0,bc,1)).$$ Therefore the two
characteristic polynomials are equal. Together with Question 8a, this
gives
$$\boxed{\operatorname{Sp}(T_n(a,b,c))=a+\operatorname{Sp}(T_n(0,bc,1)),}$$
again with algebraic multiplicities.

### Question 8c.

Assume $bc>0$. Then $b$ and $c$ have the same sign. Set
$$r=\sqrt{\frac cb}>0,
  \qquad
  D=\operatorname{diag}(1,r,r^2,\dots,r^{n-1}).$$ A direct
computation gives $$D^{-1}T_n(0,b,c)D=s\sqrt{bc}\,T_n,$$ where $s=1$ if
$b,c>0$ and $s=-1$ if $b,c<0$. Indeed the new superdiagonal and
subdiagonal entries are respectively $br$ and $c/r$, both equal to
$s\sqrt{bc}$.

Thus $T_n(a,b,c)$ is similar to $$aI_n+s\sqrt{bc}\,T_n.$$ By Question 6
its eigenvalues are $$a+2s\sqrt{bc}\cos\left(\frac{k\pi}{n+1}\right),
  \qquad k=1,
  \dots,n.$$ If $s=-1$, this list is the same as the list with $s=1$,
because replacing $k$ by $n+1-k$ changes the sign of the cosine. Hence,
in all cases $bc>0$,
$$\boxed{\lambda_k=a+2\sqrt{bc}\cos\left(\frac{k\pi}{n+1}\right),
  \qquad k=1,\dots,n.}$$ The eigenvalues are real and simple.

### Question 9a.

For $bc>0$, Question 8c gives $$S_f(T_n(a,b,c))=\frac1n\sum_{k=1}^n
  f\left(a+2\sqrt{bc}\cos\left(\frac{k\pi}{n+1}\right)\right).$$ Define
$g$ on $[-2,2]$ by $$g(x)=f(a+\sqrt{bc}\,x).$$ If $f$ is continuous on
$\mathbb{R}$, then $g$ is continuous on $[-2,2]$. Applying Question 7 to
$g$ gives $$\begin{aligned}
 \lim_{n\to\infty}S_f(T_n(a,b,c))
 &=\frac1\pi\int_{-2}^2\frac{g(x)}{\sqrt{4-x^2}}\,dx\\
 &=\frac1\pi\int_{-2}^2\frac{f(a+\sqrt{bc}\,x)}{\sqrt{4-x^2}}\,dx.
\end{aligned}$$ Thus $$\boxed{\lim_{n\to\infty}S_f(T_n(a,b,c))
  =\frac1\pi\int_{-2}^2\frac{f(a+\sqrt{bc}\,x)}{\sqrt{4-x^2}}\,dx.}$$

### Question 9b.

Let $$\lambda_{n,k}=a+2\sqrt{bc}\cos\left(\frac{k\pi}{n+1}\right),
  \qquad 1\le k\le n.$$ The sequence $k\mapsto\lambda_{n,k}$ is strictly
decreasing. Define $$L_-=a-2\sqrt{bc},
  \qquad
  L_+=a+2\sqrt{bc}.$$

If $y<L_-$, then $q_n(y)=0$ for every $n$. If $y\ge L_+$, then
$q_n(y)=n$ for every $n$.

Assume now $L_-<y<L_+$. Put
$$\theta_y=\arccos\left(\frac{y-a}{2\sqrt{bc}}\right)\in(0,\pi).$$ Then
$$\lambda_{n,k}\le y
  \iff
  \frac{k\pi}{n+1}\ge \theta_y.$$ Hence $$q_n(y)=\#\left\{1\le k\le n:
  k\ge \frac{n+1}{\pi}\theta_y\right\}
  =n-\left\lceil\frac{n+1}{\pi}\theta_y\right\rceil+1,$$ up to the
harmless convention when the ceiling equals $n+1$, which cannot occur in
the present open interval for large $n$. Dividing by $n$ gives
$$\frac{q_n(y)}n\longrightarrow 1-\frac{\theta_y}{\pi}.$$ Equivalently,
$$1-\frac{\theta_y}{\pi}
  =\frac1\pi\int_{-2}^{(y-a)/\sqrt{bc}}
  \frac{dx}{\sqrt{4-x^2}}.$$ Therefore the clean global statement is
$$\boxed{\frac{q_n(y)}n\longrightarrow F(y),}$$ where $$F(y)=
  \begin{cases}
  0,& y\le a-2\sqrt{bc},\\[1mm]
  \displaystyle \frac1\pi\int_{-2}^{(y-a)/\sqrt{bc}}
  \frac{dx}{\sqrt{4-x^2}},& a-2\sqrt{bc}<y<a+2\sqrt{bc},\\[3mm]
  1,& y\ge a+2\sqrt{bc}.
  \end{cases}$$ Consequently, whenever $F(y)>0$,
$$\boxed{q_n(y)\sim nF(y).}$$ At the lower edge $y\le a-2\sqrt{bc}$ the
count is identically zero, so one should not state a nonzero equivalent
there.

## Part III: constructive Weierstrass approximation

The Weierstrass approximation theorem is not used in this part. It is
proved from the polynomials $$Q_n(X)=(1-X^n)^{2^n},
  \qquad
  P_n(X)=Q_n\left(\frac{1-X}{2}\right).$$ We write

$$
H(x)=
\begin{cases}
0,&x<0,\\
1,&x\ge 0.
\end{cases}
$$

The plan is to approximate this step function away from its jump, build
step-function approximations to an arbitrary continuous function, and
then replace every step by an explicit polynomial.

### Question 10a.

Let $0\le\kappa<1/2$.

On $[0,\kappa]$, for $n\ge1$ and $0\le x\le\kappa$,
$$0\le x^n\le\kappa^n.$$ Using $1-(1-t)^m\le mt$ for $0\le t\le1$ and
$m\ge1$, we obtain $$0\le 1-Q_n(x)
  =1-(1-x^n)^{2^n}
  \le 2^n x^n
  \le (2\kappa)^n.$$ Since $2\kappa<1$, this tends uniformly to $0$.
Thus $$Q_n\longrightarrow1
  \quad\text{uniformly on }[0,\kappa].$$

On $[1-\kappa,1]$, we have $x^n\ge(1-\kappa)^n$. Hence $$0\le Q_n(x)
  =(1-x^n)^{2^n}
  \le \left(1-(1-\kappa)^n\right)^{2^n}.$$ Using $1-t\le e^{-t}$,
$$Q_n(x)
  \le \exp\left(-2^n(1-\kappa)^n\right)
  =\exp\left(-(2(1-\kappa))^n\right).$$ Since $2(1-\kappa)>1$, this
upper bound tends to $0$. Thus $$Q_n\longrightarrow0
  \quad\text{uniformly on }[1-\kappa,1].$$

### Question 10b.

Let $0<\eta\le1$. For $x\in[-1,1]$ put $$t=\frac{1-x}{2}.$$ Then
$P_n(x)=Q_n(t)$.

If $x\in[\eta,1]$, then $$0\le t\le\frac{1-\eta}{2}=:\kappa<\frac12,$$
so $Q_n(t)\to1$ uniformly by Question 10a. Since $H(x)=1$ on $[\eta,1]$,
this gives uniform convergence to $H$ there.

If $x\in[-1,-\eta]$, then $$\frac{1+\eta}{2}\le t\le1.$$ Writing
$\kappa=(1-\eta)/2<1/2$, this interval is contained in $[1-\kappa,1]$,
so $Q_n(t)\to0$ uniformly by Question 10a. Since $H(x)=0$ on
$[-1,-\eta]$, this gives uniform convergence to $H$ there.

Therefore $$\boxed{P_n\longrightarrow H
  \quad\text{uniformly on }[-1,1]\setminus[-\eta,\eta].}$$

### Question 11.

Assume first that $f(-1)=0$. Since $f$ is continuous on the compact
interval $[-1,1]$, it is uniformly continuous. Choose $\delta>0$ such
that
$$|x-y|\le\delta\quad\Longrightarrow\quad |f(x)-f(y)|\le\varepsilon.$$
Choose a partition $$-1=t_0<t_1<\cdots<t_N<t_{N+1}=1$$ with mesh at most
$\delta$, and set $$c_i=t_i,
  \qquad
  a_i=f(t_i)-f(t_{i-1})
  \qquad(1\le i\le N).$$ Then $-1<c_1<\cdots<c_N<1$, and
$$|a_i|=|f(t_i)-f(t_{i-1})|\le\varepsilon.$$ Define
$$S(x)=\sum_{i=1}^N a_iH(x-c_i).$$ If $x\in[t_j,t_{j+1})$ with
$0\le j\le N$, then exactly the jumps $c_1,
\dots,c_j$ have occurred, so
$$S(x)=\sum_{i=1}^j a_i=f(t_j)-f(t_0)=f(t_j),$$ because
$f(t_0)=f(-1)=0$. Hence $$|f(x)-S(x)|=|f(x)-f(t_j)|\le\varepsilon.$$ At
$x=1$, one has $S(1)=f(t_N)$ and therefore
$$|f(1)-S(1)|=|f(1)-f(t_N)|\le\varepsilon.$$ Thus
$$\boxed{\forall x\in[-1,1],\qquad
  \left|f(x)-\sum_{i=1}^N a_iH(x-c_i)\right|\le\varepsilon,}$$ with
$a_i\in[-\varepsilon,\varepsilon]$.

### Question 12.

We first prove the result for $f(-1)=0$, then remove this assumption.

Let $\varepsilon>0$ and assume $f(-1)=0$. Apply Question 11 with
tolerance $\varepsilon/4$. We obtain points $$-1<c_1<\cdots<c_N<1$$ and
coefficients $a_i$ with $|a_i|\le\varepsilon/4$ such that
$$\left|f(x)-S(x)\right|\le\frac\varepsilon4,
  \qquad
  S(x)=\sum_{i=1}^N a_iH(x-c_i).$$ For each $i$, choose a positive
number $\rho_i$ such that $$\frac{x-c_i}{\rho_i}\in[-1,1]
  \qquad\text{for all }x\in[-1,1].$$ For example, one may take
$$\rho_i=1+|c_i|.$$ Then
$$H\left(\frac{x-c_i}{\rho_i}\right)=H(x-c_i),$$ because $\rho_i>0$.

Choose $\eta>0$ small enough that the intervals
$$[c_i-\rho_i\eta,c_i+\rho_i\eta]$$ are pairwise disjoint. This is
possible because the points $c_i$ are distinct. By Question 10b, for
each fixed $i$, $$P_m\left(\frac{x-c_i}{\rho_i}\right)
  \longrightarrow
  H\left(\frac{x-c_i}{\rho_i}\right)=H(x-c_i)$$ uniformly on the set of
$x\in[-1,1]$ such that $|x-c_i|\ge \rho_i\eta$.

Let $$A=\sum_{i=1}^N |a_i|.$$ If $A=0$, then $S=0$ and the proof is
immediate. Otherwise choose $m$ large enough that, simultaneously for
all $i$ and all $x\in[-1,1]$ with $|x-c_i|\ge \rho_i\eta$,
$$\left|P_m\left(\frac{x-c_i}{\rho_i}\right)-H(x-c_i)\right|
  \le \frac{\varepsilon}{4A}.$$ Define the polynomial
$$R_m(X)=\sum_{i=1}^N a_iP_m\left(\frac{X-c_i}{\rho_i}\right).$$ Fix
$x\in[-1,1]$. Because the intervals $[c_i-\rho_i\eta,c_i+\rho_i\eta]$
are pairwise disjoint, $x$ belongs to at most one of them. For all
indices for which $|x-c_i|\ge \rho_i\eta$, the total error is bounded by
$$\sum_i |a_i|\frac{\varepsilon}{4A}\le\frac\varepsilon4.$$ For the
possible exceptional index $j$, we use only the elementary bound
$$0\le P_m(t)\le1\qquad(-1\le t\le1),$$ which follows from
$0\le(1-t)/2\le1$. Hence
$$\left|P_m\left(\frac{x-c_j}{\rho_j}\right)-H(x-c_j)\right|\le1,$$ and
its contribution is at most $|a_j|\le\varepsilon/4$. Thus
$$|R_m(x)-S(x)|\le\frac\varepsilon2.$$ Together with
$|f(x)-S(x)|\le\varepsilon/4$, this gives
$$|f(x)-R_m(x)|\le\frac{3\varepsilon}{4}<\varepsilon.$$ This proves the
result when $f(-1)=0$.

For a general continuous $f$, apply the previous case to
$$g(x)=f(x)-f(-1),$$ which satisfies $g(-1)=0$. There is a polynomial
$R$ such that $$|g(x)-R(x)|\le\varepsilon
  \qquad(x\in[-1,1]).$$ Then $$P(X)=R(X)+f(-1)$$ satisfies
$$\boxed{\forall x\in[-1,1],\qquad |f(x)-P(x)|\le\varepsilon.}$$

*Scaling note.* The proof above uses the scaled polynomials
$P_m((X-c_i)/\rho_i)$. This is the same construction as the indicated
one, but it keeps the argument of $P_m$ inside $[-1,1]$, where Question
10b applies. Since $\rho_i>0$, the step function is unchanged:
$H((x-c_i)/\rho_i)=H(x-c_i)$.

## Part IV

Let $(W_{i,j})_{1\le i\le j}$ be independent, identically distributed
real random variables with mean zero, variance one, and the moment
assumptions stated in the paper. Extend them symmetrically by
$W_{j,i}=W_{i,j}$ and set

$$
X_n=\frac1{\sqrt n}(W_{i,j})_{1\le i,j\le n}.
$$

For a test function $f$, the empirical spectral average is

$$
S_n(f)=\frac1n\sum_{j=1}^n f(\lambda_j(X_n)).
$$

For $k\ge0$, recall $$f_k(x)=x^k,
  \qquad
  \Sigma(f)=\frac1{2\pi}\int_{-2}^2 f(x)\sqrt{4-x^2}\,dx.$$ For later
use, if $c\in\mathbb{R}$ and $j\ge0$, the function
$$x\longmapsto c\,x^j\sqrt{4-x^2}$$ is continuous on the compact
interval $[-2,2]$, hence integrable there. Thus finite linear
combinations of monomials may be integrated term by term against the
semicircle weight.

### Question 13a.

For every $\omega$, the matrix $X_n(\omega)$ is real symmetric. Hence it
is diagonalizable over $\mathbb{R}$ in an orthonormal basis. If its
eigenvalues are $\lambda_1,\dots,\lambda_n$, repeated with multiplicity,
then the eigenvalues of $X_n(\omega)^k$ are
$\lambda_1^k,\dots,\lambda_n^k$. Therefore
$$\operatorname{Tr}(X_n(\omega)^k)=\sum_{j=1}^n\lambda_j^k.$$ On the
other hand, $$S_n(f_k)(\omega)=\frac1n\sum_{j=1}^n\lambda_j^k.$$ Thus,
as random variables,
$$\boxed{S_n(f_k)=\frac1n\operatorname{Tr}(X_n^k).}$$

### Question 13b.

If $k$ is odd, the integrand $x^k\sqrt{4-x^2}$ is odd on $[-2,2]$, so
$$\boxed{\Sigma(f_k)=0\qquad(k\text{ odd}).}$$ Let $k=2p$. With
$x=2\cos\theta$, $$dx=-2\sin\theta\,d\theta,
  \qquad
  \sqrt{4-x^2}=2\sin\theta,$$ and therefore $$\begin{aligned}
 \Sigma(f_{2p})
 &=\frac1{2\pi}\int_0^\pi(2\cos\theta)^{2p}\,4\sin^2\theta\,d\theta\\
 &=\frac{2^{2p+1}}\pi\int_0^\pi\cos^{2p}\theta\,\sin^2\theta\,d\theta.
\end{aligned}$$ From Question 3c,
$$A_p:=\int_0^\pi\cos^{2p}\theta\,d\theta
  =\pi\,4^{-p}\binom{2p}{p}.$$ Since
$$\int_0^\pi\cos^{2p}\theta\sin^2\theta\,d\theta
  =A_p-A_{p+1},$$ and $$\frac{A_{p+1}}{A_p}=\frac{2p+1}{2p+2},$$ we
obtain $$A_p-A_{p+1}=\frac{A_p}{2p+2}.$$ Thus $$\begin{aligned}
 \Sigma(f_{2p})
 &=\frac{2^{2p+1}}\pi\cdot \frac{1}{2p+2}
   \pi\,4^{-p}\binom{2p}{p}\\
 &=\frac1{p+1}\binom{2p}{p}.
\end{aligned}$$ Consequently $$\boxed{
  \Sigma(f_k)=
  \begin{cases}
  0,& k\text{ odd},\\[1mm]
  \displaystyle \frac1{p+1}\binom{2p}{p},& k=2p.
  \end{cases}}$$ The even moments are the Catalan numbers.

### Question 13c.

We prove $(H_k)$ for $k=0,1,2$.

**Case $k=0$.** Since $X_n^0=I_n$, $$\operatorname{Tr}(X_n^0)=n.$$
Therefore
$$\frac1n\mathbb{E}(\operatorname{Tr}(X_n^0))=1=\Sigma(f_0),$$ and
$$\frac1{n^2}\mathbb{E}(\operatorname{Tr}(X_n^0)^2)=\frac1{n^2}n^2=1=\Sigma(f_0)^2.$$
Thus $(H_0)$ holds.

**Case $k=1$.** We have
$$\operatorname{Tr}(X_n)=\frac1{\sqrt n}\sum_{i=1}^n W_{i,i}.$$ Since
the variables have mean zero,
$$\frac1n\mathbb{E}(\operatorname{Tr}(X_n))=0=\Sigma(f_1).$$
Furthermore, by independence and mean zero, the cross terms vanish:
$$\begin{aligned}
 \mathbb{E}(\operatorname{Tr}(X_n)^2)
 &=\frac1n\mathbb{E}\left(\sum_{i=1}^n W_{i,i}\right)^2\\
 &=\frac1n\sum_{i=1}^n\mathbb{E}(W_{i,i}^2)
 =\frac1n\cdot n=1.
\end{aligned}$$ Hence
$$\frac1{n^2}\mathbb{E}(\operatorname{Tr}(X_n)^2)=\frac1{n^2}\longrightarrow0=\Sigma(f_1)^2.$$
Thus $(H_1)$ holds.

**Case $k=2$.** Since $X_n$ is symmetric,
$$\operatorname{Tr}(X_n^2)=\sum_{i,j=1}^n (X_n)_{i,j}^2.$$ Using the
definition of $X_n$, $$\operatorname{Tr}(X_n^2)
  =\frac1n\left(\sum_{i=1}^n W_{i,i}^2
  +2\sum_{1\le i<j\le n}W_{i,j}^2\right).$$ Thus $$\begin{aligned}
 \mathbb{E}(\operatorname{Tr}(X_n^2))
 &=\frac1n\left(n\mathbb{E}(W_{1,1}^2)+2\binom n2\mathbb{E}(W_{1,1}^2)\right)\\
 &=\frac1n\left(n+n(n-1)\right)=n.
\end{aligned}$$ Therefore
$$\frac1n\mathbb{E}(\operatorname{Tr}(X_n^2))=1=\Sigma(f_2).$$

It remains to prove the second limit. Put $$Y_{i,j}=W_{i,j}^2,
  \qquad
  A_n=\sum_{i=1}^nY_{i,i}+2\sum_{1\le i<j\le n}Y_{i,j}.$$ Then
$$\operatorname{Tr}(X_n^2)=\frac{A_n}{n},
  \qquad
  \mathbb{E}(A_n)=n^2.$$ Since $|W_{1,1}|^4$ has finite expectation,
$Y_{1,1}$ has finite variance. Let
$$\sigma_Y^2=\operatorname{Var}(Y_{1,1})<\infty.$$ By independence of
the variables $W_{i,j}$ for $i\le j$, $$\operatorname{Var}(A_n)
  =n\sigma_Y^2+4\binom n2\sigma_Y^2
  =O(n^2).$$ Consequently
$$\mathbb{E}(A_n^2)=\mathbb{E}(A_n)^2+\operatorname{Var}(A_n)=n^4+O(n^2).$$
Hence $$\frac1{n^2}\mathbb{E}(\operatorname{Tr}(X_n^2)^2)
  =\frac1{n^2}\mathbb{E}\left(\frac{A_n^2}{n^2}\right)
  =\frac{\mathbb{E}(A_n^2)}{n^4}
  \longrightarrow1=\Sigma(f_2)^2.$$ Thus $(H_2)$ holds.

In the remainder of the part, as stated in the problem, we assume
$(H_k)$ for every $k\ge0$.

### Question 14.

Let $k\ge0$, $B>0$, and $$g_{k,B}(x)=|x|^k\mathbf{1}_{|x|>B}.$$ For
every real $x$, $$|x|^k\mathbf{1}_{|x|>B}
  \le \frac{|x|^{2k}}{B^k}.$$ Indeed, on $\{|x|>B\}$ this is equivalent
to $B^k\le |x|^k$, and outside this set the left-hand side is zero.
Therefore, for every $\omega$, $$S_n(g_{k,B})(\omega)
  \le \frac1{B^k}S_n(f_{2k})(\omega).$$ The random variable
$S_n(g_{k,B})$ is nonnegative. Markov's inequality gives
$$\begin{aligned}
 \mathbb{P}(S_n(g_{k,B})\ge\varepsilon)
 &\le \frac1\varepsilon\mathbb{E}(S_n(g_{k,B}))\\
 &\le \frac1{\varepsilon B^k}\mathbb{E}(S_n(f_{2k})).
\end{aligned}$$ Hence $$\boxed{\mathbb{P}(S_n(g_{k,B})\ge\varepsilon)
  \le \frac{\mathbb{E}(S_n(f_{2k}))}{\varepsilon B^k}.}$$

### Question 15.

Fix $k\ge0$, $B>4$, and $\varepsilon>0$. Let $\ell\ge k$. Since
$|x|>B>1$ implies $|x|^k\le |x|^\ell$, we have
$$g_{k,B}\le g_{\ell,B}.$$ Therefore
$$\mathbb{P}(S_n(g_{k,B})\ge\varepsilon)
  \le \mathbb{P}(S_n(g_{\ell,B})\ge\varepsilon).$$ By Question 14,
$$\mathbb{P}(S_n(g_{\ell,B})\ge\varepsilon)
  \le \frac{\mathbb{E}(S_n(f_{2\ell}))}{\varepsilon B^\ell}.$$ Using
Question 13a and hypothesis $(H_{2\ell})$,
$$\mathbb{E}(S_n(f_{2\ell}))\longrightarrow\Sigma(f_{2\ell}).$$ By
Question 13b,
$$\Sigma(f_{2\ell})=\frac1{\ell+1}\binom{2\ell}{\ell}\le \binom{2\ell}{\ell}\le 4^\ell.$$
Taking $\limsup$ in $n$ gives
$$\limsup_{n\to\infty}\mathbb{P}(S_n(g_{k,B})\ge\varepsilon)
  \le \frac{4^\ell}{\varepsilon B^\ell}
  =\frac1\varepsilon\left(\frac4B\right)^\ell.$$ Now let
$\ell\to\infty$. Since $B>4$, the right-hand side tends to $0$. Hence
$$\boxed{\mathbb{P}(S_n(g_{k,B})\ge\varepsilon)\longrightarrow0.}$$

### Question 16.

Let $$Z_n=S_n(f_k)=\frac1n\operatorname{Tr}(X_n^k).$$ By $(H_k)$,
$$\mathbb{E}(Z_n)=\frac1n\mathbb{E}(\operatorname{Tr}(X_n^k))\longrightarrow\Sigma(f_k),$$
and
$$\mathbb{E}(Z_n^2)=\frac1{n^2}\mathbb{E}(\operatorname{Tr}(X_n^k)^2)\longrightarrow\Sigma(f_k)^2.$$
Therefore
$$\operatorname{Var}(Z_n)=\mathbb{E}(Z_n^2)-\mathbb{E}(Z_n)^2\longrightarrow0.$$
Chebyshev's inequality gives
$$\mathbb{P}(|Z_n-\mathbb{E}Z_n|\ge\varepsilon)
  \le\frac{\operatorname{Var}(Z_n)}{\varepsilon^2}\longrightarrow0.$$
Thus
$$\boxed{\mathbb{P}(|S_n(f_k)-\mathbb{E}(S_n(f_k))|\ge\varepsilon)\longrightarrow0.}$$

### Question 17a.

Fix $B>4$, let $f$ be continuous on $\mathbb{R}$ and zero outside
$[-B,B]$, and fix $\varepsilon>0$.

We shall use explicitly the following elementary properties of the
spectral average. For each fixed matrix, $S_n$ is a positive linear
functional on functions of the eigenvalue variable:
$$S_n(af+bg)=aS_n(f)+bS_n(g),\qquad
  f\le g\Rightarrow S_n(f)\le S_n(g),$$ and it is normalised by
$S_n(1)=1$. Consequently, if $|h|\le g$, then $$|S_n(h)|\le S_n(g).$$
These identities follow immediately from the definition
$S_n(h)=n^{-1}\sum_{i=1}^n h(\lambda_i)$, with eigenvalues repeated
according to multiplicity.

Apply Question 12 to the function $t\mapsto f(Bt)$ on $[-1,1]$, then
compose the approximating polynomial with $x\mapsto x/B$. Thus there is
a polynomial $P\in\mathbb{R}[X]$ such that
$$\sup_{|x|\le B}|f(x)-P(x)|\le \eta,$$ where $\eta>0$ will be chosen
below. We take $$\eta=\frac\varepsilon{16}.$$ Since the semicircle
density is supported on $[-2,2]\subset[-B,B]$, we have
$$|\Sigma(f)-\Sigma(P)|\le \eta\Sigma(1)=\eta.$$ Indeed, on $[-2,2]$ one
has $|f-P|\le\eta$ and $\sqrt{4-x^2}\ge0$, hence $$|\Sigma(f)-\Sigma(P)|
  \le {1\over 2\pi}\int_{-2}^2 |f(x)-P(x)|\sqrt{4-x^2}\,dx
  \le \eta\Sigma(1).$$ Here $\Sigma(1)=1$ by Question 13b with $p=0$.
Moreover, because $P$ is a finite linear combination of monomials,
linearity of $S_n$, linearity of expectation, and the first part of
$(H_k)$ give $$\mathbb{E}(S_n(P))\longrightarrow \Sigma(P).$$ Choose $N$
such that, for all $n\ge N$, $$|\mathbb{E}(S_n(P))-\Sigma(P)|\le\eta.$$

For every real $x$, $$f(x)-P(x)
  =(f(x)-P(x))\mathbf{1}_{|x|\le B}-P(x)\mathbf{1}_{|x|>B},$$ because
$f(x)=0$ when $|x|>B$. Therefore, for every $n$ and every $\omega$,
$$|S_n(f)(\omega)-S_n(P)(\omega)|
  \le \eta+|S_n(P\mathbf{1}_{|x|>B})(\omega)|.$$ Indeed, the part
$(f-P)\mathbf{1}_{|x|\le B}$ has absolute value at most $\eta$, so
positivity and $S_n(1)=1$ bound its spectral average by $\eta$; the
remaining term is the polynomial tail. For $n\ge N$, we now write
$$\begin{aligned}
 |S_n(f)-\Sigma(f)|
 &\le |S_n(P)-\mathbb{E}(S_n(P))|\\
 &\quad +|\mathbb{E}(S_n(P))-\Sigma(P)|
       +|\Sigma(P)-\Sigma(f)|
       +|S_n(f)-S_n(P)|\\
 &\le |S_n(P)-\mathbb{E}(S_n(P))|
       +|S_n(P\mathbf{1}_{|x|>B})|+3\eta.
\end{aligned}$$ Since $3\eta=3\varepsilon/16<\varepsilon/2$, if both
$$|S_n(P\mathbf{1}_{|x|>B})|<\frac\varepsilon4
  \quad\text{and}\quad
  |S_n(P)-\mathbb{E}(S_n(P))|<\frac\varepsilon4,$$ then
$$|S_n(f)-\Sigma(f)|<\varepsilon.$$ Consequently, for every $n\ge N$,
$$\boxed{
  \mathbb{P}(|S_n(f)-\Sigma(f)|\ge\varepsilon)
  \le
  \mathbb{P}(|S_n(P\mathbf{1}_{|x|>B})|\ge\varepsilon/4)
  +
  \mathbb{P}(|S_n(P)-\mathbb{E}(S_n(P))|\ge\varepsilon/4).}$$

### Question 17b.

We prove that the two probabilities on the right-hand side of Question
17a tend to zero.

First, write $$P(x)=\sum_{j=0}^d c_jx^j.$$ By Question 16 and the union
bound, polynomial fluctuations vanish in probability. Indeed, if
$$C_1=\sum_{j=0}^d |c_j|,$$ then $$|S_n(P)-\mathbb{E}(S_n(P))|
  \le\sum_{j=0}^d |c_j|\,|S_n(f_j)-\mathbb{E}(S_n(f_j))|.$$ If $C_1=0$,
the quantity is zero. Otherwise, the event
$$|S_n(P)-\mathbb{E}(S_n(P))|\ge\varepsilon/4$$ is contained in the
union of the events
$$|S_n(f_j)-\mathbb{E}(S_n(f_j))|\ge\frac{\varepsilon}{4(d+1)\max(1,C_1)}
  \qquad(0\le j\le d),$$ each of which has probability tending to zero
by Question 16. Hence
$$\mathbb{P}(|S_n(P)-\mathbb{E}(S_n(P))|\ge\varepsilon/4)\longrightarrow0.$$

Second, for $|x|>B>1$ and $0\le j\le d$, we have $|x|^j\le |x|^d$.
Therefore $$|P(x)|\mathbf{1}_{|x|>B}
  \le C_1 |x|^d\mathbf{1}_{|x|>B}=C_1 g_{d,B}(x).$$ Thus
$$|S_n(P\mathbf{1}_{|x|>B})|
  \le S_n(|P|\mathbf{1}_{|x|>B})
  \le C_1 S_n(g_{d,B}).$$ The first inequality is the estimate
$|S_n(h)|\le S_n(|h|)$ applied to $h=P\mathbf{1}_{|x|>B}$, and the
second follows from positivity of $S_n$. If $C_1=0$, the probability is
zero. Otherwise Question 15 gives $$\begin{aligned}
 \mathbb{P}(|S_n(P\mathbf{1}_{|x|>B})|\ge\varepsilon/4)
 &\le \mathbb{P}\left(S_n(g_{d,B})\ge\frac{\varepsilon}{4C_1}\right)\\
 &\longrightarrow0.
\end{aligned}$$ Combining this with Question 17a yields
$$\boxed{\mathbb{P}(|S_n(f)-\Sigma(f)|\ge\varepsilon)\longrightarrow0.}$$
This is the asserted convergence in probability of the spectral averages
against every continuous compactly supported test function supported in
$[-B,B]$ with $B>4$.

## Conclusion

The final statement is a weak form of the Wigner semicircle law: for every
continuous compactly supported function $f$ covered by the argument,

$$
S_n(f)\xrightarrow{\mathbb P}
\frac1{2\pi}\int_{-2}^2 f(x)\sqrt{4-x^2}\,dx.
$$

The proof is assembled from four ingredients developed by the paper itself:

1. exact trigonometric control of a second-order recurrence;
2. explicit spectra and Riemann-sum limits for tridiagonal matrices;
3. constructive polynomial approximation without invoking Weierstrass as a black box;
4. moment, variance, and tail estimates for random spectral averages.

That architecture is the real strength of the problem. The early cosine grid
produces the arcsine law; the later trace moments produce the Catalan numbers
and the semicircle law. The two limiting measures are different, but the same
ideas of spectral averaging and polynomial approximation connect them.

For the formal verification record, including the exact compiled suppliers
for the low-degree Wigner moments and integrability, see the companion article
[Formalizing an X/ENS Correction in Lean](/2026/07/18/formalizing-xens-correction-in-lean/).

</div>
