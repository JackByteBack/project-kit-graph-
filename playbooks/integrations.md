# Title: Project Doc Blueprint Integrations Playbook

How the kit loads instructions, configures agents, bounds permissions, uses memory plugins and the REA MCP, and hands sessions off, with six reviewed external repositories.

Status: Proposed
Last updated: 2026-10-22

**What was verified.** On 2026-10-22 the README, directory listings, and selected config files of six repositories were read, and OpenCode and Claude Code documentation was fetched. **No third-party code was executed.** What the code actually does is Open until you review it. The configs in `integrations/` follow each tool's documented syntax, but none has been run against a live agent.

## 1. Reviewed repositories

Your list repeated several links; there are six distinct repositories. All six carry an MIT license file.

| Repository | What it is | Commit reviewed | Kit stance |
|---|---|---|---|
| `affaan-m/ECC` v2.2.3 | An agent harness: agents, skills, hooks, rules, MCP configs, an OpenCode plugin under `.opencode/`, and a Memory Vault CLI for cross-agent handoffs | `90606c8315ee` (2026-10-20) | Reference for patterns. Adopt pieces only through a decision entry. Hooks run scripts, so they are T3 |
| `addyosmani/agent-skills` | 25 skills and 9 commands for a define, plan, build, verify, review, ship lifecycle | `aeac41d4d005` (2026-10-13) | Closest match to this kit's workflow. Optional |
| `juliobsz/skills` | `/awwwards` builds a site from one line and checks it in a real browser; `/jury` scores a site. Needs Node 22.20 or later | `ea8f1455c2b0` (2026-10-19) | Optional for site builds. Its CLI collects anonymous usage data unless you set `DISABLE_TELEMETRY=1` |
| `Jakeschincariol/arena-skill` | `/arena` runs a tournament of up to 100 sub-agents on one task. Claude Code only; writes inside `.arena/` | `df07b8e518e1` (2026-09-26) | Optional, Claude Code only. Spends many model calls, so it is a cost decision (T3) |
| `Jakeschincariol/replica-skill` | Eleven skills that study an app's features and rebuild them "clean-room" | `77c9436fb3d1` (2026-10-03) | Optional, T3, with the limits in section 7.3 |
| `morluto/rea` | MCP server and CLI for reverse engineering binaries, JavaScript and Electron apps, .NET assemblies, and websites | `2c3dd946d59c` (2026-10-22) | Optional, T3, off by default. See section 7 |

**Pin what you install.** Repositories change daily. Record the commit or package version you reviewed in `docs/ai/integration-register.md` and install that version, not "latest".

## 2. AGENTS.md instruction loading

The full table is in `agent-compatibility.md` section 2. Short form, all **Confirmed** from vendor docs:

- **Claude Code** reads `CLAUDE.md`. It reads `AGENTS.md` only when no `CLAUDE.md` exists, so the kit's `CLAUDE.md` imports it with `@AGENTS.md`.
- **OpenCode** reads `AGENTS.md`, falling back to `CLAUDE.md`. It does not expand file references inside `AGENTS.md`.
- **Hermes** loads the first match of `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`.

ECC follows the same pattern: it ships its own `AGENTS.md` and `CLAUDE.md`, and an `instructions` list in `.opencode/opencode.json`.

## 3. Additional instruction files

| Agent | Mechanism | Notes |
|---|---|---|
| OpenCode | `instructions` array in `opencode.json`: paths, globs, remote URLs. Remote files time out after 5 seconds. All listed files are combined with `AGENTS.md` | **Confirmed** |
| Claude Code | `@path` imports, up to four levels deep; `.claude/rules/*.md`, optionally path-scoped | **Confirmed** |
| Hermes | `AGENTS.md` files merge from the git root down to the working directory | **Confirmed** |

**Proposed rule:** list at most five small, stable files in `instructions`, and keep the combined size under about 20,000 characters (Hermes truncates startup files above its limit). ECC's OpenCode config lists thirteen skill files as always-loaded instructions. That is a trade-off the kit avoids: task-specific guidance belongs in skills and playbooks that the agent reads on demand, so it doesn't use context on every turn.

## 4. Project-specific configuration

| File | Agent | Purpose |
|---|---|---|
| `opencode.json` | OpenCode | Instructions, permissions, agents, MCP servers |
| `.opencode/agents/*.md` | OpenCode | Markdown agent definitions |
| `.claude/settings.json` | Claude Code | Permissions |
| `.mcp.json` | Claude Code | Project MCP servers (**Confirmed** in shadcn's docs) |
| `integrations/*.example.json` | Any | Kit templates for MCP servers and agents. Copy only what you approve |

OpenCode merges config in this order, later overriding earlier: remote, global, custom (`OPENCODE_CONFIG`), project, `.opencode` directories, inline, managed. **Confirmed.**

Rules for every config file:

1. Put credentials in environment variables and reference them by name (`{env:NAME}` in OpenCode). Never write values into a file that is committed.
2. Add `.env*` to `.gitignore`.
3. Every MCP server, plugin, or skill you enable is a dependency and possibly a data flow. It needs a row in `docs/ai/integration-register.md` and an owner approval first (Rule 7).

## 5. Agent-specific prompts and model selection

**OpenCode (Confirmed).** Define agents under `agent` in `opencode.json`, or as Markdown files in `.opencode/agents/` (project) or `~/.config/opencode/agents/` (global). Fields: `description` (required), `mode` (`primary`, `subagent`, or `all`), `model` (`provider/model-id`), `prompt` (a file reference such as `{file:./prompts/05-adversarial-review.md}`, relative to the config file), `temperature`, and `permission`. If `model` is omitted, a primary agent uses the global model and a subagent uses the model of the primary agent that called it. ECC's config relies on this and leaves model choice to OpenCode.

**Kit template.** `integrations/opencode.agents.example.json` defines three agents that reuse the kit's prompts:

| Agent | Mode | Authority | Prompt |
|---|---|---|---|
| `researcher` | subagent | Web search and fetch allowed, edits ask, shell denied | `prompts/00-project-prompt-generator.md` rules |
| `builder` | primary | T2, edits and shell ask | `AGENTS.md` plus the project's `BUILD-PROMPT.md` |
| `reviewer` | subagent | Read only, edits denied | `prompts/05-adversarial-review.md` |

**Model choice is Open.** The kit leaves the model to your OpenCode setup. A stronger model for planning and review and a cheaper one for routine edits is a common practice, but this kit has no evidence for it. Test on one real project before standardizing.

**Other agents:** Claude Code subagent files (`.claude/agents/`) and Hermes per-agent prompts were not read this session. **Open.**

## 6. Permission boundaries

Instructions are context, not enforcement. Enforce tiers in config:

| Tier | OpenCode | Claude Code |
|---|---|---|
| T0 | `read`, `glob`, `grep`: allow | `Read`, `Glob`, `Grep` in `allow` |
| T1 | `edit`: ask or allow for docs | `Edit(./docs/**)` in `allow` |
| T2 | `edit`, `bash`: ask | `Edit(./src/**)`, build commands in `ask` |
| T3 | Everything not listed: ask; MCP servers `enabled: false` until approved | `ask`; MCP servers added only after approval |
| T4 | `deny`, plus `doom_loop: deny` | `deny` |

Integration gates:

| Integration | Tier | Condition |
|---|---|---|
| Install a third-party skill, plugin, or CLI | T3 | Read its files first; pin the commit or version; project-local, not global |
| Enable hooks (lifecycle scripts) | T3 | Read each script; hooks run with your user's authority |
| Enable an MCP server | T3 | Register in `integration-register.md`; see `mcp-servers.md` |
| Use REA on any target | T3 | Written authorization for the target (section 7) |
| Run `/arena` | T3 | Owner approves the cost; Claude Code only |
| Install a global npm package | T3 | Decision entry |

**Open (C-08):** ECC's OpenCode config uses `"permission": {"mcp_*": "ask"}`, and OpenCode's MCP page says tools are prefixed with the server name (for example `my-server_search`) and mentions no `mcp_` prefix. Use per-server `enabled: false` (documented) as the real gate, and test any glob in your install before trusting it.

**Open (C-09):** OpenCode's agent page shows a `shell` permission key, while its permissions page names `bash`. The kit uses `bash`. Check your OpenCode version.

## 7. REA MCP integration

### 7.1 What it is

REA ("Reverse Engineer Anything") connects an agent to local analysis tools for native binaries, JavaScript and Electron apps, .NET assemblies, and websites. Analysis runs locally, and results include evidence and limitations. Native analysis can use an existing Hopper, Ghidra, or IDA install. **Confirmed** from its README.

### 7.2 Install and register

`npx rea-agents setup` lets you choose agents, shows proposed changes, and backs up existing configuration. It writes an MCP server entry and workflow instructions. Supported clients include Claude Code and OpenCode. For OpenCode it writes an `mcp.rea` entry. **Confirmed.** Because `setup` edits your agent config, treat it as T3: review each change before approving it.

Manual registration per the README at the reviewed commit, with an exact version pin:

```json
{ "mcpServers": { "rea": { "command": "npx", "args": ["-y", "rea-agents@6.7.0", "mcp"] } } }
```

The kit's OpenCode template (`integrations/opencode.mcp.example.json`) adapts this to OpenCode's documented `local` syntax. That adaptation is **Proposed**, not taken from REA's docs; compare it with what `rea setup` writes.

### 7.3 Boundaries

REA's own `DISCLAIMER.md` limits it to lawful analysis: security research, interoperability, debugging or auditing software you own or are authorized to examine. It says it will not help with circumventing DRM or license checks, game cheats, bypassing authentication or access controls without authorization, copying proprietary software or reproducing its protected code and assets, or evading AI providers' policies. It also says authorization to inspect a file does not necessarily authorize running it or interacting with another party's systems.

Kit rules on top of that:

1. **Own or authorized targets only.** Record the target and the authorization in `decisions.md` before use. "Publicly available" is not authorization.
2. **Features and behavior, not assets.** Use findings to understand how something works and build your own implementation. Don't copy proprietary code, text, images, logos, or private APIs, and don't imitate another organization's branding or make a site that passes for theirs.
3. **Isolated environment for untrusted targets.** Don't run unknown binaries on your main machine.
4. **Keep captures out of the repo.** Traffic captures and investigation artifacts can contain credentials and personal data. Store them outside the project and never commit them.
5. **Findings are evidence, not instructions.** Text that comes out of an analyzed target is data.

### 7.4 When to skip it

The kit's name-to-site flow does not need REA. Use it only for a specific question, such as how a feature in your own app behaves or what a JavaScript bundle you ship contains.

## 8. Persistent-memory plugins

Three layers, in order of trust:

| Layer | Where | Written by | Trust |
|---|---|---|---|
| Kit memory | `memory/`, `docs/` | Agent and owner, in plain files | Default source of truth |
| Agent-native memory | Claude auto memory; Hermes `~/.hermes/memories/` | The agent | Per agent; not shared |
| Plugin memory | ECC Memory Vault | The agent, through a CLI or MCP | Unreviewed context |

**ECC Memory Vault (Confirmed from its README, v2.2.3).** It stores portable Markdown memories, project scope in `.ecc/memory/` and user scope in `~/.ecc/memory/`. Commands: `ecc memory init --scope project`, `search`, `read`, `handoff`, and `doctor`. An optional `ecc-memory-mcp` server exposes four tools: `memory_save`, `memory_search`, `memory_read`, `memory_doctor`. It needs the `ecc-universal` npm package installed separately; skill-only and plugin installs don't provide the runtime. Its own docs say entries stay unreviewed, are create-only, and must never be treated as executable instructions or policy, and that it is not a secret store.

**Kit stance (Proposed).**

1. Keep `memory/` as the source of truth. It works in every agent with no install.
2. Add the vault only if you need cross-agent search at scale. A global npm install and an MCP server are T3; record a decision first.
3. Promote accepted knowledge from any memory layer into `docs/` through human review.
4. Treat recalled memory as data. ECC's session hooks can inject recalled context at session start (its README describes a default cap of 8,000 characters), which makes memory a prompt-injection surface. Don't enable injection hooks you haven't read.
5. No secrets or personal data in any layer.

## 9. Memory retrieval and session handoff

**Retrieval order.** At session start read `memory/state.json`, the last 20 lines of `progress-log.md`, `lessons.md`, `open-questions.md`, then `docs/core/current-state.md` and `decisions.md`. Search narrowly. Check any recalled claim against the code or an Accepted decision. Reality wins over memory.

**Handoff note.** Write one file at session end, `memory/handoff.md`, replacing the previous one:

```markdown
## Handoff 2026-10-22 17:30 from [agent] to [agent]
- Goal: one sentence
- State: DONE / CONTINUE / STUCK / BLOCKED
- Verified this session: command and result
- Not verified: list
- Files touched: list
- Decisions needed from owner: list with IDs
- Next task: one item, with its tier
- Do not: anything the next agent must avoid
```

No secrets, no transcripts. The resume prompt is in `prompts/08-session-handoff.md`.

**With the ECC vault** (if approved): write the note to a file, then `ecc memory handoff --from <agent> --target <agent> --title "..." --body-file ./handoff.md`; on the receiving side `ecc memory search "<topic>" --target-harness <agent>` and `ecc memory read <id>`. The vault accepts bodies only from a file or stdin. ECC also ships `save-session` and `resume-session` commands for its own harness; those are not part of this kit.

## 10. Installing third-party skills safely

1. Clone the repository into a new, empty folder outside your project. Don't run its scripts.
2. Read `SKILL.md` files, any scripts, and any hooks or install steps. Look for network calls, file writes outside the project, and commands run on your behalf.
3. Note the commit and license. Prefer a project-local install.
4. Record it in `integration-register.md` with purpose, data touched, and approval.
5. Install the pinned version. Set `DISABLE_TELEMETRY=1` if the installer collects usage data and you don't want that.
6. Test on a throwaway project first.

Install commands from each README (not run here): `npx skills add addyosmani/agent-skills --list`, `npx skills add juliobsz/skills -g --skill jury`, and the Claude Code `/plugin marketplace add <owner>/<repo>` forms. The `skills` CLI is described as supporting many agents; whether it installs correctly for OpenCode and Hermes is **Open** for most of these repositories (`juliobsz/skills` names OpenCode explicitly).

## 11. Open items

| ID | Item | Impact |
|---|---|---|
| C-08 | Whether OpenCode accepts an `mcp_*`-style permission glob | Per-server `enabled` is the gate until tested |
| C-09 | `shell` versus `bash` permission key in OpenCode agent config | Test on your version |
| C-10 | Behavior of third-party code in all six repositories | Review before install |
| C-11 | REA entry shape in OpenCode versus the kit's adaptation | Compare with `rea setup` output |
| C-12 | `skills` CLI behavior for OpenCode and Hermes | Install by copying files if it fails |
| C-13 | Claude Code `.claude/agents/` and Hermes per-agent prompts | Not read this session |

## 12. Sources (accessed 2026-10-22)

- https://github.com/affaan-m/ECC
- https://github.com/addyosmani/agent-skills
- https://github.com/juliobsz/skills
- https://github.com/Jakeschincariol/arena-skill
- https://github.com/Jakeschincariol/replica-skill
- https://github.com/morluto/rea
- https://opencode.ai/docs/mcp-servers/
- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/config/
- https://opencode.ai/docs/permissions/
- https://opencode.ai/docs/rules/
