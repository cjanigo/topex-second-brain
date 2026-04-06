# Fee Estimation Engine — Topex Inc.

Reference for `/proposal-builder` and `/email-response`. Apply this protocol whenever estimating fees for a new scope of work or RFQ.

**Goal:** Produce a defensible internal breakdown Chris can review, and a quoted fee range that covers the actual cost of the work with margin.

---

## Home Base

**Newport, OR** (Lincoln County)

Use this as the origin point for all travel estimates. Adjust if Chris's field staging location differs for a given project.

---

## Step 1 — Identify Base Scope and Fee

Select the row that best matches the service type and site complexity from the email/RFQ.

### Survey — Topo + Boundary

| Complexity | Typical Site | Base Fee | Est. Field Days | Est. Hours |
|---|---|---|---|---|
| Small residential | <1 acre, 1 tax lot, no water, flat | $1,800–$2,500 | 0.5 | 14–20 |
| Standard residential | 1–5 acres, or 2 tax lots | $2,500–$3,500 | 1 | 20–28 |
| Complex residential | Multiple lots, water feature, steep terrain, or OHWM needed | $3,500–$5,500 | 1.5–2 | 28–44 |
| Large or commercial | >10 acres or heavy infrastructure | $5,000+ | 2+ | flag for manual pricing |

### Survey — Boundary Only / ROS / Easements

| Scope | Base Fee | Est. Hours |
|---|---|---|
| Simple boundary stake (1–4 corners) | $1,200–$2,000 | 10–16 |
| Legal description + exhibit map | $800–$1,500 | 7–12 |
| Record of Survey (ROS) | $2,500–$4,000 | 20–32 |
| Property Line Adjustment (PLA) | $3,000–$5,000 | 24–40 |
| Easement (locate + exhibit) | $1,500–$2,500 | 12–20 |

### Engineering

| Scope | Base Fee | Est. Hours |
|---|---|---|
| Small report or analysis | $1,500–$4,000 | 12–32 |
| Design plans (minor, 1–3 sheets) | $3,000–$8,000 | 24–64 |
| Design plans (major, full set) | $7,000–$20,000 | 56–160 |
| Hydraulic model (EPANET or similar) | $4,000–$12,000 | 32–96 |
| City engineering retainer (monthly) | $2,000–$5,000/mo | ongoing |
| Water rights examination | $2,500–$6,000 | 20–48 |
| Expert witness — minimum engagement | $1,200 minimum (4 hrs @ $300/hr) | 4+ hrs at $300/hr |

### Combined Engineering + Survey

Start from the sum of the applicable engineering and survey base fees, then apply a 5–10% combination discount if the scopes share significant field mobilization.

---

## Step 2 — Apply Modifiers

Apply each relevant modifier to the base fee. Modifiers stack multiplicatively except additive ones (marked +$).

### Timeline / Competition

| Factor | Condition | Modifier |
|---|---|---|
| Rush | Deadline < 7 calendar days from RFQ | **1.40x** |
| Rush | Deadline 7–14 calendar days from RFQ | **1.25x** |
| Sole sourced | Client contacted Chris directly, no mention of competing bids | **1.15x** |
| Competitive bid | Client is soliciting multiple firms (RFP/bid process) | **0.95x** (stay competitive) |

**Sole source signals:** client says "I was referred to you," no RFP language, direct personal contact, repeat client, attorney-referred.

### Client Type

| Factor | Condition | Modifier |
|---|---|---|
| Repeat client in good standing | Prior contract, paid on time | **1.0x** (baseline — no change) |
| New client, unknown | First contact, no track record | **1.05x** (risk buffer) |
| Attorney or agency referral | Litigation support, public project | **1.10x** (coordination overhead) |

### Site Conditions

| Factor | Condition | Modifier |
|---|---|---|
| Flat, open, accessible | Clear sight lines, easy access | **1.0x** |
| Steep terrain | Slope >20% | **1.10x** |
| Dense vegetation | Heavy brush, timber, no sight lines | **1.10x** |
| OHWM required | Site borders creek, river, slough, wetland, or tidal area | **+$800–$1,500** (add to base) |
| Difficult access | Locked gates, rough roads, boat access, private land permission needed | **1.15x** |
| Winter / wet season conditions | November through February, or persistent rain forecast | **1.10x** |

### Title Research Data Quality

Apply **after** `/title-research` runs. If title research has not yet run, note the fee as preliminary and flag it.

| Finding | Condition | Modifier |
|---|---|---|
| Rich data, recent surveys | Survey on file < 10 years old, good deed coverage | **0.90x** (easier, cheaper) |
| Adequate data | Survey 10–25 years old, deeds complete | **1.0x** (baseline) |
| Old data only | All surveys > 25 years old, no recent work | **1.10x** |
| Sparse data | Few deeds, no surveys on file, unclear history | **1.20x** |
| No data / no digital records | Nothing in Helion, pre-1977 deeds only, no plats | **1.30x** |
| High adjoiner count | 8 or more adjoining parcels | **+$400–$800** (additional deed research) |
| Low adjoiner count | 3 or fewer adjoining parcels | **-$200** (less research) |
| Pre-1977 deed gap | Records don't go back far enough to confirm chain of title | Flag: +$300–$500 and note public records request may be needed |

**How to read title research output:**
- Check `title-research-[date].md` in the project's Title Reviewing folder
- Look for: date of most recent survey, adjoiner count, data availability flags, any manual download flags
- Apply the matching row above

### Travel and Expenses

Calculate from Newport, OR to the project site.

| Drive Time (one way) | Mileage (round trip est.) | What to Add |
|---|---|---|
| < 30 min | < 40 miles RT | No surcharge |
| 30–60 min | 40–90 miles RT | +$0.70/mile (IRS rate) |
| 60–90 min | 90–150 miles RT | +$0.70/mile + 1 hr travel time @ $120/hr each way |
| > 90 min | > 150 miles RT | +$0.70/mile + full travel time @ $120/hr + flag for potential overnight |
| Multi-day field work, distant site | Overnight required | +$150/day per diem + lodging estimate |

**How to estimate drive time:** Use site address and approximate Oregon geography:
- Lincoln County coast (Newport, Lincoln City, Waldport, Depoe Bay): < 30 min, no surcharge
- Lincoln County inland (Toledo, Siletz, Harlan, Elk City): 15–45 min, minimal
- Polk County (Dallas, Falls City, Salem area): 60–90 min, add travel
- Benton County (Corvallis, Philomath): 60 min, add travel
- Beyond Lincoln/Polk/Benton: flag for manual review, assume overnight if > 2 hrs

For driving distance/time, use WebSearch ("driving time Newport OR to [address]") if needed for accuracy.

---

## Step 3 — Build Internal Breakdown

Produce this block internally (show to Chris, do not include in client-facing proposal):

```
## Fee Estimate Breakdown — [Client Name] / [Service Type]
Date: [today]

Base Scope: [describe what's included]
Base Fee Range: $X,XXX to $X,XXX
Est. Field Days: X | Est. Total Hours: XX–XX hrs

Modifiers Applied:
- [Rush / Sole source / Client type]: x[multiplier] (+$XXX)
- [Site condition factor]: x[multiplier] (+$XXX)
- [Title research finding]: x[multiplier] (+/- $XXX)
- Travel ([X miles RT, ~X min each way]): +$XXX

Running Total: $X,XXX to $X,XXX

OHWM / special add-ons: +$XXX (if applicable)

Recommended Quote: $X,XXX fixed  OR  $X,XXX–$X,XXX range
(Choose fixed fee when scope is well-defined; range when info gaps remain)

Risk Flags:
- [List anything that could blow the scope: data gaps, access uncertainty, permit coordination, etc.]

Status: [PRELIMINARY — title research not yet run] OR [UPDATED — title research complete]
```

**Rounding rule:** Round the final number to the nearest $100 (for fees under $5,000) or $500 (for fees over $5,000). Odd numbers look unconfident.

---

## Step 4 — Set the Quote Flag

| Condition | Flag |
|---|---|
| Scope is clear, modifiers applied, title research complete | Ready to quote — include in proposal |
| Scope is clear but title research not yet run | `[PRELIMINARY FEE — pending title research]` |
| Large commercial, >$15,000, or unusual scope | `[FLAG FOR CHRIS — manual pricing recommended]` |
| Expert witness (billed hourly) | Always quote as hourly at $300/hr with minimum engagement |
| City engineering retainer | Always monthly; never fixed total |

---

## Step 5 — Travel and Expense Language for Proposal

If travel costs apply (drive > 30 min one way), add this to the proposal Part C:

> "Reimbursable expenses including mileage at the current IRS rate and any lodging or per diem for field work requiring overnight travel will be billed at cost in addition to the fee above."

If no travel costs: omit this line.

---

## Industry Context (PNW / Oregon Reference)

These benchmarks inform the base tables above. Do not quote these to clients — they are for calibration only.

- Oregon PLS hourly rate (solo): $100–$160/hr market rate; Chris bills at $120/hr
- Two-person survey crew (if subcontracted): $180–$250/hr
- Civil engineering (PE): $130–$200/hr Oregon market; Chris's SOWs use $120/hr add-on rate
- Expert witness (PE/PLS): $250–$400/hr Oregon; Chris quotes $300/hr
- IRS mileage 2025: $0.70/mile
- Sole-source premium: 10–20% above competitive-market pricing is standard for direct-referral professional services
- Rush premium: 25–50% for expedited turnaround is industry standard for small engineering/survey firms
- Data scarcity premium: undocumented property boundaries require additional research, field time, and professional judgment — 20–30% premium is defensible
- Recent nearby survey discount: when a licensed surveyor has already established monuments in the area within 10 years, retracement is faster and cheaper — 10–15% reduction is appropriate
