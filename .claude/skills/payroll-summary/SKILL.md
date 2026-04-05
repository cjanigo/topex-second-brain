---
name: payroll-summary
description: Generate a payroll summary for a single pay period with all Oregon and federal tax line items. Outputs a structured Payroll Summary Record for human review. Never runs payroll or initiates payments.
---

# Payroll Summary Skill

## What This Is

Takes a pay period's gross wage input and produces a complete, itemized payroll summary with all employer and employee tax obligations: federal FICA, federal income tax withholding, Oregon withholding, Oregon STT, Oregon UI, and WBF assessment.

Governing rules, data structures, flag definitions, and hard boundaries live in:
`references/financial-ops-ai-constitution.md`

This skill prepares data. It does not run payroll, initiate payments, or submit filings.

---

## How to Invoke

```
/payroll-summary
```

Optional -- pass context inline:
```
/payroll-summary [pay-period-start] [pay-period-end]
/payroll-summary [YYYY-MM]
```

Examples:
- `/payroll-summary` -- prompts for pay period inputs
- `/payroll-summary 2026-03-01 2026-03-15` -- first half of March 2026
- `/payroll-summary 2026-03` -- full month of March 2026 (semi-monthly: two records)

---

## Execution Protocol

### Step 1 -- Gather Inputs

Prompt for any missing values:

| Input | Notes |
|---|---|
| Pay period start date | YYYY-MM-DD |
| Pay period end date | YYYY-MM-DD |
| Pay date | YYYY-MM-DD (date check/ACH is issued) |
| Gross wages | Dollar amount for this pay period |
| YTD gross wages (prior to this period) | Used for SS wage base tracking |
| Federal filing status | Single / Married / Head of Household |
| Oregon filing status | Single / Married / Head of Household |
| Federal allowances / W-4 extra withholding | From Chris's W-4 on file |
| Hours worked this period | Required for WBF assessment |
| Oregon UI employer rate | From ODOE employer rate notice (confirm annually) |

If Oregon UI rate is not provided, flag `RATE_UNCONFIRMED` and note that the most recently confirmed rate will be applied.

---

### Step 2 -- Apply Federal Tax Calculations

**Social Security (OASDI):**
- Employee: 6.2% of gross wages
- Employer: 6.2% of gross wages
- Wage base: $176,100 for 2026 (confirm annually -- flag `RATE_UNCONFIRMED` if not verified)
- If YTD gross wages + this period's gross wages exceed the wage base: calculate SS only on the remaining amount below the cap. Set SS = $0.00 for amounts above the cap.

**Medicare:**
- Employee: 1.45% of gross wages (no wage base cap)
- Employer: 1.45% of gross wages
- Additional Medicare Tax (0.9%): applies to employee only when YTD wages exceed $200,000 (single) or $250,000 (married). Flag `RATE_UNCONFIRMED` if approaching threshold.

**Federal Income Tax Withholding:**
- Apply IRS Publication 15-T withholding tables for the pay period frequency
- Use filing status and W-4 inputs provided
- If W-4 inputs are not available: flag `MISSING_FIELD` and output $0.00 as placeholder

---

### Step 3 -- Apply Oregon Tax Calculations

**Oregon Income Tax Withholding:**
- Apply current Oregon withholding tables (OR-40 instructions / Publication 150-206-436)
- Use Oregon filing status provided
- If tables not available in context: flag `RATE_UNCONFIRMED`, note the source period of the last confirmed rate, and apply that rate with a caveat

**Oregon Statewide Transit Tax (STT):**
- Employee-paid; employer withholds
- Current rate: confirm from Oregon DOR (flag `RATE_UNCONFIRMED` if not current-year confirmed)
- No wage base cap -- applies to all wages
- Formula: `gross_wages × STT_rate`

**Oregon Unemployment Insurance (UI):**
- Employer-paid only
- Apply employer's current experience rate (from ODOE employer rate notice)
- Taxable wage base: $57,700 for 2026 (confirm annually -- flag `RATE_UNCONFIRMED` if not verified)
- Stop UI calculation once YTD wages exceed the wage base
- Formula: `min(gross_wages, remaining_wage_base) × UI_rate`

**Workers Benefit Fund (WBF):**
- Employer-paid; assessed per hour worked
- Current per-hour rate: confirm from Oregon DCBS (flag `RATE_UNCONFIRMED` if not current-year confirmed)
- Formula: `hours_worked × WBF_rate_per_hour`

---

### Step 4 -- Check Reasonable Compensation

Compare YTD W-2 gross wages (after this period) to a reference threshold for a licensed civil engineer / land surveyor in Oregon.

Reference threshold (update annually): confirm current IRS reasonable compensation benchmarks for this role and geography. If the current year's threshold is not available in context, note the most recent known benchmark.

If annualized YTD wages project below the threshold:
- Add `REASONABLE_COMP_GAP` flag
- Note: "Projected annual W-2 wages may fall below IRS reasonable compensation benchmarks for a licensed PE/PLS in Oregon. Review with CPA before year-end."

Do not determine what "reasonable" is. Only flag the gap.

---

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

---

### Step 6 -- Output Payroll Summary Record

Output the full record as JSON:

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

Then output a human-readable summary:

```
PAYROLL SUMMARY -- [Pay Period Start] to [Pay Period End]
Pay Date: [Pay Date]
Employee: Chris Janigo
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
  WBF ([hours] hrs × $[rate]/hr)               $[amount]
                                              -----------
TOTAL EMPLOYER TAX COST                        $[amount]

YTD SUMMARY
  YTD Gross Wages (after this period)          $[amount]
  YTD SS Wages Applied to Cap                  $[amount]
  YTD Oregon UI Wages Applied to Cap           $[amount]

Flags: [list or "None"]
Status: DRAFT -- For review before payroll is processed.
Rates applied: [list each rate and its source/year]
```

---

### Step 7 -- Deposit Schedule Note

Based on the federal tax liability for this period, note the applicable deposit schedule:

- If total federal tax liability (employee + employer SS/Medicare + FIT withheld) for the lookback period is under $50,000: **Monthly depositor** -- deposit by the 15th of the following month
- If $50,000 or over: **Semi-weekly depositor** -- deposit by the Wednesday or Friday following pay date
- If total accumulated liability is under $2,500 for the quarter: may pay with Form 941

Flag `RATE_UNCONFIRMED` if the lookback period liability is not known.

---

## S-Corp Payment Classification Reminder

Every payment from Topex Inc. to Chris Janigo must be classified as exactly one of:

| Type | Tax Treatment | This Skill Handles? |
|---|---|---|
| W-2 Wages | Subject to FICA + Oregon payroll taxes | Yes -- this is what this skill produces |
| Distributions | No payroll tax; reported on Schedule E / K-1 | No -- track separately |
| Accountable Plan Reimbursements | Non-taxable if properly documented | No -- use `/expense-classify` |

Never commingle. If a payment is ambiguous, add `DISTRIBUTION_RISK` flag and note it for CPA review.

---

## What This Skill Does NOT Do

- Does not run payroll or initiate ACH/check payments
- Does not submit tax deposits or filings
- Does not determine reasonable compensation -- only flags the gap
- Does not track distributions or reimbursements (separate records)
- Does not file Form 941 or OQ -- use `/quarterly-filing` for that
- Does not give tax advice

---

## Governing Reference

All JSON schemas, flag definitions, hard boundaries, Oregon tax component definitions, and error handling rules are in:
`references/financial-ops-ai-constitution.md`
