"""Check the experimental contract; these checks do not establish beauty."""
from pathlib import Path
import json
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb
ROOT=Path(__file__).resolve().parent
TARGET=set(map(ord,'Damonic'))
rows=[]
for study in ['spacing','construction']:
 for style in ['Regular','BoldItalic']:
  p=ROOT/f'{study}-{style}.ttf';a=TTFont(ROOT/f'baseline-{style}.ttf');b=TTFont(p)
  ac=a.getBestCmap();bc=b.getBestCmap();changed=[];outside=[];bounds=[]
  assert ac==bc
  for cp,gn in ac.items():
   ag=a['glyf'][gn];bg=b['glyf'][gn]
   if list(ag.getCoordinates(a['glyf'])[0])!=list(bg.getCoordinates(b['glyf'])[0]):
    changed.append(chr(cp))
    if cp not in TARGET:outside.append(cp)
   assert a['hmtx'][gn][0]==b['hmtx'][gn][0]
   if cp in TARGET:
    ag.recalcBounds(a['glyf']);bg.recalcBounds(b['glyf'])
    ap=BoundsPen(a.getGlyphSet());a.getGlyphSet()[gn].draw(ap)
    bp=BoundsPen(b.getGlyphSet());b.getGlyphSet()[gn].draw(bp)
    old=(ap.bounds[0],ap.bounds[2]);new=(bp.bounds[0],bp.bounds[2])
    bounds.append({'char':chr(cp),'before':old,'after':new})
    assert -1<=new[0]<new[1]<=601
    assert b['hmtx'][gn][1]==bg.xMin
    if study=='construction':assert max(abs(x-y) for x,y in zip(old,new))<=1
  assert not outside
  assert all(b['name'].getDebugName(i)!=a['name'].getDebugName(i) for i in [1,4,6,16]),'study names collide'
  font=hb.Font(hb.Face(p.read_bytes()));buf=hb.Buffer();buf.add_str('Damonic ri ir in ni ic ci');buf.guess_segment_properties();hb.shape(font,buf)
  assert all(x.x_advance==600 for x in buf.glyph_positions)
  rows.append({'study':study,'style':style,'changed_characters':changed,'bounds':bounds,'advance_and_scope_checks':'pass'})
(ROOT/'verification.json').write_text(json.dumps(rows,indent=2))
print('Four pilot fonts pass scope, cell, shaping, naming and bounds checks.')
