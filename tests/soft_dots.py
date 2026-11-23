#!/usr/bin/env python3
"""Focused HarfBuzz checks for soft-dotted i/j composition."""
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
STYLES = ("Regular", "Italic", "Bold", "BoldItalic")


def shape(font, text, language=None, features=None):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    if language is not None:
        buf.language = language
    hb.shape(font, buf, features)
    return list(zip(buf.glyph_infos, buf.glyph_positions))


def names(tt, rows):
    order = tt.getGlyphOrder()
    return [order[info.codepoint] for info, _ in rows]


def check_i_ogonek(path, tt, font):
    cmap = tt.getBestCmap()
    encoded = cmap[0x012F]
    dotless = "uni012F.dotless"
    glyf = tt["glyf"]

    def contours(glyph):
        points, ends, _ = glyf[glyph].getCoordinates(glyf)
        starts = [0] + [end + 1 for end in ends[:-1]]
        return {tuple(points[start:end + 1]) for start, end in zip(starts, ends)}

    # The repair restores the exact native i dot, not just a taller bound.
    i_dot = contours(cmap[ord("i")]) - contours(cmap[0x0131])
    assert len(i_dot) == 1, (path.name, i_dot)
    assert i_dot <= contours(encoded), (path.name, "encoded i-ogonek is missing its native dot")
    assert dotless in glyf and dotless not in cmap.values(), path.name
    assert contours(encoded) == contours(dotless) | i_dot, path.name
    assert not contours(dotless) & i_dot, path.name

    def trace(text, language, features=None):
        rows = shape(font, text, language, features)
        return [(glyph, pos.x_advance, pos.y_advance, pos.x_offset, pos.y_offset)
                for glyph, (_, pos) in zip(names(tt, rows), rows)]

    for lang in ("lt", "en", "und"):
        plain = trace("\u012f", lang)
        assert plain == trace("i\u0328", lang) == [(encoded, 600, 0, 0, 0)], (path.name, lang, plain)
        assert trace("\u012frašas.txt", lang) == trace("i\u0328ras\u030cas.txt", lang), (path.name, lang)
        below = trace("\u012f\u0327", lang)
        assert below[0][0] == encoded and below[1][1] == 0 and below[1][4] < 0, (path.name, lang, below)
        acute = trace("\u012f\u0301", lang)
        assert acute == trace("i\u0301\u0328", lang), (path.name, lang, acute)
        assert [row[0] for row in acute] == [dotless, cmap[0x0301]], (path.name, lang, acute)
        assert [row[1] for row in acute] == [600, 0] and acute[1][4] >= 0, (path.name, lang, acute)
        for accent in ("\u0301", "\u0303"):
            explicit = trace("\u012f\u0307" + accent, lang)
            assert explicit == trace("i\u0328\u0307" + accent, lang), (path.name, lang, explicit)
            assert explicit == trace("i\u0307" + accent + "\u0328", lang), (path.name, lang, explicit)
            assert [row[0] for row in explicit] == [dotless, cmap[0x0307], cmap[ord(accent)]], (path.name, lang, explicit)
            assert [row[1] for row in explicit] == [600, 0, 0], (path.name, lang, explicit)
            assert explicit[2][4] > explicit[1][4], (path.name, lang, explicit)
        # A below mark can intervene in ccmp and must still attach to the
        # unencoded alternate. Its anchor would be missing in a cmap-only loop.
        both = trace("\u012f\u0327\u0301", lang)
        assert [row[0] for row in both] == [dotless, cmap[0x0327], cmap[0x0301]], (path.name, lang, both)
        assert both[1][4] < 0, (path.name, lang, both)


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
    check_i_ogonek(path, tt, font)


if __name__ == "__main__":
    for style in STYLES:
        check(ROOT / "dist" / f"Damonic-{style}.ttf")
    print("soft-dot checks passed")
