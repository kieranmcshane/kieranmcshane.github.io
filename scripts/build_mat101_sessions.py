#!/usr/bin/env python3
"""Build the public, student-facing MAT101 session collection.

Only two explicitly public sources are parsed: the student workbook for lesson
content and the provisional schedule for dates. Instructor notes and assessment
keys are deliberately outside this data path.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / "_mat101_sessions"
DATA_FILE = ROOT / "_data" / "mat101_sessions.json"

SESSION_SLUGS = {
    1: "forme-algebrique",
    2: "conjugue-module-quotient",
    3: "formes-trigonometrique-exponentielle",
    4: "produits-puissances-moivre-euler",
    5: "polynomes-racines-parametres",
    6: "logique-et-racines-carrees-complexes",
    7: "equations-second-degre",
    8: "racines-niemes-unite",
    9: "geometrie-redaction-synthese",
    10: "ensembles-appartenance-inclusion",
    11: "operations-lois-ensemblistes",
    12: "familles-produits-traduction",
    13: "assertions-variables",
    14: "connecteurs-tables-verite",
    15: "quantificateurs-negations",
    16: "implication-preuve-directe",
    17: "contraposee-absurde-cas",
    18: "recurrence",
    19: "analyse-synthese-revision",
}

HEADING_IDS = {
    "À savoir faire": "competences",
    "Parcours": "parcours",
    "Activité": "activite",
    "Contrôle rapide": "controle",
    "Contrôle formatif": "controle",
    "Révision mixte": "revision",
    "Ticket": "ticket",
}
REQUIRED_HEADINGS = {"À savoir faire", "Parcours", "Ticket"}
FORBIDDEN_PUBLIC_MARKERS = (
    "fiche enseignant",
    "réponses et corrections",
    "préparation matérielle",
    "déroulé minute par minute",
    "plan de tableau",
    "erreurs fréquentes",
    "après la séance",
    "correction complète",
    "passation",
    "mock-cc1-key",
    "quiz-a-complexes-base-key",
    "quiz-b-complexes-synthese-key",
    "quiz-c-ensembles-logique-key",
)


def yaml_string(value: str) -> str:
    """Return a JSON string, which is also a valid YAML scalar."""

    return json.dumps(value, ensure_ascii=False)


def plain_text(value: str) -> str:
    """Remove the small Markdown subset used by the workbook."""

    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = value.replace("**", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def assert_student_safe(value: str, context: str) -> None:
    normalized = value.casefold()
    for marker in FORBIDDEN_PUBLIC_MARKERS:
        if marker.casefold() in normalized:
            raise ValueError(f"{context}: forbidden public marker {marker!r}")


def parse_workbook(text: str) -> list[dict[str, object]]:
    """Parse and allow-list the nineteen student workbook sections."""

    session_matches = list(
        re.finditer(r"^## Séance (\d+) — (.+?)\s*$", text, re.MULTILINE)
    )
    numbers = [int(match.group(1)) for match in session_matches]
    if numbers != list(range(1, 20)):
        raise ValueError("student workbook must contain ordered sessions 1..19")

    sessions: list[dict[str, object]] = []
    for index, match in enumerate(session_matches):
        number = int(match.group(1))
        title = match.group(2).strip()
        end = (
            session_matches[index + 1].start()
            if index + 1 < len(session_matches)
            else len(text)
        )
        block = text[match.end() : end]
        heading_matches = list(
            re.finditer(r"^### (.+?)\s*$", block, re.MULTILINE)
        )
        headings = [heading.group(1).strip() for heading in heading_matches]
        unknown = sorted(set(headings) - set(HEADING_IDS))
        if unknown:
            raise ValueError(f"session {number}: unexpected public sections {unknown}")
        if len(headings) != len(set(headings)):
            raise ValueError(f"session {number}: duplicate public section")
        missing = sorted(REQUIRED_HEADINGS - set(headings))
        if missing:
            raise ValueError(f"session {number}: missing public sections {missing}")

        sections: list[tuple[str, str]] = []
        for section_index, heading_match in enumerate(heading_matches):
            section_end = (
                heading_matches[section_index + 1].start()
                if section_index + 1 < len(heading_matches)
                else len(block)
            )
            content = block[heading_match.end() : section_end].strip()
            content = re.sub(r"\n---\s*$", "", content).strip()
            if not content:
                raise ValueError(
                    f"session {number}: empty public section {heading_match.group(1)!r}"
                )
            sections.append((heading_match.group(1).strip(), content))

        skills_content = dict(sections)["À savoir faire"]
        skills = [
            item.strip().rstrip(".")
            for item in re.findall(r"^-\s+(.+?)\s*$", skills_content, re.MULTILINE)
        ]
        if len(skills) < 2:
            raise ValueError(f"session {number}: expected at least two skills")

        body_parts = []
        for heading, content in sections:
            body_parts.append(
                f"## {heading}\n{{: #{HEADING_IDS[heading]}}}\n\n{content}"
            )
        body = "\n\n".join(body_parts).rstrip() + "\n"
        assert_student_safe(title + "\n" + body, f"session {number}")
        sessions.append(
            {
                "number": number,
                "title": title,
                "skills": skills,
                "body": body,
            }
        )
    return sessions


def parse_schedule(text: str) -> dict[int, dict[str, object]]:
    """Read only the date/status cells from the provisional schedule table."""

    rows: dict[int, dict[str, object]] = {}
    row_pattern = re.compile(
        r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
        re.MULTILINE,
    )
    for match in row_pattern.finditer(text):
        number = int(match.group(1))
        date_cell = plain_text(match.group(2))
        confirmed = number <= 17
        if not confirmed and "à fixer" not in date_cell.casefold():
            raise ValueError(f"session {number}: unresolved date must remain explicit")
        rows[number] = {
            "dateLabel": f"{date_cell} 2026" if confirmed else "Date et salle à confirmer",
            "scheduleConfirmed": confirmed,
        }

    if sorted(rows) != list(range(1, 20)):
        raise ValueError("schedule must contain ordered rows 1..19")
    if [number for number, row in rows.items() if not row["scheduleConfirmed"]] != [18, 19]:
        raise ValueError("only sessions 18 and 19 may have an unresolved schedule")
    return rows


def block_for(number: int) -> tuple[str, str]:
    if number <= 9:
        return "complexes", "Chapitre 1 · Nombres complexes"
    if number <= 18:
        return "langage", "Chapitre 2 · Ensembles et langage mathématique"
    return "synthese", "Synthèse · Révision"


def render_page(
    session: dict[str, object],
    previous: dict[str, object] | None,
    next_: dict[str, object] | None,
) -> str:
    number = int(session["number"])
    title = html.escape(str(session["title"]))
    url = str(session["url"])
    date_label = html.escape(str(session["dateLabel"]))
    block_label = html.escape(str(session["blockLabel"]))
    body = str(session["body"])
    schedule_badge = (
        "Créneau planifié" if session["scheduleConfirmed"] else "Date à confirmer"
    )
    schedule_class = "" if session["scheduleConfirmed"] else " is-pending"
    schedule_detail = (
        "Cours-TD intégré · 90 min"
        if session["scheduleConfirmed"]
        else "Date et salle à confirmer"
    )

    previous_link = ""
    if previous:
        previous_link = (
            '<a rel="prev" href="{{ '
            + yaml_string(str(previous["url"]))
            + ' | relative_url }}">'
            + f"<span>← Séance {previous['number']}</span>"
            + f"<strong>{html.escape(str(previous['title']))}</strong></a>"
        )
    next_link = ""
    if next_:
        next_link = (
            '<a rel="next" href="{{ '
            + yaml_string(str(next_["url"]))
            + ' | relative_url }}">'
            + f"<span>Séance {next_['number']} →</span>"
            + f"<strong>{html.escape(str(next_['title']))}</strong></a>"
        )
    pager_links = "\n    ".join(
        link for link in (previous_link, next_link) if link
    )

    page = f'''---
layout: page
title: {yaml_string(f"Séance {number} — {session['title']}")}
permalink: {yaml_string(url)}
description: {yaml_string(f"Parcours étudiant MAT101 IMA02 pour la séance {number} : compétences, références, exercices et ticket de sortie.")}
math: true
mat101_session: true
mat101_session_number: {number}
---

<!-- Generated from the public student workbook and provisional schedule. -->
<div class="mat101-library mat101-session-page" data-mat101-session-number="{number}">
  <header class="mat101-session-detail-hero">
    <div>
      <p class="mat101-kicker">MAT101 · IMA02 · parcours étudiant</p>
      <p class="mat101-session-eyebrow">{block_label}</p>
      <h1>{title}</h1>
      <p>{date_label}</p>
    </div>
    <div class="mat101-session-detail-status{schedule_class}">
      <span>{schedule_badge}</span>
      <strong>Parcours étudiant</strong>
      <small>{schedule_detail}</small>
    </div>
  </header>

  <nav class="mat101-session-local-nav" aria-label="Navigation MAT101">
    <a href="{{{{ '/mat101/seances/' | relative_url }}}}">Les 19 séances</a>
    <a href="{{{{ '/mat101/exercices/' | relative_url }}}}">103 exercices</a>
    <a href="#competences">Compétences</a>
    <a href="#parcours">Parcours</a>
    <a href="#ticket">Ticket</a>
  </nav>

  <aside class="mat101-session-source" aria-label="Repères de la séance">
    <p><strong>Support.</strong> Les pages du polycopié et les exercices à travailler sont indiqués dans le parcours.</p>
    <p><strong>Format.</strong> Une notion courte, une mise en pratique immédiate et un ticket de sortie.</p>
  </aside>

  <article class="mat101-session-content" markdown="1">

{{% raw %}}
{body}{{% endraw %}}

  </article>

  <nav class="mat101-session-pager" aria-label="Séances précédente et suivante">
    {pager_links}
  </nav>
</div>
'''
    assert_student_safe(page, f"rendered session {number}")
    return page


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        type=Path,
        help="Path to the MAT101-2026-course-pack repository",
    )
    args = parser.parse_args()
    source = args.source.resolve()
    workbook = source / "handouts" / "ima02-student-workbook.md"
    schedule_file = source / "SCHEDULE.md"
    if not workbook.is_file() or not schedule_file.is_file():
        raise SystemExit("source course pack is missing the student workbook or schedule")

    workbook_sessions = parse_workbook(workbook.read_text(encoding="utf-8"))
    schedule = parse_schedule(schedule_file.read_text(encoding="utf-8"))

    sessions: list[dict[str, object]] = []
    for workbook_session in workbook_sessions:
        number = int(workbook_session["number"])
        block_slug, block_label = block_for(number)
        slug = SESSION_SLUGS[number]
        title = str(workbook_session["title"])
        skills = list(workbook_session["skills"])
        body = str(workbook_session["body"])
        sessions.append(
            {
                **workbook_session,
                **schedule[number],
                "slug": slug,
                "url": f"/mat101/seances/{number:02d}-{slug}/",
                "shortTitle": title,
                "block": block_slug,
                "blockLabel": block_label,
                "skillsPlain": [plain_text(skill) for skill in skills],
                "search": plain_text(" ".join([title, block_label, *skills, body])).lower(),
            }
        )

    COLLECTION.mkdir(parents=True, exist_ok=True)
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    public_sessions = [
        {key: value for key, value in session.items() if key not in {"body", "skills"}}
        for session in sessions
    ]
    data_text = json.dumps(public_sessions, ensure_ascii=False, indent=2) + "\n"
    assert_student_safe(data_text, "public session data")
    DATA_FILE.write_text(data_text, encoding="utf-8")

    for index, session in enumerate(sessions):
        previous = sessions[index - 1] if index else None
        next_ = sessions[index + 1] if index + 1 < len(sessions) else None
        path = COLLECTION / f"{int(session['number']):02d}-{session['slug']}.md"
        path.write_text(render_page(session, previous, next_), encoding="utf-8")

    expected_names = {
        f"{int(session['number']):02d}-{session['slug']}.md" for session in sessions
    }
    unexpected = sorted(
        path.name for path in COLLECTION.glob("*.md") if path.name not in expected_names
    )
    if unexpected:
        raise SystemExit(f"unexpected generated session pages remain: {unexpected}")

    print(f"Generated {len(sessions)} student pages and {DATA_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
