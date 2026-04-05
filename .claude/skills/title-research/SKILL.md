---
name: title-research
description: Use when an RFQ arrives with a property address, taxlot, legal description, or owner name and you need to pull all recorded deeds (subject parcel + all adjoiners) and plats/records of survey into the project folder.
argument-hint: "address, taxlot, legal description, or owner name"
---

# Title Research Skill

## What This Is

Automates title research for Lincoln County, Oregon properties. Given any property identifier from an RFQ (address, taxlot, legal description, or owner name), this skill:

1. Looks up the subject parcel via Lincoln County ArcGIS and assessor portals
2. Identifies all adjoining parcels via spatial query
3. Downloads the most recent deed for each parcel (subject + adjoiners) into the project's `Deeds - Plats\` folder
4. Downloads all plats and records of survey into the same `Deeds - Plats\` folder
5. Saves a title research summary to the project's `Title Reviewing\` folder
6. Organizes everything under the project folder on disk and outputs a summary

Never sends anything. Chris reviews all downloads.

---

## How to Invoke

```
/title-research [identifier]
```

Examples:
- `/title-research 456 Harbor St Newport OR`
- `/title-research 10-11-12-00-00100`
- `/title-research Lot 4, Block 2, Lincoln Shores Subdivision`
- `/title-research John Smith` (owner name fallback)

Also triggered automatically by `/email-response` when an RFQ email contains a property address or taxlot and mentions surveying, boundary, or title work.

---

## Key Portals

| Portal | URL | Purpose |
|---|---|---|
| ArcGIS REST API | `https://arcgisserver.lincolncounty.org/arcgis/rest/services/` | Parcel lookup + adjoiner spatial query |
| GIS Parcel Viewer | `https://maps.co.lincoln.or.us/` | Visual parcel map, fallback lookup |
| Property Assessment | `https://propertyweb.co.lincoln.or.us/` | Owner name, legal description, taxlot ID |
| Deed Recorder (Helion) | `https://helion.co.lincoln.or.us/DigitalResearchRoomPublic/` | Recorded deeds (free, no login, back to ~1977) |
| Surveyor Archive | `https://www.co.lincoln.or.us/359/Survey-Research` | Plats and records of survey |

---

## Portal Pre-Access (Required Before Running)

Some portals require a live browser session before they respond to automated requests. Before running this skill, open each of these URLs in a browser and accept any disclaimers:

| Portal | Pre-Access URL | Gate |
|---|---|---|
| Helion Deed Recorder | `https://helion.co.lincoln.or.us/DigitalResearchRoomPublic/` | "I Agree" disclaimer — sets session cookie required for deed search |
| Property Assessment | `https://propertyweb.co.lincoln.or.us/` | No gate, but intermittently down — verify it loads before running |
| ArcGIS REST API | `https://arcgisserver.lincolncounty.org/arcgis/rest/services/?f=json` | SSL cert expired as of 2026-04 — if it fails, skip to propertyweb fallback |

The skill can only proceed through automated steps after these portals are accessible. When triggered from `/email-response`, a self-addressed draft email with these links is sent to Chris first — run the skill after opening them.

---

## Execution Protocol

### Step 1 — Parse Input

Extract from the argument or from email context (when triggered via `/email-response`):
- Street address (e.g., 456 Harbor St, Newport OR)
- Taxlot number (Oregon format: Township-Range-Section-Taxlot, e.g., `10-11-12-00-00100`)
- Legal description (subdivision name, lot/block, or metes and bounds section reference)
- Owner name (last resort fallback)

If no usable identifier is found, prompt before proceeding:
> "I need an address, taxlot number, or owner name to look up the parcel. What property data was provided?"

---

### Step 2 — Look Up Subject Parcel

Query Lincoln County ArcGIS REST API to identify the subject parcel.

**By address:** Use the geocode or parcel address query endpoint on the tax parcel layer:
```
GET https://arcgisserver.lincolncounty.org/arcgis/rest/services/[layer]/MapServer/[id]/query
  ?where=ADDRESS+LIKE+%27[address]%25%27
  &outFields=*
  &f=json
```

**By taxlot/parcel ID:** Query by the NCPIN or TAXLOT field.

**Fallback:** If ArcGIS is unresponsive, use WebFetch to search `https://propertyweb.co.lincoln.or.us/` by address or parcel number. Extract: owner name, legal description, parcel ID, NCPIN.

Record for subject parcel:
- Parcel ID / NCPIN
- Owner name (last, first)
- Legal description (note subdivision name if present)
- Parcel geometry (as JSON ring for spatial query in Step 3)

If the parcel cannot be found, report what was tried and ask Chris to verify the address before continuing.

---

### Step 3 — Identify Adjoining Parcels

Use ArcGIS REST API spatial query to find all parcels that share a boundary with the subject parcel:

```
GET https://arcgisserver.lincolncounty.org/arcgis/rest/services/[layer]/MapServer/[id]/query
  ?geometry=[subject-parcel-geometry-json]
  &geometryType=esriGeometryPolygon
  &spatialRel=esriSpatialRelTouches
  &outFields=NCPIN,OWNER,LEGALDESC,ADDRESS
  &f=json
```

This returns all parcels whose boundaries touch the subject parcel.

**Before downloading anything**, output a confirmation table:

| # | Role | Taxlot / NCPIN | Owner | Address |
|---|---|---|---|---|
| 0 | Subject | 10-11-12-00-00100 | Smith, John | 456 Harbor St |
| 1 | Adjoiner | 10-11-12-00-00200 | Jones, Mary | 460 Harbor St |
| ... | | | | |

If adjoiner count exceeds 15, pause and confirm:
> "Found [N] adjoining parcels — this is more than expected. Confirm you want to pull deeds for all of them, or provide a subset."

---

### Step 4 — Locate Project Folder

All project folders live at:
```
C:\Users\cjani\OneDrive\Documents\Projects\[project-name]\
```

Each project folder is already structured from the survey project template:
```
[project-name]\
├── Administration\
├── Deeds - Plats\       ← deeds and plats go here
├── Field Notes\
├── Legals\
├── Raw Data\
│   ├── Drone Data\
│   ├── Photos\
│   └── Point Files\
├── Title Reviewing\     ← title research summary goes here
└── Working\
```

**If triggered from `/email-response`:** Match the project name from the `projects/` tracking folder in the Claude AI workspace, then locate the corresponding folder under `C:\Users\cjani\OneDrive\Documents\Projects\`.

**If standalone:** List matching project folders under `C:\Users\cjani\OneDrive\Documents\Projects\` and ask Chris to confirm which one. If no project exists yet (pre-proposal RFQ), use a staging folder:
```
C:\Users\cjani\OneDrive\Documents\Projects\STAGING-[YYYY-MM-DD]-[address-slug]\Deeds - Plats\
C:\Users\cjani\OneDrive\Documents\Projects\STAGING-[YYYY-MM-DD]-[address-slug]\Title Reviewing\
```

Verify the target `Deeds - Plats\` folder exists before writing. If it does not exist, report the issue rather than creating an unknown folder structure.

---

### Step 5 — Download Deeds

For each parcel in the list (subject first, then adjoiners in order):

1. **Search Helion Digital Research Room** by owner last name:
   - URL: `https://helion.co.lincoln.or.us/DigitalResearchRoomPublic/`
   - Search grantor/grantee field for the owner last name
   - Filter document type to: Warranty Deed, Bargain and Sale Deed, Statutory Warranty Deed, Quitclaim Deed, Deed

2. **Select the most recent deed** for that owner as grantee (the deed conveying the property to the current owner).

3. **Download via Bash:**
```bash
curl -o "C:/Users/cjani/OneDrive/Documents/Projects/[project-name]/Deeds - Plats/[taxlot]-[owner-last]-deed.pdf" "[document-pdf-url]"
```

4. **File naming:** `[taxlot]-[owner-last-name]-deed.pdf`
   - Example: `10-11-12-00-00100-smith-deed.pdf`

**Flag** any parcels where:
- No deed found in Helion (owner name returned no results)
- Multiple deeds found requiring selection
- Likely pre-1977 recording not in the digital system

For flagged parcels: note the issue in the summary and provide the Helion search URL for manual follow-up.

---

### Step 6 — Download Plats and Records of Survey

Using the legal description from Step 2 (subdivision name and/or township/range/section):

1. **Search Lincoln County Surveyor archive** at `https://www.co.lincoln.or.us/359/Survey-Research`:
   - Look for the subdivision plat by name
   - Look for records of survey filed for that section/township/range

2. **Search Lincoln County GIS** at `https://maps.co.lincoln.or.us/` for survey layers near the subject parcel.

3. **Download available PDFs via Bash:**
```bash
curl -o "C:/Users/cjani/OneDrive/Documents/Projects/[project-name]/Deeds - Plats/[plat-name]-[recording-no].pdf" "[pdf-url]"
```

4. **File naming:** `[plat-name]-[recording-number].pdf`
   - Example: `lincoln-shores-sub-doc12345.pdf`
   - Example: `ros-smith-boundary-doc67890.pdf`

**Note:** The surveyor portal may not expose direct PDF download URLs in all cases. If a plat is visible on the map but not directly downloadable via URL, list it in the summary under "Manual downloads needed" with the portal URL and document name so Chris can grab it directly.

---

### Step 7 — Output Summary

Print a final summary:

**Deeds Downloaded**

| # | Role | Taxlot | Owner | Deed Found | File |
|---|---|---|---|---|---|
| 0 | Subject | 10-11-12-00-00100 | Smith, John | Yes | 10-11-12-00-00100-smith-deed.pdf |
| 1 | Adjoiner | 10-11-12-00-00200 | Jones, Mary | Yes | 10-11-12-00-00200-jones-deed.pdf |
| 2 | Adjoiner | 10-11-12-00-00300 | Unknown | No — pre-1977? | See note below |

**Plats Downloaded**
- `lincoln-shores-sub-doc12345.pdf`
- `ros-survey-section12-doc67890.pdf`

**Manual Downloads Needed** (if any)
- [Document name] — [URL to portal search result]

**Folders:**
- Deeds + Plats: `C:\Users\cjani\OneDrive\Documents\Projects\[project-name]\Deeds - Plats\`
- Summary: `C:\Users\cjani\OneDrive\Documents\Projects\[project-name]\Title Reviewing\title-research-[YYYY-MM-DD].md`

---

## Known Limitations

- Helion deed search is by owner name, not parcel ID. Common last names may return many results — the most recent deed to the current owner is the target.
- Helion records start around 1977. Older recordings require a Public Records Request to the Lincoln County Clerk at (541) 265-4121.
- **Helion requires a live browser session.** A disclaimer gate ("I Agree") must be clicked manually before any automated deed search or download will work. The session cookie is browser-local and cannot be shared with the Claude Code process — open the portal in a browser first.
- **The ArcGIS REST server had an expired SSL certificate as of April 2026.** If WebFetch returns a certificate error, skip directly to the `propertyweb.co.lincoln.or.us` fallback.
- **`propertyweb.co.lincoln.or.us` is intermittently unavailable (503).** If both ArcGIS and propertyweb fail, report both errors and stop — do not guess parcel data.
- Plat download automation depends on whether the surveyor portal exposes direct PDF URLs. Map-only interfaces will require manual download.
- ArcGIS REST service layer names and IDs can change. If a query fails, check `https://arcgisserver.lincolncounty.org/arcgis/rest/services/` for current layer structure.
- Adjoiner identification uses boundary-touch spatial query. Parcels separated only by a road right-of-way may not appear as adjoiners — flag these if the legal description suggests they should be included.
