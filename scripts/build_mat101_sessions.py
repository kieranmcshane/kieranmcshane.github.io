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
from datetime import date
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

DISPLAY_HEADINGS = {
    "Ticket": "Questions",
}

HEADING_IDS = {
    "À savoir faire": "competences",
    "Parcours": "parcours",
    "Activité": "activite",
    "Contrôle rapide": "controle",
    "Contrôle formatif": "controle",
    "Révision mixte": "revision",
    "Ticket": "questions",
}
REQUIRED_HEADINGS = {"À savoir faire", "Parcours", "Ticket"}
SESSION_FORMATS: dict[int, dict[str, str]] = {
    10: {
        "kind": "interro",
        "statusBadge": "Interro",
        "statusDetail": "1 h · tiers temps 1 h 20",
    },
}

# Static past/upcoming split for the published site. Séances strictly before
# this date are marked done; later confirmed séances stay upcoming.
PUBLISHED_AS_OF = date(2026, 10, 5)
# Week of the partiel (semaine du 19/20 octobre 2026): no regular TD.
PARTIEL_WEEK = (date(2026, 10, 19), date(2026, 10, 25))
WEEKDAY_LABELS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]
MONTH_LABELS = [
    "janv.",
    "févr.",
    "mars",
    "avr.",
    "mai",
    "juin",
    "juil.",
    "août",
    "sept.",
    "oct.",
    "nov.",
    "déc.",
]
# IMA-2 / IMA-S1-02 rooms from ADE, keyed by date.weekday().
WEEKDAY_SLOTS = {
    1: ("09:45–11:15", "DLST E201"),
    3: ("13:30–15:00", "DLST B007"),
    4: ("15:15–16:45", "DLST D104"),
}
# First of the two extra séances. Séance 19 stays unconfirmed.
EXTRA_CONFIRMED = {
    18: {
        "date": date(2026, 9, 23),
        "timeLabel": "13:30–15:00",
        "room": "DLST E204",
    }
}
DATE_LABEL_RE = re.compile(
    r"^(lun\.|mar\.|mer\.|jeu\.|ven\.|sam\.|dim\.) (\d{1,2}) "
    r"(janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.) (\d{4})$"
)
FIELD_ORDER = [
    "number",
    "title",
    "dateLabel",
    "dateIso",
    "timeLabel",
    "room",
    "status",
    "scheduleConfirmed",
    "slug",
    "url",
    "shortTitle",
    "block",
    "blockLabel",
    "skillsPlain",
    "search",
    "skillsHtml",
    "kind",
    "statusBadge",
    "statusDetail",
]
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


BACKTICK = re.compile(r"`([^`]+)`")


def inline_math_html(value: str, *, delimiter: str = "paren") -> str:
    """Turn workbook backtick math into MathJax-ready inline markup."""

    chunks: list[str] = []
    index = 0
    for match in BACKTICK.finditer(value):
        if match.start() > index:
            chunks.append(html.escape(value[index : match.start()]))
        math = match.group(1)
        if delimiter == "dollar":
            chunks.append(f'<span class="math inline">${math}$</span>')
        else:
            chunks.append(f'<span class="math inline">\\({math}\\)</span>')
        index = match.end()
    if index < len(value):
        chunks.append(html.escape(value[index:]))
    return "".join(chunks)


def skill_to_html(value: str) -> str:
    return inline_math_html(value)


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
            display_heading = DISPLAY_HEADINGS.get(heading, heading)
            body_parts.append(
                f"## {display_heading}\n{{: #{HEADING_IDS[heading]}}}\n\n{content}"
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
    if number <= 8:
        return "complexes", "Chapitre 1 · Nombres complexes"
    return "langage", "Chapitre 2 · Ensembles et langage mathématique"


def french_date_label(value: date) -> str:
    return (
        f"{WEEKDAY_LABELS[value.weekday()]} {value.day} "
        f"{MONTH_LABELS[value.month - 1]} {value.year}"
    )


def parse_french_date(label: str) -> date:
    match = DATE_LABEL_RE.fullmatch(label.strip())
    if not match:
        raise ValueError(f"unrecognized session date label: {label!r}")
    weekday, day, month, year = match.groups()
    parsed = date(int(year), MONTH_LABELS.index(month) + 1, int(day))
    if WEEKDAY_LABELS[parsed.weekday()] != weekday:
        raise ValueError(f"weekday mismatch in {label!r}")
    return parsed


def reject_partiel_week(when: date, number: int) -> None:
    start, end = PARTIEL_WEEK
    if start <= when <= end:
        raise ValueError(
            f"session {number}: {when.isoformat()} falls in the partiel week "
            f"({start.isoformat()}–{end.isoformat()}); no regular TD that week"
        )


def merge_search(search: str, *bits: str | None) -> str:
    extra = " ".join(str(bit) for bit in bits if bit)
    if not extra:
        return search
    lowered = extra.casefold()
    if lowered in search:
        return search
    return f"{search} {lowered}".strip()


def reorder_session(session: dict[str, object]) -> dict[str, object]:
    ordered = {key: session[key] for key in FIELD_ORDER if key in session}
    for key, value in session.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def attach_public_schedule(
    session: dict[str, object], today: date = PUBLISHED_AS_OF
) -> dict[str, object]:
    """Add room, time, and past/upcoming status without inventing lesson content."""

    number = int(session["number"])
    updated = dict(session)
    when: date | None
    if number in EXTRA_CONFIRMED:
        extra = EXTRA_CONFIRMED[number]
        when = extra["date"]
        reject_partiel_week(when, number)
        updated.update(
            {
                "dateIso": when.isoformat(),
                "dateLabel": french_date_label(when),
                "timeLabel": extra["timeLabel"],
                "room": extra["room"],
                "scheduleConfirmed": True,
            }
        )
    elif updated.get("scheduleConfirmed"):
        when = parse_french_date(str(updated["dateLabel"]))
        reject_partiel_week(when, number)
        slot = WEEKDAY_SLOTS.get(when.weekday())
        if slot is None:
            raise ValueError(
                f"session {number}: no ADE room for {when.isoformat()}"
            )
        time_label, room = slot
        updated.update(
            {
                "dateIso": when.isoformat(),
                "dateLabel": french_date_label(when),
                "timeLabel": time_label,
                "room": room,
                "scheduleConfirmed": True,
            }
        )
    else:
        when = None
        updated.update(
            {
                "dateIso": None,
                "dateLabel": "Date et salle à confirmer",
                "timeLabel": None,
                "room": None,
                "scheduleConfirmed": False,
            }
        )

    kind = updated.get("kind") or SESSION_FORMATS.get(number, {}).get("kind")
    if when is None:
        updated["status"] = "pending"
        updated["statusBadge"] = "À confirmer"
    elif when < today:
        updated["status"] = "past"
        updated["statusBadge"] = "Séance faite"
    else:
        updated["status"] = "upcoming"
        if kind == "interro":
            updated["statusBadge"] = "Interro"
        else:
            updated["statusBadge"] = "À venir"
            updated.pop("statusDetail", None)

    if kind == "interro":
        updated["kind"] = "interro"
        updated["statusDetail"] = str(
            updated.get("statusDetail")
            or SESSION_FORMATS[number]["statusDetail"]
        )
    elif updated["status"] != "pending":
        updated.pop("statusDetail", None)

    updated["search"] = merge_search(
        str(updated.get("search") or ""),
        str(updated.get("room") or ""),
        str(updated.get("timeLabel") or ""),
        str(updated.get("dateLabel") or ""),
    )
    return reorder_session(updated)


def session_status(session: dict[str, object]) -> tuple[str, str, str]:
    status = session.get("status")
    if status == "past":
        detail = str(session.get("statusDetail") or "Cours-TD intégré · 90 min")
        return ("Séance faite", " is-past", detail)
    if status == "upcoming":
        if session.get("kind") == "interro":
            return (
                "Interro",
                " is-upcoming is-interro",
                str(session.get("statusDetail") or ""),
            )
        return (
            "À venir",
            " is-upcoming",
            str(session.get("statusDetail") or "Cours-TD intégré · 90 min"),
        )
    if status == "pending":
        return ("Date à confirmer", " is-pending", "Date et salle à confirmer")

    override = SESSION_FORMATS.get(int(session["number"]))
    if override:
        return (
            override["statusBadge"],
            " is-interro",
            override["statusDetail"],
        )
    if session["scheduleConfirmed"]:
        return ("Créneau planifié", "", "Cours-TD intégré · 90 min")
    return ("Date à confirmer", " is-pending", "Date et salle à confirmer")


def schedule_markup(session: dict[str, object]) -> tuple[str, str, str]:
    badge, css_class, detail = session_status(session)
    status_class = "mat101-session-detail-status" + css_class
    when_bits = [
        str(bit) for bit in (session.get("timeLabel"), session.get("room")) if bit
    ]
    room_html = ""
    if when_bits:
        room_html = (
            '<span class="mat101-session-room"> · '
            + html.escape(" · ".join(when_bits))
            + "</span>"
        )
    date_html = f"      <p>{html.escape(str(session['dateLabel']))}{room_html}</p>"
    status_html = (
        f'<div class="{status_class}">\n'
        f"      <span>{html.escape(badge)}</span>\n"
        f"      <small>{html.escape(detail)}</small>\n"
        "    </div>"
    )
    page_state = ""
    status = session.get("status")
    if status in {"past", "upcoming", "pending"}:
        page_state = f" is-{status}"
    return page_state, date_html, status_html


def render_page(
    session: dict[str, object],
    previous: dict[str, object] | None,
    next_: dict[str, object] | None,
) -> str:
    number = int(session["number"])
    title = html.escape(str(session["title"]))
    url = str(session["url"])
    block_label = html.escape(str(session["blockLabel"]))
    body = inline_math_html(str(session["body"]), delimiter="dollar")
    page_state, date_html, status_html = schedule_markup(session)
    source_note = (
        f"<p><strong>Interro.</strong> {html.escape(schedule_detail.rstrip('.'))}.</p>"
        if session.get("kind") == "interro"
        else "<p><strong>Support.</strong> Les pages du polycopié et les exercices à travailler sont indiqués dans le parcours.</p>"
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
layout: mat101
title: {yaml_string(f"Séance {number} — {session['title']}")}
permalink: {yaml_string(url)}
description: {yaml_string(f"Parcours étudiant MAT101 IMA02 pour la séance {number} : compétences, références, exercices et questions de sortie.")}
math: true
mat101_session: true
mat101_session_number: {number}
---

<!-- Generated from the public student workbook and provisional schedule. -->
<div class="mat101-library mat101-session-page{page_state}" data-mat101-session-number="{number}">
  <header class="mat101-session-detail-hero">
    <div>
      <p class="mat101-session-eyebrow">{block_label}</p>
      <h1>{title}</h1>
{date_html}
    </div>
    {status_html}
  </header>

  <nav class="mat101-session-local-nav" aria-label="Navigation MAT101">
    <a href="{{{{ '/mat101/seances/' | relative_url }}}}">Les 19 séances</a>
    <a href="{{{{ '/mat101/exercices/' | relative_url }}}}">103 exercices</a>
    <a href="#competences">Compétences</a>
    <a href="#parcours">Parcours</a>
    <a href="#questions">Questions</a>
  </nav>

  <aside class="mat101-session-source" aria-label="Repères de la séance">
    {source_note}
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


def patch_session_page(text: str, session: dict[str, object]) -> str:
    page_state, date_html, status_html = schedule_markup(session)
    updated, page_count = re.subn(
        r'<div class="mat101-library mat101-session-page(?: is-(?:past|upcoming|pending))?"',
        f'<div class="mat101-library mat101-session-page{page_state}"',
        text,
        count=1,
    )
    updated, date_count = re.subn(
        r"(<h1>.*?</h1>)\s*<p>.*?</p>",
        lambda match: f"{match.group(1)}\n{date_html}",
        updated,
        count=1,
        flags=re.DOTALL,
    )
    updated, status_count = re.subn(
        r'<div class="mat101-session-detail-status[^"]*">\s*<span>.*?</span>\s*<small>.*?</small>\s*</div>',
        status_html,
        updated,
        count=1,
        flags=re.DOTALL,
    )
    if page_count != 1 or date_count != 1 or status_count != 1:
        raise ValueError(
            f"session {session['number']}: could not patch the public schedule "
            f"(page={page_count}, date={date_count}, status={status_count})"
        )
    assert_student_safe(updated, f"patched session {session['number']}")
    return updated


def refresh_committed(today: date = PUBLISHED_AS_OF) -> None:
    """Refresh rooms, dates, and past/upcoming status on the committed pages."""

    sessions = [
        attach_public_schedule(session, today)
        for session in json.loads(DATA_FILE.read_text(encoding="utf-8"))
    ]
    public_sessions = [
        {key: value for key, value in session.items() if key not in {"body", "skills"}}
        for session in sessions
    ]
    data_text = json.dumps(public_sessions, ensure_ascii=False, indent=2) + "\n"
    assert_student_safe(data_text, "public session data")
    DATA_FILE.write_text(data_text, encoding="utf-8")
    for session in sessions:
        path = COLLECTION / f"{int(session['number']):02d}-{session['slug']}.md"
        path.write_text(
            patch_session_page(path.read_text(encoding="utf-8"), session),
            encoding="utf-8",
        )
    print(f"Refreshed {len(sessions)} committed sessions in {DATA_FILE.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        help="Path to the MAT101-2026-course-pack repository",
    )
    parser.add_argument(
        "--refresh-committed",
        action="store_true",
        help="Apply the public schedule to the committed session data and pages",
    )
    args = parser.parse_args()
    if args.refresh_committed:
        refresh_committed()
        return
    if args.source is None:
        raise SystemExit("source course pack is required unless --refresh-committed is set")
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
            attach_public_schedule(
                {
                    **workbook_session,
                    **schedule[number],
                    "slug": slug,
                    "url": f"/mat101/seances/{number:02d}-{slug}/",
                    "shortTitle": title,
                    "block": block_slug,
                    "blockLabel": block_label,
                    "skillsPlain": [plain_text(skill) for skill in skills],
                    "skillsHtml": [skill_to_html(skill) for skill in skills],
                    **SESSION_FORMATS.get(number, {}),
                    "search": plain_text(
                        " ".join(
                            [
                                title,
                                block_label,
                                *skills,
                                body,
                                SESSION_FORMATS.get(number, {}).get("statusBadge", ""),
                                SESSION_FORMATS.get(number, {}).get("statusDetail", ""),
                            ]
                        )
                    ).lower(),
                }
            )
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
