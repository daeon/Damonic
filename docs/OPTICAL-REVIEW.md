# Damonic 0.4.1 optical review

Three Luna agents assessed narrow-letter rhythm, bowl/curve quality, and proof rendering. The integrated changes were reviewed using actual TTF rasterizations in Pillow/FreeType. This is a restrained alpha revision, not an expert certification or native-platform test.

## Changes and observations

- Italic and Bold Italic i: extend the baseline exit from x465 to x510 in the source drawing.
- Italic and Bold Italic l: extend the baseline exit from x416 to x500. Both changes lengthen the foot without translating the stem or changing the 600-unit advance.
- The longer feet occupy more of the white interval before following letters. At 16/20 px the difference is subtle; enlarged controls make the outline change clearer. The word samples retain their overall rhythm. This judgment remains subjective.
- Regular and Bold ASCII outlines are unchanged. The a/e/s/o/b/d/p/q review did not identify a high-confidence defect warranting a redraw in this pass.
- A separate ccmp fix suppresses native i/j dots before supported combining top marks. Below-only marks preserve dots. HarfBuzz normalization may first compose sequences into existing accented glyphs; tests distinguish this from the contextual substitution.

## Repeatable proof

```sh
python scripts/optical_proof.py --before ../damonic-before/dist --after dist --out docs/optical-proof.png --overview docs/optical-overview.png
```

Use an extracted previous release's dist directory for --before. The full matrix covers all four styles at 12/14/16/18/20 px in light and dark themes, spacing neighborhoods, whole words, ambiguity/punctuation and bowl controls. The overview includes enlarged 40 px samples. Rendering is repeatable within the same Pillow/FreeType environment.

## Remaining work

Dense arches and punctuation in Bold/Bold Italic at 12 px warrant native-renderer testing. The language-specific vertical caron forms for ď/ľ/ť need a dedicated redraw and language review; moving a generic caron upward is not an adequate final solution. Hinting review, native Windows/macOS/editor/terminal testing, and sustained use remain open. No numerical readability or aesthetic score is claimed.
