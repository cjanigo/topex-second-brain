# Expert Witness Scope Writer Skill

**Status: Complete**

## What This Is

A scope of work generation skill for Chris Janigo, PE/PLS at Topex Inc. Given a project type and key parameters, this skill produces a complete, professional scope of work document ready for client delivery — including compensation terms, general conditions, and standard Topex language.

Supported project types:
- Expert witness and litigation support
- Civil engineering (design, reports, hydraulic modeling)
- Land surveying (boundary, record of survey, plat)
- Water rights examination or consulting
- City engineering
- Erosion and sediment control
- Drone / UAS services

---

## How to Invoke

```
/expert-witness-scope-writer [key parameters]
```

Examples:
- `/expert-witness-scope-writer overburden stockpile volumetric analysis, Tax Lot 801, Oregon`
- `/expert-witness-scope-writer boundary dispute, parcel survey, Lincoln County, WA`
- `/expert-witness-scope-writer water rights examination, deposition testimony`
- `/expert-witness-scope-writer` — prompts Chris for project details interactively

---

## Execution Protocol

### Step 1 — Gather Inputs

Collect the following before drafting. If any are missing and the user hasn't provided them, ask:

| Input | Required | Notes |
|---|---|---|
| Project type | Yes | Determines template and services |
| Client name | Yes | Full legal name for agreement header |
| Client address | Yes | For agreement header |
| Client email | Yes | For agreement header |
| Project description | Yes | Location, parcel/tax lot, subject matter |
| Governing state | Yes | Oregon or Washington — affects law section |
| Attorney / counsel name | If expert witness | For agreement header |
| Estimated hours by task | Optional | Helps set retainer; can be estimated |
| Special scope items | Optional | Any deliverables beyond the standard set |

If Chris provides a project description or drops in a PDF, extract what you can and ask only for what's missing.

### Step 2 — Select Template

Match the project type to a template:

| Project Type | Template |
|---|---|
| Expert witness / litigation support | See Expert Witness Template below |
| Boundary survey / record of survey | Use survey template structure |
| Civil engineering design | Use engineering template structure |
| Hydraulic modeling | Use engineering template structure |
| Water rights examination | Use water rights template structure |
| City engineering | Use engineering template structure |

For project types without a dedicated template yet, build from the Expert Witness template structure, adapting the scope section and rates.

### Step 3 — Fill and Draft

Populate the template with provided inputs. Follow these rules:

- Use the client's full legal name exactly as provided
- Dates: use the date Chris specifies, or leave a blank `__________` for manual fill
- Rates: use Chris's standard rates (see Rate Sheet below) unless he specifies otherwise
- Governing law: match to the project state (Oregon or Washington)
- Retainer: calculate as approximately 10 hours of primary work rate, rounded to nearest $500. Default $4,000 for expert witness. Flag if the scope suggests more.

### Step 4 — Output

Produce the full scope of work as clean markdown. Structure:

1. Header (Topex Inc., date, client address block)
2. Agreement title and parties
3. Numbered sections per template
4. General Terms and Conditions (standard Topex T&C — use boilerplate below)
5. Signature blocks

After the document, output a short note to Chris:

> **Review before sending:**
> - [list any blanks left for Chris to fill]
> - [flag any rates or retainer that may need adjustment]
> - [note if scope is broad enough to warrant a higher retainer]

---

## Rate Sheet (Standard Topex Rates)

| Service | Rate |
|---|---|
| Professional analysis / consulting | $225/hr |
| Report preparation / revisions | $225/hr |
| Declaration / affidavit preparation | $250/hr |
| Testimony (deposition, hearing, trial, Zoom) | $300/hr (2hr minimum) |
| Field survey (principal surveyor) | $185/hr |
| CAD drafting | $150/hr |
| GIS / mapping | $150/hr |
| Expert research | $225/hr |
| Travel time | $150/hr |

Billing increment: 0.25-hour for all services.

Update this rate sheet if Chris specifies new rates.

---

## Templates

**SOW template:** `templates/expert-witness-sow.md` — fill all `[bracketed]` fields.

**General Terms and Conditions:** `templates/topex-general-terms.txt` — append verbatim after the signature block. For Washington projects, replace "state of Oregon" with "state of Washington" in Section 16.1.

Read both files at Step 3 when drafting the document.

---

## Output Format Rules

Follow `.claude/rules/communication-style.md`:
- Formal document language — no casual tone, no emojis, no dashes in prose
- Tables for rate schedules
- Short, numbered sections
- No trailing summaries in the document itself — review notes go after the document, clearly separated

---

## When to Ask Before Drafting

Ask Chris first when:
- Project type is ambiguous between engineering and expert witness (different rate structures)
- Governing state is unclear from context
- Retainer amount seems unusually high or low for the described scope
- Client is a government entity (may need modified T&C)
