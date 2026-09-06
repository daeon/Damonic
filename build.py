"""Damonic: original parametric outline source. No source-font outlines used."""
from pathlib import Path
import math, unicodedata, json, re, os, time
import pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib.tables._g_l_y_f import flagOverlapSimple

ROOT=Path(__file__).parent
# Commands are original centreline designs; curves expand to closed cubic outlines.
D={}
def setg(chars, *strokes):
 for c in chars:D[c]=list(strokes)
# M/L/C/Q/Z path parser; Q not used.
setg('A','M90 0 L278 710 L322 710 L510 0','M161 255 L439 255')
setg('B','M115 0 L115 710','M115 671 L322 671 C490 671 493 381 318 381 L115 381','M115 381 L330 381 C522 381 523 39 322 39 L115 39')
setg('C','M491 590 C440 678 364 681 299 681 C154 681 100 549 100 355 C100 161 154 29 299 29 C385 29 447 55 495 127')
setg('D','M112 0 L112 710','M112 671 L276 671 C449 671 502 539 502 355 C502 170 449 39 276 39 L112 39')
setg('E','M490 671 L120 671 L120 39 L490 39','M120 370 L438 370')
setg('F','M125 0 L125 671 L505 671','M125 382 L451 382')
setg('G','M493 596 C444 662 378 681 300 681 C156 681 100 550 100 355 C100 160 157 29 310 29 C388 29 455 61 489 99 L489 337 L322 337')
setg('H','M115 0 L115 710','M485 0 L485 710','M115 364 L485 364')
setg('I','M135 671 L465 671','M300 671 L300 39','M135 39 L465 39')
setg('J','M183 671 L485 671 L485 213 C485 80 419 29 306 29 C190 29 128 93 113 181')
setg('K','M118 0 L118 710','M500 710 L120 304','M280 470 L508 0')
setg('L','M126 710 L126 39 L500 39')
setg('M','M80 0 L80 710 L121 710 L300 280 L479 710 L520 710 L520 0')
setg('N','M110 0 L110 710 L143 710 L461 0 L490 0 L490 710')
setg('O','M300 681 C443 681 496 556 496 355 C496 155 442 29 300 29 C158 29 104 155 104 355 C104 556 157 681 300 681 Z')
setg('P','M120 0 L120 671 L310 671 C555 671 555 340 310 340 L120 340')
setg('Q',*D['O'],'M348 164 L526 -98')
setg('R',*D['P'],'M305 340 L511 0')
setg('S','M488 584 C457 647 399 681 299 681 C186 681 118 608 118 506 C118 409 196 374 302 350 C414 325 489 282 489 176 C489 84 413 29 299 29 C195 29 131 66 100 132')
setg('T','M60 671 L540 671','M300 671 L300 0')
setg('U','M112 710 L112 231 C112 93 178 29 300 29 C422 29 488 93 488 231 L488 710')
setg('V','M86 710 L281 0 L319 0 L514 710')
setg('W','M67 710 L146 0 L182 0 C226 151 270 402 300 463 C330 402 374 151 418 0 L454 0 L533 710')
setg('X','M103 710 L497 0','M497 710 L103 0')
setg('Y','M86 710 L300 348 L514 710','M300 348 L300 0')
setg('Z','M99 671 L500 671 L99 39 L506 39')
# Lowercase: deliberately open apertures and flat, gently curved shoulders.
setg('a','M134 452 C176 494 234 501 303 501 C422 501 472 439 472 337 L472 0','M472 282 C422 309 358 319 289 319 C181 319 119 262 119 173 C119 76 178 29 269 29 C358 29 427 83 472 143')
setg('b','M120 0 L120 735','M120 398 C161 466 224 501 298 501 C431 501 488 407 488 266 C488 119 425 29 304 29 C224 29 163 61 120 125')
setg('c','M480 425 C437 478 380 501 304 501 C176 501 108 406 108 265 C108 119 180 29 307 29 C389 29 439 54 480 102')
setg('d','M480 0 L480 735','M480 398 C439 466 376 501 302 501 C169 501 112 407 112 266 C112 119 175 29 296 29 C376 29 437 61 480 125')
setg('e','M108 275 L490 275 C490 427 425 501 304 501 C176 501 108 406 108 265 C108 119 180 29 307 29 C389 29 445 55 483 97')
setg('f','M215 0 L215 541 C215 672 270 706 364 706 C409 706 451 695 476 679','M91 491 L470 491')
setg('g','M478 530 L478 30 C478 -120 418 -176 290 -176 C217 -176 161 -156 120 -126','M478 403 C432 468 376 501 298 501 C170 501 112 407 112 271 C112 136 174 49 296 49 C374 49 435 84 478 149')
setg('h','M122 0 L122 735','M122 389 C173 466 236 501 310 501 C417 501 476 449 476 324 L476 0')
setg('i','M75 474 L296 491 L296 129 C296 64 319 39 380 39 L510 39','M110 39 C226 39 296 39 296 129','M296 658 L296 735')
setg('j','M183 491 L353 491 L353 -45 C353 -134 301 -176 228 -176 C179 -176 140 -164 113 -146','M353 658 L353 735')
setg('k','M125 0 L125 735','M492 530 L127 206','M298 361 L499 0')
setg('l','M178 696 L298 696 L298 145 C298 65 331 39 396 39 L448 39')
setg('m','M80 0 L80 530','M80 398 C108 463 153 501 199 501 C262 501 300 457 300 357 L300 0','M300 396 C331 463 375 501 421 501 C487 501 520 455 520 357 L520 0')
setg('n','M122 0 L122 530','M122 389 C173 466 236 501 310 501 C417 501 476 449 476 324 L476 0')
setg('o','M300 501 C430 501 494 407 494 265 C494 123 430 29 300 29 C170 29 106 123 106 265 C106 407 170 501 300 501 Z')
setg('p','M120 -215 L120 530','M120 398 C161 466 224 501 298 501 C431 501 488 407 488 266 C488 119 425 29 304 29 C224 29 163 61 120 125')
setg('q','M480 -215 L480 530','M480 398 C439 466 376 501 302 501 C169 501 112 407 112 266 C112 119 175 29 296 29 C376 29 437 61 480 125')
setg('r','M145 0 L145 530','M145 363 C189 460 245 501 331 501 C373 501 407 490 433 470')
setg('s','M470 429 C434 475 378 501 299 501 C189 501 125 447 125 367 C125 289 198 268 304 246 C414 223 479 194 479 125 C479 63 410 29 302 29 C211 29 150 55 112 99')
setg('t','M262 683 L262 155 C262 66 302 29 380 29 C422 29 463 39 490 58','M97 491 L481 491')
setg('u','M123 530 L123 207 C123 82 182 29 289 29 C363 29 426 65 477 141','M477 530 L477 0')
setg('v','M100 530 L278 0 L322 0 L500 530')
setg('w','M68 530 L159 0 L189 0 C230 126 274 323 300 370 C326 323 370 126 411 0 L441 0 L532 530')
setg('x','M117 530 L483 0','M483 530 L117 0')
setg('y','M104 530 L302 20','M499 530 L300 -8 C246 -156 206 -183 106 -166')
setg('z','M118 491 L479 491 L115 39 L493 39')
# Numerals.
setg('0','M300 681 C435 681 488 556 488 355 C488 155 435 29 300 29 C165 29 112 155 112 355 C112 556 165 681 300 681 Z','M176 131 L424 579')
setg('1','M145 544 L309 680 L309 39','M130 39 L482 39')
setg('2','M119 564 C143 642 207 681 300 681 C419 681 478 611 478 518 C478 424 414 356 324 276 L114 78 L114 39 L501 39')
setg('3','M122 617 C170 660 234 681 303 681 C423 681 478 622 478 529 C478 427 405 370 295 370 L250 370','M295 370 C428 370 493 311 493 201 C493 93 420 29 300 29 C216 29 145 60 105 111')
setg('4','M397 0 L397 710 L359 710 L99 255 L99 229 L520 229')
setg('5','M484 671 L154 671 L134 378 C182 403 232 418 290 418 C414 418 490 346 490 225 C490 104 415 29 295 29 C211 29 144 54 105 98')
setg('6','M468 624 C425 660 381 681 310 681 C162 681 108 530 108 323 C108 127 169 29 301 29 C416 29 489 111 489 235 C489 357 419 422 314 422 C226 422 152 378 110 319')
setg('7','M105 671 L499 671 L246 0')
setg('8','M300 375 C180 375 122 433 122 527 C122 624 187 681 300 681 C413 681 478 624 478 527 C478 433 420 375 300 375 C166 375 108 304 108 203 C108 97 180 29 300 29 C420 29 492 97 492 203 C492 304 434 375 300 375 Z')
setg('9','M132 85 C175 49 219 29 290 29 C438 29 492 180 492 387 C492 583 431 681 299 681 C184 681 111 599 111 475 C111 353 181 288 286 288 C374 288 448 332 490 391')
# ASCII punctuation and operators.
setg('.','M300 0 L300 92')
setg(',','M330 83 C330 0 298 -56 254 -101')
setg(':','M300 0 L300 92','M300 389 L300 474')
setg(';',*D[','],'M300 389 L300 474')
setg('!','M300 710 L300 217','M300 0 L300 92')
setg('?','M131 583 C155 647 211 681 302 681 C411 681 476 621 476 528 C476 457 430 411 366 366 C315 331 300 301 300 221','M300 0 L300 92')
setg("'",'M300 710 L300 507')
setg('"','M207 710 L207 507','M393 710 L393 507')
setg('`','M207 735 L358 594')
setg('(', 'M399 767 C262 650 220 487 220 280 C220 73 262 -91 399 -207')
setg(')', 'M201 767 C338 650 380 487 380 280 C380 73 338 -91 201 -207')
setg('[','M416 741 L234 741 L234 -181 L416 -181')
setg(']','M184 741 L366 741 L366 -181 L184 -181')
setg('{','M458 741 L400 741 C308 741 299 681 299 571 L299 437 C299 343 255 300 151 280 C255 260 299 217 299 123 L299 -11 C299 -121 308 -181 400 -181 L458 -181')
setg('}','M142 741 L200 741 C292 741 301 681 301 571 L301 437 C301 343 345 300 449 280 C345 260 301 217 301 123 L301 -11 C301 -121 292 -181 200 -181 L142 -181')
setg('/','M116 -122 L484 779')
setg('\\','M116 779 L484 -122')
setg('|','M300 -215 L300 780')
setg('-','M124 280 L476 280')
setg('_','M40 -157 L560 -157')
setg('+','M84 280 L516 280','M300 64 L300 496')
setg('=','M98 390 L502 390','M98 171 L502 171')
setg('<','M484 498 L114 280 L484 62')
setg('>','M116 498 L486 280 L116 62')
setg('~','M83 246 C140 342 208 344 300 280 C392 216 460 218 517 314')
setg('^','M122 459 L300 695 L478 459')
setg('*','M300 520 L300 60','M101 405 L499 175','M101 175 L499 405')
setg('#','M239 710 L155 0','M445 710 L361 0','M78 477 L534 477','M54 236 L510 236')
setg('$',*D['S'],'M300 786 L300 -78')
setg('%','M88 0 L512 710','M178 681 C253 681 265 622 265 552 C265 482 253 423 178 423 C103 423 91 482 91 552 C91 622 103 681 178 681 Z','M422 287 C497 287 509 228 509 158 C509 88 497 29 422 29 C347 29 335 88 335 158 C335 228 347 287 422 287 Z')
setg('&','M505 0 L186 422 C88 552 153 681 280 681 C385 681 426 556 350 477 L193 314 C34 150 146 29 283 29 C413 29 465 151 489 307')
setg('@','M451 100 C387 47 339 29 278 29 C134 29 74 161 74 346 C74 548 160 681 306 681 C453 681 528 554 528 365 C528 229 500 177 453 177 C414 177 393 211 393 274 L393 477','M391 417 C366 460 331 477 286 477 C209 477 174 404 174 316 C174 225 210 177 277 177 C331 177 371 216 393 266')
setg(' ','')


def path_for(spec):
 p=pathops.Path(); t=re.findall(r"[MLCZ]|-?\d+(?:\.\d+)?",spec);i=0
 while i<len(t):
  c=t[i];i+=1
  n={'M':2,'L':2,'C':6,'Z':0}[c];v=list(map(float,t[i:i+n]));i+=n
  if c=='M':p.moveTo(*v)
  elif c=='L':p.lineTo(*v)
  elif c=='C':p.cubicTo(*v)
  else:p.close()
 return p

def outline(specs, weight=78, italic=False, thin=1):
 result=pathops.Path()
 for spec in specs:
  if not spec:continue
  p=path_for(spec)
  # Elliptical expansion: vertical strokes remain full weight; horizontal
  # strokes are 88% as thick. Coordinates restore after expansion.
  p=p.transform(1,0,0,1/.88,0,0)
  p.stroke(weight*thin*(1.12 if spec=="M176 131 L424 579" else 1),pathops.LineCap.BUTT_CAP,pathops.LineJoin.ROUND_JOIN,4)
  p=p.transform(1,0,0,.88,0,0)
  p.convertConicsToQuads(0.25)
  result=pathops.op(result,p,pathops.PathOp.UNION)
 if italic:result=result.transform(1,0,math.tan(math.radians(9)),1,-42,0)
 return result

def glyph(p):
 p.simplify()
 pen=TTGlyphPen(None); p.draw(Cu2QuPen(pen,0.6,reverse_direction=True));g=pen.glyph()
 if g.numberOfContours>0:g.flags[0]|=flagOverlapSimple
 return g

def name(cp):return 'uni%04X'%cp if cp<=65535 else 'u%05X'%cp

# Alternate shapes and independently adjusted italic forms.
ITALIC={
 'a':['M470 530 L470 0','M470 398 C429 466 366 501 292 501 C159 501 102 407 102 266 C102 119 165 29 286 29 C366 29 427 61 470 125'],
 'f':['M147 -196 C207 -176 244 -120 244 -28 L244 548 C244 662 294 706 378 706 C419 706 451 695 476 679','M102 491 L478 491'],
 'i':['M218 530 L218 145 C218 65 251 39 316 39 L410 39','M218 658 L218 735'],
 'l':['M227 735 L227 145 C227 65 260 39 325 39 L416 39'],
 't':['M235 683 L235 155 C235 66 275 29 353 29 C395 29 436 39 463 58','M97 491 L454 491']}
from italic_design import italic_specs
ITALIC=italic_specs(D,ITALIC)
from beautify import apply, optical_bowl
apply(D,ITALIC)

ACCENTS={0x301:['M232 592 L385 745'],0x300:['M215 745 L368 592'],0x302:['M172 597 L300 730 L428 597'],0x303:['M140 625 C190 695 238 695 300 651 C362 607 410 607 460 677'],0x308:['M208 628 L208 706','M392 628 L392 706'],0x30A:['M300 739 C359 739 377 708 377 671 C377 634 359 605 300 605 C241 605 223 634 223 671 C223 708 241 739 300 739 Z'],0x327:['M304 -34 L265 -101 C370 -101 392 -184 302 -204 L220 -204'],0x304:['M161 661 L439 661'],0x306:['M160 727 C181 594 419 594 440 727'],0x30C:['M172 730 L300 597 L428 730'],0x307:['M300 628 L300 706'],0x30B:['M186 599 L304 748','M336 599 L454 748'],0x328:['M385 0 C256 -85 272 -181 385 -181 L432 -181']}

def core_outline(c,w):
 """Independent filled shoulder contours with thinner entries and open joins."""
 result=pathops.Path()
 def add(spec):
  nonlocal result
  result=pathops.op(result,path_for(spec),pathops.PathOp.UNION)
 def stem(x,top,width):
  h=width/2;add(f'M{x-h} 0 L{x-h} {top} L{x+h} {top} L{x+h} 0 Z')
 if c in 'nh':
  stem(122,735 if c=='h' else 530,w);left=122+w/2;right=476+w/2;inside=476-w/2
  add(f'M{left} 418 C210 502 258 536 320 536 C446 536 {right} 471 {right} 324 L{right} 0 L{inside} 0 L{inside} 324 C{inside} 422 399 {536-w*.88} 320 {536-w*.88} C251 {536-w*.88} 199 418 {left} 348 Z')
 elif c=='r':
  stem(216,530,w);left=216+w/2;inner=538-w*.88
  add(f'M{left} 424 C267 502 307 538 352 538 C443 538 501 524 550 505 L517 445 C474 458 422 {inner} 352 {inner} C305 {inner} 262 418 {left} 338 Z')
 else:
  # The two m arches get a lighter stem and a broader, flatter crown so their
  # shared joins do not darken or pinch at small sizes.
  mw=w*.74;stem(80,530,mw)
  for leftcenter,rightcenter,peak in [(80,300,204),(300,520,424)]:
   left=leftcenter+mw/2;right=rightcenter+mw/2;inside=rightcenter-mw/2;inner=534-w*.76
   add(f'M{left} 418 C{left+29} 499 {peak-34} 534 {peak} 534 C{right-18} 534 {right} 470 {right} 347 L{right} 0 L{inside} 0 L{inside} 347 C{inside} 428 {peak+32} {inner} {peak} {inner} C{peak-36} {inner} {left+12} 414 {left} 349 Z')
 return result


from latin import LATIN_EXTRA
from marks import feature_text
def build(style):
 bold='Bold' in style;ital='Italic' in style;w=108 if bold else 84
 paths={};glyphs={};cmap={};metrics={}
 for c,spec in D.items():
  cp=ord(c);nm=name(cp)
  # Crowded shapes need optical stroke reductions rather than equal mechanical weight.
  thin=(1.14 if ital and c in ".,:;!?\'\"`-_=+<>~^*/\\|()[]{}" else (.85 if c in 'mwMW%@&' else (.92 if c in '*#' else 1)))
  paths[cp]=optical_bowl(c,w,path_for,pathops) if not ital and c in 'bdpq' else core_outline(c,w) if not ital and c in 'nhrm' else outline(ITALIC.get(c,spec) if ital else spec,w,ital,thin)
  glyphs[nm]=glyph(paths[cp]);cmap[cp]=nm;metrics[nm]=(600,0)
 # Additional original Latin letters, preserving fixed-width proportions.
 additional={
  0xD8:[*D['O'],'M92 -20 L508 730'],0xF8:[*D['o'],'M101 -45 L499 575'],
  0xD0:[*D['D'],'M43 355 L316 355'],
  0xF0:['M156 701 C364 756 494 501 494 265 C494 123 430 29 300 29 C170 29 106 123 106 265 C106 407 170 501 300 501 C395 501 459 437 480 351','M202 585 L428 720'],
  0xDE:['M120 0 L120 710','M120 556 L310 556 C555 556 555 225 310 225 L120 225'],
  0xFE:['M120 -215 L120 735',D['p'][1]],
  0xDF:['M121 0 L121 497 C121 635 178 706 288 706 C398 706 459 646 459 548 C459 457 409 418 330 376 C440 343 492 278 492 187 C492 83 437 29 348 29 L268 29'],
  0xC6:['M65 0 L240 710 L305 710 L305 39 L539 39','M305 671 L539 671','M305 367 L509 367','M126 255 L305 255'],
  0xE6:['M96 444 C131 486 160 501 204 501 C266 501 298 445 298 330 L298 0','M298 283 C249 316 212 319 177 319 C116 319 78 262 78 173 C78 76 115 29 173 29 C226 29 271 83 298 143','M298 275 L530 275 C530 427 490 501 417 501 C340 501 298 406 298 265 C298 119 342 29 419 29 C468 29 502 55 525 97'],
  0x141:[*D['L'],'M62 287 L387 500'],0x142:[*D['l'],'M134 257 L438 465']
 }
 for cp,spec in additional.items():
  paths[cp]=outline(spec,w,ital,.88 if cp in (0xC6,0xE6) else 1)
  nm=name(cp);glyphs[nm]=glyph(paths[cp]);cmap[cp]=nm;metrics[nm]=(600,0)
 # Complete the requested Latin Extended-A range, including letters whose
 # Unicode decomposition is not canonical. Existing ASCII geometry remains the
 # source for every fallback; only the explicitly listed crossing is added.
 for cp in range(0xA0,0x180):
  if cp in cmap: continue
  spec=LATIN_EXTRA.get(cp)
  if spec is not None:
   spec=[part for x in spec for part in (D[x] if len(x)==1 and x in D else [x])]
  if spec is None:
   # Undesigned codepoints remain absent so coverage QA catches them.
   continue
  p=outline(spec,w,ital);nm=name(cp);glyphs[nm]=glyph(p);paths[cp]=p;cmap[cp]=nm;metrics[nm]=(600,0)
 # Dotless i/j for proper accent composition.
 for cp,base in [(0x131,'i'),(0x237,'j')]:
  paths[cp]=outline((ITALIC.get(base,D[base]) if ital else D[base])[:-1],w,ital)
  nm=name(cp);glyphs[nm]=glyph(paths[cp]);cmap[cp]=nm;metrics[nm]=(600,0)
 for cp in range(0xA0,0x180):
  decomp=unicodedata.normalize('NFD',chr(cp))
  if len(decomp)!=2 or ord(decomp[0]) not in paths or ord(decomp[1]) not in ACCENTS:continue
  base,ac=decomp; bp=paths[0x131] if base=='i' else paths[ord(base)]
  ap=outline(ACCENTS[ord(ac)],w*.84,ital)
  if base.isupper() and ord(ac)!=0x327 and ord(ac)!=0x328:ap=ap.transform(1,0,0,1,0,170)
  p=pathops.op(bp,ap,pathops.PathOp.UNION);nm=name(cp)
  glyphs[nm]=glyph(p);paths[cp]=p;cmap[cp]=nm;metrics[nm]=(600,0)
 for ac,spec in ACCENTS.items():
  nm=name(ac);glyphs[nm]=glyph(outline(spec,w*.84,ital).transform(1,0,0,1,-600,0));cmap[ac]=nm;metrics[nm]=(0,-600)
 # Explicit useful non-ASCII shapes, original geometry.
 extras={
  0xA0:[''],0xA1:['M300 491 L300 406','M300 274 L300 -215'],
  0xA4:['M300 681 C443 681 496 556 496 355 C496 155 442 29 300 29 C158 29 104 155 104 355 C104 556 157 681 300 681','M76 445 L524 445','M76 265 L524 265'],
  0xA7:['M440 680 C350 720 180 660 180 540 C180 440 420 400 420 280 C420 160 250 100 160 140','M160 420 C250 380 420 340 420 220 C420 100 250 40 160 80'],
  0xA8:['M208 628 L208 706','M392 628 L392 706'],0xAA:D['a'],0xAE:["M300 681 C460 681 553 544 553 355 C553 166 460 29 300 29 C140 29 47 166 47 355 C47 544 140 681 300 681 Z","M300 620 C380 620 425 550 425 355 C425 160 380 90 300 90 C220 90 175 160 175 355 C175 550 220 620 300 620 Z","M180 120 L430 590"],
  0xB2:D['2'],0xB3:D['3'],0xB5:D['u'],0xB6:['M120 0 L120 710 L300 710 C500 710 500 420 300 420 L120 420'],0xB8:['M300 0 L300 92'],0xB9:D['1'],0xBA:D['o'],
  0xBC:['M100 0 L100 350 L320 350','M100 220 L320 220','M380 710 L380 0','M300 430 L500 430 L300 0 L500 0'],
  0xBD:['M100 350 L320 350 L320 220 L100 220','M100 0 L100 350','M380 710 L380 0','M300 430 L500 430 L300 0 L500 0'],
  0xBE:['M100 350 L320 350 L320 220 L100 220','M100 0 L100 350','M380 710 L380 0','M300 430 L500 430 L300 0 L500 0'],0xA2:[*D['c'],'M300 616 L300 -83'],
  0xA3:['M479 610 C435 663 382 681 313 681 C203 681 159 608 190 480 L235 294 C268 154 190 72 107 39 L498 39','M87 328 L441 328'],
  0xA5:[*D['Y'],'M116 291 L484 291','M116 149 L484 149'],0xA6:['M300 780 L300 368','M300 195 L300 -215'],
  0xA9:['M480 425 C437 478 380 501 304 501 C176 501 108 406 108 265 C108 119 180 29 307 29 C389 29 439 54 480 102'],
  0xAB:['M290 465 L110 280 L290 95','M510 465 L330 280 L510 95'],0xAC:['M83 372 L510 372 L510 136'],
  0xAD:D['-'],0xAF:ACCENTS[0x304],0xB0:['M300 688 C384 688 425 635 425 561 C425 487 384 434 300 434 C216 434 175 487 175 561 C175 635 216 688 300 688 Z'],
  0xB1:[*D['+'],'M84 -80 L516 -80'],0xB4:ACCENTS[0x301],0xB7:['M300 238 L300 322'],0xBB:['M90 465 L270 280 L90 95','M310 465 L490 280 L310 95'],
  0xBF:['M300 491 L300 406','M300 270 C300 190 258 170 212 138 C148 95 124 46 124 -8 C124 -108 189 -176 298 -176 C389 -176 445 -142 469 -78'],
  0xD7:['M126 454 L474 106','M126 106 L474 454'],0xF7:['M84 280 L516 280','M300 475 L300 552','M300 8 L300 85'],
  0x2010:D['-'],0x2013:['M44 280 L556 280'],0x2014:['M0 280 L600 280'],
  0x2018:['M338 749 C292 703 270 650 270 568'],0x2019:['M330 749 C330 667 308 614 262 568'],
  0x201A:['M270 180 C270 98 292 45 338 -1'],
  0x201C:['M188 749 C142 703 120 650 120 568','M388 749 C342 703 320 650 320 568'],
  0x201D:['M280 749 C280 667 258 614 212 568','M480 749 C480 667 458 614 412 568'],
  0x201E:['M280 180 C280 98 302 45 348 -1','M480 180 C480 98 502 45 548 -1'],
  0x2022:['M300 204 L300 356'],0x2026:['M110 0 L110 74','M300 0 L300 74','M490 0 L490 74'],
  0x20AC:[*D['C'],'M53 437 L404 437','M53 276 L365 276'],
  0x2190:['M75 280 L525 280','M271 482 L69 280 L271 78'],0x2192:['M75 280 L525 280','M329 482 L531 280 L329 78'],
  0x2191:['M300 36 L300 660','M103 452 L300 665 L497 452'],0x2193:['M300 674 L300 50','M103 258 L300 45 L497 258'],
  0x2212:D['-'],0x2215:D['/'],0x2260:[*D['='],'M190 29 L410 532'],0x2264:[*D['<'],'M98 -69 L502 -69'],0x2265:[*D['>'],'M98 -69 L502 -69'],
  0x221E:['M300 280 C161 508 69 450 69 280 C69 110 161 52 300 280 C439 508 531 450 531 280 C531 110 439 52 300 280 Z'],
  0x2713:['M85 276 L236 98 L516 595'],0x2717:['M130 540 L470 20','M470 540 L130 20'],  0x0132:[*D['I'],*D['J']],0x0133:[*D['i'],*D['j']],0x0149:[*D["n"],"M190 735 L300 600"],
  0x0152:[*D['O'],*D['E']],0x0153:[*D['o'],*D['e']],0x017F:D['s'],

 }
 # Ellipsis and bullets balanced using reduced strokes.
 for cp,spec in extras.items():
  p=outline(spec,w,ital);nm=name(cp);glyphs[nm]=glyph(p);cmap[cp]=nm;metrics[nm]=(600,0)
 # Semantically accurate small forms and paired-letter compositions.
 from latin_refine import refinements
 for cp,p in refinements(D,outline,w,ital,pathops).items():
  nm=name(cp);glyphs[nm]=glyph(p);paths[cp]=p;cmap[cp]=nm;metrics[nm]=(600,0)
 # Correct copyright: circled, scaled C rather than unsupported substitute.
 outer=outline(['M300 681 C460 681 553 544 553 355 C553 166 460 29 300 29 C140 29 47 166 47 355 C47 544 140 681 300 681 Z'],w*.60)
 inner=outline(D['C'],w).transform(.50,0,0,.65,150,125)
 glyphs[name(0xA9)]=glyph(pathops.op(outer,inner,pathops.PathOp.UNION))
 # Zero alternates accessible in stylistic sets.
 plainzero=outline(D['0'][:1],w,ital)
 dot=outline(['M300 312 L300 397'],w,ital)
 glyphs['zero.dotted']=glyph(pathops.op(plainzero,dot,pathops.PathOp.UNION));metrics['zero.dotted']=(600,0)
 glyphs['l.simple']=glyph(outline(['M300 735 L300 0'],w,ital));metrics['l.simple']=(600,0)
 from terminal import terminal_glyphs
 for cp,g in terminal_glyphs(w).items():
  nm=name(cp);glyphs[nm]=g;cmap[cp]=nm;metrics[nm]=(600,0)
 # Small optional ligature set. Only spans source cells; never required for terminal use.
 ligs={
  'arrowright':('->',['M130 280 L1050 280','M818 488 L1057 280 L818 72']),
  'arrowleft':('<-',['M150 280 L1070 280','M382 488 L143 280 L382 72']),
  'fatright':('=>',['M130 390 L946 390','M130 170 L946 170','M818 488 L1057 280 L818 72']),
  'equal':('==',['M120 390 L1080 390','M120 171 L1080 171']),
  'notequal':('!=',['M120 390 L1080 390','M120 171 L1080 171','M490 20 L710 542']),
  'lessequal':('<=',['M559 498 L159 280 L559 62','M691 390 L1080 390','M691 171 L1080 171']),
  'greaterequal':('>=',['M159 498 L559 280 L159 62','M691 390 L1080 390','M691 171 L1080 171'])}
 for key,(seq,spec) in ligs.items():
  nm='lig.'+key;glyphs[nm]=glyph(outline(spec,w,ital));metrics[nm]=(600*len(seq),0)
 ng=glyph(outline(['M100 0 L100 710 L500 710 L500 0 Z','M100 0 L500 710'],w*.7))
 glyphs['.notdef']=ng;metrics['.notdef']=(600,0)
 order=['.notdef']+sorted(n for n in glyphs if n!='.notdef')
 # Per-glyph terminal containment after italic design and accent composition.
 # Preserve all advances. Shift a shape when it fits; scale only exceptional
 # wider-than-cell outlines, recording every adjustment for review.
 containment=[]
 for cp,nm in sorted(cmap.items()):
  if unicodedata.category(chr(cp)).startswith('M') or not glyphs[nm].numberOfContours:continue
  g=glyphs[nm];bp=BoundsPen(None);g.draw(bp,None)
  x0,y0,x1,y1=bp.bounds
  if x0>=0 and x1<=600:continue
  width=x1-x0;scale=min(1,596/width)
  shift=max(2-x0*scale,min(0,598-x1*scale))
  pen=TTGlyphPen(None);g.draw(TransformPen(pen,(scale,0,0,1,shift,0)),None)
  glyphs[nm]=pen.glyph()
  containment.append({'codepoint':f'U+{cp:04X}','original_bounds':[x0,x1],'scale_x':scale,'shift_x':shift})
 (ROOT/('containment-'+style.replace(' ','')+'.json')).write_text(json.dumps(containment,indent=2))
 # Actual left bearings are required for correct raster positioning.
 for nm,g in glyphs.items():
  if g.numberOfContours: g.recalcBounds(None);metrics[nm]=(metrics[nm][0],g.xMin)
 fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(cmap);fb.setupGlyf(glyphs)
 fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1000,descent=-250,lineGap=0,caretSlopeRise=1000 if ital else 1,caretSlopeRun=158 if ital else 0)
 fb.setupNameTable({'familyName':'Damonic','styleName':style,'uniqueFontIdentifier':f'Damonic-0.401-alpha-{style.replace(" ","") }','fullName':f'Damonic {style}','psName':f'Damonic-{style.replace(" ","") }','version':'Version 0.401 alpha','copyright':'Copyright 2026 Damonic contributors. Original outlines.','manufacturer':'Damonic Project','vendorURL':'https://openfontlicense.org/','designer':'Damonic Project','description':'Original humanist monospaced coding and terminal typeface. Version 0.401 alpha.','licenseDescription':'SIL Open Font License, Version 1.1','licenseInfoURL':'https://openfontlicense.org/','typographicFamily':'Damonic','typographicSubfamily':style})
 fs=(1 if ital else 0)|(32 if bold else 0)|(64 if not ital and not bold else 0)|128
 fb.setupOS2(version=4,sTypoAscender=1000,sTypoDescender=-250,sTypoLineGap=0,usWinAscent=1000,usWinDescent=250,usWeightClass=700 if bold else 400,usWidthClass=5,fsSelection=fs,sxHeight=530,sCapHeight=710,yStrikeoutPosition=280,yStrikeoutSize=50)
 fb.font['OS/2'].recalcCodePageRanges(fb.font)
 fb.setupPost(isFixedPitch=1,italicAngle=-9 if ital else 0,underlinePosition=-120,underlineThickness=50)
 fb.setupMaxp();fb.font['head'].fontRevision=0.401;fb.font['head'].macStyle=(1 if bold else 0)|(2 if ital else 0)
 fb.font['OS/2'].achVendID='DAMN';fb.font['OS/2'].fsType=0
 fb.font['OS/2'].panose.bFamilyType=2;fb.font['OS/2'].panose.bProportion=9
 fea='languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n'
 fea+='feature ss01 { featureNames { name \"Dotted zero\"; }; sub uni0030 by zero.dotted; } ss01;\nfeature ss02 { featureNames { name \"Simple lowercase l\"; }; sub uni006C by l.simple; } ss02;\n'
 fea+='feature dlig {\n'+''.join(' sub '+' '.join(name(ord(c)) for c in seq)+' by lig.'+k+';\n' for k,(seq,_) in ligs.items())+'} dlig;\n'
 # Mark anchors allow decomposed Latin accents and stacked accents.
 fea += feature_text(ACCENTS, name, cmap, glyphs)
 (ROOT/'dist'/f'Damonic-{style.replace(" ","")}.fea').write_text(fea)
 addOpenTypeFeaturesFromString(fb.font,fea)
 fb.font['name'].names=[n for n in fb.font['name'].names if n.platformID!=1]
 from fontTools.otlLib.builder import buildStatTable
 buildStatTable(fb.font,[{'tag':'wght','name':'Weight','values':[{'value':700 if bold else 400,'name':'Bold' if bold else 'Regular','flags':0 if bold else 2}]},{'tag':'ital','name':'Italic','values':[{'value':1 if ital else 0,'name':'Italic' if ital else 'Roman','flags':0 if ital else 2}]}])
 # Gasp smoothing flags; no claim of manual TrueType hinting.
 from fontTools.ttLib import newTable
 fb.font['gasp']=newTable('gasp');fb.font['gasp'].gaspRange={65535:15}
 out=ROOT/'dist'/f'Damonic-{style.replace(" ","")}.ttf'
 # Reproducible builds: fontTools otherwise stamps the current wall clock.
 epoch=int(os.environ.get('SOURCE_DATE_EPOCH','1788566400'))
 mac_epoch=epoch+2082844800
 fb.font['head'].created=mac_epoch;fb.font['head'].modified=mac_epoch
 fb.font.recalcTimestamp=False
 fb.save(out)
 return {'style':style,'glyphs':len(order),'mapped_characters':len(cmap),'file':out.name}

if __name__=='__main__':
 (ROOT/'dist').mkdir(exist_ok=True)
 result=[build(s) for s in ['Regular','Italic','Bold','Bold Italic']]
 (ROOT/'buildmanifest.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
