# Rule: Always Push to GitHub After Every Change

After any file is created or modified in this repo, always commit and push to `origin/master` before ending the session or task.

## Why

Ollama (and any other subagent) reads from `github.com/cjanigo/topex-second-brain`, not the local filesystem. Any unpushed changes are invisible to downstream agents. Skills, project READMEs, context files, and rules must be on GitHub to take effect.

## What to Push

Everything. No exceptions:
- Skill files (`.claude/skills/`)
- Project READMEs (`projects/`)
- Proposals (`proposals/`)
- Context files (`context/`)
- Rules (`.claude/rules/`)
- Templates (`templates/`)
- Schedule files (`schedule/`)
- CLAUDE.md

## When to Push

After every task that modifies or creates any file. Do not wait for the user to ask.

## How

```bash
git add -A
git commit -m "..."
git push origin master
```

Stage all tracked and untracked files, commit with a descriptive message, and push immediately.
