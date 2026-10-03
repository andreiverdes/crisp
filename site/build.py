#!/usr/bin/env python3
"""Inline data.json + vendor CSS/JS into one self-contained crisp.html that opens from file://."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
html = (HERE / "index.html").read_text()
data = json.dumps(json.load(open(HERE / "data.json")), separators=(",", ":")).replace("</", "<\\/")
css = (HERE / "vendor" / "horizon.css").read_text()
react = (HERE / "vendor" / "react.js").read_text()
horizon = (HERE / "vendor" / "horizon.js").read_text()
for blob in (react, horizon):
    assert "</script" not in blob

html = html.replace('<link rel="stylesheet" href="vendor/horizon.css">', f"<style>\n{css}\n</style>")
html = html.replace('<script src="vendor/react.js"></script>', f'<script id="crisp-data" type="application/json">{data}</script>\n<script>\n{react}\n</script>')
html = html.replace('<script src="vendor/horizon.js"></script>', f"<script>\n{horizon}\n</script>")
assert "vendor/" not in html and "crisp-data" in html
out = HERE.parent / "web" / "benchmark" / "index.html"
out.write_text(html)
print(f"{out}: {out.stat().st_size // 1024} KB")
