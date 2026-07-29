#!/usr/bin/env python3
"""Extract the first 110 Répertoire problems into reviewable native data.

The PDF remains the primary source.  This script uses Poppler's reading-order
extraction, keeps mathematical Unicode glyphs, and emits deterministic JSON
consumed by Jekyll.  Problems 111-127 retain their hand-composed MathJax
versions in ``repertoire-raisonne.md``.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "assets/documents/repertoire-raisonne-algebre-analyse.pdf"
DEFAULT_CATALOGUE = ROOT / "_data/repertoire_raisonne.json"
DEFAULT_OUTPUT = ROOT / "_data/repertoire_native_transcriptions.json"


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


def extract_raw_text(pdf: Path) -> str:
    with tempfile.TemporaryDirectory(prefix="repertoire-native-") as temp_dir:
        output = Path(temp_dir) / "repertoire.txt"
        subprocess.run(
            ["pdftotext", "-raw", str(pdf), str(output)],
            check=True,
            capture_output=True,
            text=True,
        )
        return output.read_text(encoding="utf-8")


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    # Page numbers immediately precede Poppler's form-feed marker.  Remove
    # only those numbers, never standalone digits that belong to a displayed
    # fraction or exponent.
    text = re.sub(r"\n\s*\d+\s*\f", "\n\f", text)
    text = re.sub(r"\f[^\n]*\n", "\n", text)
    text = text.translate(
        {
            ord("\x01"): "",
            ord("\x02"): "[",
            ord("\x03"): "]",
            ord("\x08"): "{",
            ord("\x12"): "(",
            ord("\x13"): ")",
            ord("\x14"): "[",
            ord("\x15"): "]",
            ord("Ö"): "∏",
            ord("Õ"): "∑",
            ord("Í"): "∑",
            ord("Ø"): "∪",
            ord("\x9a"): "^",
        }
    )
    # Poppler can expose delimiter glyphs as PDF control codes.  Keep line
    # breaks and tabs, but never let an unhandled control character reach
    # Jekyll's YAML-backed JSON reader.
    text = "".join(
        character
        for character in text
        if character in "\n\t" or not unicodedata.category(character).startswith("C")
    )
    text = re.sub(r"(?m)^\s*\d+\s+[^\n]+\s+\d+\s*$", "", text)
    text = re.sub(r"(?m)^CHAPITRE\s+\d+\s*$", "", text)
    text = re.sub(r"(?m)^(Première|Deuxième) partie.*$", "", text)
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s*□\s*$", "", text.strip())
    return text.strip()


def split_problems(raw_text: str) -> dict[int, tuple[str, str]]:
    corpus = raw_text[raw_text.index("Problème 1 ") :]
    parts = re.split(r"(?m)^Problème (\d+) ", corpus)
    extracted: dict[int, tuple[str, str]] = {}
    for index in range(1, len(parts), 2):
        number = int(parts[index])
        chunk = parts[index + 1]
        heading_and_statement, separator, solution = chunk.partition("Solution.")
        if not separator:
            raise ValueError(f"Problem {number} has no Solution marker")

        heading_lines = heading_and_statement.splitlines()
        if len(heading_lines) < 2:
            raise ValueError(f"Problem {number} has no extracted statement")
        statement = "\n".join(heading_lines[1:])

        solution = re.split(
            r"\fCHAPITRE|\nCHAPITRE|\f(?:Première|Deuxième) partie",
            solution,
            maxsplit=1,
        )[0]
        extracted[number] = (clean_text(statement), clean_text(solution))
    return extracted


def reviewed_overrides() -> dict[int, dict[str, str]]:
    return {
        80: {
            "statement": (
                "Soit f ∈ C([0,1], ℂ) telle que\n\n"
                "∫₀¹ xⁿ f(x) dx = 0  pour tout n ∈ ℕ.\n\n"
                "Montrer que f = 0."
            ),
            "solution": (
                "Par linéarité, l’intégrale de fP est nulle pour tout polynôme "
                "complexe P. Le théorème de Weierstrass fournit une suite de "
                "polynômes Pₖ convergeant uniformément vers la fonction conjuguée "
                "de f sur [0,1]. Dès lors,\n\n"
                "0 = limₖ ∫₀¹ f(x)Pₖ(x) dx = ∫₀¹ |f(x)|² dx.\n\n"
                "La continuité de f entraîne f = 0 sur tout l’intervalle."
            )
        }
    }


def repair_pdf_word_spacing(text: str) -> str:
    """Repair the few words whose spaces are absent from the PDF text layer."""
    replacements = {
        "Sil’égalitéestatteinte,touteslesinégalitéssontdeségalités.Leslignessontdoncorthonormées,":
            "Si l’égalité est atteinte, toutes les inégalités sont des égalités. "
            "Les lignes sont donc orthonormées,",
        "lesracinesdistinctesde𝑃,demultiplicités𝑚1,":
            "les racines distinctes de 𝑃, de multiplicités 𝑚1,",
        "Notons𝜆1,": "Notons 𝜆1,",
        "𝑚𝑟.Choisissons": "𝑚𝑟. Choisissons",
        "convergencedescoefficientsentraînelaconvergenceuniformedespolynômessurtoutcompact.":
            "convergence des coefficients entraîne la convergence uniforme des polynômes sur tout compact.",
        "Cesfonctionssontholomorphesdansledemi-planinférieur:surtoutcompactdecedemi-plan,":
            "Ces fonctions sont holomorphes dans le demi-plan inférieur : sur tout compact de ce demi-plan,",
        "Réciproquement,sitouslescoefficientsdeFourierde":
            "Réciproquement, si tous les coefficients de Fourier de",
        "Comme1/(2𝜋)estirrationnel,lethéorèmedesrotationsirrationnellesaffirmequelesclasses":
            "Comme 1/(2𝜋) est irrationnel, le théorème des rotations irrationnelles affirme que les classes",
    }
    for compact, spaced in replacements.items():
        text = text.replace(compact, spaced)
    return text


def build(pdf: Path, catalogue: Path) -> list[dict[str, object]]:
    entries = catalogue_entries(catalogue)
    extracted = split_problems(extract_raw_text(pdf))
    overrides = reviewed_overrides()

    expected = set(range(1, 128))
    if set(extracted) != expected:
        missing = sorted(expected - set(extracted))
        extra = sorted(set(extracted) - expected)
        raise ValueError(f"Extraction mismatch: missing={missing}, extra={extra}")

    output: list[dict[str, object]] = []
    for number in range(1, 111):
        statement, solution = extracted[number]
        statement = repair_pdf_word_spacing(statement)
        solution = repair_pdf_word_spacing(solution)
        item = dict(entries[number])
        item.update(
            {
                "statement": statement,
                "solution": solution,
                "transcription": "Transcription textuelle issue du fac-similé",
            }
        )
        item.update(overrides.get(number, {}))
        if len(str(item["statement"])) < 8:
            raise ValueError(f"Problem {number} has a suspiciously short statement")
        if len(str(item["solution"])) < 40:
            raise ValueError(f"Problem {number} has a suspiciously short solution")
        output.append(item)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--catalogue", type=Path, default=DEFAULT_CATALOGUE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    payload = build(args.pdf, args.catalogue)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(payload)} native transcriptions to {args.output}")


if __name__ == "__main__":
    main()
