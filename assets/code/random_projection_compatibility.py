"""Reproduce the finite-dimensional experiment in Figure 3.

The script samples pairs of complex Haar-random subspaces. Their squared
principal-angle cosines are the squared singular values of U*V. For binary
projective measurements, the exact white-noise compatibility degree is

    min_x 1 / (sqrt(x) + sqrt(1 - x)).

Run from the repository root:

    python3 assets/code/random_projection_compatibility.py

The default seed, dimensions, cases, and sample count match the blog figure.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


DEFAULT_CASES = (
    (0.50, 0.50, "inside"),
    (0.90, 0.20, "boundary"),
    (0.95, 0.20, "outside"),
)
DEFAULT_DIMENSIONS = (24, 48, 96, 160)


def limiting_spectral_interval(alpha: float, beta: float) -> tuple[float, float]:
    """Return the limiting support of squared principal-angle cosines."""
    if not 0.0 <= alpha <= 1.0 or not 0.0 <= beta <= 1.0:
        raise ValueError("alpha and beta must lie in [0, 1]")
    center = alpha + beta - 2.0 * alpha * beta
    radius = 2.0 * math.sqrt(alpha * (1.0 - alpha) * beta * (1.0 - beta))
    return max(0.0, center - radius), min(1.0, center + radius)


def block_visibility(value: np.ndarray | float) -> np.ndarray | float:
    """Return the compatibility visibility of one principal-angle block."""
    clipped = np.clip(value, 0.0, 1.0)
    return 1.0 / (np.sqrt(clipped) + np.sqrt(1.0 - clipped))


def limiting_visibility(alpha: float, beta: float) -> float:
    """Return the high-dimensional prediction at rank fractions alpha, beta."""
    lower, upper = limiting_spectral_interval(alpha, beta)
    closest_to_half = min(max(0.5, lower), upper)
    return float(block_visibility(closest_to_half))


def haar_subspace_frame(
    dimension: int,
    rank: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample an orthonormal frame for a complex Haar-random subspace."""
    if not 0 <= rank <= dimension:
        raise ValueError("rank must lie between zero and dimension")
    if rank == 0:
        return np.empty((dimension, 0), dtype=np.complex128)
    gaussian = (
        rng.standard_normal((dimension, rank))
        + 1j * rng.standard_normal((dimension, rank))
    ) / math.sqrt(2.0)
    frame, triangular = np.linalg.qr(gaussian, mode="reduced")
    diagonal = np.diag(triangular)
    phases = np.where(np.abs(diagonal) > 0.0, diagonal / np.abs(diagonal), 1.0)
    return frame * phases.conjugate()


def finite_visibility(
    dimension: int,
    alpha: float,
    beta: float,
    rng: np.random.Generator,
) -> float:
    """Sample the exact finite-dimensional degree for one projection pair."""
    rank_e = min(dimension, max(0, math.floor(alpha * dimension)))
    rank_f = min(dimension, max(0, math.floor(beta * dimension)))
    if rank_e == 0 or rank_f == 0:
        return 1.0

    # Unitary invariance lets us fix the first subspace.
    frame_e = np.eye(dimension, rank_e, dtype=np.complex128)
    frame_f = haar_subspace_frame(dimension, rank_f, rng)
    singular_values = np.linalg.svd(
        frame_e.conjugate().T @ frame_f,
        compute_uv=False,
    )
    principal_values = np.clip(singular_values**2, 0.0, 1.0)
    return float(np.min(block_visibility(principal_values)))


def run_experiment(
    *,
    dimensions: tuple[int, ...],
    samples: int,
    seed: int,
) -> list[dict[str, str | int | float]]:
    """Return the seeded Monte Carlo summaries used in Figure 3."""
    if samples < 1:
        raise ValueError("samples must be positive")
    rng = np.random.default_rng(seed)
    rows: list[dict[str, str | int | float]] = []
    for alpha, beta, region in DEFAULT_CASES:
        target = limiting_visibility(alpha, beta)
        for dimension in dimensions:
            values = np.array(
                [
                    finite_visibility(dimension, alpha, beta, rng)
                    for _ in range(samples)
                ]
            )
            lower, median, upper = np.quantile(values, [0.1, 0.5, 0.9])
            rows.append(
                {
                    "region": region,
                    "alpha": alpha,
                    "beta": beta,
                    "dimension": dimension,
                    "samples": samples,
                    "seed": seed,
                    "q10": float(lower),
                    "median": float(median),
                    "q90": float(upper),
                    "limiting_tau": target,
                }
            )
    return rows


def write_csv(rows: list[dict[str, str | int | float]], path: Path) -> None:
    """Write summaries with stable column order."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "region",
        "alpha",
        "beta",
        "dimension",
        "samples",
        "seed",
        "q10",
        "median",
        "q90",
        "limiting_tau",
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dimensions",
        type=int,
        nargs="+",
        default=DEFAULT_DIMENSIONS,
    )
    parser.add_argument("--samples", type=int, default=48)
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/data/finite-dimension-check.csv"),
    )
    args = parser.parse_args()
    rows = run_experiment(
        dimensions=tuple(args.dimensions),
        samples=args.samples,
        seed=args.seed,
    )
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
