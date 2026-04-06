---
name: payroll
description: Payroll pipeline for Topex Inc. Handles three modes based on argument: single pay period summary (YYYY-MM or date range), quarterly filing package for Form 941 and Oregon OQ (Q# YYYY), or year-end close for W-2 / 1099-NEC / 1120-S / FUTA (YYYY). Never runs payroll, initiates deposits, submits filings, or gives tax advice.
argument-hint: [YYYY-MM-DD | YYYY-MM | Q# YYYY | YYYY]
---

# Payroll Skill

## What This Is

Three-mode payroll pipeline for Topex Inc.:

| Mode | What It Produces |
|---|---|
| **Payroll Summary** | Single pay period: all employee and employer tax line items, net pay, YTD tracking |
| **Quarterly Filing** | Form 941 + Oregon OQ/132 + WBF quarterly summary + filing checklist |
| **Annual Close** | W-2 data file, 1099-NEC candidates, Form 1120-S summary, FUTA reconciliation, year-end checklist |

Governing rules, data structures, flag definitions, and hard boundaries:
`references/financial-ops-ai-constitution.md`

## Invocation

```
/payroll [argument]
```

| Argument | Mode Selected |
|---|---|
| `YYYY-MM-DD YYYY-MM-DD` | Payroll Summary -- explicit date range |
| `YYYY-MM-DD` | Payroll Summary -- single date (pay date) |
| `YYYY-MM` | Payroll Summary -- month (semi-monthly: two records) |
| `Q1 2026`, `Q4 2025`, `YYYY-Q#` | Quarterly Filing |
| `YYYY` (4 digits only) | Annual Close |
| No argument | Prompt: which mode? |

---

## Shared Rules

### S-Corp Payment Classification

Every payment from Topex Inc. to Chris Janigo must be one of:

| Type | Tax Treatment | Skill Handles? |
|---|---|---|
| W-2 Wages | Subject to FICA + Oregon payroll taxes | Yes |
| Distributions | No payroll tax; reported on Schedule E / K-1 | No -- track separately |
| Accountable Plan Reimbursements | Non-taxable if documented | No -- use `/expense-classify` |

Never commingle. If ambiguous, add `DISTRIBUTION_RISK` flag for CPA review.

### Hard Limits (All Modes)

- Never runs payroll or initiates ACH/check payments
- Never submits tax deposits, filings, or e-files any form
- Never makes tax elections or recommends filing positions
- Never gives tax advice
- Never determines reasonable compensation -- only flags the gap

---

## Mode: Payroll Summary

### Step 1 -- Gather Inputs

| Input | Notes |
|---|---|
| Pay period start date | YYYY-MM-DD |
| Pay period end date | YYYY-MM-DD |
| Pay date | YYYY-MM-DD |
| Gross wages | Dollar amount |
| YTD gross wages (prior to this period) | For SS wage base tracking |
| Federal filing status | Single / Married / Head of Household |
| Oregon filing status | Single / Married / Head of Household |
| Federal allowances / W-4 extra withholding | From W-4 on file |
| Hours worked this period | Required for WBF |
| Oregon UI employer rate | From ODOE employer rate notice -- flag `RATE_UNCONFIRMED` if not provided |

### Step 2 -- Federal Tax Calculations

**Social Security (OASDI):**
- Employee: 6.2% | Employer: 6.2%
- Wage base: $176,100 for 2026 -- flag `RATE_UNCONFIRMED` if not verified
- Stop SS once YTD gross wages reach the cap

**Medicare:**
- Employee + Employer: 1.45% each (no cap)
- Additional Medicare Tax (0.9%) employee-only when YTD wages > $200K (single) / $250K (married) -- flag `RATE_UNCONFIRMED` if approaching

**Federal Income Tax Withholding:**
- Apply IRS Publication 15-T tables for pay frequency
- Flag `MISSING_FIELD` and output $0.00 if W-4 inputs unavailable

### Step 3 -- Oregon Tax Calculations

**Oregon Income Tax Withholding:**
- Apply current Oregon withholding tables (OR-40 / Publication 150-206-436)
- Flag `RATE_UNCONFIRMED` if tables not current-year verified

**Oregon STT:**
- Employee-paid, employer withholds -- no wage base cap
- Flag `RATE_UNCONFIRMED` if rate not current-year confirmed

**Oregon UI:**
- Employer-paid only
- Wage base: $57,700 for 2026 -- flag `RATE_UNCONFIRMED` if not verified
- Formula: `min(gross_wages, remaining_wage_base) × UI_rate`

**WBF:**
- Employer-paid, per hour worked
- Formula: `hours_worked × WBF_rate_per_hour` -- flag `RATE_UNCONFIRMED` if rate not confirmed

### Step 4 -- Reasonable Compensation Check

Compare projected annual W-2 wages to IRS benchmarks for a licensed PE/PLS in Oregon.
- Flag `REASONABLE_COMP_GAP` if projected wages fall below the threshold
- Note: "Review with CPA before year-end." Do not determine what "reasonable" is.

### Step 5 -- Calculate Net Pay

```
Net Pay = Gross Wages
        - Federal Income Tax Withheld
        - Employee Social Security
        - Employee Medicare
        - Oregon Income Tax Withheld
        - Oregon STT
```

Employer taxes (employer SS, employer Medicare, Oregon UI, WBF) are separate employer obligations -- not deducted from net pay.

### Step 6 -- Output Payroll Summary Record

```json
{
  "record_type": "payroll_summary",
  "pay_period_start": "YYYY-MM-DD",
  "pay_period_end": "YYYY-MM-DD",
  "pay_date": "YYYY-MM-DD",
  "employee": "Chris Janigo",
  "gross_wages": "decimal string",
  "federal_income_tax_withheld": "decimal string",
  "social_security_employee": "decimal string",
  "medicare_employee": "decimal string",
  "social_security_employer": "decimal string",
  "medicare_employer": "decimal string",
  "oregon_withholding": "decimal string",
  "oregon_stt": "decimal string",
  "oregon_ui_employer": "decimal string",
  "wbf_hours": "decimal string",
  "wbf_assessment": "decimal string",
  "net_pay": "decimal string",
  "ytd_gross_wages": "decimal string",
  "ytd_federal_taxes": "decimal string",
  "ytd_oregon_taxes": "decimal string",
  "flags": [],
  "status": "draft"
}
```

Human-readable output:

```
PAYROLL SUMMARY -- [Pay Period Start] to [Pay Period End]
Pay Date: [Pay Date] | Employee: Chris Janigo
----------------------------------------------------------
GROSS WAGES                                    $[amount]

EMPLOYEE DEDUCTIONS
  Federal Income Tax Withheld                 ($[amount])
  Social Security (6.2%)                      ($[amount])
  Medicare (1.45%)                            ($[amount])
  Oregon Income Tax Withheld                  ($[amount])
  Oregon STT ([rate]%)                        ($[amount])
                                              -----------
NET PAY                                        $[amount]

EMPLOYER OBLIGATIONS (not deducted from net pay)
  Social Security (6.2%)                       $[amount]
  Medicare (1.45%)                             $[amount]
  Oregon UI ([rate]%, taxable wages $[amount])  $[amount]
  WBF ([hours] hrs x $[rate]/hr)               $[amount]
                                              -----------
TOTAL EMPLOYER TAX COST                        $[amount]

YTD SUMMARY
  YTD Gross Wages (after this period)          $[amount]
  YTD SS Wages Applied to Cap                  $[amount]
  YTD Oregon UI Wages Applied to Cap           $[amount]

Flags: [list or "None"]
Status: DRAFT -- For review before payroll is processed.
Rates applied: [list each rate and source/year]
```

### Step 7 -- Deposit Schedule Note

- Under $50,000 lookback liability: **Monthly** -- deposit by 15th of following month
- $50,000 or over: **Semi-weekly** -- deposit by Wednesday or Friday following pay date
- Under $2,500 for quarter: may pay with Form 941
- Flag `RATE_UNCONFIRMED` if lookback liability unknown

---

## Mode: Quarterly Filing

### Quarter Date Ranges

| Quarter | Period | Due Date (Form 941 + OQ) |
|---|---|---|
| Q1 | Jan 1 -- Mar 31 | April 30 |
| Q2 | Apr 1 -- Jun 30 | July 31 |
| Q3 | Jul 1 -- Sep 30 | October 31 |
| Q4 | Oct 1 -- Dec 31 | January 31 |

### Step 1 -- Identify the Quarter

Determine quarter from argument or default to most recently completed quarter. Confirm: Q#, year, start/end dates, filing due date.

### Step 2 -- Gather Payroll Records

Ask user for all Payroll Summary Records for the quarter. Accept JSON, table, or summary by pay period.

For each pay period collect: pay dates, gross wages, FIT withheld, SS employee + employer, Medicare employee + employer, Oregon withholding, Oregon STT, Oregon UI employer, WBF hours + assessment.

Flag `MISSING_FIELD` for any missing pay period. Do not proceed to totals until user confirms the set is complete or acknowledges the gaps.

### Step 3 -- Compute Form 941 Totals

| Line | Description | Calculation |
|---|---|---|
| Line 2 | Wages, tips, other comp | Sum of gross wages |
| Line 3 | Federal income tax withheld | Sum of FIT withheld |
| Line 5a col 1 | SS wages | Sum of SS-taxable wages (up to annual wage base) |
| Line 5a col 2 | SS tax (employee + employer) | SS wages x 12.4% |
| Line 5c col 1 | Medicare wages | Sum of all gross wages (no cap) |
| Line 5c col 2 | Medicare tax (employee + employer) | Medicare wages x 2.9% |
| Line 6 | Total taxes before adjustments | FIT + SS tax + Medicare tax |
| Line 12 | Total taxes after adjustments | Line 6 (adjust fractions of cents) |
| Line 13 | Total deposits made | Prompt Chris to enter actual deposits |
| Line 14 | Balance due / overpayment | Line 12 minus Line 13 |

Flag `MISSING_FIELD` for Line 13 if deposit amounts not provided.

### Step 4 -- Compute Oregon OQ Totals

| OQ Field | Calculation |
|---|---|
| Total subject wages | Sum of all gross wages |
| Oregon income tax withheld | Sum of Oregon withholding |
| Oregon UI taxable wages | Sum up to UI wage base per employee |
| Oregon UI tax due | UI taxable wages x employer UI rate |
| Oregon STT total | Sum of STT withheld |
| WBF total hours | Sum of hours worked |
| WBF total assessment | Sum of WBF assessments |

### Step 5 -- Oregon Form 132 (Employee Detail)

Single employee: Chris Janigo

| Field | Value |
|---|---|
| Employee name | Chris Janigo |
| SSN | [Redacted -- enter before filing] |
| Subject wages | Total gross wages for quarter |
| Oregon UI taxable wages | Wages up to UI wage base |
| Hours worked | Total WBF hours for quarter |

### Step 6 -- Verify Deposit Schedule

For each deposit due during the quarter, flag if the deposit date is unknown or if total deposits (Line 13) do not match Line 12.

### Step 7 -- Apply Flags

| Check | Flag |
|---|---|
| Any pay period missing | `MISSING_FIELD` |
| Oregon UI / STT / WBF rate unconfirmed | `RATE_UNCONFIRMED` |
| SS or Oregon UI wage base unconfirmed | `RATE_UNCONFIRMED` |
| Deposit amounts not provided | `MISSING_FIELD` |
| Line 12 does not equal Line 13 | `AMOUNT_ANOMALY` |
| YTD wages suggest reasonable comp gap | `REASONABLE_COMP_GAP` |

### Step 8 -- Output OQ Summary Record

```json
{
  "record_type": "oq_quarterly_summary",
  "tax_year": "YYYY",
  "quarter": "Q#",
  "period_start": "YYYY-MM-DD",
  "period_end": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "total_wages": "decimal string",
  "oregon_withholding_total": "decimal string",
  "oregon_ui_wages": "decimal string",
  "oregon_ui_tax": "decimal string",
  "oregon_stt_total": "decimal string",
  "wbf_total_hours": "decimal string",
  "wbf_total_assessment": "decimal string",
  "form_oq_ready": true,
  "form_132_ready": true,
  "flags": [],
  "status": "draft"
}
```

### Step 9 -- Output Human-Readable Filing Package

```
QUARTERLY FILING PACKAGE
Quarter: [Q#] [YYYY] | Period: [start] to [end] | Due: [due date]
==================================================================

FORM 941 -- FEDERAL QUARTERLY SUMMARY
--------------------------------------
Line 2   Wages, tips, other compensation          $[amount]
Line 3   Federal income tax withheld             ($[amount])
Line 5a  SS wages x 12.4%                        $[amount]
Line 5c  Medicare wages x 2.9%                   $[amount]
Line 6   Total taxes before adjustments           $[amount]
Line 12  Total taxes after adjustments            $[amount]
Line 13  Total deposits made                      $[amount]  [FLAG if unknown]
Line 14  Balance due / (overpayment)              $[amount]

OREGON FORM OQ SUMMARY
-----------------------
Subject wages                                     $[amount]
Oregon income tax withheld                        $[amount]
Oregon UI taxable wages                           $[amount]
Oregon UI tax due ([rate]%)                       $[amount]
Oregon STT ([rate]%)                              $[amount]
WBF hours                                         [hours]
WBF assessment ($[rate]/hr)                       $[amount]

OREGON FORM 132 -- EMPLOYEE DETAIL
------------------------------------
Employee: Chris Janigo | SSN: [REDACTED -- enter before filing]
Subject wages: $[amount] | UI taxable wages: $[amount] | Hours: [hours]

FILING CHECKLIST
----------------
[ ] Form 941 -- due [date]
[ ] Oregon Form OQ -- due [date]
[ ] Oregon Form 132 -- submitted with OQ
[ ] Federal tax deposit verified (Line 13 matches actual deposits)
[ ] Oregon withholding deposit verified
[ ] WBF -- assessed annually by DCBS; track hours here for annual billing

DEPOSIT SCHEDULE: [Monthly | Semi-weekly | Pay with return]

Flags: [list or "None"]

DRAFT -- Verify all figures before filing.
Rates applied: [list each rate, type, and source period]
```

---

## Mode: Annual Close

### Filing Deadlines

| Form | Recipient | Due Date |
|---|---|---|
| W-2 to employee | Chris Janigo | January 31 |
| W-2 / W-3 to SSA | Social Security Administration | January 31 |
| W-2 / W-3 to Oregon DOR | Oregon DOR | January 31 |
| 1099-NEC to recipients | Subcontractors, vendors | January 31 |
| 1099-NEC to IRS (Form 1096) | IRS | January 31 |
| Form 940 (FUTA) | IRS | January 31 |
| Oregon Form OR-20-S | Oregon DOR | March 15 (or Sep 15 if extended) |
| Federal Form 1120-S | IRS | March 15 (or Sep 15 if extended) |

### Step 1 -- Gather Full-Year Payroll Records

Ask for all Payroll Summary Records for the year. Accept JSON, table, or quarterly summary.

Collect per pay period: dates, gross wages, FIT withheld, SS employee + employer, Medicare employee + employer, Oregon withholding, Oregon STT, Oregon UI employer, WBF hours + assessment, net pay.

Flag `MISSING_FIELD` for any missing period. Do not proceed until user confirms the set is complete or acknowledges gaps.

### Step 2 -- Compute W-2 Box Values

| Box | Label | Calculation |
|---|---|---|
| 1 | Wages, tips, other comp | Sum of gross wages (less pre-tax deductions if any) |
| 2 | Federal income tax withheld | Sum of FIT withheld |
| 3 | Social security wages | Sum of SS-taxable wages (up to SS wage base) |
| 4 | Social security tax withheld | Sum of SS employee withheld |
| 5 | Medicare wages and tips | Sum of all gross wages (no cap) |
| 6 | Medicare tax withheld | Sum of Medicare employee withheld |
| 16 | State wages (Oregon) | Same as Box 1 unless Oregon-specific adjustments |
| 17 | State income tax withheld | Sum of Oregon withholding |
| 18 | Local wages (TriMet/LTD) | Confirm applicability for business address |
| 19 | Local income tax withheld | Sum of STT withheld if Box 18 applies |

Boxes 12, 13, 14: flag for CPA to populate (e.g., S-corp health insurance in Box 12, Code DD).

**S-Corp Health Insurance:** If Topex Inc. paid health insurance premiums for Chris, those must be in Box 1 and Box 12. Flag as CPA review item.

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

### Step 4 -- FUTA Reconciliation

- Rate: 6.0% on first $7,000 wages per employee
- Credit: up to 5.4% if Oregon UI paid in full and on time (effective rate = 0.6%)
- If Oregon UI paid late or rate varies: flag for CPA

```
FUTA taxable wages = min(annual gross wages, $7,000)
FUTA gross tax    = FUTA taxable wages x 6.0%
FUTA credit       = FUTA taxable wages x 5.4% (if Oregon UI paid in full and on time)
FUTA net tax      = FUTA gross tax - FUTA credit
```

Flag any quarter where cumulative FUTA liability may have exceeded $500 and no deposit was noted.

### Step 5 -- 1099-NEC Candidate List

From expense records (user-provided or from `/expense-classify` outputs), identify all CONT category vendors:

- Sum all payments during the fiscal year
- Threshold >= $600: add to candidate list | < $600: note as below threshold
- Flag `1099_THRESHOLD` for any vendor approaching $600 with outstanding invoices
- Required if: individual, sole proprietor, partnership, or LLC taxed as sole prop/partnership AND payments >= $600 for services
- NOT required if: vendor is a C-corp or S-corp (confirm via W-9) or payments are for goods only
- Flag `MISSING_FIELD` if vendor address, EIN, or SSN is not on file

```
1099-NEC CANDIDATES -- [YYYY]
==============================
| Vendor | Total Paid | Threshold Met | Entity Type | W-9 on File | Flag |
|--------|-----------|---------------|-------------|-------------|------|
| [name] | $[amount] | Yes | [type] | Yes/No | [flag or None] |

Action required before January 31:
- Obtain W-9 from any vendor without one on file
- Confirm entity type for any Unknown entries
- Verify mailing addresses for all recipients
```

### Step 6 -- Form 1120-S Data Summary

Collect from user: gross receipts, COGS (typically $0), officer W-2 comp, distributions, all deductible expenses by category, S-corp items (health insurance, retirement, home office).

```
FORM 1120-S DATA SUMMARY -- [YYYY]
Topex Inc. | S-Corporation
====================================
INCOME
  Gross receipts / revenue                          $[amount]
  Cost of goods sold                                $[amount]
  Gross profit                                      $[amount]
  Total income                                      $[amount]

DEDUCTIONS
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
  Other deductions                                  $[amount]
  Total deductions                                  $[amount]

ORDINARY BUSINESS INCOME (LOSS)                     $[amount]

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

### Step 7 -- Year-End Checklist

```
YEAR-END CLOSE CHECKLIST -- [YYYY]
====================================
PAYROLL & W-2
[ ] All 12 months of payroll records gathered and reconciled
[ ] W-2 boxes computed and reviewed by Chris
[ ] SSN and EIN entered (outside this system)
[ ] S-corp health insurance added to Box 1 / Box 12 (confirm with CPA)
[ ] W-2 filed with SSA and Oregon DOR by January 31

1099-NEC
[ ] CONT vendor list compiled and thresholds checked
[ ] W-9 on file for all 1099 recipients
[ ] Entity type confirmed for all vendors
[ ] 1099-NEC sent to recipients and IRS by January 31

FUTA
[ ] FUTA taxable wages confirmed ($7,000 cap)
[ ] Oregon UI paid in full and on time
[ ] Form 940 filed by January 31

FORM 1120-S
[ ] Gross receipts reconciled to invoicing records
[ ] All expense categories populated
[ ] Depreciation and home office deduction with CPA
[ ] Shareholder basis tracked by CPA
[ ] Reasonable compensation reviewed with CPA
[ ] Form 1120-S filed by March 15 (or September 15 if extended)
[ ] Schedule K-1 issued for personal return (Form 1040)

BANK RECONCILIATION
[ ] All accounts reconciled to December 31 statements
[ ] All open flags from /bank-categorize resolved

Flags: [list or "None"]
DRAFT -- CPA review required before any filing.
```

---

## Governing Reference

`references/financial-ops-ai-constitution.md`
