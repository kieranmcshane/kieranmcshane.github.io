#!/usr/bin/env python3
"""Build the site-native MAT101 exercise and solution data.

Statements are extracted as real, selectable text from the credited source PDF.
The source PDF remains available as the archival reference, but raster crops are
not used as the primary web content. Solution HTML is generated from the
credited standalone LaTeX correction with Pandoc and remains MathJax-ready.
"""

from __future__ import annotations

import json
import html
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "assets/documents/mat101/mat_101_20220913.pdf"
SOLUTION_TEX = ROOT / "assets/documents/mat101/corrige-exercices-mat101.tex"
EXERCISE_DATA = ROOT / "_data/mat101_exercises.json"
TAG_DATA = ROOT / "_data/mat101_tags.json"
OUTPUT_DATA = ROOT / "_data/mat101_native.json"

CHAPTER_SOURCE_STARTS = {
    "complexes": 30,
    "ensembles": 61,
    "fonctions": 93,
    "limites": 116,
}

SOURCE_PAGE_RANGES = ((30, 35), (61, 70), (93, 103), (116, 120))

# Difficulty markers transcribed from the headings in the source booklet.
# Exercise 3.13 is the only exercise without a printed marker.
EXERCISE_DIFFICULTIES = {
    "1.1": "*", "1.2": "*", "1.3": "*", "1.4": "*", "1.5": "*",
    "1.6": "**", "1.7": "**", "1.8": "**", "1.9": "**", "1.10": "**",
    "1.11": "**", "1.12": "**", "1.13": "**", "1.14": "**", "1.15": "*",
    "1.16": "*", "1.17": "**", "1.18": "***", "1.19": "***", "1.20": "***",
    "2.1": "*", "2.2": "*", "2.3": "*", "2.4": "*", "2.5": "*/**",
    "2.6": "**", "2.7": "**", "2.8": "**", "2.9": "*", "2.10": "*",
    "2.11": "*", "2.12": "**", "2.13": "**", "2.14": "*", "2.15": "*",
    "2.16": "*", "2.17": "**", "2.18": "**", "2.19": "*", "2.20": "*",
    "2.21": "*", "2.22": "*", "2.23": "***", "2.24": "*", "2.25": "*",
    "2.26": "**", "2.27": "**", "2.28": "**", "2.29": "**", "2.30": "**",
    "2.31": "**", "2.32": "**", "2.33": "***", "2.34": "**", "2.35": "***",
    "3.1": "*", "3.2": "*", "3.3": "*/**", "3.4": "**", "3.5": "**",
    "3.6": "*", "3.7": "**", "3.8": "**", "3.9": "*", "3.10": "**",
    "3.11": "**", "3.12": "*", "3.13": None, "3.14": "**", "3.15": "**",
    "3.16": "**", "3.17": "**", "3.18": "*", "3.19": "*", "3.20": "**",
    "3.21": "*", "3.22": "**", "3.23": "*", "3.24": "*", "3.25": "**",
    "3.26": "**", "3.27": "**", "3.28": "**", "3.29": "**", "3.30": "***",
    "3.31": "***",
    "4.1": "*", "4.2": "*", "4.3": "*", "4.4": "*", "4.5": "**",
    "4.6": "**", "4.7": "**", "4.8": "**", "4.9": "**", "4.10": "*",
    "4.11": "*/**", "4.12": "**", "4.13": "**", "4.14": "*", "4.15": "**",
    "4.16": "**", "4.17": "**",
}

STATEMENT_HEADING = re.compile(
    r"^Exercice\s+([1-4]\.\d+)\.\s*(?:\((?:\*{1,3}|\*/\*\*)\))?",
    re.MULTILINE,
)
SOLUTION_HEADING = re.compile(
    r'<h2 class="unnumbered" id="exercice-([1-4]\.\d+)">.*?</h2>\s*'
    r"(.*?)(?=<h[12]\b|\Z)",
    re.DOTALL,
)
TABLE_BLOCK = re.compile(r"<table>.*?</table>", re.DOTALL)
EMPTY_FIRST_HEADER = re.compile(
    r"(<thead>\s*<tr>\s*)<th([^>]*)></th>",
    re.DOTALL,
)
DOT_NUMBER_CELL = re.compile(
    r'<td style="text-align: left;">\.</td>'
)

SOURCE_TEXT_REPLACEMENTS = {
    "\x08": "{",
    "\x10": "« ",
    "\x11": " »",
    "\x12": "(",
    "\x13": ")",
    "\x14": "[",
    "\x15": "]",
    "\x1a": "∞",
    "\x1b": "ff",
    "\x1c": "fi",
    "\x1d": "ô",
    "\x1e": "ffi",
    "Exer i e": "Exercice",
    "Exer i es": "Exercices",
    "Fon tions": "Fonctions",
    "fon tion": "fonction",
    "fon tions": "fonctions",
    "appli ation": "application",
    "appli ations": "applications",
    "Cal uler": "Calculer",
    " al uler": " calculer",
    "É rire": "Écrire",
    "é rire": "écrire",
    " ave ": " avec ",
    " 'est": " c'est",
    " omme": " comme",
    " omplexe": " complexe",
    " omplexes": " complexes",
    " ompas": " compas",
    " ombien": " combien",
    " ommut": " commut",
    " ompat": " compat",
    " ompos": " compos",
    " onstru": " constru",
    " onstrui": " construi",
    " onstruction": " construction",
    " ontre": " contre",
    " ontrapos": " contrapos",
    " onject": " conject",
    " onjugu": " conjugu",
    " onsid": " consid",
    " onver": " conver",
    " onstante": " constante",
    " orrespond": " correspond",
    " orriger": " corriger",
    " ourbe": " courbe",
    " ours": " cours",
    " oupe": " coupe",
    " ré urren": " récurren",
    " ré ipro": " récipro",
    " ra ine": " racine",
    " ra ines": " racines",
    " arré": " carré",
    " arrés": " carrés",
    " ha un": " chacun",
    " ha une": " chacune",
    " haque": " chaque",
    " in onnue": " inconnue",
    "stri tement": "strictement",
    "inje tive": "injective",
    "impli ation": "implication",
    "indi ation": "indication",
    "en e qui on erne": "en ce qui concerne",
    "règles i-dessus": "règles ci-dessus",
    " in lus": " inclus",
    " distin t": " distinct",
    " dire t": " direct",
    " exa t": " exact",
    " fa e": " face",
    " arte": " carte",
    " artes": " cartes",
    " entre": " centre",
    " er le": " cercle",
    " oord": " coord",
    " e théorème": " ce théorème",
    " e jeu": " ce jeu",
    " e cas": " ce cas",
    " e as": " ce cas",
    " e qui": " ce qui",
    " e qu'": " ce qu'",
    " es deux": " ces deux",
    " es trois": " ces trois",
    " es propriétés": " ces propriétés",
    " ette ": " cette ",
    " eux ": " ceux ",
    " né ess": " nécess",
    " pré is": " précis",
    " pro é": " procé",
    " asso i": " associ",
    " puissan es": " puissances",
    " équivalen e": " équivalence",
    " lasses": " classes",
    " lasse": " classe",
    " in lusion": " inclusion",
    " in lusions": " inclusions",
    "interse tion": "intersection",
    "Constru tion": "Construction",
    "constru tion": "construction",
    "multipli ation": "multiplication",
    "quanti fi ateurs": "quantificateurs",
    "quanti fi ations": "quantifications",
    "équivalen e": "équivalence",
    " onditions": " conditions",
    "pré aution": "précaution",
    "pré édent": "précédent",
    " onvain re": " convaincre",
    "en ore": "encore",
    " hose": " chose",
    "Asso i": "Associ",
    " ontenir": " contenir",
    " ontient": " contient",
    "quel onque": "quelconque",
    " roissant": " croissant",
    "dé roissant": "décroissant",
    "rempla e": "remplace",
    "Syra use": "Syracuse",
    "fra tions": "fractions",
    " pré au": " précau",
    "récurren e": "récurrence",
}

ROOT_DIAGRAMS = {
    "1.12": r"""
<section class="mat101-root-geometry" aria-labelledby="mat101-root-geometry-1-12">
<h3 id="mat101-root-geometry-1-12">Lecture géométrique</h3>
<p>Pour une équation \(z^n=\rho e^{i\theta}\), les solutions sont les sommets d’un polygone régulier : elles appartiennent au cercle de rayon \(\rho^{1/n}\), sont espacées d’un angle \(2\pi/n\), puis l’ensemble est tourné de \(\theta/n\).</p>
<div class="mat101-root-grid">
<figure class="mat101-root-diagram">
<canvas data-mat101-root-diagram data-root-count="3" data-start-angle="0.5235987756" data-angle-label="π/6" data-labels="z₀|z₁|z₂" width="560" height="560" aria-hidden="true"></canvas>
<figcaption><strong>\(z^3=i\)</strong><span>Trois racines sur le cercle unité, séparées de \(2\pi/3\) et tournées de \(\pi/6\).</span></figcaption>
</figure>
<figure class="mat101-root-diagram">
<canvas data-mat101-root-diagram data-root-count="4" data-start-angle="0" data-labels="1|i|−1|−i" width="560" height="560" aria-hidden="true"></canvas>
<figcaption><strong>\(z^4=1\)</strong><span>Les quatre racines de l’unité forment un carré inscrit.</span></figcaption>
</figure>
<figure class="mat101-root-diagram">
<canvas data-mat101-root-diagram data-root-count="4" data-start-angle="0.5235987756" data-angle-label="π/6" data-labels="z₀|z₁|z₂|z₃" width="560" height="560" aria-hidden="true"></canvas>
<figcaption><strong>\(z^4=e^{2i\pi/3}\)</strong><span>Le même carré est tourné de \((2\pi/3)/4=\pi/6\).</span></figcaption>
</figure>
</div>
</section>
""".strip(),
    "1.18": r"""
<section class="mat101-root-geometry" aria-labelledby="mat101-root-geometry-1-18">
<h3 id="mat101-root-geometry-1-18">Les cinquièmes racines sur le cercle unité</h3>
<p>Les arguments \(0,2\pi/5,4\pi/5,6\pi/5,8\pi/5\) découpent le cercle en cinq arcs égaux. Les racines de \(z^5-1\) sont donc exactement les sommets d’un pentagone régulier.</p>
<div class="mat101-root-grid mat101-root-grid-single">
<figure class="mat101-root-diagram">
<canvas data-mat101-root-diagram data-root-count="5" data-start-angle="0" data-labels="1|ζ|ζ²|ζ³|ζ⁴" data-muted-index="0" width="560" height="560" aria-hidden="true"></canvas>
<figcaption><strong>\(\zeta=e^{2i\pi/5}\)</strong><span>Le point \(1\), dessiné en contour, est une racine de \(P(z)=z^5-1\), mais pas de \(Q(z)=z^4+z^3+z^2+z+1\).</span></figcaption>
</figure>
</div>
</section>
""".strip(),
}


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def page_plan() -> list[tuple[int, list[str]]]:
    chapters = json.loads(EXERCISE_DATA.read_text())
    plan: list[tuple[int, list[str]]] = []
    for chapter in chapters:
        source_page = CHAPTER_SOURCE_STARTS[chapter["id"]]
        for page in chapter["pages"]:
            plan.append((source_page, page["exercises"]))
            source_page += 1
    return plan


def normalize_source_text(text: str) -> str:
    """Repair the known font-encoding artefacts in the 2022 source PDF."""

    for source, replacement in SOURCE_TEXT_REPLACEMENTS.items():
        text = text.replace(source, replacement)

    text = text.replace("\f", "\n")
    text = re.sub(r"[\x00-\x07\x09\x0b\x0e-\x0f\x16-\x19\x1f]", "", text)
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    text = re.sub(
        r"^(?:MAT101, Chap\.[^\n]*|Exercices[^\n]*MAT101, Chap\.[^\n]*)$",
        "",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(r"^[ \t]*\d{1,3}[ \t]*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[ \t]+|[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def format_statement_text(text: str) -> tuple[str, str]:
    """Return a readable HTML transcription and a compact search string."""

    text = normalize_source_text(text)
    text = re.sub(r"^\s*Exercices\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(
        r"^(?:Assertions et tables de vérité|Raisonnements|Fonctions|"
        r"Identités remarquables|Identitésremarquables|"
        r"Réels et approximation|Réelsetapproximation|"
        r"Quantifications successives|Quantificationssuccessives|"
        r"Limites des suites|Limitesdessuites)\s*$",
        "",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    text = re.sub(r"\n\s*(?=(?:\d{1,2}\.|[A-Z]\)|\([a-z]\))\s)", "\n\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    for source, replacement in SOURCE_TEXT_REPLACEMENTS.items():
        if ord(source[0]) >= 32:
            text = text.replace(source, replacement)
    text = re.sub(r" +", " ", text)
    text = text.replace("( c'est", "(c'est")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    paragraphs = [
        f"<p>{html.escape(paragraph).replace(chr(10), '<br>')}</p>"
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]
    statement_html = (
        '<div class="mat101-statement-transcription" lang="fr">\n'
        + "\n".join(paragraphs)
        + "\n</div>"
    )
    search_text = re.sub(r"\s+", " ", text).strip()
    return statement_html, search_text


def build_statement_text() -> dict[str, dict[str, str | int]]:
    chapters = json.loads(EXERCISE_DATA.read_text())
    expected_ids = [
        exercise_id
        for chapter in chapters
        for page in chapter["pages"]
        for exercise_id in page["exercises"]
    ]
    page_by_exercise = {
        exercise_id: source_page
        for source_page, exercise_ids in page_plan()
        for exercise_id in exercise_ids
    }
    recueil_page_by_exercise = {
        exercise_id: page["pdfPage"]
        for chapter in chapters
        for page in chapter["pages"]
        for exercise_id in page["exercises"]
    }

    with tempfile.TemporaryDirectory(prefix="mat101-statements-") as directory:
        work = Path(directory)
        source_parts = []
        for first_page, last_page in SOURCE_PAGE_RANGES:
            text_path = work / f"statements-{first_page}-{last_page}.txt"
            run(
                "pdftotext",
                "-f",
                str(first_page),
                "-l",
                str(last_page),
                "-raw",
                str(SOURCE_PDF),
                str(text_path),
            )
            source_parts.append(text_path.read_text())
        source_text = normalize_source_text("\n".join(source_parts))

    matches = list(STATEMENT_HEADING.finditer(source_text))
    statements: dict[str, dict[str, str | int]] = {}
    for index, match in enumerate(matches):
        exercise_id = match.group(1)
        if exercise_id not in page_by_exercise:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source_text)
        statement_html, search_text = format_statement_text(
            source_text[match.end():end]
        )
        statements[exercise_id] = {
            "html": statement_html,
            "searchText": search_text,
            "sourcePage": page_by_exercise[exercise_id],
            "recueilPage": recueil_page_by_exercise[exercise_id],
        }

    missing = [exercise_id for exercise_id in expected_ids if exercise_id not in statements]
    if missing:
        raise RuntimeError(f"Exercises without semantic statements: {missing}")
    return statements


def build_solution_html() -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="mat101-pandoc-") as directory:
        html_path = Path(directory) / "solutions.html"
        run(
            "pandoc",
            str(SOLUTION_TEX),
            "--from=latex",
            "--to=html5",
            "--mathjax",
            "--output",
            str(html_path),
        )
        html = html_path.read_text()
    def enhance_table(match: re.Match[str]) -> str:
        table = match.group(0)
        dot_cells = DOT_NUMBER_CELL.findall(table)
        if dot_cells and EMPTY_FIRST_HEADER.search(table):
            table = EMPTY_FIRST_HEADER.sub(
                r"\1<th\2>N°</th>",
                table,
                count=1,
            )
            row_number = 0

            def restore_row_number(_: re.Match[str]) -> str:
                nonlocal row_number
                row_number += 1
                return (
                    '<td class="mat101-row-number" '
                    'style="text-align: center;">'
                    f"{row_number}"
                    "</td>"
                )

            table = DOT_NUMBER_CELL.sub(restore_row_number, table)

        table = table.replace(
            "<table>",
            '<table class="mat101-math-table">',
            1,
        )
        table = table.replace("<th ", '<th scope="col" ')
        return (
            '<div class="mat101-table-scroll" role="region" '
            'aria-label="Tableau de résultats mathématiques" tabindex="0">\n'
            f"{table}\n"
            "</div>"
        )

    solutions = {}
    for match in SOLUTION_HEADING.finditer(html):
        solution = match.group(2).strip()
        solution = re.sub(
            r"<p><strong>Idée et plan\.</strong></p>\s*(<p>.*?</p>)",
            r'<aside class="mat101-method"><strong>Idée et plan.</strong>\1</aside>',
            solution,
            flags=re.DOTALL,
        )
        solution = re.sub(
            r"<p>(?=(?:(?!</p>).)*<strong>Examen de la solution\.</strong>)",
            '<p class="mat101-solution-review">',
            solution,
            flags=re.DOTALL,
        )
        exercise_id = match.group(1)
        solution = TABLE_BLOCK.sub(
            enhance_table,
            solution,
        )
        if exercise_id in ROOT_DIAGRAMS:
            solution = f"{ROOT_DIAGRAMS[exercise_id]}\n{solution}"
        solutions[exercise_id] = solution
    if len(solutions) != 103:
        raise RuntimeError(f"Expected 103 solution blocks, found {len(solutions)}")
    return solutions


def main() -> None:
    chapters = json.loads(EXERCISE_DATA.read_text())
    tag_index = json.loads(TAG_DATA.read_text())["tags"]
    exercise_ids = {
        exercise_id
        for chapter in chapters
        for page in chapter["pages"]
        for exercise_id in page["exercises"]
    }
    if set(EXERCISE_DIFFICULTIES) != exercise_ids:
        raise RuntimeError("Difficulty markers do not match the exercise index")

    exercise_tags: dict[str, list[dict[str, str]]] = defaultdict(list)
    known_slugs: set[str] = set()
    for tag in tag_index:
        slug = tag["slug"]
        if slug in known_slugs:
            raise RuntimeError(f"Duplicate tag slug: {slug}")
        known_slugs.add(slug)
        for exercise_id in tag["exercises"]:
            if exercise_id not in exercise_ids:
                raise RuntimeError(f"Unknown exercise {exercise_id} in tag {slug}")
            exercise_tags[exercise_id].append(
                {"slug": slug, "label": tag["label"]}
            )
    untagged = sorted(exercise_ids - set(exercise_tags))
    if untagged:
        raise RuntimeError(f"Exercises without tags: {untagged}")

    statements = build_statement_text()
    solutions = build_solution_html()
    records = []
    for chapter in chapters:
        for page in chapter["pages"]:
            for exercise_id in page["exercises"]:
                records.append(
                    {
                        "id": exercise_id,
                        "chapterId": chapter["id"],
                        "chapterNumber": chapter["number"],
                        "chapterTitle": chapter["title"],
                        "difficulty": EXERCISE_DIFFICULTIES[exercise_id],
                        "tags": exercise_tags[exercise_id],
                        "statementHtml": statements[exercise_id]["html"],
                        "statementSearchText": statements[exercise_id]["searchText"],
                        "statementSourcePage": statements[exercise_id]["sourcePage"],
                        "statementPdfPage": statements[exercise_id]["recueilPage"],
                        "transcriptionStatus": "extracted",
                        "mathematicalReviewStatus": "pending",
                        "solutionHtml": solutions[exercise_id],
                    }
                )
    OUTPUT_DATA.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        f"Built {len(records)} native exercises with semantic statements "
        "and MathJax-ready solutions"
    )


if __name__ == "__main__":
    main()
