---
name: draft-invoice
description: Scan sent email to estimate billable hours for hourly/on-call projects, format a draft invoice matching Topex Inc. format, and save to Gmail as a draft. Chris reviews and sends manually. Run on the 24th of each month.
---

# Draft Invoice Skill

## What This Is

Generates a draft invoice for hourly and on-call projects by scanning sent email for billable activity during a billing period. Time estimates are based on the nature and content of each email -- since every sent email to a client represents work done to gather the information in it.

Chris reviews and sends invoices himself. This skill only produces a draft.

**Applies to:** Hourly, T&M, and on-call contracts only. Lump sum and fixed-fee projects are excluded.

**Output:** A formatted invoice draft saved as a Gmail draft to cjanigo@topexeng-ls.com for review.

---

## How to Invoke

```
/draft-invoice
```

Optional -- target a specific project or period:
```
/draft-invoice [project name or client]
/draft-invoice [YYYY-MM]
/draft-invoice [project] [YYYY-MM]
```

Examples:
- `/draft-invoice` -- draft invoices for all hourly projects, last calendar month
- `/draft-invoice sheridan` -- draft invoice for City of Sheridan only
- `/draft-invoice 2026-03` -- draft for March 2026

---

## Execution Protocol

### Step 1 -- Load Hourly Projects

Read all `projects/*/README.md`. For each project, extract:

| Field | Where to Find It |
|---|---|
| Project name | H1 heading |
| Status | `**Status:**` field -- skip if `Archived` or `Complete` |
| Contract type | `**Contract Value:**` field |
| Client name | Contacts table |
| Client email | Contacts table |
| Billing rate | Notes, scope, or payment terms section |

**Identify hourly projects** by scanning the contract value, payment terms, and billing fields:

| Signal | Action |
|---|---|
| Contains "lump sum" or "lump-sum" | Skip -- not hourly |
| Contains "fixed fee" or "fixed-fee" | Skip unless billing field says "based on hours" |
| Contains "hourly", "T&M", "time and material", "on-call", "on call" | Include |
| Payment terms say "invoicing based on hours worked" | Include |
| Contract type is ambiguous | Flag for Chris and skip |

Build a list of hourly projects with: project name, client name, client email(s), billing rate (default $120/hr if not specified), and keywords for email matching.

---

### Step 2 -- Determine Billing Period

Default billing period: the **previous calendar month** (e.g., if today is April 2, the default is March 1 through March 31).

If the user specifies a period (e.g., `2026-03`), use that range instead.

Format dates for Gmail search: `after:YYYY/MM/DD before:YYYY/MM/DD`

---

### Step 3 -- Search Sent Emails per Project

For each hourly project, search sent email for the billing period:

```
in:sent after:YYYY/MM/DD before:YYYY/MM/DD [client email or project keywords]
```

Match by client email address first. If no email address is available, fall back to project name keywords in subject/body.

Fetch up to 20 results per project. For each result, use `gmail_read_message` to get:
- Subject
- Date sent
- Recipients (To, Cc)
- Body (full text)
- Attachment names if any

---

### Step 4 -- Estimate Time Per Email

For each matched sent email, estimate billable hours based on the content and the type of work it represents.

**Core principle:** When Chris sends an email, the clock includes everything it took to write it -- the site visit, the research, the calculation, the call beforehand. The email is the evidence. Estimate accordingly.

| Email Type | Estimated Hours |
|---|---|
| Quick reply, status update, simple coordination | 0.25 |
| Scheduling, forwarding documents, simple questions | 0.25 |
| Research, data review, or calculations required before reply | 0.5 to 1.0 |
| Meeting attendance mentioned in email | Stated duration or estimated meeting length, plus 0.25 if travel noted |
| Site visit, inspection, or field work mentioned | Stated duration or estimate 2.0 to 4.0 depending on complexity |
| Punchlist or inspection walkthrough | 1.5 to 3.0 depending on scope |
| Report or document transmitted as attachment | 1.0 to 3.0 depending on length/complexity signals |
| Travel only (mileage reimbursement) | Flag as separate line item -- not hours |

**Signals to look for in the email body:**

| Signal | Interpretation |
|---|---|
| "meeting", "meeting attendance", "development meeting" | Attendance-based time estimate |
| "walked", "site visit", "inspection", "punchlist" | Field work |
| "reviewed", "calculated", "modeled", "drafted" | Production time |
| "attached", "please find", "enclosed" | Deliverable transmission |
| "quick question", "just a note", "following up" | Minimal effort |
| "call with", "spoke with", "phone call" | Meeting time |
| Explicit time ("spent 2 hours", "all morning") | Use stated time |
| Travel mentioned ("drove to", "mileage", "travel") | Add travel time and/or mileage reimbursement |

Write a one-line justification for each estimate. Chris will review these before sending.

---

### Step 5 -- Group Into Line Items

Group line items by project, sorted by date ascending. Each email becomes one or more line items.

**Standard line item:**

| Field | Content |
|---|---|
| Description (header) | Project name |
| Sub-description | Contract type (e.g., "On-Call Engineering and Land Surveying Support") |
| Person + Date | Chris Janigo -- [Month DD, YYYY] |
| Task | Short plain-English description derived from email subject and body |
| Rate | Billing rate (default $120.00) |
| Qty | Estimated hours (round to nearest 0.25) |
| Line Total | Rate x Qty |

**Mileage/travel line items (if applicable):**

Separate line item at the applicable rate. If the project README specifies a reimbursement rate, use that. Otherwise use the IRS standard mileage rate ($0.70/mile for 2025). If miles are unknown, flag for Chris to fill in.

---

### Step 6 -- Format the Draft Invoice

Format one invoice per client. If a client has multiple hourly projects in the same billing period, combine all line items into a single invoice.

Format per `templates/invoice-draft.txt`. Substitute all `[placeholder]` fields with computed values. Keep the TIME ESTIMATE SUMMARY block at the bottom for Chris's review.

---

### Step 7 -- Save as Gmail Draft

Save the formatted draft as a Gmail draft **to cjanigo@topexeng-ls.com** using `gmail_create_draft`:

- **To:** cjanigo@topexeng-ls.com
- **Subject:** DRAFT INVOICE -- [Client/Organization] -- [Month YYYY]
- **Body:** Full formatted invoice + time estimate summary
- **contentType:** text/plain

One draft per client. Do not combine multiple clients into one draft. Do not send.

---

### Step 8 -- Report to Chris

After saving all drafts, output a summary table:

| Client | Period | Line Items | Subtotal | Draft Saved | Needs Input? |
|--------|--------|------------|----------|-------------|--------------|
| City of Sheridan | March 2026 | 6 | $1,152.30 | Yes | No |
| [Client] | March 2026 | 3 | $480.00 | Yes | Yes -- mileage unknown |

Then list any items flagged for Chris's attention:
- Emails where the task type was ambiguous and the estimate is a rough guess
- Missing client address (needed before sending)
- Mileage amounts that need to be filled in
- Any emails that looked billable but could not be matched to a project

---

## Time Estimation Philosophy

The goal is a reasonable starting point -- not perfection. Chris will adjust before sending.

- Round all estimates to the nearest 0.25 hours
- Err slightly high for complex tasks, slightly low for simple replies
- Flag any estimate over 2 hours with a note explaining why
- When in doubt, estimate conservatively -- easier for Chris to add time than to explain a high invoice

---

## Billing Rate

Default: **$120.00/hour** unless the project README specifies a different rate.

Travel reimbursement: IRS standard mileage rate or project-specified rate, whichever applies. Add as a separate line item from the hourly charges.

---

## Identifying Hourly vs. Lump Sum

Most on-call city engineering contracts are hourly. Most design or survey contracts are lump sum. When the README is ambiguous:
- Look for per-unit or per-hour language anywhere in the file
- If the payment terms mention "hours worked", treat as hourly
- If still unclear, flag for Chris and exclude from the draft

---

## What This Skill Does NOT Do

- Does not send invoices -- Chris reviews and sends manually
- Does not update accounting software or track invoice numbers
- Does not handle lump-sum or fixed-fee projects
- Does not track cumulative "billed to date" (that belongs in the project READMEs)
- Does not calculate late fees or retainage

---

## Gmail Account

Connected: **cjanigo@topexeng-ls.com**
