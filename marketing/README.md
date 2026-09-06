# Damonic marketing kit

**Make room for the code.**

- `Damonic-Landing.html`: standalone responsive landing page with all four base fonts embedded and an editable specimen. Open locally; download links point to the public release. This file is ready to host, but has not been deployed as a separate website.
- `assets/damonic-hero`: 1280 × 640 repository banner / link-preview graphic.
- `assets/damonic-social`: 1080 × 1080 square launch graphic.
- `assets/damonic-specimen`: 1080 × 1440 four-style specimen poster.
- `LAUNCH-KIT.md`: launch posts, feature copy, FAQ and claim boundaries. Drafts only; no social posts have been sent.
- `BRAND.md`: positioning, palette and asset rules.

Graphics come in PNG and SVG. SVG lettering is outlined from the actual Damonic font, so it renders correctly without installing the font. The landing page uses the actual WOFF2 fonts.

To regenerate after a font change, run `python release.py build`, then `python marketing/build_materials.py`. Install CairoSVG 2.8.2 for PNG export; SVG and HTML need only the normal project dependencies.

Use the square graphic with the short post, the hero at the top of the repository, and the specimen poster for a fuller introduction to the family. Keep the alpha label visible. Read `../OFL.txt` for the original font license.
