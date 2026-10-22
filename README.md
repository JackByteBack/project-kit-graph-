# Title: Project Doc Blueprint Documentation

Entry point for the starter kit: instructions, prompts, playbooks, and templates that let any coding agent build a project from its own files and memory.

Status: Draft
Last updated: 2026-10-22

## What this kit does

It gives every project one self-contained folder. An agent started inside it (Claude Code, OpenCode, Hermes, or another) reads the rules, the project facts, and its own working memory from plain Markdown files, then does the work inside written limits. Nothing depends on one vendor's memory feature.

Core idea, unchanged from the original instructions: **analyze first, decide second, document third, and implement only when the task authorizes it.**

## Quick start

**Only want the prompt?** `python scaffold.py prompt "My Project" --details "audience, goals, links" --out prompt.md` writes one self-contained file to attach to any agent that has web search and file write. The `new` command below does the same and also builds the whole project folder.

**From a project name only**

1. `python scaffold.py new "My Project"` creates `projects/my-project/` with docs, memory, playbooks, prompts, and agent files.
2. Optional: write what you know in that folder's `BRIEF.md`.
3. Open your agent inside that folder and give it `PROMPT-GENERATOR.md`. The agent needs web search and file write. It researches the project, then writes `research/` and a senior-level `BUILD-PROMPT.md`.
4. Start a fresh session and give the agent `BUILD-PROMPT.md`. It builds in verified loops and keeps `memory/` current.

**For an existing repository**

1. Copy this kit's files into the repo, or run `python scaffold.py init --out <repo> --triggers <flags>`.
2. Give the agent `prompts/02-audit-existing-project.md`.

## What is in the kit

| Path | Purpose |
|---|---|
| `AGENTS.md` | Universal, self-contained instructions. OpenCode and Hermes load it directly. |
| `CLAUDE.md` | Imports `AGENTS.md` for Claude Code. |
| `opencode.json`, `.claude/settings.json` | Starter permission configs that enforce the authorization tiers. |
| `scaffold.py` | Generates projects, selects docs by trigger, builds the index, validates, graphs. |
| `docs/` | 68 templates plus a selection log, grouped by subject. A project keeps only what its triggers call for. |
| `playbooks/` | Reusable engineering knowledge: prompt, loop, and graph engineering, context and memory, evals, research, site standards, agent compatibility, integrations, MCP servers. |
| `prompts/` | Ready-to-attach prompts, including the project-name generator and a UI build prompt for approved design MCPs. |
| `integrations/` | Copy-only example configs for the shadcn/ui, 21st.dev, Figma, and REA MCP servers and for OpenCode agents. Nothing is enabled by default. |
| `memory/` | Shared agent memory: state, progress log, lessons, open questions. |
| `projects/` | One folder per project made with `new`, plus a registry. |
| `blueprint-guide.html` | Visual reference of the workflow, tiers, and document tree. |

## Commands

| Command | Result |
|---|---|
| `python scaffold.py new "Name"` | Full project folder under `projects/`, registered |
| `python scaffold.py init --name "Name" --preset site --out DIR` | Add docs, memory, and agent files to a folder |
| `python scaffold.py list` | Triggers, presets, and the docs each triggers |
| `python scaffold.py validate` | Headers, links, index coverage, JSON validity, secret patterns |
| `python scaffold.py graph` | Document mention graph in `docs/ai/doc-graph.md` |
| `python scaffold.py readme` | Refresh the index below; run last |

Presets: `minimal`, `web-app`, `api`, `site` (default for `new`), `full`, `all`.

## Known limits

- `scaffold.py` prepares files. It cannot search the web; the agent does.
- Instruction files are context, not enforcement. Permission configs enforce, and the Hermes equivalent is unverified (see `playbooks/agent-compatibility.md`, items C-01 to C-06).
- Thresholds in `playbooks/site-building-standards.md` are Proposed defaults, not verified against current standards.
- The validator checks structure. It cannot judge whether a Confirmed claim has real evidence.

<!-- INDEX:START -->

## Documentation Index

### Start here

| Document | Purpose | Status |
|---|---|---|
| [Project Doc Blueprint Universal Agent Instructions](AGENTS.md) | Agent-neutral master instructions for Claude Code, OpenCode, Hermes, and any other coding agent. | Draft |
| [Project Doc Blueprint Claude Code Entry](CLAUDE.md) | Claude Code entry point that imports the universal agent instructions. | Draft |

### docs/core

| Document | Purpose | Status |
|---|---|---|
| [Project Name Project Intake](docs/core/project-intake.md) | Captures the facts and needs that drive documentation selection. | Draft |
| [Project Name Project Instructions](docs/core/instructions.md) | Project-specific rules for AI-assisted work and engineering collaboration. | Draft |
| [Project Name Status Labels](docs/core/status-labels.md) | Defines the knowledge-status labels used across all documents. | Accepted |
| [Project Name Product Requirements](docs/core/prd.md) | Problem, users, goals, scope, requirements, and success criteria. | Draft |
| [Project Name Decisions](docs/core/decisions.md) | Accepted decisions, rejected alternatives, and pending decisions with rationale. | Draft |
| [Project Name Current State](docs/core/current-state.md) | Verified project status, progress, open items, blockers, and known issues. | Draft |
| [Project Name Coding Agent Rules](docs/core/agents.md) | Rules and constraints for coding agents and collaborators. | Draft |
| [Project Name Glossary](docs/core/glossary.md) | Domain terminology, abbreviations, and identifiers. | Draft |
| [Project Name Selection Log](docs/core/selection-log.md) | Records why each candidate document was created, consolidated, or omitted. | Proposed |

### docs/product

| Document | Purpose | Status |
|---|---|---|
| [Project Name Admin Journeys](docs/product/admin-journeys.md) | Flows for administrators and operators. | Draft |
| [Project Name Application Flow](docs/product/app-flow.md) | Complex application flows and state transitions. | Draft |
| [Project Name Content Guidelines](docs/product/content-guidelines.md) | Voice, tone, and rules for user-facing and generated text. | Draft |
| [Project Name User Definition](docs/product/define-the-user.md) | Who the users are, what they need, and their constraints. | Draft |
| [Project Name Demo Plan](docs/product/demo.md) | Scope and script for a time-boxed demo or deliverable. | Draft |
| [Project Name File and Content Formats](docs/product/file-content-format.md) | Formats the project reads or writes. | Draft |
| [Project Name Idea](docs/product/idea.md) | Original concept and motivation before requirements. | Draft |
| [Project Name Iteration Log](docs/product/iteration.md) | How feedback becomes changes between releases. | Draft |
| [Project Name Research](docs/product/research.md) | Findings from market, user, or technical research. | Draft |
| [Project Name Roadmap](docs/product/roadmap.md) | Planned direction across releases. | Draft |
| [Project Name User Journeys](docs/product/user-journeys.md) | End-to-end flows each user role follows. | Draft |

### docs/architecture

| Document | Purpose | Status |
|---|---|---|
| [Project Name Architecture](docs/architecture/architecture.md) | Components, boundaries, data flows, and trust boundaries. | Draft |
| [Project Name Technology](docs/architecture/technology.md) | Selected technologies, versions, and rationale. | Draft |
| [Project Name API](docs/architecture/api.md) | Endpoints, access rules, and error formats. | Draft |
| [Project Name Backend Schema](docs/architecture/backend-schema.md) | Entities, fields, relationships, sensitivity, and retention. | Draft |
| [Project Name Background Jobs](docs/architecture/background-jobs.md) | Queued and asynchronous work. | Draft |
| [Project Name Project Structure](docs/architecture/project-structure.md) | Required directory layout and conventions. | Draft |
| [Project Name Rejected Options](docs/architecture/rejected-options.md) | Significant alternatives considered and declined. | Draft |
| [Project Name Scheduled Tasks](docs/architecture/scheduled-tasks.md) | Scheduled behavior and ownership. | Draft |

### docs/design

| Document | Purpose | Status |
|---|---|---|
| [Project Name Accessibility](docs/design/accessibility.md) | Accessibility requirements and verification. | Draft |
| [Project Name Design System](docs/design/design-system.md) | Visual language and reusable UI patterns. | Draft |
| [Project Name Design Notes](docs/design/design.md) | Design rationale and decisions for specific surfaces. | Draft |
| [Project Name UI Architecture](docs/design/ui-architecture.md) | Front-end structure, state, and rendering strategy. | Draft |

### docs/web

| Document | Purpose | Status |
|---|---|---|
| [Project Name Analytics and Privacy](docs/web/analytics-privacy.md) | What data the site collects, which third parties receive it, and under which rules. | Draft |
| [Project Name Information Architecture](docs/web/information-architecture.md) | Sitemap, navigation, and special pages. | Draft |
| [Project Name Launch Checklist](docs/web/launch-checklist.md) | Verification checklist before a site goes live. | Draft |
| [Project Name Performance Budgets](docs/web/performance.md) | Performance targets and measured results. | Draft |
| [Project Name SEO Plan](docs/web/seo.md) | Target terms, metadata, structured data, and technical SEO per page. | Draft |
| [Project Name Site Brief](docs/web/site-brief.md) | The single job, visitor, proof, and bold idea that steer every design and content decision. | Draft |

### docs/ai

| Document | Purpose | Status |
|---|---|---|
| [Project Name Agent Setup](docs/ai/agent-setup.md) | Which agents work on the project and how each loads instructions, permissions, and memory. | Draft |
| [Project Doc Blueprint Integration Register](docs/ai/integration-register.md) | Every MCP server, skill, plugin, hook, and agent-side service the project uses, with data flow and approval. | Draft |
| [Project Name Loop Contract](docs/ai/loop-contract.md) | Limits, success criteria, and stop rules for unattended agent loops. | Draft |
| [Project Name Prompt Registry](docs/ai/prompt-registry.md) | Versioned list of prompts this project relies on, with test results. | Draft |
| [Project Name Workflow Graph](docs/ai/workflow-graph.md) | Nodes, handoffs, and gates for multi-agent or multi-stage work. | Draft |

### docs/engineering

| Document | Purpose | Status |
|---|---|---|
| [Project Name Code Review](docs/engineering/code-review.md) | Pull-request workflow and review checklist. | Draft |
| [Project Name Code Style](docs/engineering/code-style.md) | Coding conventions and tooling. | Draft |
| [Project Name Control Specification](docs/engineering/control-spec.md) | Dedicated specification for one safety-critical control (copy per control). | Draft |
| [Project Name Critical Bugs](docs/engineering/critical-bugs.md) | Release-blocking defects. | Draft |
| [Project Name Development](docs/engineering/development.md) | Local developer setup and commands. | Draft |
| [Project Name Known Issues](docs/engineering/known-issues.md) | Unresolved defects with impact and ownership. | Draft |
| [Project Name QA Testing](docs/engineering/qa-testing.md) | Manual QA passes and results. | Draft |
| [Project Name Setup](docs/engineering/setup.md) | Initial environment setup. | Draft |
| [Project Name Task Breakdown](docs/engineering/task-breakdown.md) | Milestones and tasks with dependencies. | Draft |
| [Project Name Testing](docs/engineering/testing.md) | Test strategy, layers, commands, and coverage. | Draft |

### docs/security

| Document | Purpose | Status |
|---|---|---|
| [Project Name Authorization Matrix](docs/security/authorization-matrix.md) | Defines what Claude and contributors may do autonomously, must ask about, or must never do without written approval. | Proposed |
| [Project Name Attack Surface](docs/security/attack-surface.md) | Inventory of externally reachable entry points. | Draft |
| [Project Name Authentication and Authorization](docs/security/auth.md) | Authentication mechanisms and access-control requirements. | Draft |
| [Project Name Critical Security Exposures](docs/security/critical-security-exposures.md) | Confirmed high-severity exposures and their remediation. | Draft |
| [Project Name Data Security](docs/security/data-security.md) | Handling of distinct security-sensitive data flows. | Draft |
| [Project Name Incident Response](docs/security/incident-response.md) | Steps for handling security or availability incidents. | Draft |
| [Project Name Secrets](docs/security/secrets.md) | Secret names, storage, access, and rotation, never values. | Draft |
| [Project Name Security Checklist](docs/security/security-checklist.md) | Verification checklist per change and release. | Draft |
| [Project Name Security Review](docs/security/security-review.md) | Dated security review results. | Draft |
| [Project Name Security](docs/security/security.md) | Security principles, data handling, privacy requirements, and responsibilities. | Draft |
| [Project Name Threat Model](docs/security/threat-model.md) | Assets, actors, trust boundaries, threats, and mitigations. | Draft |

### docs/operations

| Document | Purpose | Status |
|---|---|---|
| [Project Name Deployment](docs/operations/deployment.md) | Hosting, environments, and release process. | Draft |
| [Project Name Monitoring](docs/operations/monitoring.md) | Monitoring, alerting, and operational requirements. | Draft |
| [Project Name Operations](docs/operations/operations.md) | Day-to-day operational procedures. | Draft |
| [Project Name Preview Deployment](docs/operations/preview-deployment.md) | Preview environment process. | Draft |
| [Project Name Production Deployment](docs/operations/production-deployment.md) | Production release process. | Draft |

### playbooks

| Document | Purpose | Status |
|---|---|---|
| [Project Doc Blueprint Playbooks Index](playbooks/00-index.md) | Reading guide for the reusable engineering playbooks shared by every project. | Proposed |
| [Project Doc Blueprint Agent Compatibility Guide](playbooks/agent-compatibility.md) | How Claude Code, OpenCode, and Hermes read this kit, and what stays unverified. | Proposed |
| [Project Doc Blueprint Context and Memory Playbook](playbooks/context-and-memory.md) | How to give agents durable context and their own memory so they work across sessions and across tools. | Proposed |
| [Project Doc Blueprint Evals and Verification Playbook](playbooks/evals-and-verification.md) | How to test prompts, loops, and finished sites so "done" means verified. | Proposed |
| [Project Doc Blueprint Graph Engineering Playbook](playbooks/graph-engineering.md) | How to model agent work as graphs, and how to model a project's knowledge as a graph. | Proposed |
| [Project Doc Blueprint Integrations Playbook](playbooks/integrations.md) | How the kit loads instructions, configures agents, bounds permissions, uses memory plugins and the REA MCP, and hands sessions off, with six reviewed external repositories. | Proposed |
| [Project Doc Blueprint Loop Engineering Playbook](playbooks/loop-engineering.md) | How to design agent loops that make steady progress, verify themselves, and stop safely. | Proposed |
| [Project Doc Blueprint MCP Servers Playbook](playbooks/mcp-servers.md) | Rules and setup notes for the shadcn/ui, 21st.dev, Figma, and REA MCP servers. | Proposed |
| [Project Doc Blueprint Prompt Engineering Playbook](playbooks/prompt-engineering.md) | How to write senior-level prompts that any coding agent can execute and that can be verified. | Proposed |
| [Project Doc Blueprint Research Protocol](playbooks/research-protocol.md) | How an agent researches a project from its name alone and records evidence others can check. | Proposed |
| [Project Doc Blueprint Site Building Standards](playbooks/site-building-standards.md) | Quality bars and craft rules for building an excellent, fast, accessible, findable website. | Proposed |

### prompts

| Document | Purpose | Status |
|---|---|---|
| [Project Doc Blueprint Prompts Index](prompts/00-index.md) | Which prompt to use for which situation. | Proposed |
| [Project Doc Blueprint Project Prompt Generator](prompts/00-project-prompt-generator.md) | Self-contained meta-prompt: give an agent a project name, and it researches and writes a senior-level build prompt. | Proposed |
| [Project Doc Blueprint Build Master Prompt Template](prompts/01-build-master-prompt.md) | Fill-in template for a build prompt when you already know the project and don't need the generator. | Proposed |
| [Project Doc Blueprint Existing Project Audit Prompt](prompts/02-audit-existing-project.md) | Prompt for an agent to inspect an existing repository and produce an evidence-based documentation set. | Proposed |
| [Project Doc Blueprint Design Direction Prompt](prompts/03-design-direction.md) | Prompt for producing a distinctive, subject-specific design system before any UI code is written. | Proposed |
| [Project Doc Blueprint Content and SEO Prompt](prompts/04-content-and-seo.md) | Prompt for writing real page copy and an SEO plan grounded in research. | Proposed |
| [Project Doc Blueprint Adversarial Review Prompt](prompts/05-adversarial-review.md) | Prompt for a skeptical reviewer that finds problems in a built site or a doc set, without fixing them. | Proposed |
| [Project Doc Blueprint Loop Runner Prompt](prompts/06-loop-runner.md) | Prompt that makes an agent work in verified iterations against a written loop contract. | Proposed |
| [Project Doc Blueprint Graph Orchestrator Prompt](prompts/07-graph-orchestrator.md) | Prompt for a lead agent that runs a site build as a graph of focused subagents and gates. | Proposed |
| [Project Doc Blueprint Session Handoff Prompt](prompts/08-session-handoff.md) | Prompts to resume work in a fresh session and to close a session cleanly. | Proposed |
| [Project Doc Blueprint UI Build With Design MCPs Prompt](prompts/09-ui-build-with-design-mcps.md) | Prompt for building UI from a design system using only approved shadcn/ui, 21st.dev, and Figma MCP servers. | Proposed |

### memory

| Document | Purpose | Status |
|---|---|---|
| [Project Name Agent Memory](memory/README.md) | Shared working memory any agent reads at session start and updates at session end. | Draft |
| [Project Name Lessons](memory/lessons.md) | Learnings that should change future agent behavior on this project. | Draft |
| [Project Name Open Questions](memory/open-questions.md) | Questions awaiting the owner, with impact. | Open |
| [Project Name Progress Log](memory/progress-log.md) | Append-only record of sessions and iterations, newest last. | Draft |

### projects

| Document | Purpose | Status |
|---|---|---|
| [Project Doc Blueprint Projects Registry](projects/README.md) | Registry of projects created with scaffold.py new; each row links to a self-contained project folder. | Draft |

## Consolidation Map

| Subject | Documented in |
|---|---|
| — | — |

<!-- INDEX:END -->

## Open questions

- Which agents will you run first? Record them in `docs/ai/agent-setup.md` in each project.
- Does "graph engineering" mean workflow graphs, knowledge graphs, or both? The playbook covers both; confirm.
- Do you want each project's `scaffold.py` and `playbooks/` copied in (current behavior) or shared from one kit? Copying keeps each project self-contained but lets copies drift.

## Next recommended actions

1. Run `python scaffold.py new` on a real project and give `PROMPT-GENERATOR.md` to your agent.
2. Review `docs/security/authorization-matrix.md` and both permission configs, then tighten them.
3. Record the first prompt you rely on in `docs/ai/prompt-registry.md` after testing it on three inputs.
