"""Render small-size text proofs using Pillow/FreeType, not native platform QA."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
image=Image.new('RGB',(1500,1080),'#f4f2eb')
draw=ImageDraw.Draw(image)
for j,style in enumerate(['Regular','Italic','Bold','BoldItalic']):
    path=ROOT/'dist'/f'Damonic-{style}.ttf'
    font=ImageFont.truetype(str(path),26)
    label=ImageFont.truetype(str(path),19)
    draw.text((30,15+j*265),style,font=label,fill='#224238')
    for i,text in enumerate(['ri in printing minimum return ring',
        '¤ § ¨ ª ® ² ³ µ ¶ ¹ º ¼ ½ ¾',
        'Đđ Ħħ Ĳĳ Ŀŀ Łł Ŋŋ Œœ Ŧŧ ŉ ſ',
        '“quotes” „low” ‚single‘ Àéñö x\u0301\u0301']):
        draw.text((30,45+j*265+i*43),text,font=font,fill='#22332e')
image.save(ROOT/'docs/core-proof.png')
nerd=ROOT/'dist/DamonicNerdFontMono-Regular.ttf'
if nerd.exists():
    from fontTools.ttLib import TTFont
    reference=TTFont(ROOT/'vendor/symbols-src/SymbolsNerdFontMono-Regular.ttf')
    points=sorted(reference.getBestCmap())
    selected=points[::max(1,len(points)//160)][:160]
    image=Image.new('RGB',(1400,900),'#14231f')
    draw=ImageDraw.Draw(image)
    font=ImageFont.truetype(str(nerd),36)
    textfont=ImageFont.truetype(str(ROOT/'dist/Damonic-Regular.ttf'),10)
    for i,cp in enumerate(selected):
        x=20+(i%20)*69;y=12+(i//20)*108
        draw.text((x,y),chr(cp),font=font,fill='#e2ebe4')
        draw.text((x,y+50),f'{cp:04X}',font=textfont,fill='#a5bdae')
    image.save(ROOT/'docs/symbol-proof.png')
