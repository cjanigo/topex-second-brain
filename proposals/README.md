# Proposals — Topex Inc.

_Proposals sent to potential clients. Updated by `/proposal-builder` when a proposal is drafted._

**Rule:** If a proposal has not converted to a signed project within 30 days of the sent date, it is assumed lost and marked `Expired`. The `/proposal-review` skill handles this monthly.

**Rule:** Any proposal (Won, Lost, or Expired) with a sent date older than 30 days is moved to `archives/proposals/` during `/proposal-review`. Pending proposals are never archived until they expire first.

**Rule:** Follow up with the client 7 days after sending a proposal. If no response, follow up again at 14 days. Log follow-up dates in the proposal README.

**Rule:** Any calendar blocks scheduled for proposal-stage work must be marked `(TENTATIVE)` in the event title and include a note in the description. Remove tentative status only after the contract is fully executed AND the down payment is received. See `.claude/rules/proposal-calendar-tentative.md`.

---

## Active Proposals (Pending)

| Proposal ID | Client | Service | Fee | Sent | Expiry |
|---|---|---|---|---|---|
| [P26006](260320-emerio-boundary-topo-subdivision/README.md) | Emerio (Jennifer Arnold) | Boundary, Topo, ROS, Subdivision Plat | $42,350 | 2026-03-20 | 2026-04-19 |

---

## All Proposals

| Proposal ID | Client | Service | Fee | Sent | Expiry | Status | Project |
|---|---|---|---|---|---|---|---|
| [P26001](260303-ramon-sera-topo-survey/README.md) | Ramon Sera | Topo + Boundary Survey | $2,600 | 2026-03-03 | 2026-04-03 | Won | [26007](../projects/26007-ramon-sera-topo-survey/) |
| [P26002](260223-ocean-equity-subdivision-tentative-plan/README.md) | Ocean Equity Investments (Brodie Beckstead) | Subdivision Tentative Plan — Engineering | $1,500 retainer + addendum | 2026-02-23 | 2026-03-25 | Expired | — |
| [P26003](260309-cac-lincoln-county-parking-analysis/README.md) | Children's Advocacy Center of Lincoln County (Paul Schrader) | Parking Alternatives Analysis — Engineering | $10,000 | 2026-03-09 | 2026-04-08 | Won | [26009](../projects/26009-cac-parking-lot/) |
| [P26004](260327-doug-peterson-boundary-survey/README.md) | Doug Peterson | Boundary Survey Stakeout + Survey Map | $2,250 | 2026-03-27 | 2026-04-26 | Won | [26015](../projects/26015-peterson-boundary-survey/) |
| [P26005](260210-sandpoint-douglass-loop-drive/README.md) | Sandpoint LLC / Jeffrey Douglass | Civil Engineering + PLA & Lot Consolidation Survey | $6,180 ($1,800 + $4,380 addendum) | 2026-02-10 | 2026-03-12 | Won | [26003](../projects/26003-sandpoint-douglass-loop-drive/) |
| [P26006](260320-emerio-boundary-topo-subdivision/README.md) | Emerio (Jennifer Arnold) | Boundary, Topo, ROS, Subdivision Plat | $42,350 | 2026-03-20 | 2026-04-19 | Pending | — |
| [P26007](260315-twin-rocks-hwy101-approach/README.md) | Twin Rocks Friends Camp (Jeff Sargent) | Hwy 101 Approach Design & ODOT Permitting | $3,663 | 2026-03-15 | 2026-04-14 | Won | [26012](../projects/26012-twin-rocks-hwy101-approach/) |

---

## Status Definitions

| Status | Meaning |
|---|---|
| **Pending** | Proposal sent, awaiting client decision |
| **Won** | Client signed — project created in `projects/` |
| **Lost** | Client declined or selected another consultant |
| **Expired** | No response within 30 days — assumed not selected |

---

## Related Skills

- `/proposal-builder` — Draft a new proposal from an incoming RFQ
- `/proposal-review` — Monthly review of proposals: mark expired, analyze patterns
