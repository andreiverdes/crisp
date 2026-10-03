#!/usr/bin/env python3
"""Render web/twitter-card.svg (1200x675, dark) for Twitter/X summary_large_image. Numbers from site/data.json.
Rasterize with: python3 site/twitter.py && (browser) -> web/twitter-card.png at 2x."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
d = json.load(open(os.path.join(HERE, "data.json")))
s = d["lanes"][0]["crisp"]
ste = d["ste"]; ts = sum(r["steTok"] for r in ste); tc = sum(r["crispTok"] for r in ste)

W, H = 1200, 675
bg, panel, line = "#0d1117", "#161b22", "#30363d"
fg, muted, subtle = "#e6edf3", "#9da7b3", "#6e7681"
accent, green, red = "#58a6ff", "#3fb950", "#f85149"
mono = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
sans = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

before = ["Great question! There are a few", "different ways you could approach", "this, but generally speaking, the", "best option in most cases would", "probably be to look into using a", "connection pool. I hope this helps,", "let me know if you have any questions!"]
after = ["Use a connection pool. Opening a", "connection per request exhausts the", "database's connection limit under", "load."]
nb, na = len(" ".join(before).split()), len(" ".join(after).split())

def lines(xs, x, y, color, strike=False, lh=20):
    out = []
    for i, t in enumerate(xs):
        yy = y + i * lh
        out.append(f'<text x="{x}" y="{yy}" font-family="{mono}" font-size="13" fill="{color}">{esc(t)}</text>')
        if strike:
            out.append(f'<line x1="{x}" y1="{yy-4}" x2="{x+len(t)*7.85}" y2="{yy-4}" stroke="{color}" stroke-width="1" opacity=".55"/>')
    return "\n".join(out)

stats = [(f"−{s['tokPct']:.0f}%", "tokens vs baseline", green),
         (f"{s['wins']}/30", "blind pairings won", accent),
         (f"{s['factsKept']:.0f}%", "facts kept", fg),
         (f"−{100*(1-tc/ts):.0f}%", "tokens vs ASD-STE100", green)]
stat_svg = "".join(
    f'<text x="{72+i*150}" y="540" font-family="{sans}" font-size="34" font-weight="700" letter-spacing="-0.8" fill="{col}">{esc(v)}</text>'
    f'<text x="{72+i*150}" y="564" font-family="{sans}" font-size="12" fill="{muted}">{esc(label)}</text>'
    for i, (v, label, col) in enumerate(stats))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="CRISP: say the useful thing once, as clearly as possible, then stop.">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{accent}" stop-opacity=".18"/><stop offset=".6" stop-color="{accent}" stop-opacity="0"/></linearGradient>
    <radialGradient id="glow" cx="0.85" cy="0.15" r="0.6"><stop offset="0" stop-color="{green}" stop-opacity=".10"/><stop offset="1" stop-color="{green}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="{bg}"/>
  <rect width="{W}" height="{H}" fill="url(#g)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>

  <text x="72" y="128" font-family="{sans}" font-size="84" font-weight="800" letter-spacing="-3.5" fill="{fg}">CRISP</text>
  <text x="72" y="166" font-family="{sans}" font-size="15" letter-spacing="2.6" fill="{muted}">CONCISE · RELEVANT · INTUITIVE · SIMPLE · PROTOCOL</text>

  <text x="72" y="248" font-family="{sans}" font-size="34" font-weight="650" letter-spacing="-1" fill="{fg}">Say the useful thing once,</text>
  <text x="72" y="290" font-family="{sans}" font-size="34" font-weight="650" letter-spacing="-1" fill="{fg}">as clearly as possible, then stop.</text>
  <text x="72" y="336" font-family="{sans}" font-size="17" fill="{muted}">A writing protocol for humans and LLMs. One engineer talking to another.</text>
  <text x="72" y="362" font-family="{sans}" font-size="17" fill="{muted}">System prompt, slash command, or a verb: “crispify this.”</text>

  <line x1="72" y1="490" x2="660" y2="490" stroke="{line}"/>
  {stat_svg}

  <rect x="708" y="140" width="420" height="400" rx="14" fill="{panel}" stroke="{line}"/>
  <text x="732" y="186" font-family="{sans}" font-size="11.5" font-weight="700" letter-spacing="1.6" fill="{red}">BEFORE · {nb} WORDS</text>
  {lines(before, 732, 212, subtle, strike=True)}
  <line x1="732" y1="364" x2="1104" y2="346" stroke="{line}"/>
  <text x="732" y="396" font-family="{sans}" font-size="11.5" font-weight="700" letter-spacing="1.6" fill="{green}">CRISP · {na} WORDS</text>
  {lines(after, 732, 422, fg)}
  <text x="1104" y="518" text-anchor="end" font-family="{mono}" font-size="12" fill="{muted}">−{100*(1-na/nb):.0f}% words · nothing lost</text>

  <text x="72" y="632" font-family="{sans}" font-size="13" fill="{subtle}">github.com/andreiverdes/crisp</text>
  <text x="{W-72}" y="632" text-anchor="end" font-family="{sans}" font-size="12" fill="{subtle}">Claude Sonnet 5.5 · 10 prompts × 3 samples · blind-judged</text>
</svg>
'''
p = os.path.join(ROOT, "web", "twitter-card.svg")
open(p, "w").write(svg)
print(p, len(svg), "bytes")
