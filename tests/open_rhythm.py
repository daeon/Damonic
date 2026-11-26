#!/usr/bin/env python3
"""Check the intended upright eye, arch channels, and cell-advance invariants."""
from pathlib import Path

from fontTools.pens.pointInsidePen import PointInsidePen
from fontTools.ttLib import TTFont

DIST = Path(__file__).resolve().parents[1] / 'dist'


def check_face(path, bold):
    with TTFont(path) as font:
        glyphs = font.getGlyphSet()
        cmap = font.getBestCmap()

        def ink(char, x, y):
            pen = PointInsidePen(glyphs, (x, y))
            glyphs[cmap[ord(char)]].draw(pen)
            return pen.getResult()

        for char in 'aceohmnrs':
            assert font['hmtx'][cmap[ord(char)]][0] == 600, (path.name, char)
        assert all(not ink('e', 275, y) for y in (299, 306, 312)), (path.name, 'e eye')
        assert ink('e', 275, 269) and ink('e', 275, 480), (path.name, 'e bar and top')
        arch_probe = 455 if bold else 472
        assert not ink('m', 203, arch_probe), (path.name, 'first m arch channel')
        assert not ink('m', 423, arch_probe), (path.name, 'second m arch channel')


def main():
    for family in ('Damonic', 'DamonicNerdFontMono'):
        for style in ('Regular', 'Bold'):
            path = DIST / f'{family}-{style}.ttf'
            check_face(path, style == 'Bold')
            print(f'{path.name}: open e eye and m arch channels, 600-unit advances')


if __name__ == '__main__':
    main()
