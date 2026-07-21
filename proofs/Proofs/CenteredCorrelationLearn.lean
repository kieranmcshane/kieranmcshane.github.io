import Mathlib

open scoped BigOperators

namespace CenteredCorrelationLearn

variable {ι : Type*} (u : Finset ι)
variable (p r s : ι → ℝ) (rbar sbar T : ℝ)

/-- Replacing the raw cross-moment is a genuine equality rewrite. -/
theorem rewrite_cross_moment
    (hT : ∑ i ∈ u, p i * (r i * s i) = T) :
    T - rbar * sbar = (∑ i ∈ u, p i * (r i * s i)) - rbar * sbar := by
  rw [hT]

/-- A legal but strategically circular rewrite: solve the definition of `C` for `T`. -/
theorem rewrite_through_center (C : ℝ)
    (hC : C = T - rbar * sbar) :
    T = C + rbar * sbar := by
  linarith

/-- A legal first-moment rewrite that is usually less useful at this point. -/
theorem rewrite_left_mean
    (hr : ∑ i ∈ u, p i * r i = rbar) :
    T - rbar * sbar = T - (∑ i ∈ u, p i * r i) * sbar := by
  rw [hr]

/-- The analogous legal detour on the second local mean. -/
theorem rewrite_right_mean
    (hs : ∑ i ∈ u, p i * s i = sbar) :
    T - rbar * sbar = T - rbar * (∑ i ∈ u, p i * s i) := by
  rw [hs]

/-- The two first-moment identities insert exactly the zero terms needed for centering. -/
theorem insert_zero_means
    (hp : ∑ i ∈ u, p i = 1)
    (hr : ∑ i ∈ u, p i * r i = rbar)
    (hs : ∑ i ∈ u, p i * s i = sbar) :
    (∑ i ∈ u, p i * (r i * s i)) - rbar * sbar =
      ∑ i ∈ u, p i *
        (r i * s i - r i * sbar - rbar * s i + rbar * sbar) := by
  symm
  calc
    ∑ i ∈ u, p i *
        (r i * s i - r i * sbar - rbar * s i + rbar * sbar) =
        ∑ i ∈ u,
          (p i * (r i * s i) - (p i * r i) * sbar -
            rbar * (p i * s i) + p i * (rbar * sbar)) := by
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ = (∑ i ∈ u, p i * (r i * s i)) -
          (∑ i ∈ u, p i * r i) * sbar -
          rbar * (∑ i ∈ u, p i * s i) +
          (∑ i ∈ u, p i) * (rbar * sbar) := by
      rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_sub_distrib]
      rw [Finset.sum_mul, Finset.mul_sum, Finset.sum_mul]
    _ = (∑ i ∈ u, p i * (r i * s i)) - rbar * sbar := by
      rw [hp, hr, hs]
      ring

/-- The four-term summand is the product of the two centered factors. -/
theorem factor_centered_summand (ri si : ℝ) :
    ri * si - ri * sbar - rbar * si + rbar * sbar =
      (ri - rbar) * (si - sbar) := by
  ring

/-- The complete covariance identity used in the article. -/
theorem centered_covariance_identity
    (hp : ∑ i ∈ u, p i = 1)
    (hr : ∑ i ∈ u, p i * r i = rbar)
    (hs : ∑ i ∈ u, p i * s i = sbar)
    (hT : ∑ i ∈ u, p i * (r i * s i) = T) :
    T - rbar * sbar = ∑ i ∈ u, p i * ((r i - rbar) * (s i - sbar)) := by
  rw [rewrite_cross_moment u p r s rbar sbar T hT]
  rw [insert_zero_means u p r s rbar sbar hp hr hs]
  congr 1
  funext i
  rw [factor_centered_summand rbar sbar]

/-- The scalar weighted Cauchy--Schwarz step used after rank-one norm factorization. -/
theorem weighted_cauchy_schwarz
    (a b : ι → ℝ)
    (hp : ∀ i ∈ u, 0 ≤ p i) :
    ∑ i ∈ u, p i * a i * b i ≤
      √(∑ i ∈ u, p i * a i ^ 2) * √(∑ i ∈ u, p i * b i ^ 2) := by
  calc
    ∑ i ∈ u, p i * a i * b i =
        ∑ i ∈ u, (√(p i) * a i) * (√(p i) * b i) := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [mul_mul_mul_comm, Real.mul_self_sqrt (hp i hi)]
      ring
    _ ≤ √(∑ i ∈ u, (√(p i) * a i) ^ 2) *
          √(∑ i ∈ u, (√(p i) * b i) ^ 2) :=
      Real.sum_mul_le_sqrt_mul_sqrt u _ _
    _ = √(∑ i ∈ u, p i * a i ^ 2) * √(∑ i ∈ u, p i * b i ^ 2) := by
      congr 2 <;>
        apply Finset.sum_congr rfl <;>
        intro i hi <;>
        rw [mul_pow, Real.sq_sqrt (hp i hi)]

/-- Centering converts the weighted second moment into a variance deficit. -/
theorem weighted_variance_identity
    (hp : ∑ i ∈ u, p i = 1)
    (hr : ∑ i ∈ u, p i * r i = rbar) :
    ∑ i ∈ u, p i * (r i - rbar) ^ 2 =
      (∑ i ∈ u, p i * r i ^ 2) - rbar ^ 2 := by
  calc
    ∑ i ∈ u, p i * (r i - rbar) ^ 2 =
        ∑ i ∈ u, (p i * r i ^ 2 - 2 * rbar * (p i * r i) + p i * rbar ^ 2) := by
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ = (∑ i ∈ u, p i * r i ^ 2) -
          2 * rbar * (∑ i ∈ u, p i * r i) +
          (∑ i ∈ u, p i) * rbar ^ 2 := by
      rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
      rw [Finset.mul_sum, Finset.sum_mul]
    _ = (∑ i ∈ u, p i * r i ^ 2) - rbar ^ 2 := by
      rw [hp, hr]
      ring

end CenteredCorrelationLearn
