# Bambu Filament Tracker — Setup & Reference

Last updated: 2026-03-19

---

## What this does

Scrapes Bambu Lab's US store daily for filament color availability, updates an Excel spreadsheet with a new date column, and publishes a live website on GitHub Pages.

**Live site:** https://plazman888.github.io/bambu-filament-tracker/
**GitHub repo:** https://github.com/Plazman888/bambu-filament-tracker

---

## File locations

| File | Path |
|------|------|
| Excel spreadsheet | `/Users/michaelwhitney/Documents/AI STUFF/HTML files created by Claudette/Bambu_Filament_Tracker.xlsx` |
| Git repo / scripts | `/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/` |
| build_tracker.py | `/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/build_tracker.py` |
| generate_html.py | `/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/generate_html.py` |
| index.html (website) | `/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/index.html` |

Both Macs use the same paths because:
- Same username: `michaelwhitney`
- Documents folder synced via iCloud

---

## How the daily run works

### Step 1 — Scrape

Use Chrome MCP to open each Bambu Lab product page and run this JavaScript:

```js
const colorItems = document.querySelectorAll('ul.flex.flex-wrap li[value]');
const results = Array.from(colorItems)
  .filter(li => li.querySelector('img') !== null)
  .map(li => ({
    color: li.getAttribute('value'),
    inStock: li.querySelector('span.rotate-45') === null
  }));
JSON.stringify(results);
```

Pages:
- PLA Basic:   https://us.store.bambulab.com/products/pla-basic-filament
- PLA Matte:   https://us.store.bambulab.com/products/pla-matte
- PETG Basic:  https://us.store.bambulab.com/products/petg-basic
- PETG HF:     https://us.store.bambulab.com/products/petg-hf
- TPU 95A HF:  https://us.store.bambulab.com/products/tpu-95a-hf
- TPU for AMS: https://us.store.bambulab.com/products/tpu-for-ams
- TPU 90A colors: https://us.store.bambulab.com/products/tpu-85a-tpu-90a
- TPU 85A colors: https://us.store.bambulab.com/products/tpu-85a-tpu-90a?id=573761693833371666

Note: TPU 85A-90A is one product with a variant selector. Scrape both URLs separately.
Prefix 90A results with "90A — " and 85A results with "85A — ".

DOM indicator for out-of-stock: `span.rotate-45` inside the `li[value]` element.

### Step 2 — Update spreadsheet

Edit `build_tracker.py`:
- Update `TODAY` (format: M/D/YY, e.g. `3/19/26`)
- Update the `colors` list in the `FILAMENTS` dict with the scraped data

Then run:
```bash
python3 "/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/build_tracker.py"
```

The script reads the existing XLSX and appends a new date column. It skips automatically if TODAY already exists (duplicate protection).

### Step 3 — Regenerate website

Run:
```bash
python3 "/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/generate_html.py"
```

Then push to GitHub:
```bash
cd "/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker"
git add index.html generate_html.py build_tracker.py
git commit -m "Availability update $(date +%Y-%m-%d)"
git push
```

GitHub Pages auto-deploys within ~1 minute of push.

---

## Spreadsheet format

- **Summary sheet** (first tab): one row per filament line, aggregate in-stock/out-of-stock counts
- **Per-filament sheets**: column A = row number, column B = color name, columns C onward = one column per date
- Status values: ✅ (in stock) or 🚫 (out of stock)
- Dark theme styling: title `#1A1A2E`, headers `#0F3460`, rows `#1E1E2E`/`#252535`

---

## Website features

- 3-column layout: PLA / PETG / TPU (single column on mobile ≤700px)
- Date picker populated from all historical dates in the spreadsheet
- SVG bar chart showing in-stock vs out-of-stock per filament
- Collapsible sections per filament type (open by default)
- Light/dark mode toggle (persists via localStorage)
- `?reset` URL param clears saved theme preference
- Contact: plazman888@icloud.com
- All historical data embedded as JSON in the HTML — no server needed

---

## Git / GitHub

- Repo: https://github.com/Plazman888/bambu-filament-tracker
- Branch: main
- GitHub Pages source: main branch / root
- PAT token is embedded in the git remote URL (check with `git remote -v`)
- **Important:** The PAT token used during setup should be regenerated. After regenerating at https://github.com/settings/tokens, update the remote:
  ```bash
  cd "/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker"
  git remote set-url origin https://Plazman888:NEW_TOKEN@github.com/Plazman888/bambu-filament-tracker.git
  ```
  Then update the scheduled task prompt with the new token too.

---

## Scheduled task

- Task ID: `update-bambu-filament-availability`
- Schedule: daily at 4:00 PM
- Currently set up on: Mac mini (second Mac)
- MacBook Pro task: cancelled/disabled

---

## Mac setup requirements

- Python 3 (pre-installed on both Macs)
- openpyxl: `pip3 install openpyxl --break-system-packages`
- Cowork installed
- Chrome open (for scraping via Chrome MCP)

---

## To brief a new Claude session

Paste this into a new Cowork chat:

> I have a daily Bambu Lab filament availability tracker. The setup doc is at `/Users/michaelwhitney/Documents/3D PRINTING/bambu-filament-tracker/SETUP.md` — please read it and then help me with [your request].
