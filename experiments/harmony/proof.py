"""Render actual pilot fonts; blind labels include a duplicate control."""
from pathlib import Path
import base64, json
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
# Fixed anonymous order. Reveal only after independent visual assessment.
ORDER=[('K','construction'),('M','baseline'),('P','spacing'),('R','baseline')]
STYLES=['Regular','BoldItalic']
TRAIN=['Damonic','Da am mo on ni ic','ri ir in ni ic ci rn nr','minimum printing return']
HOLD=['ammoniac anionic cicada','acacia cacao maniac','riri inin ill lil mimic','if (incoming == nil) {','  return domain[index];','} // scan incoming data']
UI='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(size):return ImageFont.truetype(UI,size)
def draw_sheet(filename,hold=False):
    width=2040;panel=480;gap=24;header=70;row=820 if hold else 700
    im=Image.new('RGB',(width,header+row*2+20),'#edf0ed');d=ImageDraw.Draw(im)
    d.text((24,15),'Damonic: anonymous '+('transfer proof' if hold else 'construction proof'),font=font(23),fill='#20342e')
    for s,style in enumerate(STYLES):
        y=header+s*row
        for i,(label,key) in enumerate(ORDER):
            x=24+i*(panel+gap)
            d.text((x,y),label+' / '+style,font=font(18),fill='#20342e')
            fpath=ROOT/f'{key}-{style}.ttf'
            for j,(bg,fg) in enumerate([('#fffdf5','#172c30'),('#172c30','#fffdf5')]):
                top=y+32+j*((row-40)//2);bottom=top+(row-48)//2
                d.rectangle((x,top,x+panel,bottom),fill=bg)
                yy=top+10
                if not hold:
                    f=ImageFont.truetype(str(fpath),84)
                    d.text((x+12,yy),'Damonic',font=f,fill=fg);yy+=104
                for size in ([12,16,20] if hold else [16,20]):
                    d.text((x+12,yy),str(size)+' px',font=font(11),fill=fg);yy+=15
                    f=ImageFont.truetype(str(fpath),size)
                    lines=HOLD[:3] if hold else TRAIN[1:]
                    for line in lines:
                        assert d.textlength(line,font=f)<panel-24
                        d.text((x+12,yy),line,font=f,fill=fg);yy+=size+5
                if hold:
                    yy+=8
                    f=ImageFont.truetype(str(fpath),16)
                    for line in HOLD[3:]:
                        d.text((x+12,yy),line,font=f,fill=fg);yy+=21
    im.save(ROOT/filename)
    return im

def html():
    faces=[];sections=[]
    for label,key in ORDER:
        cards=[]
        for style in STYLES:
            family=label+style
            data=base64.b64encode((ROOT/f'{key}-{style}.ttf').read_bytes()).decode()
            faces.append(f"@font-face{{font-family:{family};src:url(data:font/ttf;base64,{data})}}")
            cards.append(f'<h3>{style}</h3><div class="word" style="font-family:{family}">Damonic</div><pre class="sample" style="font-family:{family}"></pre>')
        sections.append(f'<section><h2>Candidate {label}</h2>'+''.join(cards)+'</section>')
    doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Damonic — harmony experiment</title><style>FACES
    *{box-sizing:border-box}body{margin:0;background:#f2f1e8;color:#172c30;font:16px/1.5 system-ui}main{max-width:1500px;margin:auto;padding:28px}h1{font-size:32px}.controls{display:flex;gap:18px;flex-wrap:wrap;margin:24px 0}textarea{width:100%;height:140px;padding:16px;font:16px/1.5 monospace}button{padding:8px 16px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}section{border:1px solid #80958e;padding:20px;min-width:0}.word{font-size:clamp(40px,6vw,84px);overflow:auto}pre{font-size:var(--size,16px);line-height:1.6;overflow:auto}.dark{background:#172c30;color:#fffdf5}details{margin:28px 0}h3{font-size:14px;margin-top:32px}@media(max-width:800px){.grid{grid-template-columns:1fr}}</style><main><h1>Damonic: test the rhythm</h1><p>Seven-letter experiment. Compare at your normal coding size before enlarging. These are actual embedded fonts; pilot outlines are not a complete release.</p><div class="controls"><label>Size <input id="size" type="range" min="12" max="28" value="16"><output id="value">16 px</output></label><button id="theme">Change theme</button><button id="hold">Show transfer text</button></div><textarea id="text" spellcheck="false"></textarea><div class="grid">CARDS</div><details><summary>Reveal the studies and duplicate control</summary><p>K: construction study, original outer horizontal extents retained. M: baseline 0.4.1. P: spacing study. R: identical baseline control. An apparent difference between M and R is a review inconsistency.</p><p>Only D, a, m, o, n, i and c are revised in the pilot fonts. Accented forms and the remaining alphabet are baseline shapes.</p></details><details><summary>Read the experiment outcome</summary><p>Neither pilot established a reliable coding-size improvement. Both anonymous reviewers reported ties at 12/16/20 px. All four pilot fonts passed scope, cell, shaping and sanitizer checks. These technical checks do not establish visual harmony.</p><p>The construction study simplifies i and changes the a/m/n texture; the spacing study makes modest horizontal adjustments. The next step is a stronger shared construction study across related letters. No production release is replaced by these pilots.</p></details></main><script>
    const input=document.getElementById('text');input.value=INITIAL;function update(){document.querySelectorAll('.sample').forEach(e=>e.textContent=input.value);const n=document.getElementById('size').value;document.documentElement.style.setProperty('--size',n+'px');document.getElementById('value').textContent=n+' px'}input.oninput=update;document.getElementById('size').oninput=update;document.getElementById('theme').onclick=()=>document.body.classList.toggle('dark');document.getElementById('hold').onclick=()=>{input.value=HOLD;update()};update();</script></html>'''
    (ROOT/'Damonic-Harmony-Experiment.html').write_text(doc.replace('FACES','\n'.join(faces)).replace('CARDS','\n'.join(sections)).replace('INITIAL',json.dumps('\n'.join(TRAIN))).replace('HOLD',json.dumps('\n'.join(HOLD))))
def named_overview():
    im=Image.new('RGB',(1680,650),'#172c30');d=ImageDraw.Draw(im)
    d.text((28,15),'Damonic: completed harmony studies',font=font(25),fill='#fffdf5')
    for col,(key,label) in enumerate([('baseline','Current 0.4.1'),('construction','Construction study'),('spacing','Spacing study')]):
        x=28+col*550
        for row,style in enumerate(STYLES):
            y=70+row*270
            d.text((x,y),label+' / '+style,font=font(17),fill='#b9c6be')
            f=ImageFont.truetype(str(ROOT/f'{key}-{style}.ttf'),96)
            d.text((x,y+30),'Damonic',font=f,fill='#fffdf5')
            f=ImageFont.truetype(str(ROOT/f'{key}-{style}.ttf'),24)
            d.text((x,y+154),'ri ir in ni ic ci rn nr',font=f,fill='#fffdf5')
            d.text((x,y+192),'minimum printing return',font=f,fill='#fffdf5')
    d.text((28,612),'Seven-letter pilots. No coding-size winner established; production font unchanged.',font=font(18),fill='#b9c6be')
    im.save(ROOT/'named-comparison.png')

if __name__=='__main__':
    draw_sheet('comparison.png');draw_sheet('transfer.png',True);html();named_overview()
