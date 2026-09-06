# R5 packaging review — 2026-09-06

This records the packaging operation, not a new aesthetic revision.

## Input and preservation

Input: the supplied `Damonic-R5-Coherent-Flow.zip`, containing the original
`R5-outlines.json` (75,940 bytes).

Accepted JSON SHA-256:
`52bdb8e62d0c8c5c1d2cfd0a3e60dfa65d7363c605d64086f90879e9947c6765`.

The repository stores a lossless XZ copy. Generated source archives contain
normal uncompressed JSON. All 42 mapped glyphs were compiled and compared to
the previous study's proof builder: **42/42 compiled outlines equal**.
The `.notdef` marker and packaging metadata are new; the accepted drawing is not.

## Checks actually run before upload

- 16 unit tests passed with Python 3.13.5, FontTools 4.63.0, Pillow 12.3.0 and Brotli 1.2.0.
- 246 non-space glyph/size raster checks passed: 41 visible characters at 12, 14, 16, 18, 20 and 24 px, using FreeType 2.14.3.
- Mapped coverage is exactly 42, including space; all advances remain 600 units in a 1000-unit em.
- Rebuilding the same source produced identical TTF bytes with the pinned local toolchain.
- WOFF2 decoding retained cmap, metrics and all glyph geometry.
- All generated font tables were decompiled; family identity, license metadata, cell bounds and sidebearing consistency passed.
- The initial OS/2 version mismatch warning was corrected to version 4 and the checks were rerun cleanly.

The GitHub workflow repeats the included tests and packaging checks in its own
runner. This document does not assert a GitHub run succeeded; the Actions logs
and generated reports are the evidence for that separate execution.

## Boundaries

Only a Regular study with 42 characters is packaged. There is no attempt to fill
missing glyphs from the old production font. Distinct family naming prevents
intentional replacement of the installed `Damonic` family.

No new HarfBuzz shaping audit, OpenType Sanitizer run, independent design review,
manual hinting, native IDE/terminal test, broad script test or user reading trial
was performed for this packaging step. FreeType raster checks are not native
editor testing. Small-size appearance is still provisional.

Production source, existing styles, Nerd assets, the main branch and the
0.4.2-alpha release are not modified by the isolated R5 branch/release workflow.
