#!/usr/bin/env python3
"""Deterministically merge the pinned Nerd Fonts SymbolsNerdFontMono cmap/glyphs.

The base font's ASCII cmap and outlines are protected. Symbols are copied as prefixed
TT glyphs and assigned 600-unit advances; collisions retain the Damonic glyph and are
recorded in the generated JSON manifest.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, tempfile, zipfile, urllib.request
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen

VERSION='v3.5.1'
ARCHIVE='NerdFontsSymbolsOnly-v3.5.1.zip'
ARCHIVE_SHA256='fdca3682534f6f65e1ccb2345b0362ccf67d9b8eca7c8025330946e93e2473bc'
SYMBOL_FONT='SymbolsNerdFontMono-Regular.ttf'
EPOCH=int(os.environ.get('SOURCE_DATE_EPOCH','1788566400'))


def sha(path):
 h=hashlib.sha256(); h.update(Path(path).read_bytes()); return h.hexdigest()

def unique_name(name, existing):
 base='NF_'+name
 out=base; i=2
 while out in existing: out=f'{base}_{i}'; i+=1
 return out

def rewrite_components(g, renames):
 # glyf component references are glyph names. Rewrite recursively by field.
 if hasattr(g,'components'):
  for c in g.components:
   if c.glyphName in renames: c.glyphName=renames[c.glyphName]

def set_names(font, style):
 sub='Regular' if style=='Regular' else ('Bold Italic' if style=='BoldItalic' else style)
 family='Damonic Nerd Font Mono'
 full=f'{family} {sub}'
 ps='DamonicNerdFontMono-'+style
 for nid,val in [(1,family),(2,sub),(3,full),(4,full),(6,ps),(16,family),(17,sub)]:
  font['name'].setName(val,nid,3,1,0x409)
 # Ensure deterministic font revision/name records are otherwise untouched.
 font['head'].created=EPOCH + 2082844800; font['head'].modified=EPOCH + 2082844800

def relpath(p):
 try: return str(Path(p).resolve().relative_to(Path(__file__).parents[1]))
 except ValueError: return str(Path(p).resolve())

def merge(base_path, out_path, symbol_path, manifest_path):
 base=TTFont(base_path, recalcBBoxes=False, recalcTimestamp=False)
 sym=TTFont(symbol_path, recalcBBoxes=False, recalcTimestamp=False)
 # Preserve original ASCII glyph bytes for the proof manifest.
 base_cmap=base['cmap'].getBestCmap(); sym_cmap=sym['cmap'].getBestCmap()
 original_order=list(base.getGlyphOrder())
 existing=set(original_order); glyf=base['glyf']; hmtx=base['hmtx'].metrics
 gs=sym.getGlyphSet()
 # Copy all symbol glyphs, including unencoded components, under stable names.
 renames={n:unique_name(n,existing) for n in sym.getGlyphOrder() if n not in ('.notdef','.null','nonmarkingreturn','CR')}
 for old,new in renames.items():
  # Symbols are 2048 UPM; fit the 600-unit cell horizontally and base 1000 UPM vertically.
  # Drawing through the glyph set decomposes composites, avoiding dangling component names.
  src_aw=sym['hmtx'].metrics.get(old,(2048,0))[0]
  # Decompose composites, then uniformly contain each icon in a 600 x 1250 box.
  bp=BoundsPen(gs); gs[old].draw(bp)
  if bp.bounds:
   xmin,ymin,xmax,ymax=bp.bounds; bw=max(1,xmax-xmin); bh=max(1,ymax-ymin)
  else: xmin=ymin=xmax=ymax=0; bw=bh=1
  scale=min(600.0/src_aw if src_aw else 600.0/2048.0,598.0/bw,1248.0/bh)
  rp=DecomposingRecordingPen(gs); gs[old].draw(rp)
  # Replay through a transform; vertical placement retains the source baseline,
  # then translates only if needed to stay within the -250..1000 cell.
  pen0=TTGlyphPen(None); rp.replay(TransformPen(pen0,(scale,0,0,scale,0,0))); g=pen0.glyph()
  g.recalcBounds(glyf)
  dx=300-(xmin+xmax)*scale/2; dy=0
  if g.yMin+dy < -250: dy=-250-(g.yMin+dy)
  if g.yMax+dy > 1000: dy=1000-(g.yMax+dy)
  if dx or dy:
   rp2=DecomposingRecordingPen(gs); gs[old].draw(rp2); pen1=TTGlyphPen(None); rp2.replay(TransformPen(pen1,(scale,0,0,scale,dx,dy))); g=pen1.glyph(); g.recalcBounds(glyf)
  glyf[new]=g; existing.add(new)
  hmtx[new]=(600,round(g.xMin))
 # Add only noncolliding mappings. ASCII is always protected even if absent from base cmap.
 merged_cmap=dict(base_cmap); entries=[]
 for cp,old in sorted(sym_cmap.items()):
  if cp < 0x80:
   status='protected_ascii'
  elif cp in merged_cmap:
   status='collision_base_preserved'
  else:
   merged_cmap[cp]=renames.get(old,old); status='merged'
  entries.append({'codepoint':f'U+{cp:04X}','decimal':cp,'source_glyph':old,'damonic_glyph':renames.get(old), 'status':status})
 # Rebuild cmap with Unicode subtables and retain platform conventions.
 cmap=newTable('cmap'); cmap.tableVersion=0; cmap.tables=[]
 for platform,enc,fmt in [(0,4,4),(3,10,12),(3,1,4)]:
  t=CmapSubtable.newSubtable(fmt); t.platformID=platform; t.platEncID=enc; t.language=0; t.cmap=({cp:g for cp,g in merged_cmap.items() if cp <= 0xFFFF} if fmt==4 else merged_cmap.copy()); cmap.tables.append(t)
 base['cmap']=cmap
 # Ensure order references all newly added glyphs and metrics are valid.
 base.setGlyphOrder(original_order+list(renames.values()))
 style=Path(base_path).stem.removeprefix('Damonic-')
 set_names(base,style)
 # Remove symbol-only decorative metadata and preserve base OpenType tables/features.
 base['maxp'].numGlyphs=len(base.getGlyphOrder())
 base['maxp'].recalc(base)
 base['hhea'].recalc(base)
 base.save(out_path,reorderTables=False)
 manifest={'schema':1,'nerd_fonts_release':VERSION,'archive':ARCHIVE,'archive_sha256':ARCHIVE_SHA256,
  'symbol_font':SYMBOL_FONT,'symbol_font_sha256':sha(symbol_path),'source_url':'https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/NerdFontsSymbolsOnly.zip','source_date_epoch':EPOCH,
  'base':relpath(base_path),'output':relpath(out_path),'base_ascii_protected':True,
  'units_per_em':base['head'].unitsPerEm,'symbol_source_units_per_em':sym['head'].unitsPerEm,'symbol_advance_width':600,'source_symbol_glyphs':len(sym.getGlyphOrder()),
  'source_mapped_codepoints':len(sym_cmap),'merged_codepoints':sum(e['status']=='merged' for e in entries),
  'collisions':sum(e['status']=='collision_base_preserved' for e in entries),
  'protected_ascii':sum(e['status']=='protected_ascii' for e in entries),'entries':entries}
 Path(manifest_path).write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 return manifest

def _extract_symbol(archive):
 with zipfile.ZipFile(archive) as z: data=z.read(SYMBOL_FONT)
 fd,tmp=tempfile.mkstemp(suffix='.ttf'); os.close(fd); Path(tmp).write_bytes(data); return Path(tmp)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--base'); ap.add_argument('--output'); ap.add_argument('--manifest'); ap.add_argument('--archive',default=str(Path(__file__).parents[1]/'vendor'/ARCHIVE)); ap.add_argument('--symbol-font')
 a=ap.parse_args(); archive=Path(a.archive)
 if not archive.exists():
  archive.parent.mkdir(parents=True,exist_ok=True)
  urllib.request.urlretrieve('https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/NerdFontsSymbolsOnly.zip',archive)
 if sha(archive)!=ARCHIVE_SHA256: raise SystemExit(f'archive sha256 mismatch: {sha(archive)}')
 if not a.base and not a.output:
  root=Path(__file__).parents[1]
  symbol=Path(a.symbol_font) if a.symbol_font else _extract_symbol(archive)
  for style in ('Regular','Italic','Bold','BoldItalic'):
   merge(root/'dist'/f'Damonic-{style}.ttf', root/'dist'/f'DamonicNerdFontMono-{style}.ttf', symbol, root/'dist'/f'DamonicNerdFontMono-{style}.manifest.json')
  if not a.symbol_font: symbol.unlink(missing_ok=True)
  return
 if not a.base or not a.output: ap.error('--base and --output are required together')
 if a.symbol_font: symbol=Path(a.symbol_font)
 else:
  symbol=_extract_symbol(archive)
 out=Path(a.output); manifest=Path(a.manifest or out.with_suffix('.manifest.json')); out.parent.mkdir(parents=True,exist_ok=True)
 m=merge(Path(a.base),out,symbol,manifest); print(json.dumps({k:m[k] for k in ('output','source_mapped_codepoints','merged_codepoints','collisions','protected_ascii','symbol_advance_width')},sort_keys=True))
 if not a.symbol_font: symbol.unlink(missing_ok=True)
if __name__=='__main__': main()
