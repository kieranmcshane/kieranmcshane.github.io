#!/usr/bin/env python3
"""Numerical checks for the two-qubit examples in the centered-tensor post."""

from __future__ import annotations

import numpy as np


def nuclear_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.svd(matrix, compute_uv=False).sum())


def separable_example(p: float) -> tuple[float, float]:
    r = np.array([0.0, 0.0, 2.0 * p - 1.0])
    correlation = np.diag([0.0, 0.0, 1.0])
    centered = correlation - np.outer(r, r)
    purity = p * p + (1.0 - p) ** 2
    bound = 2.0 * (1.0 - purity)
    return nuclear_norm(centered), bound


def entangled_example(gamma: float) -> tuple[float, float]:
    u = np.sin(2.0 * gamma)
    centered = np.diag([u, -u, u * u])
    marginal_purity = 1.0 - 0.5 * u * u
    bound = 2.0 * (1.0 - marginal_purity)
    return nuclear_norm(centered), bound


def main() -> None:
    tolerance = 1e-12

    for p in np.linspace(0.0, 1.0, 11):
        lhs, rhs = separable_example(float(p))
        if not np.isclose(lhs, rhs, atol=tolerance):
            raise AssertionError(f"separable check failed at p={p}: {lhs} != {rhs}")

    for gamma in np.linspace(0.02, np.pi / 4.0, 11):
        lhs, rhs = entangled_example(float(gamma))
        if not lhs > rhs + tolerance:
            raise AssertionError(
                f"entangled check failed at gamma={gamma}: {lhs} <= {rhs}"
            )

    print("11 separable saturation checks passed")
    print("11 entangled-state violation checks passed")


if __name__ == "__main__":
    main()
