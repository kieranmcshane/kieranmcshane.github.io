#!/usr/bin/env python3
"""Re-run Rating Lab audits from the frozen public replay packets."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rating_lab.audit import write_report  # noqa: E402


def _git_revision() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _download_public_audit(base_url: str, destination: Path) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "https":
        raise ValueError("--public-base must be an HTTPS URL")
    root = base_url.rstrip("/")
    files = [
        "manifest.json",
        *[f"{sport}.json" for sport in ("tennis", "football", "national-football", "chess")],
        *[
            f"audit/{sport}-replay.json.gz"
            for sport in ("tennis", "football", "national-football", "chess")
        ],
    ]
    for name in files:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        request = Request(
            f"{root}/{name}",
            headers={
                "User-Agent": "rating-lab-model-auditor/1.0",
                "Cache-Control": "no-cache",
            },
        )
        with urlopen(request, timeout=60) as response:
            target.write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "assets" / "data" / "rating-lab",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Defaults to <data-dir>/audit/report.json",
    )
    parser.add_argument(
        "--artifact-only",
        action="store_true",
        help="Verify hashes and recompute metrics without rerunning candidate grids.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero unless every sport passes.",
    )
    parser.add_argument(
        "--public-base",
        help=(
            "Download the deployed sport JSON and frozen packets before auditing, "
            "for example https://kieranmcshane.github.io/assets/data/rating-lab"
        ),
    )
    args = parser.parse_args()
    temporary = tempfile.TemporaryDirectory(prefix="rating-lab-public-audit-")
    try:
        data_dir = Path(temporary.name) if args.public_base else args.data_dir
        if args.public_base:
            _download_public_audit(args.public_base, data_dir)
        report = write_report(
            data_dir,
            report_path=args.report,
            full_replay=not args.artifact_only,
            auditor_revision=_git_revision(),
        )
    finally:
        temporary.cleanup()
    print(
        f"model audit: {report['status']} "
        f"({report['verification_level']}; {len(report['sports'])} sports)"
    )
    for sport in report["sports"]:
        passed = sum(check["passed"] for check in sport["checks"])
        print(
            f"{sport['sport']}: {sport['status']} "
            f"({passed}/{len(sport['checks'])} checks)"
        )
    return 1 if args.strict and report["status"] != "pass" else 0


if __name__ == "__main__":
    raise SystemExit(main())
