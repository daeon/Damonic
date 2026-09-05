# Damonic release plan

Target: 0.4.0 Alpha, four base styles plus four complete Nerd Font Mono styles.

## Source atlas and component briefs
- build.py owns outlines, composition, OpenType features and metadata; beautify.py and italic_design.py supply current optical designs. Preserve existing ASCII outlines.
- terminal.py owns cell-aligned box, block, Braille and Powerline geometry.
- New scripts/patch_nerd.py owns pinned upstream icon acquisition and integration; licenses/ holds upstream notices.
- New tests/ verifies output contracts; release.py owns deterministic packaging and standalone preview.

## Contract and impact map
Python sources -> base TTF (600-unit advances, zero-width marks, 1200-unit optional ligatures) -> icon merge -> patched TTF -> QA -> preview and release archives.
Renaming affects internal names, filenames, docs and installation; icon merge affects cmap, glyph order, metrics and license notices; mark changes affect GPOS and accent extents; none should alter ASCII contours.

## Evidence ledger
- Prior baseline audit: fsType=4 and vendor ???? need correction; current names Bearing Mono.
- Baseline: 745 mapped characters, partial Latin coverage, mark but no mkmk.
- Baseline standalone build works; prior proof/package tools depend on old sibling directories. Replace release orchestration.
- Official Nerd Fonts release page identifies v3.5.1 (confirmed by live GitHub API; cached web page was older). Pin source bytes and verify expected symbol cmap; do not promise future symbols.

## Execution
1. Review gates and preserve baseline.
2. Rename core metadata; complete Latin1/ExtendedA and punctuation; improve marks.
3. Integrate complete pinned Nerd Fonts Mono symbols with collision manifest and licenses.
4. Build QA, repeat-build hashes, standalone preview, contribution docs and CI.
5. Save installable and source archives.

## Verification and rollback
Check every style: names, style links, fsType, glyph bounds, cmap coverage, shaping, alternates, ligature advances, symbols, preserved ASCII outlines. Rebuild twice and compare hashes. Inspect rendered coding and icon proofs. Baseline directory is read-only and rollback is installation of previous version.

## Release gates
Alpha is local and reversible; no public publishing or 1.0 claim. Native Windows/macOS/Linux installation, terminal cursor/selection/wrapping, hinting comparison, experienced type review and developer beta remain required before 1.0. Variable fonts and additional writing systems are later scope.

User addition: ship Damonic.ttc containing all eight faces, plus individual TTF compatibility files in one ZIP. TTC is a collection, not continuous variable axes.

Independent skeptic review passed with explicit coverage, metadata, shaping, symbol provenance, repeatability and TTC checks.
