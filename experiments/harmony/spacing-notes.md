# Damonic harmony spacing study

This is a bounded pilot for the word **Damonic**, covering exactly `D a m o n i c` in Regular and Bold Italic. It is intended for visual judgment and is not a release font: spacing changes are not propagated to accented or related glyphs.

Run it from the repository root with:

```sh
python experiments/harmony/spacing.py
```

The script copies each baseline, transforms only those seven simple glyph outlines horizontally, updates their nominal left sidebearings, and keeps every advance at 600 units. It does not add or alter kerning or tracking. Existing contours, vertical coordinates, instructions, OpenType features, and all non-study glyphs are retained. The family name is `Damonic Harmony Study` so these pilot fonts do not collide with the production family.

Exact target changes (font units):

| Font | Glyph order | Target coordinate width | Target left sidebearing |
| --- | --- | --- | --- |
| Regular | D a m o n i c | 470, 455, 475, 465, 455, 455, 455 | 64, 66, 63, 66, 68, 68, 66 |
| Bold Italic | D a m o n i c | 500, 490, 495, 490, 490, 470, 490 | 45, 52, 48, 52, 52, 65, 52 |

Widths are measured from the source glyph coordinate extents and scaled to the listed targets; each outline is then translated to the listed left sidebearing. This is deliberately conservative horizontal proportion work: it retains the existing curve construction, while acknowledging that horizontal scaling changes stroke weight slightly (especially in the Bold Italic). The italic targets are intended to reduce late-word gaps; the visual comparison determines whether this helps.

These seven glyphs are a neighborhood pilot, not a complete spacing system. Accents, composites, punctuation, and other letters remain baseline values, so the study must not be shipped without a broader propagation pass.
