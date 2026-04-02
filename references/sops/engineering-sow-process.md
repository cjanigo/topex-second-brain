# SOP: Engineering Scope of Work Process

_How to write, send, and track an engineering scope of work at Topex Inc._

---

## When to Use This SOP

Any time a client requests civil engineering services (analysis, design, modeling, reporting) that require a written agreement before work begins. Distinct from survey SOWs, which use the survey-sow-process SOP.

---

## Step 1: Scope the Work

Before writing anything, clarify:

- What is the deliverable? (report, concept plans, cost estimates, engineered drawings, permit application)
- What data is available? (LIDAR, GIS, as-builts, survey, field data)
- Is field work needed? If yes, add a field task and coordinate scheduling.
- How many agencies are involved? Each round of agency review = potential scope expansion.
- Is there a hard deadline? If yes, note it in the schedule section.

---

## Step 2: Write the Scope

Use `templates/engineering-sow.md` as the starting point.

Structure:

| Section | Content |
|---|---|
| Overview | 2-3 sentences: problem, site context, approach |
| Task 1 | Project management (boilerplate - always include) |
| Task 2+ | Technical tasks (be specific about methods and outputs) |
| Last Task | Reimbursable (boilerplate - always include) |
| Part B | Fee proposal and invoice terms |
| Part C | Schedule and authorization |
| Attachment A | General Terms and Conditions |

**Fee guidance:**
- Fixed Fee for well-defined desktop studies
- Time and Materials or NTE for open-ended work or multiple agency iterations
- Always include 9% late charge language

**Common task types:**

| Task Type | Notes |
|---|---|
| Parking analysis | Include ADA + municipal code review; use DOGAMI LIDAR if no survey |
| Hydraulic modeling | Specify model type (EPANET, HEC-RAS), scenarios, and deliverable format |
| Feasibility study | 30% cost estimates are appropriate; note +/- tolerance |
| City engineering support | Usually T&M; define deliverable as "staff support hours" |
| Drainage design | Specify design storm, jurisdiction standards, and permit pathway |

---

## Step 3: Send the Scope

- Send as PDF (branded Topex letterhead)
- Include Attachment A (General Terms and Conditions) every time
- Ask for signature and return via email
- For fixed fee work: include payment instructions in the cover email

---

## Step 4: Track Signature and Payment

- When signed scope is returned, note the date in the project README
- For fixed fee: confirm first payment before scheduling work
- For monthly billing: note start date in project README

---

## Step 5: Create the Project

Once signed:

1. Create `projects/[NNNNN]-[client-slug]/README.md` using the standard project README format
2. Add deliverables checklist to the README
3. Add schedule from Gantt or estimated timeline
4. File the signed PDF scope in the project folder (Google Drive or local)

---

## Combined Engineering and Survey Scopes

When a project requires both field surveying and civil engineering design (e.g., park improvements, site grading, ADA upgrades), use the combined template instead of the engineering-only template:

- Template: `templates/engineering-survey-combined-sow.md`
- Use T&M do-not-exceed (not fixed fee) — design unknowns make fixed fee risky
- Always itemize Survey Equipment Fee and Technology Fee separately in the fee table
- Tie equipment layout to manufacturer specs to limit liability if the equipment design changes
- ESC plan belongs in the design task, not a separate task

## Reference Examples

- CAC Parking Lot Analysis (2026): `references/examples/engineering-sow-cac-parking-2026.md`
  - Desktop-only, fixed fee, multi-agency coordination, 30% cost estimates

- Coast Park Playground Survey and Civil Site Design (2026): `references/examples/engineering-sow-coast-park-2026.md`
  - Combined survey + site design, T&M do-not-exceed, public client, ADA + ESC, bidding support included

---

## Common Mistakes to Avoid

- Forgetting Attachment A (General Terms and Conditions) - always attach
- Not specifying data sources for desktop studies - creates expectation mismatch
- Leaving agency coordination rounds open-ended - each round should be explicitly scoped or flagged as a potential amendment trigger
- Starting work before signed scope is returned
