"""Check the punctuation family in all eight freshly built TTF faces."""
from pathlib import Path
from fontTools.ttLib import TTFont

DIST = Path(__file__).resolve().parents[1] / 'dist'
FAMILIES = ('Damonic', 'DamonicNerdFontMono')
STYLES = ('Regular', 'Italic', 'Bold', 'BoldItalic')

for family in FAMILIES:
    for style in STYLES:
        path = DIST / f'{family}-{style}.ttf'
        with TTFont(path) as f:
            names = [f.getBestCmap()[ord(c)] for c in ',;.:']
            comma, semi, period, colon = [f['glyf'][n] for n in names]
            # The tail is shared, and extends far enough below the dot to survive
            # downsampling. Do not enlarge the cell or move separator heads.
            assert comma.yMin == semi.yMin <= -150, (path.name, comma.yMin, semi.yMin)
            assert comma.yMax == 83 and semi.yMax == colon.yMax
            assert period.yMin == colon.yMin == 0
            assert all(f['hmtx'][n][0] == 600 for n in names)
            assert all(0 <= g.xMin < g.xMax <= 600 for g in (comma, semi))
print('Separator tails, related dot geometry and fixed advances passed in all eight faces.')
