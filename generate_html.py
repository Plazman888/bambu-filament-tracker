"""
Generates index.html for the Bambu Lab Filament Availability Tracker.
"""

TODAY = "3/19/26"

FILAMENTS = {
    "PLA Basic": {
        "group": "PLA",
        "url": "https://us.store.bambulab.com/products/pla-basic-filament",
        "colors": [
            ("Jade White",      True),  ("Orange",          True),
            ("Blue",            True),  ("Gray",            True),
            ("Beige",           False), ("Silver",          False),
            ("Yellow",          True),  ("Blue Grey",       False),
            ("Pink",            True),  ("Brown",           True),
            ("Red",             True),  ("Black",           True),
            ("Bambu Green",     True),  ("Bronze",          True),
            ("Gold",            False), ("Purple",          False),
            ("Magenta",         False), ("Cyan",            True),
            ("Mistletoe Green", True),  ("Light Gray",      True),
            ("Dark Gray",       False), ("Maroon Red",      True),
            ("Sunflower Yellow",True),  ("Turquoise",       True),
            ("Indigo Purple",   True),  ("Bright Green",    False),
            ("Cocoa Brown",     True),  ("Hot Pink",        False),
            ("Cobalt Blue",     False), ("Pumpkin Orange",  True),
        ],
    },
    "PLA Matte": {
        "group": "PLA",
        "url": "https://us.store.bambulab.com/products/pla-matte",
        "colors": [
            ("Matte Ivory White",    True),  ("Matte Ash Gray",       True),
            ("Matte Mandarin Orange",True),  ("Matte Sakura Pink",    False),
            ("Matte Lemon Yellow",   True),  ("Matte Charcoal",       True),
            ("Matte Grass Green",    True),  ("Matte Latte Brown",    False),
            ("Matte Scarlet Red",    False), ("Matte Ice Blue",       False),
            ("Matte Lilac Purple",   True),  ("Matte Marine Blue",    True),
            ("Matte Dark Red",       True),  ("Matte Dark Blue",      False),
            ("Matte Dark Brown",     True),  ("Matte Dark Green",     True),
            ("Matte Desert Tan",     False), ("Matte Bone White",     False),
            ("Matte Plum",           False), ("Matte Sky Blue",       False),
            ("Matte Apple Green",    False), ("Matte Dark Chocolate", True),
            ("Matte Caramel",        False), ("Matte Terracotta",     False),
            ("Matte Nardo Gray",     True),
        ],
    },
    "PETG Basic": {
        "group": "PETG",
        "url": "https://us.store.bambulab.com/products/petg-basic",
        "colors": [
            ("Black", True), ("White", True), ("Gray",        True),
            ("Red",   True), ("Yellow",True), ("Reflex Blue", True),
            ("Dark Brown", True),
        ],
    },
    "PETG HF": {
        "group": "PETG",
        "url": "https://us.store.bambulab.com/products/petg-hf",
        "colors": [
            ("Blue",         False), ("Red",           False), ("Black",        True),
            ("Gray",         False), ("White",          False), ("Dark Gray",    False),
            ("Cream",        False), ("Orange",         False), ("Green",        False),
            ("Yellow",       False), ("Lime Green",     False), ("Forest Green", False),
            ("Lake Blue",    False), ("Peanut Brown",   False),
        ],
    },
    "TPU 95A HF": {
        "group": "TPU",
        "url": "https://us.store.bambulab.com/products/tpu-95a-hf",
        "colors": [
            ("Black", True), ("White", False), ("Gray",   True),
            ("Yellow",True), ("Blue",  True),  ("Red",    False),
        ],
    },
    "TPU for AMS": {
        "group": "TPU",
        "url": "https://us.store.bambulab.com/products/tpu-for-ams",
        "colors": [
            ("Red",       True),  ("Yellow",    False), ("Blue",      True),
            ("Neon Green",True),  ("White",     True),  ("Gray",      True),
            ("Black",     True),
        ],
    },
    "TPU 85A-90A": {
        "group": "TPU",
        "url": "https://us.store.bambulab.com/products/tpu-85a-tpu-90a",
        "colors": [
            ("85A — Light Cyan",   True),  ("85A — Neon Orange",  True),
            ("85A — Black",        True),  ("85A — Flesh",        True),
            ("85A — Lime Green",   True),  ("90A — Black",        True),
            ("90A — White",        True),  ("90A — Quicksilver",  True),
            ("90A — Crystal Blue", True),  ("90A — Grape Jelly",  True),
            ("90A — Cocoa Brown",  True),  ("90A — Frozen",       True),
            ("90A — Blaze",        True),
        ],
    },
}

GROUPS = ["PLA", "PETG", "TPU"]


def stats(colors):
    total  = len(colors)
    in_stk = sum(1 for _, s in colors if s)
    out    = total - in_stk
    pct    = round(in_stk / total * 100) if total else 0
    return total, in_stk, out, pct


def bar_color(pct):
    if pct >= 75: return "#4caf50"
    if pct >= 40: return "#ff9800"
    return "#f44336"


def build_chart():
    """SVG stacked bar chart — one bar per filament line."""
    CHART_H   = 140   # px, max bar height
    BAR_W     = 36
    GAP       = 18
    PAD_L     = 8
    LABEL_H   = 36    # space below bars for labels
    SVG_H     = CHART_H + LABEL_H + 10

    items = list(FILAMENTS.items())
    max_total = max(len(info["colors"]) for _, info in items)
    n = len(items)
    SVG_W = PAD_L * 2 + n * BAR_W + (n - 1) * GAP

    bars = ""
    labels = ""
    short = ["PLA\nBasic", "PLA\nMatte", "PETG\nBasic", "PETG\nHF",
             "TPU\n95A HF", "TPU\nAMS", "TPU\n85/90A"]

    for i, (name, info) in enumerate(items):
        total, in_stk, out, pct = stats(info["colors"])
        x = PAD_L + i * (BAR_W + GAP)
        full_h = round(total / max_total * CHART_H)
        in_h   = round(in_stk / total * full_h) if total else 0
        out_h  = full_h - in_h
        y_top  = CHART_H - full_h

        # out-of-stock on top (red), in-stock on bottom (blue)
        if out_h > 0:
            bars += f'<rect x="{x}" y="{y_top}" width="{BAR_W}" height="{out_h}" fill="#c0504d" rx="3"/>'
        if in_h > 0:
            bars += f'<rect x="{x}" y="{y_top + out_h}" width="{BAR_W}" height="{in_h}" fill="#4472c4" rx="3"/>'

        # two-line label
        lx = x + BAR_W // 2
        ly = CHART_H + 14
        parts = short[i].split("\n")
        labels += f'<text x="{lx}" y="{ly}" text-anchor="middle" fill="#9ca3af" font-size="10" font-family="system-ui">{parts[0]}</text>'
        if len(parts) > 1:
            labels += f'<text x="{lx}" y="{ly + 13}" text-anchor="middle" fill="#9ca3af" font-size="10" font-family="system-ui">{parts[1]}</text>'

    legend = f'''
      <rect x="{SVG_W - 130}" y="4" width="12" height="12" fill="#4472c4" rx="2"/>
      <text x="{SVG_W - 114}" y="14" fill="#9ca3af" font-size="11" font-family="system-ui">In Stock</text>
      <rect x="{SVG_W - 60}" y="4" width="12" height="12" fill="#c0504d" rx="2"/>
      <text x="{SVG_W - 44}" y="14" fill="#9ca3af" font-size="11" font-family="system-ui">Out</text>'''

    return f'''<svg viewBox="0 0 {SVG_W} {SVG_H}" width="100%" style="max-width:{SVG_W}px;display:block;margin:0 auto">
      {legend}
      {bars}
      {labels}
    </svg>'''


def build_column(group_name):
    group_filaments = {k: v for k, v in FILAMENTS.items() if v["group"] == group_name}

    # Aggregate stats for the column header
    all_colors = [c for info in group_filaments.values() for c in info["colors"]]
    total, in_stk, out, pct = stats(all_colors)
    bc = bar_color(pct)

    sections = ""
    for name, info in group_filaments.items():
        t, ins, ot, p = stats(info["colors"])
        pills = "".join(
            f'<span class="pill {"in" if s else "out"}" title="{c}">{"✅" if s else "🚫"} {c}</span>'
            for c, s in info["colors"]
        )
        sections += f'''
        <details open>
          <summary>
            <span class="section-name">{name}</span>
            <span class="section-meta">
              <span class="si">{ins}✅</span>
              <span class="so">{ot}🚫</span>
              <a class="shop-link" href="{info['url']}" target="_blank" onclick="event.stopPropagation()">Shop ↗</a>
            </span>
          </summary>
          <div class="pills">{pills}</div>
        </details>'''

    return f'''
    <div class="col">
      <div class="col-header">
        <div class="col-title">{group_name}</div>
        <div class="col-summary">
          <span class="si">{in_stk} in stock</span>
          <span class="so">{out} out</span>
          <span class="pct">{pct}%</span>
        </div>
        <div class="prog-wrap"><div class="prog-bar" style="width:{pct}%;background:{bc}"></div></div>
      </div>
      {sections}
    </div>'''


def build_html():
    chart  = build_chart()
    cols   = "".join(build_column(g) for g in GROUPS)

    # Overall totals for the header
    all_c  = [c for info in FILAMENTS.values() for c in info["colors"]]
    _, ins, out, pct = stats(all_c)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bambu Lab Filament Availability</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #111827;
      color: #e5e7eb;
    }}

    /* ── Header ── */
    header {{
      background: #1f2937;
      border-bottom: 1px solid #374151;
      padding: 1rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: .5rem;
    }}
    header h1 {{ font-size: 1.1rem; font-weight: 700; color: #f9fafb; }}
    .header-meta {{ font-size: .78rem; color: #6b7280; text-align: right; }}
    .header-meta strong {{ color: #9ca3af; }}

    /* ── Chart ── */
    .chart-wrap {{
      background: #1f2937;
      border-bottom: 1px solid #374151;
      padding: 1.25rem 1.5rem 1rem;
    }}
    .chart-title {{
      font-size: .78rem;
      font-weight: 600;
      color: #6b7280;
      text-transform: uppercase;
      letter-spacing: .06em;
      margin-bottom: .75rem;
    }}

    /* ── Columns ── */
    .columns {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      padding: 1rem;
      max-width: 1200px;
      margin: 0 auto;
    }}

    /* ── Column header ── */
    .col-header {{
      background: #1f2937;
      border: 1px solid #374151;
      border-radius: 10px 10px 0 0;
      padding: .9rem 1rem .75rem;
      margin-bottom: 2px;
    }}
    .col-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: #f9fafb;
      margin-bottom: .35rem;
    }}
    .col-summary {{
      display: flex;
      gap: .75rem;
      font-size: .8rem;
      font-weight: 600;
      margin-bottom: .5rem;
    }}
    .prog-wrap {{
      height: 5px;
      background: #374151;
      border-radius: 99px;
      overflow: hidden;
    }}
    .prog-bar {{
      height: 100%;
      border-radius: 99px;
    }}

    /* ── Collapsible sections ── */
    details {{
      background: #1f2937;
      border: 1px solid #374151;
      border-top: none;
      overflow: hidden;
    }}
    details:last-child {{ border-radius: 0 0 10px 10px; }}

    summary {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: .6rem 1rem;
      cursor: pointer;
      user-select: none;
      list-style: none;
      gap: .5rem;
    }}
    summary::-webkit-details-marker {{ display: none; }}
    summary::before {{
      content: "▸";
      color: #4b5563;
      font-size: .75rem;
      transition: transform .2s;
      flex-shrink: 0;
    }}
    details[open] > summary::before {{ transform: rotate(90deg); }}
    summary:hover {{ background: #263244; }}

    .section-name {{
      font-size: .88rem;
      font-weight: 600;
      color: #e5e7eb;
      flex: 1;
    }}
    .section-meta {{
      display: flex;
      align-items: center;
      gap: .5rem;
      font-size: .75rem;
    }}
    .shop-link {{
      color: #4b5563;
      text-decoration: none;
      font-size: .72rem;
    }}
    .shop-link:hover {{ color: #9ca3af; }}

    /* ── Stats colors ── */
    .si  {{ color: #4ade80; }}
    .so  {{ color: #f87171; }}
    .pct {{ color: #9ca3af; }}

    /* ── Pills ── */
    .pills {{
      display: flex;
      flex-wrap: wrap;
      gap: .3rem;
      padding: .6rem 1rem .75rem;
    }}
    .pill {{
      font-size: .7rem;
      padding: .2rem .45rem;
      border-radius: 99px;
      white-space: nowrap;
    }}
    .pill.in  {{ background: #14532d; color: #bbf7d0; }}
    .pill.out {{ background: #450a0a; color: #fca5a5; }}

    /* ── Footer ── */
    footer {{
      text-align: center;
      padding: 2rem 1rem;
      font-size: .72rem;
      color: #374151;
    }}

    /* ── Mobile: single column ── */
    @media (max-width: 700px) {{
      .columns {{
        grid-template-columns: 1fr;
        padding: .75rem;
      }}
      header h1 {{ font-size: 1rem; }}
    }}
  </style>
</head>
<body>

<header>
  <h1>🧵 Bambu Lab Filament Availability</h1>
  <div class="header-meta">
    <strong>{ins}</strong> in stock &nbsp;·&nbsp; <strong>{out}</strong> out
    &nbsp;·&nbsp; Updated {TODAY}
  </div>
</header>

<div class="chart-wrap">
  <div class="chart-title">Colors by Filament Line</div>
  {chart}
</div>

<div class="columns">
  {cols}
</div>

<footer>Data scraped from us.store.bambulab.com · Updated daily</footer>

</body>
</html>"""


if __name__ == "__main__":
    import os
    out = "/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(build_html())
    print("Generated:", out)
