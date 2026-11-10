"""Build the SVGs in assets/.

python scripts/cards.py          # rebuild hero, terminal and impact SVGs from assets/oss.json
python scripts/cards.py --fetch  # refresh assets/oss.json from GitHub first, then patch README counts
"""
import base64
import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
LOGOS = ASSETS / "logos"
STATS = ASSETS / "oss.json"
README = ROOT / "README.md"

USER = "Mahdi-Hasan"
# Personal, coursework or test repos that the portfolio does not list.
EXCLUDE_OWNERS = {USER, "Fazle-Rakib", "gourab98", "jspw", "sybilgit"}
EXCLUDE_REPOS: set[str] = set()

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
MERGED, OPEN = "#A371F7", "#3FB950"

# Hero content that does not come from GitHub
CHIPS = [("microsoft", "Microsoft"), ("JetBrains", "JetBrains"), ("vercel", "Vercel"),
         ("openclaw", "OpenClaw"), ("pydantic", "Pydantic"), ("Project-MONAI", "MONAI")]
TICKER = [("merged", "microsoft/agent-framework#9969"), ("merged", "HKUDS/DeepTutor#2454"),
          ("merged", "openclaw/openclaw#196631"), ("merged", "ivmartel/dwv#2370"),
          ("open", "pydantic/pydantic-ai#12590"), ("merged", "Nano-Collective/nanocoder#1961"),
          ("open", "Project-MONAI/MONAI#9251")]
FEATURED = [("microsoft/agent-framework", 9969, "Skip Gemini settings when a client is injected"),
            ("openclaw/openclaw", 196631, "Roll byte sizes over to the next unit"),
            ("HKUDS/DeepTutor", 2375, "Read lesson JSON from reasoning-model replies"),
            ("ivmartel/dwv", 2370, "Decode Korean ISO 2022 IR 149 DICOM strings")]

# Lucide icon paths (24x24, stroke-based)
ICONS = {
    "pr": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M6 9v12"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.27 6.96 12 12.01l8.73-5.05"/><path d="M12 22.08V12"/>',
    "star": '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "flow": '<rect x="3" y="3" width="8" height="8" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect x="13" y="13" width="8" height="8" rx="2"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "lang": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/>',
    "briefcase": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
}
# GitHub Octicons (16x16, fill-based)
OCTICONS = {
    "merge": "M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z",
    "pr": "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z",
}


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;")


def f(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


def lucide(name, x, y, size, color):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({size / 24:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def octicon(name, x, y, size, color):
    return f'<path transform="translate({f(x)} {f(y)}) scale({size / 16:.4f})" fill="{color}" d="{OCTICONS[name]}"/>'


def logo(owner):
    """Embed an org avatar as a data URI (an SVG loaded via <img> cannot fetch outside images)."""
    path = LOGOS / f"{owner}.png"
    if not path.exists():
        with urllib.request.urlopen(f"https://github.com/{owner}.png?size=48") as resp:
            path.write_bytes(resp.read())
    data = path.read_bytes()
    mime = "image/jpeg" if data[:2] == b"\xff\xd8" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def image(owner, x, y, size, clip_id, radius):
    uri = logo(owner)
    return (f'<clipPath id="{clip_id}"><rect x="{f(x)}" y="{f(y)}" width="{size}" height="{size}" rx="{radius}"/></clipPath>'
            f'<image href="{uri}" xlink:href="{uri}" x="{f(x)}" y="{f(y)}" width="{size}" height="{size}" clip-path="url(#{clip_id})"/>')


def odometer(num, x, y, size, fill, key, delay):
    """Each digit is a 0-9 column that rolls up and lands on the real value. Returns (svg, width)."""
    out, cx = [], x
    step, dw = size * 1.2, size * 0.62
    for i, ch in enumerate(num):
        if not ch.isdigit():
            out.append(f'<text x="{f(cx)}" y="{y}" font-size="{size}" font-weight="800" fill="{fill}">{esc(ch)}</text>')
            cx += size * (0.7 if ch == "K" else 0.62 if ch == "+" else 0.35)
            continue
        laps = 10 + int(ch)
        k = f"{key}d{i}"
        col = "".join(
            f'<text x="{f(cx)}" y="{f(y + n * step)}" font-size="{size}" font-weight="800" fill="{fill}">{n % 10}</text>'
            for n in range(laps + 1)
        )
        out.append(
            f'<style>@keyframes {k}{{to{{transform:translateY(-{f(laps * step)}px)}}}}</style>'
            f'<clipPath id="c{k}"><rect x="{f(cx - 2)}" y="{f(y - size * 0.9)}" width="{f(dw + 4)}" height="{f(size * 1.12)}"/></clipPath>'
            f'<g clip-path="url(#c{k})"><g style="animation:{k} {1.1 + i * 0.25:.2f}s {delay:.2f}s cubic-bezier(.2,.8,.2,1) both">{col}</g></g>'
        )
        cx += dw
    return "".join(out), cx - x


def lcg(seed):
    while True:
        seed = (seed * 9301 + 49297) % 233280
        yield seed / 233280


def hero(s):
    rnd = lcg(11)
    grid = []
    for c in range(53):
        for row in range(19):
            v = next(rnd)
            op = 0.3 if v > 0.86 else 0.16 if v > 0.66 else 0.08 if v > 0.42 else 0.03
            tw = f' class="tw" style="animation-delay:{next(rnd) * 5:.2f}s"' if v > 0.92 else ""
            grid.append(f'<rect x="{6 + c * 16}" y="{4 + row * 16}" width="12" height="12" rx="2.5" fill-opacity="{op}"{tw}/>')

    chips, cx, cy = [], 40, 224
    for i, (owner, name) in enumerate(CHIPS):
        w = len(name) * 7 + 46
        if i == 3:
            cx, cy = 40, cy + 32
        chips.append(
            f'<rect x="{cx}" y="{cy}" width="{w}" height="28" rx="8" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".14"/>'
            + image(owner, cx + 6, cy + 5, 18, f"av{i}", 4)
            + f'<text x="{cx + 31}" y="{cy + 18.5}">{name}</text>'
        )
        cx += w + 8

    def pill(x, w, icon, grad, text):
        return (f'<rect x="{x}" y="156" width="{w}" height="34" rx="10" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".14"/>'
                f'<rect x="{x + 6}" y="162" width="22" height="22" rx="6" fill="url(#{grad})"/>'
                + lucide(icon, x + 10.5, 166.5, 13, "#fff") + f'<text x="{x + 36}" y="178">{text}</text>')

    pills = (
        pill(40, 316, "briefcase", "ib", '<tspan font-size="13" font-weight="700" fill="#fff">Senior Software Engineer</tspan>'
             '<tspan font-size="13" fill="#94A3B8"> @ </tspan><tspan font-size="13" font-weight="600" fill="#22D3EE">CloudApper AI</tspan>')
        + pill(364, 112, "clock", "ia", '<tspan font-size="17" font-weight="800" fill="#FBBF24">5+</tspan>'
               '<tspan font-size="13" font-weight="700" fill="#fff"> years</tspan>')
    )

    # 2x2 live stat tiles
    x0, y0, tw_, th, gap, gr = 496, 34, 154, 117, 12, "url(#tx)"
    top_owner = s["top_repo"].split("/")[0]
    top_name = s["top_repo"] if len(s["top_repo"]) <= 21 else s["top_repo"][:20] + "…"

    def spark(x, y):
        d = s["growth"]
        xa, xb, ya, yb = x + 82, x + tw_ - 16, y + 70, y + 44
        peak = max(d) or 1
        pts = " ".join(f"{f(xa + (xb - xa) * i / (len(d) - 1))},{f(ya - v / peak * (ya - yb))}" for i, v in enumerate(d))
        return f'<polyline class="draw" points="{pts}" fill="none" stroke="{gr}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'

    def stars_extra(x, y, num_w):
        return (f'<text x="{f(x + 14 + num_w + 6)}" y="{y + 72}" font-size="13" font-weight="700" fill="#FBBF24">stars</text>'
                + image(top_owner, x + 14, y + 88, 14, "oc", 3.5)
                + f'<text x="{x + 33}" y="{y + 99}" font-size="11" fill="#CBD5E1">{esc(top_name)}</text>')

    tiles = [
        ("PULL REQUESTS", lambda x, y: octicon("pr", x + 14, y + 15, 13, "#A5B4FC"), str(s["prs"]),
         "fixes · features · docs", lambda x, y, w: spark(x, y)),
        ("LARGEST REPO", lambda x, y: lucide("star", x + 14, y + 15, 13, "#FBBF24"), s["top_stars"].removesuffix(" stars"),
         "", stars_extra),
        ("PROJECTS", lambda x, y: lucide("box", x + 14, y + 15, 13, "#A5B4FC"), str(s["projects"]),
         "AI · health · dev tools", None),
        ("MERGED", lambda x, y: octicon("merge", x + 14, y + 15, 13, MERGED), str(s["merged"]),
         f"of {s['prs']} PRs", None),
    ]
    tile_svg = []
    for i, (label, icon, num, sub, extra) in enumerate(tiles):
        x, y = x0 + (i % 2) * (tw_ + gap), y0 + (i // 2) * (th + gap)
        dot_x, dot_y = x + tw_ - 16, y + 22
        num_svg, num_w = odometer(num, x + 14, y + 72, 30, gr, f"t{i}", 0.3 + i * 0.1)
        tile_svg.append(
            f'<g class="tile" style="animation-delay:{0.2 + i * 0.1:.2f}s">'
            f'<clipPath id="tc{i}"><rect x="{x}" y="{y}" width="{tw_}" height="{th}" rx="12"/></clipPath>'
            f'<rect x="{x}" y="{y}" width="{tw_}" height="{th}" rx="12" fill="#0D1117" fill-opacity=".78" stroke="#fff" stroke-opacity=".13"/>'
            f'<g clip-path="url(#tc{i})"><rect x="{x}" y="{y}" width="{tw_}" height="3" fill="{gr}"/>'
            f'<rect class="shine" style="animation-delay:{i * 0.7:.1f}s" x="{x - 70}" y="{y}" width="60" height="3" fill="url(#sh)"/></g>'
            + icon(x, y)
            + f'<text x="{x + 34}" y="{y + 26}" font-size="10" font-weight="600" letter-spacing=".9" fill="#94A3B8">{label}</text>'
            f'<circle class="ping" style="transform-origin:{dot_x}px {dot_y}px" cx="{dot_x}" cy="{dot_y}" r="3.2" fill="#34D399"/>'
            f'<circle cx="{dot_x}" cy="{dot_y}" r="3.2" fill="#34D399"/>'
            + num_svg
            + (f'<text x="{x + 14}" y="{y + 99}" font-size="11" fill="#CBD5E1">{esc(sub)}</text>' if sub else "")
            + (extra(x, y, num_w) if extra else "")
            + "</g>"
        )

    def strip(start):
        x, out = start, []
        for state, name in TICKER:
            col, lab = (MERGED, "MERGED") if state == "merged" else (OPEN, "OPEN")
            out.append(
                octicon("merge" if state == "merged" else "pr", x, 313, 14, col)
                + f'<text x="{f(x + 20)}" y="324" fill="{col}" font-weight="700" font-size="10.5" letter-spacing=".8">{lab}</text>'
                f'<text x="{f(x + 26 + len(lab) * 8)}" y="324" fill="#CBD5E1">{name}</text>'
            )
            x += 20 + len(lab) * 8 + 6 + len(name) * 6.9 + 36
        return "".join(out), x - start

    one, width = strip(20)
    two, _ = strip(20 + width)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="848" height="342" viewBox="0 0 848 342"><style>
.t{{font-family:{FONT}}}
.tw{{animation:tw 4.5s ease-in-out infinite}}@keyframes tw{{0%,100%{{fill-opacity:.05}}50%{{fill-opacity:.42}}}}
.run{{animation:run 34s linear infinite}}@keyframes run{{to{{transform:translateX(-{f(width)}px)}}}}
.in{{animation:up .7s ease-out both}}.tile{{animation:up .6s ease-out both}}@keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.ping{{animation:ping 1.8s ease-out infinite}}@keyframes ping{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(2.6);opacity:0}}}}
.status{{animation:ping 1.8s ease-out infinite;transform-origin:45px 50px}}
.glow{{animation:breathe 6s ease-in-out infinite}}@keyframes breathe{{0%,100%{{opacity:.45}}50%{{opacity:.8}}}}
.shine{{animation:shine 3.2s ease-in-out infinite}}@keyframes shine{{0%{{transform:translateX(0)}}60%,100%{{transform:translateX({tw_ + 80}px)}}}}
.draw{{stroke-dasharray:200;stroke-dashoffset:200;animation:draw 1.6s .6s ease-out forwards}}@keyframes draw{{to{{stroke-dashoffset:0}}}}
</style><defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B0F1F"/><stop offset="1" stop-color="#111A3A"/></linearGradient>
<linearGradient id="mg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset=".38" stop-color="#fff" stop-opacity=".22"/><stop offset=".62" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="mask"><rect width="848" height="342" fill="url(#mg)"/></mask>
<radialGradient id="rg" cx=".8" cy=".05" r=".55"><stop offset="0" stop-color="#6366F1" stop-opacity=".45"/><stop offset="1" stop-color="#6366F1" stop-opacity="0"/></radialGradient>
<linearGradient id="tx" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A5B4FC"/><stop offset="1" stop-color="#22D3EE"/></linearGradient>
<linearGradient id="ib" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366F1"/><stop offset="1" stop-color="#A855F7"/></linearGradient>
<linearGradient id="ia" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F59E0B"/><stop offset="1" stop-color="#F97316"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0B0F1F"/><stop offset=".07" stop-color="#0B0F1F" stop-opacity="0"/><stop offset=".93" stop-color="#0B0F1F" stop-opacity="0"/><stop offset="1" stop-color="#0B0F1F"/></linearGradient>
<clipPath id="clip"><rect width="848" height="342" rx="16"/></clipPath></defs>
<g clip-path="url(#clip)" class="t">
<rect width="848" height="342" fill="url(#bg)"/>
<g mask="url(#mask)" fill="#818CF8">{''.join(grid)}</g>
<rect class="glow" width="848" height="342" fill="url(#rg)"/>
<g class="in">
<circle class="status" cx="45" cy="50" r="4" fill="#34D399"/><circle cx="45" cy="50" r="4" fill="#34D399"/>
<text x="57" y="54.5" font-size="12.5" fill="#6EE7B7" font-weight="600" letter-spacing=".3">Open to any roles</text>
<text x="40" y="106" font-size="44" font-weight="800" fill="#fff" letter-spacing="-1">Mehedi Hasan</text>
<text x="40" y="139" font-size="20" font-weight="700" fill="url(#tx)">Full-Stack Software &amp; Product Engineer</text>
{pills}
{lucide("code", 40, 205, 12, "#64748B")}<text x="58" y="215" font-size="10.5" font-weight="600" fill="#64748B" letter-spacing="1.2">OPEN-SOURCE CONTRIBUTOR TO</text>
</g>
<g class="in" style="animation-delay:.15s" font-size="12" font-weight="500" fill="#E2E8F0">{''.join(chips)}</g>
{''.join(tile_svg)}
<rect y="300" width="848" height="42" fill="#020617" fill-opacity=".6"/>
<line x1="0" y1="300" x2="848" y2="300" stroke="#fff" stroke-opacity=".06"/>
<g font-size="12.5"><g class="run">{one}{two}</g></g>
<rect y="300" width="848" height="42" fill="url(#fade)"/>
</g></svg>"""


def terminal(s):
    ok = f'<tspan fill="{MERGED}">✓</tspan>'
    lines = [("cmd", "gh pr list --author @me --state merged --limit 4")]
    for repo, n, title in FEATURED:
        lines.append(("out", f'{ok}<tspan fill="#C9D1D9"> {repo.ljust(27)}</tspan><tspan fill="{MERGED}">#{n}</tspan>'
                             f'<tspan fill="#8B949E">  {esc(title)}</tspan>'))
    lines.append(("cmt", "# totals across all repos"))
    dot = '<tspan fill="#8B949E"> · </tspan>'
    lines.append(("out", f'<tspan fill="#C9D1D9">{s["prs"]} PRs</tspan>{dot}<tspan fill="{MERGED}">{s["merged"]} merged</tspan>{dot}'
                         f'<tspan fill="#C9D1D9">{s["projects"]} projects</tspan>{dot}<tspan fill="#FBBF24">{s["top_stars"]} ★</tspan>'
                         '<tspan fill="#8B949E"> on the largest repo</tspan>'))
    y, t, out = 68, 0.4, []
    for i, (kind, text) in enumerate(lines):
        if kind == "cmd":
            w, d = (len(text) + 2) * 8.45 + 4, max(0.45, len(text) * 0.03)
            out.append(f'<clipPath id="c{i}"><rect x="24" y="{y - 16}" height="22" width="0">'
                       f'<animate attributeName="width" from="18" to="{f(w)}" begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze"/></rect></clipPath>'
                       f'<text x="28" y="{y}" clip-path="url(#c{i})"><tspan fill="#3FB950">$</tspan><tspan fill="#E6EDF3"> {esc(text)}</tspan></text>')
            t += d + 0.25
        else:
            fill = ' fill="#6E7681"' if kind == "cmt" else ""
            body = esc(text) if kind == "cmt" else text
            out.append(f'<text x="28" y="{y}" opacity="0" xml:space="preserve"{fill}>{body}'
                       f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".25s" fill="freeze"/></text>')
            t += 0.3 if kind == "cmt" else 0.22
        nxt = lines[i + 1][0] if i + 1 < len(lines) else None
        y += 36 if kind == "out" and nxt not in (None, "out") else 27
    y += 8
    out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".1s" fill="freeze"/>'
               f'<text x="28" y="{y}" fill="#3FB950">$</text><rect class="cur" x="44" y="{y - 13}" width="9" height="17" fill="#E6EDF3"/></g>')
    h = y + 26
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="848" height="{h}" viewBox="0 0 848 {h}"><style>
.m{{font-family:{MONO};font-size:14px}}
.cur{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
</style>
<rect x=".5" y=".5" width="847" height="{h - 1}" rx="12" fill="#0D1117" stroke="#30363D"/>
<path d="M12.5 .5h823a12 12 0 0 1 12 12V36H.5V12.5a12 12 0 0 1 12-12z" fill="#161B22"/>
<line x1="0" y1="36" x2="848" y2="36" stroke="#30363D"/>
<circle cx="22" cy="18" r="6" fill="#FF5F57"/><circle cx="42" cy="18" r="6" fill="#FEBC2E"/><circle cx="62" cy="18" r="6" fill="#28C840"/>
<text x="424" y="22.5" text-anchor="middle" class="m" font-size="12" fill="#8B949E">mehedi@oss: ~/open-source</text>
<g class="m">{''.join(out)}</g></svg>"""


# Impact cards (light/dark aware, sit further down the README)
CARD_STYLE = f"""<style>
.card{{animation:up .5s ease-out both}}
@keyframes up{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:translateY(0)}}}}
.bg{{fill:#FFFFFF;stroke:#E4E7EC}}
.ico{{stroke:#4F46E5;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.lbl{{font:600 11px {FONT};letter-spacing:.08em;fill:#667085}}
.num{{font:700 34px {FONT};letter-spacing:-.02em;fill:url(#gl)}}
.sub{{font:400 12.5px {FONT};fill:#475467}}
.bar{{fill:url(#gl)}}
@media (prefers-color-scheme: dark){{
.bg{{fill:#0D1117;stroke:#262C36}}
.ico{{stroke:#818CF8}}
.lbl{{fill:#8B949E}}
.num{{fill:url(#gd)}}
.sub{{fill:#C9D1D9}}
.bar{{fill:url(#gd)}}
}}
</style>
<defs>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4F46E5"/><stop offset="1" stop-color="#0891B2"/></linearGradient>
<linearGradient id="gd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A5B4FC"/><stop offset="1" stop-color="#22D3EE"/></linearGradient>
</defs>"""

W, H, GAP, COLS = 201, 128, 14, 4

IMPACT = [
    ("lock", "SSO USERS", "60K+", "central SSO · .NET · Redis"),
    ("building", "COMPANIES", "800+", "on PIHR · 50,000+ users"),
    ("file", "INVOICES", "~100K", "90% accuracy · 3,000+ clients"),
    ("flow", "MANUAL WORK", "70%+", "less, via automation"),
    ("zap", "API SPEED", "20–30%", "faster · caching · queues"),
    ("shield", "PHI LEAKS", "Zero", "in production · HIPAA"),
    ("lang", "BANGLA SUMMARY", "~2×", "accuracy · fine-tuned mT5"),
    ("award", "LINKEDIN C# & OOP", "Top 5%", "of 1M+ people"),
]


def card(i, icon, label, num, sub):
    x = (i % COLS) * (W + GAP)
    y = (i // COLS) * (H + GAP)
    return (
        f'<g class="card" style="animation-delay:{i * 0.06:.2f}s">'
        f'<clipPath id="c{i}"><rect x="{x}" y="{y}" width="{W}" height="{H}" rx="12"/></clipPath>'
        f'<rect class="bg" x="{x}" y="{y}" width="{W}" height="{H}" rx="12" stroke-width="1"/>'
        f'<rect class="bar" x="{x}" y="{y}" width="{W}" height="3" clip-path="url(#c{i})"/>'
        f'<g class="ico" transform="translate({x + 20} {y + 22}) scale(.667)">{ICONS[icon]}</g>'
        f'<text x="{x + 44}" y="{y + 34}" class="lbl">{esc(label)}</text>'
        f'<text x="{x + 20}" y="{y + 80}" class="num">{esc(num)}</text>'
        f'<text x="{x + 20}" y="{y + 106}" class="sub">{esc(sub)}</text>'
        "</g>"
    )


def cards_svg(cards):
    rows = (len(cards) + COLS - 1) // COLS
    w = COLS * W + (COLS - 1) * GAP
    h = rows * H + (rows - 1) * GAP
    body = "".join(card(i, *c) for i, c in enumerate(cards))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 2}" height="{h + 2}" '
        f'viewBox="-1 -1 {w + 2} {h + 2}">{CARD_STYLE}{body}</svg>'
    )


def gh_json(*args):
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def growth(dates, points=9):
    """Cumulative PR count at evenly spaced times from the first PR to now."""
    times = sorted(datetime.fromisoformat(d.replace("Z", "+00:00")) for d in dates)
    start, end = times[0], datetime.now(timezone.utc)
    marks = [start + (end - start) * i / (points - 1) for i in range(points)]
    return [sum(t <= m for t in times) for m in marks]


def fetch_stats():
    prs = gh_json("search", "prs", "--author", USER, "--limit", "1000", "--json", "repository,state,createdAt")
    prs = [
        p for p in prs
        if p["repository"]["nameWithOwner"].split("/")[0] not in EXCLUDE_OWNERS
        and p["repository"]["nameWithOwner"] not in EXCLUDE_REPOS
    ]
    repos = sorted({p["repository"]["nameWithOwner"] for p in prs})
    stars = {r: gh_json("api", f"repos/{r}")["stargazers_count"] for r in repos}
    top = max(stars, key=stars.get)
    n = stars[top]
    return {
        "prs": len(prs),
        "merged": sum(p["state"] == "merged" for p in prs),
        "projects": len(repos),
        "top_stars": f"{n // 10_000 * 10}K+" if n >= 10_000 else f"{n:,}",
        "top_repo": top,
        "growth": growth([p["createdAt"] for p in prs]),
    }


def patch_readme(s):
    raw = README.read_bytes().decode("utf-8")
    text = raw
    text = re.sub(r"(\*\*Open source:\*\* )\d+( PRs)", rf"\g<1>{s['prs']}\g<2>", text)
    text = re.sub(r"\d+ open-source PRs, \d+ merged, \d+ projects",
                  f"{s['prs']} open-source PRs, {s['merged']} merged, {s['projects']} projects", text)
    if text != raw:
        README.write_bytes(text.encode("utf-8"))


def main():
    if "--fetch" in sys.argv:
        stats = fetch_stats()
        STATS.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        patch_readme(stats)
    stats = json.loads(STATS.read_text(encoding="utf-8"))
    outputs = {"hero": hero(stats), "terminal": terminal(stats), "impact": cards_svg(IMPACT)}
    for name, svg in outputs.items():
        (ASSETS / f"{name}.svg").write_text(svg, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
