#!/usr/bin/env python3
"""Build the native Répertoire cards from a geometry-aware PDF transcription.

The checked-in Markdown source is produced from the reviewed PDF with equation
recognition enabled.  Unlike ``pdftotext``, it preserves the two-dimensional
structure of fractions, roots, indices, exponents, matrices, and integrals.
This script converts that reviewable source into deterministic JSON consumed by
Jekyll.  Problems 111-127 retain their hand-composed versions in
``repertoire-raisonne.md``.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "scripts/data/repertoire_raisonne_mathjax.md"
DEFAULT_CATALOGUE = ROOT / "_data/repertoire_raisonne.json"
DEFAULT_OUTPUT = ROOT / "_data/repertoire_native_transcriptions.json"
PROBLEM_HEADING = re.compile(
    r"(?m)^(?P<hash>#{2,3}) Problème (?P<hash_number>\d+) [^\n]+$"
    r"|(?P<bold>\*\*Problème\s+(?P<bold_number>\d+))"
)
SOLUTION_MARKER = re.compile(r"\*\*Solution\.\*\*\s*")
PAGE_SEPARATOR = re.compile(r"(?m)^-{20,}\s*$")
PAGE_ANCHOR = re.compile(r'<span id="page-\d+-\d+"></span>')
STRUCTURAL_LINE = re.compile(
    r"(?m)^(?:#{1,6}\s+(?!Problème\b).+"
    r"|\*\*(?:Première|Deuxième) partie\b.*\*\*)\s*$"
)
MATH_SPAN = re.compile(r"\$\$.*?\$\$|\$(?!\$).*?\$", re.DOTALL)
DISPLAY_MATH = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)
UNORDERED_ITEM = re.compile(r"^[-*+]\s+(.+)$")
ORDERED_ITEM = re.compile(r"^\d+[.)]\s+(.+)$")
TABLE_DELIMITER = re.compile(r"^:?-{3,}:?$")
STATEMENT_START = re.compile(
    r"(?:Montrer|Soit|Soient|Calculer|Déterminer|Décrire|Donner|Construire|"
    r"Établir|Prouver|Trouver|Existe-t-il|Combien|Caractériser|Étudier|"
    r"On considère|On pose|Pour tout|Pour quelles|Que peut-on|À quelle|Quand)"
    r"\b"
)


def catalogue_entries(path: Path) -> dict[int, dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries: dict[int, dict[str, object]] = {}
    for part in data:
        for chapter in part["chapters"]:
            for number, title, page in chapter["problems"]:
                entries[number] = {
                    "number": number,
                    "title": title,
                    "pdfPage": page,
                    "chapterId": chapter["id"],
                    "chapterNumber": chapter["number"],
                    "chapterTitle": chapter["title"],
                    "partId": part["id"],
                }
    return entries


def clean_markdown(text: str) -> str:
    text = PAGE_SEPARATOR.sub("", text.replace("\r\n", "\n"))
    text = PAGE_ANCHOR.sub("", text)
    text = STRUCTURAL_LINE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s*□\s*$", "", text.strip())
    return text.strip()


def statement_start(heading: re.Match[str], chunk: str, number: int) -> int:
    if heading.group("hash"):
        return 0

    leading_offset = len(chunk) - len(chunk.lstrip())
    leading = chunk.lstrip()
    if not leading.startswith("**"):
        closing = leading.find("**")
        if closing < 0:
            raise ValueError(f"Problem {number} has no closing title marker")
        return leading_offset + closing + 2

    # Some pages style only the “Problème N” label in bold, leaving the title
    # and statement concatenated in the PDF layout.  The statement itself
    # always starts with one of the exercise verbs below.
    leading = leading[2:].lstrip()
    leading_offset = len(chunk) - len(leading)
    start = STATEMENT_START.search(leading)
    if start is None:
        raise ValueError(f"Problem {number} has no detectable statement start")
    return leading_offset + start.start()


def split_problems(source: str) -> dict[int, tuple[str, str]]:
    headings = list(PROBLEM_HEADING.finditer(source))
    extracted: dict[int, tuple[str, str]] = {}
    for index, heading in enumerate(headings):
        number = int(heading.group("hash_number") or heading.group("bold_number"))
        end = headings[index + 1].start() if index + 1 < len(headings) else len(source)
        chunk = source[heading.end() : end]
        solution_marker = SOLUTION_MARKER.search(chunk)
        if solution_marker is None:
            raise ValueError(f"Problem {number} has no Solution marker")
        start = statement_start(heading, chunk, number)
        statement = clean_markdown(chunk[start : solution_marker.start()])
        solution = clean_markdown(chunk[solution_marker.end() :])
        extracted[number] = (statement, solution)
    return extracted


def prose_markup(text: str) -> str:
    """Escape prose and render the small Markdown emphasis subset."""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def inline_markup(text: str) -> str:
    """Render prose without interpreting TeX asterisks as Markdown.

    Marker uses dollar delimiters for both inline and display mathematics.
    Expressions such as ``$A^*$`` and ``$f * g$`` must therefore be isolated
    before applying Markdown emphasis rules to the surrounding prose.
    """
    rendered: list[str] = []
    cursor = 0
    for match in MATH_SPAN.finditer(text):
        rendered.append(prose_markup(text[cursor : match.start()]))
        rendered.append(html.escape(match.group(0), quote=False))
        cursor = match.end()
    rendered.append(prose_markup(text[cursor:]))
    return "".join(rendered)


def table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_markdown_table(lines: list[str]) -> bool:
    if len(lines) < 2 or not all(line.startswith("|") for line in lines):
        return False
    delimiter = table_row(lines[1])
    return bool(delimiter) and all(
        TABLE_DELIMITER.fullmatch(cell.replace(" ", "")) for cell in delimiter
    )


def table_markup(lines: list[str]) -> str:
    header = table_row(lines[0])
    delimiter = table_row(lines[1])
    rows = [table_row(line) for line in lines[2:]]
    if len(delimiter) != len(header) or any(
        len(row) != len(header) for row in rows
    ):
        raise ValueError("Markdown table has inconsistent column counts")

    head = "".join(
        f'<th scope="col">{inline_markup(cell)}</th>' for cell in header
    )
    body = "".join(
        "<tr>"
        + "".join(f"<td>{inline_markup(cell)}</td>" for cell in row)
        + "</tr>"
        for row in rows
    )
    return (
        '<div class="repertoire-native-table-wrap"><table>'
        f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody>"
        "</table></div>"
    )


def list_markup(lines: list[str]) -> str | None:
    unordered = [UNORDERED_ITEM.fullmatch(line) for line in lines]
    ordered = [ORDERED_ITEM.fullmatch(line) for line in lines]
    if all(unordered):
        tag = "ul"
        matches = unordered
    elif all(ordered):
        tag = "ol"
        matches = ordered
    else:
        return None

    items = "".join(
        f"<li>{inline_markup(match.group(1))}</li>"
        for match in matches
        if match is not None
    )
    return f"<{tag}>{items}</{tag}>"


def markdown_to_mathjax_html(markdown: str) -> str:
    """Render the small, controlled Markdown subset emitted by Marker."""
    rendered: list[str] = []
    blocks = re.split(r"\n\s*\n", markdown.strip())
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if is_markdown_table(lines):
            rendered.append(table_markup(lines))
            continue
        rendered_list = list_markup(lines)
        if rendered_list is not None:
            rendered.append(rendered_list)
            continue
        compact = " ".join(lines)
        cursor = 0
        for match in DISPLAY_MATH.finditer(compact):
            prose = compact[cursor : match.start()].strip()
            if prose:
                rendered.append(f"<p>{inline_markup(prose)}</p>")
            equation = html.escape(match.group(1).strip(), quote=False)
            rendered.append(
                f'<div class="repertoire-native-equation">\\[{equation}\\]</div>'
            )
            cursor = match.end()
        prose = compact[cursor:].strip()
        if prose:
            rendered.append(f"<p>{inline_markup(prose)}</p>")
    return "".join(rendered)


def validate_math(number: int, field: str, markdown: str) -> None:
    if "$" in MATH_SPAN.sub("", markdown):
        raise ValueError(f"Problem {number} has unbalanced math delimiters in {field}")


def validate_transcription(
    number: int, field: str, markdown: str, rendered: str
) -> None:
    validate_math(number, field, markdown)
    if PAGE_ANCHOR.search(markdown) or re.search(r"(?m)^#{1,6}\s+", markdown):
        raise ValueError(f"Problem {number} contains page debris in {field}")
    if re.search(r"<p>\s*(?:\||[-*+]\s+|\d+[.)]\s+)", rendered):
        raise ValueError(f"Problem {number} contains unrendered Markdown in {field}")


def build(source: Path, catalogue: Path) -> list[dict[str, object]]:
    entries = catalogue_entries(catalogue)
    extracted = split_problems(source.read_text(encoding="utf-8"))

    expected = set(range(1, 128))
    if set(extracted) != expected:
        missing = sorted(expected - set(extracted))
        extra = sorted(set(extracted) - expected)
        raise ValueError(f"Transcription mismatch: missing={missing}, extra={extra}")

    output: list[dict[str, object]] = []
    for number in range(1, 111):
        statement, solution = extracted[number]
        statement_html = markdown_to_mathjax_html(statement)
        solution_html = markdown_to_mathjax_html(solution)
        validate_transcription(number, "statement", statement, statement_html)
        validate_transcription(number, "solution", solution, solution_html)
        item = dict(entries[number])
        item.update(
            {
                "statement": statement,
                "solution": solution,
                "statementMathjax": statement_html,
                "solutionMathjax": solution_html,
                "transcription": "Transcription mathématique issue du fac-similé",
            }
        )
        if len(statement) < 8:
            raise ValueError(f"Problem {number} has a suspiciously short statement")
        if len(solution) < 40:
            raise ValueError(f"Problem {number} has a suspiciously short solution")
        output.append(item)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--catalogue", type=Path, default=DEFAULT_CATALOGUE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the checked-in JSON is not the deterministic build output.",
    )
    args = parser.parse_args()

    payload = build(args.source, args.catalogue)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != serialized:
            raise SystemExit(
                f"{args.output} is stale; run {Path(__file__).name} to regenerate it"
            )
        print(f"Verified {len(payload)} native transcriptions in {args.output}")
        return

    args.output.write_text(serialized, encoding="utf-8")
    print(f"Wrote {len(payload)} native transcriptions to {args.output}")


if __name__ == "__main__":
    main()
