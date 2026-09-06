"""OpenType mark feature source for Damonic Latin accents."""
import unicodedata

def feature_text(accents, name, cmap, glyphs):
    fea=''
    for cp in accents:
        cls='@BOTTOM' if cp in (0x327,0x328) else '@TOP'
        # Accent outlines are translated -600; -300 centers their local anchor
        # and causes a +600 attachment shift over the base anchor at x=300.
        fea += f'markClass {name(cp)} <anchor -300 {0 if cls=="@BOTTOM" else 580}> {cls};\n'
    # Unicode's soft-dotted rule removes the native dot when an above mark is
    # present.  Use a mark filter so a below mark (for example ogonek) may sit
    # between the base and the above mark without preventing the substitution.
    # The dotless glyphs are emitted before this feature is assembled.
    fea += 'feature ccmp {\n'
    fea += ' lookup soft_dot_suppression {\n'
    fea += '  lookupflag UseMarkFilteringSet @TOP;\n'
    fea += f'  sub {name(ord("i"))}\' @TOP by {name(0x131)};\n'
    fea += f'  sub {name(ord("j"))}\' @TOP by {name(0x237)};\n'
    fea += ' } soft_dot_suppression;\n'
    fea += '} ccmp;\n'
    fea += 'feature mark {\n'
    for cp,nm in sorted(cmap.items()):
        cat=unicodedata.category(chr(cp))
        if cat.startswith('L'):
            g=glyphs[nm]
            y=max(750 if chr(cp).isupper() else 580, getattr(g,'yMax',0)+50)
            bottom=min(0,getattr(g,'yMin',0)-30)
            fea += f' pos base {nm} <anchor 300 {y}> mark @TOP <anchor 300 {bottom}> mark @BOTTOM;\n'
    fea += '} mark;\nfeature mkmk {\n'
    for ac in accents:
        if ac not in (0x327,0x328):
            top=max(760,getattr(glyphs[name(ac)],'yMax',710)+50)
            fea += f' pos mark {name(ac)} <anchor -300 {top}> mark @TOP;\n'
        else:
            bottom=getattr(glyphs[name(ac)],'yMin',-220)-40
            fea += f' pos mark {name(ac)} <anchor -300 {bottom}> mark @BOTTOM;\n'
    return fea + '} mkmk;\n'
