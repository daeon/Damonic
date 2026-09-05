# Contributing

Edit canonical Python sources, build locally, and attach before/after proofs at 12, 14, 16 and 20 px. Preserve the 600-unit grid, optional two-cell ligatures and zero-width marks. Never fix a monospaced pair with proportional kerning. Review both neighboring sides of a changed glyph and all four styles.

Do not copy outlines from inspiration fonts or other projects. Record the origin and license of any new symbol source. Keep Nerd Fonts assets pinned with hashes and complete notices.

Run `python release.py build` and `python tests/verify.py` before proposing changes. Include rendered evidence, scope, why the change is needed and remaining limitations. UFO snapshots are generated for interchange; transfer intended edits back to canonical sources.

Use a focused issue with version, family/style, OS/application, size/scaling, sample text, actual result, expected result and screenshot. Changes to a shared shape must include a word-level proof, not just one favorable pair.
