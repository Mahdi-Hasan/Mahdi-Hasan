"""Build the stat-card SVGs in assets/.

python scripts/cards.py          # rebuild both SVGs from assets/oss.json
python scripts/cards.py --fetch  # refresh assets/oss.json from GitHub first, then patch README counts
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
STATS = ASSETS / "oss.json"
README = ROOT / "README.md"

USER = "Mahdi-Hasan"
# Personal, coursework or abandoned repos that the portfolio does not list.
EXCLUDE_OWNERS = {USER, "Fazle-Rakib", "gourab98", "jspw", "sybilgit"}
EXCLUDE_REPOS = {"pydantic/pydantic-ai"}

# Lucide icon paths (24x24, stroke-based)
ICONS = {
    "pr": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M6 9v12"/>',
    "merge": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/>',
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
}

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Helvetica, Arial, sans-serif"

STYLE = f"""<style>
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


def oss_cards(s):
    return [
        ("pr", "PULL REQUESTS", str(s["prs"]), "fixes · features · docs"),
        ("merge", "MERGED", str(s["merged"]), "accepted by maintainers"),
        ("box", "PROJECTS", str(s["projects"]), "AI · health · dev tools"),
        ("star", "LARGEST REPO", s["top_stars"], f"stars · {s['top_repo']}"),
    ]


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;")


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


def build(cards):
    rows = (len(cards) + COLS - 1) // COLS
    w = COLS * W + (COLS - 1) * GAP
    h = rows * H + (rows - 1) * GAP
    body = "".join(card(i, *c) for i, c in enumerate(cards))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 2}" height="{h + 2}" '
        f'viewBox="-1 -1 {w + 2} {h + 2}">{STYLE}{body}</svg>'
    )


def gh_json(*args):
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def fetch_stats():
    prs = gh_json("search", "prs", "--author", USER, "--limit", "1000", "--json", "repository,state")
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
    }


def patch_readme(s):
    raw = README.read_bytes().decode("utf-8")
    text = raw
    text = re.sub(r"(\*\*Open source:\*\* )\d+( PRs)", rf"\g<1>{s['prs']}\g<2>", text)
    text = re.sub(r"\*\*\d+ PRs to \d+ projects\*\*", f"**{s['prs']} PRs to {s['projects']} projects**", text)
    text = re.sub(
        r"lines=\d+\+open-source\+PRs\+%C2%B7\+\d+\+merged\+%C2%B7\+\d+\+projects",
        f"lines={s['prs']}+open-source+PRs+%C2%B7+{s['merged']}+merged+%C2%B7+{s['projects']}+projects",
        text,
    )
    text = re.sub(
        r'alt="\d+ pull requests · \d+ merged · \d+ projects · [^"]*"',
        f'alt="{s["prs"]} pull requests · {s["merged"]} merged · {s["projects"]} projects · '
        f'{s["top_stars"]} stars on {s["top_repo"]}"',
        text,
    )
    if text != raw:
        README.write_bytes(text.encode("utf-8"))


def main():
    if "--fetch" in sys.argv:
        stats = fetch_stats()
        STATS.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        patch_readme(stats)
    stats = json.loads(STATS.read_text(encoding="utf-8"))
    for name, cards in (("oss", oss_cards(stats)), ("impact", IMPACT)):
        (ASSETS / f"{name}.svg").write_text(build(cards), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
