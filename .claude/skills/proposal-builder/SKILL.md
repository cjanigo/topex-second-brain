---
name: proposal-builder
description: Direct invocation only — RFQ proposals triggered from /email-response run inline there. Use this when building a proposal outside of email triage (e.g., from a phone call or meeting).
---

# Proposal Builder

This skill's full protocol is embedded in `/email-response` and runs automatically when an RFQ is detected there.

When invoked directly (outside of email triage), run the same protocol standalone:

1. Ask Chris for: client name, client email, service type, site address/parcel info, any deadline, and whether this is sole-sourced or competitive
2. Select template from `templates/` by service type (see `/email-response` SKILL.md for the template map)
3. **Estimate fee using the Fee Estimation Engine** (see `references/fee-estimation.md` — follow all five steps):
   - Select base scope and fee from the tables
   - Apply modifiers: rush/deadline, sole source, client type, site conditions, travel from Newport OR
   - Apply title research modifiers if `/title-research` has been run on this property
   - Build the internal breakdown block and show it to Chris before filling the proposal
   - Set the appropriate quote flag (ready, preliminary, flag for manual review, or hourly)
4. Fill template — use `[INSERT: ...]` for gaps; include OHWM language if water present
5. Always include: Part C fee, 50%/50% payment terms, $120/hr add-on, $300/hr expert witness rate, Part D schedule language, Attachment A reference
6. If the proposal involves a Lincoln County property and title research has not been run yet:
   - Mark the fee as `[PRELIMINARY — pending title research]`
   - Remind Chris to run `/title-research [identifier]` after opening the portal links
   - Note that the fee will be updated once title research results are available
7. Save to `proposals/YYMMDD-client-name-service-type/README.md` and add row to `proposals/README.md`
8. Present to Chris:
   - Internal fee breakdown (not for client)
   - Filled proposal text (ready to paste into Word / export as PDF)
   - Any `[INSERT: ...]` gaps to fill before sending
   - Next steps: review, export to PDF with Topex letterhead, send to client; update proposal README with send date after sending

For template selection guide and full field definitions, see `.claude/skills/email-response/SKILL.md` — Proposal-Building Protocol section.
For fee tables, modifiers, travel formula, and breakdown format, see `references/fee-estimation.md`.
