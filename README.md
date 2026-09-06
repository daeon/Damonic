# Damonic

Damonic is an open-source monospaced font for coding and terminal work. It combines humanist letterforms with a fixed-width grid, four styles, and an optional Nerd Fonts edition for terminal icons.

Fira Code, Source Code Pro, and Consolas inspired the design brief. Damonic uses original letter outlines rather than outlines taken from those fonts.

**Current version: 0.4.2 Alpha.** The font is available to try, but spacing, rendering, and application compatibility are still being refined.

[Downloads](https://github.com/daeon/Damonic/releases) · [Letterform specimen](docs/core-proof.png) · [Contributing](CONTRIBUTING.md)

## Why try it?

- **Consistent terminal alignment.** Letters use a fixed cell width, with box-drawing, block, Braille, and Powerline characters included. The Nerd edition fits its icons to single cells.
- **Four coordinated styles.** Regular, Italic, Bold, and Bold Italic are available in both the base and Nerd families.
- **Optional character features.** Keep ordinary operators or enable a small set of ligatures. Choose a dotted zero or a simpler lowercase `l` if you prefer them.
- **One-file installation.** A font collection contains both families and all four styles. Individual font files are also available.
- **Editable source.** The project includes the outline generator and build scripts, so contributors can inspect, modify, and rebuild the font.

Damonic may suit you if you like the humanist character of its inspirations and want to try an evolving alternative. It does not yet offer the maturity, script coverage, or extensive ligature repertoire of established coding fonts.

## Choose an edition

| Family | Contents |
| --- | --- |
| **Damonic** | Letters, numbers, punctuation, and terminal drawing characters. |
| **Damonic Nerd Font Mono** | The same typeface plus all 10,624 mapped symbol codepoints from the pinned Nerd Fonts Symbols Mono 3.5.1 release. |

The Nerd edition is useful for icon-based shell prompts and editor interfaces. Its coverage refers to that specific upstream symbol release, not all Unicode symbols.

Both editions include printable ASCII, Latin-1 Supplement, Latin Extended-A, and combining accents. Greek and Cyrillic are not currently supported.

## Install

1. Download and extract the font ZIP from [Releases](https://github.com/daeon/Damonic/releases).
2. Install `dist/Damonic.ttc` using your operating system's font manager.
3. Restart your editor or terminal and select **Damonic** or **Damonic Nerd Font Mono**.

The TTC contains eight faces: four styles in each of the two families. If your application cannot use a TTC, install the desired individual TTF files instead. Avoid installing duplicate copies from both formats.

This is a collection of static styles, not a variable font. WOFF2 files are included for web use. Open the included `Damonic-Preview.html` to try the embedded fonts before installing.

## Optional features

Enable these through your application's OpenType feature settings, where supported:

| Feature | Effect |
| --- | --- |
| `dlig` | Ligatures for `->`, `<-`, `=>`, `==`, `!=`, `<=`, and `>=`. Each retains two cells. Off by default. |
| `ss01` | Dotted zero instead of the default slashed zero. |
| `ss02` | Simple lowercase `l`. |

## Current limitations

Damonic is still an alpha. Native Windows, macOS, and Linux rendering, editor and terminal behavior, and extended everyday use need further testing. Manual hinting has not been completed, and some accent shapes and combinations need more visual review. There is no claim that Damonic improves reading speed or reduces fatigue.

Try it at your normal coding size with your own code and prompt. If something looks uneven, report the full word or line as well as the individual characters, along with your font version, style, application, operating system, size, display scaling, and a screenshot.

See the [roadmap](docs/ROADMAP.md), [verification notes](docs/VERIFICATION.md), and [optical review](docs/OPTICAL-REVIEW.md) for outstanding work.

## Build and contribute

Use Python 3.11 or newer:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python release.py build
python tests/verify.py
python tests/soft_dots.py
python release.py package
```

On Windows, activate with `.venv\Scripts\activate`. A first build from a Git checkout downloads and verifies the pinned Nerd Fonts assets; the source archive includes them.

The Python outline generator is the canonical source. Generated UFO files are interchange snapshots; editing them does not change the next build. See [CONTRIBUTING.md](CONTRIBUTING.md) for drawing constraints and review requirements.

## License

Damonic's original font software is licensed under the [SIL Open Font License 1.1](OFL.txt). No Reserved Font Name is declared for Damonic. The Nerd Fonts symbols retain their upstream notices in [licenses](licenses/) and the vendored assets.
