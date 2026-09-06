# Damonic launch kit

## Core line

**Make room for the code.**

Damonic is a free, open source humanist monospace for coding and terminal work. Four styles, a complete Nerd Fonts Mono edition, and one eight-face collection.

Damonic is an alpha release for people who want to try it, test it in real workflows and help shape what comes next. It is not a paid standalone product or a finished 1.0 release.

## GitHub launch description

> **Make room for the code with Damonic 0.4.0 Alpha.**
>
> Damonic is a free, open source humanist monospace made for coding and terminal work. It ships Regular, Italic, Bold and Bold Italic in a single eight-face TTC, plus individual TTF and WOFF2 files. Enable optional `dlig` arrows and comparisons, `ss01` dotted zero or `ss02` simple lowercase `l` when you want more distinction at a glance.
>
> The Nerd Font Mono edition includes all 10,624 mapped codepoints from the pinned Nerd Fonts Symbols Mono 3.5.1 repertoire. This is an engineering alpha: install it, use it in your editor or terminal, and report what needs attention on the road to 1.0.

## Social posts

**Post 1 — short launch post**

Make room for the code. Meet Damonic: a free, open-source coding font with four styles and a complete Nerd Fonts Mono edition. Try the alpha: https://github.com/daeon/Damonic/releases/tag/v0.4.0-alpha

**Post 2**

New font, early days. Damonic is an open source humanist monospace with Regular, Italic, Bold and Bold Italic, an eight-face TTC, TTF/WOFF2 fallbacks and optional Nerd Font symbols. It is an alpha, so real editor and terminal feedback matters. https://github.com/daeon/Damonic/releases/tag/v0.4.0-alpha

## Developer-community launch post

### Damonic 0.4.0 Alpha: a humanist monospace for code

I’m sharing Damonic, a free and open source coding font built for editors and terminals. The design is humanist and monospace, with a compact 600-unit cell and four static styles: Regular, Italic, Bold and Bold Italic.

The alpha includes a few deliberate controls for code legibility: optional `dlig` for `->`, `<-`, `=>`, `==`, `!=`, `<=` and `>=`; `ss01` dotted zero; and `ss02` simple lowercase `l`. Those features are off or unchanged by default, so you can choose the distinctions that fit your setup.

If you use icons in a terminal or prompt, the Nerd Font Mono family includes the full mapped repertoire from pinned Nerd Fonts Symbols Mono 3.5.1: 10,624 mapped codepoints in each Nerd face. The release includes an eight-face TTC, individual TTF files for applications that cannot use TTC, and WOFF2 for the web.

This is a working alpha. Native installation and editor/terminal behavior across operating systems, high-DPI rendering, broader diacritic review, type-design review and a developer beta are still part of the path to 1.0. Please share your OS, application, font family/style, size, display scaling and a small screenshot when reporting an issue.

Download the alpha, try it in your normal workflow, and open an issue with concrete examples. The original font software is licensed under SIL OFL 1.1; Nerd Font symbols retain their upstream notices and licenses.

## Five features to lead with

- **Humanist monospace proportions:** a 600-unit cell on a 1000-unit em, shaped for code and terminal layouts.
- **Four static styles:** Regular, Italic, Bold and Bold Italic, with weights 400 and 700 and a 9-degree italic angle.
- **Optional code distinctions:** `dlig` arrows/comparisons, `ss01` dotted zero and `ss02` simple lowercase `l`.
- **Nerd Font Mono edition:** all 10,624 mapped codepoints from pinned Nerd Fonts Symbols Mono 3.5.1 in each Nerd face.
- **Flexible packaging:** an eight-face TTC, individual TTF compatibility files and WOFF2 web fonts.

## FAQ

### Is Damonic free?

Yes. Damonic is free and open source. It is distributed under SIL Open Font License 1.1 (`OFL.txt`).

### Is this a finished release?

No. 0.4.0 is an alpha. It is ready for hands-on evaluation, while native platform testing, broader review and a developer beta remain before 1.0.

### What does the TTC contain?

`dist/Damonic.ttc` contains eight discrete faces: four Damonic styles and four Damonic Nerd Font Mono styles. A TTC is a collection of styles, not a variable font with continuous weight or italic sliders.

### What is in the Nerd Font edition?

Each Nerd face contains the complete mapped repertoire of the pinned Nerd Fonts Symbols Mono 3.5.1 release: 10,624 mapped codepoints. “Complete” refers to that pinned repertoire, not every possible Unicode symbol.

### What are the tradeoffs of the alpha?

Some FontBakery findings and intentional exceptions remain documented, and complex accent sequences still need visual review. Greek and Cyrillic are not declared supported. No manual hinting or native platform behavior is claimed yet.

### Can I use it in a product or redistribute it?

The original font software is covered by SIL OFL 1.1; read `OFL.txt` for the license terms. Nerd Font symbols retain their upstream copyright and license notices in `licenses/`; redistribute those notices with a patched font.

## Marketing claims rules

### Approved claims

- “Free and open source,” “SIL OFL 1.1,” and “0.4.0 Alpha.”
- “Humanist monospace for coding and terminal work.”
- “Four static styles: Regular, Italic, Bold and Bold Italic.”
- “Optional `dlig` ligatures, dotted zero (`ss01`) and simple lowercase `l` (`ss02`).”
- “Eight-face TTC, individual TTF files and WOFF2 files.”
- “10,624 mapped codepoints from the pinned Nerd Fonts Symbols Mono 3.5.1 repertoire.”
- “The local verification harness passes 90 checks,” when the claim is paired with the verification document and described as local evidence.

### Do not claim

- Proven lower fatigue, better productivity, improved readability or better performance.
- Native Windows, macOS or Linux certification, universal editor/terminal compatibility or high-DPI validation.
- A polished, complete or production-ready 1.0 font.
- Support for every Unicode symbol, Greek or Cyrillic coverage, variable font axes or manual hinting.
- That the base FontBakery report is clean; documented warnings and failures remain.
- That the font is a paid standalone product. Keep the free, open source alpha status explicit.

When in doubt, describe what ships and what was measured; link readers to `README.md` and `docs/VERIFICATION.md` for scope and limitations.
