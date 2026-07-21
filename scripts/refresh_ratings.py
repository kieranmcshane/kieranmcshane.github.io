#!/usr/bin/env python3
"""Refresh Rating Lab static JSON from public data sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rating_lab.pipeline import _get, write_outputs  # noqa: E402
from rating_lab.player_pipeline import (  # noqa: E402
    build_player_payload,
    player_schema,
    validate_player_payload,
)


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
    parser.add_argument("--players-only", action="store_true", help="Refresh only historical football-player cohorts")
    args = parser.parse_args()
    if args.players_only:
        args.output.mkdir(parents=True, exist_ok=True)
        payload = build_player_payload(_get)
        validate_player_payload(payload)
        (args.output / "player-football.json").write_text(
            json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n"
        )
        (args.output / "player-schema.json").write_text(json.dumps(player_schema(), indent=2) + "\n")
        print(
            "player-football: current ("
            + ", ".join(f"{cohort['name']}: {cohort['matches']} matches" for cohort in payload["cohorts"])
            + ")"
        )
        return 0
    manifest = write_outputs(args.output, args.sports, chess_months=args.chess_months)
    for sport, status in manifest["sports"].items():
        print(f"{sport}: {status['status']} ({status['latest_result']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
