"""Regression checks for the optically inset upright diagonal capitals."""
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1] / "dist"
# At least 34 units of side space, including the widest Bold W.
for family in ("Damonic", "DamonicNerdFontMono"):
    for style in ("Regular", "Bold"):
        with TTFont(ROOT / f"{family}-{style}.ttf") as font:
            cmap = font.getBestCmap()
            for char, contours in (("A", 2), ("V", 1), ("W", 1), ("Y", 1)):
                name = cmap[ord(char)]
                glyph = font["glyf"][name]
                assert font["hmtx"][name][0] == 600, (family, style, char, "cell")
                assert glyph.numberOfContours == contours, (family, style, char, "topology")
                assert 34 <= glyph.xMin < glyph.xMax <= 566, (family, style, char, "inset")
                if char != "W":
                    assert 48 <= glyph.xMin and glyph.xMax <= 552, (family, style, char, "inset")
                if char == "A":
                    assert glyph.endPtsOfContours[-1] > glyph.endPtsOfContours[0], (family, style)
print("Diagonal capitals verified in four upright faces.")
