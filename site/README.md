# Site build

Everything under `web/` is static and deployed by `.github/workflows/pages.yml`.

```
python3 bench/headtohead.py   # optional: direct pairings (Anthropic vs OpenAI, STE vs CRISP); needs the omp gateway
python3 site/build_data.py    # shared/results + headtohead.json -> site/data.json
python3 site/build.py         # web/benchmark/index.src.html + data.json -> web/benchmark/index.html
python3 site/build_home.py    # web/index.src.html -> web/index.html
python3 site/hero.py          # SKILL.md banner SVGs
```

Both pages share `web/style.css`, `web/fonts/`, and the traced logo (`web/logo.svg`, inlined as an SVG symbol by the build scripts). No framework, no npm.

## Social image

`web/og-image.png` (1200×675) is resized from `resources/twitter.png`. The build scripts stamp its content hash into the og:image URL, so link unfurlers re-fetch when it changes.
