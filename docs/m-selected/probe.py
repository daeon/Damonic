"""M-preserving m stem-weight probes. No outline changes to other letters."""
from pathlib import Path
import sys
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import build
OUT=Path(__file__).resolve().parent
for style in ['Regular','Bold']:
    for ratio in [.78,.82]:
        w=84 if style=='Regular' else 108
        g=build.glyph(build.core_outline('m',w,m_ratio=ratio));g.recalcBounds(None)
        f=TTFont(OUT/f'M-{style}.ttf',recalcTimestamp=False)
        gn=f.getBestCmap()[ord('m')];f['glyf'][gn]=g;f['hmtx'][gn]=(600,g.xMin)
        f.save(OUT/f'M{int(ratio*100)}-{style}.ttf')
im=Image.new('RGB',(1560,790),'#f4f2eb');d=ImageDraw.Draw(im)
ui=ImageFont.truetype('DejaVuSans.ttf',18)
for row,style in enumerate(['Regular','Bold']):
    for col,(key,title) in enumerate([('M','M / selected baseline'),('M78','M / slightly stronger m'),('M82','M / stronger m')]):
        x=24+col*520;y=20+row*390
        d.text((x,y),title+' / '+style,font=ui,fill='#18312f')
        path=OUT/f'{key}-{style}.ttf'
        f=ImageFont.truetype(str(path),84);d.text((x,y+40),'Damonic',font=f,fill='#18312f')
        for j,size in enumerate([12,16,20,28]):
            f=ImageFont.truetype(str(path),size)
            d.text((x,y+155+j*47),'minimum nmnm terminal',font=f,fill='#18312f')
im.save(OUT/'m-weight-probes.png')

# A direct comparison of the selected baseline with the actual shipped face.
current=ROOT/'dist'/'Damonic-Regular.ttf'
if current.exists():
    im=Image.new('RGB',(1160,390),'#172c30');d=ImageDraw.Draw(im)
    for col,(path,title) in enumerate([(OUT/'M-Regular.ttf','M / selected 0.4.1'),(current,'M refined / 0.4.2')]):
        x=28+col*580
        d.text((x,20),title,font=ui,fill='#c3d0c7')
        d.text((x,58),'Damonic',font=ImageFont.truetype(str(path),96),fill='#fffdf5')
        for j,size in enumerate([16,20,28]):
            d.text((x,188+j*52),'minimum nmnm terminal',font=ImageFont.truetype(str(path),size),fill='#fffdf5')
    im.save(OUT/'accepted-comparison.png')
