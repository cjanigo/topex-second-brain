# Decision Log

Append-only. When a meaningful decision is made, log it here.

Format: [YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...

---

[2026-04-01] DECISION: Built research skill as first custom skill | REASONING: Research is a high-value, time-consuming task that spans all project types; a structured multi-step protocol beats ad hoc searching and produces more reliable, actionable results | CONTEXT: Skill lives at .claude/skills/research/SKILL.md; classifies research by type (technical, regulatory, water rights, legal, operational, site-specific), loads current project context before searching, executes in 4 passes, and synthesizes into a standardized output format

[2026-04-02] DECISION: Added 26012 Twin Rocks Friends Camp as active project | REASONING: SOW dated 2026-03-15 for Hwy 101 approach design and ODOT permitting; 50% down payment received, work scheduled to begin week of 2026-04-20 | CONTEXT: $3,663 fixed fee; Tasks: site design, retaining wall design, ODOT permitting; one revision included before stamped construction set; dune overlay zone applies

[2026-04-02] DECISION: Created proposals/ folder and proposal tracking system | REASONING: Proposals sent to potential clients were not being tracked; need to know win rate, which proposals expired, and what to improve for future proposals | CONTEXT: proposals/ folder parallel to projects/; each proposal gets a dated folder (YYMMDD-client-name-service-type) with README.md; 30-day rule = no signed project within 30 days means Expired; Ramon Sera topo survey (P26001, sent 2026-03-03) is first entry (status: Won, became project 26007)

[2026-04-02] DECISION: Built proposal-builder and proposal-review skills | REASONING: Drafting proposals from scratch is a time drain; RFQ emails should immediately trigger a draft SOW; monthly review of lost proposals reveals patterns to improve win rate | CONTEXT: proposal-builder called automatically from email-response when RFQ keywords detected; proposal-review runs monthly to mark expired proposals and analyze win rate by service type and fee range; both skills documented in .claude/skills/

[2026-04-02] DECISION: Follow up on all proposals 7 days after sending | REASONING: P26002 (Ocean Equity Investments) expired with no response and no follow-up — a simple check-in would have kept the door open | CONTEXT: Rule added to proposals/README.md; follow-up dates should be logged in each proposal README; second follow-up at 14 days if still no response

[2026-04-02] DECISION: Updated gantt-sync to include pending proposals as tentative calendar events | REASONING: Proposals represent potential work that affects scheduling capacity; showing them as tentative on calendar prevents overbooking if multiple proposals are pending simultaneously | CONTEXT: Tentative events tagged proposal-id: [folder-name] in description; title prefix [PROPOSAL]; removed automatically by gantt-sync when proposal is Won or Expired
