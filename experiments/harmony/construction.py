"""Seven-glyph construction study for Damonic.

This is an isolated experiment.  It copies the supplied baseline fonts and
replaces only ``D a m o n i c``.  The lowercase set is built from one arch
vocabulary and one stroke system; the final x fitting keeps the baseline
glyph spans and the 600-unit cell constant so this study measures drawing.
"""
from pathlib import Path
import sys
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
import pathops

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import build  # safe: build() is protected by its __main__ guard

TARGET = "Damonic"


def specs(style):
    """Return coherent centreline specs, with a deliberate italic variant."""
    # The same shoulder curve appears in n, m, and the bowl turns of a/o/c.
    # It is deliberately flatter at the crown than the production baseline.
    upright = {
        "D": ["M102 0 L102 710", "M102 671 L278 671 C445 671 500 548 500 355 C500 162 445 39 278 39 L102 39"],
        "a": ["M130 395 C174 470 235 510 306 510 C422 510 474 445 474 334 L474 0", "M474 284 C425 315 360 326 292 326 C183 326 121 270 121 174 C121 78 179 29 271 29 C360 29 427 79 474 145"],
        "m": ["M82 0 L82 530", "M82 383 C118 468 160 510 211 510 C274 510 304 458 304 354 L304 0", "M304 383 C337 468 378 510 426 510 C490 510 520 458 520 354 L520 0"],
        "o": ["M300 510 C426 510 490 414 490 268 C490 122 426 29 300 29 C174 29 110 122 110 268 C110 414 174 510 300 510 Z"],
        "n": ["M122 0 L122 530", "M122 383 C166 468 228 510 303 510 C416 510 476 450 476 327 L476 0"],
        # Conventional stem, baseline foot, and one separated compact dot.
        "i": ["M90 491 L300 491 L300 39", "M110 39 L510 39", "M300 658 L300 735"],
        "c": ["M478 420 C438 476 380 510 304 510 C177 510 110 414 110 268 C110 122 180 29 306 29 C388 29 440 58 480 112"],
    }
    if style == "Bold Italic":
        # These are designed as italic skeletons first; the common shear is
        # applied below by outline(), giving the set a shared italic rhythm.
        upright.update({
            "D": ["M110 0 L110 710", "M110 671 L276 671 C442 671 503 548 503 355 C503 162 442 39 276 39 L110 39"],
            "a": ["M151 395 C190 466 245 510 310 510 C416 510 466 445 466 334 L466 0", "M466 284 C421 315 365 326 302 326 C203 326 148 270 148 174 C148 78 202 29 286 29 C367 29 426 79 466 145"],
            "m": ["M108 0 L108 530", "M108 383 C140 468 178 510 224 510 C281 510 308 458 308 354 L308 0", "M308 383 C338 468 376 510 420 510 C478 510 505 458 505 354 L505 0"],
            "o": ["M294 510 C411 510 470 414 470 268 C470 122 411 29 294 29 C181 29 122 122 122 268 C122 414 181 510 294 510 Z"],
            "n": ["M146 0 L146 530", "M146 383 C185 468 241 510 309 510 C414 510 466 450 466 327 L466 0"],
            "i": ["M95 483 L270 491 L270 135 C270 65 300 39 350 39 L510 39", "M270 658 L270 735"],
            "c": ["M457 420 C422 476 371 510 301 510 C184 510 130 414 130 268 C130 122 195 29 311 29 C386 29 431 58 466 112"],
        })
    return upright


def fit_x(g, target):
    """Fit outline xMin/xMax to target bounds while retaining its y design."""
    bp = BoundsPen(None)
    g.draw(bp, None)
    if not bp.bounds:
        return g
    x0, _, x1, _ = bp.bounds
    tx0, tx1 = target
    scale = (tx1 - tx0) / (x1 - x0)
    shift = tx0 - x0 * scale
    pen = TTGlyphPen(None)
    g.draw(TransformPen(pen, (scale, 0, 0, 1, shift, 0)), None)
    out = pen.glyph()
    out.recalcBounds(None)
    return out


def build_study(style, filename):
    baseline = TTFont(str(HERE / filename.replace("construction-", "baseline-")), recalcTimestamp=False)
    cmap = baseline.getBestCmap()
    glyphset = baseline.getGlyphSet()
    made = specs(style)
    weight = 108 if style == "Bold Italic" else 84
    for char in TARGET:
        name = cmap[ord(char)]
        # Preserve the actual baseline glyf bounds, including the italic
        # design's integer coordinate extrema.
        refpen = BoundsPen(baseline.getGlyphSet())
        baseline.getGlyphSet()[name].draw(refpen)
        target = (refpen.bounds[0], refpen.bounds[2])
        # italic=True applies the controlled 9-degree construction shear.
        stroke = weight * (0.78 if char == "m" else 1.0)
        p = build.outline(made[char], weight=stroke, italic=(style == "Bold Italic"))
        g = build.glyph(p)
        g = fit_x(g, target)
        baseline["glyf"][name] = g
        baseline["hmtx"][name] = (600, g.xMin)
    # Family naming is intentionally unique so the study cannot collide with
    # installed Damonic faces.  All non-target glyphs/tables remain baseline.
    suffix = "Harmony Construction"
    family = f"Damonic {suffix}"
    subfamily = style
    ids = {1, 2, 3, 4, 6, 16, 17}
    baseline["name"].names = [n for n in baseline["name"].names if n.nameID not in ids]
    values = {1: family, 2: subfamily, 3: f"{family} {subfamily}",
              4: f"{family} {subfamily}", 6: f"Damonic-HarmonyConstruction-{style.replace(' ', '')}",
              16: family, 17: subfamily}
    for platform, encoding, language in ((1, 0, 0), (3, 1, 0x409)):
        for nid, value in values.items():
            baseline["name"].setName(value, nid, platform, encoding, language)
    baseline.save(str(HERE / filename))
    baseline.close()


if __name__ == "__main__":
    build_study("Regular", "construction-Regular.ttf")
    build_study("Bold Italic", "construction-BoldItalic.ttf")
    print("built construction-Regular.ttf and construction-BoldItalic.ttf")
