# Website

Static, no build step beyond one templating script. Deployed to GitHub Pages from this directory by `.github/workflows/pages.yml`.

- `index.src.html` + `style.css` + `fonts/`: homepage source. `python3 site/build_home.py` writes `index.html` (inlines the traced logo as an SVG symbol, stamps the og:image version).
- `benchmark/index.html`: the 3-tab dashboard, built with HorizonUI by `python3 site/build_data.py && python3 site/build.py` (self-contained). `vendor/` is HorizonUI for that page's dev copy.
- `logo.svg`, `favicon.svg`: the CRISP mark, traced from `art/logo.png`.
- `og-image.png` (1200×675): link-preview image for X, LinkedIn, iMessage, Slack. `github-banner.png`: README banner. `social-preview.png` (1280×640): upload in GitHub Settings → Social preview.
- Fonts: Outfit, Caveat, JetBrains Mono, self-hosted (OFL; licences in `third_party/fonts/`).

Preview: `cd web && python3 -m http.server 8765`.
