#!/usr/bin/env python3
"""Render web/hero.svg (and a light variant) for the README. Numbers come from site/data.json."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
d = json.load(open(os.path.join(HERE, "data.json")))
s = d["lanes"][0]["crisp"]                      # Sonnet lane, shipped prompt
ste = d["ste"]; tb = sum(r["baseTok"] for r in ste); ts = sum(r["steTok"] for r in ste); tc = sum(r["crispTok"] for r in ste)
h2h = d["headtohead"]["team"]; aw = sum(r["winner"] == "anthropic" for r in h2h); ow = sum(r["winner"] == "openai" for r in h2h)

W, H = 1200, 420

def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render(theme):
    dark = theme == "dark"
    bg, panel, line = ("#0d1117", "#161b22", "#30363d") if dark else ("#ffffff", "#f6f8fa", "#d0d7de")
    fg, muted, subtle = ("#e6edf3", "#9da7b3", "#6e7681") if dark else ("#1f2328", "#59636e", "#8c959f")
    accent, green, red = ("#58a6ff", "#3fb950", "#f85149") if dark else ("#0969da", "#1a7f37", "#cf222e")
    mono = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    sans = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"



    stats = [(f"−{s['tokPct']:.0f}%", "tokens vs baseline", green),
             (f"{s['wins']}/30", "blind pairings won", accent),
             (f"{s['factsKept']:.0f}%", "required facts kept", fg),
             (f"−{100*(1-tc/ts):.0f}%", "tokens vs ASD-STE100", green)]
    stat_svg = ""
    for i, (v, label, col) in enumerate(stats):
        x = 64 + i * 150
        stat_svg += f'<text x="{x}" y="334" font-family="{sans}" font-size="30" font-weight="650" letter-spacing="-0.5" fill="{col}">{esc(v)}</text>'
        stat_svg += f'<text x="{x}" y="356" font-family="{sans}" font-size="11.5" fill="{muted}">{esc(label)}</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="CRISP: say the useful thing once, then stop. {s['tokPct']:.0f}% fewer tokens, {s['wins']} of 30 blind pairings won, {s['factsKept']:.0f}% of required facts kept.">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{accent}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="r"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#r)">
    <rect width="{W}" height="{H}" fill="{bg}"/>
    <rect width="{W}" height="{H}" fill="url(#g)"/>
    <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{line}"/>

    <!-- left: wordmark -->
    <text x="64" y="96" font-family="{sans}" font-size="64" font-weight="750" letter-spacing="-2.5" fill="{fg}">CRISP</text>
    <text x="64" y="128" font-family="{sans}" font-size="15" letter-spacing="2.2" fill="{muted}">CONCISE · RELEVANT · INTUITIVE · SIMPLE · PROTOCOL</text>
    <text x="64" y="186" font-family="{sans}" font-size="26" font-weight="600" letter-spacing="-0.6" fill="{fg}">Say the useful thing once,</text>
    <text x="64" y="218" font-family="{sans}" font-size="26" font-weight="600" letter-spacing="-0.6" fill="{fg}">as clearly as possible, then stop.</text>
    <text x="64" y="252" font-family="{sans}" font-size="14.5" fill="{muted}">A writing protocol for humans and LLMs. One engineer talking to another.</text>
    <text x="64" y="274" font-family="{sans}" font-size="14.5" fill="{muted}">Works as a system prompt, a slash command, or a verb: “crispify this.”</text>

    <line x1="64" y1="300" x2="640" y2="300" stroke="{line}"/>
    {stat_svg}

    <!-- right: install terminal -->
    <rect x="676" y="52" width="460" height="316" rx="12" fill="{panel}" stroke="{line}"/>
    <circle cx="700" cy="76" r="5" fill="{red}" opacity=".9"/><circle cx="718" cy="76" r="5" fill="#d29922" opacity=".9"/><circle cx="736" cy="76" r="5" fill="{green}" opacity=".9"/>
    <text x="906" y="80" text-anchor="middle" font-family="{sans}" font-size="11" fill="{subtle}">Claude Code</text>
    <line x1="676" y1="96" x2="1136" y2="96" stroke="{line}"/>

    <text x="700" y="128" font-family="{sans}" font-size="11" font-weight="650" letter-spacing="1.4" fill="{muted}">INSTALL</text>
    <text x="700" y="150" font-family="{mono}" font-size="12" fill="{fg}"><tspan fill="{green}">$</tspan> claude plugins marketplace add \\</text>
    <text x="716" y="168" font-family="{mono}" font-size="12" fill="{fg}">andreiverdes/awesome-claude</text>
    <text x="700" y="186" font-family="{mono}" font-size="12" fill="{fg}"><tspan fill="{green}">$</tspan> claude plugins install awesome-claude@awesome-claude</text>

    <text x="700" y="222" font-family="{sans}" font-size="11" font-weight="650" letter-spacing="1.4" fill="{muted}">USE</text>
    <text x="700" y="244" font-family="{mono}" font-size="12" fill="{fg}"><tspan fill="{accent}">&gt;</tspan> /crisp</text>
    <text x="700" y="262" font-family="{mono}" font-size="12" fill="{fg}"><tspan fill="{accent}">&gt;</tspan> crispify this</text>
    <text x="700" y="280" font-family="{mono}" font-size="12" fill="{fg}"><tspan fill="{accent}">&gt;</tspan> make this crispier</text>

    <text x="700" y="316" font-family="{sans}" font-size="11" font-weight="650" letter-spacing="1.4" fill="{muted}">OR IN ANY PROJECT</text>
    <text x="700" y="338" font-family="{mono}" font-size="12" fill="{fg}"><tspan fill="{green}">$</tspan> python3 skills/crisp/scripts/install.py --command</text>

    <text x="{W-64}" y="{H-24}" text-anchor="end" font-family="{sans}" font-size="11" fill="{subtle}">crisp-bench/v1 · Claude Sonnet 5.5 · 10 prompts × 3 samples · blind-judged</text>
  </g>
</svg>
'''

import hashlib, glob, re
out = os.path.join(ROOT, "web")
readme = os.path.join(ROOT, "README.md")
for theme in ("dark", "light"):
    svg = render(theme)
    tag = hashlib.sha1(svg.encode()).hexdigest()[:8]
    for old in glob.glob(os.path.join(out, f"hero-{theme}-*.svg")):
        os.remove(old)
    name = f"hero-{theme}-{tag}.svg"
    open(os.path.join(out, name), "w").write(svg)
    skill = os.path.join(ROOT, "skills", "crisp", "SKILL.md")
    sk = open(skill).read()
    sk = re.sub(rf"raw\.githubusercontent\.com/andreiverdes/crisp/main/web/hero-{theme}(-[0-9a-f]{{8}})?\.svg",
                f"raw.githubusercontent.com/andreiverdes/crisp/main/web/{name}", sk)
    open(skill, "w").write(sk)
    print(name, len(svg), "bytes; SKILL.md updated (README uses web/github-banner.png)")
