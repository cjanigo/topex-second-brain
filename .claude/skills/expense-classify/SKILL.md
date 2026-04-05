---
name: expense-classify
description: Classify a receipt, invoice, or transaction into an IRS-compliant expense category with flags. Outputs a structured Expense Record JSON for human review. Never makes filing decisions.
---

# Expense Classify Skill

## What This Is

Takes a receipt, invoice, pasted transaction line, or document description and produces a structured, classified Expense Record ready for bookkeeping review.

Governing rules, data structures, category codes, and hard boundaries live in:
`references/financial-ops-ai-constitution.md`

All outputs are drafts for human review. This skill never makes filing decisions.

---

## How to Invoke

```
/expense-classify
```

Optional -- pass context inline:
```
/expense-classify [paste receipt text or transaction description]
/expense-classify [Paperless-ngx document ID]
/expense-classify [vendor] [amount] [date] [description]
```

Examples:
- `/expense-classify` -- prompts for input
- `/expense-classify "Amazon $47.82 2026-03-15 USB cable and field notebook"`
- `/expense-classify doc:2026-0342` -- reference a Paperless-ngx document
- `/expense-classify` then paste a bank transaction line

---

## Execution Protocol

### Step 1 -- Gather Input

If the user has not provided a document or transaction, ask:

1. Vendor or payee name
2. Date of transaction
3. Amount (USD)
4. Payment method (corporate card / personal card / check / ACH / cash / unknown)
5. Description or memo (what was purchased or paid for)
6. Business purpose (why this was a business expense)
7. Project reference (if applicable)
8. Paperless-ngx document ID (if the source document is already ingested)

Accept pasted text, CSV rows, or plain English descriptions. Extract fields from whatever is provided.

---

### Step 2 -- Extract Fields

From the input, extract:

| Field | Notes |
|---|---|
| Vendor | Clean and normalize the name (e.g., "AMZN MKTP" → "Amazon") |
| Date | Normalize to YYYY-MM-DD |
| Amount | Normalize to decimal string (e.g., "47.82") |
| Payment method | Map to: `corporate_card`, `personal_card`, `check`, `ach`, `cash`, `unknown` |
| Description | Clean plain-English description of what was purchased |
| Business purpose | Verbatim from input or inferred from description -- flag if absent |

If any required field cannot be extracted, set to `null` and add `MISSING_FIELD` flag.

---

### Step 3 -- Classify Expense

Apply the category code from the constitution's Section E6 table.

**Classification logic:**

| Input Signal | Category Code |
|---|---|
| Fuel, oil, vehicle maintenance | `AUTO` |
| Mileage reimbursement | `AUTO` |
| Advertising, marketing, website | `ADV` |
| Bank fee, wire fee, merchant fee | `BANK` |
| Payment to subcontractor or 1099 vendor | `CONT` |
| Equipment purchase (non-depreciable, under $2,500) | `EQUIP` |
| Equipment purchase over $2,500 | `EQUIP` + `HIGH_VALUE` flag |
| Home office portion of rent/utilities | `HOME` |
| Business insurance, E&O, general liability | `INS` |
| CPA, attorney, or licensed professional fees | `LEGAL` |
| Professional licenses, PE/PLS renewal, permits | `LICENSE` |
| Business meals (50% rule applies) | `MEALS` |
| Office supplies, paper, printer ink | `OFFICE` |
| Owner W-2 wages | `PAYROLL` |
| Cell phone, internet (business portion) | `PHONE` |
| Postage, shipping, FedEx | `POSTAGE` |
| Office rent or equipment lease | `RENT` |
| Software, SaaS subscriptions, cloud storage | `SOFTWARE` |
| Oregon UI, payroll taxes, business taxes | `TAXES` |
| Hotel, airfare, non-local travel | `TRAVEL` |
| PPE, work boots, field clothing | `UNIFORM` |
| Utilities at business location | `UTIL` |
| Owner distribution or equity draw | `DISTRIB` |
| Clearly personal (gym, groceries, entertainment) | `PERSONAL` |
| Ambiguous -- cannot determine with confidence | `null` + `CATEGORY_UNCERTAIN` flag |

If two categories are plausible, output top two with confidence notes and flag `CATEGORY_UNCERTAIN`.

---

### Step 4 -- Determine Business vs. Reimbursable vs. Personal

| Payment Method | Business Purpose Present | Classification |
|---|---|---|
| Corporate card / check / ACH | Yes | `reimbursable: false` (direct corporate expense) |
| Personal card / cash | Yes | `reimbursable: true` (flag for accountable plan) |
| Either | No | `reimbursable: null` + `MISSING_PURPOSE` flag |
| Either | Clearly personal | `category_code: PERSONAL` + `PERSONAL_SUSPECTED` flag |

If the transaction appears to mix personal and business amounts, add `MIXED_USE` flag. Do not split the amount -- output full amount and flag.

---

### Step 5 -- Apply Flags

Check each flag from the constitution's Section F:

| Check | Flag |
|---|---|
| No supporting document or document ID | `MISSING_RECEIPT` |
| Business purpose is null or absent | `MISSING_PURPOSE` |
| Personal and business components suspected | `MIXED_USE` |
| Amount, vendor, and date match a prior record in this session | `DUPLICATE_CANDIDATE` |
| Document date is in a prior fiscal year | `PRIOR_YEAR` |
| Reimbursement claim with no receipt or mileage log | `UNSUBSTANTIATED_REIMB` |
| Payment to owner (wages vs. distribution ambiguous) | `DISTRIBUTION_RISK` |
| Amount over $2,500 | `HIGH_VALUE` |
| Cumulative payments to this CONT vendor approaching $600 | `1099_THRESHOLD` |
| Category confidence is low | `CATEGORY_UNCERTAIN` |
| Personal transaction suspected | `PERSONAL_SUSPECTED` |

---

### Step 6 -- Output Expense Record

Output the classified record as JSON:

```json
{
  "record_type": "expense",
  "fiscal_year": "YYYY",
  "fiscal_month": "YYYY-MM",
  "date": "YYYY-MM-DD",
  "vendor": "string",
  "description": "string",
  "amount": "decimal string",
  "payment_method": "corporate_card | personal_card | check | ach | cash | unknown",
  "category_code": "string or null",
  "category_label": "string or null",
  "reimbursable": true | false | null,
  "business_purpose": "string or null",
  "project_reference": "string or null",
  "document_id": "string or null",
  "flags": [],
  "status": "draft"
}
```

Then output a human-readable summary below the JSON:

```
EXPENSE CLASSIFICATION SUMMARY
-------------------------------
Vendor:           [vendor]
Date:             [date]
Amount:           $[amount]
Category:         [code] -- [label]
Payment:          [method]
Reimbursable:     [Yes / No / Unknown]
Business Purpose: [purpose or MISSING]
Flags:            [list or "None"]
Status:           Draft -- awaiting review

[If CATEGORY_UNCERTAIN: "Top 2 candidates: [code1] ([label1]) | [code2] ([label2])"]
[If HIGH_VALUE: "Amount exceeds $2,500 -- verify depreciation treatment with CPA."]
[If MIXED_USE: "Possible personal component -- do not process until owner reviews."]
[If 1099_THRESHOLD: "Cumulative payments to this vendor may be approaching $600. Verify 1099-NEC requirement."]
```

---

### Step 7 -- Batch Processing

If the user provides multiple receipts or a list of transactions, process each one sequentially and output:
1. Individual JSON records for each transaction
2. A batch summary table at the end:

```
| # | Vendor | Date | Amount | Category | Flags |
|---|--------|------|--------|----------|-------|
| 1 | Amazon | 2026-03-15 | $47.82 | OFFICE | None |
| 2 | Shell | 2026-03-16 | $62.40 | AUTO | MISSING_PURPOSE |
| 3 | [Vendor] | 2026-03-17 | $3,200.00 | EQUIP | HIGH_VALUE |
```

Then list all flagged items requiring Chris's attention.

---

## What This Skill Does NOT Do

- Does not give tax advice or recommend deduction strategies
- Does not determine depreciation schedules (flags HIGH_VALUE for CPA review)
- Does not submit data to any accounting system
- Does not resolve MIXED_USE splits -- that requires human judgment
- Does not track cumulative vendor totals across sessions (flags based on session data only)
- Does not approve or finalize any record -- all outputs are drafts

---

## Governing Reference

All category codes, JSON schemas, flag definitions, hard boundaries, and error handling rules are in:
`references/financial-ops-ai-constitution.md`
