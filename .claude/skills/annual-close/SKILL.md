---
name: annual-close
description: Year-end financial close for Topex Inc. Produces W-2 data file, 1099-NEC candidate list, Form 1120-S data summary, and FUTA reconciliation from full-year payroll records. Outputs drafts for CPA review. Never files anything.
---

# Annual Close Skill

## What This Is

Aggregates all payroll summary records and expense records for a fiscal year to produce:
- W-2 data file (all boxes populated except SSN/EIN -- those are entered before filing)
- 1099-NEC candidate list (CONT vendors with cumulative payments >= $600)
- Form 1120-S data summary (officer compensation, income, deductions, distributions)
- FUTA reconciliation
- Year-end checklist

Governing rules, data structures, flag definitions, and hard boundaries live in:
`references/financial-ops-ai-constitution.md`

This skill prepares data for CPA review. It does not file, advise, or make tax elections.

---

## How to Invoke

```
/annual-close
```

Optional -- specify the year:
```
/annual-close [YYYY]
```

Examples:
- `/annual-close` -- defaults to the most recently completed fiscal year
- `/annual-close 2025` -- close fiscal year 2025

---

## Filing Deadlines Reference

| Form | Recipient | Due Date |
|---|---|---|
| W-2 to employee | Chris Janigo | January 31 |
| W-2 / W-3 to SSA | Social Security Administration | January 31 |
| W-2 / W-3 to Oregon DOR | Oregon Department of Revenue | January 31 |
| 1099-NEC to recipients | Subcontractors, vendors | January 31 |
| 1099-NEC to IRS | IRS (Form 1096 summary) | January 31 |
| Form 940 (FUTA) | IRS | January 31 |
| Oregon Form OR-20-S | Oregon DOR | March 15 (or September 15 if extended) |
| Federal Form 1120-S | IRS | March 15 (or September 15 if extended) |

---

## Execution Protocol

### Step 1 -- Gather Full-Year Payroll Records

Ask the user to provide all Payroll Summary Records for the year (from `/payroll-summary` outputs). Accept JSON records, a table, or a summary by quarter.

For each pay period, collect at minimum:
- Pay period dates
- Gross wages
- Federal income tax withheld
- SS employee + employer (and total)
- Medicare employee + employer (and total)
- Oregon withholding
- Oregon STT
- Oregon UI employer
- WBF hours and assessment
- Net pay

Flag any pay period missing from the input with `MISSING_FIELD`. Do not proceed to W-2 computation until the user confirms the record set is complete or explicitly acknowledges the gaps.

---

### Step 2 -- Compute W-2 Box Values

Calculate each W-2 box from the full-year payroll records:

| Box | Label | Calculation |
|---|---|---|
| 1 | Wages, tips, other comp | Sum of gross wages (less pre-tax deductions if any) |
| 2 | Federal income tax withheld | Sum of federal withholding |
| 3 | Social security wages | Sum of SS-taxable wages (up to SS wage base) |
| 4 | Social security tax withheld | Sum of SS employee withheld |
| 5 | Medicare wages and tips | Sum of all gross wages (no cap) |
| 6 | Medicare tax withheld | Sum of Medicare employee withheld |
| 16 | State wages (Oregon) | Same as Box 1 unless Oregon-specific adjustments |
| 17 | State income tax withheld | Sum of Oregon withholding |
| 18 | Local wages (TriMet/LTD) | Confirm applicability for Chris's business address |
| 19 | Local income tax withheld | Sum of STT withheld (if Box 18 applies) |

Boxes not listed above (12, 13, 14): flag for CPA to populate if applicable (e.g., S-corp health insurance reported in Box 12, Code DD).

**S-Corp Health Insurance Note:**
If Topex Inc. paid health insurance premiums for Chris as owner-employee, those premiums must be included in Box 1 wages and reported in Box 12 (Code DD) or as applicable under IRS guidance. Flag this as a CPA review item -- do not calculate without confirmation of premium amounts.

---

### Step 3 -- Output W-2 Data File

```
W-2 DATA FILE -- [YYYY]
Topex Inc. | EIN: [REDACTED -- enter before filing]
Employee: Chris Janigo | SSN: [REDACTED -- enter before filing]
==============================================================

Box 1  Wages, tips, other comp                    $[amount]
Box 2  Federal income tax withheld                $[amount]
Box 3  Social security wages                      $[amount]
Box 4  Social security tax withheld               $[amount]
Box 5  Medicare wages and tips                    $[amount]
Box 6  Medicare tax withheld                      $[amount]
Box 16 State wages (Oregon)                       $[amount]
Box 17 State income tax withheld                  $[amount]
Box 18 Local wages                                $[amount or "N/A -- confirm"]
Box 19 Local income tax withheld                  $[amount or "N/A -- confirm"]

Box 12 / Box 14: [FLAG -- CPA to populate if S-corp health insurance or other items apply]
Box 13: Statutory employee: No | Retirement plan: [confirm] | Third-party sick pay: No

Flags: [list or "None"]
DRAFT -- SSN and EIN must be entered before filing. CPA review required.
```

---

### Step 4 -- FUTA Reconciliation

Federal Unemployment Tax Act (FUTA):
- Rate: 6.0% on first $7,000 of wages per employee
- FUTA credit: up to 5.4% credit if Oregon UI paid in full and on time (effective FUTA rate = 0.6%)
- If Oregon UI was paid late or Oregon UI rate varies: flag for CPA -- credit reduction may apply

Calculation:
```
FUTA taxable wages = min(annual gross wages, $7,000)
FUTA gross tax = FUTA taxable wages × 6.0%
FUTA credit = FUTA taxable wages × 5.4% (if Oregon UI paid in full and on time)
FUTA net tax = FUTA gross tax - FUTA credit
```

Deposit rule: if FUTA liability exceeds $500 in any quarter, a deposit was due by the last day of the month following that quarter. Flag any quarter where the cumulative FUTA liability may have exceeded $500 and no deposit was noted.

---

### Step 5 -- 1099-NEC Candidate List

From expense records (provided by user or from `/expense-classify` outputs), identify all CONT category vendors:

For each CONT vendor:
1. Sum all payments made during the fiscal year
2. If cumulative payments >= $600: add to 1099-NEC candidate list
3. If cumulative payments < $600: note as below threshold
4. Flag any vendor approaching $600 who may have additional invoices outstanding: `1099_THRESHOLD`

**1099-NEC required if:**
- Vendor is an individual, sole proprietor, partnership, or LLC taxed as a sole proprietor/partnership
- Total payments for the year are $600 or more
- Payments are for services rendered to the business

**1099-NEC NOT required if:**
- Vendor is a corporation (C-corp or S-corp) -- confirm via W-9
- Payments are for goods only (not services)

For each candidate, flag `MISSING_FIELD` if the vendor's address, EIN, or SSN is not on file.

Output:

```
1099-NEC CANDIDATES -- [YYYY]
==============================

| Vendor | Total Paid | Threshold Met | Entity Type | W-9 on File | Flag |
|--------|-----------|---------------|-------------|-------------|------|
| [name] | $[amount] | Yes | [type] | Yes/No | [flag or None] |
| [name] | $[amount] | Yes | Unknown | No | MISSING_FIELD |
| [name] | $[amount] | No ($[amount]) | -- | -- | Below threshold |

Action required before January 31:
- Obtain W-9 from any vendor without one on file
- Confirm entity type for any "Unknown" entries
- Verify mailing addresses for all recipients
```

---

### Step 6 -- Form 1120-S Data Summary

The 1120-S data summary is a structured input package for the CPA or TurboTax Business. It does not replace professional tax preparation.

Collect from the user:
- Total gross receipts (from invoicing records)
- Total cost of goods sold (if any -- typically $0 for professional services)
- Total officer W-2 compensation (from W-2 Box 1)
- Total distributions to owner (from owner payment records)
- All deductible business expenses by category (from expense records)
- Any S-corp-specific items: health insurance premiums, retirement contributions, home office deduction

Output:

```
FORM 1120-S DATA SUMMARY -- [YYYY]
Topex Inc. | S-Corporation
====================================

INCOME
  Gross receipts / revenue                          $[amount]
  Cost of goods sold                                $[amount]
  Gross profit                                      $[amount]
  Other income                                      $[amount]
  Total income                                      $[amount]

DEDUCTIONS (Schedule K / Page 1)
  Officer compensation (W-2 Box 1)                  $[amount]
  [ADV] Advertising                                 $[amount]
  [AUTO] Vehicle expenses                           $[amount]
  [BANK] Bank and merchant fees                     $[amount]
  [CONT] Contract labor                             $[amount]
  [DEPR] Depreciation (Form 4562)                   $[FLAG -- CPA to compute]
  [EQUIP] Equipment                                 $[amount]
  [HOME] Home office (Form 8829)                    $[FLAG -- CPA to compute]
  [INS] Insurance                                   $[amount]
  [LEGAL] Legal and professional fees               $[amount]
  [LICENSE] Licenses and permits                    $[amount]
  [MEALS] Meals (50% of total)                      $[amount]
  [OFFICE] Office supplies                          $[amount]
  [PHONE] Telephone and internet                    $[amount]
  [RENT] Rent and lease                             $[amount]
  [SOFTWARE] Software and subscriptions             $[amount]
  [TAXES] Taxes and licenses                        $[amount]
  [TRAVEL] Travel                                   $[amount]
  [UNIFORM] Work clothing / PPE                     $[amount]
  [UTIL] Utilities                                  $[amount]
  Other deductions (itemized)                       $[amount]
  Total deductions                                  $[amount]

ORDINARY BUSINESS INCOME (LOSS)                     $[amount]

SCHEDULE K ITEMS (pass-through to owner's 1040)
  Ordinary business income (Line 1)                 $[amount]
  Section 179 deduction                             $[FLAG -- confirm with CPA]
  Charitable contributions                          $[amount or N/A]
  Other deductions / credits                        $[FLAG -- CPA review]

OFFICER / SHAREHOLDER
  Officer compensation (Box 7)                      $[amount]
  Distributions to shareholder                      $[amount]
  Beginning shareholder basis                       $[FLAG -- CPA to track]
  Ending shareholder basis                          $[FLAG -- CPA to track]

REASONABLE COMPENSATION CHECK
  Annual W-2 wages:                                 $[amount]
  IRS benchmark for PE/PLS in Oregon:               $[FLAG -- confirm with CPA]
  Status:                                           [Within range / GAP FLAGGED]

Flags: [list or "None"]
DRAFT -- For CPA review before filing Form 1120-S.
```

---

### Step 7 -- Year-End Checklist

```
YEAR-END CLOSE CHECKLIST -- [YYYY]
====================================

PAYROLL & W-2
[ ] All 12 months of payroll records gathered and reconciled
[ ] W-2 Box 1-6 values computed
[ ] W-2 Box 16-19 values computed (Oregon)
[ ] S-corp health insurance added to Box 1 / Box 12 (confirm with CPA)
[ ] W-2 data reviewed by Chris
[ ] SSN and EIN entered (outside this system)
[ ] W-2 filed with SSA and Oregon DOR by January 31

1099-NEC
[ ] CONT vendor list compiled
[ ] Vendors at or over $600 identified
[ ] W-9 on file for all 1099 recipients
[ ] Entity type confirmed for all vendors
[ ] 1099-NEC drafted and mailed to recipients by January 31
[ ] Form 1096 summary filed with IRS by January 31

FUTA
[ ] FUTA taxable wages confirmed ($7,000 cap)
[ ] Oregon UI paid in full and on time (required for 5.4% credit)
[ ] Form 940 prepared and filed by January 31
[ ] Any quarterly FUTA deposits verified

FORM 1120-S
[ ] Gross receipts reconciled to invoicing records
[ ] All expense categories populated
[ ] Depreciation schedules provided to CPA (Form 4562)
[ ] Home office deduction computed (Form 8829) if applicable
[ ] Shareholder basis tracked by CPA
[ ] Reasonable compensation reviewed with CPA
[ ] Form 1120-S filed by March 15 (or September 15 if extended)
[ ] Schedule K-1 issued to Chris for personal return (Form 1040)

BANK RECONCILIATION
[ ] All bank accounts reconciled to December 31 statements
[ ] All credit card accounts reconciled
[ ] All open flags from /bank-categorize resolved

Flags: [list or "None"]
DRAFT -- CPA review required before any filing.
```

---

## What This Skill Does NOT Do

- Does not compute depreciation (CPA / Form 4562 required)
- Does not compute home office deduction (CPA / Form 8829 required)
- Does not track shareholder basis (CPA responsibility)
- Does not make S-corp tax elections or recommendations
- Does not file any form or submit any data
- Does not give tax advice

---

## Governing Reference

All JSON schemas, flag definitions, hard boundaries, Oregon tax component definitions, and error handling rules are in:
`references/financial-ops-ai-constitution.md`
