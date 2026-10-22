# Title: Project Doc Blueprint Claude Code Entry

Claude Code entry point that imports the universal agent instructions.

Status: Draft
Last updated: 2026-10-20

@AGENTS.md

## Claude Code notes

- **Why this file exists.** Claude Code reads `CLAUDE.md` and, when both files exist, ignores a bare `AGENTS.md`. Importing `AGENTS.md` here keeps one source of truth. Confirmed in the Claude Code memory docs (code.claude.com/docs/en/memory, accessed 2026-10-20).
- **Instructions are context, not enforcement.** Block actions with `.claude/settings.json` permissions or hooks. The kit ships a starter file.
- **Native memory is a supplement.** Claude Code auto memory is Claude-only. Keep project facts in `memory/` so every agent shares them.
- **Prompting Claude.** Be explicit about the action wanted, give the reason, use XML tags for long inputs, and put long documents above the question. See `playbooks/prompt-engineering.md`.
