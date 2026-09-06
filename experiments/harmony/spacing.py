"""Build the bounded Damonic harmony spacing study.

The study changes only the seven lowercase/uppercase glyphs in ``Damonic``.
Advances remain 600 units and no kerning or tracking data is introduced.
"""

from __future__ import annotations

from pathlib import Path
from shutil import copyfile

from fontTools.ttLib import TTFont


HERE = Path(__file__).resolve().parent
GLYPHS = "Damonic"
ADVANCE = 600

# Target black widths and nominal left sidebearings, in font units.  The
# regular targets gently pull the very wide m inward and give n/i/c a little
# more room.  The italic targets are deliberately bounded more tightly because
# their slanted overhangs currently produce very large n-i and i-c gaps.
STUDY = {
    "baseline-Regular.ttf": {
        "output": "spacing-Regular.ttf",
        "widths": {"D": 470, "a": 455, "m": 475, "o": 465, "n": 455, "i": 455, "c": 455},
        "lsbs": {"D": 64, "a": 66, "m": 63, "o": 66, "n": 68, "i": 68, "c": 66},
        "family": "Damonic Harmony Study",
        "subfamily": "Regular",
    },
    "baseline-BoldItalic.ttf": {
        "output": "spacing-BoldItalic.ttf",
        "widths": {"D": 500, "a": 490, "m": 495, "o": 490, "n": 490, "i": 470, "c": 490},
        "lsbs": {"D": 45, "a": 52, "m": 48, "o": 52, "n": 52, "i": 65, "c": 52},
        "family": "Damonic Harmony Study",
        "subfamily": "Bold Italic",
    },
}


def _set_name(name_table, name_id: int, value: str) -> None:
    """Replace all platform/language records for a name ID consistently."""
    records = [record for record in name_table.names if record.nameID == name_id]
    if not records:
        name_table.setName(value, name_id, 3, 1, 0x409)
        return
    for record in records:
        name_table.setName(value, name_id, record.platformID, record.platEncID, record.langID)


def _transform_glyph(font: TTFont, glyph_name: str, target_width: float, target_lsb: int) -> None:
    glyf = font["glyf"]
    glyph = glyf[glyph_name]
    coordinates, end_points, flags = glyph.getCoordinates(glyf)
    if glyph.numberOfContours < 0:
        raise ValueError(f"{glyph_name} is composite; this bounded study expects simple outlines")

    # Use the actual outline bounds as the transform anchor.  This keeps the
    # curve treatment intact while changing only horizontal proportion and
    # placement.  Y coordinates, instructions, and contour topology remain.
    xmin = min(point[0] for point in coordinates)
    xmax = max(point[0] for point in coordinates)
    source_width = xmax - xmin
    if source_width <= 0:
        raise ValueError(f"{glyph_name} has no usable horizontal extent")
    scale = target_width / source_width
    transformed = coordinates.copy()
    for index, point in enumerate(transformed):
        transformed[index] = ((point[0] - xmin) * scale + target_lsb, point[1])
    glyph.coordinates = transformed
    glyph.endPtsOfContours = end_points
    glyph.flags = flags
    glyph.recalcBounds(glyf)
    font["hmtx"][glyph_name] = (ADVANCE, target_lsb)


def build(input_path: Path, output_path: Path, family: str, subfamily: str, widths, lsbs) -> None:
    copyfile(input_path, output_path)
    font = TTFont(output_path, recalcTimestamp=False)
    cmap = font.getBestCmap()
    for character in GLYPHS:
        glyph_name = cmap[ord(character)]
        _transform_glyph(font, glyph_name, widths[character], lsbs[character])

    # A distinct family name prevents accidentally installing this pilot over
    # the production Damonic family.  Name IDs 1/4/6 are the visible identity;
    # IDs 16/17 are updated when present for newer naming systems.
    _set_name(font["name"], 1, family)
    _set_name(font["name"], 2, subfamily)
    _set_name(font["name"], 3, f"{family}-{subfamily}-harmony-pilot")
    _set_name(font["name"], 4, f"{family} {subfamily}")
    _set_name(font["name"], 6, f"Damonic-HarmonyStudy-{subfamily.replace(' ', '')}")
    _set_name(font["name"], 16, family)
    _set_name(font["name"], 17, subfamily)
    font.save(output_path)


def main() -> None:
    for baseline, spec in STUDY.items():
        build(HERE / baseline, HERE / spec["output"], spec["family"], spec["subfamily"], spec["widths"], spec["lsbs"])


if __name__ == "__main__":
    main()
