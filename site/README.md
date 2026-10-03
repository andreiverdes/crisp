# CRISP benchmark page

Three tabs: CRISP vs baseline, CRISP vs ASD-STE100, Anthropic vs OpenAI. Dashboard first, verbatim answers and judge notes underneath.

## Open it

`web/benchmark/index.html` is self-contained (data, HorizonUI, React inlined). Works from `file://` and from GitHub Pages.

## Publish to GitHub Pages

1. Push to `main`. `.github/workflows/pages.yml` uploads `web/` on every change.
2. Repo → Settings → Pages → Source: **GitHub Actions** (one-time).

Or skip Actions: Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/docs`.

## Rebuild

```
python3 bench/headtohead.py   # direct pairings: Anthropic vs OpenAI, STE vs CRISP (needs omp gateway)
python3 site/build_data.py    # shared/results + headtohead.json -> site/data.json
python3 site/build.py         # index.html + data.json + vendor -> site/crisp.html
# build.py writes web/benchmark/index.html directly
```

`index.html` + `data.json` + `vendor/` are the dev layout; `index.html` alone needs a local server because it fetches `data.json`.

HorizonUI is vendored from `claude-design/horizon-ui/ds-bundle` (the browser-global build). The npm package `@horizonloop/ui` is an ESM React library; switching to it would mean a Vite build step for no change in output, so the page stays a single file.

## Hero banner

`python3 site/hero.py` regenerates `web/hero-{dark,light}.svg` from `data.json`. Self-contained SVG (system fonts, no external refs) so GitHub renders it in the README; the `<picture>` block in `README.md` swaps on the viewer's color scheme.

## Twitter card

`python3 site/twitter.py` writes `web/twitter-card.svg` (1200×675). Rasterize at 2x in a headless browser to `web/twitter-card.png` (2400×1350, under 1 MB; X accepts up to 5 MB). Attach the PNG to the tweet, or point `twitter:image` at the raw GitHub URL.
