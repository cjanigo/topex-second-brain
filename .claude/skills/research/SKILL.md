# Research Skill

## What This Is

A deep research skill for Chris Janigo, PE/PLS, sole operator of Topex Inc. This is not a quick web search — it is a structured multi-step investigation that:

1. Understands the research question in the context of Chris's active work
2. Identifies the research type and selects the right approach
3. Executes multiple search and fetch passes, following leads
4. Synthesizes findings into something actionable
5. Flags anything that requires a decision or changes how a project should proceed

---

## How to Invoke

```
/research [question or topic]
```

Examples:
- `/research Washington State water right transfer requirements for surface water`
- `/research FEMA Zone AE floodplain standards for bridge hydraulic design`
- `/research what survey equipment is best for drone-assisted boundary work`
- `/research case law on adverse possession with color of title in Washington`

---

## Execution Protocol

When this skill is invoked, follow these steps:

### Step 1 — Classify the Research Type

Determine which category best fits the question:

| Type | Examples |
|---|---|
| Technical / Standards | ASCE, surveying standards, hydrology methods, FEMA FIS requirements |
| Regulatory / Permitting | Local jurisdiction rules, state agency requirements, code compliance |
| Water Rights | Washington water law, DOE adjudications, water right transfers, exams |
| Legal / Expert Witness | Case law, technical standards used in litigation, precedent |
| Operational | Equipment, software, vendors, workflow comparisons |
| Site / Project-Specific | Recorded documents, aerial history, jurisdiction-specific rules for a site |

### Step 2 — Load Context

Before searching, read:
- `context/current-priorities.md` — what's active and urgent
- `context/work.md` — what types of work are in scope
- Any relevant project README in `projects/`

Use this to frame the research: Is this for a specific active project? Does it affect a deadline? Does it change how work should be scoped or sequenced?

### Step 3 — Execute Multi-Step Research

Do not stop at one or two searches. Follow leads. Structure the search in passes:

**Pass 1 — Establish the landscape**
Search broadly to understand the domain, key terms, governing bodies, and major standards or statutes. Identify 3-5 authoritative sources.

**Pass 2 — Go deep**
Fetch the most relevant sources. Look for specific requirements, exceptions, thresholds, procedures, or precedents that actually answer the question.

**Pass 3 — Fill gaps**
If anything is unclear or contradictory, run targeted follow-up searches. Look for:
- Recent updates or changes to standards/law
- Washington State-specific rules (most of Chris's work is in WA)
- Local variations (county or city-level rules)
- Practical guidance, not just the rule text

**Pass 4 — Cross-check**
Verify key findings against a second source where possible. Flag anything that could not be confirmed.

### Step 4 — Synthesize

Structure the output as:

---

**Research: [Topic]**
*Type: [classification] | Project/Context: [if applicable]*

**Bottom Line**
[2-4 sentences: the direct answer to the question, or the key finding. What does Chris need to know right now?]

**Key Findings**
[Bullets or a table — whichever is clearer. Lead with the most actionable. Keep it tight.]

**Watch Out For**
[Any gotchas, recent changes, ambiguities, or things that could bite a project. Omit this section if nothing notable.]

**Sources**
[List 3-5 sources with titles and URLs. Prioritize: official sources > technical references > secondary.]

**Implications for Active Work** *(only if relevant)*
[If findings affect a current project or deadline, flag it explicitly here.]

---

### Step 5 — Flag Decisions

If the research surfaces something that requires Chris to make a decision (e.g., a regulatory requirement changes project scope, or a standard is unclear enough that professional judgment is needed), call it out explicitly:

> **Decision Needed:** [What the decision is and why it can't be resolved by research alone]

---

## Research Principles

- Washington State is the primary jurisdiction unless stated otherwise
- When standards conflict (local vs. state vs. federal), flag all levels and note which governs
- Engineering and surveying standards change — note if a source is more than 3 years old
- Water rights research should always note the water right number, priority date, and source if known
- Expert witness research should prioritize peer-reviewed sources and published standards over secondary commentary
- If a question is outside Chris's license scope (e.g., structural, electrical), note the limitation

---

## Output Format Rules

Follow the communication style rules in `.claude/rules/communication-style.md`:
- Short over long
- Tables over nested bullets for structured data
- No dashes of any kind in written prose
- No emojis in research output (this is a formal document context)
- Casual but precise tone in Bottom Line; formal in findings

---

## When to Ask a Clarifying Question

If the research question is ambiguous in a way that would send the research in completely different directions, ask one focused question before starting. Examples:

- "Is this for the [project name] project or a general reference?"
- "Are you researching WA State rules specifically, or federal requirements?"
- "Is this for expert witness testimony or for your own project design?"

Do not over-ask. If reasonable assumptions can be made, make them and state what you assumed.
