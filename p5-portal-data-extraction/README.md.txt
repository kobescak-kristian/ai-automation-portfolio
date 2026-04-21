# P5 — Portal Data Extraction System

## Overview
Python automation that extracts structured contravention data 
from a web-based portal with no export function, and delivers 
a formatted 3-tab Excel workbook ready for fleet management 
and tribunal tracking.

## Who This Is For
Fleet operators, transport companies, and vehicle leasing firms 
managing high volumes of traffic contraventions through a 
portal with no bulk export or API access.

## Problem Solved
Each contravention must be opened individually to view offence 
details, hearing schedule, tribunal assignment, and judgement. 
At high volumes this is unworkable manually. Missing a tribunal 
hearing results in an automatic Guilty — No Show judgement plus 
additional penalty, with no right to contest.

## How It Works
1. Script opens Chrome — user authenticates manually in browser
2. Script fetches full contravention list via the portal's 
   dynamic data endpoint
3. Loops through each record, extracts contravention details 
   and all hearing rows
4. Progress saved to checkpoint file after each record
5. If interrupted, re-run resumes from last saved point
6. On completion: exports timestamped 3-tab Excel, 
   removes checkpoint files

## Usage
1. Install: `pip install selenium undetected-chromedriver 
   beautifulsoup4 pandas openpyxl`
2. Run: `python main.py`
3. When Chrome opens, authenticate manually in the portal
4. Return to terminal and press Enter
5. Script runs — progress saved after each record
6. If interrupted, re-run resumes from last checkpoint
7. Output: timestamped `.xlsx` in the same folder

## Output
3-tab Excel workbook:
- **Records** — one row per contravention, 16+ columns 
  including amounts, offence, location, hearing summary, 
  evidence and document links
- **Hearings** — full hearing history per record with 
  clickable document links, deduplicated
- **Summary** — counts and amounts by month, locality, 
  and judgement type

## Tools
Python · Selenium · undetected-chromedriver · 
BeautifulSoup4 · pandas · openpyxl

## Key Technical Decisions

**Browser-based automation:** Data loads dynamically via 
JavaScript — not present in initial HTML response. Browser 
automation was required to access dynamically loaded content.

**Dynamic content handling:** Record data loads via a dynamic 
data loading mechanism identified via network inspection — 
not available in page source.

**Checkpoint system:** Designed for high-volume use where 
mid-run interruptions are likely. Saves state after every 
record. Restart reads checkpoint and skips already-fetched 
records — zero progress lost on failure.

**Hearing deduplication:** Portal serves duplicate hearing 
rows for some records. Deduplicated during extraction.

**Manual authentication:** No credentials stored or 
hardcoded. User authenticates with their own session — 
script takes over after login is complete.

## Outcome
Single script run extracts all contraventions, full hearing 
history, and document links — producing a formatted 3-tab 
Excel workbook. Eliminates manual per-record processing and 
reduces operational risk of missed deadlines. Checkpoint 
system makes the tool viable at high volumes where manual 
alternatives are not feasible.

## Known Limitations
**Session expiry:** Authentication expires between runs — 
fresh login required each time.

**Packaging:** Single executable packaging unresolved on 
current Python version. Distribution: run via terminal.

**Data scope:** Limited to records visible on the portal — 
pre-launch historical records not available.

**Single-user:** No multi-account or delegated access in v1.0.

**Scale:** Designed for high-volume runs (15k–20k records). 
Full-scale testing pending.

**Scheduling:** Manual trigger only.

*Future direction: scheduled runs with automated delivery 
of output workbook.*

## Status
Complete — v1.0 · executable packaging pending

## Files
- `extraction_pipeline_sample.py` — Illustrative extract 
  showing checkpoint recovery and Excel export logic. 
  Full implementation available on request.
- `diagram.jpg` — Architecture flow diagram

*Sample output not published — contains personal 
enforcement data.*

## Metadata

| Field | Value |
|---|---|
| Trigger type | Manual execution |
| Input source | Web-based portal (authenticated browser session) |
| Output destinations | Local .xlsx file |
| AI role | None — deterministic extraction and formatting |
| Routing logic | None |
| Deduplication | Hearing row deduplication during extraction |
| Business pattern | Dynamic content extraction + checkpoint recovery + structured export |
| Edge cases | Dynamic content loading · mid-run interruptions · duplicate hearing rows · session expiry |