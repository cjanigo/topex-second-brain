---
name: bank-categorize
description: Process a bank or credit card feed (CSV, JSON, or pasted rows), match vendors, apply IRS-compliant category codes, flag mixed-use and uncategorized transactions, and output structured records for bookkeeping review.
---

# Bank Categorize Skill

## What This Is

Takes a bank or credit card transaction feed and produces a clean, categorized set of Banking Transaction Records ready for bookkeeping review.

**Primary institution:** Found Bank (found.com) -- Topex Inc. business checking and card.

Governing rules, data structures, category codes, flag definitions, and hard boundaries live in:
`references/financial-ops-ai-constitution.md`

All outputs are drafts for human review. This skill does not submit data to any accounting system.

---

## How to Invoke

```
/bank-categorize
```

Optional -- scope the run:
```
/bank-categorize [YYYY-MM]
/bank-categorize [account]
/bank-categorize [YYYY-MM] [account]
```

Examples:
- `/bank-categorize` -- prompts for transaction input
- `/bank-categorize 2026-03` -- process March 2026 transactions
- `/bank-categorize 2026-03 checking` -- process March 2026 checking account only
- Paste transactions directly after invoking

---

## Accepted Input Formats

### Found Bank CSV Export (Primary Format)

Found Bank exports transactions as CSV. Export from the Found dashboard: Transactions > Export. The standard Found export format:

```
Date,Description,Amount,Category,Type,Notes
03/15/2026,Amazon,47.82,Office Supplies,expense,
03/16/2026,Shell Oil,62.40,Auto & Transport,expense,Field visit - client site
03/17/2026,Client Payment - City of Sheridan,2500.00,Income,income,Invoice #INV-042
```

**Found CSV field mapping:**

| Found Column | Maps To | Notes |
|---|---|---|
| Date | `date` | Normalize to YYYY-MM-DD |
| Description | `description_raw` | Also clean to `description_cleaned` |
| Amount | `amount` | Always positive in Found export; direction from Type column |
| Category | Found's own label | Reference only -- override with IRS category code from constitution |
| Type | `transaction_type` | `expense` → `debit`, `income` → `credit` |
| Notes | `business_purpose` | If present, use as business purpose; reduces `MISSING_PURPOSE` flags |

**Found's category labels are useful signals but do not replace IRS-compliant category codes.** Map Found categories to constitution codes (Section E6) -- do not use Found's labels in output records.

| Found Category | Maps To (IRS Code) |
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

### Other Accepted Formats

**Plain text / pasted lines:**
```
3/15 Amazon $47.82
3/16 Shell Oil $62.40
3/17 Deposit $2,500.00
```

**Generic CSV (non-Found):**
```
Date,Description,Amount,Type
03/15/2026,AMAZON MKTPLACE,47.82,DEBIT
03/16/2026,SHELL OIL 00062,62.40,DEBIT
03/17/2026,CLIENT DEPOSIT,2500.00,CREDIT
```

**JSON array** (from n8n or other pipeline):
```json
[
  { "date": "2026-03-15", "description": "AMAZON MKTPLACE", "amount": "47.82", "type": "debit" },
  ...
]
```

If format is ambiguous, extract what is available and flag `MISSING_FIELD` for any required fields that cannot be parsed.

---

## Execution Protocol

### Step 1 -- Parse Input

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

---

### Step 2 -- Identify Transaction Direction

| Transaction Type | Meaning | Default Action |
|---|---|---|
| Debit | Money leaving the account | Classify as expense |
| Credit | Money entering the account | Classify as income or offset |

**Credit classification rules:**

| Credit Description Signal | Classification |
|---|---|
| Client name, invoice number, or "payment" | `income` -- revenue; do not classify as expense |
| "Refund", "return", "reversal" | `income` -- offset to original expense; note the original vendor |
| Payroll / owner paycheck | `PAYROLL` -- tag for payroll reconciliation |
| Transfer between accounts | `transfer` -- exclude from P&L; flag for reconciliation |
| Loan or line of credit draw | Flag `MISSING_FIELD` -- classify after confirming nature of funds |
| Ambiguous | Flag `CATEGORY_UNCERTAIN` |

---

### Step 3 -- Match Vendor

Compare the cleaned description against known vendors using context from AnythingLLM (prior categorization history) or the user's known vendor list.

**Match confidence levels:**

| Confidence | Criteria | Action |
|---|---|---|
| High | Exact or near-exact match to known vendor | Apply stored category |
| Medium | Partial match or common merchant pattern | Apply category, add note |
| Low | No match found | Set `matched_vendor: null`, set `category_code: null`, flag `CATEGORY_UNCERTAIN` |

Common merchant patterns for Topex's business:

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

For HOME DEPOT, LOWES, COSTCO, and similar mixed-use retailers: always flag `CATEGORY_UNCERTAIN` and ask Chris to confirm the business purpose.

---

### Step 4 -- Apply Category Code

Apply the category code from the constitution's Section E6. See `/expense-classify` for the full classification decision logic.

Additional rules for bank transactions:

| Situation | Rule |
|---|---|
| Transaction looks personal | Set `category_code: PERSONAL`, flag `PERSONAL_SUSPECTED` |
| Amount matches a known business vendor but the date seems personal | Flag `CATEGORY_UNCERTAIN` -- confirm with Chris |
| Large round-number debit (e.g., $1,000.00, $5,000.00) | Flag `AMOUNT_ANOMALY` if no matching invoice or known vendor |
| Large round-number credit | Flag `AMOUNT_ANOMALY` -- confirm source (client payment vs. loan vs. transfer) |
| Subscription or recurring charge under $50 | Apply SOFTWARE unless vendor is personal |
| Recurring charge over $200 | Flag for confirmation if vendor is not in known list |

---

### Step 5 -- Detect Mixed-Use and Personal Transactions

**Flag `MIXED_USE` if any of these are true:**
- Vendor is known to sell both personal and business items (Costco, Amazon, Home Depot)
- Description includes both a business item and a non-business item (uncommon but possible)
- Transaction is from a personal account (if account type is identified as personal)

**Flag `PERSONAL_SUSPECTED` if:**
- Vendor is clearly personal (gym, grocery store, restaurant with no business context, entertainment)
- Transaction occurs on a weekend with no business context
- Description matches common personal spending patterns

**Do not auto-exclude personal transactions.** Flag them, output them, let Chris review and mark as excluded.

---

### Step 6 -- Detect Duplicates

Within the current session's transaction set, check for duplicates:
- Same amount + same vendor + same or adjacent date = `DUPLICATE_CANDIDATE`
- Output both records; do not suppress either
- Note: "Possible duplicate of transaction on [date]. Verify before including in totals."

---

### Step 7 -- Output Banking Transaction Records

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

---

### Step 8 -- Output Human-Readable Summary

After all records, output a summary table:

```
BANK CATEGORIZATION SUMMARY -- [Account] | [Period]
======================================================

CATEGORIZED TRANSACTIONS
| Date       | Vendor (cleaned)     | Amount    | Category | Flags     |
|------------|----------------------|-----------|----------|-----------|
| 2026-03-15 | Amazon               | $47.82    | OFFICE   | None      |
| 2026-03-16 | Shell Oil            | $62.40    | AUTO     | MISSING_PURPOSE |
| 2026-03-18 | Google Workspace     | $14.99    | SOFTWARE | None      |

INCOME / CREDITS
| Date       | Description          | Amount    | Type     | Flags     |
|------------|----------------------|-----------|----------|-----------|
| 2026-03-17 | Client Deposit       | $2,500.00 | income   | None      |

FLAGGED -- REQUIRES REVIEW
| Date       | Vendor               | Amount    | Flags                    |
|------------|----------------------|-----------|--------------------------|
| 2026-03-19 | Costco               | $184.22   | CATEGORY_UNCERTAIN, MIXED_USE |
| 2026-03-20 | [Unknown Vendor]     | $1,200.00 | CATEGORY_UNCERTAIN, AMOUNT_ANOMALY |

TOTALS (categorized transactions only, excluding flagged and personal)
  Total debits categorized:    $[amount]  ([count] transactions)
  Total credits (income):      $[amount]  ([count] transactions)
  Total flagged:               [count] transactions -- review required
  Total personal suspected:    [count] transactions -- excluded from totals

Action Items:
- [list each flagged item and what Chris needs to do]
- [e.g., "Shell Oil on 3/16: add business purpose (field visit, client meeting, etc.)"]
- [e.g., "Costco on 3/19: confirm whether this was office supplies or personal"]
- [e.g., "Unknown $1,200 on 3/20: identify vendor and business purpose"]

DRAFT -- All records require Chris's review before use in bookkeeping.
```

---

### Step 9 -- Missing Receipt Flagging

After categorization, cross-reference the transaction list against any receipts or documents provided (if provided). For any debit transaction that:
- Has no document ID
- Is over $75
- Is not a recurring subscription

Add `MISSING_RECEIPT` flag. Note: IRS requires receipts for business expenses over $75 (and best practice for all expenses).

---

## Batch Month-End Processing

When processing a full month's transactions:

1. Process all transactions from the bank CSV
2. Output categorized records
3. Output flagged transactions table
4. Output action items for Chris
5. Output month-end summary:

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
  CONT:       [count]  $[total]
  TAXES:      [count]  $[total]
  [other categories with amounts...]

DRAFT -- Resolve all flagged items before closing the month.
```

---

## What This Skill Does NOT Do

- Does not connect to bank APIs or pull live feeds (user provides the export)
- Does not reconcile to account statements (that requires balance verification)
- Does not submit data to accounting software
- Does not split mixed-use transactions -- flags them for Chris to decide
- Does not give tax advice or recommend expense treatment
- Does not track cumulative vendor totals across sessions (flags 1099_THRESHOLD based on session data)

---

## Governing Reference

All category codes, JSON schemas, flag definitions, hard boundaries, and error handling rules are in:
`references/financial-ops-ai-constitution.md`
