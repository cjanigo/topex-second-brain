# Rule: Proposal-Stage Calendar Events Are Tentative

Any schedule block added to Google Calendar for a proposal (project not yet under contract) must be marked tentative until **both** conditions are met:

1. Contract/scope is fully executed (signed by client)
2. Down payment is received

## How to Mark Tentative

- Append `(TENTATIVE)` to the event title
- Add to description: `TENTATIVE -- scope not yet signed.`

## When to Remove Tentative

Once contract is executed and down payment is received:

- Remove `(TENTATIVE)` from the title
- Remove the tentative note from the description

## Applies To

- All calendar events created by `/gantt-sync` or manually for proposals in the `Pending` status
- Includes field survey blocks, office work blocks, and any other schedule holds

## Where This Matters

- `/proposal-builder` — when adding tentative schedule blocks to the calendar
- `/gantt-sync` — should respect tentative status for proposals not yet Won
