# Title: Project Doc Blueprint Playbooks Index

Reading guide for the reusable engineering playbooks shared by every project.

Status: Proposed
Last updated: 2026-10-20

Playbooks are reference knowledge. They hold no project facts. Project facts live in `docs/`, and agent working memory lives in `memory/`.

| Playbook | Read when | Length |
|---|---|---|
| `prompt-engineering.md` | Writing or reviewing any prompt | Medium |
| `loop-engineering.md` | Designing unattended or repeated agent runs | Medium |
| `graph-engineering.md` | Splitting work across agents, or mapping project knowledge | Medium |
| `context-and-memory.md` | Setting up memory and context files | Medium |
| `evals-and-verification.md` | Testing prompts, loops, or finished sites | Short |
| `research-protocol.md` | Researching a project from its name | Medium |
| `site-building-standards.md` | Building any website | Long |
| `agent-compatibility.md` | Running the kit in Claude Code, OpenCode, or Hermes | Medium |
| `integrations.md` | Adding skills, plugins, memory tools, or the REA MCP; configuring agent prompts, models, and permissions; handing off sessions | Long |
| `mcp-servers.md` | Enabling the shadcn/ui, 21st.dev, Figma, or REA MCP servers | Medium |

Suggested order for a new project: `research-protocol.md`, `prompt-engineering.md`, `site-building-standards.md`, then the others as the work needs them.
