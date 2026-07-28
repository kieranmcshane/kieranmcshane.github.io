#!/usr/bin/env python3
"""Fail when the public Rating Lab regresses to a stale or empty delivery.

The request is deliberately cache-busted and asks every intermediary to
revalidate. This checks delivered HTML and the public manifest, not repository
source or a successful Pages deployment step.
"""

from __future__ import annotations

import json
from html.parser import HTMLParser
import re
import sys
import time
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


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
        if tag == "tr" and self.in_ranking_table and attributes.get(
            "data-static-default"
        ) == "true":
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
        if status.get("status") == "retained" and "last validated" not in message.lower():
            failures.append(f"{sport} retained status lacks an intelligible warning")
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
