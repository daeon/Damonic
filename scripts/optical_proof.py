#!/usr/bin/env python3
"""Make reproducible, side-by-side small-size optical proofs for Damonic.

The proof uses Pillow/FreeType to render the supplied TTFs at the requested
pixel sizes. It intentionally keeps text and colors fixed so before/after
comparisons show optical changes rather than specimen changes.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

STYLES = ("Regular", "Italic", "Bold", "BoldItalic")
SIZES = (12, 14, 16, 18, 20)
TEXT_LINES = (
    "ri  ir  in  ni  rn  nr",
    "minimum  printing  return",
    "‘single’  “double”  ‘quoted’",
    ".,:;!?  ()[]{}  /\\|  <>  -_=+  *#@%&",
    "a  e  s  o  b  d  p  q",
)
THEMES = (
    ("light", "#f5f3ed", "#182520", "#49645a"),
    ("dark", "#18231f", "#eef2e9", "#9bb8aa"),
)


def font_path(directory: Path, style: str) -> Path:
    # Accept either the checked-in Damonic names or the old Bearing-like names
    # used by early local proofs, while still rendering the actual TTF.
    candidates = (directory / f"Damonic-{style}.ttf", directory / f"BearingMono-{style}.ttf")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"no {style} TTF in {directory} (looked for {', '.join(p.name for p in candidates)})")


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def draw_version(draw: ImageDraw.ImageDraw, origin: tuple[int, int], directory: Path, label: str, panel_width: int) -> int:
    x0, y0 = origin
    draw.text((x0, y0), label, fill="#d07c45" if label == "BEFORE" else "#53b58a", font=ImageFont.truetype("DejaVuSans-Bold.ttf", 22))
    y = y0 + 38
    for style in STYLES:
        path = font_path(directory, style)
        draw.text((x0, y), style, fill="#a7b5ad", font=ImageFont.truetype("DejaVuSans-Bold.ttf", 15))
        y += 25
        for size in SIZES:
            for theme, bg, ink, muted in THEMES:
                # Each row is independently themed, making light/dark raster
                # differences visible without blending the two backgrounds.
                row_h = len(TEXT_LINES) * (size + 7) + 33
                draw.rectangle((x0, y, x0 + panel_width, y + row_h), fill=bg)
                draw.text((x0 + 10, y + 7), f"{size}px {theme}", fill=muted, font=ImageFont.truetype("DejaVuSans.ttf", 12))
                font = load_font(path, size)
                baseline = y + 25
                for line in TEXT_LINES:
                    draw.text((x0 + 125, baseline), line, fill=ink, font=font)
                    baseline += size + 7
                y += row_h + 8
            y += 7
        y += 18
    return y


def render(before: Path | None, after: Path | None, output: Path) -> None:
    versions = [("BEFORE", before), ("AFTER", after)]
    versions = [(label, path) for label, path in versions if path is not None]
    if not versions:
        raise ValueError("provide --before and/or --after")
    panel_width = 930
    top = 36
    # Fixed dimensions make generated proofs stable for review and diffing.
    panel_height = 4 * (38 + 25 + 5 * (2 * (len(TEXT_LINES) * (20 + 7) + 33 + 8) + 7 + 18)) + 100
    width = len(versions) * panel_width + (len(versions) + 1) * 24
    height = panel_height
    image = Image.new("RGB", (width, height), "#101714")
    draw = ImageDraw.Draw(image)
    for index, (label, directory) in enumerate(versions):
        assert directory is not None
        x = 24 + index * (panel_width + 24)
        draw_version(draw, (x, top), directory, label, panel_width)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def render_overview(before: Path | None, after: Path | None, output: Path) -> None:
    """Render a compact review sheet at 16, 20 and 40 px."""
    versions = [("BEFORE", before), ("AFTER", after)]
    versions = [(label, path) for label, path in versions if path is not None]
    # 40px text needs a wide cell to keep the complete specimen visible.
    panel_width = 900
    cell_width = 290
    cell_h = 5 * (40 + 8) + 34
    style_h = 2 * cell_h + 5 + 22
    width = len(versions) * (panel_width + 28) + 28
    height = 4 * style_h + 80
    image = Image.new("RGB", (width, height), "#101714")
    draw = ImageDraw.Draw(image)
    heading = ImageFont.truetype("DejaVuSans-Bold.ttf", 21)
    small = ImageFont.truetype("DejaVuSans.ttf", 12)
    for vi, (label, directory) in enumerate(versions):
        assert directory is not None
        vx = 18 + vi * (panel_width + 28)
        draw.text((vx, 14), label, fill="#d07c45" if label == "BEFORE" else "#53b58a", font=heading)
        for si, style in enumerate(STYLES):
            y0 = 48 + si * style_h
            draw.text((vx, y0), style, fill="#a7b5ad", font=small)
            path = font_path(directory, style)
            for size_index, size in enumerate((16, 20, 40)):
                x = vx + size_index * (cell_width + 10)
                y = y0 + 22
                for theme, bg, ink, muted in THEMES:
                    h = cell_h
                    draw.rectangle((x, y, x + cell_width, y + h), fill=bg)
                    draw.text((x + 8, y + 7), f"{size}px {theme}", fill=muted, font=small)
                    font = load_font(path, size)
                    baseline = y + 24
                    # Keep the overview legible at 20/40px; the full matrix
                    # carries the complete punctuation and phrase specimen.
                    lines = (
                        ("ri  ir  in  ni  rn  nr", "minimum", "printing", "return", "a  e  s  o  b  d  p  q")
                        if size < 40 else ("ri  in", "rn  nr", "minimum", "return")
                    )
                    for line in lines:
                        draw.text((x + 8, baseline), line, fill=ink, font=font)
                        baseline += size + 8
                    y += h + 5
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, help="directory containing baseline style TTFs")
    parser.add_argument("--after", type=Path, help="directory containing candidate style TTFs")
    parser.add_argument("--out", type=Path, default=Path("docs/optical-proof.png"), help="output PNG")
    parser.add_argument("--overview", type=Path, help="also write a compact 16/20/40px overview PNG")
    args = parser.parse_args(argv)
    render(args.before, args.after, args.out)
    if args.overview:
        render_overview(args.before, args.after, args.overview)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
