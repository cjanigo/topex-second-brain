# Scope Sync Skill

## What This Is

Reads recent project emails, compares them against the project's `## Scope Summary`, and proposes updates to the project README. Specifically:

- Updates `## Deliverables` checkboxes for confirmed completions
- Appends entries to `## Change Log` for clarifications and absorbed work
- Appends entries to `## Scope Flags` for potential scope creep
- Flags items that warrant a formal scope addendum (new deliverables, additional field work, material extra effort)

**Nothing is written without Chris's approval.** The skill proposes a diff; Chris confirms before any file is changed.

---

## How to Invoke

```
/scope-sync [project number or keyword]
```

Examples:
- `/scope-sync 26003` — check one project by number
- `/scope-sync property line` — check by keyword
- `/scope-sync` — check all active projects (slower, use sparingly)

---

## Execution Protocol

### Step 1 — Load the Project

Read the target `projects/*/README.md`. Extract:

| Field | Where |
|---|---|
| Project name and number | H1 heading |
| Status | `**Status:**` — skip if `Archived` or `Complete` |
| Client name and email | Header fields or contacts table |
| Scope Summary | `## Scope Summary` bullets — this is the baseline |
| Deliverables | `## Deliverables` checklist |
| Existing Change Log | `## Change Log` table |
| Existing Scope Flags | `## Scope Flags` table |

If no `## Scope Summary` exists, note it and stop. Tell Chris the README needs a Scope Summary before scope-sync can run for this project.

---

### Step 2 — Fetch Recent Emails

Search both inbox and sent mail for emails related to this project. Use `gmail_search_messages` with two queries:

**Inbox (client messages):**
```
from:[client email] newer_than:60d
```
Also try broader keyword search if client email is unknown:
```
[project number OR client name OR key project term] newer_than:60d
```

**Sent mail:**
```
in:sent to:[client email] newer_than:60d
```

Fetch up to 15 results per query. For each result, use `gmail_read_message` to get subject, date, body, and attachment names. For threads with multiple replies, use `gmail_read_thread` to get the full conversation in order.

Deduplicate by thread ID — read each thread once.

---

### Step 3 — Extract Events from Each Thread

For each thread, identify discrete events. An event is something that happened related to scope, deliverables, or project status.

Read each message in the thread chronologically. For each message, note:
- Who sent it (client vs. Chris)
- What was attached (if anything)
- What was requested, confirmed, or clarified

Extract these event types:

| Event Type | What to Look For |
|---|---|
| Deliverable sent | Chris's email has attachment matching a deliverable name or keyword |
| Client confirmation | Client reply says received, looks good, approved, thank you |
| Scope clarification | Either party clarifies what is/isn't included — no change in work |
| New request | Client asks for something new ("can you also", "we also need", "one more thing") |
| Revision request | Client asks for changes to something already delivered |
| Question about timeline | Not a scope event — skip |
| Admin / scheduling | Not a scope event — skip |

Build a list of all events found across all threads.

---

### Step 4 — Classify Each Event

Compare each event against the `## Scope Summary` bullets and existing `## Deliverables` list.

**Classification rules:**

**DELIVERED**
- Chris sent an email with an attachment
- The attachment matches a deliverable in the README (by name or keyword)
- Action: propose checking off that deliverable

**CLARIFICATION**
- Either party clarified what was included or excluded
- The clarification does not add work — it resolves ambiguity in existing scope
- Action: propose a Change Log entry, type `CLARIFICATION`

**ABSORBED** (out-of-scope, absorbed into project cost)
Flag as absorbed if ALL of the following are true:
- The request is not in the Scope Summary
- Estimated effort is small (one email answer, minor map edit, small revision)
- There is no explicit "this is new work" framing
- Absorbing it does not set a bad precedent for future requests of the same type
- Action: propose a Change Log entry, type `ABSORBED`

**FLAGGED** (potential scope creep — warrants addendum consideration)
Flag as potential scope creep if ANY of the following are true:
- Request adds a new deliverable not in the Scope Summary
- Request requires additional field work or site visits
- Request adds additional parcels, properties, or areas
- Request changes the deliverable format substantially (e.g., 8.5x11 to full-size sheets)
- Request implies multiple revision rounds (second or third round of the same deliverable)
- Request involves a new permit, application, or coordination with a new agency
- Client explicitly acknowledges the request is extra ("I know this is more work")
- Effort is medium or large (estimated > 2 hours of additional work)
- Action: propose a Scope Flags entry, type `FLAGGED`, and include a plain-language description and rough effort estimate (small / medium / large)

**Addendum recommended** — elevate flag to addendum recommendation if:
- The request is clearly a new deliverable with a defined output
- Estimated effort is large (half day or more)
- Or the request is similar in scope to a task already in the budget

---

### Step 5 — Present Proposed Changes

Do NOT write anything yet. Present a summary to Chris first:

```
Scope Sync — [Project Name] — [date]

Emails reviewed: [N threads, date range]

Proposed Changes:

DELIVERABLES
- [x] Legal description for Tax Lot 200 — confirmed delivered 2026-03-28 (email: "RE: PLA Docs")

CHANGE LOG (new entries)
- 2026-03-22 | CLARIFICATION | Client confirmed title reports are their responsibility, not Topex | "RE: PLA Update"
- 2026-03-30 | ABSORBED | Minor revision to boundary exhibit — corrected label typo | "RE: Exhibit Fix"

SCOPE FLAGS (new entries)
- 2026-03-29 | Effort: medium | FLAGGED — Client asked for a drainage analysis of the adjusted parcels. Not in SOW. | "RE: Grading"
  → Addendum recommended: this is a separate engineering task with its own deliverable.

Nothing written yet. Reply "looks good" to apply all changes, or tell me which items to adjust or skip.
```

Use plain language. No jargon. Keep it short enough to skim in 30 seconds.

---

### Step 6 — Apply Approved Changes

After Chris confirms (any of: "looks good", "do it", "apply", "yes"):

1. **Deliverables:** Check off confirmed items in `## Deliverables` (change `- [ ]` to `- [x]`)

2. **Change Log:** Append new rows to the `## Change Log` table. Format:
   ```
   | YYYY-MM-DD | TYPE | Description | Email subject |
   ```
   Append only — never edit existing rows.

3. **Scope Flags:** Append new rows to the `## Scope Flags` table. Format:
   ```
   | YYYY-MM-DD | Description | small/medium/large | Pending |
   ```
   New flags always start as `Pending`.

If Chris says to skip or adjust specific items, apply only the approved ones.

---

## Classification Heuristics — Quick Reference

| Signal | Classification |
|---|---|
| Attachment sent matching deliverable | DELIVERED |
| "Confirmed received", "looks good", "approved" | Confirm DELIVERED |
| "Just to clarify", "as we discussed", no new work | CLARIFICATION |
| Minor typo fix, one label change, small email Q&A | ABSORBED |
| "Can you also add...", "we also need..." | FLAGGED (evaluate effort) |
| Second or third revision of same deliverable | FLAGGED |
| Additional parcel, property, or area added | FLAGGED (addendum likely) |
| New agency, permit, or coordination layer | FLAGGED (addendum likely) |
| "I know this is extra work" | FLAGGED (addendum) |

When in doubt, flag it. Chris can always dismiss a flag. Missing a scope creep item costs money.

---

## Scope Summary Requirement

This skill depends on a `## Scope Summary` section in the project README. If it's missing:

1. Offer to generate one from the SOW tasks listed in the README
2. Ask Chris to confirm it before running the full sync
3. The generated summary should be 4 to 7 plain-language bullets describing what was promised

---

## Gmail Account

Connected: **cjanigo@topexeng-ls.com**

Chris's outgoing address is `cjanigo@topexeng-ls.com`. Use this to distinguish Chris's messages from client replies in thread analysis.

---

## Updating the CLAUDE.md Skills Table

After this skill is built and working, add it to the Skills table in `CLAUDE.md`:

| Skill | Invoke | What It Does |
|---|---|---|
| scope-sync | `/scope-sync [project]` | Reads recent emails, classifies scope changes, proposes README updates (deliverables, change log, scope flags) |
