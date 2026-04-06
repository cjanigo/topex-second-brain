---
name: morning-coffee
description: Use when someone asks for a morning briefing, daily summary, day overview, morning coffee report, or daily digest. Summarizes emails received, drafted responses, and project status, then saves a briefing as a Gmail draft addressed to Chris.
disable-model-invocation: true
---

# Morning Coffee Skill

## What This Does

Runs a full morning briefing for Chris Janigo at Topex Inc. Each morning:

1. Summarizes emails received in the last 24 hours
2. Lists any auto-drafted replies sitting in Gmail drafts
3. Reports status on all active projects (from `projects/` READMEs)
4. Calls out today's deadlines and urgent items
5. Saves the full briefing as a Gmail draft to himself at cjanigo@topexeng-ls.com

---

## How to Invoke

```
/morning-coffee
```

No arguments needed. Run manually or via daily schedule.

---

## Execution Protocol

### Step 0 — Find a Good News Story

Use WebSearch to find one piece of good news from the last 24 hours. Search for something like: `good news today [date]` or `positive news [date]`. Pick one short, feel-good story -- science, wildlife, community, human interest, or anything uplifting. Not politics. Not business. Capture:
- Headline
- One sentence summary
- Source name

This goes at the top of the briefing.

### Step 1 — Load Project Context

Read all project READMEs before doing anything else. These are the source of truth for deadlines, deliverables, and status.

Glob pattern: `projects/*/README.md`

For each project found, extract:
- Project name
- Client name
- Current status (Active / On Hold / Complete)
- Overall project deadline
- Deliverables — parse every checkbox line (`- [ ]` or `- [x]`) and capture:
  - Deliverable description
  - Due date (from inline `(due: ...)` text)
  - Status: Pending (`- [ ]`) or Done (`- [x]`)
- Any blockers or open items noted in the README

Also read:
- `context/current-priorities.md` — active deadline list
- `context/me.md` — Chris's credentials and role (for email signature)

### Step 2 — Fetch Recent Emails

Use `gmail_search_messages` with query: `in:inbox after:YYYY/MM/DD`

Where the date is yesterday (24 hours ago). Fetch up to 30 results.

For each message, use `gmail_read_message` to get:
- From (sender name + email)
- Subject
- Snippet or first paragraph of body
- Whether it's been read

Build a triage list:
| From | Subject | Read? | Project Match | Action Needed |
|---|---|---|---|---|

Match each email to an active project using keywords from the project READMEs. Use the keyword index from the email-response skill as a reference:

| Keyword | Project |
|---|---|
| expert witness, testimony, deposition, case, legal | Expert Witness |
| property line, boundary, PLA, parcel, lot line | Property Line Adjustment |
| hydraulic, EPANET, flood, drainage, stormwater, flow | Hydraulic Model |
| survey, monument, plat, record of survey, GPS | General Surveying |
| water right, DOE, adjudication, certificate | Water Rights |
| city engineer, municipal, ROW, permit | City Engineering |
| erosion, sediment, CESCL, SWPPP, grading | Erosion Control |
| drone, UAS, aerial, LiDAR, point cloud | Drone / UAS |

### Step 3 — Check Gmail Drafts

Use `gmail_list_drafts` to find any drafts that exist. For each draft:
- Note the subject and recipient
- Flag if it looks like an auto-drafted reply (Re: prefix, sent to a client)
- Note whether it appears send-ready or has placeholders like `[INSERT: ...]`

### Step 4 — Check Google Calendar

Use `gcal_list_events` to get today's events and anything scheduled in the next 3 days.

Look for:
- Scheduled calls or meetings
- Field work
- Internal deadlines

### Step 5 — Compose the Briefing

Format the briefing as plain text using the template below. Keep it short and scannable.

---

**TEMPLATE:**

```
Morning Coffee — [Weekday], [Month Day, Year]

GOOD NEWS
[Headline] -- [Source]
[One sentence summary]

TODAY'S FOCUS
[1-3 sentence plain-English summary of what matters most today. Lead with the hardest deadline.]

DELIVERABLES
[Table: Project | Deliverable | Due Date | Days Out | Status]
Show all pending deliverables first (sorted by due date), then done items. Mark done rows with a checkmark. If a due date is TBD, list last.

EMAILS (last 24 hours)
[Table: From | Subject | Project | Action?]
[If no emails: "No new emails in the last 24 hours."]

DRAFTS READY TO SEND
[Bulleted list: "Re: [Subject] → [Recipient]" — flag any with [INSERT] placeholders]
[If none: "No drafts pending."]

CALENDAR (today + next 3 days)
[Table: Date | Time | Event]
[If nothing: "No events scheduled."]

PROJECT STATUS
[Table: Project | Client | Next Pending Deliverable | Due Date | Overall Deadline]
Pull from the README data loaded in Step 1. Show only active projects. Next Pending Deliverable = first unchecked item by due date.

---
JOKE OF THE DAY
[One short, clean joke. Engineering, surveying, or dad-joke style preferred. Keep it work-appropriate.]

---
Chris Janigo, PE, PLS | Topex Inc.
```

---

Rules for the briefing:
- No dashes in prose
- Short over long — if there is nothing to report in a section, say so in one line
- Tables for all structured data
- No em dashes, no en dashes
- Pacific time for all times

### Step 6 — Write the Joke

Pick one short, clean joke to close the briefing. Engineering, surveying, construction, or dad-joke style preferred. Generate it fresh each day -- don't reuse the same joke.

### Step 7 — Save as Gmail Draft

Use `gmail_create_draft` with:
- `to`: `cjanigo@topexeng-ls.com`
- `subject`: `Morning Coffee: [Weekday, Month Day]`
- `body`: the full briefing text (plain text)
- `contentType`: `text/plain`

Do NOT send. Save as draft only. Chris will see it in Gmail drafts when he opens his inbox.

### Step 8 — Confirm

Output a single line to confirm completion:

> Morning Coffee briefing saved to Gmail drafts for [date]. Open Gmail to review.

---

## Notes

- Gmail MCP supports draft creation only — this skill cannot send emails directly. The draft is addressed to cjanigo@topexeng-ls.com and will appear in Gmail drafts.
- If no emails arrived in the last 24 hours, say so — don't skip the section.
- If `projects/` has no READMEs, flag it and skip the deliverables and project status sections.
- Deliverable status is read directly from README checkboxes: `- [ ]` = Pending, `- [x]` = Done. Do not infer status from anything else.
- If all deliverables on a project are checked done, still show the project in PROJECT STATUS but mark it complete.
- If Google Calendar returns no events, say so — don't skip the calendar section.
- Do not editorialize about project health. Report facts: status, deadline, next action.
- The briefing is for Chris only — do not use client-facing tone.