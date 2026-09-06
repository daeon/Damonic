#!/usr/bin/env python3
"""Build the exact R5 study; no production glyphs, fallback or synthetic styles.

The compressed JSON is a lossless transport copy of the accepted drawing.
Use --extract-source to produce an ordinary editable JSON file. The source
archive always contains the uncompressed JSON. Outputs are deterministic
with the pinned toolchain. All requested checks must pass before packaging.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import fontTools
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
FAMILY = 'Damonic R5 Study'
STEM = 'DamonicR5Study-Regular'
VERSION = '0.5.0-alpha.5'
SOURCE_SHA = '52bdb8e62d0c8c5c1d2cfd0a3e60dfa65d7363c605d64086f90879e9947c6765'
CHARACTERS = ' !0123456789DIOabcdefghijklmnopqrstuvwxyz|'
STAMP = 3861043200


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_bytes(source: Path | None = None) -> bytes:
    if source is not None:
        return source.read_bytes()
    raw = HERE / 'R5-outlines.json'
    packed = HERE / 'R5-outlines.json.xz'
    return raw.read_bytes() if raw.exists() else lzma.decompress(packed.read_bytes())


def load_source(source: Path | None = None) -> tuple[dict, bytes]:
    raw = source_bytes(source)
    if source is None and digest(raw) != SOURCE_SHA:
        raise ValueError('R5 source checksum mismatch; refusing a substituted drawing')
    data = json.loads(raw)
    if data['units_per_em'] != 1000 or data['advance_width'] != 600:
        raise ValueError('R5 requires 1000 UPM and 600-unit cells')
    if set(data['glyphs']) != set(CHARACTERS) or data['glyphs'][' '] != '':
        raise ValueError('Unexpected R5 character coverage')
    return data, raw


def build_font(data: dict, destination: Path) -> None:
    fb = FontBuilder(1000, isTTF=True)
    names = {c: 'space' if c == ' ' else f'uni{ord(c):04X}' for c in CHARACTERS}
    order = ['.notdef', *names.values()]
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({ord(c): name for c, name in names.items()})
    outlines, metrics = {}, {}
    # Visible hollow missing-character marker; never pretend it is coverage.
    notdef = 'M80 0L80 710L520 710L520 0ZM140 60L460 60L460 650L140 650Z'
    for name, svg in [('.notdef', notdef), *[(names[c], data['glyphs'][c]) for c in CHARACTERS]]:
        pen = TTGlyphPen(None)
        if svg:
            parse_path(svg, Cu2QuPen(pen, max_err=0.35, reverse_direction=False))
        glyph = pen.glyph()
        glyph.recalcBounds(None)
        outlines[name] = glyph
        metrics[name] = (600, glyph.xMin if glyph.numberOfContours else 0)
    fb.setupGlyf(outlines)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-270, lineGap=0)
    fb.setupNameTable({
        'familyName': FAMILY, 'styleName': 'Regular',
        'typographicFamily': FAMILY, 'typographicSubfamily': 'Regular',
        'fullName': FAMILY + ' Regular', 'psName': STEM,
        'uniqueFontIdentifier': VERSION + ';Damonic;' + STEM,
        'version': 'Version 0.500; R5 experimental study',
        'copyright': 'Copyright 2026 Damonic contributors.',
        'licenseDescription': 'Licensed under the SIL Open Font License, Version 1.1.',
        'licenseInfoURL': 'https://openfontlicense.org/',
        'description': '42-character Regular study. Incomplete ASCII. No icons, ligatures or other styles.',
        'sampleText': 'Damonic minimum priority assign signal',
    })
    fb.setupOS2(version=4, sTypoAscender=900, sTypoDescender=-270, sTypoLineGap=0,
                usWinAscent=900, usWinDescent=270, sxHeight=530, sCapHeight=710,
                usWeightClass=400, usWidthClass=5, fsType=0, fsSelection=0xC0,
                achVendID='DMNC', xAvgCharWidth=600)
    fb.font['OS/2'].panose.bProportion = 9
    fb.setupPost(isFixedPitch=1)
    fb.setupMaxp()
    fb.font['head'].created = fb.font['head'].modified = STAMP
    fb.font['head'].fontRevision = 0.5
    fb.font.recalcTimestamp = False
    destination.parent.mkdir(parents=True, exist_ok=True)
    fb.save(destination)


def inspect_font(path: Path, data: dict) -> dict:
    with TTFont(path, checkChecksums=2) as font:
        # Force every table to decompile now, not later in a user's editor.
        for tag in font.keys():
            font[tag]
        cmap = font.getBestCmap()
        if set(cmap) != {ord(c) for c in CHARACTERS}:
            raise ValueError('Built coverage differs from source')
        bounds = {}
        for name in font.getGlyphOrder():
            glyph = font['glyf'][name]
            advance, lsb = font['hmtx'][name]
            if advance != 600:
                raise ValueError(f'Non-monospace advance: {name}')
            if glyph.numberOfContours:
                if not (0 <= glyph.xMin <= glyph.xMax <= 600 and -270 <= glyph.yMin <= glyph.yMax <= 900):
                    raise ValueError(f'Out-of-cell outline: {name}')
                if lsb != glyph.xMin:
                    raise ValueError(f'LSB mismatch: {name}')
                bounds[name] = [glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax]
        if font['name'].getDebugName(1) != FAMILY or font['post'].isFixedPitch != 1:
            raise ValueError('Incorrect family identity or pitch')
        if any(tag in font for tag in ('GSUB', 'GPOS', 'kern', 'fvar')):
            raise ValueError('Unexpected feature or variation table')
        return {'mapped_characters': len(cmap), 'glyph_count_including_notdef': len(font.getGlyphOrder()),
                'advance_units': 600, 'units_per_em': font['head'].unitsPerEm,
                'family': FAMILY, 'bounds': bounds, 'tables': list(font.keys())}


def make_specimen(data: dict) -> str:
    rows = ['Damonic', 'minimum priority inline', 'assign signal graceful',
            'abcdefghijklmnopqrstuvwxyz', '0123456789', 'I l 1 | O 0 o', 'ri ir in ni ii rr']
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1140" height="720" viewBox="0 0 1140 720">',
             '<rect width="1140" height="720" fill="white"/>',
             '<text x="36" y="42" font-family="sans-serif" font-size="22">Damonic R5 Study | actual source outlines</text>',
             '<text x="36" y="68" font-family="sans-serif" font-size="14">Experimental Regular. 42 characters. Not a complete coding font.</text>']
    for row, text in enumerate(rows):
        size = 64 if row == 0 else 48
        scale = size / 1000
        for col, ch in enumerate(text):
            path = data['glyphs'][ch]
            if path:
                parts.append(f'<path transform="translate({36 + col * size * 0.6:.3f} {156 + row * 84}) scale({scale} {-scale})" d="{escape(path)}"/>')
    return ''.join(parts) + '</svg>\n'


def zip_directory(root: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(p for p in root.rglob('*') if p.is_file()):
            info = zipfile.ZipInfo((Path(root.name) / path.relative_to(root)).as_posix(), (2026, 9, 6, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def build(out: Path, license_path: Path, source: Path | None = None) -> dict:
    data, raw = load_source(source)
    if not license_path.is_file():
        raise FileNotFoundError('OFL.txt is required for the package')
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('Use an empty --out directory to avoid mixing stale artifacts')
    out.mkdir(parents=True, exist_ok=True)
    ttf = out / (STEM + '.ttf')
    build_font(data, ttf)
    with tempfile.TemporaryDirectory() as directory:
        rebuilt = Path(directory) / ttf.name
        build_font(data, rebuilt)
        if ttf.read_bytes() != rebuilt.read_bytes():
            raise ValueError('Repeated TTF builds differ')
    with TTFont(ttf, recalcTimestamp=False) as font:
        font.flavor = 'woff2'
        font.save(out / (STEM + '.woff2'))
    report = inspect_font(ttf, data)
    woff_report = inspect_font(out / (STEM + '.woff2'), data)
    if report != woff_report:
        raise ValueError('TTF and WOFF2 metadata or bounds differ')
    with TTFont(ttf) as a, TTFont(out / (STEM + '.woff2')) as b:
        for ch in CHARACTERS:
            name = a.getBestCmap()[ord(ch)]
            if a['glyf'][name] != b['glyf'][name] or a['hmtx'][name] != b['hmtx'][name]:
                raise ValueError(f'WOFF2 round-trip changed {ch!r}')
    report.update({'version': VERSION, 'source_sha256': digest(raw),
                   'source_matches_accepted_R5': digest(raw) == SOURCE_SHA,
                   'deterministic_ttf': True, 'woff2_geometry_roundtrip': True,
                   'fonttools_version': fontTools.__version__,
                   'limits': ['Incomplete ASCII: only three uppercase letters and two punctuation symbols.',
                              'No Bold, Italic, Nerd/Powerline symbols, ligatures, variable axes or hinting.',
                              'Native IDE and terminal behavior, cross-platform rendering and independent design review are untested.']})
    (out / 'BUILD-REPORT.json').write_text(json.dumps(report, indent=2) + '\n')
    from PIL import ImageFont, features
    raster_checks = 0
    for size in (12, 14, 16, 18, 20, 24):
        raster_font = ImageFont.truetype(str(ttf), size)
        for ch in CHARACTERS:
            if ch != ' ':
                if raster_font.getmask(ch).getbbox() is None:
                    raise ValueError(f'Empty raster for {ch!r} at {size}px')
                raster_checks += 1
    qa = {'status': 'PASS for the named local checks only', 'raster_checks': raster_checks,
          'sizes_px': [12, 14, 16, 18, 20, 24], 'freetype': features.version('freetype2'),
          'source_sha256': digest(raw), 'deterministic_ttf': True,
          'woff2_geometry_roundtrip': True, 'native_editor_tested': False}
    (out / 'QA-REPORT.json').write_text(json.dumps(qa, indent=2) + '\n')
    (out / 'Specimen.svg').write_text(make_specimen(data))
    shutil.copyfile(license_path, out / 'OFL.txt')
    shutil.copyfile(HERE / 'README.md', out / 'README.md')
    source_root = out / ('Damonic-R5-' + VERSION + '-Source')
    source_root.mkdir()
    (source_root / 'R5-outlines.json').write_bytes(raw)
    for name in ('build.py', 'test_package.py', 'requirements.txt', 'README.md'):
        shutil.copyfile(HERE / name, source_root / name)
    shutil.copyfile(license_path, source_root / 'OFL.txt')
    shutil.copyfile(out / 'BUILD-REPORT.json', source_root / 'BUILD-REPORT.json')
    zip_directory(source_root, out / (source_root.name + '.zip'))
    checksums = {p.name: digest(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}
    (out / 'SHA256SUMS.txt').write_text(''.join(f'{value}  {name}\n' for name, value in checksums.items()))
    return report


def package(out: Path) -> Path:
    destination = out.parent / ('Damonic-R5-' + VERSION + '.zip')
    zip_directory(out, destination)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--license', type=Path)
    parser.add_argument('--source', type=Path, help='Explicit edited JSON; recorded as a non-accepted source')
    parser.add_argument('--extract-source', type=Path, help='Write the exact JSON and exit; never overwrites')
    parser.add_argument('--package', action='store_true')
    args = parser.parse_args()
    if args.extract_source:
        raw = source_bytes(args.source)
        if args.source is None and digest(raw) != SOURCE_SHA:
            raise ValueError('Source checksum mismatch')
        with args.extract_source.open('xb') as handle:
            handle.write(raw)
        return
    if args.out is None:
        parser.error('--out is required unless using --extract-source')
    license_path = args.license or (HERE / 'OFL.txt' if (HERE / 'OFL.txt').exists() else HERE.parents[1] / 'OFL.txt')
    report = build(args.out.resolve(), license_path.resolve(), args.source)
    if args.package:
        print(package(args.out.resolve()))
    print(json.dumps({k: report[k] for k in ('family', 'version', 'mapped_characters', 'deterministic_ttf', 'source_matches_accepted_R5')}, indent=2))


if __name__ == '__main__':
    main()
