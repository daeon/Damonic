"""Build Damonic from canonical Python sources; package deterministic releases."""
from pathlib import Path
import argparse, base64, hashlib, json, os, shutil, subprocess, sys, zipfile
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.recordingPen import DecomposingRecordingPen
import ufoLib2

ROOT = Path(__file__).resolve().parent
STYLES = ('Regular', 'Italic', 'Bold', 'BoldItalic')
VERSION = '0.4.1-alpha'
os.environ.setdefault('SOURCE_DATE_EPOCH', '1788566400')

def run(*args):
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)

def font_paths():
    return [ROOT/'dist'/f'{family}-{style}.ttf'
            for family in ('Damonic', 'DamonicNerdFontMono') for style in STYLES]

def export_ufo(path):
    font = TTFont(path, recalcTimestamp=False)
    ufo = ufoLib2.Font()
    info = ufo.info
    info.familyName = 'Damonic'
    info.styleName = font['name'].getDebugName(2)
    info.unitsPerEm = font['head'].unitsPerEm
    info.ascender, info.descender = 1000, -250
    info.xHeight, info.capHeight = 530, 710
    info.italicAngle = font['post'].italicAngle
    info.versionMajor, info.versionMinor = 0, 401
    info.copyright = font['name'].getDebugName(0)
    info.openTypeOS2WeightClass = font['OS/2'].usWeightClass
    glyphset = font.getGlyphSet()
    reverse = {}
    for cp, name in font.getBestCmap().items():
        reverse.setdefault(name, []).append(cp)
    for name in font.getGlyphOrder():
        glyph = ufo.newGlyph(name)
        glyph.width = font['hmtx'][name][0]
        glyph.unicodes = reverse.get(name, [])
        pen = DecomposingRecordingPen(glyphset)
        glyphset[name].draw(pen)
        pen.replay(glyph.getPen())
    ufo.glyphOrder = font.getGlyphOrder()
    features = path.with_suffix('.fea')
    if features.exists():
        ufo.features.text = features.read_text()
    out = ROOT/'interchange'/path.with_suffix('.ufo').name
    out.parent.mkdir(exist_ok=True)
    ufo.save(out, overwrite=True)

def preview():
    faces = []
    cards = []
    for path in font_paths():
        font = TTFont(path, recalcTimestamp=False)
        family = font['name'].getDebugName(1)
        style = font['name'].getDebugName(2)
        key = path.stem
        data = base64.b64encode(path.with_suffix('.woff2').read_bytes()).decode()
        faces.append(f"@font-face{{font-family:'{key}';src:url(data:font/woff2;base64,{data}) format('woff2')}}")
        cards.append(f'<section><h2>{family} · {style}</h2><pre class="sample" style="font-family:{key}"></pre></section>')
    doc = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Damonic 0.4.1 Alpha</title><style>
    FACES
    :root{color-scheme:light;--bg:#f4f2eb;--ink:#22332e;--line:#b8c3bb;--panel:#fffdf7}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:clamp(20px,5vw,70px)}h1{font:clamp(40px,8vw,78px)/1.2 Damonic-Regular;margin:18px 0}h2{font-size:15px;font-weight:600}small{letter-spacing:.12em}p{max-width:720px}header{padding-bottom:32px;border-bottom:1px solid var(--line)}.controls{display:flex;gap:20px;flex-wrap:wrap;align-items:center;margin:28px 0}button{padding:10px 20px;background:var(--ink);color:var(--bg);border:0;border-radius:5px;cursor:pointer}textarea{width:100%;min-height:220px;padding:20px;font:16px/1.5 Damonic-Regular;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:6px}section{margin-top:35px;padding-top:20px;border-top:1px solid var(--line)}pre{overflow:auto;line-height:1.6;font-size:var(--size,16px);padding:20px;background:var(--panel);border-radius:6px}.muted{font-size:14px;opacity:.8}body.dark{color-scheme:dark;--bg:#14231f;--ink:#e2ebe4;--line:#4b6257;--panel:#1c2e27}.icons{font:26px/2 DamonicNerdFontMono-Regular;word-break:break-all}
    </style><main><header><small>ORIGINAL CODING TYPEFACE / 0.4.1 ALPHA</small><h1>Damonic</h1><p>Eight faces. One collection. An original monospace with a complete Nerd Fonts Mono edition. Inspect the actual embedded fonts at working sizes.</p><p class="muted">The TTC contains discrete styles. Native terminal and platform testing remains part of the road to 1.0.</p></header><div class="controls"><label>Size <input id="size" type="range" min="10" max="32" value="16"> <output id="sizeValue">16 px</output></label><label><input type="checkbox" id="dlig"> Operator ligatures</label><label><input type="checkbox" id="ss01"> Dotted zero</label><label><input type="checkbox" id="ss02"> Simple l</label><button id="theme">Toggle theme</button></div><label for="text">Shared specimen text</label><textarea id="text" spellcheck="false"></textarea>CARDS<section><h2>Nerd Fonts symbol sample</h2><p class="muted">These are a sample; the included coverage manifest verifies the complete upstream mapping.</p><div class="icons">&#xf015; &#xf07b; &#xf013; &#xf120; &#xe0b0; &#xe0b2; &#xe0a0; &#xe725; &#xe73c; &#xf121; &#xf09b; &#xf17c; &#xf179; &#xf17a;</div></section></main><script>
    const input=document.getElementById('text');input.value='printing minimum string return\\nri ir in ni rn nr rim ring bring\\nIl1|! O0o {} [] () 0123456789\\nÀéñö Đđ Œœ Łł ß “quotes”\\n// Damonic: clear code and quiet rhythm.\\nfunction scan(input) {\\n  if (input.length >= 10 && input[0] != 0) {\\n    return count(input);\\n  }\\n}\\n┌────────────┐\\n│ ~/projects │\\n└────────────┘';
    function update(){document.querySelectorAll('.sample').forEach(el=>el.textContent=input.value);document.documentElement.style.setProperty('--size',document.getElementById('size').value+'px');document.getElementById('sizeValue').value=document.getElementById('size').value+' px';const features=['dlig','ss01','ss02'].map(id=>'"'+id+'" '+(document.getElementById(id).checked?1:0)).join(',');document.querySelectorAll('.sample,textarea').forEach(el=>el.style.fontFeatureSettings=features)}document.querySelectorAll('input,textarea').forEach(el=>el.addEventListener('input',update));document.getElementById('theme').onclick=()=>document.body.classList.toggle('dark');update();
    </script></html>'''
    (ROOT/'Damonic-Preview.html').write_text(doc.replace('FACES','\n'.join(faces)).replace('CARDS','\n'.join(cards)))

def build():
    run('build.py')
    run('scripts/patch_nerd.py')
    collection = TTCollection()
    collection.fonts = [TTFont(p, recalcTimestamp=False) for p in font_paths()]
    collection.save(ROOT/'dist/Damonic.ttc', shareTables=True)
    for path in font_paths():
        font = TTFont(path, recalcTimestamp=False)
        font.flavor = 'woff2'
        font.save(path.with_suffix('.woff2'))
    for path in font_paths()[:4]:
        export_ufo(path)
    preview()
    print('Built eight faces, TTC, WOFF2, UFO snapshots and preview.')

def zip_files(output, paths):
    temporary=output.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(paths):
            entry=zipfile.ZipInfo('Damonic/'+path.relative_to(ROOT).as_posix(), (2026,9,5,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o100644 << 16
            archive.writestr(entry,path.read_bytes(),compresslevel=9)
    with zipfile.ZipFile(temporary) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('Archive integrity check failed')
    os.replace(temporary,output)

def package():
    paths=[p for p in ROOT.rglob('*') if p.is_file() and not any((x.startswith('.') and x not in ('.github','.gitignore')) or x=='__pycache__' for x in p.relative_to(ROOT).parts) and p.suffix not in ('.zip','.pyc','.tmp') and p.name!='SHA256SUMS.txt']
    # Vendor ZIP files are pinned inputs and belong in the source release.
    paths += list((ROOT/'vendor').rglob('*.zip'))
    checksum=ROOT/'SHA256SUMS.txt'
    checksum.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(paths)))
    paths.append(checksum)
    binary=[p for p in paths if p.parts[len(ROOT.parts)] in ('dist','licenses','docs') or p.suffix in ('.md','.html') or p.name in ('OFL.txt','SHA256SUMS.txt') or (p.parts[len(ROOT.parts)]=='vendor' and p.suffix in ('.json','.txt','.md'))]
    zip_files(ROOT/f'Damonic-{VERSION}.zip',binary)
    zip_files(ROOT/f'Damonic-{VERSION}-Source.zip',paths)
    print('Packaged binary and source archives.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','package','preview'])
    args=parser.parse_args()
    globals()[args.command]()
