---
name: proposal-builder
description: Direct invocation only — RFQ proposals triggered from /email-response run inline there. Use this when building a proposal outside of email triage (e.g., from a phone call or meeting).
---

# Proposal Builder

This skill's full protocol is embedded in `/email-response` and runs automatically when an RFQ is detected there.

When invoked directly (outside of email triage), run the same protocol standalone:

1. Ask Chris for: client name, client email, service type, site/parcel info, any deadline
2. Select template from `templates/` by service type
3. Estimate fee — always flag as `[REVIEW FEE — based on limited info]`
4. Fill template — use `[INSERT: ...]` for gaps; include OHWM language if water present
5. Always include: Part C fee, 50%/50% payment terms, $120/hr add-on, $300/hr expert witness rate, Part D schedule language, Attachment A reference
6. Save to `proposals/YYMMDD-client-name-service-type/README.md` and add row to `proposals/README.md`
7. Present filled proposal, fee estimate, and gaps to Chris

For fee tables, template selection guide, and full field definitions, see `.claude/skills/email-response/SKILL.md` — Proposal-Building Protocol section.
