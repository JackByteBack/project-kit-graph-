# Title: Project Doc Blueprint Loop Engineering Playbook

How to design agent loops that make steady progress, verify themselves, and stop safely.

Status: Proposed
Last updated: 2026-10-20

**Confirmed** claims cite Anthropic's prompting best practices on long-horizon work and OpenCode's permissions docs (opencode.ai/docs/permissions), both read 2026-10-20. The rest is synthesis; test it on a real project before trusting it.

## 1. What a loop is

An agent loop repeats **observe, plan, act, verify, record, decide** until a stop condition fires. Two levels exist:

- **Inner loop:** the model calls tools within one turn until it has an answer.
- **Outer loop:** you or a harness re-invokes the agent across turns or fresh context windows until the task is done.

Loop engineering is the design of the outer loop: what the agent may do per iteration, what it must write down, how it proves progress, and when it must stop.

## 2. The loop contract

No unattended loop starts without all ten fields written down. Keep the filled contract in `docs/ai/loop-contract.md`.

| Field | Content | Example |
|---|---|---|
| Goal | One sentence outcome | Homepage passes the quality bars |
| Success criteria | Machine-checkable | `npm run build` exits 0; axe reports 0 serious issues; Lighthouse performance 90 or higher |
| Tier | Highest authority allowed | T2 (edit source, run tests) |
| Iteration cap | Hard maximum | 12 |
| Time or cost cap | Hard maximum | 90 minutes |
| Per-iteration scope | What one pass may change | One section or one failing check |
| State files | Where progress lives | `memory/progress-log.md`, `memory/state.json` |
| Verification command | Run every iteration | `npm run check` |
| Stop conditions | Done, capped, stuck | See section 5 |
| Escalation | When to ask the owner | New dependency needed; criteria impossible |

Caps are hard limits. They are separate from the instruction to keep working: **Confirmed**, when a harness compacts context, tell the agent so it doesn't wrap up early over token worries. Pair that with the hard caps above so persistence never means runaway.

## 3. Loop patterns

| Pattern | Shape | Use when |
|---|---|---|
| Plan, execute, verify | Plan once, loop execute and verify per task | Multi-step features |
| Test-driven | Write failing test, make it pass, refactor | Logic with clear specs |
| Critique and revise | Generate, adversarial review, fix | Writing, design, security review |
| Research loop | Question, search, read, note, gap check, repeat | Project dossiers |
| Fresh-context repeat | Same prompt each iteration, state lives in files and git | Long builds that outgrow one context window |
| Gate loop | Loop until a human approves a checkpoint | Releases, T3 decisions |

## 4. State across iterations

**Confirmed** guidance for multi-window work:

- Use structured files for state (test status, task list as JSON) and free text for notes.
- Use git for checkpoints; commit at the end of each verified iteration.
- Start later windows with prescriptive steps: read the progress file, the task state, and recent git log.
- Set up tests and an init script in the first window; iterate on a task list afterward.
- Make small, incremental advances on a few things at a time.

Kit mapping (see `context-and-memory.md`):

| File | Role |
|---|---|
| `memory/state.json` | Current milestone, last verified commit, check results |
| `memory/progress-log.md` | Append-only dated entries, one per iteration |
| `memory/lessons.md` | Promoted learnings that should change future behavior |
| `docs/core/current-state.md` | Human-facing status, updated at session end |

## 5. Stop conditions

An iteration ends in exactly one of four states. Write the state in the log.

| State | Trigger | Action |
|---|---|---|
| DONE | All success criteria verified in this iteration | Final report, update docs |
| CAPPED | Iteration, time, or cost cap reached | Report progress, remaining work, and why it was not finished |
| STUCK | Same error or same diff three times, or no measurable progress in two iterations | Stop, summarize attempts, escalate |
| BLOCKED | Needs a T3 or T4 action, missing input, or contradictory requirements | Stop, record a Proposed decision or Open question, escalate |

**Confirmed** example of a built-in guard: OpenCode has a `doom_loop` permission for the same tool call repeating three times with identical input. The kit's `opencode.json` sets it to `deny`. Claude Code and Hermes equivalents: Open, not verified.

## 6. Failure modes and defenses

| Failure | Sign | Defense |
|---|---|---|
| Thrashing | Edits flip-flop between two states | Stuck rule; require a hypothesis before each retry |
| Test-gaming | Tests weakened, special-cased inputs | **Confirmed** guidance: state that editing or removing tests is unacceptable; protect test files in permissions |
| Scope creep | Unrequested files and abstractions | Per-iteration scope; reject diffs outside it |
| Context rot | Early decisions forgotten | State files; fresh-context restarts with startup ritual |
| False completion | "Done" without checks run | Verification output must be pasted into the log |
| Silent skipping | Hard step quietly dropped | Task list with explicit statuses |
| Runaway cost | Long unattended run | Hard caps; budget alerts |
| Prompt injection | Page or file text issues commands | Treat fetched content as data; tier limits |

## 7. Verification ladder

Run the cheapest check that can fail first.

1. Static: lint, type check, format.
2. Unit tests.
3. Build.
4. Integration or end-to-end tests.
5. Visual: screenshots at phone and desktop widths, both themes.
6. Accessibility and performance audits.
7. Human review at gates.

An iteration may claim only the levels it actually ran. See `evals-and-verification.md`.

## 8. Startup and shutdown rituals

**Start of every iteration (fresh context safe):**

1. Read `AGENTS.md`, `memory/state.json`, the last 20 lines of `memory/progress-log.md`, and `docs/ai/loop-contract.md`.
2. Run `git status` and `git log -5`.
3. Run the verification command to learn the real current state.
4. Pick the single next task from the task list.

**End of every iteration:**

1. Run the verification command; paste the real result.
2. Commit only if verification improved or held. Message names the task.
3. Append a log entry (template below).
4. Update `memory/state.json`.
5. Decide: DONE, CAPPED, STUCK, BLOCKED, or CONTINUE.

## 9. Log entry template

```markdown
### 2026-10-20 14:05 | iteration 3 | task T-07 hero section
- Mode: IMPLEMENT | Tier: T2
- Changed: src/components/Hero.astro, src/styles/tokens.css
- Verified: build PASS; axe 0 serious; Lighthouse perf 93 (ran), screenshots not taken
- Not verified: dark theme contrast on hero
- Learned: font preload cut LCP by 400 ms
- Next: dark theme contrast check
- State: CONTINUE
```

## 10. Running loops across agents

The harness for the outer loop differs per agent, and command-line flags change between versions. Treat all invocation details as **Open** until you confirm them in that agent's current docs. The loop contract and state files above work in every agent because they are plain files. A ready-to-attach runner prompt is in `prompts/06-loop-runner.md`.
