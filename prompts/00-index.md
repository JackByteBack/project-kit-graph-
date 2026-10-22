# Title: Project Doc Blueprint Prompts Index

Which prompt to use for which situation.

Status: Proposed
Last updated: 2026-10-20

| File | Use when | Needs |
|---|---|---|
| `00-project-prompt-generator.md` | You have only a project name and want a senior-level build prompt | An agent with web search and file write |
| `01-build-master-prompt.md` | You know the project and want to write the build prompt by hand | Nothing |
| `02-audit-existing-project.md` | A repository exists and needs its documentation built from evidence | Agent inside the repo |
| `03-design-direction.md` | Research is done and you need a distinctive design system | `research/dossier.md` |
| `04-content-and-seo.md` | You need real copy and an SEO plan | `research/dossier.md` |
| `05-adversarial-review.md` | A build or doc set needs independent review | Fresh session |
| `06-loop-runner.md` | Running verified iterations against a loop contract | `docs/ai/loop-contract.md` |
| `07-graph-orchestrator.md` | Running a build as a graph of subagents | Agent with subagents (or run nodes in order) |
| `08-session-handoff.md` | Starting or ending a session | `memory/` |
| `09-ui-build-with-design-mcps.md` | Building UI with approved shadcn/ui, 21st.dev, or Figma MCP servers | `docs/design/design-system.md`, an Approved row in `docs/ai/integration-register.md` |

Typical flow from a name only: `00` in session one, then `07` or `06` with the generated `BUILD-PROMPT.md` in session two, then `05` in session three.
