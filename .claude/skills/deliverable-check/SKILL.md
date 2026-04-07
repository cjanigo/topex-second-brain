---
name: deliverable-check
description: Scan sent email to determine which project deliverables have been submitted and whether any have open follow-up questions from clients.
---

# Deliverable Check Skill

## What This Is

Scans sent email to determine whether project deliverables have been sent to clients, and whether any delivered items are waiting on follow-up questions. Uses Gmail sent mail and thread analysis to infer completion status without requiring Chris to manually update anything.

**Completion logic:**
- **Delivered** — Chris sent an email with an attachment matching the deliverable, and no reply in that thread contains questions
- **Pending Follow-up** — Chris sent a matching email with attachment, but a client reply contains questions (the item is not closed)
- **Not Yet Sent** — No matching sent email with an attachment found

---

## How to Invoke

```
/deliverable-check
```

Optional — check a single project:
```
/deliverable-check [project name or keyword]
```

Examples:
- `/deliverable-check` — check all active projects
- `/deliverable-check hydraulic` — check only the hydraulic model project
- `/deliverable-check expert witness` — check the expert witness project

---

## Execution Protocol

### Step 1 — Load Active Projects

Read all `projects/*/README.md` files. For each project, extract:

| Field | Where to Find It |
|---|---|
| Project name | H1 heading |
| Status | `**Status:**` field — skip if `Archived` or `Complete` |
| Client / recipient | Contacts table or notes |
| Deliverables | Scope of Work section — extract tangible outputs (reports, maps, models, plats, plans, drawings, etc.) |
| Keywords | Project name, client name, key technical terms from scope |

**Extracting deliverables from scope:**

Look for noun phrases describing outputs. Examples of what counts as a deliverable:
- Reports (expert witness report, preliminary engineering report, draft PER, final report)
- Maps or GIS products (GIS base map, water system map, system mapping)
- Models (EPANET model, water model, hydraulic model)
- Survey documents (record of survey, plat, boundary survey, legal description)
- Drawings or plans (site layout, schematic, engineered plans)
- Declarations or affidavits
- Cost estimates
- Letters or memos transmitted to a client

If the README has an explicit `## Deliverables` section, prefer that over inferring from scope. If no explicit section exists, infer from the Scope of Work tasks.

Build a deliverable list per project. Each deliverable needs:
- A short name (e.g., "GIS base map", "Expert witness report")
- Search keywords to find it in email (e.g., "GIS map", "base map", "system map")

---

### Step 2 — Search Sent Mail for Each Deliverable

For each project, search sent mail for emails with attachments that could represent a deliverable submission.

Use `gmail_search_messages` with:
```
in:sent has:attachment [project keywords]
```

Build the query using the project keywords from `context/project-index.md`. Combine the most distinctive keywords for the project into an `in:sent has:attachment (keyword OR keyword)` query.

Fetch up to 10 results per project. For each result, use `gmail_read_message` to get:
- Subject
- Date sent
- Recipients (To, Cc)
- Body snippet
- Attachment names

Match each sent email to a specific deliverable by comparing the subject, body, and attachment names against your deliverable keyword list.

---

### Step 3 — Check Each Thread for Follow-Up Questions

For every sent email that matches a deliverable, use `gmail_read_thread` with the thread ID to get the full conversation.

Scan all replies that came **after** the matching sent email and are **not from Chris** (i.e., not from `cjanigo@topexeng-ls.com`).

A reply counts as a **follow-up question** if it contains any of:
- A question mark (`?`)
- Phrases like: "can you", "could you", "please clarify", "question", "what about", "I have a", "need to know", "not sure", "confused"

If a follow-up question reply is found → status = **Pending Follow-up**
If no such reply → status = **Delivered**

If no matching sent email was found at all → status = **Not Yet Sent**

---

### Step 4 — Report

Output a status table for each active project with deliverables found:

```
Deliverable Status — [date]

Project: Expert Witness Report
| Deliverable              | Status              | Sent Date   | Notes                          |
|--------------------------|---------------------|-------------|--------------------------------|
| Supplemental report      | Delivered           | 2026-03-28  | No open questions              |
| Final expert report      | Not Yet Sent        |             |                                |

Project: Hydraulic Model and Map
| Deliverable              | Status              | Sent Date   | Notes                          |
|--------------------------|---------------------|-------------|--------------------------------|
| GIS base map             | Pending Follow-up   | 2026-03-25  | Reply from Paul Newman 3/27 has questions |
| EPANET model             | Not Yet Sent        |             |                                |

Project: Property Line Adjustment
| Deliverable              | Status              | Sent Date   | Notes                          |
|--------------------------|---------------------|-------------|--------------------------------|
| Boundary survey / plat   | Not Yet Sent        |             |                                |
```

After the table, list any **Pending Follow-up** items with the question text from the client's reply so Chris knows what needs to be addressed:

```
Pending Follow-up Details:

GIS base map — Paul Newman replied 2026-03-27:
  "[quote the relevant question or sentence from the reply]"
```

---

### Step 5 — Offer to Update Project READMEs

After reporting, ask Chris:

> Want me to update the project READMEs to reflect these statuses? I can add a `## Deliverable Status` section to each project file with the current state.

If Chris says yes, append (or update) a `## Deliverable Status` section to each relevant `projects/*/README.md`:

```markdown
## Deliverable Status

_Last checked: YYYY-MM-DD_

| Deliverable           | Status            | Sent Date  | Notes                  |
|-----------------------|-------------------|------------|------------------------|
| GIS base map          | Pending Follow-up | 2026-03-25 | Open question from OWD |
| EPANET model          | Not Yet Sent      |            |                        |
```

Do not overwrite any other sections. Only add or replace the `## Deliverable Status` block.

---

### Step 6 — Offer to Add Reply Tasks to schedule/tasks.md

If any deliverables have **Pending Follow-up** status, ask:

> Want me to add reply tasks to schedule/tasks.md for any of these?

List the pending items and let Chris choose. If he says yes (to all or specific items), append a row to `schedule/tasks.md` for each selected item:

| Field | Value |
|---|---|
| uid | _(leave blank — gantt-sync will fill in)_ |
| Date | Today's date (YYYY-MM-DD) |
| Start | _(leave blank — Chris sets the time)_ |
| Duration | 1h |
| Task | Reply to [client name] re: [deliverable name] |
| Project | [project number] |

If Start is left blank, gantt-sync will skip creating a calendar event for that row until Chris fills it in.

Do not add tasks for **Not Yet Sent** deliverables — those are multi-day project work that belongs in GanttProject.

---

## Deliverable Inference Guide

When reading scope sections, use this to identify what counts as a deliverable:

| Scope language | Likely deliverable |
|---|---|
| "Prepare report", "final report", "draft report" | Report document |
| "Create GIS", "digitize maps", "base map", "system map" | Map / GIS file |
| "Build model", "calibrate model", "computer model" | Model file or report |
| "Record of survey", "survey plat", "boundary survey" | Survey document |
| "Schematic", "site layout", "drawings", "plans" | Drawing set |
| "Cost estimate" | Estimate document |
| "Declaration", "affidavit" | Legal document |
| "Kick-off meeting" | Not a deliverable — skip |
| "Coordination", "project management" | Not a deliverable — skip |
| "Site visit", "data collection" | Not a deliverable — skip |

---

## Handling Ambiguity

| Situation | Response |
|---|---|
| Sent email found but no attachment | Skip — not a deliverable submission |
| Multiple sent emails match the same deliverable | Use the most recent one |
| Thread has a reply from Chris after the client question | The follow-up question may be resolved — note it but mark as "Likely Resolved, verify" |
| Can't determine if a reply contains a question | Flag it as "Review needed" and show Chris the reply excerpt |
| Project has no clear deliverables in scope | Note "No deliverables identified — check README" and skip |

---

## Gmail Account

Connected: **cjanigo@topexeng-ls.com**

Sent mail is accessed via `gmail_search_messages` with `in:sent`. Chris's outgoing address is `cjanigo@topexeng-ls.com` — use this to distinguish Chris's replies from client replies when reading threads.

---

## Notes on Project README Format

If a project README has an explicit `## Deliverables` section listing items, the skill will use that list directly. To make tracking more reliable over time, consider adding this section to new project READMEs:

```markdown
## Deliverables

- [ ] [Deliverable name] — [brief description]
- [ ] [Deliverable name] — [brief description]
```

The skill will also read checked items (`- [x]`) and treat them as manually confirmed complete, skipping the email search for those.