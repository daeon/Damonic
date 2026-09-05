"""Original Bearing Mono terminal geometry. All coordinates use a 600 x 1250 cell.
No font outlines are imported. Run this file to verify coverage and bounds.
"""
import math
import unicodedata
from fontTools.pens.ttGlyphPen import TTGlyphPen

X, Y, B, T = 300, 375, -250, 1000
CELL_HEIGHT = T - B


def polygon(pen, pts):
    pen.moveTo(tuple(round(c) for c in pts[0]))
    for p in pts[1:]: pen.lineTo(tuple(round(c) for c in p))
    pen.closePath()


def rectangles(pen, boxes):
    """Emit exact union contours of axis-aligned rectangles, including holes."""
    boxes = [tuple(round(v) for v in r) for r in boxes if r[2]>r[0] and r[3]>r[1]]
    if not boxes: return
    xs=sorted({r[i] for r in boxes for i in (0,2)})
    ys=sorted({r[i] for r in boxes for i in (1,3)})
    occupied=set()
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            if any(a<=xs[i] and c>=xs[i+1] and b<=ys[j] and d>=ys[j+1] for a,b,c,d in boxes): occupied.add((i,j))
    edges=set()
    for i,j in occupied:
        a,b,c,d=xs[i],ys[j],xs[i+1],ys[j+1]
        # Clockwise outer contour; holes automatically reverse.
        pts=[(a,b),(a,d),(c,d),(c,b)]
        for s,e in zip(pts,pts[1:]+pts[:1]):
            if (e,s) in edges: edges.remove((e,s))
            else: edges.add((s,e))
    while edges:
        s,e=min(edges); edges.remove((s,e)); pts=[s]; prev=s; current=e
        while current!=s:
            pts.append(current)
            candidates=[b for a,b in edges if a==current]
            # At diagonal-only contact, stay on the clockwise boundary.
            dx,dy=current[0]-prev[0],current[1]-prev[1]
            def turn(q):
                ex,ey=q[0]-current[0],q[1]-current[1]
                return math.atan2(dx*ey-dy*ex,dx*ex+dy*ey)
            nxt=min(candidates,key=turn)
            edges.remove((current,nxt));prev,current=current,nxt
        # Reduce the grid boundary to necessary corners.
        clean=[]
        for k,p in enumerate(pts):
            a=pts[k-1];b=pts[(k+1)%len(pts)]
            if (p[0]-a[0])*(b[1]-p[1])!=(p[1]-a[1])*(b[0]-p[0]): clean.append(p)
        polygon(pen,clean)


def disk(pen,x,y,r):
    polygon(pen,[(x+math.cos(-i*math.pi/8)*r,y+math.sin(-i*math.pi/8)*r) for i in range(16)])


def arms_from_name(name):
    words=name.replace('BOX DRAWINGS ','').split(' AND ')
    styles={'LIGHT','HEAVY','SINGLE','DOUBLE'}
    default=next((w for w in words[0].split() if w in styles),'LIGHT')
    arms={}
    for clause in words:
        tokens=clause.split();style=next((w for w in tokens if w in styles),default)
        for token in tokens:
            for d in {'HORIZONTAL':('LEFT','RIGHT'),'VERTICAL':('UP','DOWN')}.get(token,(token,)):
                if d in ('LEFT','RIGHT','UP','DOWN'): arms[d]=style
    return arms


def box_glyph(cp,weight):
    p=TTGlyphPen(None);name=unicodedata.name(chr(cp));light=round(weight*.78);heavy=round(light*1.8)
    if 'DIAGONAL' in name:
        w=light/2
        if cp in (0x2571,0x2573): polygon(p,list(reversed([(0,B),(w,B),(600,T-w),(600,T),(600-w,T),(0,B+w)])))
        if cp in (0x2572,0x2573): polygon(p,[(0,T),(w,T),(600,B+w),(600,B),(600-w,B),(0,T-w)])
        return p.glyph()
    if 'ARC' in name:
        # One rounded elbow, straight limbs tangent to a quarter-circle.
        sx=1 if 'RIGHT' in name else -1;sy=1 if 'UP' in name else -1;r=145;h=light/2
        points=[]
        # Canonical elbow connects right arm with down arm. Reflect as needed.
        def tr(a,b):return (X+sx*a,Y-sy*b)
        pts=[(300,h),(r,h)]
        # Center (r,-r), outer radius r+h; top tangent to left tangent.
        pts += [(r+(r+h)*math.cos(a),-r+(r+h)*math.sin(a)) for a in [math.pi/2+i*math.pi/32 for i in range(17)]]
        pts += [(-h,-CELL_HEIGHT/2),(h,-CELL_HEIGHT/2),(h,-r)]
        pts += [(r+(r-h)*math.cos(a),-r+(r-h)*math.sin(a)) for a in [math.pi-i*math.pi/32 for i in range(17)]]
        pts += [(300,-h)]
        polygon(p,[tr(a,b) for a,b in pts]);return p.glyph()
    if 'DASH' in name:
        n=3 if 'TRIPLE' in name else 4 if 'QUADRUPLE' in name else 2
        thick=heavy if 'HEAVY' in name else light;h=thick/2;boxes=[]
        lo,hi=(0,600) if 'HORIZONTAL' in name else (B,T)
        period=(hi-lo)/n;gap=period*.27
        for i in range(n):
            a=lo+i*period+gap/2;b=lo+(i+1)*period-gap/2
            boxes.append((a,Y-h,b,Y+h) if 'HORIZONTAL' in name else (X-h,a,X+h,b))
        rectangles(p,boxes);return p.glyph()
    arms=arms_from_name(name);boxes=[];off=light*1.05
    for d,style in arms.items():
        thick=heavy if style=='HEAVY' else light;h=thick/2
        for rail in (-off,off) if style=='DOUBLE' else (0,):
            # Default junction reaches the furthest perpendicular rail.
            perp=('UP','DOWN') if d in ('LEFT','RIGHT') else ('LEFT','RIGHT')
            extent=max([((off if arms[q]=='DOUBLE' else 0)+(heavy if arms[q]=='HEAVY' else light)/2) for q in perp if q in arms] or [0])
            end=extent
            # Double junctions follow the boundaries of the connected arms.
            # A rail facing a perpendicular arm forms an inside corner; the
            # opposite rail forms the outside corner. This also handles tees
            # and crosses without drawing spurious bars through their gaps.
            perpendicular=[q for q in perp if q in arms]
            if style=='DOUBLE' and perpendicular and all(arms[q]=='DOUBLE' for q in perpendicular):
                facing=('UP' if rail>0 else 'DOWN') if d in ('LEFT','RIGHT') else ('RIGHT' if rail>0 else 'LEFT')
                end=(-off if facing in perpendicular else off)+h
            if d=='LEFT':boxes.append((0,Y+rail-h,X+end,Y+rail+h))
            elif d=='RIGHT':boxes.append((X-end,Y+rail-h,600,Y+rail+h))
            elif d=='UP':boxes.append((X+rail-h,Y-end,X+rail+h,T))
            else:boxes.append((X+rail-h,B,X+rail+h,Y+end))
    rectangles(p,boxes);return p.glyph()


def terminal_glyphs(weight=78):
    out={cp:box_glyph(cp,weight) for cp in range(0x2500,0x2580)}
    quadrants={0x2596:[0],0x2597:[1],0x2598:[2],0x2599:[0,1,2],0x259A:[1,2],0x259B:[0,2,3],0x259C:[1,2,3],0x259D:[3],0x259E:[0,3],0x259F:[0,1,3]}
    for cp in range(0x2580,0x25A0):
        p=TTGlyphPen(None);boxes=[]
        if cp==0x2580:boxes=[(0,Y,600,T)]
        elif 0x2581<=cp<=0x2588: boxes=[(0,B,600,B+CELL_HEIGHT*(cp-0x2580)/8)]
        elif 0x2589<=cp<=0x258F: boxes=[(0,B,600*(0x2590-cp)/8,T)]
        elif cp==0x2590:boxes=[(300,B,600,T)]
        elif cp in (0x2591,0x2592,0x2593):
            # Seamless 8 x 16 ordered dither: 25%, 50%, and 75% coverage.
            threshold={0x2591:1,0x2592:2,0x2593:3}[cp];matrix=((0,2),(3,1))
            for x in range(8):
                for y in range(16):
                    if matrix[y%2][x%2]<threshold: boxes.append((x*75,B+y*CELL_HEIGHT/16,(x+1)*75,B+(y+1)*CELL_HEIGHT/16))
        elif cp==0x2594:boxes=[(0,T-CELL_HEIGHT/8,600,T)]
        elif cp==0x2595:boxes=[(525,B,600,T)]
        else:
            for q in quadrants[cp]:
                x=300*(q%2);y=B+CELL_HEIGHT/2*(q//2);boxes.append((x,y,x+300,y+CELL_HEIGHT/2))
        rectangles(p,boxes);out[cp]=p.glyph()
    # Braille standard bit order: 1 4 / 2 5 / 3 6 / 7 8.
    dots=[(185,660),(185,420),(185,180),(415,660),(415,420),(415,180),(185,-60),(415,-60)]
    for cp in range(0x2800,0x2900):
        p=TTGlyphPen(None)
        for bit,(x,y) in enumerate(dots):
            if (cp-0x2800)&(1<<bit): disk(p,x,y,50+weight*.12)
        out[cp]=p.glyph()
    for cp in range(0xE0A0,0xE0A4):
        p=TTGlyphPen(None);w=weight*.7
        if cp==0xE0A0: # Version-control branch: trunk and a right-hand branch.
            rectangles(p,[(155-w/2,60,155+w/2,650),(155,350-w/2,420,350+w/2),(420-w/2,350,420+w/2,590)])
            for x,y in [(155,90),(155,650),(420,590)]:disk(p,x,y,65)
        elif cp==0xE0A1: # Line number symbol.
            rectangles(p,[(120,80,120+w,700),(120,80,450,80+w),(350,300,350+w,700)])
        elif cp==0xE0A2: # Lock, with an open counter in the shackle.
            rectangles(p,[(115,40,485,420),(170,400,170+w,680),(430-w,400,430,680),(170,680-w,430,680)])
        else: # Column indicator.
            rectangles(p,[(120,600,480,600+w),(120,100,480,100+w),(270,100,270+w,650)])
        out[cp]=p.glyph()
    for cp in range(0xE0B0,0xE0B4):
        p=TTGlyphPen(None);right=cp in (0xE0B0,0xE0B1)
        pts=[(0,B),(600,Y),(0,T)] if cp%2==0 else [(0,B),(weight*.8,B),(600,Y),(weight*.8,T),(0,T),(600-weight*1.1,Y)]
        if not right: pts=[(600-x,y) for x,y in pts]
        polygon(p,pts);out[cp]=p.glyph()
    return out


if __name__=='__main__':
    for weight in (78,108):
        glyphs=terminal_glyphs(weight)
        assert len(glyphs)==424,len(glyphs)
        for cp,g in glyphs.items():
            if g.numberOfContours:
                g.recalcBounds(None)
                assert 0<=g.xMin<=g.xMax<=600,(hex(cp),g.xMin,g.xMax)
                assert B<=g.yMin<=g.yMax<=T,(hex(cp),g.yMin,g.yMax)
    print('424 terminal glyphs: regular/bold coverage and cell bounds verified.')
