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
- `context/project-index.md` — keyword index for matching emails to projects in Step 2

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