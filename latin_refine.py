"""Original semantic drawings and compact compositions for Latin additions."""
def refinements(D, outline, w, italic, pathops):
    result = {}
    def draw(spec, weight=1):
        return outline(spec, w*weight, italic)
    def union(*parts):
        p = pathops.Path()
        for part in parts:
            p = pathops.op(p, part, pathops.PathOp.UNION)
        return p
    def compact(c, sx, sy, dx, dy):
        return draw(D[c]).transform(sx, 0, 0, sy, dx, dy)
    # Distinctive descending right stem of eng; no invented crossbar.
    result[0x14A] = draw(['M110 0 L110 710 L143 710 L475 20',
        'M490 710 L490 -32 C490 -150 438 -186 337 -174'])
    result[0x14B] = draw(['M122 0 L122 530',
        'M122 389 C173 466 236 501 310 501 C417 501 476 449 476 324 L476 -32 C476 -150 422 -186 326 -174'])
    result[0x111] = draw([*D['d'], 'M330 635 L560 635'])
    result[0x127] = draw([*D['h'], 'M55 635 L315 635'])
    result[0x138] = draw(['M125 0 L125 530','M492 530 L127 206','M298 361 L499 0'])
    result[0x13F] = union(draw(D['L']), draw(['M420 285 L420 330']))
    result[0x140] = union(draw(D['l']), draw(['M475 285 L475 330']))
    result[0x132] = union(compact('I',.48,1,0,0), compact('J',.48,1,300,0))
    result[0x133] = union(compact('i',.48,1,0,0), compact('j',.48,1,300,0))
    result[0x152] = union(compact('O',.60,1,0,0), compact('E',.48,1,292,0))
    result[0x153] = union(compact('o',.60,1,0,0), compact('e',.48,1,292,0))
    result[0x17F] = draw(['M220 0 L220 541 C220 672 275 706 369 706 C414 706 456 695 481 679', 'M96 491 L403 491'])
    # Currency sign has four rays around a small ring, rather than a letter.
    result[0xA4] = draw(['M300 492 C411 492 460 419 460 320 C460 221 411 148 300 148 C189 148 140 221 140 320 C140 419 189 492 300 492 Z',
        'M102 530 L187 440','M498 530 L413 440','M102 110 L187 200','M498 110 L413 200'], .83)
    result[0xA7] = draw(['M454 647 C403 706 214 710 172 618 C118 503 279 446 373 393 C497 322 452 193 327 185 C232 181 153 233 150 320 C147 407 254 454 345 409',
        'M147 72 C216 3 391 11 437 98 C490 199 346 267 237 326'], .90)
    result[0xAE] = union(draw(['M300 681 C460 681 553 544 553 355 C553 166 460 29 300 29 C140 29 47 166 47 355 C47 544 140 681 300 681 Z'], .60), compact('R',.48,.64,145,126))
    result[0xAA] = compact('a',.65,.65,105,365)
    result[0xBA] = compact('o',.65,.65,105,365)
    for cp,c in [(0xB9,'1'),(0xB2,'2'),(0xB3,'3')]:
        result[cp] = compact(c,.65,.57,105,320)
    result[0xB5] = draw(['M123 -215 L123 530','M123 207 C123 82 182 29 289 29 C363 29 426 65 477 141','M477 530 L477 0'])
    result[0xB6] = draw(['M330 0 L330 671 L250 671 C71 671 70 360 250 360 L330 360','M478 710 L478 0'], .85)
    result[0xB8] = draw(['M304 -34 L265 -101 C370 -101 392 -184 302 -204 L220 -204'], .84)
    for cp,num,den in [(0xBC,'1','4'),(0xBD,'1','2'),(0xBE,'3','4')]:
        result[cp] = union(compact(num,.40,.46,-8,376), compact(den,.40,.46,342,0),
            draw(['M170 20 L430 690'],.60))
    return result
