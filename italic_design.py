"""Independent italic skeleton drawings for Bearing Mono 0.2.

Coordinates are BEFORE the builder's nine-degree shear and -42 translation.
No existing font outlines or earlier personal typeface designs are used.
"""

def italic_specs(D, existing):
    """Return complete italic override mapping; leave caller dictionaries intact."""
    out = {c: list(paths) for c, paths in existing.items()}
    out.update({
        # Single-storey a retains a flat exit, with the bowl turning into the stem.
        'a': ['M456 530 L456 0', 'M456 397 C417 468 357 501 286 501 C170 501 121 406 121 265 C121 115 185 29 290 29 C364 29 417 72 456 145'],
        # A rising, flatter shoulder; a curved return removes the sheared-upright feel.
        'n': ['M136 0 L136 530', 'M136 381 C179 462 236 501 302 501 C405 501 454 450 454 341 L454 128 C454 62 472 34 507 29'],
        'h': ['M136 0 L136 735', 'M136 381 C179 462 236 501 302 501 C405 501 454 450 454 341 L454 128 C454 62 472 34 507 29'],
        'm': ['M108 0 L108 530', 'M108 380 C135 465 170 501 215 501 C270 501 296 446 296 345 L296 0', 'M296 380 C323 465 357 501 398 501 C453 501 478 446 478 345 L478 110 C478 57 486 36 507 29'],
        'r': ['M231 0 L231 530', 'M231 355 C252 449 286 501 338 501 C412 501 454 491 492 468'],
        'u': ['M148 530 L148 204 C148 85 192 29 285 29 C352 29 410 75 450 152', 'M450 530 L450 118 C450 60 470 32 505 29'],
        # Subtly curved diagonal exits, without script loops or added swashes.
        'v': ['M122 530 L274 49 C280 31 288 22 300 22 C313 22 322 35 330 56 L475 530'],
        'w': ['M94 530 L164 56 C167 34 173 22 183 22 C193 22 200 34 207 59 L300 370 L396 59 C403 34 410 22 420 22 C431 22 438 36 443 61 L495 530'],
        'y': ['M132 530 L303 28', 'M476 530 L302 19 C257 -113 228 -175 153 -175 L137 -175'],
        # Bowl extrema and stem transitions differ deliberately from upright b/d/p/q.
        'b': ['M136 0 L136 735', 'M136 383 C177 459 228 501 297 501 C408 501 466 416 466 274 C466 125 413 29 303 29 C226 29 174 74 136 138'],
        'd': ['M456 0 L456 735', 'M456 397 C417 468 357 501 286 501 C170 501 121 406 121 265 C121 115 185 29 290 29 C364 29 417 72 456 145'],
        'p': ['M144 -215 L144 530', 'M144 383 C185 459 234 501 301 501 C412 501 466 416 466 274 C466 125 413 29 303 29 C226 29 182 74 144 138'],
        'q': ['M456 -215 L456 530', 'M456 397 C417 468 357 501 286 501 C170 501 121 406 121 265 C121 115 185 29 290 29 C364 29 417 72 456 145'],
        'g': ['M454 530 L454 19 C454 -114 401 -174 300 -174 C231 -174 180 -157 149 -135', 'M454 396 C412 470 357 501 286 501 C174 501 122 407 122 274 C122 138 180 49 290 49 C360 49 415 93 454 155'],
        # Slightly rising crossbar, roomier opening, asymmetric bowl.
        'e': ['M120 264 L466 291 C465 426 407 501 297 501 C175 501 117 404 117 263 C117 112 187 29 304 29 C379 29 433 59 467 110'],
        # f gains an independently placed arch; no clipped ascender terminal.
        'f': ['M155 -190 C215 -173 245 -112 245 -26 L245 544 C245 656 286 706 358 706 C397 706 421 696 445 679', 'M113 491 L455 491'],
        # Extend the italic exits to keep ``ir``/``in`` from opening up after
        # the slanted stem. This is an outline change: the terminal is longer
        # and flatter, while the stem and 600-unit cell remain unchanged.
        'i': ['M75 474 L236 491 L236 153 C236 73 263 39 320 39 L510 39', 'M236 658 L236 735'],
        # The tall l has the same optical correction at its baseline exit; its
        # broad terminal gives ``lr`` a usable rhythm without translating the
        # narrow stem inside its cell.
        'l': ['M232 735 L232 147 C232 72 259 39 322 39 L500 39'],
        't': ['M241 683 L241 163 C241 69 278 29 348 29 C387 29 428 41 457 65', 'M112 491 L449 491'],
        # Cap tops are narrower than baseline; these are redrawn polygon systems.
        'M': ['M104 0 L96 710 L120 710 L300 281 L427 710 L451 710 L507 0'],
        'W': ['M85 710 L161 38 C163 14 170 0 182 0 L201 0 L293 454 L421 0 L441 0 C452 0 460 14 462 37 L463 710'],
        'V': ['M111 710 L285 0 L319 0 L456 710'],
        'Y': ['M113 710 L296 348 L452 710', 'M296 348 L309 0'],
        'T': ['M76 671 L470 671', 'M275 671 L302 0'],
        '7': ['M119 671 L456 671 L260 0'],
        '/': ['M134 -122 L449 779'],
        # Shear translation at -157 is -66.87; endpoints keep the optical span.
        '_': ['M80 -157 L600 -157'],
    })
    assert all(c in D for c in out), 'Italic overrides must preserve coverage'
    return out
