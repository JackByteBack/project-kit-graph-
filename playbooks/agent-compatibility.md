# Title: Project Doc Blueprint Agent Compatibility Guide

How Claude Code, OpenCode, and Hermes read this kit, and what stays unverified.

Status: Proposed
Last updated: 2026-10-20

All facts marked **Confirmed** were read from the official documentation on 2026-10-20 (links in section 6). Agent products change quickly; recheck before relying on any detail.

## 1. Strategy

One file for every agent, with thin adapters:

```
AGENTS.md        universal, self-contained master (OpenCode, Hermes, others)
CLAUDE.md        imports AGENTS.md (Claude Code)
opencode.json    OpenCode permissions and extra instruction files
.claude/         Claude Code permissions
memory/          shared agent memory, plain files, readable by any agent
```

## 2. Compatibility matrix

| Capability | Claude Code | OpenCode | Hermes |
|---|---|---|---|
| Project instruction file | `CLAUDE.md` or `.claude/CLAUDE.md`; reads `AGENTS.md` only if no `CLAUDE.md` exists in or above the working directory. **Confirmed** | `AGENTS.md`; falls back to `CLAUDE.md` if there is no `AGENTS.md`. **Confirmed** | First match wins: `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`. **Confirmed** |
| Imports from the instruction file | `@path` imports, relative to the file, up to four levels. **Confirmed** | Not auto-expanded; use the `instructions` array or tell the agent to read the file. **Confirmed** | Not documented on the pages read. **Open** |
| Extra instruction files | `.claude/rules/*.md`, optionally path-scoped. **Confirmed** | `instructions` in `opencode.json`: paths, globs, URLs. **Confirmed** | `AGENTS.md` merges from git root down to the working directory. **Confirmed** |
| Permission config | `.claude/settings.json` rules written `Tool(specifier)`. Evaluated deny, then ask, then allow, and the first match decides, so an allow can't carve an exception out of a deny. Bash wildcards use `*`; a trailing `:*` is equivalent to a trailing ` *`. Read and Edit paths use gitignore-style patterns (`./` relative to the working directory, `//` absolute, `~/` home). A Read deny also blocks Edit and Write on that path. **Confirmed** | `opencode.json` `permission`: allow, ask, deny per tool; bash patterns; last match wins; `doom_loop`; `external_directory`. **Confirmed** | Not documented on the pages read. **Open** |
| Native memory | Auto memory written by Claude; first 200 lines or 25 KB loaded. **Confirmed** | Not documented on the pages read. **Open** | `~/.hermes/memories/MEMORY.md` and `USER.md`, written by the agent. **Confirmed** |
| Persona file | Not applicable | Not documented: **Open** | `~/.hermes/SOUL.md`. **Confirmed** |
| Size limits on context files | Keep concise; no hard figure read | No figure read | Scales with model, minimum 20,000 characters; truncates head and tail. **Confirmed** |
| Enforcement | Instructions are context, not enforcement; use permissions or hooks. **Confirmed** | Permissions in config | **Open** |

## 3. Setup per agent

### Claude Code

1. Put the kit or project folder at the working directory.
2. `CLAUDE.md` loads and imports `AGENTS.md`.
3. Copy or review `.claude/settings.json`; tighten for the project.
4. Optional: add `.claude/rules/` for path-specific rules.

### OpenCode

1. `AGENTS.md` loads from the project root.
2. `opencode.json` adds `docs/core/*` files to the context and sets permissions.
3. Because references in `AGENTS.md` aren't auto-expanded, the instruction "read these files first" in `AGENTS.md` section 5 relies on the agent's file-read tool, and the config's `instructions` list covers the essentials.
4. Web research needs web search or fetch to be enabled for your model and provider. **Open:** confirm in your install; the permission keys `websearch` and `webfetch` exist.

### Hermes

1. `AGENTS.md` loads (unless a `.hermes.md` exists, which takes priority). **Don't create `.hermes.md` unless you want to replace `AGENTS.md`.**
2. Hermes keeps its own notes under `~/.hermes/memories/`. The project's `memory/` folder is separate; the `AGENTS.md` protocol tells the agent to read and write it.
3. Changes to instruction files take effect at the start of a new session. **Confirmed.**
4. Keep `AGENTS.md` under 20,000 characters to avoid truncation. The kit's check is `python scaffold.py validate` (warns above 20,000).

### Any other agent

Attach `AGENTS.md` and the project's `BUILD-PROMPT.md`, or paste them, and tell the agent to read `memory/` and `docs/core/`. Plain Markdown and plain files are the common denominator.

## 4. Attaching the project-name prompt

1. Run `python scaffold.py new "Project Name"`.
2. Give the agent `PROMPT-GENERATOR.md` as a separate prompt (paste it, or tell the agent to read that file).
3. The agent researches, then writes `research/` and `BUILD-PROMPT.md`.
4. Start a fresh session and give the agent `BUILD-PROMPT.md` to build.

Research needs an agent with web access. The scaffold script cannot search the web; it prepares files only.

## 5. Open items

| ID | Item | Impact |
|---|---|---|
| C-01 | Hermes permission and safety configuration | Can't enforce tiers by config there; rely on instructions and review |
| C-02 | OpenCode native memory and persistence | Use `memory/` files meanwhile |
| C-03 | Hermes handling of `@path` imports | Kit avoids imports in `AGENTS.md` |
| C-04 | Granular `read` and `edit` path patterns in `opencode.json` | Kit uses only documented bash patterns and tool-level values |
| C-05 | Exact CLI flags for unattended loops in each agent | Loop runner prompt avoids flags |
| C-06 | Web search availability per OpenCode provider | Research may need a different provider or a manual dossier |
| C-07 | Rule order differs: OpenCode uses the last matching rule, Claude Code uses deny, then ask, then allow | Don't copy one agent's permission file into the other without reordering |

## 6. Sources (accessed 2026-10-20)

- Claude Code memory: https://code.claude.com/docs/en/memory
- Claude Code permissions: https://code.claude.com/docs/en/permissions
- OpenCode rules: https://opencode.ai/docs/rules/
- OpenCode config: https://opencode.ai/docs/config/
- OpenCode permissions: https://opencode.ai/docs/permissions/
- Hermes context files: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- Hermes "Which file does what": https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what
- Claude prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
