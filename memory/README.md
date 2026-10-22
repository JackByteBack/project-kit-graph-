# Title: Project Name Agent Memory

Shared working memory any agent reads at session start and updates at session end.

Status: Draft
Last updated: 2026-10-21

## Files

| File | Purpose | Edit rule |
|---|---|---|
| state.json | Structured status: phase, last verified commit, check results | Overwrite each session |
| progress-log.md | Dated entries, one per session or iteration | Append only |
| lessons.md | Learnings promoted from repeated findings | Add when a finding repeats |
| open-questions.md | Questions awaiting the owner | Add and close; keep closed ones |

## Protocol

1. **Session start.** Read state.json, the last 20 lines of progress-log.md, lessons.md, open-questions.md, then docs/core/current-state.md and decisions.md. Compare with `git status`, `git log -5`, and the verification command. Reality wins over memory.
2. **During work.** Log each finished task or costly discovery when it happens, not at the end.
3. **Session end.** Append a log entry, update state.json, promote repeated findings to lessons.md, and update docs/core/current-state.md.

## Rules

- No secrets, tokens, passwords, private keys, personal records, or production data.
- Tag entries: stated by owner, verified, or inferred. Treat inferred entries as Open.
- Authority order: owner statement, Accepted decisions, AGENTS.md, other docs, this folder, tool native memory, model recall. When two disagree, fix the lower one and log the correction.
- Full guidance: playbooks/context-and-memory.md.
