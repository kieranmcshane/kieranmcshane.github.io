#!/usr/bin/env python3
"""Rebuild the public Polymarket/Kalshi paper-trading audit."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rating_lab.market_audit import write_market_strategy_report  # noqa: E402


def _download_public_payloads(base_url: str, destination: Path) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "https":
        raise ValueError("--public-base must be an HTTPS URL")
    for sport in ("tennis", "football", "national-football", "chess"):
        request = Request(
            f"{base_url.rstrip('/')}/{sport}.json",
            headers={
                "User-Agent": "rating-lab-market-strategy-auditor/1.0",
                "Cache-Control": "no-cache",
            },
        )
        with urlopen(request, timeout=60) as response:
            (destination / f"{sport}.json").write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "assets" / "data" / "rating-lab",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "assets" / "data" / "rating-lab" / "audit" / "market-strategy-report.json",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero unless every embedded provider ledger reproduces exactly.",
    )
    parser.add_argument(
        "--public-base",
        help=(
            "Download deployed sport JSON before auditing, for example "
            "https://kieranmcshane.github.io/assets/data/rating-lab"
        ),
    )
    args = parser.parse_args()
    temporary = tempfile.TemporaryDirectory(prefix="rating-lab-market-audit-")
    try:
        data_dir = args.data_dir
        if args.public_base:
            data_dir = Path(temporary.name)
            _download_public_payloads(args.public_base, data_dir)
        report = write_market_strategy_report(data_dir, args.output)
    finally:
        temporary.cleanup()
    print(
        f"market strategy audit: {report['status']} · "
        f"{len(report['audits'])} provider/sport ledgers "
        f"({report['audit_sha256'][:12]})"
    )
    return 1 if args.strict and report["status"] != "pass" else 0


if __name__ == "__main__":
    raise SystemExit(main())
