"""
Generates index.html for the Bambu Lab Filament Availability Tracker GitHub Pages site.
Reads availability data from the FILAMENTS dict (shared with build_tracker.py).
"""

import json
from datetime import datetime

TODAY = "3/19/26"

FILAMENTS = {
    "PLA Basic": {
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
        "url": "https://us.store.bambulab.com/products/petg-basic",
        "colors": [
            ("Black", True), ("White", True), ("Gray",       True),
            ("Red",   True), ("Yellow",True), ("Reflex Blue",True),
            ("Dark Brown", True),
        ],
    },
    "PETG HF": {
        "url": "https://us.store.bambulab.com/products/petg-hf",
        "colors": [
            ("Blue",    False), ("Red",          False), ("Black",        True),
            ("Gray",    False), ("White",         False), ("Dark Gray",    False),
            ("Cream",   False), ("Orange",        False), ("Green",        False),
            ("Yellow",  False), ("Lime Green",    False), ("Forest Green", False),
            ("Lake Blue",False),("Peanut Brown",  False),
        ],
    },
    "TPU 95A HF": {
        "url": "https://us.store.bambulab.com/products/tpu-95a-hf",
        "colors": [
            ("Black", True), ("White", False), ("Gray",   True),
            ("Yellow",True), ("Blue",  True),  ("Red",    False),
        ],
    },
    "TPU for AMS": {
        "url": "https://us.store.bambulab.com/products/tpu-for-ams",
        "colors": [
            ("Red",       True),  ("Yellow",    False), ("Blue",      True),
            ("Neon Green",True),  ("White",     True),  ("Gray",      True),
            ("Black",     True),
        ],
    },
    "TPU 85A-90A": {
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

def build_html():
    cards = ""
    for name, info in FILAMENTS.items():
        colors = info["colors"]
        total   = len(colors)
        in_stk  = sum(1 for _, s in colors if s)
        out_stk = total - in_stk
        pct     = round(in_stk / total * 100)

        # Progress bar color: green→yellow→red
        bar_color = "#4caf50" if pct >= 75 else "#ff9800" if pct >= 40 else "#f44336"

        color_pills = ""
        for color, in_stock in colors:
            cls   = "pill in-stock" if in_stock else "pill out-stock"
            label = "✅" if in_stock else "🚫"
            color_pills += f'<span class="{cls}" title="{color}">{label} {color}</span>'

        cards += f"""
        <div class="card">
          <div class="card-header">
            <div>
              <h2 class="card-title">{name}</h2>
              <a class="store-link" href="{info['url']}" target="_blank">Shop ↗</a>
            </div>
            <div class="stats">
              <span class="stat in">{in_stk} in stock</span>
              <span class="stat out">{out_stk} out</span>
              <span class="stat pct">{pct}%</span>
            </div>
          </div>
          <div class="progress-wrap">
            <div class="progress-bar" style="width:{pct}%; background:{bar_color}"></div>
          </div>
          <div class="pills">{color_pills}</div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bambu Lab Filament Availability Tracker</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #111827;
      color: #e5e7eb;
      min-height: 100vh;
    }}
    header {{
      background: #1f2937;
      border-bottom: 1px solid #374151;
      padding: 1.25rem 1.5rem;
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: .5rem;
    }}
    header h1 {{
      font-size: 1.25rem;
      font-weight: 700;
      color: #f9fafb;
    }}
    .updated {{
      font-size: .8rem;
      color: #6b7280;
    }}
    main {{
      max-width: 960px;
      margin: 0 auto;
      padding: 1.5rem 1rem;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }}
    .card {{
      background: #1f2937;
      border: 1px solid #374151;
      border-radius: 10px;
      padding: 1rem;
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: .6rem;
      gap: .5rem;
    }}
    .card-title {{
      font-size: 1rem;
      font-weight: 600;
      color: #f9fafb;
      margin-bottom: .15rem;
    }}
    .store-link {{
      font-size: .72rem;
      color: #6b7280;
      text-decoration: none;
    }}
    .store-link:hover {{ color: #9ca3af; }}
    .stats {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: .15rem;
      white-space: nowrap;
    }}
    .stat {{ font-size: .75rem; font-weight: 600; }}
    .stat.in  {{ color: #4ade80; }}
    .stat.out {{ color: #f87171; }}
    .stat.pct {{ color: #9ca3af; }}
    .progress-wrap {{
      height: 5px;
      background: #374151;
      border-radius: 99px;
      margin-bottom: .75rem;
      overflow: hidden;
    }}
    .progress-bar {{
      height: 100%;
      border-radius: 99px;
      transition: width .3s;
    }}
    .pills {{
      display: flex;
      flex-wrap: wrap;
      gap: .3rem;
    }}
    .pill {{
      font-size: .7rem;
      padding: .2rem .45rem;
      border-radius: 99px;
      white-space: nowrap;
    }}
    .in-stock  {{ background: #14532d; color: #bbf7d0; }}
    .out-stock {{ background: #450a0a; color: #fca5a5; }}
    footer {{
      text-align: center;
      padding: 2rem 1rem;
      font-size: .75rem;
      color: #4b5563;
    }}
  </style>
</head>
<body>
  <header>
    <h1>🧵 Bambu Lab Filament Availability Tracker</h1>
    <span class="updated">Last updated: {TODAY}</span>
  </header>
  <main>{cards}
  </main>
  <footer>Data scraped from us.store.bambulab.com · Updated daily</footer>
</body>
</html>"""
    return html


if __name__ == "__main__":
    out = "/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/index.html"
    import os
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(build_html())
    print("Generated:", out)
