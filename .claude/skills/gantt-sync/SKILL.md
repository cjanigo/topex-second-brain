# Gantt Sync Skill

## What This Is

Syncs Chris Janigo's GanttProject work schedule to Google Calendar. Reads the `.gan` file,
diffs it against existing calendar events, and creates/updates/deletes as needed.

Safe to run daily — all synced events are tagged with the task UID so duplicates never occur.

---

## How to Invoke

```
/gantt-sync
```

Optional — dry run (report what would change, create nothing):
```
/gantt-sync dry-run
```

---

## Source File

```
C:\Users\cjani\Documents\GanttProject\ongoing work schedule.gan
```

If the file path has changed or is unreachable, stop and tell Chris immediately.

---

## Execution Protocol

### Step 1 — Parse the .gan File

Read the file and extract all **leaf tasks** (tasks with no child `<task>` elements) with start dates >= today.

For each leaf task, collect:

| Field | XML Source | Notes |
|---|---|---|
| uid | `uid` attribute | Stable unique ID — used for deduplication |
| name | `name` attribute | Event title |
| start | `start` attribute | YYYY-MM-DD format |
| duration | `duration` attribute | Working days (Mon-Fri) |
| parent_name | Parent `<task>` `name` attribute | Prepended to title for context |
| complete | `complete` attribute | Skip tasks where complete = 100 |

**Skip these tasks:**
- `complete="100"` — already done
- Tasks with no `name` or name starting with `task_` — placeholder tasks
- Tasks with start dates before today

**Working-day end date calculation:**

Duration is in Mon-Fri working days. To get the Google Calendar end date (exclusive):
- Start from the task's start date
- Count forward N working days (skip Sat/Sun)
- The end date = last working day + 1 calendar day

Example: start=2026-04-02, duration=3 → working days: Apr 2 (Thu), Apr 3 (Fri), Apr 6 (Mon) → end = 2026-04-07

**Event title format:**
```
[Parent Name]: [Task Name]
```
If task has no parent (top-level), use task name only.

**Event description format** (required for deduplication — do not omit):
```
gantt-uid: [uid]
```

### Step 2 — Fetch Existing Synced Events

Use `gcal_list_events` with:
- `q`: `gantt-uid`
- `timeMin`: today's date at 00:00:00
- `timeZone`: `America/Los_Angeles`
- `maxResults`: 250

This returns all previously-synced events from today onward. Build a lookup map: `uid → event`.

Also fetch events from 30 days in the past to catch any recently-past tasks that may have shifted:
- Same query, `timeMin` = 30 days ago, `timeMax` = today

### Step 3 — Diff and Sync

Compare the .gan task list against the calendar event map:

| Situation | Action |
|---|---|
| Task in .gan, no calendar event with matching uid | **Create** event |
| Task in .gan, matching calendar event, same start+end | **Skip** (no change) |
| Task in .gan, matching calendar event, different start or end | **Delete** old event, **Create** new event |
| Calendar event with gantt-uid not found in .gan task list | **Delete** event (task removed or completed) |

Use `gcal_create_event` to create and `gcal_delete_event` to delete. There is no partial update — always delete and recreate when dates change.

**Create event parameters:**
```
summary: [title]
description: "gantt-uid: [uid]"
start: { date: "YYYY-MM-DD" }
end: { date: "YYYY-MM-DD" }  ← exclusive end (last day + 1)
```

No time, no reminders — all-day events only.

### Step 4 — Report

After syncing, output a summary to Chris:

```
Gantt Sync — [date]
Source: ongoing work schedule.gan

Created:  N events
Updated:  N events  (deleted + recreated)
Deleted:  N events
Unchanged: N events

Changes:
+ Newport Frank Wade: Drafting Plans  (Apr 2 - Apr 6)
~ 26007 Ramon Sera: Survey  (rescheduled Apr 9 → Apr 14)
- 26005 Kaufman: Report Filing  (task marked complete)
```

If nothing changed: "Calendar is up to date. No changes made."

If dry-run mode: prefix all lines with [DRY RUN] and make no API calls.

---

## Error Handling

| Problem | Response |
|---|---|
| .gan file not found | Stop. Tell Chris the path and ask him to verify. |
| .gan file is malformed XML | Stop. Show the parse error. |
| Calendar API error on create/delete | Log the error, continue with remaining tasks, report failures at the end. |
| More than 50 changes detected | Pause and confirm with Chris before proceeding — large diffs may indicate a file swap or data issue. |

---

## Calendar Account

Primary calendar: `cjanigo@topexeng-ls.com`
Timezone: `America/Los_Angeles`

---

## Scheduling This Skill

To run automatically every morning, use:

```
/schedule
```

Then tell the scheduler: "Run `/gantt-sync` every weekday morning at 7am Pacific."

The scheduled agent will run `/gantt-sync` each morning, sync the calendar, and log results.
