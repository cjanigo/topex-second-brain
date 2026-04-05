---
name: quarterly-filing
description: Aggregate payroll summary records for a quarter and produce export-ready Form 941 and Oregon OQ data with a filing checklist and due dates. Outputs drafts for human review. Never submits filings.
---

# Quarterly Filing Skill

## What This Is

Takes all payroll summary records for a given quarter and produces export-ready data for:
- IRS Form 941 (Employer's Quarterly Federal Tax Return)
- Oregon Form OQ (Oregon Quarterly Tax Report)
- Oregon Form 132 (Employee Detail Report)
- WBF quarterly hours and assessment summary

Also outputs a filing checklist with due dates and deposit schedule verification.

Governing rules, data structures, flag definitions, and hard boundaries live in:
`references/financial-ops-ai-constitution.md`

This skill prepares export data. It does not submit filings, make tax elections, or recommend positions.

---

## How to Invoke

```
/quarterly-filing
```

Optional -- specify the quarter:
```
/quarterly-filing [Q1|Q2|Q3|Q4] [YYYY]
/quarterly-filing [YYYY-Q#]
```

Examples:
- `/quarterly-filing` -- defaults to the most recently completed quarter
- `/quarterly-filing Q1 2026` -- January through March 2026
- `/quarterly-filing Q4 2025` -- October through December 2025

---

## Quarter Date Ranges

| Quarter | Period | Due Date (Form 941 + OQ) |
|---|---|---|
| Q1 | Jan 1 -- Mar 31 | April 30 |
| Q2 | Apr 1 -- Jun 30 | July 31 |
| Q3 | Jul 1 -- Sep 30 | October 31 |
| Q4 | Oct 1 -- Dec 31 | January 31 |

---

## Execution Protocol

### Step 1 -- Identify the Quarter

Determine the quarter from user input or default to the most recently completed quarter based on today's date.

Confirm:
- Quarter (Q1/Q2/Q3/Q4)
- Fiscal year
- Period start date (YYYY-MM-DD)
- Period end date (YYYY-MM-DD)
- Filing due date

---

### Step 2 -- Gather Payroll Records

Ask the user to provide all Payroll Summary Records for the quarter (from `/payroll-summary` outputs). Accept:
- Pasted JSON records
- A list of gross wages by pay period
- A summary table with pay period dates and key figures

For each pay period in the quarter, collect:

| Field | Source |
|---|---|
| Pay period dates | Payroll Summary Record |
| Gross wages | Payroll Summary Record |
| Federal income tax withheld | Payroll Summary Record |
| SS employee | Payroll Summary Record |
| SS employer | Payroll Summary Record |
| Medicare employee | Payroll Summary Record |
| Medicare employer | Payroll Summary Record |
| Oregon withholding | Payroll Summary Record |
| Oregon STT | Payroll Summary Record |
| Oregon UI employer | Payroll Summary Record |
| WBF hours | Payroll Summary Record |
| WBF assessment | Payroll Summary Record |

If any pay period is missing from the input, flag `MISSING_FIELD` and note which period is absent. Do not proceed to totals until the user confirms whether the missing period had zero wages or provides the data.

---

### Step 3 -- Compute Form 941 Totals

Aggregate across all pay periods in the quarter:

| Line | Description | Calculation |
|---|---|---|
| Line 2 | Wages, tips, and other compensation | Sum of all gross wages |
| Line 3 | Federal income tax withheld | Sum of all FIT withheld |
| Line 5a col 1 | SS wages | Sum of SS-taxable wages (up to annual wage base) |
| Line 5a col 2 | SS tax (employee + employer) | SS wages × 12.4% |
| Line 5c col 1 | Medicare wages | Sum of all gross wages (no cap) |
| Line 5c col 2 | Medicare tax (employee + employer) | Medicare wages × 2.9% |
| Line 6 | Total taxes before adjustments | FIT withheld + SS tax + Medicare tax |
| Line 12 | Total taxes after adjustments | Line 6 (adjust for fractions of cents if needed) |
| Line 13 | Total deposits made | Prompt Chris to enter actual deposit amounts |
| Line 14 | Balance due or overpayment | Line 12 minus Line 13 |

Flag `MISSING_FIELD` for Line 13 if deposit amounts are not provided. Output $0.00 as placeholder.

---

### Step 4 -- Compute Oregon OQ Totals

Aggregate across all pay periods in the quarter:

| OQ Field | Calculation |
|---|---|
| Total subject wages | Sum of all gross wages |
| Oregon income tax withheld | Sum of all Oregon withholding |
| Oregon UI taxable wages | Sum of wages up to UI wage base per employee |
| Oregon UI tax due | UI taxable wages × employer UI rate |
| Oregon STT total | Sum of all STT withheld |
| WBF total hours | Sum of all hours worked |
| WBF total assessment | Sum of all WBF assessments |

---

### Step 5 -- Compute Oregon Form 132 (Employee Detail)

Single employee: Chris Janigo

| Form 132 Field | Value |
|---|---|
| Employee name | Chris Janigo |
| SSN | [Redacted -- enter before filing] |
| Subject wages | Total gross wages for quarter |
| Oregon UI taxable wages | Wages up to UI wage base |
| Hours worked | Total WBF hours for quarter |

---

### Step 6 -- Verify Deposit Schedule

Based on federal tax liability for the quarter:

| Lookback Period Liability | Deposit Schedule | Deposit Deadlines |
|---|---|---|
| Under $50,000 | Monthly | By 15th of following month |
| $50,000 or over | Semi-weekly | Wednesday or Friday following pay date |
| Under $2,500 for quarter | May pay with 941 | By filing due date |

For each deposit that was due during the quarter, flag if the deposit date is unknown or if total deposits (Line 13) do not equal Line 12.

---

### Step 7 -- Apply Flags

| Check | Flag |
|---|---|
| Any pay period missing from input | `MISSING_FIELD` |
| Oregon UI rate not confirmed for current year | `RATE_UNCONFIRMED` |
| STT rate not confirmed for current year | `RATE_UNCONFIRMED` |
| WBF rate not confirmed for current year | `RATE_UNCONFIRMED` |
| SS wage base not confirmed for current year | `RATE_UNCONFIRMED` |
| Oregon UI wage base not confirmed for current year | `RATE_UNCONFIRMED` |
| Deposit amounts not provided (Line 13 = $0) | `MISSING_FIELD` |
| Line 12 does not equal Line 13 (balance due or overpayment) | `AMOUNT_ANOMALY` |
| YTD wages suggest reasonable compensation gap | `REASONABLE_COMP_GAP` |

---

### Step 8 -- Output Oregon OQ Summary Record

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
  "form_oq_ready": true | false,
  "form_132_ready": true | false,
  "flags": [],
  "status": "draft"
}
```

---

### Step 9 -- Output Human-Readable Filing Package

```
QUARTERLY FILING PACKAGE
Quarter: [Q#] [YYYY] | Period: [start] to [end] | Due: [due date]
==================================================================

FORM 941 -- FEDERAL QUARTERLY SUMMARY
--------------------------------------
Line 2   Wages, tips, other compensation          $[amount]
Line 3   Federal income tax withheld             ($[amount])
Line 5a  SS wages × 12.4%                        $[amount]
Line 5c  Medicare wages × 2.9%                   $[amount]
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
[ ] Form 941 -- Federal quarterly return -- due [date]
[ ] Oregon Form OQ -- due [date]
[ ] Oregon Form 132 -- submitted with OQ
[ ] Federal tax deposit verified (Line 13 matches actual deposits)
[ ] Oregon withholding deposit verified
[ ] WBF -- assessed annually by DCBS; track hours here for annual billing

DEPOSIT SCHEDULE: [Monthly | Semi-weekly | Pay with return]

Flags: [list or "None"]

DRAFT -- All figures must be verified by Chris or CPA before filing.
Rates applied: [list each rate, type, and source period]
```

---

## What This Skill Does NOT Do

- Does not e-file or submit any form
- Does not initiate tax deposits or payments
- Does not amend prior-quarter returns
- Does not determine penalty amounts for late deposits
- Does not give tax advice or recommend filing positions
- Does not track individual pay period deposits -- Chris provides those

---

## Governing Reference

All JSON schemas, flag definitions, Oregon tax component definitions, hard boundaries, and error handling rules are in:
`references/financial-ops-ai-constitution.md`
