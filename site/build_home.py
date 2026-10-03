#!/usr/bin/env python3
"""web/index.src.html -> web/index.html: inline the traced logo once as an SVG <symbol> and stamp the og:image version."""
import hashlib, pathlib, re

WEB = pathlib.Path(__file__).resolve().parent.parent / "web"
logo = (WEB / "logo.svg").read_text()
viewbox = re.search(r'viewBox="([^"]+)"', logo).group(1)
mark = re.sub(r"\s+", " ", re.search(r"(<g .*</g>)", logo, re.S).group(1))
og_v = hashlib.sha1((WEB / "og-image.png").read_bytes()).hexdigest()[:8]

src = (WEB / "index.src.html").read_text()
out = src.replace("{{MARK_VIEWBOX}}", viewbox).replace("{{MARK}}", mark).replace("{{OG_V}}", og_v)
assert "{{" not in out
(WEB / "index.html").write_text(out)
print(f"web/index.html: {len(out) // 1024} KB, og v={og_v}")
