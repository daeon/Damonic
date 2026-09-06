# Construction study — final candidate K

A seven-glyph experiment on D/a/m/o/n/i/c in Regular and Bold Italic. This is an experimental font, not a release: related letters and accents remain baseline drawings.

The study uses related centerline drawings for the lowercase curves and shoulders. It does not mechanically reuse one curve for every shape. Regular uses an 84-unit expansion and Bold Italic 108 units, with m reduced to 78% to accommodate two counters. Fitting can alter the resulting horizontal stem thickness. The upright i uses a flat entry and baseline foot with one separated dot; the italic i retains a curved exit. The a upper terminal and m/n shoulder geometry also change.

After drawing, each glyph is fitted to its baseline actual ink x bounds, measured with BoundsPen. TrueType off-curve control points can extend beyond those ink bounds; hmtx left sidebearings are set from the resulting glyph control bounds as required for raster placement. Independent checks allow at most one unit of ink-bound difference after rounding. All advances stay 600 units.

This holds outer horizontal extents, not every optical interval: changing internal contours changes perceived space. It therefore cannot perfectly isolate construction from optical spacing.

The initial draft was rejected for an incorrect Regular weight and malformed i. The root corrected those implementation defects and reviewed the regenerated raster before the anonymous assessment. rejected-initial.png records that rejected draft; it is not the candidate assessed by reviewers.

Run from the repository root:

```sh
python experiments/harmony/construction.py
```

The script copies the supplied baseline TTFs and changes only the seven target glyphs plus study naming. Its family is Damonic Harmony Construction. It does not call the production build entry point.
