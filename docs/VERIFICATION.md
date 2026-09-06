# Verification — 0.4.1 Alpha

The local independent harness passes 86 checks across the four base fonts, four Nerd fonts and eight TTC faces. It verifies Latin coverage, metrics, shaping, stacked accents, symbol coverage and cell containment, family/style names, and matching TTC/TTF behavior. Commands: `python tests/verify.py` and `python tests/soft_dots.py` (both pass). The old exact-ASCII-baseline check is intentionally not applied to this optical revision; `optical-diff.json` records changed outlines and confirms unchanged advances and character coverage.

All eight TTF files pass OpenType Sanitizer 9.2.0 with no warnings. See `ots-report.json`.

Every Nerd face contains all 10,624 mapped codepoints from the pinned Nerd Fonts Symbols Mono 3.5.1 reference, including an upstream blank symbol. Eight colliding Powerline codepoints retain the original cell-aligned Damonic shapes. Each Nerd face maps 11,397 total codepoints; each base face maps 781. Complete coverage means this pinned repertoire, not every possible Unicode symbol.

FontBakery 1.1.0 universal profile on the four base faces reports 282 PASS, 18 WARN, 8 FAIL, 12 INFO and 152 SKIP. The eight FAIL results are four legacy Macintosh-name entries introduced by STAT name generation and four missing smart-dropout instruction programs. These do not prevent sanitizer acceptance; they remain production cleanup/hinting review items. Warnings include intentional two-cell optional ligatures, outline contour heuristics, soft hyphen, alternate caron review and style naming/profile details. The full report is included; this is not represented as a clean FontBakery production release.

The PNG proofs use Pillow/FreeType. They are not evidence of native Windows/macOS installation or editor/terminal behavior. Browser controls have source-level validation; an interactive browser was not available here. Native testing, diacritic/language review, experienced type-design review and developer beta remain required before 1.0.

The Nerd edition passes the FontBakery OpenType profile with {'(not finished)': 0, 'INFO': 4, 'PASS': 114, 'SKIP': 65, 'WARN': 5}.

Build-repeatability evidence for this version is recorded in `reproducibility.json`.
