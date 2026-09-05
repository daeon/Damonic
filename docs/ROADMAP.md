# Roadmap to 1.0

## Alpha engineering
Rename and normalize metadata; fill declared Latin coverage; preserve current ASCII forms; position combining marks; integrate all symbols from a pinned Nerd Fonts release; produce reproducible builds, eight-face TTC, TTF fallbacks, web fonts and source distribution. Automated reports document the measured state.

## Design review
Have an experienced type designer review the entire alphabet, weight consistency, punctuation, diacritics and italic rhythm. Test `ri`, `in`, `rn`, `m`, `il`, `1lI`, `0Oo`, `minimum`, `printing`, `return`, dense code and terminal tables. Review at actual working sizes in light and dark themes. New Latin glyphs need the same attention as ASCII. Approve hinting only after comparing native small-size renders.

## Native application matrix
Test Windows (DirectWrite, Windows Terminal, VS Code), macOS (CoreText, Terminal/iTerm2, VS Code) and Linux (FreeType, a terminal and editor). Check installation and style linking, TTC support, font fallback, cursor position, selection, wrapping, multiline marks, box joins, Powerline separators and icon alignment at 100%, 125%, 150% and 200% where applicable. Test sizes 12–20 px. Record application versions and screenshots.

## Production gates
Review FontBakery findings and sanitizer results. Resolve critical correctness findings; document profile-specific exceptions. Confirm deterministic builds in CI and source/license completeness. Run a beta with 5–10 developers for one to two weeks, triage reports and repeat regression proofs. Publish the repository and tagged releases only after ownership and public release details are settled.

## Later scope
Variable weights need compatible masters and intermediate optical review. Greek/Cyrillic and other scripts require deliberate design and language expertise. Continuous italic interpolation is not implied by packaging static styles in a TTC.
