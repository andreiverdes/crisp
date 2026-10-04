#!/usr/bin/env python3
"""web/benchmark/index.src.html + site/data.json -> web/benchmark/index.html (data inlined, logo symbol, og version)."""
import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
logo = (WEB / "logo.svg").read_text()
viewbox = re.search(r'viewBox="([^"]+)"', logo).group(1)
mark = re.sub(r"\s+", " ", re.search(r"(<g .*</g>)", logo, re.S).group(1))
og_v = hashlib.sha1((WEB / "og-image.png").read_bytes()).hexdigest()[:8]
css_v = hashlib.sha1((WEB / "style.css").read_bytes()).hexdigest()[:8]
data = json.dumps(json.load(open(ROOT / "site" / "data.json")), separators=(",", ":")).replace("</", "<\\/")

src = (WEB / "benchmark" / "index.src.html").read_text()
out = src.replace("{{MARK_VIEWBOX}}", viewbox).replace("{{MARK}}", mark).replace("{{OG_V}}", og_v).replace("{{CSS_V}}", css_v).replace("{{DATA}}", data)
assert "{{" not in out.replace(data, "")
dst = WEB / "benchmark" / "index.html"
dst.write_text(out)
print(f"{dst.relative_to(ROOT)}: {len(out) // 1024} KB")
