# Rule: Project Update → Schedule Sync

**Whenever a project README is created or updated**, also:

1. **Update `schedule/tasks.md`** — add any new meetings, deadlines, or time-sensitive tasks as timed entries (timed events go here, not in the .gan file).
2. **Run `/gantt-sync`** — syncs both the .gan file and tasks.md to Google Calendar.

## What counts as a trigger

- Creating a new project README
- Updating deliverable status, schedule, or meeting dates in any project README
- Adding or changing milestones in any project README

## What to add to tasks.md

| Item Type | Add to tasks.md? | Notes |
|---|---|---|
| Meeting with a specific time | Yes | Include Zoom link or location in the Task field |
| Deadline (no specific time) | Yes | Use 08:00 start, 30m duration as a morning reminder |
| Multi-day work block | No | Add to the .gan file instead |
| Recurring milestone (e.g., monthly invoice) | No | Already handled by gantt-sync billing milestones |

## Format reminder

```
| | YYYY-MM-DD | HH:MM | Xh or Xm | Task description (Zoom/location info) | Project |
```

Leave the uid column blank — gantt-sync fills it in automatically.
