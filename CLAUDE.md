# Bambu Filament Tracker — Project Memory

## What This Is
A daily-updated web page tracking Bambu Lab filament color availability.
Live site: https://plazman888.github.io/bambu-filament-tracker/
GitHub repo: https://github.com/Plazman888/bambu-filament-tracker

## File Locations (iCloud path — works on both machines)

| File | Path |
|------|------|
| All scripts + repo | ~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude/Projects/bambu-filament-tracker/ |
| Filament spreadsheet | .../bambu-filament-tracker/data/Bambu_Filament_Tracker.xlsx |
| Scheduled task skill | ~/Library/Mobile Documents/com~apple~CloudDocs/Documents/AI STUFF/Apps and other things AI has created for me/Claude/Scheduled/update-bambu-filament-availability/SKILL.md |
| Scraper script | .../AI STUFF/Apps.../update_bambu_tracker.py |

## Key Scripts

| Script | Purpose |
|--------|---------|
| build_tracker.py | Updates the Excel spreadsheet with new availability data |
| generate_html.py | Regenerates index.html from latest data |
| update_bambu_tracker.py | Scraper — fetches availability from Bambu Lab store |

## How Publishing Works
1. Scheduled task (daily ~2am) scrapes Bambu Lab store pages via Chrome JS
2. Runs build_tracker.py to update the xlsx
3. Runs generate_html.py to regenerate index.html
4. `git commit` + `git push` to GitHub
5. GitHub Pages serves index.html automatically

## Git / Credentials
- Remote: git@github.com:Plazman888/bambu-filament-tracker.git (SSH)
- SSH key on Mac mini: ~/.ssh/id_ed25519 (added to GitHub 2026-05-07)
- No token in git config — credentials via SSH key only

## MacBook Access
On MacBook, the iCloud path resolves as:
~/Documents/Claude/Projects/bambu-filament-tracker/
(Documents folder is iCloud-synced on MacBook)

## Cowork Workspace
Point the bambu-filament-tracker Cowork project workspace to:
- MacBook: ~/Documents/Claude/Projects/bambu-filament-tracker/
- Mac mini: connect via iCloud path using Desktop Commander
