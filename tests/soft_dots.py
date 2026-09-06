#!/usr/bin/env python3
"""Focused HarfBuzz checks for soft-dotted i/j composition."""
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
STYLES = ("Regular", "Italic", "Bold", "BoldItalic")


def shape(font, text):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf)
    return list(zip(buf.glyph_infos, buf.glyph_positions))


def names(tt, rows):
    order = tt.getGlyphOrder()
    return [order[info.codepoint] for info, _ in rows]


def check(path):
    tt = TTFont(path, recalcBBoxes=False)
    font = hb.Font(hb.Face(path.read_bytes()))
    cmap = tt.getBestCmap()

    for base, dotless in (("i", "uni0131"), ("j", "uni0237")):
        rows = shape(font, base + "\u0301\u0301")
        got = names(tt, rows)
        # HarfBuzz may canonically compose the first acute (í) before ccmp;
        # either that no-dot precomposed glyph or the explicit dotless base is
        # correct, provided the dotted base never survives.
        assert got and got[0] in ({dotless, "uni00ED"} if base == "i" else {dotless}), (path.name, base, got)
        assert got[0] not in {cmap[ord(base)], "uni006A"}, (path.name, base, got)
        assert len(rows) >= 2 and rows[0][1].x_advance == 600, (path.name, base, rows)
        assert all(pos.x_advance == 0 for _, pos in rows[1:]), (path.name, base, rows)

    # A below mark alone does not trigger soft-dot suppression.  A below mark
    # between base and above mark is ignored by the filtered ccmp lookup.
    # Cedilla is used here because i-ogonek canonically composes to U+012F.
    keep = names(tt, shape(font, "i\u0327"))
    assert keep and keep[0] == cmap[ord("i")], (path.name, keep)
    filtered = names(tt, shape(font, "i\u0327\u030B"))
    assert filtered and filtered[0] == "uni0131", (path.name, filtered)


if __name__ == "__main__":
    for style in STYLES:
        check(ROOT / "dist" / f"Damonic-{style}.ttf")
    print("soft-dot checks passed")
