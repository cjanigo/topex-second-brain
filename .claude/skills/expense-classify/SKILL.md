---
name: expense-classify
description: Classify a single receipt/invoice or process a bulk bank feed. Auto-detects input type. IRS-compliant category codes and flags. Never makes filing decisions. All outputs are drafts for human review.
---

# Expense Classify Skill

## What This Is

Handles two workflows from a single invoke:

- **Single-item mode** -- takes a receipt, invoice, pasted transaction, or document ID and produces a structured Expense Record
- **Bank feed mode** -- takes a Found Bank CSV export or multi-row transaction feed and produces a full set of Banking Transaction Records with a batch summary

Both workflows use the same classification engine: IRS-compliant category codes, vendor matching, and flag rules defined in `references/financial-ops-ai-constitution.md`.

All outputs are drafts for human review. This skill never makes filing decisions.

---

## How to Invoke

```
/expense-classify
```

Optional -- pass context inline:
```
/expense-classify [receipt text, transaction description, or document ID]
/expense-classify [YYYY-MM]
/expense-classify [YYYY-MM] [account]
/expense-classify bank
/expense-classify receipt
```

Examples:
- `/expense-classify` -- prompts for input, auto-detects mode
- `/expense-classify "Amazon $47.82 2026-03-15 USB cable and field notebook"` -- single item
- `/expense-classify doc:2026-0342` -- classify a Paperless-ngx document
- `/expense-classify 2026-03` -- process March 2026 bank transactions (paste CSV when prompted)
- `/expense-classify 2026-03 checking` -- March checking account only
- `/expense-classify bank` -- force bank feed mode
- `/expense-classify receipt` -- force single-item mode

---

## Input Auto-Detection

| Input received | Mode |
|---|---|
| CSV with headers (`Date,Description,Amount...`) | Bank feed |
| 3 or more transaction rows (any format) | Bank feed |
| Single line, receipt text, doc ID, or 1--2 rows | Single-item |
| `bank` argument | Force bank feed |
| `receipt` argument | Force single-item |
| Ambiguous | Ask Chris which mode |

---

## Accepted Input Formats

**Single-item:** Receipt text, pasted invoice, plain English description, Paperless-ngx doc ID, or a single CSV row.

**Found Bank CSV (primary bank format):**
```
Date,Description,Amount,Category,Type,Notes
03/15/2026,Amazon,47.82,Office Supplies,expense,
03/16/2026,Shell Oil,62.40,Auto & Transport,expense,Field visit - client site
03/17/2026,Client Payment - City of Sheridan,2500.00,Income,income,Invoice #INV-042
```

**Generic CSV:**
```
Date,Description,Amount,Type
03/15/2026,AMAZON MKTPLACE,47.82,DEBIT
03/16/2026,SHELL OIL 00062,62.40,DEBIT
```

**Plain text / pasted lines:**
```
3/15 Amazon $47.82
3/16 Shell Oil $62.40
3/17 Deposit $2,500.00
```

**JSON array:**
```json
[
  { "date": "2026-03-15", "description": "AMAZON MKTPLACE", "amount": "47.82", "type": "debit" }
]
```

If format is ambiguous, extract what is available and flag `MISSING_FIELD` for required fields that cannot be parsed.

---

## Execution Protocol

---

### Single-Item Mode

#### Step 1 -- Gather Input

If no document or transaction was provided, ask for:
1. Vendor or payee name
2. Date of transaction
3. Amount (USD)
4. Payment method (corporate card / personal card / check / ACH / cash / unknown)
5. Description or memo (what was purchased)
6. Business purpose (why this was a business expense)
7. Project reference (if applicable)
8. Paperless-ngx document ID (if the source document is already ingested)

Accept pasted text, CSV rows, or plain English.

#### Step 2 -- Extract Fields

| Field | Notes |
|---|---|
| Vendor | Clean and normalize (e.g., "AMZN MKTP" → "Amazon") |
| Date | Normalize to YYYY-MM-DD |
| Amount | Normalize to decimal string (e.g., "47.82") |
| Payment method | Map to: `corporate_card`, `personal_card`, `check`, `ach`, `cash`, `unknown` |
| Description | Clean plain-English description of what was purchased |
| Business purpose | Verbatim from input or inferred -- flag if absent |

If any required field cannot be extracted, set to `null` and add `MISSING_FIELD` flag.

#### Step 3 -- Classify Expense

See **Shared: Category Classification** below.

#### Step 4 -- Determine Business vs. Reimbursable vs. Personal

| Payment Method | Business Purpose Present | Classification |
|---|---|---|
| Corporate card / check / ACH | Yes | `reimbursable: false` (direct corporate expense) |
| Personal card / cash | Yes | `reimbursable: true` (flag for accountable plan) |
| Either | No | `reimbursable: null` + `MISSING_PURPOSE` flag |
| Either | Clearly personal | `category_code: PERSONAL` + `PERSONAL_SUSPECTED` flag |

If the transaction mixes personal and business amounts, add `MIXED_USE` flag. Do not split the amount -- output full amount and flag.

#### Step 5 -- Apply Flags

See **Shared: Flag Rules** below.

#### Step 6 -- Output Expense Record

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
  "reimbursable": "true | false | null",
  "business_purpose": "string or null",
  "project_reference": "string or null",
  "document_id": "string or null",
  "flags": [],
  "status": "draft"
}
```

Then output a human-readable summary:

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

If multiple items are provided in single-item mode, process each sequentially and output a batch summary table at the end (see Bank Feed Mode Step 8 for table format).

---

### Bank Feed Mode

#### Step 1 -- Parse Input

For each transaction, extract:

| Field | Notes |
|---|---|
| Date | Normalize to YYYY-MM-DD |
| Description (raw) | Preserve exactly as received from bank |
| Description (cleaned) | Normalize: remove trailing codes, clean merchant name (e.g., "AMZN MKTP US*2X4AB" → "Amazon") |
| Amount | Normalize to decimal string |
| Transaction type | Debit (money out) or Credit (money in) |
| Account | If provided (checking, savings, credit card, etc.) |

If any required field cannot be parsed, set to `null` and add `MISSING_FIELD` flag.

**Found Bank CSV field mapping:**

| Found Column | Maps To | Notes |
|---|---|---|
| Date | `date` | Normalize to YYYY-MM-DD |
| Description | `description_raw` | Also clean to `description_cleaned` |
| Amount | `amount` | Always positive in Found export; direction from Type column |
| Category | Found's own label | Reference only -- override with IRS category code |
| Type | `transaction_type` | `expense` → `debit`, `income` → `credit` |
| Notes | `business_purpose` | Use as business purpose if present; reduces `MISSING_PURPOSE` flags |

**Found category label → IRS code mapping:**

| Found Category | IRS Code |
|---|---|
| Auto & Transport | AUTO |
| Business Services | LEGAL or MISC |
| Equipment | EQUIP |
| Home Office | HOME |
| Income | credit -- not an expense |
| Insurance | INS |
| Meals & Entertainment | MEALS |
| Office Supplies | OFFICE |
| Other Expenses | MISC |
| Payroll | PAYROLL |
| Professional Services | LEGAL or CONT |
| Software & Tech | SOFTWARE |
| Taxes | TAXES |
| Travel | TRAVEL |
| Utilities | UTIL |
| Uncategorized | `CATEGORY_UNCERTAIN` flag |

#### Step 2 -- Identify Transaction Direction

| Type | Meaning | Default Action |
|---|---|---|
| Debit | Money leaving the account | Classify as expense |
| Credit | Money entering the account | Classify as income or offset |

**Credit classification rules:**

| Credit Description Signal | Classification |
|---|---|
| Client name, invoice number, or "payment" | `income` -- revenue; do not classify as expense |
| "Refund", "return", "reversal" | `income` -- offset to original expense; note original vendor |
| Payroll / owner paycheck | `PAYROLL` -- tag for payroll reconciliation |
| Transfer between accounts | `transfer` -- exclude from P&L; flag for reconciliation |
| Loan or line of credit draw | Flag `MISSING_FIELD` -- classify after confirming nature of funds |
| Ambiguous | Flag `CATEGORY_UNCERTAIN` |

#### Step 3 -- Match Vendor

See **Shared: Vendor Matching** below.

#### Step 4 -- Apply Category Code

See **Shared: Category Classification** below.

Additional rules for bank transactions:

| Situation | Rule |
|---|---|
| Transaction looks personal | Set `category_code: PERSONAL`, flag `PERSONAL_SUSPECTED` |
| Amount matches a known business vendor but the date seems personal | Flag `CATEGORY_UNCERTAIN` -- confirm with Chris |
| Large round-number debit (e.g., $1,000.00, $5,000.00) | Flag `AMOUNT_ANOMALY` if no matching invoice or known vendor |
| Large round-number credit | Flag `AMOUNT_ANOMALY` -- confirm source (client payment vs. loan vs. transfer) |
| Subscription or recurring charge under $50 | Apply SOFTWARE unless vendor is personal |
| Recurring charge over $200 | Flag for confirmation if vendor is not in known list |

#### Step 5 -- Detect Mixed-Use and Personal Transactions

See **Shared: Flag Rules** below for `MIXED_USE` and `PERSONAL_SUSPECTED`.

**Do not auto-exclude personal transactions.** Flag them, output them, let Chris review and mark as excluded.

#### Step 6 -- Detect Duplicates

Within the current session's transaction set, check for duplicates:
- Same amount + same vendor + same or adjacent date = `DUPLICATE_CANDIDATE`
- Output both records; do not suppress either
- Note: "Possible duplicate of transaction on [date]. Verify before including in totals."

#### Step 7 -- Missing Receipt Flagging

For any debit transaction that:
- Has no document ID
- Is over $75
- Is not a recurring subscription

Add `MISSING_RECEIPT` flag. Note: IRS requires receipts for business expenses over $75 (and best practice for all expenses).

#### Step 8 -- Output Banking Transaction Records

For each transaction, output a structured record:

```json
{
  "record_type": "bank_transaction",
  "fiscal_year": "YYYY",
  "fiscal_month": "YYYY-MM",
  "date": "YYYY-MM-DD",
  "institution": "string or null",
  "account_last4": "string or null",
  "description_raw": "string",
  "description_cleaned": "string or null",
  "amount": "decimal string",
  "transaction_type": "debit | credit",
  "category_code": "string or null",
  "category_label": "string or null",
  "matched_vendor": "string or null",
  "project_reference": "string or null",
  "flags": [],
  "status": "categorized | uncategorized | flagged | excluded"
}
```

#### Step 9 -- Output Human-Readable Summary

After all records:

```
BANK CATEGORIZATION SUMMARY -- [Account] | [Period]
======================================================

CATEGORIZED TRANSACTIONS
| Date       | Vendor (cleaned)     | Amount    | Category | Flags     |
|------------|----------------------|-----------|----------|-----------|
| 2026-03-15 | Amazon               | $47.82    | OFFICE   | None      |
| 2026-03-16 | Shell Oil            | $62.40    | AUTO     | MISSING_PURPOSE |

INCOME / CREDITS
| Date       | Description          | Amount    | Type     | Flags     |
|------------|----------------------|-----------|----------|-----------|
| 2026-03-17 | Client Deposit       | $2,500.00 | income   | None      |

FLAGGED -- REQUIRES REVIEW
| Date       | Vendor               | Amount    | Flags                    |
|------------|----------------------|-----------|--------------------------|
| 2026-03-19 | Costco               | $184.22   | CATEGORY_UNCERTAIN, MIXED_USE |

TOTALS (categorized transactions only, excluding flagged and personal)
  Total debits categorized:    $[amount]  ([count] transactions)
  Total credits (income):      $[amount]  ([count] transactions)
  Total flagged:               [count] transactions -- review required
  Total personal suspected:    [count] transactions -- excluded from totals

Action Items:
- [each flagged item and what Chris needs to do]
- [e.g., "Shell Oil on 3/16: add business purpose"]
- [e.g., "Costco on 3/19: confirm office supplies or personal"]

DRAFT -- All records require Chris's review before use in bookkeeping.
```

For a full month run, also output a month-end summary:

```
MONTH-END SUMMARY -- [YYYY-MM]
================================
Total transactions:              [count]
Categorized (clean):             [count]  $[total]
Flagged (needs review):          [count]  $[total]
Personal / excluded:             [count]  $[total]
Uncategorized:                   [count]  $[total]

By Category:
  OFFICE:     [count]  $[total]
  AUTO:       [count]  $[total]
  SOFTWARE:   [count]  $[total]
  [other categories...]

DRAFT -- Resolve all flagged items before closing the month.
```

---

### Shared: Vendor Matching

Compare the cleaned description against known vendors. Apply the stored category for high-confidence matches.

| Match Confidence | Criteria | Action |
|---|---|---|
| High | Exact or near-exact match to known vendor | Apply stored category |
| Medium | Partial match or common merchant pattern | Apply category, add note |
| Low | No match found | `matched_vendor: null`, `category_code: null`, flag `CATEGORY_UNCERTAIN` |

**Known merchant patterns for Topex:**

| Pattern in Description | Likely Vendor | Default Category |
|---|---|---|
| AMZN, AMAZON | Amazon | OFFICE or EQUIP |
| SHELL, CHEVRON, ARCO, 76 | Fuel station | AUTO |
| GOOGLE, GSUITE, WORKSPACE | Google | SOFTWARE |
| MICROSOFT, MSFT | Microsoft | SOFTWARE |
| ADOBE | Adobe | SOFTWARE |
| ESRI | Esri / ArcGIS | SOFTWARE |
| QGIS | QGIS | SOFTWARE |
| STAPLES, OFFICE DEPOT | Office supply store | OFFICE |
| HOME DEPOT, LOWES | Hardware store | EQUIP or OFFICE (confirm purpose) |
| AUTOZONE, NAPA | Auto parts | AUTO |
| USPS, UPS, FEDEX | Shipping | POSTAGE |
| GUSTO | Gusto payroll | PAYROLL or TAXES |
| IRS | IRS | TAXES |
| OREGON DOR, OR DOR | Oregon Dept of Revenue | TAXES |
| ODOE | Oregon Dept of Employment | TAXES (UI) |
| INTUIT, QUICKBOOKS | Intuit | SOFTWARE |
| TURBOTAX | TurboTax | SOFTWARE or LEGAL |
| COSTCO | Costco | OFFICE or PERSONAL (flag for review) |
| RESTAURANT, CAFE, DINING | Restaurant | MEALS |
| HOTEL, MARRIOTT, HILTON, HAMPTON | Hotel | TRAVEL |
| AIRLINE, ALASKA AIR, UNITED, DELTA | Airline | TRAVEL |
| ZOOM | Zoom | SOFTWARE |
| DROPBOX | Dropbox | SOFTWARE |

For HOME DEPOT, LOWES, COSTCO, and similar mixed-use retailers: always flag `CATEGORY_UNCERTAIN` and ask Chris to confirm business purpose.

---

### Shared: Category Classification

Apply the category code from the constitution's Section E6:

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

### Shared: Flag Rules

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
| Vendor is personal (gym, grocery, entertainment with no business context) | `PERSONAL_SUSPECTED` |

---

## What This Skill Does NOT Do

- Does not connect to bank APIs or pull live feeds (user provides the export)
- Does not reconcile to account statements (requires balance verification)
- Does not submit data to any accounting system
- Does not split mixed-use transactions -- flags them for Chris to decide
- Does not give tax advice or recommend expense treatment or deduction strategies
- Does not determine depreciation schedules (flags HIGH_VALUE for CPA review)
- Does not resolve MIXED_USE splits -- that requires human judgment
- Does not track cumulative vendor totals across sessions (flags based on session data only)
- Does not approve or finalize any record -- all outputs are drafts

---

## Governing Reference

All category codes, JSON schemas, flag definitions, hard boundaries, and error handling rules are in:
`references/financial-ops-ai-constitution.md`
