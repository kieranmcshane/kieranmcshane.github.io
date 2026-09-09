#!/usr/bin/env python3
"""Generate Open Graph preview images and sync page front matter."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images" / "social"
WIDTH = 1200
HEIGHT = 630

NOTES_COLORS = {
    "ink": "#172033",
    "muted": "#5d6778",
    "accent": "#3157c8",
    "teal": "#0d7580",
    "soft": "#f3f6ff",
    "white": "#ffffff",
    "card": "#ffffff",
    "border": "#d8dee4",
}

MAT101_COLORS = {
    "ink": "#172033",
    "muted": "#5d6778",
    "accent": "#006f7b",
    "accent_dark": "#04535c",
    "soft": "#edf8f8",
    "white": "#ffffff",
    "card": "#ffffff",
    "border": "#cad6dc",
    "highlight": "#2d7c7a",
}

MAT101_IMAGE = "/assets/images/og-mat101.png"
MAT101_IMAGE_ALT = "MAT101 — IMA02"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        font_path = Path(path)
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def normalize_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    return re.sub(r'(")\s*---\n', r"\1\n---\n", text, count=1)


def parse_front_matter(path: Path) -> tuple[str, dict[str, str], str]:
    text = normalize_front_matter(path.read_text(encoding="utf-8"))
    if not text.startswith("---"):
        return text, {}, text
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return text, {}, text
    body = text[match.end() :]
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return text, fields, body


def upsert_front_matter_field(text: str, key: str, value: str) -> str:
    text = normalize_front_matter(text)
    quoted_value = f'"{value}"' if not value.startswith('"') else value
    field_line = f"{key}: {quoted_value}"
    if not text.startswith("---"):
        return f"---\n{field_line}\n---\n{text}"
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return text
    front_matter = match.group(1)
    body = text[match.end() :]
    pattern = re.compile(rf"^{key}:.*(?:\n|$)", re.MULTILINE)
    if pattern.search(front_matter):
        front_matter = pattern.sub(field_line + "\n", front_matter, count=1)
    else:
        front_matter = front_matter.rstrip() + "\n" + field_line + "\n"
    front_matter = front_matter.rstrip() + "\n"
    return f"---\n{front_matter}---\n{body}"


def wrap_text(text: str, width: int) -> list[str]:
    wrapped = textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)
    return wrapped or [text]


def draw_notes_card(
    title: str,
    description: str,
    eyebrow: str,
    output_path: Path,
) -> None:
    colors = NOTES_COLORS
    image = Image.new("RGB", (WIDTH, HEIGHT), colors["soft"])
    draw = ImageDraw.Draw(image)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        red = int(0xF3 + (0xFF - 0xF3) * ratio)
        green = int(0xF6 + (0xFF - 0xF6) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(red, green, 255))

    draw.rounded_rectangle((56, 56, WIDTH - 56, HEIGHT - 56), radius=28, fill=colors["card"], outline=colors["border"], width=2)
    draw.rounded_rectangle((56, 56, WIDTH - 56, 112), radius=28, fill=colors["accent"])
    draw.rectangle((56, 84, WIDTH - 56, 112), fill=colors["accent"])

    eyebrow_font = load_font(28, bold=True)
    title_font = load_font(58, bold=True)
    body_font = load_font(34)
    footer_font = load_font(28, bold=True)

    draw.text((92, 78), eyebrow.upper(), fill=colors["white"], font=eyebrow_font)

    title_lines = wrap_text(title, 24)[:3]
    y = 156
    for line in title_lines:
        draw.text((92, y), line, fill=colors["ink"], font=title_font)
        y += 68

    description_lines = wrap_text(description, 42)[:3]
    y += 8
    for line in description_lines:
        draw.text((92, y), line, fill=colors["muted"], font=body_font)
        y += 46

    draw.text((92, HEIGHT - 108), "kieranmcshane.github.io", fill=colors["teal"], font=footer_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=True)


def draw_mat101_card(output_path: Path) -> None:
    colors = MAT101_COLORS
    image = Image.new("RGB", (WIDTH, HEIGHT), colors["soft"])
    draw = ImageDraw.Draw(image)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        red = int(0xED + (0xF7 - 0xED) * ratio)
        green = int(0xF8 + (0xFC - 0xF8) * ratio)
        blue = int(0xF8 + (0xFD - 0xF8) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(red, green, blue))

    draw.rounded_rectangle((56, 56, WIDTH - 56, HEIGHT - 56), radius=28, fill=colors["card"], outline=colors["border"], width=2)
    draw.rounded_rectangle((56, 56, WIDTH - 56, 128), radius=28, fill=colors["accent"])
    draw.rectangle((56, 100, WIDTH - 56, 128), fill=colors["accent"])
    draw.rounded_rectangle((WIDTH - 220, 148, WIDTH - 92, 220), radius=16, fill=colors["soft"], outline=colors["border"], width=2)

    eyebrow_font = load_font(28, bold=True)
    title_font = load_font(92, bold=True)
    body_font = load_font(34)
    footer_font = load_font(28, bold=True)
    badge_font = load_font(42, bold=True)

    draw.text((92, 82), "IMA02 · UVSQ", fill=colors["white"], font=eyebrow_font)
    draw.text((92, 168), "MAT101", fill=colors["ink"], font=title_font)

    description = (
        "19 séances, bibliothèque d'exercices et parcours étudiant "
        "pour les nombres complexes et la logique."
    )
    y = 292
    for line in wrap_text(description, 40)[:3]:
        draw.text((92, y), line, fill=colors["muted"], font=body_font)
        y += 46

    draw.text((WIDTH - 206, 176), "C", fill=colors["accent"], font=badge_font)
    draw.text((WIDTH - 168, 176), "∀", fill=colors["highlight"], font=badge_font)

    draw.text((92, HEIGHT - 108), "kieranmcshane.github.io/mat101", fill=colors["accent_dark"], font=footer_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=True)


def is_mat101_page(path: Path, fields: dict[str, str]) -> bool:
    layout = fields.get("layout", "").strip('"')
    if layout == "mat101" or fields.get("mat101_session", "").strip('"') in {"true", "True"}:
        return True
    if path.parent.name == "_mat101_sessions":
        return True
    if path.name in {"mat101-sessions.md", "mat101-exercises.md"}:
        return True
    if path.parent.name == "mat101":
        return True
    return page_url(path, fields).startswith("/mat101/")


def page_url(path: Path, fields: dict[str, str]) -> str:
    permalink = fields.get("permalink", "").strip('"')
    if permalink:
        return permalink if permalink.endswith("/") else f"{permalink}/"
    if path.parent.name == "_posts":
        date = fields.get("date", "2026-01-01").strip('"')[:10]
        slug = path.stem.split("-", 3)[-1] if path.name.count("-") >= 3 else path.stem
        year, month, day = date.split("-")
        return f"/{year}/{month}/{day}/{slug}/"
    if path.parent.name == "_mat101_sessions":
        return f"/mat101/seances/{path.stem}/"
    if path.name == "index.md":
        return "/"
    return f"/{path.stem}/"


def slug_for(path: Path, fields: dict[str, str]) -> str:
    url = page_url(path, fields).strip("/").replace("/", "-") or "home"
    return re.sub(r"[^a-zA-Z0-9-]+", "-", url).strip("-").lower()


def collect_pages() -> list[tuple[Path, dict[str, str], str]]:
    pages: list[tuple[Path, dict[str, str], str]] = []
    for pattern in ("_posts/*.md", "*.md", "_mat101_sessions/*.md", "mat101/index.md"):
        for path in sorted(ROOT.glob(pattern)):
            if path.name == "README.md":
                continue
            text, fields, _body = parse_front_matter(path)
            title = fields.get("title", "").strip('"')
            if not title:
                continue
            pages.append((path, fields, text))
    return pages


def cleanup_mat101_previews() -> None:
    for path in OUTPUT_DIR.glob("mat101*.png"):
        path.unlink(missing_ok=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    default_path = ROOT / "assets" / "images" / "og-default.png"
    mat101_path = ROOT / "assets" / "images" / "og-mat101.png"

    draw_notes_card(
        title="Kieran McShane: Notes",
        description="Research notes, mathematical writing, and interactive resources.",
        eyebrow="Notes",
        output_path=default_path,
    )
    draw_mat101_card(mat101_path)
    cleanup_mat101_previews()

    for path, fields, text in collect_pages():
        title = fields.get("title", "").strip('"')
        if is_mat101_page(path, fields):
            relative_image = MAT101_IMAGE
            image_alt = MAT101_IMAGE_ALT
        else:
            description = (
                fields.get("description", "").strip('"')
                or fields.get("excerpt", "").strip('"')
                or fields.get("subtitle", "").strip('"')
                or "Research notes, mathematical writing, and interactive resources."
            )
            slug = slug_for(path, fields)
            image_path = OUTPUT_DIR / f"{slug}.png"
            draw_notes_card(
                title=title,
                description=description,
                eyebrow=fields.get("layout", "page").strip('"').replace("_", " "),
                output_path=image_path,
            )
            relative_image = f"/assets/images/social/{slug}.png"
            image_alt = title

        updated = upsert_front_matter_field(text, "image", relative_image)
        updated = upsert_front_matter_field(updated, "image_alt", image_alt)
        path.write_text(updated, encoding="utf-8")

    print(f"Generated default preview at {default_path}")
    print(f"Generated MAT101 subsite preview at {mat101_path}")
    print(f"Generated {len(list(OUTPUT_DIR.glob('*.png')))} page previews in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
