# Title: Project Doc Blueprint Session Handoff Prompt

Prompts to resume work in a fresh session and to close a session cleanly.

Status: Proposed
Last updated: 2026-10-20

---

## Resume prompt

<role>You are resuming work on this project in a fresh session. You have no memory of earlier sessions except the files.</role>

<task>
  1. Read `AGENTS.md`, `docs/core/current-state.md`, `docs/core/decisions.md`, `memory/state.json`, the last 20 lines of `memory/progress-log.md`, `memory/lessons.md`, `memory/open-questions.md`.
  2. Run `git status` and `git log -5`, and the project's verification command.
  3. Compare memory with reality. List any conflicts and trust reality.
  4. Reply with: the current phase, what is verified, what is in progress, the top blockers, and your proposed next task with its tier. Then wait for approval unless the loop contract already authorizes the work.
</task>

## Close prompt

<task>
  1. Run the verification command and record the real result.
  2. Append a dated entry to `memory/progress-log.md`: what changed, what was verified, what was not, what you learned, what is next.
  3. Update `memory/state.json` and `docs/core/current-state.md`. Move answered questions out of `memory/open-questions.md` without deleting them.
  4. Promote any finding that appeared twice to `memory/lessons.md`.
  5. Refresh `README.md` last if the doc index changed.
  6. Report in under 150 words. List anything you did not verify.
</task>
