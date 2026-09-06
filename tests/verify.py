#!/usr/bin/env python3
"""Independent Damonic 0.4 QA.  Emits a machine-readable JSON report."""
from __future__ import annotations
import argparse, json, os, sys, tempfile, unicodedata
from pathlib import Path

try:
    from fontTools.ttLib import TTFont, TTCollection
    from fontTools.pens.boundsPen import BoundsPen
    import uharfbuzz as hb
except Exception as exc:  # report a useful failure rather than silently skipping QA
    print(json.dumps({"ok": False, "checks": [{"name": "dependencies", "ok": False, "detail": str(exc)}]}, indent=2))
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
STYLES = {"Regular": (False, False), "Italic": (False, True), "Bold": (True, False), "BoldItalic": (True, True)}
REQUIRED = set(range(0xA0, 0x100)) | set(range(0x100, 0x180)) | {0x00AB,0x00BB,0x2010,0x2013,0x2014,0x2018,0x2019,0x201C,0x201D,0x201E,0x2022,0x2026}
MARKS = {cp for cp in range(0x300, 0x370) if unicodedata.category(chr(cp)) in ("Mn", "Me")}

def result(name, ok, detail=""):
    return {"name": name, "ok": bool(ok), "detail": str(detail)}

def names(font, nid):
    return {x.toUnicode() for x in font["name"].names if x.nameID == nid}

def shape(path, text, features=None):
    data = Path(path).read_bytes(); face = hb.Face(data); font = hb.Font(face)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, features or {})
    return [(i.codepoint, i.cluster, p.x_advance, p.x_offset, p.y_offset) for i,p in zip(buf.glyph_infos, buf.glyph_positions)]

def check_font(path):
    out = []; font = TTFont(path, recalcBBoxes=False); cmap = font.getBestCmap()
    style = path.stem.removeprefix("Damonic-")
    bold, italic = STYLES.get(style, (None, None))
    out.append(result("family name", "Damonic" in (names(font,16)|names(font,1)), sorted(names(font,1)|names(font,16))))
    out.append(result("style name", style in STYLES, style))
    out.append(result("revision 0.402", abs(font["head"].fontRevision-.402) < 1/65536, font["head"].fontRevision))
    uid = names(font,3)
    out.append(result("unique ID identifies Damonic style", any("Damonic" in x and style in x for x in uid), sorted(uid)))
    out.append(result("OS/2 fsType zero", font["OS/2"].fsType == 0, font["OS/2"].fsType))
    out.append(result("vendor DAMN", font["OS/2"].achVendID.strip() == "DAMN", font["OS/2"].achVendID))
    if bold is not None:
        fs, ms = font["OS/2"].fsSelection, font["head"].macStyle
        out.append(result("style linking flags", bool(fs&32)==bold and bool(fs&1)==italic and bool(ms&1)==bold and bool(ms&2)==italic, {"fsSelection":fs,"macStyle":ms}))
    missing = [cp for cp in REQUIRED if cp not in cmap]
    out.append(result("Latin1/Extended-A and quotes coverage", not missing, [f"U+{x:04X}" for x in missing[:20]]))
    empty=[]; bounds=[]; glyphset=font.getGlyphSet()
    for cp, gn in cmap.items():
        pen=BoundsPen(glyphset); glyphset[gn].draw(pen)
        if pen.bounds is None and not chr(cp).isspace() and cp not in (0x2800,): empty.append(f"U+{cp:04X}")
        if pen.bounds and cp not in MARKS and unicodedata.category(chr(cp)) not in ("Mn","Me"):
            x0,y0,x1,y1=pen.bounds
            if x0 < -2 or x1 > 602: bounds.append(f"U+{cp:04X}:{x0:g}..{x1:g}")
    out.append(result("mapped glyphs nonempty (spaces exempt)", not empty, empty[:20]))
    out.append(result("basic horizontal bounds", not bounds, bounds[:20]))
    badwidth=[]
    for cp,gn in cmap.items():
        want=0 if unicodedata.category(chr(cp)) in ("Mn","Me") else 600
        if font["hmtx"][gn][0] != want: badwidth.append(f"U+{cp:04X}={font['hmtx'][gn][0]}")
    out.append(result("mapped advances 600 / marks 0", not badwidth, badwidth[:20]))
    # Each feature must cause a substantive substitution, and dlig must collapse a pair.
    for tag, text in (("ss01","0"),("ss02","l"),("dlig","->")):
        off=shape(path,text,{tag:False}); on=shape(path,text,{tag:True})
        changed = [x[0] for x in off] != [x[0] for x in on] or len(off)!=len(on)
        out.append(result(f"HarfBuzz {tag} on/off changes", changed, {"off":len(off),"on":len(on)}))
    # Repeated acute deliberately avoids a precomposed character. Compare the
    # effective positions with both mark features disabled and enabled.
    stacked_off=shape(path,"A\u0301\u0307",{"mark":False,"mkmk":False})
    stacked_on=shape(path,"A\u0301\u0307",{"mark":True,"mkmk":True})
    # (Keep cursor arithmetic explicit; offsets are in font units.)
    def positions(rows):
        x=0; ans=[]
        for gid,cluster,adv,xoff,yoff in rows:
            ans.append((x+xoff,yoff)); x += adv
        return ans
    pon, poff=positions(stacked_on),positions(stacked_off)
    # At least one mark must acquire a distinct effective vertical placement.
    distinct=any(a != b for a,b in zip(pon[1:],poff[1:]))
    out.append(result("stacked mark positioning", len(stacked_on)>=2 and distinct, {"off":poff,"on":pon}))
    gpos_tags=[]
    if "GPOS" in font and font["GPOS"].table.FeatureList:
        gpos_tags=[r.FeatureTag for r in font["GPOS"].table.FeatureList.FeatureRecord]
    out.append(result("GPOS mark and mkmk features", "mark" in gpos_tags and "mkmk" in gpos_tags, gpos_tags))
    return font, cmap, out

def compare_ascii(font, baseline, style):
    checks=[]
    if not baseline.exists(): return [result("baseline available", False, str(baseline))]
    # Compare only the corresponding weight/slant; comparing against all four
    # styles would report every intentional style difference as a regression.
    p = baseline / f"BearingMono-{style}.ttf"
    if not p.exists(): return [result("matching baseline style available", False, str(p))]
    for p in [p]:
        old=TTFont(p, recalcBBoxes=False); newc=font.getBestCmap(); oldc=old.getBestCmap(); dif=[]
        for cp in range(0x20,0x7F):
            if cp not in oldc or cp not in newc: continue
            a=old["glyf"][oldc[cp]]; b=font["glyf"][newc[cp]]
            try: ac=a.getCoordinates(old["glyf"])[0]; bc=b.getCoordinates(font["glyf"])[0]
            except Exception: continue
            if list(ac)!=list(bc): dif.append(f"U+{cp:04X}")
        checks.append(result(f"ASCII contours vs {p.name}", not dif, dif[:20]))
    return checks

def nerd_checks(path, reference=None):
    checks=[]
    if not path.exists(): return [result("Nerd Font artifacts present", False, str(path))]
    f=TTFont(path, recalcBBoxes=False); cmap=f.getBestCmap(); symbols=[cp for cp in cmap if cp>=0xE000]
    empty=[]; bounds=[]; ref_empty=set(); refc={}
    if reference and reference.exists():
        rf=TTFont(reference, recalcBBoxes=False); refc=rf.getBestCmap(); rgs=rf.getGlyphSet()
        for cp,gn in refc.items():
            rp=BoundsPen(rgs); rgs[gn].draw(rp)
            if rp.bounds is None: ref_empty.add(cp)
    for cp,gn in cmap.items():
        pen=BoundsPen(f.getGlyphSet()); f.getGlyphSet()[gn].draw(pen)
        if pen.bounds is None and not chr(cp).isspace() and cp not in (0x2800,) and cp not in ref_empty: empty.append(f"U+{cp:04X}")
        if pen.bounds and unicodedata.category(chr(cp)) not in ("Mn","Me"):
            x0,y0,x1,y1=pen.bounds
            if x0 < -2 or x1 > 602 or y0 < -250 or y1 > 1000: bounds.append(f"U+{cp:04X}:{x0:g},{y0:g}..{x1:g},{y1:g}")
    if reference and reference.exists():
        expected=set(TTFont(reference, lazy=True).getBestCmap())
        missing=sorted(expected-set(cmap)); cmap_ok=not missing; detail=f"{len(cmap)} mapped; reference {len(expected)}; missing {len(missing)}"
    else:
        missing=[]; cmap_ok=False; detail="vendored official SymbolsNerdFontMono v3.5.1 reference required"
    checks=[result("Nerd Font full symbol cmap", cmap_ok, detail), result("Nerd mapped glyphs nonempty", not empty, empty[:20]), result("Nerd bounds 0..600 / -250..1000", not bounds, bounds[:20]), result("Nerd ASCII retention", all(cp in cmap for cp in range(0x20,0x7F)), "")]
    bad=[gn for cp,gn in cmap.items() if unicodedata.category(chr(cp)) not in ("Mn","Me") and f["hmtx"][gn][0] != 600]
    checks.append(result("Nerd mapped advances 600", not bad, bad[:20]))
    return checks

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--baseline", type=Path); ap.add_argument("--nerd-reference", type=Path, help="official SymbolsNerdFontMono.ttf for exact cmap comparison"); args=ap.parse_args()
    checks=[]; dist=ROOT/"dist"; fonts=[]
    for style in STYLES:
        p=dist/f"Damonic-{style}.ttf"
        if not p.exists(): checks.append(result(f"artifact {p.name} present",False,str(p))); continue
        fonts.append(p); font,cmap,got=check_font(p); checks.extend(got)
        if args.baseline: checks.extend(compare_ascii(font,args.baseline/"dist",style))
    nerd_paths=sorted(dist.glob("DamonicNerdFontMono-*.ttf"))
    if len(nerd_paths)!=4: checks.append(result("four Nerd Font artifacts present",False,[p.name for p in nerd_paths]))
    reference=args.nerd_reference
    if reference is None:
        env_ref=os.environ.get("DAMONIC_NERD_REFERENCE")
        reference=Path(env_ref) if env_ref else ROOT/"vendor/symbols-src/SymbolsNerdFontMono-Regular.ttf"
    if reference is None or not reference.exists():
        checks.append(result("official Nerd reference present",False,str(reference or "--nerd-reference / DAMONIC_NERD_REFERENCE")))
    for p in nerd_paths: checks.extend(nerd_checks(p,reference))
    ttc=dist/"Damonic.ttc"
    if not ttc.exists(): checks.append(result("Damonic.ttc present",False,str(ttc)))
    else:
        col=TTCollection(ttc); checks.append(result("TTC has eight faces",len(col.fonts)==8,len(col.fonts)))
        expected=[]
        for style in STYLES:
            expected.append(("Damonic", "Regular" if style=="Regular" else ("Italic" if style=="Italic" else ("Bold" if style=="Bold" else "Bold Italic")), dist/f"Damonic-{style}.ttf"))
        for style in STYLES:
            sub="Regular" if style=="Regular" else ("Italic" if style=="Italic" else ("Bold" if style=="Bold" else "Bold Italic"))
            expected.append(("Damonic Nerd Font Mono",sub,dist/f"DamonicNerdFontMono-{style}.ttf"))
        pairs=[]
        for i,(family,sub,path) in enumerate(expected):
            found=[f for f in col.fonts if f["name"].getDebugName(1)==family and f["name"].getDebugName(2)==sub]
            ok=len(found)==1
            if ok and path.exists():
                tf=found[0]; sf=TTFont(path,recalcBBoxes=False)
                ok=(tf.getBestCmap()==sf.getBestCmap() and all(tf["hmtx"][g][0]==sf["hmtx"][g][0] for g in tf.getBestCmap().values()))
                # Exercise a representative feature/mark sample through the TTC face.
                with tempfile.NamedTemporaryFile(suffix='.ttf') as tmp:
                    tf.save(tmp.name)
                    sample="0l->A\u0301"; feats={"ss01":True,"ss02":True,"dlig":True}
                    ok=ok and shape(tmp.name,sample,feats)==shape(path,sample,feats)
            pairs.append({"family":family,"subfamily":sub,"ok":ok})
        checks.append(result("TTC exact family/style faces and matching TTF tables",all(p["ok"] for p in pairs),pairs))
    report={"ok":all(x["ok"] for x in checks),"checks":checks,"checked_fonts":[p.name for p in fonts]}
    print(json.dumps(report,indent=2,sort_keys=True)); return 0 if report["ok"] else 1
if __name__=="__main__": raise SystemExit(main())
