---
name: email-response
description: Read unread inbox emails, match to active projects, draft replies, and save as Gmail drafts. Handles RFQ proposals and title research prompts inline. Never sends. Chris reviews and sends manually.
---

# Email Response Skill

## What This Is

An automated email drafting skill for Chris Janigo, PE/PLS at Topex Inc. For every unread email in the inbox, this skill:

1. Reads the email thread
2. Identifies which active project(s) it relates to (by keyword matching)
3. Loads project context from `projects/` and `context/`
4. Drafts a reply in Chris's voice and saves it as a Gmail draft
5. Never sends — Chris reviews and sends manually
6. Prompts Chris for any information needed to make the reply complete

---

## How to Invoke

```
/email-response
```

Optional — process a specific message:
```
/email-response [search query or subject keywords]
```

Examples:
- `/email-response` — process all unread inbox emails
- `/email-response subject:hydraulic` — process only emails matching that query
- `/email-response from:client@example.com` — process emails from a specific sender

---

## Execution Protocol

### Step 1 — Load Context

Before reading any emails, load:
- `context/current-priorities.md` — active deadlines and focus areas
- `context/me.md` — Chris's credentials and role
- `context/project-index.md` — one-line summary of all active projects for keyword matching

Do NOT load all project READMEs upfront. Instead, use the index to match each email to the right project, then load only that project's README for full context. This keeps token usage low.


### Step 3 — Triage Each Email

For each email, determine:

1. **RFQ check** — Before anything else, check if this is a request for quote or proposal. See RFQ Detection below.
2. **Project match** — Match the subject, body, and sender against the project index loaded in Step 1. If a match is found, load that project's README now for full context.
3. **Action required** — What does the sender actually want? (answer a question, confirm a schedule, review a document, etc.)
4. **Information gaps** — What would Chris need to know to answer fully? If gaps exist, list them — ask Chris before drafting, or flag in the draft.
5. **Urgency** — Does this relate to a deadline within 7 days?

#### RFQ Detection

| Signal Type | Keywords / Conditions | Action |
|---|---|---|
| High-confidence | "quote", "proposal", "RFQ", "RFP", "scope of work", "how much", "cost estimate", "fee", "are you available", "can you help" | Flag as RFQ |
| Supporting | New sender not in project index + mentions parcel, address, survey, or engineering need | Flag as RFQ if combined with any high-confidence signal |
| RFQ confirmed | — | Do NOT draft standard reply; run proposal-building protocol below; note in Step 6 table: "RFQ — proposal saved to proposals/" |

**Proposal-Building Protocol (inline)**

**A. Gather fields from the email:**

| Field | Source |
|---|---|
| Client name | Email sender name |
| Client email | Email From address |
| Client address | Email body (if provided) |
| Service requested | Email body — what did they ask for? |
| Site/parcel info | Tax lot number, address, or location |
| Any scope specifics | Size, complexity, special requirements |
| Deadline or urgency | Any dates mentioned |

If client name, service type, or site location are missing, ask Chris before proceeding.

**B. Select template by service type:**

| Service Type | Template |
|---|---|
| Topographic survey (with or without boundary) | `templates/survey-sow-topo.md` |
| Boundary survey, ROS, easement, legal description | `templates/survey-sow.md` |
| Civil engineering (design, plans, analysis) | `templates/engineering-sow.md` |
| Expert witness / litigation support | `templates/expert-witness-sow.md` |
| Combined engineering + survey | `templates/engineering-survey-combined-sow.md` |

If ambiguous, make a reasonable selection and flag it.

**C. Estimate fee using the Fee Estimation Engine:**

Full protocol, base rate tables, multipliers, travel formula, and output format are in `references/fee-estimation.md`. Follow all five steps:

1. **Select base scope and fee** from the tables (survey topo+boundary, boundary only, or engineering)
2. **Apply modifiers** — timeline/rush, sole source, client type, site conditions, travel. Use the drive-time bands from Newport, OR. Look up drive time via WebSearch if the address is unfamiliar.
3. **Apply title research modifiers** if `/title-research` has already run — check the project's Title Reviewing folder for the summary. If title research has NOT run yet, mark the fee `[PRELIMINARY — pending title research]`.
4. **Build the internal breakdown block** — show to Chris, do not include in the client proposal. Format per the template in `references/fee-estimation.md` Step 3.
5. **Set the quote flag** — ready to quote, preliminary, flag for manual review, or hourly (per Step 4 of the reference).

**Key signals to extract from the RFQ email for fee estimation:**
- Site address or location → drive time and travel cost
- Any deadline mentioned → rush modifier
- "Referred by," direct contact, or no mention of other firms → sole source modifier
- Water features, steep terrain, dense brush → site condition modifier
- Whether it's a new or known client → client type modifier
- Service type and site size → base rate row selection

**D. Fill the template:**
- Replace every `[PLACEHOLDER]` with available information; use `[INSERT: ...]` for gaps
- Include OHWM language if site borders a creek, slough, river, wetland, or tidal area
- Always include: Part C fee with 50%/50% payment terms, $120/hr add-on rate, $300/hr expert witness rate, Part D schedule language (begin upon signed SOW and down payment), Attachment A reference

**E. Save proposal entry:**
1. Folder name: `proposals/YYMMDD-client-name-service-type/` (today's date)
2. Generate next sequential proposal ID from `proposals/README.md` (e.g., P26002)
3. Create `proposals/[folder-name]/README.md` using `templates/proposal-readme.md` — status: Pending
4. Add a row to `proposals/README.md` index — Status: Pending, no linked project yet

**F. Present to Chris:**
- Filled proposal text (ready to paste into Word / export as PDF)
- Fee estimate with flag if needs manual review
- Any `[INSERT: ...]` gaps to fill before sending
- Next steps: review, export to PDF with Topex letterhead, send to client; update proposal README with send date after sending

**If flagged as RFQ AND the email contains a property address, taxlot number, legal description, or owner + parcel reference:**
- Do NOT invoke `/title-research` automatically — county portals require a live browser session before automated access works
- Instead, save a self-addressed Gmail draft to `cjanigo@topexeng-ls.com` with:
  - **Subject:** `Title Research Ready: [property address or taxlot]`
  - **Body:**
    - One line: client name, property identifier, and service type from the RFQ
    - "Want me to run title research on this one? Open the portal links below first, then run the command."
    - Portal pre-access links (open in browser and accept any disclaimers before running):
      - Helion (deeds): https://helion.co.lincoln.or.us/DigitalResearchRoomPublic/ — click "I Agree"
      - Property Assessment: https://propertyweb.co.lincoln.or.us/
      - ArcGIS (parcel + adjoiners): https://arcgisserver.lincolncounty.org/arcgis/rest/services/?f=json
    - Command to run when ready: `/title-research [extracted identifier]`
- This draft is informational only — nothing runs until Chris manually invokes `/title-research`
- Note in the Step 6 summary table: "Title research prompt saved as draft — portal links provided, awaiting your go-ahead"

**After `/title-research` runs on this project:**
- Read the `title-research-[date].md` summary in the project's Title Reviewing folder
- Extract: date of most recent survey on file, adjoiner count, data availability flags
- Re-run Step C of the fee engine using the title research modifiers from `references/fee-estimation.md`
- Update the proposal README fee field with the revised estimate and change the flag from `[PRELIMINARY]` to `[UPDATED — title research complete]`
- Notify Chris: "Fee estimate updated based on title research — see proposal README"

### Step 4 — Draft the Reply

For each email, compose a draft reply following these rules:

**Tone and Style** (per `.claude/rules/communication-style.md`)
- Casual but professional
- Short — clients want answers, not essays
- No em dashes or en dashes — no dashes of any kind
- Emojis are OK in email
- Mix short paragraphs with bullets; avoid bullet-heavy walls
- Tables when data maps to rows/columns

**Structure**
- Open with a direct acknowledgment (not "I hope this email finds you well")
- Answer the question or address the action item first
- If you need more info from the client, ask one clear question
- Close naturally (no formal sign-off needed)
- Sign: Chris Janigo, PE, PLS | Topex Inc.

**Project Context**
- If the email matches an active project, pull in relevant details from that project's README
- Reference deadlines if they affect the client's question
- Do not reveal internal scheduling notes or priority labels to clients

**Handling Gaps**
- If key information is missing and Chris needs to fill it in, insert a placeholder like: `[INSERT: ...]`
- At the end of the draft body, add a note block (not sent to client) listing what Chris should verify before sending

### Step 5 — Save as Draft

Use `gmail_create_draft` with:
- `to`: original sender's email address
- `threadId`: the thread ID of the original message (to create a threaded reply)
- `body`: the drafted reply
- `contentType`: `text/plain`

Do NOT include a subject — it will be auto-derived as "Re: [original subject]" from the thread.

Do NOT send. Drafts only.

### Step 6 — Report to Chris

After processing all emails, output a summary table:

| # | From | Subject | Project | Draft Status | Needs Input? |
|---|---|---|---|---|---|
| 1 | sender@example.com | Re: Survey quote | Property Line Adjustment | Saved | No |
| 2 | client2@example.com | Drainage question | Hydraulic Model | Saved | Yes — see draft |

Then list any questions Chris needs to answer before the drafts are send-ready.

---

## Prompting Protocol

If you need information from Chris to complete a draft, ask it here — not inside the draft. Keep it short:

> **Draft for [Subject] needs:**
> - What is the current estimated completion date for the property line adjustment?
> - Did you already send the fee proposal to this client?

After Chris answers, go back and update the draft via `gmail_create_draft` (creating a new draft replaces the old one — note the new draftId).

---

## Project Keyword Index

Project-specific keywords are in `context/project-index.md`. Load that file in Step 1 — do not hardcode keywords here.

---

## Output Format Rules

Follow `.claude/rules/communication-style.md`:
- No dashes in prose
- Short over long
- Tables for structured data
- No emojis in placeholders or notes — only in actual email text where appropriate

---

## Gmail Account

Connected and verified: **cjanigo@topexeng-ls.com**. Drafts are saved directly to this inbox. No additional setup needed.

---

## When to Ask Before Drafting

Ask Chris first (do not draft) when:
- The email is from an attorney or relates to litigation and the right tone is unclear
- The email is a fee dispute or complaint
- The email requests a commitment that affects a deadline already in the system
- The email is ambiguous about what project it belongs to and context could change the response significantly
