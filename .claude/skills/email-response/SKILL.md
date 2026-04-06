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
- All project READMEs in `projects/` — for keyword matching and context

Build a mental map of active projects and their keywords. Always load project READMEs from `projects/` first — deadlines and client details live there and should inform every draft. Do not rely on any hardcoded keyword or deadline list here; read the READMEs at runtime every time.

### Step 2 — Fetch Unread Emails

Use `gmail_search_messages` to find emails:
- Default query: `is:unread in:inbox`
- Apply any user-provided search filter on top

Fetch up to 20 at a time. For each result:
1. Use `gmail_read_message` to get the message content and thread ID.
2. If the message has a `threadId` (i.e., it is part of a thread with prior messages), also call `gmail_read_thread` with that thread ID to get the full conversation in order. Use this context when drafting — prior messages often contain commitments, questions, or decisions that should inform the reply.

### Step 3 — Triage Each Email

For each email, determine:

1. **RFQ check** — Before anything else, check if this is a request for quote or proposal. See RFQ Detection below.
2. **Project match** — Does the subject, body, or sender match any active project keywords? If yes, note which project(s).
3. **Action required** — What does the sender actually want? (answer a question, confirm a schedule, review a document, etc.)
4. **Information gaps** — What would Chris need to know to answer fully? If gaps exist, list them — ask Chris before drafting, or flag in the draft.
5. **Urgency** — Does this relate to a deadline within 7 days?

#### RFQ Detection

Flag an email as an RFQ if any of these appear in the subject or body:

**High-confidence signals:** "quote", "proposal", "RFQ", "RFP", "scope of work", "what would you charge", "how much", "price", "cost estimate", "fee", "are you available", "do you do", "can you help with"

**Supporting signals (combine with the above):** new sender not in any active project, mentions a parcel, address, tax lot, property, survey, or engineering need

**If flagged as RFQ:**
- Do NOT draft a standard reply email
- Instead, execute the proposal-building protocol below inline
- Note in the Step 6 summary table: "RFQ — proposal draft built and saved to proposals/"

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

**C. Estimate fee** (always flag as `[REVIEW FEE — based on limited info]`):

Survey (topo + boundary):
| Site Size / Complexity | Fee Range |
|---|---|
| Small residential (<1 acre, single tax lot, no water features) | $1,800 to $2,500 |
| Standard residential (1 to 5 acres, or two tax lots) | $2,500 to $3,500 |
| Complex (multiple tax lots, water feature, steep terrain, or OHWM needed) | $3,500 to $5,500 |
| Large or commercial | $5,000+ (flag for Chris to price manually) |

Survey (boundary only, ROS, easements):
| Scope | Fee Range |
|---|---|
| Simple boundary stake (1 to 4 corners) | $1,200 to $2,000 |
| Legal description + exhibit | $800 to $1,500 |
| Record of survey | $2,500 to $4,000 |

Engineering:
| Scope | Fee Range |
|---|---|
| Small report or analysis | $1,500 to $4,000 |
| Design plans (minor) | $3,000 to $8,000 |
| Hydraulic model | $4,000 to $12,000 |
| City engineering (monthly) | $2,000 to $5,000/month |

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

This index grows over time. Update when new projects are added to `projects/`.

| Keyword | Project |
|---|---|
| expert witness, testimony, deposition, case | Expert Witness Report |
| property line, boundary, PLA, parcel, lot line | Property Line Adjustment |
| hydraulic, EPANET, flood, drainage, stormwater, flow, culvert | Hydraulic Model and Map |
| survey, monument, plat, record of survey, boundary, GPS | General Surveying |
| water right, DOE, adjudication, certificate, permit to appropriate | Water Rights |
| city engineer, municipal, right-of-way, ROW, permit | City Engineering |
| erosion, sediment, CESCL, SWPPP, grading | Erosion Control |
| drone, UAS, aerial, LiDAR, point cloud | Drone / UAS |

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
