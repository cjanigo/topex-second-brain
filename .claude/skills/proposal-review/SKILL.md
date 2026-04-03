# Proposal Review Skill

## What This Is

Monthly review of all proposals in `proposals/`. Marks expired proposals (no project created within 30 days), then analyzes all lost/expired proposals to identify patterns and suggest improvements for future proposals.

Run this once a month — or whenever you want a read on your win rate and proposal quality.

---

## How to Invoke

```
/proposal-review
```

---

## Execution Protocol

### Step 1 — Load All Proposals

Read `proposals/README.md` to get the full proposal table. For each proposal, read its `README.md` from `proposals/[folder]/README.md`.

Collect for each:
- Proposal ID and folder name
- Client name
- Service type
- Fee proposed
- Date sent
- Expiry date (sent + 30 days)
- Current status
- Linked project (if Won)
- Win/Loss Notes

---

### Step 2 — Mark Expired Proposals

For each proposal with **Status: Pending**:

1. Compare today's date against the expiry date
2. If today > expiry date:
   - Check `projects/README.md` (if it exists) or scan `projects/` folder for any project linked to this proposal
   - If no project exists: update the proposal's README.md status from `Pending` to `Expired` and add a Win/Loss Notes entry: `"No response within 30 days. Assumed not selected."`
   - If a project exists but the proposal wasn't updated: update status to `Won` and add the project link
3. Update `proposals/README.md` table to reflect new statuses

**Do not delete any proposals.** Expired proposals are kept for analysis.

---

### Step 3 — Analyze Lost and Expired Proposals

Collect all proposals with Status: **Lost** or **Expired**.

Analyze across these dimensions:

**Win Rate**
```
Won: N / Total: N  (XX%)
Lost: N | Expired: N | Pending: N
```

**By Service Type**
| Service Type | Sent | Won | Lost/Expired | Win Rate |
|---|---|---|---|---|
| Topo + Boundary Survey | N | N | N | XX% |
| Boundary Survey | N | N | N | XX% |
| Civil Engineering | N | N | N | XX% |
| Expert Witness | N | N | N | XX% |

**By Fee Range**
| Fee Range | Sent | Won | Win Rate |
|---|---|---|---|
| Under $2,000 | N | N | XX% |
| $2,000 - $5,000 | N | N | XX% |
| $5,000 - $15,000 | N | N | XX% |
| Over $15,000 | N | N | XX% |

**By Outcome Reason** (from Win/Loss Notes)
Summarize known reasons for losses: price, timeline, no response, competitor selected, etc.

**Time to Sign** (for Won proposals)
Average days from sent to signed for Won proposals.

**Response Rate**
Proposals where client responded (Won + Lost with known reason) vs. Expired (no response).

---

### Step 4 — Generate Recommendations

Based on the analysis, generate 3 to 5 specific, actionable recommendations. Examples:

- "3 of 4 expired proposals were for boundary-only surveys under $1,500. Consider whether pricing is competitive for small jobs or if these clients need a follow-up call."
- "Average time to sign for Won proposals is 3 days — fast turnaround is working. Keep responding to RFQs same day."
- "2 proposals listed no specific schedule — clients may need a concrete start date to commit. Add a tentative field week to every proposal."
- "Expert witness proposals have a 0% close rate when sent to opposing counsel. Stop writing those and redirect to direct client engagement."

Keep recommendations specific and tied to actual data from the proposals. Do not generate generic business advice.

---

### Step 5 — Output Report

Print a summary report to the screen. Do not save it to a file — this is for review only.

```
Proposal Review — [Month YYYY]
Run date: [YYYY-MM-DD]

STATUS UPDATE
  Marked Expired: N proposals
  Marked Won (project found): N proposals
  Still Pending: N proposals

WIN RATE
  Won: N / Total sent: N (XX%)
  Lost: N | Expired: N

BY SERVICE TYPE
  [table]

BY FEE RANGE
  [table]

AVERAGE TIME TO SIGN (Won): N days

RECOMMENDATIONS
  1. [specific recommendation]
  2. [specific recommendation]
  3. [specific recommendation]
```

---

## Scheduling This Skill

To run automatically on the first of each month, use:

```
/schedule
```

Then tell the scheduler: "Run `/proposal-review` on the first of each month."

---

## Notes

- Proposals are never deleted. Expired = not won, but the data stays for trend analysis.
- Win/Loss Notes in each proposal README are the most valuable input. Update them when you hear back from a client.
- As the proposal library grows (12+ proposals), the pattern analysis becomes more reliable.
- This skill only reads and updates `proposals/`. It does not touch `projects/`.
