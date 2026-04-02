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

Build a mental map of active projects and their keywords. Always load project READMEs from `projects/` first — deadlines and client details live there and should inform every draft.

| Project | Keywords to Match | Deadline |
|---|---|---|
| Expert Witness Report | expert witness, report, testimony, case, deposition, legal | 2026-04-01 (TODAY) |
| Property Line Adjustment | property line, boundary, adjustment, parcel, lot line, PLA | 2026-04-04 |
| Hydraulic Model and Map | hydraulic, model, EPANET, map, flood, flow, drainage, stormwater, culvert | 2026-04-14 |

This table is a starting snapshot. Always re-read `projects/*/README.md` at runtime to get current deadlines, client names, parcel numbers, and any notes added since this file was last updated.

### Step 2 — Fetch Unread Emails

Use `gmail_search_messages` to find emails:
- Default query: `is:unread in:inbox`
- Apply any user-provided search filter on top

Fetch up to 20 at a time. For each result, use `gmail_read_message` to get the full content.

### Step 3 — Triage Each Email

For each email, determine:

1. **Project match** — Does the subject, body, or sender match any active project keywords? If yes, note which project(s).
2. **Action required** — What does the sender actually want? (answer a question, confirm a schedule, review a document, etc.)
3. **Information gaps** — What would Chris need to know to answer fully? If gaps exist, list them — ask Chris before drafting, or flag in the draft.
4. **Urgency** — Does this relate to a deadline within 7 days?

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
