# M selected — 0.4.2 refinement

Damon selected candidate M from the anonymous harmony comparison. M was the unchanged 0.4.1 baseline, also shown as the R duplicate. This selection supersedes the previous proposal for a broader redraw. K and P remain historical studies on the experiment branch and are not adopted.

## What changes

Only the Regular m drawing changes: its three stems use 78% of the nominal 84-unit stroke instead of 74%, increasing their nominal width from 62.16 to 65.52 units. The shoulder curves, inner crown heights, stem centers and 600-unit character advance stay the same. The resulting outer ink extends about two units farther on each side. This is a small optical refinement, not a claim to have resolved every spacing concern.

Bold stays at 74% to preserve its tighter counters. Italic and Bold Italic use their existing independent constructions unchanged. The i/r outlines and positions remain exactly those of M. The font's feature and symbol repertoires are retained.

The root reviewed 74/78/82% stem probes at 12/16/20/28 px and enlarged wordmarks. The 78% Regular probe was chosen as a restrained increase in apparent stem weight beside n. The larger increase was not adopted; neither increase was applied automatically to Bold or italic styles. A Luna review supported only a small Regular test, explicitly noting that total m ink and its two arches already affect apparent weight. This is a subjective design judgment, not an independently proven readability gain.

## Reproduce the exploratory proof

```sh
python docs/m-selected/probe.py
```

The included M-Regular.ttf and M-Bold.ttf are frozen 0.4.1 inputs. The additional M78/M82 outputs are exploratory render inputs, not the shipped fonts. The selected production change is Regular only. The build core accepts an explicit m_ratio solely to reproduce the alternate drawings from the same constructor.

These proofs use Pillow/FreeType. Native Windows/macOS/terminal use and further optical review remain alpha limitations. The original font license is ../../OFL.txt.
