#!/usr/bin/env python3
"""Generate the density comparison used in the X-ENS correction."""

from __future__ import annotations

import math
from pathlib import Path


WIDTH = 1200
HEIGHT = 590
LEFT = 94
RIGHT = 1150
TOP = 82
BOTTOM = 510
Y_MAX = 0.65

INK = "#172033"
MUTED = "#5d6778"
GRID = "#d9dee8"
ARC = "#3157c8"
SEMICIRCLE = "#b3541e"
BACKGROUND = "#fdfdfd"


def x_pixel(x: float) -> float:
    return LEFT + (x + 2.0) / 4.0 * (RIGHT - LEFT)


def y_pixel(y: float) -> float:
    """Map an unclipped density value; the SVG clip path trims the excess."""
    return BOTTOM - max(y, 0.0) / Y_MAX * (BOTTOM - TOP)


def path_for(function, samples: int = 640) -> str:
    points = []
    for index in range(samples + 1):
        x = -1.999 + 3.998 * index / samples
        points.append((x_pixel(x), y_pixel(function(x))))
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
    for value in [0.0, 0.15, 0.30, 0.45, 0.60]:
        y = y_pixel(value)
        horizontal_grid.extend(
            [
                f'<line x1="{LEFT}" y1="{y:.2f}" x2="{RIGHT}" y2="{y:.2f}" '
                f'stroke="{GRID}" stroke-width="1" />',
                f'<text x="{LEFT - 15}" y="{y + 5:.2f}" text-anchor="end" '
                f'class="tick">{value:g}</text>',
            ]
        )

    x_axis = []
    for value in [-2, -1, 0, 1, 2]:
        x = x_pixel(value)
        x_axis.extend(
            [
                f'<line x1="{x:.2f}" y1="{BOTTOM}" x2="{x:.2f}" y2="{BOTTOM + 7}" '
                f'stroke="{INK}" stroke-width="1.5" />',
                f'<text x="{x:.2f}" y="{BOTTOM + 31}" text-anchor="middle" '
                f'class="tick">{value}</text>',
            ]
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">Arcsine and semicircle densities on the same axes</title>
  <desc id="desc">The solid blue arcsine density is U-shaped and leaves the plot at both endpoints because it diverges. The dashed rust semicircle density peaks at zero and vanishes at both endpoints.</desc>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}" />
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: {INK}; letter-spacing: 0; }}
    .tick {{ font-size: 16px; fill: {MUTED}; }}
    .legend {{ font-size: 17px; font-weight: 650; }}
    .legend-note {{ font-size: 15px; fill: {MUTED}; }}
  </style>
  <defs>
    <clipPath id="plot-clip"><rect x="{LEFT}" y="{TOP}" width="{RIGHT - LEFT}" height="{BOTTOM - TOP}" /></clipPath>
  </defs>

  <line x1="{LEFT}" y1="36" x2="{LEFT + 48}" y2="36" stroke="{ARC}" stroke-width="4" stroke-linecap="round" />
  <text x="{LEFT + 61}" y="42" class="legend">Arcsine</text>
  <text x="{LEFT + 137}" y="42" class="legend-note">diverges at ±2</text>

  <line x1="{LEFT + 330}" y1="36" x2="{LEFT + 378}" y2="36" stroke="{SEMICIRCLE}" stroke-width="4" stroke-dasharray="12 8" stroke-linecap="round" />
  <text x="{LEFT + 391}" y="42" class="legend">Semicircle</text>
  <text x="{RIGHT}" y="42" text-anchor="end" class="legend-note">same horizontal and vertical scales</text>

  {''.join(horizontal_grid)}
  <line x1="{LEFT}" y1="{BOTTOM}" x2="{RIGHT}" y2="{BOTTOM}" stroke="{INK}" stroke-width="1.8" />
  <line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{BOTTOM}" stroke="{INK}" stroke-width="1.8" />
  {''.join(x_axis)}
  <text x="{(LEFT + RIGHT) / 2:.2f}" y="{BOTTOM + 65}" text-anchor="middle" class="tick">x</text>
  <text x="28" y="{(TOP + BOTTOM) / 2:.2f}" text-anchor="middle" class="tick" transform="rotate(-90 28 {(TOP + BOTTOM) / 2:.2f})">density</text>

  <g clip-path="url(#plot-clip)">
    <path d="{path_for(arcsine)}" fill="none" stroke="{ARC}" stroke-width="4" stroke-linecap="round" />
    <path d="{path_for(semicircle)}" fill="none" stroke="{SEMICIRCLE}" stroke-width="4" stroke-dasharray="12 8" stroke-linecap="round" />
  </g>
</svg>
'''


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "images" / "arcsine-semicircle-comparison.svg"
    output.write_text(build_svg(), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
