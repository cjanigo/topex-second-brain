# Expert Witness Scope Writer Skill

**Status: Complete**

## What This Is

A scope of work generation skill for Chris Janigo, PE/PLS at Topex Inc. Given a project type and key parameters, this skill produces a complete, professional scope of work document ready for client delivery — including compensation terms, general conditions, and standard Topex language.

Supported project types:
- Expert witness and litigation support
- Civil engineering (design, reports, hydraulic modeling)
- Land surveying (boundary, record of survey, plat)
- Water rights examination or consulting
- City engineering
- Erosion and sediment control
- Drone / UAS services

---

## How to Invoke

```
/expert-witness-scope-writer [key parameters]
```

Examples:
- `/expert-witness-scope-writer overburden stockpile volumetric analysis, Tax Lot 801, Oregon`
- `/expert-witness-scope-writer boundary dispute, parcel survey, Lincoln County, WA`
- `/expert-witness-scope-writer water rights examination, deposition testimony`
- `/expert-witness-scope-writer` — prompts Chris for project details interactively

---

## Execution Protocol

### Step 1 — Gather Inputs

Collect the following before drafting. If any are missing and the user hasn't provided them, ask:

| Input | Required | Notes |
|---|---|---|
| Project type | Yes | Determines template and services |
| Client name | Yes | Full legal name for agreement header |
| Client address | Yes | For agreement header |
| Client email | Yes | For agreement header |
| Project description | Yes | Location, parcel/tax lot, subject matter |
| Governing state | Yes | Oregon or Washington — affects law section |
| Attorney / counsel name | If expert witness | For agreement header |
| Estimated hours by task | Optional | Helps set retainer; can be estimated |
| Special scope items | Optional | Any deliverables beyond the standard set |

If Chris provides a project description or drops in a PDF, extract what you can and ask only for what's missing.

### Step 2 — Select Template

Match the project type to a template:

| Project Type | Template |
|---|---|
| Expert witness / litigation support | See Expert Witness Template below |
| Boundary survey / record of survey | Use survey template structure |
| Civil engineering design | Use engineering template structure |
| Hydraulic modeling | Use engineering template structure |
| Water rights examination | Use water rights template structure |
| City engineering | Use engineering template structure |

For project types without a dedicated template yet, build from the Expert Witness template structure, adapting the scope section and rates.

### Step 3 — Fill and Draft

Populate the template with provided inputs. Follow these rules:

- Use the client's full legal name exactly as provided
- Dates: use the date Chris specifies, or leave a blank `__________` for manual fill
- Rates: use Chris's standard rates (see Rate Sheet below) unless he specifies otherwise
- Governing law: match to the project state (Oregon or Washington)
- Retainer: calculate as approximately 10 hours of primary work rate, rounded to nearest $500. Default $4,000 for expert witness. Flag if the scope suggests more.

### Step 4 — Output

Produce the full scope of work as clean markdown. Structure:

1. Header (Topex Inc., date, client address block)
2. Agreement title and parties
3. Numbered sections per template
4. General Terms and Conditions (standard Topex T&C — use boilerplate below)
5. Signature blocks

After the document, output a short note to Chris:

> **Review before sending:**
> - [list any blanks left for Chris to fill]
> - [flag any rates or retainer that may need adjustment]
> - [note if scope is broad enough to warrant a higher retainer]

---

## Rate Sheet (Standard Topex Rates)

| Service | Rate |
|---|---|
| Professional analysis / consulting | $225/hr |
| Report preparation / revisions | $225/hr |
| Declaration / affidavit preparation | $250/hr |
| Testimony (deposition, hearing, trial, Zoom) | $300/hr (2hr minimum) |
| Field survey (principal surveyor) | $185/hr |
| CAD drafting | $150/hr |
| GIS / mapping | $150/hr |
| Expert research | $225/hr |
| Travel time | $150/hr |

Billing increment: 0.25-hour for all services.

Update this rate sheet if Chris specifies new rates.

---

## Expert Witness Template

```
TOPEX INC.
SCOPE OF WORK
[Date]

To: [Client Legal Name]
    [Address Line 1]
    [City, State ZIP]
    [Email]

EXPERT WITNESS & LITIGATION SUPPORT AGREEMENT

This Expert Witness & Litigation Support Agreement ("Agreement") is entered into as of [Date], by and between:

Client: [Client Legal Name]
Counsel: __________________________, by attorney [Attorney Name]
Expert: Chris Janigo, PE, PLS, CWRE ("Expert")

1. Scope of Engagement

Expert is retained to provide professional [services description] related to [subject matter], including but not limited to:

- [Service item 1]
- [Service item 2]
- [Service item 3]
- Preparation of supplemental and final expert reports
- Preparation of declarations or affidavits
- Testimony by deposition, hearing, or trial (including by Zoom)

2. Nature of Engagement

Expert is engaged as an independent expert witness in anticipation of litigation. All opinions will be formed independently and based on Expert's professional judgment.

3. Compensation

Client agrees to compensate Expert at the following rates:

- Professional analysis / consulting: $225 per hour
- Report preparation / revisions: $225 per hour
- Declaration / affidavit preparation: $250 per hour
- Testimony (deposition, hearing, trial, Zoom): $300 per hour
  - Two (2) hour minimum per testimony event

Time is billed in 0.25-hour increments.

4. Retainer

Client shall pay an initial retainer of $[amount] upon execution of this Agreement. The retainer will be applied to the final invoice. Expert may require replenishment of the retainer prior to testimony or additional work.

Expert reserves the right to suspend work if invoices are unpaid or the retainer is exhausted.

5. Expenses

Client shall reimburse reasonable out-of-pocket expenses, including but not limited to data acquisition, software processing costs, and document reproduction. Any travel expenses will be billed separately if required.

6. Report Status

All reports are considered preliminary and draft until finalized in writing by Expert. Drafts are not intended for disclosure unless agreed to in writing by Expert and counsel.

7. Testimony

Expert agrees to testify truthfully and in accordance with professional standards. Compensation is not contingent upon the outcome of the matter or the substance of Expert's opinions.

8. Confidentiality

Expert shall maintain the confidentiality of all non-public information provided in connection with this engagement, except as required by law or court order.

9. No Legal Services

Expert is not providing legal advice and does not represent Client in any legal capacity.

10. Governing Law

This Agreement shall be governed by and construed in accordance with the laws of the State of [Oregon/Washington].

AGREED AND ACCEPTED:

Client / Counsel:
Signature: ___________________________
Name & Title: ________________________
Date: _______________________________

Expert:
Signature: ___________________________
Name: Chris Janigo
Date: _______________________________
```

---

## Standard Topex General Terms and Conditions (Boilerplate)

Append verbatim after the signature block. For Washington projects, replace "state of Oregon" in Section 16.1 with "state of Washington".

```
TOPEX INC. – GENERAL TERMS AND CONDITIONS

1. Force Majeure. TOPEX Inc.'s fees, costs, and schedule are subject to equitable adjustments, up to and including termination of the Agreement, for delays caused by occurrences or circumstances beyond TOPEX Inc.'s reasonable control, such as fires, floods, earthquakes, strikes, riots, war, terrorism, threat of terrorism, acts of God, acts or regulations of a governmental agency, emergency, security measures or other circumstances, including, without limitation, unusual weather conditions ("Force Majeure").

2. Invoices and Payment.

2.1. Unless otherwise agreed in writing, prepayment for Services is required. Should the Parties agree for Services to be billed monthly, invoices will be payable within thirty (30) days of receipt by the Client. If the Client objects to any portion of an invoice, the Client shall notify TOPEX Inc. in writing within seven (7) business days from the date of receipt of the invoice, and shall state the reasons for the objection, and timely pay the portion of the invoice that is not in dispute. The Parties shall work together in good faith to settle the disputed portion of any invoice.

2.2. Invoiced charges not paid within the time periods set forth in Section 2.1, shall be deemed delinquent and accrue interest at a rate of nine percent (9.0%) per month, or the maximum amount allowed by applicable law, whichever is less. Late payments shall be first applied to accrued interest and then to unpaid principal. Interest charges will not apply to any disputed portion of an invoice, to the extent the dispute is resolved in favor of the Client.

3. Termination.

3.1. Either Party may terminate the Agreement for cause by written notice to the other Party (i) upon breach by the other Party of a material obligation under the Agreement, (ii) if the other Party goes into bankruptcy, is liquidated or is otherwise unable to pay its debts as they become due, or (iii) if the other Party resolves to appoint or has appointed for it an administrator, receiver or other similar officer affecting the Party's business, property or assets in a manner that affects or could affect the Party's ability to pay its debts as they become due or its ability to fulfill its obligations under this Agreement or a contract integrating this Agreement.

3.2. Client may terminate the Agreement for its convenience upon five (5) business days' written notice to TOPEX Inc., in which event Client shall pay all fees and expenses for Services accrued as of the termination date and TOPEX Inc.'s reasonable costs resulting from termination, including, without limitation, demobilization costs, as detailed in a final invoice.

4. Insurance. During the term of this Agreement, TOPEX Inc. shall, at its own expense, maintain and carry the insurance as set forth below. TOPEX Inc. will furnish certificates of such insurance or policy declaration pages upon request.

| Type | Limits |
|---|---|
| Worker's Compensation | Statutory Limit |
| Employer's Liability — Bodily Injury by Accident | $1,000,000 |
| Employer's Liability — Bodily Injury by Disease (Each Employee) | $1,000,000 |
| Employer's Liability — Bodily Injury by Disease (Policy Limit) | $1,000,000 |
| Commercial General Liability incl. Contractual Liability, Broad Form Property Damage, and Completed Operations | $1,000,000 (Combined Single Limit) / $2,000,000 (General Aggregate) |
| Automobile Liability incl. Bodily Injury/Property for Owned, Hired, and Non-Owned Vehicles | $1,000,000 (Combined Single Limit) |
| Professional Liability (Errors and Omissions) — Per Claim / Aggregate | $3,000,000 / $3,000,000 |

5. Indemnification; Limitation of Liability.

5.1. Each Party (each the "Indemnifying Party") shall indemnify the other, its affiliates and their respective directors, officers, and employees (individually, an "Indemnitee" and collectively, "Indemnitees") from and against Claims arising out of the Agreement, to the extent Claims are caused by the negligence, breach of contract, or willful misconduct of the Indemnifying Party. The foregoing does not include attorney's fees or other fees.

5.2. Neither Party shall be liable to the other, including without limitation, insurers, for any lost, delayed, or diminished profits, revenues, business opportunities or production or for any incidental, collateral, special, indirect, punitive, exemplary, financial, consequential, or economic losses or damages of any kind or nature whatsoever, however caused regardless of whether the Indemnitee, as applicable, knew or should have known of the possibility of such losses or damages.

5.3. A TOPEX Inc. Indemnitee will not be liable to a Client Indemnitee or anyone claiming by, through or under it, including without limitation, insurers, for any amount in excess of two hundred fifty thousand dollars ($250,000) in the aggregate.

5.4. The provisions of this Section will (i) apply to the fullest extent allowed by law, and (ii) survive the completion of Services and the expiration, cancellation, or termination of the Agreement.

6. Standard of Care. TOPEX Inc.'s Services shall be performed using the degree of care and skill ordinarily exercised by other members of the engineering, science, and land surveying professions providing substantively similar Services in the same locality and time, subject to the time limits and financial and physical constraints applicable to the Services and Project. TOPEX Inc. makes no representations and provides no warranties or guarantees other than those expressly set forth herein.

7. Client Responsibilities.

7.1. Client shall assist TOPEX Inc. in connection with Services as reasonably necessary, including, without limitation, as specified in the authorized Proposal. If applicable to the Services, Client will provide TOPEX Inc.:

A. Specifications (including, without limitation, facility schematics, Site schematics, engineering drawings and plot plans) detailing the construction of underground and aboveground facilities located at the Site that pertain to TOPEX Inc.'s Services or are necessary to enable TOPEX Inc. to perform the Services.

B. All information related to the Services in Client's possession, custody or control reasonably required by TOPEX Inc. or which Client knows would affect the accuracy or completeness of Services.

7.2. Site Access.

A. Client shall provide reasonable ingress to and egress from the Site for TOPEX Inc. and its subcontractors and their respective personnel, equipment, and vehicles, including but not limited to obtaining any site access, consents or easements and complying with their terms. If Client does not own the project site, Client warrants and represents to TOPEX Inc. that Client has the authority and permission of the owner and occupant of the project site to grant this right of entry to TOPEX Inc.

B. Client acknowledges that TOPEX Inc.'s ability to comply with the schedule for performance of Services is contingent upon timely and complete Site access. TOPEX Inc. shall not be responsible for damages or delays arising from the Client's actions or inactions regarding Site access. Depending on the Services to be performed in connection with the Project, TOPEX Inc.'s Proposal may require that an authorized, knowledgeable representative of the Site owner be present during some or all of the on-site activities.

7.3. Client warrants and represents that all information provided by, on behalf of, or at the request of Client or any governmental agency to TOPEX Inc. (including any TOPEX Inc. subcontractor), shall be accurate and complete. TOPEX Inc. has the right to rely on such information, without independent investigation, verification, or inquiry.

13. Use of Name. Client authorizes TOPEX Inc. to use Client's name, and a general description of the Services and subject matter thereof, as a reference for prospective clients and projects.

14. Work Product.

14.1. Client agrees that TOPEX Inc. shall retain ownership rights in all deliverables conceived, developed, or made by TOPEX Inc. and its affiliates during performance of the Services including all documents, data, calculations, field notes, estimates, work papers, reports, materials, methodologies, technologies, know-how and all other information prepared, developed, or furnished by or on behalf of TOPEX Inc. ("Work Product").

14.2. Upon its receipt of payment in full for the Services, TOPEX Inc. shall grant Client a non-exclusive, royalty-free license to use such work product only for the Project, as specified by the authorized Proposal, for the purposes for which was prepared by TOPEX Inc.

14.3. Work Product is created solely for the purposes of TOPEX Inc.'s performance of the Services. Any unauthorized changes made by Client to, and any re-use by Client of, the Work Product, shall be at Client's sole risk and without liability to TOPEX Inc.

15. Severability. If one or more provisions of this Agreement is determined to be invalid, unlawful, or unenforceable in whole or in part, the validity, lawfulness, and enforceability of the remaining provisions (and of the same provision to the extent enforceable) will not be impaired, and the Parties agree to substitute a provision as similar in intent to the subject provision as possible without compromising the validity or enforceability of the substitute provision.

16. Governing Law; Conflict Resolution.

16.1. The Agreement is governed by and shall be construed in accordance with the laws of the state of [Oregon/Washington] in which the Project is located. The state of [Oregon/Washington] courts in which the Project is located have exclusive jurisdiction and venue over all disputes arising out of the Agreement and is deemed to be the place of performance for all obligations under the Agreement. The Parties waive any objection to this section on grounds of inconvenient forum or otherwise.

16.2. The Parties agree that all disputes arising under the Agreement shall be submitted to nonbinding mediation unless the Parties mutually agree otherwise. The Parties agree to waive their rights to a jury trial of any conflict related hereto.

16.3. As to any dispute involving Client or the subject matter of the Services in which TOPEX Inc. is either not a named party or not at fault, Client shall reimburse TOPEX Inc. for any reasonable attorney's fees, other legal fees and expenses, and other costs incurred and the time of TOPEX Inc.'s personnel spent in responding, defending, or participating in subpoenas, depositions, examinations, appearances or production of documents/records.

17. Miscellaneous.

17.1. Subcontracts. TOPEX Inc. may subcontract all or any part of the Services without the prior written approval of Client, but such subcontracting shall not relieve TOPEX Inc. of any of its obligations under this Agreement.

17.2. Entire Agreement. The Agreement, including approved Proposals, constitutes the entire understanding between the Parties and the full and final expression of such understanding, and supersedes all prior and contemporaneous agreements, representations, or conditions, express or implied, oral, or written.

17.3. Waiver; Amendment. A provision of this Agreement may be waived, deleted, or modified only by a document signed by the Parties stating their intent to modify the Agreement.

17.4. Survival. All provisions of this Agreement that by their nature would usually be construed to survive an expiration or termination shall survive the expiration or termination of the Agreement.

17.5. Notices. Unless TOPEX Inc. is directed otherwise, any required Notices provided hereunder will be made in writing to the persons identified in the Proposal and delivered by electronic mail, first class mail, or such services as may be agreed by the Parties.
```

---

## Output Format Rules

Follow `.claude/rules/communication-style.md`:
- Formal document language — no casual tone, no emojis, no dashes in prose
- Tables for rate schedules
- Short, numbered sections
- No trailing summaries in the document itself — review notes go after the document, clearly separated

---

## When to Ask Before Drafting

Ask Chris first when:
- Project type is ambiguous between engineering and expert witness (different rate structures)
- Governing state is unclear from context
- Retainer amount seems unusually high or low for the described scope
- Client is a government entity (may need modified T&C)
