# Damonic R5 Study — Coherent Flow

Experimental **Regular** package of the R5 drawing selected in the design conversation. This is a separate family named **Damonic R5 Study**. It does not replace Damonic 0.4.2, its four styles, or its Nerd edition.

[Build status](https://github.com/daeon/Damonic/actions?query=branch%3Ar5-coherent-flow) · [Releases](https://github.com/daeon/Damonic/releases) · [Packaging review](PACKAGING-REVIEW.md)

A successful study build publishes the isolated prerelease tag `r5-study-0.5.0-alpha.5`. The existing production release is not replaced.

R5 keeps the roundness, stronger main stems and wider `i` developed in R2–R4. Its last aesthetic pass refined `a`, `e`, `g` and `s`. Packaging does not redraw the letters or fill missing characters from a different font.

## Scope — read before installing

Exactly **42 mapped characters**, including space:

```text
 !0123456789DIOabcdefghijklmnopqrstuvwxyz|
```

There are 26 lowercase letters, three uppercase letters (`D I O`), ten digits, `!`, `|`, and space. This is **not complete ASCII** and is not ready to replace a daily coding font. Unsupported text can trigger application fallback. There are no ligatures, Nerd/Powerline symbols, Bold, Italic, variable axes, or hinting. Small-size rendering and native editor/terminal behavior remain unapproved.

## Release contents

The GitHub build produces `DamonicR5Study-Regular.ttf`, its WOFF2 equivalent, a source archive, `Specimen.svg`, `BUILD-REPORT.json`, `QA-REPORT.json`, the OFL license, and checksums. The family has a 1000-unit em and a 600-unit advance for every mapped character. No kerning is added.

Install only the TTF through your operating system's font manager, restart the application, and choose **Damonic R5 Study**. WOFF2 is for web use. This study can coexist with the existing **Damonic** family. Installation and native rendering are not tested by the build.

## Rebuild

Use Python 3.13 in a virtual environment, matching the CI build:

```sh
python -m pip install -r studies/r5/requirements.txt
python -m unittest discover -s studies/r5 -p 'test_package.py' -v
python studies/r5/build.py --out .build/r5 --package
```

Use an empty output directory. From the extracted source archive, omit `studies/r5/` from these commands. The archive includes an ordinary, editable `R5-outlines.json` and its OFL license.

In the repository, `R5-outlines.json.xz` is the lossless compressed original source snapshot, not a compiled font. After installing the build dependencies, extract it without installing the study into your operating system:

```sh
python studies/r5/build.py --extract-source R5-editable.json
```

Edit that JSON and rebuild with `--source R5-editable.json`; the report then records whether its checksum matches the accepted R5. Default builds fail on source corruption. SHA-256 of the accepted uncompressed source: `52bdb8e62d0c8c5c1d2cfd0a3e60dfa65d7363c605d64086f90879e9947c6765`.

## Verification and limits

The build checks exact coverage, metrics, family identity, bounds, deterministic TTF output, table decoding, and a WOFF2 geometry round-trip. The unit suite also checks unsupported-character absence, source preservation and actual FreeType rasterization. These are engineering checks, not proof of readability or aesthetic superiority. The source snapshot's historical status text describes its earlier design-study delivery; this README describes the new packaging step.

Native IDE/terminal interaction, manual hinting, independent review, full family coverage, and broad language support remain untested or absent. No production files or upstream icon assets are merged into this study.

## License

Original Damonic font software is covered by the repository's SIL Open Font License 1.1 (`OFL.txt`), copied unchanged into both packages. No additional font or icon assets are included.
