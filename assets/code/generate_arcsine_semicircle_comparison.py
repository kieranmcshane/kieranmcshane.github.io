#!/usr/bin/env python3
"""Generate the density comparison used in the X-ENS correction."""

from __future__ import annotations

import math
from pathlib import Path


WIDTH = 1200
HEIGHT = 650
LEFT = 92
RIGHT = 1130
TOP = 118
BOTTOM = 535
Y_MAX = 1.05

INK = "#172033"
MUTED = "#5d6778"
GRID = "#d9dee8"
ARC = "#3157c8"
SEMICIRCLE = "#b3541e"
BACKGROUND = "#fdfdfd"


def x_pixel(x: float) -> float:
    return LEFT + (x + 2.0) / 4.0 * (RIGHT - LEFT)


def y_pixel(y: float) -> float:
    clipped = min(max(y, 0.0), Y_MAX)
    return BOTTOM - clipped / Y_MAX * (BOTTOM - TOP)


def path_for(function, samples: int = 480) -> str:
    points = []
    for index in range(samples + 1):
        x = -1.999 + 3.998 * index / samples
        y = function(x)
        points.append((x_pixel(x), y_pixel(y)))
    return " ".join(
        ("M" if index == 0 else "L") + f" {x:.2f} {y:.2f}"
        for index, (x, y) in enumerate(points)
    )


def arcsine(x: float) -> float:
    return 1.0 / (math.pi * math.sqrt(4.0 - x * x))


def semicircle(x: float) -> float:
    return math.sqrt(4.0 - x * x) / (2.0 * math.pi)


def build_svg() -> str:
    horizontal_grid = []
    y_ticks = [0.0, 0.25, 0.5, 0.75, 1.0]
    for value in y_ticks:
        y = y_pixel(value)
        horizontal_grid.append(
            f'<line x1="{LEFT}" y1="{y:.2f}" x2="{RIGHT}" y2="{y:.2f}" '
            f'stroke="{GRID}" stroke-width="1" />'
        )
        horizontal_grid.append(
            f'<text x="{LEFT - 16}" y="{y + 5:.2f}" text-anchor="end" '
            f'class="tick">{value:g}</text>'
        )

    x_axis = []
    for value in [-2, -1, 0, 1, 2]:
        x = x_pixel(value)
        x_axis.append(
            f'<line x1="{x:.2f}" y1="{BOTTOM}" x2="{x:.2f}" y2="{BOTTOM + 8}" '
            f'stroke="{INK}" stroke-width="1.5" />'
        )
        x_axis.append(
            f'<text x="{x:.2f}" y="{BOTTOM + 32}" text-anchor="middle" '
            f'class="tick">{value}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">Arcsine and semicircle densities on the interval from minus two to two</title>
  <desc id="desc">The arcsine density is U-shaped and diverges at both endpoints. The semicircle density is largest at zero and vanishes at both endpoints.</desc>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}" />
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: {INK}; letter-spacing: 0; }}
    .title {{ font-size: 30px; font-weight: 700; }}
    .subtitle {{ font-size: 18px; fill: {MUTED}; }}
    .tick {{ font-size: 16px; fill: {MUTED}; }}
    .label {{ font-size: 20px; font-weight: 700; paint-order: stroke; stroke: {BACKGROUND}; stroke-width: 6px; stroke-linejoin: round; }}
    .arc-label {{ fill: {ARC}; }}
    .semicircle-label {{ fill: {SEMICIRCLE}; }}
    .note {{ font-size: 16px; fill: {MUTED}; }}
  </style>
  <defs>
    <clipPath id="plot-clip"><rect x="{LEFT}" y="{TOP}" width="{RIGHT - LEFT}" height="{BOTTOM - TOP}" /></clipPath>
    <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <path d="M0,8 L4,0 L8,8" fill="none" stroke="{ARC}" stroke-width="1.6" />
    </marker>
  </defs>

  <text x="{LEFT}" y="48" class="title">Two limiting spectral densities on the same support</text>
  <text x="{LEFT}" y="78" class="subtitle">Arcsine puts more mass near the edges; semicircle puts more mass in the bulk.</text>

  {''.join(horizontal_grid)}
  <line x1="{LEFT}" y1="{BOTTOM}" x2="{RIGHT}" y2="{BOTTOM}" stroke="{INK}" stroke-width="1.8" />
  <line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{BOTTOM}" stroke="{INK}" stroke-width="1.8" />
  {''.join(x_axis)}
  <text x="{(LEFT + RIGHT) / 2:.2f}" y="{BOTTOM + 66}" text-anchor="middle" class="tick">x</text>
  <text x="28" y="{(TOP + BOTTOM) / 2:.2f}" text-anchor="middle" class="tick" transform="rotate(-90 28 {(TOP + BOTTOM) / 2:.2f})">density</text>

  <g clip-path="url(#plot-clip)">
    <path d="{path_for(arcsine)}" fill="none" stroke="{ARC}" stroke-width="4" stroke-linecap="round" />
    <path d="{path_for(semicircle)}" fill="none" stroke="{SEMICIRCLE}" stroke-width="4" stroke-dasharray="12 8" stroke-linecap="round" />
  </g>

  <line x1="{x_pixel(-1.94):.2f}" y1="{TOP + 45}" x2="{x_pixel(-1.94):.2f}" y2="{TOP + 6}" stroke="{ARC}" stroke-width="3" marker-end="url(#arrow-blue)" />
  <line x1="{x_pixel(1.94):.2f}" y1="{TOP + 45}" x2="{x_pixel(1.94):.2f}" y2="{TOP + 6}" stroke="{ARC}" stroke-width="3" marker-end="url(#arrow-blue)" />
  <text x="{x_pixel(-1.73):.2f}" y="{TOP + 42}" class="note" fill="{ARC}">diverges</text>
  <text x="{x_pixel(1.73):.2f}" y="{TOP + 42}" text-anchor="end" class="note" fill="{ARC}">diverges</text>

  <text x="{x_pixel(-0.82):.2f}" y="{y_pixel(arcsine(-0.82)) + 48:.2f}" class="label arc-label">arcsine</text>
  <line x1="{x_pixel(-0.58):.2f}" y1="{y_pixel(arcsine(-0.82)) + 34:.2f}" x2="{x_pixel(-0.35):.2f}" y2="{y_pixel(arcsine(-0.35)) + 3:.2f}" stroke="{ARC}" stroke-width="3" />
  <text x="{x_pixel(0.45):.2f}" y="{y_pixel(semicircle(0.45)) - 24:.2f}" class="label semicircle-label">semicircle</text>
  <line x1="{x_pixel(0.45):.2f}" y1="{y_pixel(semicircle(0.45)) - 15:.2f}" x2="{x_pixel(1.05):.2f}" y2="{y_pixel(semicircle(1.05)) - 2:.2f}" stroke="{SEMICIRCLE}" stroke-width="3" stroke-dasharray="10 7" />

  <text x="{LEFT}" y="{HEIGHT - 24}" class="note">The arcsine curve is clipped vertically; its density tends to infinity as x approaches either endpoint.</text>
</svg>
'''


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "images" / "arcsine-semicircle-comparison.svg"
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
