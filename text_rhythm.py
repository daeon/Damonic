"""Upright lowercase optical drawings for a more open reading rhythm."""

def upright_specs(weight):
    """Keep the 600-unit cell and overshoots; open crowded joins and mouths."""
    bold = weight >= 100
    # The larger eye in e leaves room for the heavier crossbar in Bold.
    bar = 239 if bold else 250
    return {
        'a': [
            'M146 423 C187 471 238 501 305 501 C415 501 471 431 471 333 L471 0',
            'M471 284 C418 310 355 320 288 320 C183 320 110 260 110 170 C110 80 173 29 268 29 C350 29 426 76 471 145',
        ],
        'c': ['M466 403 C433 466 378 501 303 501 C193 501 112 401 112 265 C112 131 193 29 305 29 C378 29 433 62 464 124'],
        'e': [f'M107 {bar} L481 {bar} C486 385 423 501 305 501 C190 501 107 399 107 258 C107 125 191 29 306 29 C372 29 416 58 452 104'],
        'o': ['M302 501 C414 501 489 390 489 266 C489 137 411 29 298 29 C185 29 111 135 111 262 C111 392 188 501 302 501 Z'],
        's': ['M453 413 C418 469 367 501 298 501 C200 501 130 451 130 379 C130 313 188 281 299 252 C408 224 468 185 468 120 C468 60 406 29 307 29 C220 29 156 62 119 117'],
    }


def shoulder_specs(char, weight):
    """Spaced arches with lower entries; preserve the main stem weights."""
    w = weight
    if char in 'nh':
        left = 122 + w / 2
        right = 477 + w / 2
        inside = 477 - w / 2
        top = 735 if char == 'h' else 530
        crown = 536 - w * .78
        return (
            f'M{122-w/2} 0 L{122-w/2} {top} L{left} {top} L{left} 0 Z',
            f'M{left} 391 C211 478 262 536 331 536 C448 536 {right} 450 {right} 311 L{right} 0 L{inside} 0 L{inside} 311 C{inside} 412 397 {crown} 328 {crown} C255 {crown} 205 387 {left} 317 Z',
        )
    if char == 'r':
        left = 200 + w / 2
        crown = 538 - w * .82
        return (
            f'M{200-w/2} 0 L{200-w/2} 530 L{left} 530 L{left} 0 Z',
            f'M{left} 401 C264 484 327 538 397 538 C452 538 501 524 539 491 L500 435 C468 455 431 {crown} 391 {crown} C323 {crown} 273 389 {left} 328 Z',
        )
    # Narrower Bold arches leave visible separation in minimum/committed.
    mw = w * (.74 if w < 100 else .69)
    crown = 534 - w * .70
    specs = [f'M{80-mw/2} 0 L{80-mw/2} 530 L{80+mw/2} 530 L{80+mw/2} 0 Z']
    for entry, exit, peak in [(80, 300, 208), (300, 520, 428)]:
        left, right, inside = entry+mw/2, exit+mw/2, exit-mw/2
        specs.append(
            f'M{left} 398 C{left+26} 477 {peak-40} 534 {peak} 534 C{right-22} 534 {right} 457 {right} 331'
            f' L{right} 0 L{inside} 0 L{inside} 331 C{inside} 418 {peak+33} {crown} {peak-3} {crown}'
            f' C{peak-43} {crown} {left+14} 391 {left} 325 Z'
        )
    return tuple(specs)
