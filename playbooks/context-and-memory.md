# Title: Project Doc Blueprint Context and Memory Playbook

How to give agents durable context and their own memory so they work across sessions and across tools.

Status: Proposed
Last updated: 2026-10-20

**Confirmed** facts below come from official docs read on 2026-10-20: Claude Code memory (code.claude.com/docs/en/memory), OpenCode rules (opencode.ai/docs/rules), Hermes context files and "Which File Does What" (hermes-agent.nousresearch.com/docs). Items without a label are design proposals.

## 1. Five layers of context

| Layer | Written by | Lifetime | Where | Example |
|---|---|---|---|---|
| 1. Instruction files | Humans | Permanent | `AGENTS.md`, `CLAUDE.md` | Rules, modes, tiers |
| 2. Project docs | Humans and agents | Long | `docs/` | PRD, architecture, decisions |
| 3. Agent memory | Agents | Medium | `memory/` | Progress, lessons, state |
| 4. Session context | The conversation | One session | Context window | Current task details |
| 5. Retrieval | Tools | On demand | Search, file reads, web | Research sources |

Rule of thumb: stable facts go in layers 1 and 2, learned working knowledge goes in layer 3, and nothing important lives only in layer 4.

## 2. What each agent loads

| Agent | Project instructions | Native memory | Confirmed |
|---|---|---|---|
| Claude Code | `CLAUDE.md` (or `.claude/CLAUDE.md`); reads `AGENTS.md` only when no `CLAUDE.md` exists; `@path` imports, up to four levels deep; `.claude/rules/*.md` | Auto memory: Claude writes its own notes; first 200 lines or 25 KB loaded each session | Yes |
| OpenCode | `AGENTS.md`, falling back to `CLAUDE.md`; `instructions` array in `opencode.json` takes paths, globs, and URLs; references inside `AGENTS.md` are not auto-expanded | Not documented on the pages read: Open | Yes for loading |
| Hermes | First match of `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`; `AGENTS.md` files merge from git root down; size limit scales with the model, minimum 20,000 characters, longer files are truncated | `~/.hermes/memories/MEMORY.md` (agent notes) and `USER.md` (user profile), written by the agent; persona in `~/.hermes/SOUL.md` | Yes |

Consequences for this kit:

1. `AGENTS.md` is the self-contained master, because OpenCode doesn't expand references and Hermes loads one file.
2. `CLAUDE.md` imports `AGENTS.md` so Claude Code stays in sync.
3. Project knowledge that every agent must share lives in `memory/` and `docs/`, not in any single tool's native memory.
4. Keep each context file well under 20,000 characters.

## 3. The `memory/` folder

Created for every project by `python scaffold.py new`.

| File | Purpose | Edit rule |
|---|---|---|
| `README.md` | The memory protocol (this section, condensed) | Rarely |
| `state.json` | Structured status: milestone, last verified commit, check results, open task IDs | Overwrite each session |
| `progress-log.md` | Append-only dated entries | Append only; never rewrite history |
| `lessons.md` | Promoted learnings that should change behavior | Add when a finding repeats or costs time |
| `open-questions.md` | Questions awaiting the owner, with impact | Add and close; keep closed ones |

## 4. Protocol

**Session start**

1. Read `AGENTS.md` rules (already loaded by most agents), then `memory/state.json`, the last 20 lines of `progress-log.md`, `lessons.md`, and `open-questions.md`.
2. Read `docs/core/current-state.md` and `decisions.md`.
3. Compare memory with reality: run `git status`, `git log -5`, and the verification command. If memory and reality disagree, reality wins; fix the memory entry.

**During work**

- Write a log line whenever you finish a task or learn something costly. Don't wait for the end; a crash loses the session.

**Session end**

1. Append a log entry (template in `loop-engineering.md`).
2. Update `state.json`.
3. If a finding appeared twice, promote it to `lessons.md`.
4. If a lesson affects every project, propose adding it to `AGENTS.md` as a decision for the owner to approve.
5. Update `docs/core/current-state.md`.

## 5. What memory may and may not hold

**May hold:** project facts, decisions with IDs, tool quirks, commands that work, mistakes to avoid, preferences the owner stated for this project.

**Must not hold:** secrets, tokens, passwords, private keys, personal records, or production data. Government ID and payment numbers never go in memory. Don't store guesses about the owner's personality or health. If an entry came from inference rather than a statement, mark it `[inferred]` and treat it as Open.

## 6. Authority and conflicts

Highest to lowest: owner statement in this session, `decisions.md` Accepted entries, `AGENTS.md`, other docs, `memory/`, agent native memory, model recall.

When two sources disagree, follow the higher one, then correct the lower one and log the correction. Never silently delete a lesson that was once valid; strike it through with the reason (Rule 5).

## 7. Entry format

Short, dated, attributable.

```markdown
- 2026-10-20 [stated by owner] Primary audience is first-year students. Source: owner message.
- 2026-10-20 [verified] `npm run build` needs Node 20 or later. Source: package.json engines, build run.
- 2026-10-20 [inferred] Owner prefers short copy. Needs confirmation.
```

Tags: `stated by owner`, `verified` (checked in code or by running something), `inferred` (open to confirm).

## 8. Size and hygiene

- Keep `lessons.md` under about 60 lines. Merge duplicates; prune anything the code or docs now enforce.
- Keep `progress-log.md` readable: when it passes about 300 lines, summarize old months into a dated block and keep the recent entries.
- Never let memory become a second PRD. Requirements belong in `prd.md`.

## 9. Retrieval and context budget

- Prefer reading a specific file over loading everything.
- Put long reference material above the question when prompting (see `prompt-engineering.md`).
- Delegate broad searches to subagents that return summaries (see `graph-engineering.md`).
- If your harness compacts context, tell the agent so it saves state to files first and doesn't stop early.

## 10. Open items

- **Open:** OpenCode native memory behavior. Check its docs before relying on it.
- **Open:** Whether Hermes reads `memory/` automatically. It does not by default; the project `AGENTS.md` instructs the agent to read it.
