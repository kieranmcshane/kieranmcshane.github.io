#!/usr/bin/env python3
"""Refresh Rating Lab static JSON from public data sources."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rating_lab.pipeline import write_outputs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sports",
        nargs="+",
        choices=("tennis", "football", "national-football", "chess"),
        default=["tennis", "football", "national-football", "chess"],
    )
    parser.add_argument("--output", type=Path, default=ROOT / "assets/data/rating-lab")
    parser.add_argument("--chess-months", type=int, default=36)
    args = parser.parse_args()
    manifest = write_outputs(args.output, args.sports, chess_months=args.chess_months)
    for sport, status in manifest["sports"].items():
        print(f"{sport}: {status['status']} ({status['latest_result']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
