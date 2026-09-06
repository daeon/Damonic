# Damonic harmony experiment — Thoughtloop decision record

**Decision: do not promote either pilot to a font release.** The studies are real, inspectable font builds, but neither established a reliable improvement in coding-size rhythm. The next route is a broader construction experiment, not another pair-spacing patch or a claim that the baseline is already harmonious.

## What was built

| Label | Study | Constraint |
|---|---|---|
| K | Construction | Redraw D/a/m/o/n/i/c; retain actual horizontal ink extents within one unit. |
| M | Baseline 0.4.1 | Unchanged. |
| P | Horizontal proportions and spacing | Fit the seven existing outlines to revised widths and positions. |
| R | Duplicate baseline | Identical font/render control. |

Regular and Bold Italic were tested. Every glyph retains its advance; ordinary characters stay 600 units. Accents and non-pilot letters remain baseline drawings. These are seven-letter studies, not complete fonts for installation. Open Damonic-Harmony-Experiment.html to compare actual embedded fonts and enter your own text.

## Evidence and limits

- **PASS — experiment scope:** the four pilots change only the seven target glyph outlines, along with study naming. Character maps and advances are preserved.
- **PASS — exported font validity:** all four pilot TTFs pass OpenType Sanitizer. Bounds/sidebearing and HarfBuzz checks pass; see verification.json and sanitizer.json.
- **PASS — a real construction difference exists:** the revised upright i has a flat entry and baseline foot, and a/m/n curve construction changes. The baseline and study are not identical fonts.
- **UNKNOWN — improved coding-size harmony:** two fresh Luna reviewers, shown anonymous PNGs without source/label mappings, reported no reliable winner at 12/16/20 px. They also did not uniquely identify the duplicate pair; their feedback therefore establishes limited perceptual separation, not expert validation of the design.
- **UNKNOWN — native-platform readability:** only Pillow/FreeType rendering was available. The HTML permits evaluation in the user's browser, but no native Windows/macOS editor or terminal test is claimed.
- **UNKNOWN — full-family coherence:** only seven letters and two styles were changed. Unmodified letters in code samples are useful transfer controls, not proof that related glyphs were redesigned.

The root's visible assessment: K simplifies the upright i and changes the a/m/n texture; P's width changes are modest. Neither result yet resolves the user's broader concern convincingly enough to adopt. The experiment does not establish that spacing is irrelevant or that mixed outline methods are inherently defective.

## Review record

Reviewer A: all candidates effectively tied; no dependable coding-size preference. Repeated narrow stems and dense Bold Italic text at 12 px remained a concern across the set.

Reviewer B: all candidates effectively tied on the transfer sheet; no dependable candidate-specific gain or regression. Candidate choice remained unknown.

These are independent review turns using the same model family, not independent human type-design expertise. Their agreement cannot substitute for an observable improvement. No beauty score or readability-speed claim is made.

The first construction draft was rejected before anonymous review: it used the wrong Regular weight and a malformed i. The root corrected the draft, m weight, glyph fitting/sidebearings, and naming before regenerating the final proofs. rejected-initial.png retains the failed implementation for audit; it is not the final candidate.

## What changes in the next design decision

Do not combine the two pilots merely because both were built. First establish a visibly stronger n/o/H/O construction direction, including D and m alongside the controls. Then expand to h/u/a/c/e/b/d/p/q/i/l/r/t/f so the proposed system is evaluated across its related letters. Keep the fixed grid; evaluate stem/counter balance and curve behavior together. Retain baseline comparison and fresh words, and require a clear, location-specific improvement before propagation to all styles or Nerd editions.

The current hypothesis is that the accumulated glyph-specific construction decisions need a stronger shared direction. That remains a hypothesis; these modest pilots did not settle it. The source implementation is unchanged, and no production version is advanced by this experiment.

## Reproduce

From the repository root, with the project dependencies installed and DejaVu Sans available for proof labels:

```sh
python experiments/harmony/spacing.py
python experiments/harmony/construction.py
python experiments/harmony/verify.py
python experiments/harmony/proof.py
```

The folder includes the exact 0.4.1 baseline TTFs used by the scripts. Original font licensing is in ../../OFL.txt. The construction builder imports the root build helpers; run from this repository checkout rather than copying that script alone. Review construction-notes.md and spacing-notes.md for the experimental confounds: scaling affects stroke thickness, and internal contour changes affect perceived spacing even when outer bounds match.
