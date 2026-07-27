#!/usr/bin/env python3
"""Build the site-native MAT101 exercise and solution data.

The statement images are lossless crops of the credited source PDF, preserving
the mathematical typography exactly. The solution HTML is generated from the
credited standalone LaTeX correction with Pandoc and remains MathJax-ready.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "assets/documents/mat101/mat_101_20220913.pdf"
SOLUTION_TEX = ROOT / "assets/documents/mat101/corrige-exercices-mat101.tex"
EXERCISE_DATA = ROOT / "_data/mat101_exercises.json"
TAG_DATA = ROOT / "_data/mat101_tags.json"
OUTPUT_DATA = ROOT / "_data/mat101_native.json"
OUTPUT_IMAGES = ROOT / "assets/images/mat101/statements"

CHAPTER_SOURCE_STARTS = {
    "complexes": 30,
    "ensembles": 61,
    "fonctions": 93,
    "limites": 116,
}

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

HEADING_ID = re.compile(r"^([1-4]\.\d+)\.$")
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


def render_page(source_page: int, work: Path) -> tuple[Path, Path]:
    prefix = work / f"page-{source_page}"
    run(
        "pdftoppm",
        "-f",
        str(source_page),
        "-l",
        str(source_page),
        "-r",
        "144",
        "-png",
        "-singlefile",
        str(SOURCE_PDF),
        str(prefix),
    )
    xml_base = work / f"page-{source_page}.xml"
    run(
        "pdftohtml",
        "-f",
        str(source_page),
        "-l",
        str(source_page),
        "-xml",
        "-hidden",
        "-nodrm",
        str(SOURCE_PDF),
        str(xml_base),
    )
    xml_path = xml_base if xml_base.exists() else xml_base.with_suffix(".xml.xml")
    return prefix.with_suffix(".png"), xml_path


def heading_markers(xml_path: Path, expected: set[str]) -> tuple[int, int, list[tuple[str, int]]]:
    page = ET.parse(xml_path).getroot().find("page")
    if page is None:
        raise RuntimeError(f"No page node in {xml_path}")
    width = int(page.attrib["width"])
    height = int(page.attrib["height"])
    text_nodes = list(page.findall("text"))
    markers: list[tuple[str, int]] = []
    for node in text_nodes:
        match = HEADING_ID.match("".join(node.itertext()).strip())
        if not match or match.group(1) not in expected:
            continue
        top = int(node.attrib["top"])
        same_line = [
            "".join(candidate.itertext()).strip().lower()
            for candidate in text_nodes
            if abs(int(candidate.attrib["top"]) - top) <= 2
        ]
        if any(label.startswith("exer") for label in same_line):
            markers.append((match.group(1), top))
    return width, height, sorted(set(markers), key=lambda marker: marker[1])


def trim_white(image: Image.Image, padding: int = 16) -> Image.Image:
    background = Image.new(image.mode, image.size, "white")
    difference = ImageChops.difference(image, background).convert("L")
    bounds = difference.point(lambda value: 255 if value > 12 else 0).getbbox()
    if not bounds:
        return image
    left, top, right, bottom = bounds
    return image.crop(
        (
            max(0, left - padding),
            max(0, top - padding),
            min(image.width, right + padding),
            min(image.height, bottom + padding),
        )
    )


def save_segment(
    page_image: Image.Image,
    xml_width: int,
    xml_height: int,
    top: int,
    bottom: int,
    exercise_id: str,
    segment_number: int,
) -> str:
    scale_x = page_image.width / xml_width
    scale_y = page_image.height / xml_height
    left = int(96 * scale_x)
    right = int((xml_width - 96) * scale_x)
    crop = page_image.crop(
        (
            left,
            max(0, int(top * scale_y)),
            right,
            min(page_image.height, int(bottom * scale_y)),
        )
    )
    crop = trim_white(crop)
    filename = f"exercice-{exercise_id.replace('.', '-')}-{segment_number}.webp"
    output = OUTPUT_IMAGES / filename
    crop.save(output, "WEBP", lossless=True, method=6)
    return f"/assets/images/mat101/statements/{filename}"


def build_statement_images() -> dict[str, list[str]]:
    chapters = json.loads(EXERCISE_DATA.read_text())
    all_ids = [
        exercise
        for chapter in chapters
        for page in chapter["pages"]
        for exercise in page["exercises"]
    ]
    expected = set(all_ids)
    images: dict[str, list[str]] = defaultdict(list)
    segment_counts: dict[str, int] = defaultdict(int)
    previous_exercise: str | None = None
    previous_source_page: int | None = None

    if OUTPUT_IMAGES.exists():
        shutil.rmtree(OUTPUT_IMAGES)
    OUTPUT_IMAGES.mkdir(parents=True)

    with tempfile.TemporaryDirectory(prefix="mat101-native-") as directory:
        work = Path(directory)
        for source_page, declared_ids in page_plan():
            if (
                previous_source_page is not None
                and source_page != previous_source_page + 1
            ):
                previous_exercise = None
            previous_source_page = source_page

            png_path, xml_path = render_page(source_page, work)
            xml_width, xml_height, markers = heading_markers(xml_path, expected)
            found_ids = [exercise_id for exercise_id, _ in markers]
            if found_ids != declared_ids:
                raise RuntimeError(
                    f"Page {source_page}: headings {found_ids} != declared {declared_ids}"
                )

            with Image.open(png_path).convert("RGB") as page_image:
                # Continuation pages begin just below the running header.  Keep
                # this deliberately above the first body line: whitespace is
                # trimmed later, while cutting too low can lose a question.
                body_top = 230
                # Stop above the printed page number while retaining footnotes.
                body_bottom = xml_height - 200

                if not markers:
                    if previous_exercise is None:
                        raise RuntimeError(f"Unassigned continuation on page {source_page}")
                    segment_counts[previous_exercise] += 1
                    images[previous_exercise].append(
                        save_segment(
                            page_image,
                            xml_width,
                            xml_height,
                            body_top,
                            body_bottom,
                            previous_exercise,
                            segment_counts[previous_exercise],
                        )
                    )
                    continue

                first_top = markers[0][1]
                if previous_exercise is not None and first_top > body_top + 70:
                    segment_counts[previous_exercise] += 1
                    images[previous_exercise].append(
                        save_segment(
                            page_image,
                            xml_width,
                            xml_height,
                            body_top,
                            first_top - 12,
                            previous_exercise,
                            segment_counts[previous_exercise],
                        )
                    )

                for index, (exercise_id, marker_top) in enumerate(markers):
                    next_top = (
                        markers[index + 1][1] - 12
                        if index + 1 < len(markers)
                        else body_bottom
                    )
                    segment_counts[exercise_id] += 1
                    images[exercise_id].append(
                        save_segment(
                            page_image,
                            xml_width,
                            xml_height,
                            marker_top - 12,
                            next_top,
                            exercise_id,
                            segment_counts[exercise_id],
                        )
                    )
                    previous_exercise = exercise_id

    missing = [exercise_id for exercise_id in all_ids if not images[exercise_id]]
    if missing:
        raise RuntimeError(f"Exercises without statement images: {missing}")
    return images


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
        solutions[match.group(1)] = TABLE_BLOCK.sub(
            enhance_table,
            solution,
        )
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

    statements = build_statement_images()
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
                        "statementImages": statements[exercise_id],
                        "solutionHtml": solutions[exercise_id],
                    }
                )
    OUTPUT_DATA.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        f"Built {len(records)} native exercises, "
        f"{sum(len(record['statementImages']) for record in records)} statement images"
    )


if __name__ == "__main__":
    main()
