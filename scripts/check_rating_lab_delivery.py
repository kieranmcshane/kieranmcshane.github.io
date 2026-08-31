#!/usr/bin/env python3
"""Fail when the public Rating Lab regresses to a stale or empty delivery.

The request is deliberately cache-busted and asks every intermediary to
revalidate. This checks delivered HTML, the public manifest, and each sport's
split predictor core, not repository source or a successful Pages deployment
step.
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

FORECAST_GRACE_DAYS = 1
BLOCKING_FORECAST_FORMATS = {
    "tennis knockout draw",
    "knockout cup",
    "two-legged qualifying round",
    "round-robin league",
    "round-robin tournament",
}


class DeliveryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_ranking_table = False
        self.static_rows = 0
        self.evidence_rows = 0
        self._in_evidence_body = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "table" and attributes.get("id") == "ranking-table":
            self.in_ranking_table = True
        if tag == "table" and "rating-lab-evidence-table" in classes:
            self._in_evidence_body = True
        if (
            tag == "tr"
            and self.in_ranking_table
            and attributes.get("data-static-default") == "true"
        ):
            self.static_rows += 1
        if tag == "tr" and self._in_evidence_body:
            self.evidence_rows += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "table" and self.in_ranking_table:
            self.in_ranking_table = False
        elif tag == "table" and self._in_evidence_body:
            self._in_evidence_body = False


def fetch(url: str) -> bytes:
    parts = urlsplit(url)
    query = f"{parts.query}&" if parts.query else ""
    query += f"verify={time.time_ns()}"
    cache_busted = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, query, parts.fragment)
    )
    request = Request(
        cache_busted,
        headers={
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "User-Agent": "rating-lab-delivery-check/1.0",
        },
    )
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return response.read()


def _date_value(value: object) -> date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def competition_temporal_failures(
    payload: dict,
    *,
    as_of: date | None = None,
) -> list[str]:
    """Return unsafe competition-forecast delivery contradictions."""
    failures: list[str] = []
    reference_date = as_of or datetime.now(timezone.utc).date()
    predictor = payload.get("tournament_predictor") or {}
    for competition in predictor.get("competitions") or []:
        competition_id = (
            competition.get("id") or competition.get("label") or "unknown competition"
        )
        lifecycle = competition.get("state") or competition.get("status") or "upcoming"
        lifecycle = {"complete": "finished", "scheduled": "upcoming"}.get(
            lifecycle, lifecycle
        )
        health = competition.get("source_health")
        completed = competition.get("completed_matches")
        total = competition.get("total_matches")
        try:
            remaining = max(int(competition.get("remaining_matches", 0)), 0)
        except (TypeError, ValueError):
            remaining = 0
        try:
            grace_days = max(
                int(competition.get("forecast_grace_days", FORECAST_GRACE_DAYS)),
                0,
            )
        except (TypeError, ValueError):
            grace_days = FORECAST_GRACE_DAYS
        last_fixture = _date_value(competition.get("last_fixture"))
        next_fixture = _date_value(competition.get("next_fixture"))
        overdue = (
            lifecycle != "finished"
            and remaining > 0
            and (
                bool(
                    last_fixture
                    and reference_date > last_fixture + timedelta(days=grace_days)
                )
                or bool(
                    competition.get("format") in BLOCKING_FORECAST_FORMATS
                    and next_fixture
                    and reference_date > next_fixture + timedelta(days=grace_days)
                )
            )
        )

        if lifecycle not in {"upcoming", "live", "finished"}:
            failures.append(f"{competition_id} has a non-canonical lifecycle")
        if competition.get("status") != competition.get("state"):
            failures.append(f"{competition_id} lifecycle aliases disagree")
        if (
            not isinstance(completed, int)
            or not isinstance(competition.get("remaining_matches"), int)
            or not isinstance(total, int)
            or completed < 0
            or remaining < 0
            or completed + remaining != total
        ):
            failures.append(f"{competition_id} result counts do not reconcile")
        if health not in {"current", "delayed", "incomplete"}:
            failures.append(f"{competition_id} has no valid source-health verdict")
        if not competition.get("source_health_reason"):
            failures.append(f"{competition_id} has no source-health explanation")
        forecast_as_of = _date_value(competition.get("forecast_as_of"))
        if not forecast_as_of:
            failures.append(f"{competition_id} has no valid forecast as-of date")
        elif forecast_as_of > reference_date:
            failures.append(f"{competition_id} has a future forecast as-of date")
        if not competition.get("forecast_checked_at"):
            failures.append(f"{competition_id} has no source-check timestamp")
        if overdue and health != "delayed":
            failures.append(
                f"{competition_id} is overdue but is not marked source delayed"
            )

        must_withhold = overdue or health in {"delayed", "incomplete"}
        if must_withhold:
            if competition.get("forecast_available") is not False:
                failures.append(
                    f"{competition_id} publishes an available forecast from a non-current source"
                )
            if competition.get("models"):
                failures.append(
                    f"{competition_id} publishes model probabilities from a non-current source"
                )
            if competition.get("settled_performance") or competition.get("performance"):
                failures.append(
                    f"{competition_id} publishes performance analysis from a non-current source"
                )
            if competition.get("state_view") != "forecast_withheld":
                failures.append(
                    f"{competition_id} does not expose the fail-closed forecast view"
                )
        elif competition.get("forecast_available") is False:
            failures.append(
                f"{competition_id} claims a current source for an unavailable forecast"
            )
        elif competition.get("forecast_available") and not competition.get("models"):
            failures.append(
                f"{competition_id} has an available forecast without models"
            )
        if lifecycle == "finished" and competition.get("next_fixture") is not None:
            failures.append(
                f"{competition_id} is finished but still exposes a next fixture"
            )
    return failures


def check(page_url: str) -> list[str]:
    failures = []
    html = fetch(page_url).decode("utf-8")
    parser = DeliveryParser()
    parser.feed(html)
    if parser.static_rows < 50:
        failures.append(
            f"server-rendered leaderboard has {parser.static_rows} rows; expected 50"
        )
    if parser.evidence_rows < 5:  # header plus four cohorts
        failures.append("server-rendered per-cohort accuracy evidence is incomplete")
    forbidden = (
        "requires JavaScript",
        "Loading current rating state",
        "Loading cohort rules",
        "Weighted across published cohorts",
    )
    for phrase in forbidden:
        if phrase in html:
            failures.append(f"delivered HTML still contains {phrase!r}")
    if "sports are never pooled" not in html:
        failures.append("headline does not explicitly prohibit cross-sport pooling")

    manifest_url = urljoin(page_url, "../assets/data/rating-lab/manifest.json")
    manifest = json.loads(fetch(manifest_url))
    for sport, status in manifest.get("sports", {}).items():
        message = str(status.get("message") or "")
        if re.fullmatch(r"'[^']+'", message):
            failures.append(f"{sport} exposes a raw exception key: {message}")
        if (
            status.get("status") == "retained"
            and "last validated" not in message.lower()
        ):
            failures.append(f"{sport} retained status lacks an intelligible warning")
        core_url = urljoin(
            page_url,
            f"../assets/data/rating-lab/split/{sport}-core.json",
        )
        core = json.loads(fetch(core_url))
        failures.extend(
            f"{sport}: {failure}" for failure in competition_temporal_failures(core)
        )
    media_url = urljoin(
        page_url,
        "../assets/data/rating-lab/split/media-index.json",
    )
    media = json.loads(fetch(media_url)).get("entities", {})
    if len(media) < 100:
        failures.append(
            f"verified media registry has {len(media)} entities; expected at least 100"
        )
    if "atp:s0ag" not in media:
        failures.append("verified media registry is missing the default #1 tennis row")
    return failures


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_rating_lab_delivery.py PAGE_URL", file=sys.stderr)
        return 2
    failures = []
    for attempt in range(6):
        try:
            failures = check(sys.argv[1])
        except Exception as error:
            failures = [f"delivery request failed: {error}"]
        if not failures:
            print("Rating Lab delivery check passed.")
            return 0
        if attempt < 5:
            time.sleep(10)
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
