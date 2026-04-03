# Proposal Builder Skill

## What This Is

Drafts a complete Topex Inc. scope of work and saves a proposal tracking entry when Chris receives a request for quote (RFQ) or request for proposal (RFP). Surfaces the draft for review — nothing goes to the client until Chris approves and sends it.

This skill is called automatically from `/email-response` when an RFQ is detected. It can also be invoked directly.

---

## How to Invoke

**Directly:**
```
/proposal-builder
```

**Called from email-response** (pass context from the triggering email):
```
/proposal-builder [client name] [service type] [email thread summary]
```

---

## RFQ Detection (for email-response integration)

When `/email-response` is processing an email, flag it as an RFQ if any of the following are present in the subject or body:

**High-confidence signals:**
- "quote", "proposal", "RFQ", "RFP", "scope of work", "what would you charge", "how much", "price", "cost estimate", "fee"
- "are you available", "do you do", "can you help with"

**Supporting signals (combine with the above):**
- New sender (not in any active project contact list)
- No prior thread history
- Mentions a parcel, address, tax lot, property, survey, or engineering need

If flagged as RFQ: **do not draft a reply email.** Instead, call `/proposal-builder` with the relevant context and show the proposal draft for Chris's review.

---

## Execution Protocol

### Step 1 — Gather Information

Collect from the email (or from Chris if invoked directly):

| Field | Source |
|---|---|
| Client name | Email sender name |
| Client email | Email From address |
| Client address | Email body (if provided) |
| Service requested | Email body — what did they ask for? |
| Site/parcel info | Tax lot number, address, or location |
| Any scope specifics | Size, complexity, special requirements mentioned |
| Deadline or urgency | Any dates mentioned |

If any critical fields are missing (client name, service type, or site location), ask Chris before proceeding. List the gaps clearly:

> To build the proposal, I need:
> - Client's mailing address
> - Which county the property is in
> - Approximate parcel size

---

### Step 2 — Select Template

Match the service type to the right template:

| Service Type | Template |
|---|---|
| Topographic survey (with or without boundary) | `templates/survey-sow-topo.md` |
| Boundary survey, ROS, easement, legal description | `templates/survey-sow.md` |
| Civil engineering (design, plans, analysis) | `templates/engineering-sow.md` |
| Expert witness / litigation support | `templates/expert-witness-sow.md` |
| Combined engineering + survey | `templates/engineering-survey-combined-sow.md` |

If the service type is ambiguous, make a reasonable selection and flag it for Chris.

---

### Step 3 — Estimate Fee

Use the fee guidelines below as a starting point. Adjust up for complexity, travel, or access issues. Adjust down for simple sites or repeat clients.

**Survey fees (topo + boundary):**
| Site Size / Complexity | Fee Range |
|---|---|
| Small residential parcel (<1 acre, single tax lot, no water features) | $1,800 to $2,500 |
| Standard residential (1 to 5 acres, or two tax lots) | $2,500 to $3,500 |
| Complex (multiple tax lots, water feature, steep terrain, or OHWM needed) | $3,500 to $5,500 |
| Large or commercial | $5,000+ (flag for Chris to price manually) |

**Survey fees (boundary only, ROS, easements):**
| Scope | Fee Range |
|---|---|
| Simple boundary stake (1 to 4 corners) | $1,200 to $2,000 |
| Legal description + exhibit | $800 to $1,500 |
| Record of survey | $2,500 to $4,000 |

**Engineering fees:**
| Scope | Fee Range |
|---|---|
| Small report or analysis | $1,500 to $4,000 |
| Design plans (minor) | $3,000 to $8,000 |
| Hydraulic model | $4,000 to $12,000 |
| City engineering (monthly) | $2,000 to $5,000/month |

Always flag the fee as a draft estimate. Insert the number but note: `[REVIEW FEE — based on limited info]`.

---

### Step 4 — Fill the Template

Fill in the selected template with all available information. Replace every `[PLACEHOLDER]` field.

**Include OHWM language** if: site borders a creek, slough, river, wetland, or tidal area.
**Include volume calc language** if: client mentions grading, fill, cut, stockpile, or elevation change.
**Include drone/UAS language** if: site is large or has access issues where aerial data would help.

For anything uncertain, insert: `[INSERT: ...]`

**Always include:**
- Part C fee with standard payment terms (50% down, 50% on delivery)
- $120/hr add-on rate
- $300/hr expert witness rate
- Part D schedule language (begin upon signed SOW and down payment)
- Attachment A reference (General Terms and Conditions)

---

### Step 5 — Save Proposal Entry

After generating the draft proposal text, create a new proposal folder entry:

1. Determine the proposal folder name: `YYMMDD-client-name-service-type` (today's date)
2. Generate the next sequential proposal ID from `proposals/README.md` (e.g., P26002)
3. Create `proposals/[folder-name]/README.md` using `templates/proposal-readme.md` — fill in all known fields, status = Pending
4. Add a row to the `proposals/README.md` index table with Status: Pending and no linked project

---

### Step 6 — Output to Chris

Present:

1. **Filled proposal text** — ready to paste into Word or convert to PDF using the Topex SOW format
2. **Fee estimate** — with a flag if it needs manual review
3. **Gaps to fill** — any `[INSERT: ...]` placeholders that need Chris's input before sending
4. **Next steps:**
   - Review and adjust the proposal
   - Export to PDF (use Topex letterhead format)
   - Send to client
   - After sending, confirm the send date is recorded in `proposals/[folder]/README.md`

**Do not save a Gmail draft for the proposal itself** — proposals are attached as PDF, not sent inline. The email-response skill will handle any cover email once Chris is ready to send.

---

## After the Proposal Is Sent

Chris should update the proposal README manually (or ask Claude to update it):
- Set `Sent:` to the actual send date
- Set `Expiry:` to sent date + 30 days
- Update `proposals/README.md` index row

When the client signs:
- Update status to Won
- Create a project folder: `projects/NNNNN-client-name/README.md`
- Link the project in the proposal README
- Remove any tentative calendar events (gantt-sync will handle on next run)

---

## Notes

- This skill drafts the SOW text. Formatting into PDF with Topex letterhead is done manually in Word.
- All proposals are tracked in `proposals/` regardless of outcome.
- The `/proposal-review` skill handles monthly cleanup (marking expired, analyzing patterns).
- Fee estimates in this skill are guidelines, not quotes. Chris always reviews before sending.
