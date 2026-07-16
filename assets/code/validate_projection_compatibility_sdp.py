"""Independently audit the two-projection compatibility formula with an SDP.

For two projections P and Q, the blog uses the closed form

    tau = 1 / sqrt(1 + 2 ||[P, Q]||).

This program does not use that formula inside the optimization. It maximizes
the common visibility t directly over the binary joint-measurability
constraints, then compares the SDP optimum with the closed form afterward.

Run from the repository root:

    python3 -m pip install -r assets/code/sdp-requirements.txt
    python3 assets/code/validate_projection_compatibility_sdp.py
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import cvxpy as cp
import numpy as np


DEFAULT_CASES = (
    (2, 1, 1),
    (3, 1, 2),
    (4, 1, 2),
    (4, 2, 3),
    (6, 1, 4),
    (6, 2, 3),
    (6, 3, 4),
    (6, 5, 2),
)


def haar_projection(
    dimension: int,
    rank: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample a complex Haar-random projection of the requested rank."""
    gaussian = (
        rng.standard_normal((dimension, rank))
        + 1j * rng.standard_normal((dimension, rank))
    ) / math.sqrt(2.0)
    frame = np.linalg.qr(gaussian, mode="reduced")[0]
    projection = frame @ frame.conjugate().T
    return (projection + projection.conjugate().T) / 2.0


def closed_form_visibility(projection_p: np.ndarray, projection_q: np.ndarray) -> float:
    """Evaluate the formula only after the independent SDP has been solved."""
    commutator = projection_p @ projection_q - projection_q @ projection_p
    commutator_norm = float(np.linalg.norm(commutator, ord=2))
    return 1.0 / math.sqrt(1.0 + 2.0 * commutator_norm)


def sdp_visibility(
    projection_p: np.ndarray,
    projection_q: np.ndarray,
    solver: str,
) -> float:
    """Maximize visibility using the original binary compatibility constraints."""
    dimension = projection_p.shape[0]
    identity = np.eye(dimension, dtype=np.complex128)
    visibility = cp.Variable(name="visibility")
    joint_plus_plus = cp.Variable(
        (dimension, dimension),
        hermitian=True,
        name="joint_plus_plus",
    )

    noisy_p = visibility * projection_p + (1.0 - visibility) * identity / 2.0
    noisy_q = visibility * projection_q + (1.0 - visibility) * identity / 2.0
    constraints = (
        visibility >= 0.0,
        visibility <= 1.0,
        joint_plus_plus >> 0,
        noisy_p - joint_plus_plus >> 0,
        noisy_q - joint_plus_plus >> 0,
        identity - noisy_p - noisy_q + joint_plus_plus >> 0,
    )
    problem = cp.Problem(cp.Maximize(visibility), constraints)

    if solver == "CLARABEL":
        problem.solve(
            solver=solver,
            tol_gap_abs=1e-9,
            tol_gap_rel=1e-9,
            tol_feas=1e-9,
            max_iter=500,
        )
    elif solver == "SCS":
        problem.solve(solver=solver, eps=1e-8, max_iters=200_000)
    else:
        problem.solve(solver=solver)

    if problem.status not in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}:
        raise RuntimeError(f"SDP failed with status {problem.status!r}")
    return float(visibility.value)


def choose_solver(requested: str | None) -> str:
    """Choose a conic solver that supports positive-semidefinite constraints."""
    installed = set(cp.installed_solvers())
    if requested is not None:
        if requested not in installed:
            raise RuntimeError(f"requested solver {requested!r} is not installed")
        return requested
    for candidate in ("SCS", "CLARABEL"):
        if candidate in installed:
            return candidate
    raise RuntimeError("install CLARABEL or SCS through CVXPY before running this audit")


def run_audit(seed: int, solver: str) -> list[dict[str, int | float | str]]:
    """Run the fixed seeded cases and return one row per independent SDP."""
    rng = np.random.default_rng(seed)
    rows: list[dict[str, int | float | str]] = []
    for case, (dimension, rank_p, rank_q) in enumerate(DEFAULT_CASES, start=1):
        projection_p = haar_projection(dimension, rank_p, rng)
        projection_q = haar_projection(dimension, rank_q, rng)
        sdp_tau = sdp_visibility(projection_p, projection_q, solver)
        formula_tau = closed_form_visibility(projection_p, projection_q)
        rows.append(
            {
                "case": case,
                "dimension": dimension,
                "rank_p": rank_p,
                "rank_q": rank_q,
                "seed": seed,
                "solver": solver,
                "sdp_tau": sdp_tau,
                "formula_tau": formula_tau,
                "absolute_error": abs(sdp_tau - formula_tau),
            }
        )
    return rows


def write_csv(rows: list[dict[str, int | float | str]], output: Path) -> None:
    """Write the audit trail with a stable column order."""
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = tuple(rows[0].keys())
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument("--solver", type=str)
    parser.add_argument("--tolerance", type=float, default=2e-6)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/data/sdp-validation.csv"),
    )
    args = parser.parse_args()

    solver = choose_solver(args.solver)
    rows = run_audit(args.seed, solver)
    write_csv(rows, args.output)
    largest_error = max(float(row["absolute_error"]) for row in rows)
    print(f"Solved {len(rows)} independent SDPs with {solver}.")
    print(f"Largest absolute discrepancy: {largest_error:.3e}")
    print(f"Wrote audit data to {args.output}")
    if largest_error > args.tolerance:
        raise SystemExit(
            f"largest discrepancy exceeds tolerance {args.tolerance:.3e}"
        )


if __name__ == "__main__":
    main()
