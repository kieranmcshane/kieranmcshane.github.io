#!/usr/bin/env python3
"""Reproduce the two-qubit checks and detection-region figure.

The calculations start from 4 x 4 density matrices. Bloch vectors, correlation
matrices, marginal purities, partial transposes, and both separability tests are
then computed numerically rather than inserted as closed-form inputs.

From the repository root:

    python3 assets/code/centered_correlation_examples.py --write-artifacts

To inspect an arbitrary two-qubit state stored as a 4 x 4 NumPy array:

    python3 assets/code/centered_correlation_examples.py --matrix rho.npy
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np


COMPLEX = np.complex128
IDENTITY = np.eye(2, dtype=COMPLEX)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=COMPLEX)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=COMPLEX)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=COMPLEX)
PAULIS = (SIGMA_X, SIGMA_Y, SIGMA_Z)


@dataclass(frozen=True)
class CriterionValues:
    r: np.ndarray
    s: np.ndarray
    correlation: np.ndarray
    centered: np.ndarray
    purity_a: float
    purity_b: float
    devicente_lhs: float
    centered_lhs: float
    centered_budget: float
    min_partial_transpose_eigenvalue: float


def projector(vector: np.ndarray) -> np.ndarray:
    return np.outer(vector, vector.conj())


def nuclear_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.svd(matrix, compute_uv=False).sum())


def reduced_states(rho: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    tensor = rho.reshape(2, 2, 2, 2)
    rho_a = np.trace(tensor, axis1=1, axis2=3)
    rho_b = np.trace(tensor, axis1=0, axis2=2)
    return rho_a, rho_b


def partial_transpose_b(rho: np.ndarray) -> np.ndarray:
    return rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def realign(rho: np.ndarray) -> np.ndarray:
    """Return R(rho) with R(A tensor B) = vec(A) vec(B)^T."""
    return rho.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4)


def bloch_data(rho: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r = np.array(
        [np.trace(rho @ np.kron(sigma, IDENTITY)).real for sigma in PAULIS]
    )
    s = np.array(
        [np.trace(rho @ np.kron(IDENTITY, sigma)).real for sigma in PAULIS]
    )
    correlation = np.array(
        [
            [np.trace(rho @ np.kron(left, right)).real for right in PAULIS]
            for left in PAULIS
        ]
    )
    return r, s, correlation


def evaluate(rho: np.ndarray) -> CriterionValues:
    rho_a, rho_b = reduced_states(rho)
    r, s, correlation = bloch_data(rho)
    centered = correlation - np.outer(r, s)
    purity_a = float(np.trace(rho_a @ rho_a).real)
    purity_b = float(np.trace(rho_b @ rho_b).real)
    centered_budget = 2.0 * np.sqrt(
        max(0.0, 1.0 - purity_a) * max(0.0, 1.0 - purity_b)
    )
    min_pt = float(np.linalg.eigvalsh(partial_transpose_b(rho)).min())
    return CriterionValues(
        r=r,
        s=s,
        correlation=correlation,
        centered=centered,
        purity_a=purity_a,
        purity_b=purity_b,
        devicente_lhs=nuclear_norm(correlation),
        centered_lhs=nuclear_norm(centered),
        centered_budget=centered_budget,
        min_partial_transpose_eigenvalue=min_pt,
    )


def validate_density_matrix(rho: np.ndarray, tolerance: float = 1e-10) -> None:
    """Reject malformed inputs before reporting separability criteria."""
    if rho.shape != (4, 4):
        raise ValueError(f"expected a 4 x 4 matrix, received shape {rho.shape}")
    if not np.allclose(rho, rho.conj().T, atol=tolerance):
        raise ValueError("the matrix is not Hermitian")
    if not np.isclose(np.trace(rho), 1.0, atol=tolerance):
        raise ValueError("the matrix does not have trace one")
    minimum = float(np.linalg.eigvalsh(rho).min())
    if minimum < -tolerance:
        raise ValueError(f"the matrix is not positive semidefinite (min={minimum:.3e})")


def print_report(rho: np.ndarray) -> None:
    """Print both norm tests and the PPT diagnostic for one two-qubit state."""
    validate_density_matrix(rho)
    values = evaluate(rho)
    options = {"precision": 6, "suppress_small": True}
    print("r =", np.array2string(values.r, **options))
    print("s =", np.array2string(values.s, **options))
    print("T =\n", np.array2string(values.correlation, **options))
    print("C = T - r s^T =\n", np.array2string(values.centered, **options))
    print(
        "de Vicente: "
        f"{values.devicente_lhs:.8f} <= 1 "
        f"({'passes' if values.devicente_lhs <= 1.0 + 1e-10 else 'violates'})"
    )
    print(
        "centered: "
        f"{values.centered_lhs:.8f} <= {values.centered_budget:.8f} "
        f"({'passes' if values.centered_lhs <= values.centered_budget + 1e-10 else 'violates'})"
    )
    print(
        "minimum partial-transpose eigenvalue: "
        f"{values.min_partial_transpose_eigenvalue:.8f}"
    )


def classical_separable_state(p: float) -> np.ndarray:
    ket_00 = np.array([1, 0, 0, 0], dtype=COMPLEX)
    ket_11 = np.array([0, 0, 0, 1], dtype=COMPLEX)
    return p * projector(ket_00) + (1.0 - p) * projector(ket_11)


def schmidt_state(gamma: float) -> np.ndarray:
    vector = np.array([np.cos(gamma), 0, 0, np.sin(gamma)], dtype=COMPLEX)
    return projector(vector)


def polarized_noise_state(p: float, gamma: float) -> np.ndarray:
    zero = np.array([1, 0], dtype=COMPLEX)
    product_noise = np.kron(projector(zero), IDENTITY / 2.0)
    return p * schmidt_state(gamma) + (1.0 - p) * product_noise


def zhang_false_negative_state(p: float) -> np.ndarray:
    """Two-qubit family from Zhang et al., entangled for every positive p."""
    singlet = np.array([0, 1, -1, 0], dtype=COMPLEX) / np.sqrt(2.0)
    ket_00 = np.array([1, 0, 0, 0], dtype=COMPLEX)
    ket_01 = np.array([0, 1, 0, 0], dtype=COMPLEX)
    product_noise = (
        (2.0 / 3.0) * projector(ket_00) + (1.0 / 3.0) * projector(ket_01)
    )
    return p * projector(singlet) + (1.0 - p) * product_noise


def random_pure_qubit(rng: np.random.Generator) -> np.ndarray:
    vector = rng.normal(size=2) + 1j * rng.normal(size=2)
    return projector(vector / np.linalg.norm(vector))


def random_separable_state(
    rng: np.random.Generator,
    terms: int = 4,
) -> np.ndarray:
    weights = rng.dirichlet(np.ones(terms))
    state = np.zeros((4, 4), dtype=COMPLEX)
    for weight in weights:
        state += weight * np.kron(random_pure_qubit(rng), random_pure_qubit(rng))
    return state


def criterion_margin(p: float, gamma: float, criterion: str) -> float:
    values = evaluate(polarized_noise_state(p, gamma))
    if criterion == "devicente":
        return values.devicente_lhs - 1.0
    if criterion == "centered":
        return values.centered_lhs - values.centered_budget
    raise ValueError(f"unknown criterion: {criterion}")


def detection_threshold(gamma: float, criterion: str) -> float:
    if gamma <= 0.0 or criterion_margin(1.0, gamma, criterion) <= 0.0:
        return 1.0
    low, high = 0.0, 1.0
    for _ in range(70):
        midpoint = (low + high) / 2.0
        if criterion_margin(midpoint, gamma, criterion) > 0.0:
            high = midpoint
        else:
            low = midpoint
    return high


def validate(verbose: bool = True) -> None:
    tolerance = 2e-11

    for p in np.linspace(0.0, 1.0, 11):
        values = evaluate(classical_separable_state(float(p)))
        expected = 4.0 * p * (1.0 - p)
        if not np.isclose(values.centered_lhs, expected, atol=tolerance):
            raise AssertionError(f"separable LHS failed at p={p}")
        if not np.isclose(values.centered_budget, expected, atol=tolerance):
            raise AssertionError(f"separable budget failed at p={p}")

    for gamma in np.linspace(0.02, np.pi / 4.0, 11):
        values = evaluate(schmidt_state(float(gamma)))
        if not values.centered_lhs > values.centered_budget + tolerance:
            raise AssertionError(f"pure-state centered test failed at gamma={gamma}")
        if not values.devicente_lhs > 1.0 + tolerance:
            raise AssertionError(f"pure-state de Vicente test failed at gamma={gamma}")

    gamma = 0.5 * np.arcsin(0.6)
    values = evaluate(polarized_noise_state(0.45, gamma))
    if not np.isclose(values.devicente_lhs, 0.99, atol=tolerance):
        raise AssertionError("separating example de Vicente value failed")
    if not np.isclose(values.centered_lhs, 0.6624, atol=tolerance):
        raise AssertionError("separating example centered value failed")
    if not np.isclose(values.centered_budget, 0.3868097207, atol=tolerance):
        raise AssertionError("separating example budget failed")
    if not values.min_partial_transpose_eigenvalue < -tolerance:
        raise AssertionError("separating example should be NPT")
    rho = polarized_noise_state(0.45, gamma)
    rho_a, rho_b = reduced_states(rho)
    realigned_centered = nuclear_norm(realign(rho - np.kron(rho_a, rho_b)))
    if not np.isclose(realigned_centered, 0.5 * values.centered_lhs, atol=tolerance):
        raise AssertionError("realignment/Bloch normalization identity failed")

    centered_threshold = detection_threshold(gamma, "centered")
    devicente_threshold = detection_threshold(gamma, "devicente")
    if not np.isclose(centered_threshold, 0.1876104202, atol=2e-9):
        raise AssertionError("centered threshold failed")
    if not np.isclose(devicente_threshold, 5.0 / 11.0, atol=2e-9):
        raise AssertionError("de Vicente threshold failed")

    for p_value in np.linspace(0.0, 1.0, 11):
        if criterion_margin(float(p_value), 0.0, "centered") > tolerance:
            raise AssertionError("gamma=0 should not violate the centered criterion")
        if criterion_margin(float(p_value), 0.0, "devicente") > tolerance:
            raise AssertionError("gamma=0 should not violate de Vicente")
    near_zero = 1.0e-5
    if not np.isclose(
        detection_threshold(near_zero, "centered"), np.sqrt(5.0) - 2.0, atol=3e-6
    ):
        raise AssertionError("centered right-hand limit at gamma=0 failed")
    if not np.isclose(
        detection_threshold(near_zero, "devicente"), 1.0, atol=5e-5
    ):
        raise AssertionError("de Vicente right-hand limit at gamma=0 failed")

    low, high = 0.0, 1.0
    for _ in range(70):
        midpoint = (low + high) / 2.0
        sample = evaluate(zhang_false_negative_state(midpoint))
        if sample.centered_lhs > sample.centered_budget:
            high = midpoint
        else:
            low = midpoint
    if not np.isclose(high, 0.2209372712, atol=2e-9):
        raise AssertionError("Zhang false-negative threshold failed")
    missed = evaluate(zhang_false_negative_state(0.1))
    if not missed.min_partial_transpose_eigenvalue < -tolerance:
        raise AssertionError("false-negative example should be NPT")
    if not missed.centered_lhs <= missed.centered_budget + tolerance:
        raise AssertionError("centered test should miss the p=0.1 example")

    rng = np.random.default_rng(20260717)
    for index in range(20):
        weight = float(rng.random())
        state = weight * np.kron(random_pure_qubit(rng), random_pure_qubit(rng))
        state += (1.0 - weight) * np.kron(
            random_pure_qubit(rng), random_pure_qubit(rng)
        )
        sample = evaluate(state)
        if not np.isclose(sample.centered_lhs, sample.centered_budget, atol=2e-10):
            raise AssertionError(f"two-term saturation check failed at {index}")

    for index in range(50):
        sample = evaluate(random_separable_state(rng))
        if sample.centered_lhs > sample.centered_budget + 2e-10:
            raise AssertionError(f"random separable centered check failed at {index}")
        if sample.min_partial_transpose_eigenvalue < -2e-10:
            raise AssertionError(f"random separable PPT check failed at {index}")

    if verbose:
        print("11 separable saturation checks passed")
        print("11 pure entangled-state checks passed")
        print("separating family and detection thresholds passed")
        print("gamma=0 endpoint and right-hand limits passed")
        print("Zhang false-negative threshold passed")
        print("20 random two-term saturation checks passed")
        print("50 random separable-state checks passed")


def detection_curves() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # The exact endpoint gamma=0 is separable for every p.  The plotted curves
    # describe the entangled interior gamma>0, so we sample strictly inside it.
    gamma_radians = np.linspace(np.pi / 720.0, np.pi / 4.0, 180)
    centered = np.array(
        [detection_threshold(value, "centered") for value in gamma_radians]
    )
    devicente = np.array(
        [detection_threshold(value, "devicente") for value in gamma_radians]
    )
    return gamma_radians, centered, devicente


def write_csv_file(
    path: Path,
    gamma_radians: np.ndarray,
    centered: np.ndarray,
    devicente: np.ndarray,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["gamma_radians", "centered_detection_threshold", "devicente_threshold"]
        )
        for row in zip(gamma_radians, centered, devicente, strict=True):
            writer.writerow([f"{value:.10f}" for value in row])


def points(
    x_values: np.ndarray,
    y_values: np.ndarray,
    x_map,
    y_map,
) -> str:
    return " ".join(
        f"{x_map(float(x)):.2f},{y_map(float(y)):.2f}"
        for x, y in zip(x_values, y_values, strict=True)
    )


def write_svg_file(
    path: Path,
    gamma_radians: np.ndarray,
    centered: np.ndarray,
    devicente: np.ndarray,
) -> None:
    width, height = 1100, 700
    left, right, top, bottom = 100, 45, 65, 100
    plot_width = width - left - right
    plot_height = height - top - bottom
    x_map = lambda value: left + plot_width * value / (np.pi / 4.0)
    y_map = lambda value: top + plot_height * (1.0 - value)

    # These are right-hand limits as gamma approaches the separable axis.
    # Open endpoints keep them visually distinct from values at gamma=0.
    plot_gamma = np.concatenate(([0.0], gamma_radians))
    plot_centered = np.concatenate(([np.sqrt(5.0) - 2.0], centered))
    plot_devicente = np.concatenate(([1.0], devicente))

    lower_polygon = (
        f"{x_map(0):.2f},{y_map(0):.2f} "
        f"{x_map(np.pi / 4):.2f},{y_map(0):.2f} "
        + points(plot_gamma[::-1], plot_centered[::-1], x_map, y_map)
    )
    middle_polygon = points(plot_gamma, plot_centered, x_map, y_map) + " " + points(
        plot_gamma[::-1], plot_devicente[::-1], x_map, y_map
    )
    upper_polygon = (
        points(plot_gamma, plot_devicente, x_map, y_map)
        + f" {x_map(np.pi / 4):.2f},{y_map(1):.2f} {x_map(0):.2f},{y_map(1):.2f}"
    )
    centered_line = points(plot_gamma, plot_centered, x_map, y_map)
    devicente_line = points(plot_gamma, plot_devicente, x_map, y_map)

    grid = []
    labels = []
    for p_value in np.linspace(0.0, 1.0, 6):
        y = y_map(float(p_value))
        grid.append(f'<line class="grid" x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}"/>')
        labels.append(f'<text class="tick" x="{left-18}" y="{y+6:.2f}" text-anchor="end">{p_value:.1f}</text>')
    gamma_ticks = (
        (0.0, "0"),
        (np.pi / 12.0, "π/12"),
        (np.pi / 6.0, "π/6"),
        (np.pi / 4.0, "π/4"),
    )
    for gamma_value, gamma_label in gamma_ticks:
        x = x_map(float(gamma_value))
        grid.append(f'<line class="grid" x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{height-bottom}"/>')
        labels.append(f'<text class="math-tick" x="{x:.2f}" y="{height-bottom+32}" text-anchor="middle">{gamma_label}</text>')

    example_gamma = float(0.5 * np.arcsin(0.6))
    example_x = x_map(example_gamma)
    example_y = y_map(0.45)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Detection regions for the polarized-noise two-qubit family</title>
  <desc id="desc">For positive p and gamma the family is NPT entangled. The lower grey region is missed by both norm tests, the middle light teal region is detected only by the centered criterion, and the upper dark teal region is detected by both the centered and de Vicente criteria. The colored regions show right-hand limits near gamma zero; the exact gamma-zero axis is separable and is drawn separately. A marked example at gamma equal to one half arcsine of three fifths and p equal to 0.45 is detected only by centering.</desc>
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <style>
    .axis {{ stroke: #172033; stroke-width: 2.4; }}
    .grid {{ stroke: #c9d1da; stroke-width: 1; }}
    .tick {{ font: 18px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #435064; }}
    .math-tick {{ font: 19px Georgia, "Times New Roman", serif; fill: #435064; }}
    .label {{ font: 22px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #172033; }}
    .region {{ font: 600 21px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .small {{ font: 17px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #526173; }}
    .boundary-centered {{ font: 17px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #a33b20; }}
    .boundary-devicente {{ font: 17px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #172033; }}
    .annotation {{ font: 17px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #ffffff; }}
  </style>
  <polygon points="{lower_polygon}" fill="#eef1f4"/>
  <polygon points="{middle_polygon}" fill="#b9e1df"/>
  <polygon points="{upper_polygon}" fill="#087f8c"/>
  {''.join(grid)}
  <polyline points="{centered_line}" fill="none" stroke="#a33b20" stroke-width="4"/>
  <polyline points="{devicente_line}" fill="none" stroke="#172033" stroke-width="4"/>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#ffffff" stroke-width="9"/>
  <line class="axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}"/>
  <line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}"/>
  <circle cx="{x_map(0):.2f}" cy="{y_map(np.sqrt(5.0)-2.0):.2f}" r="6" fill="#ffffff" stroke="#a33b20" stroke-width="3"/>
  <circle cx="{x_map(0):.2f}" cy="{y_map(1.0):.2f}" r="6" fill="#ffffff" stroke="#172033" stroke-width="3"/>
  {''.join(labels)}
  <text class="label" x="{(left+width-right)/2:.2f}" y="{height-28}" text-anchor="middle">Schmidt angle γ (radians)</text>
  <text class="label" transform="translate(30 {(top+height-bottom)/2:.2f}) rotate(-90)" text-anchor="middle">mixture weight p</text>
  <text class="region" x="{x_map(np.deg2rad(31)):.2f}" y="{y_map(0.78):.2f}" text-anchor="middle" fill="#ffffff">detected by both</text>
  <text class="region" x="{x_map(np.deg2rad(30)):.2f}" y="{y_map(0.31):.2f}" text-anchor="middle" fill="#172033">centered criterion only</text>
  <text class="region" x="{x_map(np.deg2rad(31)):.2f}" y="{y_map(0.08):.2f}" text-anchor="middle" fill="#526173">NPT, neither test detects</text>
  <text class="boundary-centered" x="{x_map(np.deg2rad(43)):.2f}" y="{y_map(float(centered[-9]))-14:.2f}" text-anchor="end">centered boundary</text>
  <text class="boundary-devicente" x="{x_map(np.deg2rad(43)):.2f}" y="{y_map(float(devicente[-9]))-14:.2f}" text-anchor="end">de Vicente boundary</text>
  <circle cx="{example_x:.2f}" cy="{example_y:.2f}" r="8" fill="#ffffff" stroke="#a33b20" stroke-width="4"/>
  <path d="M {example_x+10:.2f} {example_y-6:.2f} L {example_x+90:.2f} {example_y-70:.2f}" fill="none" stroke="#a33b20" stroke-width="2"/>
  <text class="annotation" x="{example_x+96:.2f}" y="{example_y-76:.2f}">example: p=0.45, γ=½ arcsin(3/5)</text>
</svg>'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")


def write_artifacts(repository_root: Path) -> None:
    gamma_radians, centered, devicente = detection_curves()
    write_csv_file(
        repository_root / "assets/data/centered-detection-regions.csv",
        gamma_radians,
        centered,
        devicente,
    )
    write_svg_file(
        repository_root / "assets/images/centered-detection-regions.svg",
        gamma_radians,
        centered,
        devicente,
    )
    print("wrote centered-detection-regions.csv")
    print("wrote centered-detection-regions.svg")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-artifacts",
        action="store_true",
        help="write the CSV and SVG used by the article",
    )
    parser.add_argument(
        "--matrix",
        type=Path,
        help="load a 4 x 4 two-qubit density matrix from a NumPy .npy file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate(verbose=args.matrix is None or args.write_artifacts)
    if args.matrix is not None:
        print_report(np.asarray(np.load(args.matrix), dtype=COMPLEX))
    if args.write_artifacts:
        repository_root = Path(__file__).resolve().parents[2]
        write_artifacts(repository_root)


if __name__ == "__main__":
    main()
