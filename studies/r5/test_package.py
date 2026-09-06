"""Engineering regression checks. Does not score aesthetics or native IDE behavior."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from fontTools.ttLib import TTFont
from PIL import ImageFont, features
from build import CHARACTERS, FAMILY, SOURCE_SHA, build_font, digest, inspect_font, load_source, source_bytes


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.data, cls.raw = load_source()
        cls.font = cls.root / 'one.ttf'
        build_font(cls.data, cls.font)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_accepted_source_checksum(self):
        self.assertEqual(digest(self.raw), SOURCE_SHA)

    def test_exact_coverage(self):
        with TTFont(self.font) as font:
            self.assertEqual(set(font.getBestCmap()), {ord(c) for c in CHARACTERS})
            self.assertEqual(len(font.getBestCmap()), 42)

    def test_no_fake_ascii_completion(self):
        with TTFont(self.font) as font:
            for ch in 'ABCEFGH{}[]();.,+-=':
                self.assertNotIn(ord(ch), font.getBestCmap())

    def test_distinct_family(self):
        with TTFont(self.font) as font:
            self.assertEqual(font['name'].getDebugName(1), FAMILY)
            self.assertNotEqual(font['name'].getDebugName(1), 'Damonic')
            self.assertEqual(font['name'].getDebugName(17), 'Regular')

    def test_metrics_and_bounds(self):
        report = inspect_font(self.font, self.data)
        self.assertEqual(report['advance_units'], 600)
        self.assertEqual(report['units_per_em'], 1000)

    def test_space_is_empty(self):
        with TTFont(self.font) as font:
            self.assertEqual(font['glyf']['space'].numberOfContours, 0)
            self.assertEqual(font['hmtx']['space'], (600, 0))

    def test_notdef_is_visible(self):
        self.assertIsNotNone(ImageFont.truetype(str(self.font), 20).getmask('A').getbbox())

    def test_no_synthetic_features_or_hinting(self):
        with TTFont(self.font) as font:
            for table in ['kern', 'GPOS', 'GSUB', 'fvar', 'fpgm', 'prep']:
                self.assertNotIn(table, font)
            self.assertTrue(all(not getattr(g, 'program', None) or not g.program.getBytecode()
                                for g in font['glyf'].glyphs.values()))

    def test_license_and_style_metadata(self):
        with TTFont(self.font) as font:
            self.assertIn('Open Font License', font['name'].getDebugName(13))
            self.assertEqual(font['OS/2'].fsType, 0)
            self.assertEqual(font['OS/2'].usWeightClass, 400)
            self.assertEqual(font['head'].macStyle, 0)

    def test_reproducible_ttf(self):
        other = self.root / 'two.ttf'
        build_font(self.data, other)
        self.assertEqual(self.font.read_bytes(), other.read_bytes())

    def test_woff2_roundtrip(self):
        path = self.root / 'roundtrip.woff2'
        with TTFont(self.font, recalcTimestamp=False) as font:
            font.flavor = 'woff2'
            font.save(path)
        with TTFont(self.font) as a, TTFont(path) as b:
            self.assertEqual(a.getBestCmap(), b.getBestCmap())
            self.assertEqual(a['hmtx'].metrics, b['hmtx'].metrics)
            for name in a.getGlyphOrder():
                self.assertEqual(a['glyf'][name], b['glyf'][name])

    def test_native_size_rasterization(self):
        checks = 0
        for size in [12, 14, 16, 18, 20, 24]:
            font = ImageFont.truetype(str(self.font), size)
            for ch in CHARACTERS:
                if ch != ' ':
                    self.assertIsNotNone(font.getmask(ch).getbbox(), (size, ch))
                    checks += 1
        self.assertEqual(checks, 246)

    def test_fixed_width_supported_strings(self):
        for size in [12, 16, 24]:
            font = ImageFont.truetype(str(self.font), size)
            for text in ['minimum priority', 'ri ir rn nr in ni ii rr', 'assign signal', CHARACTERS]:
                self.assertAlmostEqual(font.getlength(text), len(text) * font.getlength('i'), places=4)

    def test_preserves_source_bytes(self):
        self.assertEqual(source_bytes(), self.raw)

    def test_edited_source_requires_explicit_input(self):
        edited = json.loads(self.raw)
        edited['study'] = 'Local edited copy'
        path = self.root / 'edited.json'
        path.write_text(json.dumps(edited))
        data, raw = load_source(path)
        self.assertEqual(data['glyphs'], self.data['glyphs'])
        self.assertNotEqual(digest(raw), SOURCE_SHA)

    def test_reject_invalid_coverage(self):
        edited = json.loads(self.raw)
        del edited['glyphs']['i']
        path = self.root / 'invalid.json'
        path.write_text(json.dumps(edited))
        with self.assertRaises(ValueError):
            load_source(path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
