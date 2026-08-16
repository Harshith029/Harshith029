"""Generate the dot-matrix SVG assets used by README.md.

Everything is drawn from scratch and committed to the repo, so nothing
depends on a third-party image host staying up.

    python scripts/gen_assets.py

Edit NEOFETCH below to change the profile card text, then re-run.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

# GitHub's own contribution-graph greens, so the page matches the commit grid.
BG = "#0d1117"
DIM = "#21262d"
SCALE = ["#0e4429", "#006d32", "#26a641", "#39d353"]
BRIGHT = "#39d353"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
BORDER = "#30363d"

NAME = "HARSHITH"
TAGLINE = "AI ENGINEER  ·  FULL-STACK DEVELOPER"

NEOFETCH = [
    ("Role", "AI Engineer / Full-Stack Developer"),
    ("Languages", "Python, JavaScript, TypeScript, Java"),
    ("Focus", "Agent security · LLM tooling · Dev-infra"),
    ("Building", "safemigrate-lint · Sentinel · faultline"),
    ("Learning", "Distributed systems, system design"),
    ("Editor", "VS Code · Neovim"),
    ("Email", "harshith.pali3286@gmail.com"),
    ("Web", "harshith029.github.io/Portfolio-v2"),
]

# 5x7 dot font, only the glyphs this page needs.
FONT = {
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def dot(cx, cy, r, fill, delay=None, opacity=None):
    """A grid dot. With `delay` it cycles through the green scale as a wave."""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    if delay is None:
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{op}/>'
    vals = ";".join([SCALE[0], SCALE[1], SCALE[2], BRIGHT, SCALE[2], SCALE[1], SCALE[0]])
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{op}>'
        f'<animate attributeName="fill" values="{vals}" dur="3.2s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="r" values="{r};{r + 0.7:.1f};{r}" dur="3.2s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
        f"</circle>"
    )


def glyph_cells(text):
    """Yield (col, row) for every lit pixel, plus total width in cells."""
    cells, x = [], 0
    for ch in text:
        rows = FONT[ch]
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1":
                    cells.append((x + c, r))
        x += len(rows[0]) + 1
    return cells, x - 1


# ─────────────────────────────────────────────────────────── header ──
def build_header():
    W, H, PITCH = 1000, 230, 18
    cells, cols = glyph_cells(NAME)
    lit = set(cells)
    grid_w = cols * PITCH
    ox = (W - grid_w) // 2
    oy = 42

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="{esc(NAME)}">',
         f'<rect width="100%" height="100%" fill="{BG}"/>', "<g>"]

    # Dim dots fill the whole banner; lit dots spell the name and pulse as a wave.
    for row in range(-2, 10):
        for col in range(-((ox // PITCH) + 1), cols + (ox // PITCH) + 2):
            cx, cy = ox + col * PITCH, oy + row * PITCH
            if not (-PITCH < cx < W + PITCH):
                continue
            if (col, row) in lit:
                p.append(dot(cx, cy, 5.4, SCALE[2], delay=-(col * 0.055 + row * 0.02)))
            else:
                p.append(dot(cx, cy, 1.9, DIM))
    p.append("</g>")

    p.append(
        f'<text x="{W // 2}" y="204" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
        f'font-size="14" letter-spacing="4" fill="{MUTED}">{esc(TAGLINE)}</text>'
    )
    p.append("</svg>")
    return "\n".join(p)


# ────────────────────────────────────────────────────────── neofetch ──
def build_neofetch():
    W, H = 920, 380
    PAD, PITCH = 26, 16
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="neofetch profile card">',
         f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>']

    # Terminal chrome
    p.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="38" rx="10" fill="#161b22"/>')
    p.append(f'<rect x="0.5" y="28" width="{W - 1}" height="11" fill="#161b22"/>')
    p.append(f'<line x1="0" y1="39" x2="{W}" y2="39" stroke="{BORDER}"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        p.append(f'<circle cx="{22 + i * 19}" cy="19.5" r="6" fill="{c}"/>')
    p.append(f'<text x="{W // 2}" y="24" text-anchor="middle" font-family="ui-monospace, monospace" '
             f'font-size="12" fill="{MUTED}">harshith029 — neofetch</text>')

    # Left: dot-matrix "H" monogram
    cells, cols = glyph_cells("H")
    lit = set(cells)
    ox, oy = PAD + 44, 96
    for row in range(7):
        for col in range(5):
            cx, cy = ox + col * PITCH * 1.5, oy + row * PITCH * 1.5
            if (col, row) in lit:
                p.append(dot(cx, cy, 6.5, SCALE[2], delay=-(col * 0.12 + row * 0.05)))
            else:
                p.append(dot(cx, cy, 2.2, DIM))

    # Right: neofetch body
    tx = 300
    y = 82
    mono = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    p.append(f'<text x="{tx}" y="{y}" font-family="{mono}" font-size="15" font-weight="bold" fill="{BRIGHT}">'
             f'harshith029<tspan fill="{MUTED}">@</tspan>github</text>')
    y += 10
    p.append(f'<line x1="{tx}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="{BORDER}"/>')
    y += 24

    keyw = max(len(k) for k, _ in NEOFETCH)
    for k, v in NEOFETCH:
        p.append(
            f'<text x="{tx}" y="{y}" font-family="{mono}" font-size="13.5">'
            f'<tspan fill="{BRIGHT}" font-weight="bold">{esc(k.ljust(keyw))}</tspan>'
            f'<tspan fill="{MUTED}"> : </tspan>'
            f'<tspan fill="{TEXT}">{esc(v)}</tspan></text>'
        )
        y += 25

    # Palette swatches, like a real neofetch footer
    y += 6
    sw = 26
    for i, c in enumerate(SCALE + ["#58a6ff", "#bc8cff", "#f778ba", "#e3b341"]):
        p.append(f'<rect x="{tx + i * (sw + 5)}" y="{y}" width="{sw}" height="13" rx="2" fill="{c}"/>')

    p.append("</svg>")
    return "\n".join(p)


# ─────────────────────────────────────────────────────────────  rule ──
def build_rule():
    W, H, PITCH = 900, 12, 14
    n = W // PITCH
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="">']
    for i in range(n):
        cx = i * PITCH + PITCH / 2
        # fade toward both edges
        edge = min(i, n - 1 - i) / (n / 2)
        op = round(min(1.0, 0.12 + edge * 1.1), 2)
        p.append(
            f'<circle cx="{cx:.1f}" cy="6" r="1.9" fill="{SCALE[1]}" opacity="{op}">'
            f'<animate attributeName="fill" values="{SCALE[1]};{BRIGHT};{SCALE[1]}" dur="4s" '
            f'begin="{-i * 0.05:.2f}s" repeatCount="indefinite"/></circle>'
        )
    p.append("</svg>")
    return "\n".join(p)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, svg in [("header.svg", build_header()),
                      ("neofetch.svg", build_neofetch()),
                      ("rule.svg", build_rule())]:
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print(f"wrote {name:16} {os.path.getsize(path):>7} bytes")


if __name__ == "__main__":
    main()
