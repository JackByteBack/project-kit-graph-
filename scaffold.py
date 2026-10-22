#!/usr/bin/env python3
"""Project Doc Blueprint scaffold (v3.1).

Generates a documentation tree from the Project Doc Blueprint, selects
conditional documents by trigger, builds the README index last, and validates
headers, links, index coverage and accidental secrets.

Usage:
  python scaffold.py list
  python scaffold.py new "My Project"   # projects/my-project/ with docs, memory, prompts, agent files
  python scaffold.py prompt "My Project" [--details "..."] [--out prompt.md]
                                        # print the attachable project-prompt generator
  python scaffold.py init --name "My App" --preset web-app --out ../my-app
  python scaffold.py init --name "My App" --triggers ui,db,auth --also setup
  python scaffold.py graph              # build docs/ai/doc-graph.md from document mentions
  python scaffold.py readme             # refresh the README index in place
  python scaffold.py validate           # exit code 1 on errors
"""
import argparse
import datetime
import json
import pathlib
import re
import shutil
import sys

KIT = pathlib.Path(__file__).resolve().parent
STATUSES = ("Draft", "Confirmed", "Accepted", "Proposed", "Open")
IDX_START, IDX_END = "<!-- INDEX:START -->", "<!-- INDEX:END -->"

TRIGGERS = {
    "ui": "Screens or user interfaces",
    "ui-deep": "Large UI needing a standalone design philosophy and UI architecture",
    "roles": "Multiple user roles",
    "content": "User-facing text or generated content",
    "contentfmt": "Specific file or content formats the project reads or writes",
    "controls": "Safety-critical or special-behavior controls",
    "demo": "Time-boxed demo or deliverable",
    "arch": "Components and architectural boundaries",
    "tech": "Selected technologies or external services",
    "layout": "Required directory layout",
    "style": "Defined coding conventions",
    "db": "Database or persistent data store",
    "api": "API or service interface",
    "jobs": "Queued or asynchronous work",
    "schedule": "Scheduled tasks",
    "devsetup": "Local developer setup",
    "testing": "Automated testing or QA",
    "pr": "Pull-request workflow",
    "deploy": "Hosting, environments, or releases",
    "plan": "Multi-stage implementation plan",
    "sensitive": "Personal, confidential, or sensitive data",
    "auth": "Login, roles, permissions, or sessions",
    "secrets": "Secret keys, tokens, or credentials",
    "incident": "Meaningful ongoing incident risk",
    "alternatives": "Significant architectural alternatives",
    "flows": "Complex application flows",
    "monitoring": "Monitoring and operational requirements",
    "dataflow": "Distinct security-sensitive data flows",
    "defects": "Significant unresolved defects",
    "review": "Formal security review or exposure tracking",
    "roadmap": "Multi-release product direction",
    "research": "Open product or technical research",
    "site": "Public website or web application",
    "seo": "Search visibility or discoverability matters",
    "analytics": "Analytics, tracking, or third-party scripts",
    "agentic": "AI agents build or operate the project (prompts, loops, graphs, memory)",
}

PRESETS = {
    "minimal": [],
    "web-app": ["ui", "content", "arch", "tech", "layout", "style", "devsetup",
                "testing", "deploy", "plan", "flows"],
    "api": ["arch", "tech", "db", "api", "auth", "sensitive", "secrets", "devsetup",
            "testing", "pr", "deploy", "monitoring", "plan"],
    "site": ["ui", "content", "arch", "tech", "layout", "style", "devsetup",
             "testing", "deploy", "plan", "flows", "site", "seo", "analytics", "agentic"],
    "full": list(TRIGGERS),
}

# ---------------------------------------------------------------- catalog
# Section tuple: (heading, hint, columns=None, status="Open", rows=None)
CATALOG = []


def D(name, folder, title, purpose, trig, sections=None, merged_into=None,
      status="Draft", body=None):
    CATALOG.append(dict(name=name, folder=folder, title=title, purpose=purpose,
                        trig=trig, sections=sections or [], merged_into=merged_into,
                        status=status, body=body))


TRIGGER_ROWS = [[d, "Open", k] for k, d in TRIGGERS.items()]

# ---- core
D("project-intake", "core", "Project Intake",
  "Captures the facts and needs that drive documentation selection.", "core", [
    ("Project name and purpose", "One paragraph. Source: owner."),
    ("Target users and their needs", "Who uses it and what they need. Source: owner."),
    ("Main features and intended outcomes", "Separate proposed features from implemented ones."),
    ("Current implementation and development stage", "Idea, prototype, in build, live. Cite repository evidence."),
    ("Technologies and frameworks", "Verified from manifests; unverified items stay Open."),
    ("Data collected, generated, stored, or transmitted", "List data classes, not real records."),
    ("User roles and permissions", "Roles and what each may do."),
    ("External integrations", "Each needs a decision entry before use (Rule 7)."),
    ("Security and privacy requirements", "Legal, contractual, or owner requirements."),
    ("Existing documentation and conventions", "What already exists and must be preserved (Rule 10)."),
    ("Deployment and operational requirements", "Hosting, environments, uptime, budget."),
    ("Trigger checklist", "Mark each characteristic Yes or No, then pass the flags to scaffold.py.",
     ["Characteristic", "Present?", "Flag"], "Open", TRIGGER_ROWS),
])
D("instructions", "core", "Project Instructions",
  "Project-specific rules for AI-assisted work and engineering collaboration.", "core", [
    ("Read-first documentation", "Ordered list of docs to read before any change.", None, "Proposed"),
    ("Repository-specific rules", "Conventions verified in the repo."),
    ("Implementation constraints", "Frameworks, versions, forbidden patterns."),
    ("Security requirements", "Reference security.md; list non-negotiables."),
    ("Testing expectations", "Reference testing.md; what must pass before done."),
    ("Documentation maintenance rules", "Which docs to update after which changes.", None, "Proposed"),
    ("Permission boundaries", "Reference docs/security/authorization-matrix.md.", None, "Proposed"),
    ("Definition of done", "Checklist for finished work."),
    ("Rules for asking questions", "Ask only when the repo cannot answer and it materially matters.", None, "Proposed"),
    ("Rules for handling uncertainty", "Mark Open, do not guess, do not fabricate.", None, "Proposed"),
])
D("agents", "core", "Coding Agent Rules",
  "Project-specific coding-agent rules that extend the root AGENTS.md.", "core", [
    ("Relationship to the root AGENTS.md", "The root AGENTS.md holds the universal rules and is what agents load. Put only project-specific additions here and keep them consistent with it.", None, "Proposed"),
    ("Read-first documentation", "Files an agent reads at session start.", None, "Proposed"),
    ("Agent recognition", "Which file the intended agent actually loads (CLAUDE.md, AGENTS.md). Verify; do not assume."),
    ("Development constraints", "Allowed commands, scope limits, branch rules."),
    ("Authorization tiers", "Summarize T0 to T4 from the authorization matrix.", None, "Proposed"),
    ("Definition of done", "Tests run, docs updated, current-state.md updated."),
])
D("current-state", "core", "Current State",
  "Verified project status, progress, open items, blockers, and known issues.", "core", [
    ("Current phase", "Single phase name with evidence."),
    ("Verified implementation status", "Only what is verified in code or tests."),
    ("Completed work", "Dated entries with evidence links."),
    ("In-progress work", "Owner and status per item."),
    ("Open items", "Every significant open item, with impact and whether it blocks."),
    ("Known issues", "Track each issue in one table.",
     ["ID", "Issue", "Impact", "Owner", "Status"]),
    ("Technical debt", "Known shortcuts and their cost."),
    ("Immediate blockers", "What stops progress and who can unblock."),
    ("Next actions", "Ordered, concrete next steps."),
])
D("decisions", "core", "Decisions",
  "Accepted decisions, rejected alternatives, and pending decisions with rationale.", "core", [
    ("Accepted", "Never delete; supersede with a new entry (Rule 5).",
     ["ID", "Date", "Decision", "Reason", "Status"]),
    ("Rejected Options", "Options considered and declined.",
     ["ID", "Option", "Reason Rejected", "Related Decision"]),
    ("Pending", "A recommendation stays Proposed until the owner approves.",
     ["ID", "Decision Needed", "Options", "Recommendation", "Decision Owner", "Status"]),
])
D("prd", "core", "Product Requirements",
  "Problem, users, goals, scope, requirements, and success criteria.", "core", [
    ("Problem statement", "What problem, for whom, why now."),
    ("Target users", "Reference define-the-user.md if present."),
    ("User needs", "Needs, not solutions."),
    ("Product goals", "Measurable where possible."),
    ("Non-goals", "Explicitly out of scope."),
    ("Scope", "In scope for this release."),
    ("Functional requirements", "Mark each Confirmed or Proposed.", ["ID", "Requirement", "Status", "Source"]),
    ("Non-functional requirements", "Performance, accessibility, privacy, availability.", ["ID", "Requirement", "Status", "Source"]),
    ("Acceptance criteria", "Testable statements mapped to requirement IDs."),
    ("Success metrics", "How success is measured and by when."),
    ("Constraints", "Budget, time, platform, legal."),
    ("Dependencies", "Each needs a decision entry (Rule 7)."),
    ("Open questions", "Unresolved requirements."),
])
D("glossary", "core", "Glossary",
  "Domain terminology, abbreviations, and identifiers.", "core", [
    ("Terms", "Create only if the domain has real terminology.", ["Term", "Definition", "Source"]),
])
D("status-labels", "core", "Status Labels",
  "Defines the knowledge-status labels used across all documents.", "core",
  status="Accepted", body=[
    "## Labels", "",
    "| Label | Meaning | Who may set it |", "|---|---|---|",
    "| Confirmed | Verified by the project owner or authoritative project evidence | Claude, citing the evidence source |",
    "| Proposed | A recommendation or design that has not been approved | Claude |",
    "| Open | Missing, uncertain, or awaiting a decision | Claude |",
    "| Accepted | A proposed approach explicitly approved by the owner | Owner only |",
    "| Rejected | An option considered and declined | Owner, with recorded reason |",
    "",
    "## Evidence sources", "",
    "Record the kind of evidence when it matters: owner statement, source code, test run, configuration, external documentation. An owner-confirmed requirement and a code-verified implementation detail are different kinds of evidence.",
    "",
    "## Rules", "",
    "- One primary status per document in the header.",
    "- Apply Confirmed, Proposed, and Open to individual statements.",
    "- Never mark a document Confirmed while it contains unresolved assumptions.",
    "- A recommendation stays Proposed until the owner approves it, then becomes Accepted.",
])

# ---- product
D("idea", "product", "Idea", "Original concept and motivation before requirements.", "research", [
    ("Concept", "What the idea is, in the owner's words."), ("Motivation", "Why it matters.")])
D("research", "product", "Research", "Findings from market, user, or technical research.", "research", [
    ("Questions", "What needs answering.", ["ID", "Question", "Method", "Status"]),
    ("Findings", "Each finding cites its source; unverified items stay Open.")])
D("define-the-user", "product", "User Definition", "Who the users are, what they need, and their constraints.", "ui", [
    ("Primary users", "Roles, goals, context."), ("Pain points", "Observed or owner-stated; label which."),
    ("Constraints", "Devices, connectivity, accessibility needs.")], merged_into="prd")
D("user-journeys", "product", "User Journeys", "End-to-end flows each user role follows.", ["ui", "roles"], [
    ("Journey inventory", "One section per role; mark each flow Confirmed or Proposed.", ["ID", "Role", "Goal", "Status"]),
    ("Flow detail", "Steps, entry points, success and failure states.")])
D("admin-journeys", "product", "Admin Journeys", "Flows for administrators and operators.", "roles", [
    ("Admin tasks", "Tasks, required permissions, audit expectations.", ["ID", "Task", "Permission", "Status"])])
D("app-flow", "product", "Application Flow", "Complex application flows and state transitions.", "flows", [
    ("Primary flow", "Include a Mermaid diagram that matches the implementation."),
    ("State transitions", "Valid states and guards."), ("Failure paths", "What happens on error.")])
D("demo", "product", "Demo Plan", "Scope and script for a time-boxed demo or deliverable.", "demo", [
    ("Deadline and audience", "Date and who sees it."), ("Demo scope", "What is shown and what is deliberately cut."),
    ("Script", "Ordered steps with fallback if something fails.")])
D("roadmap", "product", "Roadmap", "Planned direction across releases.", "roadmap", [
    ("Now / Next / Later", "Mark all future items Proposed.", ["Horizon", "Item", "Status"])])
D("iteration", "product", "Iteration Log", "How feedback becomes changes between releases.", "roadmap", [
    ("Feedback intake", "Where feedback arrives and who triages.")], merged_into="roadmap")
D("content-guidelines", "product", "Content Guidelines", "Voice, tone, and rules for user-facing and generated text.", "content", [
    ("Voice and tone", "Definitions with examples."), ("Terminology", "Reference glossary.md."),
    ("Generated content rules", "Review, labeling, and safety rules for generated text.")])
D("file-content-format", "product", "File and Content Formats", "Formats the project reads or writes.", "contentfmt", [
    ("Formats", "Format, schema, validation, example with synthetic data.", ["Format", "Schema", "Validation", "Status"])])

# ---- architecture
D("architecture", "architecture", "Architecture", "Components, boundaries, data flows, and trust boundaries.", "arch", [
    ("System overview", "Describe the existing implementation accurately."),
    ("Components and responsibilities", "One row per component.", ["Component", "Responsibility", "Boundary", "Status"]),
    ("External integrations", "Each approved in decisions.md."),
    ("Data flows", "Sources, sinks, data classes."),
    ("Trust boundaries", "Where trust changes."),
    ("Failure points", "What breaks and what happens."),
    ("Scalability considerations", "Known limits."),
    ("Security considerations", "Reference threat-model.md."),
    ("Architecture diagram", "Mermaid. Must match the real system.", None, "Open"),
    ("Proposed future architecture", "Keep separate from current architecture.", None, "Proposed"),
])
D("technology", "architecture", "Technology", "Selected technologies, versions, and rationale.", "tech", [
    ("Technology inventory", "Verified versions only.",
     ["Technology", "Version", "Purpose", "Reason selected", "Alternatives", "Approval"]),
    ("Compatibility constraints", "Version and platform limits."),
    ("Operational and security implications", "Cost, hosting, supply chain."),
    ("Technology diagram", "Mermaid, when it clarifies interactions.")])
D("backend-schema", "architecture", "Backend Schema", "Entities, fields, relationships, sensitivity, and retention.", "db", [
    ("Entities", "Fields, types, keys.", ["Entity", "Fields", "Keys", "Sensitivity", "Status"]),
    ("Relationships and constraints", "Foreign keys, indexes."),
    ("Retention and access", "How long, who can read or write."),
    ("Audit requirements", "What must be logged."),
    ("Migration considerations", "Ordering, rollback, data safety.")])
D("api", "architecture", "API", "Endpoints, access rules, and error formats.", "api", [
    ("Endpoints", "Verified against code; unverified stays Open.", ["Method", "Path", "Access", "Status"]),
    ("Error format", "Shape and codes."), ("Versioning and rate limits", "Policy.")])
D("project-structure", "architecture", "Project Structure", "Required directory layout and conventions.", "layout", [
    ("Directory layout", "Verified tree with the purpose of each directory."),
    ("Placement rules", "Where new files go.")])
D("background-jobs", "architecture", "Background Jobs", "Queued and asynchronous work.", "jobs", [
    ("Jobs", "Trigger, retries, idempotency, failure handling.", ["Job", "Trigger", "Retry policy", "Status"])])
D("scheduled-tasks", "architecture", "Scheduled Tasks", "Scheduled behavior and ownership.", "schedule", [
    ("Schedules", "Cron, owner, expected duration, failure alert.", ["Task", "Schedule", "Owner", "Status"])])
D("rejected-options", "architecture", "Rejected Options", "Significant alternatives considered and declined.", "alternatives", [
    ("Options", "Link each to a decision ID.", ["ID", "Option", "Reason Rejected", "Related Decision"])])

# ---- design
D("design-system", "design", "Design System", "Visual language and reusable UI patterns.", "ui", [
    ("Design reference review", "Record whether https://getdesign.md was actually accessed. Unreviewed means Open."),
    ("Design philosophy", "Principles specific to this project."), ("Visual hierarchy", "What draws attention first."),
    ("Typography", "Families, scale, weights."), ("Color system", "Tokens and contrast ratios."),
    ("Spacing", "Scale and layout grid."), ("Responsive layouts", "Breakpoints and behavior."),
    ("Components", "Inventory and states."), ("Navigation", "Structure and patterns."),
    ("Interaction states", "Hover, focus, active, disabled."), ("Motion", "Durations, easing, reduced-motion."),
    ("Loading and error states", "Patterns."), ("Mobile performance", "Budgets.")])
D("design", "design", "Design Notes", "Design rationale and decisions for specific surfaces.", "ui-deep", [
    ("Rationale", "Why the design is the way it is.")], merged_into="design-system")
D("accessibility", "design", "Accessibility", "Accessibility requirements and verification.", "ui", [
    ("Target standard", "For example WCAG 2.2 AA. Mark Open until the owner confirms."),
    ("Verification", "Tools and manual checks actually run.")])
D("ui-architecture", "design", "UI Architecture", "Front-end structure, state, and rendering strategy.", "ui-deep", [
    ("Rendering strategy", "SSR, SSG, SPA. Verified from code."), ("State management", "Where state lives."),
    ("Component structure", "Layers and conventions.")])

# ---- engineering
D("code-style", "engineering", "Code Style", "Coding conventions and tooling.", "style", [
    ("Conventions", "Naming, formatting, linting. Verified from config files."),
    ("Tooling", "Formatter and linter commands.")])
D("development", "engineering", "Development", "Local developer setup and commands.", "devsetup", [
    ("Prerequisites", "Versions verified from manifests."), ("Setup steps", "Commands that match the real toolchain."),
    ("Environment variables", "Names only, never values. See secrets.md."), ("Common tasks", "Run, test, build.")])
D("setup", "engineering", "Setup", "Initial environment setup.", "devsetup", [
    ("Setup", "Prefer folding into development.md.")], merged_into="development")
D("testing", "engineering", "Testing", "Test strategy, layers, commands, and coverage.", "testing", [
    ("Test strategy", "What is tested and why."),
    ("Test layers", "Existing, planned, executed. Keep them distinct.", ["Layer", "Exists", "Executed", "Command"]),
    ("Acceptance criteria mapping", "Map PRD criteria to tests."),
    ("Test data and synthetic-data rules", "No production data."),
    ("Device and browser matrix", "When applicable."),
    ("Security and regression coverage", "Gaps are Open."),
    ("CI requirements", "Required checks."), ("Known testing gaps", "Honest list.")])
D("qa-testing", "engineering", "QA Testing", "Manual QA passes and results.", "testing", [
    ("QA passes", "Record only passes actually performed.", ["Date", "Scope", "Result", "Evidence"])], merged_into="testing")
D("code-review", "engineering", "Code Review", "Pull-request workflow and review checklist.", "pr", [
    ("Workflow", "Branching, reviewers, merge rules."), ("Review checklist", "Security, tests, docs, dependencies.")])
D("known-issues", "engineering", "Known Issues", "Unresolved defects with impact and ownership.", "defects", [
    ("Issues", "Move here when current-state.md gets crowded.", ["ID", "Issue", "Impact", "Owner", "Status"])])
D("critical-bugs", "engineering", "Critical Bugs", "Release-blocking defects.", "defects", [
    ("Critical bugs", "Evidence and mitigation per bug.", ["ID", "Bug", "Evidence", "Impact", "Status"])], merged_into="known-issues")
D("task-breakdown", "engineering", "Task Breakdown", "Milestones and tasks with dependencies.", "plan", [
    ("Milestones", "Track blockers.", ["ID", "Goal", "Blocked By", "Status"]),
    ("Tasks", "Each task has acceptance criteria elsewhere.", ["ID", "Task", "Milestone", "Depends On", "Status"])])
D("control-spec", "engineering", "Control Specification", "Dedicated specification for one safety-critical control (copy per control).", "controls", [
    ("Control", "Name and purpose."), ("Required behavior", "Exact, testable behavior."),
    ("Failure behavior", "What happens when the control fails."), ("Verification", "How it is tested.")])

# ---- security
D("authorization-matrix", "security", "Authorization Matrix",
  "Defines what Claude and contributors may do autonomously, must ask about, or must never do without written approval.", "core",
  status="Proposed", body=[
    "## Tiers", "",
    "| Tier | Name | Autonomy |", "|---|---|---|",
    "| T0 | Read | Autonomous |",
    "| T1 | Docs | Autonomous |",
    "| T2 | Code | Autonomous only if the task authorizes implementation |",
    "| T3 | Ask first | Record a Proposed decision, wait for owner approval |",
    "| T4 | Forbidden without written approval | Stop; never proceed on inference |",
    "",
    "## Action matrix", "",
    "| Action | Tier | Approval | Record in |", "|---|---|---|---|",
    "| Read source, docs, configuration (never secret values) | T0 | None | n/a |",
    "| Run read-only commands | T0 | None | n/a |",
    "| Create or edit documentation | T1 | None | current-state.md |",
    "| Edit memory/ and research/ files | T1 | None | memory/progress-log.md |",
    "| Edit source within task scope | T2 | Task authorizes implementation | current-state.md |",
    "| Run tests, linters, builds | T2 | Task authorizes implementation | testing.md |",
    "| Add a dependency | T3 | Owner approval | decisions.md |",
    "| Adopt a third-party service | T3 | Owner approval | decisions.md |",
    "| Enable an MCP server, install a third-party skill or plugin, or enable agent hooks | T3 | Owner approval; read the code first; pin the version | integration-register.md, decisions.md |",
    "| Run `rea setup` or use a reverse-engineering tool on any target | T3 | Owner approval plus recorded authorization for the target | decisions.md |",
    "| Run a many-sub-agent job such as /arena | T3 | Owner approves the cost | integration-register.md |",
    "| Send project or design content to a remote MCP server | T3 | Owner approval; no confidential material | integration-register.md |",
    "| Introduce a material data flow | T3 | Owner approval | decisions.md, data-security.md |",
    "| Database schema migration | T3 | Owner approval plus rollback plan | decisions.md, backend-schema.md |",
    "| Change CI/CD configuration | T3 | Owner approval | decisions.md |",
    "| Delete files or directories | T3 | Owner approval | current-state.md |",
    "| Change privacy or data-collection behavior | T3 | Owner approval | decisions.md, security.md |",
    "| Weaken a security control | T4 | Written owner approval | decisions.md |",
    "| Handle or rotate secrets | T4 | Written owner approval | secrets.md (names only) |",
    "| Deploy to production | T4 | Written owner approval | production release checklist |",
    "| Modify production data or access permissions | T4 | Written owner approval | decisions.md |",
    "| Destructive operations (force push, drop, recursive delete) | T4 | Written owner approval | decisions.md |",
    "| Expose or transmit secrets | T4 | Never permitted | n/a |",
    "",
    "## Enforcement mapping", "",
    "`.claude/settings.json` implements this matrix: `allow` covers T0 and T1, `ask` covers T2 and T3, `deny` covers T4 and secret paths. The file is a starting point; **Open**: review and tighten per project.",
    "",
    "## Approval record", "",
    "| ID | Action | Requested by | Approved by | Date | Scope | Expiry |", "|---|---|---|---|---|---|---|",
    "| — | — | — | — | — | — | — |",
])
D("security", "security", "Security", "Security principles, data handling, privacy requirements, and responsibilities.", "sensitive", [
    ("Principles", "Proportionate to real risk."), ("Data classification", "Classes and handling rules.", ["Class", "Examples", "Handling", "Status"]),
    ("Privacy requirements", "Legal and owner requirements."), ("Responsibilities", "Who owns what."),
    ("Findings", "Evidence-based only.", ["ID", "Finding", "Evidence", "Impact", "Severity", "Mitigation", "Status"])])
D("auth", "security", "Authentication and Authorization", "Authentication mechanisms and access-control requirements.", ["auth", "roles"], [
    ("Authentication provider", "Open until confirmed."), ("Session management", "Proposed default: HTTP-only secure cookies if compatible.", None, "Proposed"),
    ("Roles and permissions", "Role to permission mapping.", ["Role", "Permissions", "Status"]),
    ("Access-control checks", "Where enforced and how verified.")])
D("data-security", "security", "Data Security", "Handling of distinct security-sensitive data flows.", "dataflow", [
    ("Sensitive data flows", "Source, sink, protection in transit and at rest.", ["Flow", "Data class", "Protection", "Status"])])
D("threat-model", "security", "Threat Model", "Assets, actors, trust boundaries, threats, and mitigations.", "sensitive", [
    ("Assets", "What is worth protecting."), ("Actors", "Legitimate and hostile."),
    ("Trust boundaries", "Reference architecture.md."),
    ("Attack surface", "Entry points."),
    ("Threats and mitigations", "Separate confirmed, suspected, and unverified.", ["ID", "Finding", "Evidence", "Impact", "Severity", "Mitigation", "Status"]),
    ("Residual risk", "Accepted risks with owner.")])
D("attack-surface", "security", "Attack Surface", "Inventory of externally reachable entry points.", "sensitive", [
    ("Entry points", "Verified from code or configuration.", ["Entry point", "Exposure", "Controls", "Status"])], merged_into="threat-model")
D("secrets", "security", "Secrets", "Secret names, storage, access, and rotation, never values.", "secrets", [
    ("Secret inventory", "Names only. Use YOUR_API_KEY_HERE style placeholders.", ["Name", "Storage", "Access", "Rotation", "Status"]),
    ("Rotation procedure", "Steps."), ("Leak response", "Reference incident-response.md.")])
D("security-checklist", "security", "Security Checklist", "Verification checklist per change and release.", "sensitive", [
    ("Per change or pull request", "- [ ] Tick only after the control is verified."),
    ("Before preview deployment", "- [ ] Tick only after verified."),
    ("Before production release", "- [ ] Tick only after verified."),
    ("After security-sensitive changes", "- [ ] Tick only after verified.")])
D("security-review", "security", "Security Review", "Dated security review results.", "review", [
    ("Review log", "Scope, method, result, evidence.", ["Date", "Scope", "Method", "Result"])])
D("critical-security-exposures", "security", "Critical Security Exposures", "Confirmed high-severity exposures and their remediation.", "review", [
    ("Exposures", "Confirmed only.", ["ID", "Finding", "Evidence", "Impact", "Severity", "Mitigation", "Status"])])
D("incident-response", "security", "Incident Response", "Steps for handling security or availability incidents.", "incident", [
    ("Detection and triage", "Signals and severity."), ("Containment", "First actions."),
    ("Communication", "Who is told, when."), ("Recovery and review", "Post-incident record.")])

# ---- operations
D("deployment", "operations", "Deployment", "Hosting, environments, and release process.", "deploy", [
    ("Environments", "Verified from configuration.", ["Environment", "Purpose", "Access", "Status"]),
    ("Release process", "Steps. Production release needs written owner approval (T4)."),
    ("Rollback", "How to revert."), ("Monitoring", "Or link monitoring.md.")])
D("preview-deployment", "operations", "Preview Deployment", "Preview environment process.", "deploy", [
    ("Process", "Prefer folding into deployment.md.")], merged_into="deployment")
D("production-deployment", "operations", "Production Deployment", "Production release process.", "deploy", [
    ("Process", "Prefer folding into deployment.md.")], merged_into="deployment")
D("monitoring", "operations", "Monitoring", "Monitoring, alerting, and operational requirements.", "monitoring", [
    ("Signals", "Metrics, logs, traces.", ["Signal", "Source", "Alert", "Status"]),
    ("Alerting and ownership", "Who responds.")])
D("operations", "operations", "Operations", "Day-to-day operational procedures.", "monitoring", [
    ("Runbook", "Routine procedures.")], merged_into="monitoring")

# ---- web (site projects)
PERF_ROWS = [
    ["Largest Contentful Paint", "2.5 s or less (mobile, p75)", "—", "—", "Proposed"],
    ["Interaction to Next Paint", "200 ms or less", "—", "—", "Proposed"],
    ["Cumulative Layout Shift", "0.1 or less", "—", "—", "Proposed"],
    ["JavaScript on a content page", "As small as the job allows; justify anything over about 100 KB compressed", "—", "—", "Proposed"],
    ["Images", "Modern formats, responsive srcset, explicit dimensions", "—", "—", "Proposed"],
    ["Fonts", "Few families and weights, font-display swap, fallback stacks", "—", "—", "Proposed"],
]
D("site-brief", "web", "Site Brief", "The single job, visitor, proof, and bold idea that steer every design and content decision.", "site", [
    ("The job", "One sentence: what the site must get a visitor to do or understand."),
    ("Primary visitor", "Who, in what state of mind, on what device. Source: research dossier or owner."),
    ("Proof", "What makes the claim believable. Cite sources."),
    ("The one bold idea", "One distinctive decision in type, color, layout, or interaction. Everything else stays quiet.", None, "Proposed"),
    ("Success measures", "How you will know it worked.", ["Measure", "Target", "Source", "Status"]),
    ("Out of scope", "What the site deliberately does not do.")])
D("information-architecture", "web", "Information Architecture", "Sitemap, navigation, and special pages.", "site", [
    ("Sitemap", "One job per page and one primary action per page.", ["Page", "URL", "Job", "Primary action", "Status"]),
    ("Navigation", "Labels visitors recognize; important content within two clicks."),
    ("Special pages", "404, empty, loading, and error states."),
    ("URL rules", "Short, lowercase, stable; redirects for moved pages.")])
D("seo", "web", "SEO Plan", "Target terms, metadata, structured data, and technical SEO per page.", "seo", [
    ("Target terms", "Map terms to pages using the research dossier.", ["Page", "Term", "Intent", "Status"]),
    ("Metadata", "Unique title and description per page.", ["Page", "Title draft", "Description draft", "Status"]),
    ("Structured data", "Only where it matches real content."),
    ("Technical SEO", "Canonical URLs, sitemap.xml, robots.txt, social card metadata.")])
D("performance", "web", "Performance Budgets", "Performance targets and measured results.", "site", [
    ("Budgets", "Targets are Proposed defaults. Record the environment with every measurement and leave Measured empty until a run happens.",
     ["Metric", "Target", "Measured", "Environment", "Status"], "Proposed", PERF_ROWS)])
D("analytics-privacy", "web", "Analytics and Privacy", "What data the site collects, which third parties receive it, and under which rules.", "analytics", [
    ("Data collected", "List data classes, purpose, and retention. Collect the minimum.", ["Data", "Purpose", "Retention", "Status"]),
    ("Third-party scripts and services", "Each is a dependency and a data flow and needs a decision entry and owner approval.",
     ["Service", "Purpose", "Data sent", "Decision ID", "Status"]),
    ("Consent and regional rules", "Which rules apply to the audience. Open until confirmed."),
    ("Cookies and storage", "What is set, why, and for how long.")])
D("launch-checklist", "web", "Launch Checklist", "Verification checklist before a site goes live.", "site", status="Draft", body=[
    "Tick a box only after the check has run and its result is recorded in testing.md. A checklist is not proof by itself.", "",
    "## Content", "",
    "- [ ] Content proofread; no unmarked placeholders",
    "- [ ] Every factual claim has a source or is marked Open", "",
    "## Search and sharing", "",
    "- [ ] Unique title and description on every page",
    "- [ ] Sitemap and robots live; canonical URLs correct",
    "- [ ] Social card metadata and image checked", "",
    "## Quality", "",
    "- [ ] Accessibility scan and keyboard pass done",
    "- [ ] Performance budgets met on mobile",
    "- [ ] Light and dark themes checked",
    "- [ ] 404 and error pages designed",
    "- [ ] Forms tested end to end, including failure paths", "",
    "## Security and privacy", "",
    "- [ ] Security headers set; dependencies audited",
    "- [ ] Analytics and consent behavior reviewed",
    "- [ ] No secrets in client code or the repository", "",
    "## Release", "",
    "- [ ] Redirects from old URLs in place (if any)",
    "- [ ] Rollback understood",
    "- [ ] Written owner approval recorded for production release (T4)",
])

# ---- ai (agent-operated projects)
LOOP_ROWS = [[f, "—", "Open"] for f in (
    "Goal", "Success criteria", "Tier", "Iteration cap", "Time or cost cap",
    "Per-iteration scope", "State files", "Verification command", "Stop conditions", "Escalation")]
D("agent-setup", "ai", "Agent Setup", "Which agents work on the project and how each loads instructions, permissions, and memory.", "agentic", [
    ("Agents in use", "One row per agent. Mark Verified only after checking that agent's current documentation.",
     ["Agent", "Instruction file loaded", "Permission config", "Native memory", "Verified"]),
    ("Shared memory", "Project memory lives in memory/ so every agent reads and writes the same files."),
    ("Context file size", "Keep AGENTS.md under 20,000 characters. Hermes truncates longer startup files; scaffold.py validate warns above that."),
    ("Open compatibility items", "Track unresolved agent behavior here. Start from playbooks/agent-compatibility.md section 5.")])
D("prompt-registry", "ai", "Prompt Registry", "Versioned list of prompts this project relies on, with test results.", "agentic", [
    ("Prompts", "Record a prompt before relying on it. Results come only from runs that happened.",
     ["ID", "Purpose", "File", "Version", "Last tested", "Result", "Status"]),
    ("Eval sets", "Where each prompt's test inputs and rubric live.", ["Prompt ID", "Eval set path", "Rubric", "Status"])])
D("loop-contract", "ai", "Loop Contract", "Limits, success criteria, and stop rules for unattended agent loops.", "agentic", [
    ("Contract", "Fill every field before any unattended run. Caps are hard limits. See playbooks/loop-engineering.md.",
     ["Field", "Value", "Status"], "Open", LOOP_ROWS)])
D("workflow-graph", "ai", "Workflow Graph", "Nodes, handoffs, and gates for multi-agent or multi-stage work.", "agentic", [
    ("Nodes", "One row per node. See playbooks/graph-engineering.md section A3.",
     ["ID", "Role", "Inputs", "Outputs", "Tier", "Exit criteria", "On failure", "Context"]),
    ("Edges", "Handoffs and conditions.", ["From", "To", "Condition", "Payload format"]),
    ("Diagram", "Mermaid. Must match the real workflow.")])
D("integration-register", "ai", "Integration Register",
  "Every MCP server, skill, plugin, hook, and agent-side service the project uses, with data flow and approval.", "agentic", [
    ("Register", "One row per integration. Nothing is enabled without an Approved row (Rule 7). Pin the version or commit reviewed. Credentials appear by variable name only.",
     ["Integration", "Kind", "Version or commit", "Purpose", "Data sent", "Credential name", "Tier", "Decision ID", "Status"]),
    ("Verification record", "After enabling: connected, one read-only call, no secrets in the repo.",
     ["Integration", "Connected", "Read-only call result", "Secrets check", "Date"]),
    ("Component and asset sources", "Anything retrieved from an outside registry or generator: source, date, license or terms. Unknown license means Open and not shipped.",
     ["Item", "Source", "Retrieved", "License or terms", "Status"])])

BY_NAME = {d["name"]: d for d in CATALOG}
READ_ORDER = ["AGENTS", "CLAUDE", "BRIEF", "PROMPT-GENERATOR", "BUILD-PROMPT", "00-index", "README",
              "project-intake", "instructions", "status-labels", "prd", "decisions", "current-state",
              "agents", "authorization-matrix", "glossary", "architecture", "technology"]


# ---------------------------------------------------------------- rendering
def header(project, title, purpose, status, today):
    return [f"# Title: {project} {title}", "", purpose, "", f"Status: {status}", f"Last updated: {today}", ""]


def render_doc(doc, project, today):
    out = header(project, doc["title"], doc["purpose"], doc["status"], today)
    if doc["body"]:
        return "\n".join(out + doc["body"]) + "\n"
    for s in doc["sections"]:
        heading, hint = s[0], s[1]
        cols = s[2] if len(s) > 2 else None
        status = s[3] if len(s) > 3 and s[3] else "Open"
        rows = s[4] if len(s) > 4 else None
        out += [f"## {heading}", "", f"**Status: {status}**", "", f"> {hint}", ""]
        if cols:
            out.append("| " + " | ".join(cols) + " |")
            out.append("|" + "|".join("---" for _ in cols) + "|")
            for r in (rows or [["—"] * len(cols)]):
                out.append("| " + " | ".join(r) + " |")
            out.append("")
        code = s[5] if len(s) > 5 else None
        items = s[6] if len(s) > 6 else None
        if code:
            out += ["```mermaid", code, "```", ""]
        if items:
            out += [f"- [ ] {i}" for i in items] + [""]
    return "\n".join(out)


def doc_trigs(doc):
    t = doc["trig"]
    return [t] if isinstance(t, str) else list(t)


def doc_path(doc):
    return pathlib.PurePosixPath("docs") / doc["folder"] / f"{doc['name']}.md"


def resolve(args):
    chosen = set()
    if args.preset:
        chosen |= set(PRESETS.get(args.preset, []))
    if args.triggers:
        chosen |= set(x.strip() for x in args.triggers.split(",") if x.strip())
    if args.preset == "all" or "all" in chosen:
        chosen = set(TRIGGERS)
        standalone_all = True
    else:
        standalone_all = False
    unknown = chosen - set(TRIGGERS)
    if unknown:
        sys.exit(f"Unknown trigger(s): {', '.join(sorted(unknown))}. Run: python scaffold.py list")
    also = set(x.strip() for x in (args.also or "").split(",") if x.strip())
    selected, reasons = [], {}
    for d in CATALOG:
        core = "core" in doc_trigs(d)
        hit = [t for t in doc_trigs(d) if t in chosen]
        if d["merged_into"]:
            if standalone_all or d["name"] in also:
                selected.append(d); reasons[d["name"]] = ("Optional", "Requested standalone")
            else:
                reasons[d["name"]] = ("Consolidated", f"Covered in {d['merged_into']}.md")
        elif core:
            selected.append(d); reasons[d["name"]] = ("Required", "Mandatory core")
        elif hit:
            selected.append(d); reasons[d["name"]] = ("Recommended", f"Trigger: {', '.join(hit)}")
        else:
            reasons[d["name"]] = ("Not needed", f"Trigger absent: {', '.join(doc_trigs(d))}")
    return selected, reasons


def write_if_absent(path, text):
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def selection_log(project, reasons, today):
    out = header(project, "Selection Log",
                 "Records why each candidate document was created, consolidated, or omitted.", "Proposed", today)
    out += ["Generated mechanically from the chosen triggers. **Open**: owner review of every Not needed entry.", "",
            "| Document | Classification | Reason |", "|---|---|---|"]
    for d in CATALOG:
        c, r = reasons[d["name"]]
        out.append(f"| {d['name']}.md | {c} | {r} |")
    return "\n".join(out) + "\n"


ROOT_FILES = ("README.md", "AGENTS.md", "CLAUDE.md", "BRIEF.md", "BUILD-PROMPT.md", "PROMPT-GENERATOR.md")
DOC_DIRS = ("docs", "playbooks", "prompts", "memory", "research")
GROUP_ORDER = ["Start here", "docs/core", "docs/product", "docs/architecture", "docs/design",
               "docs/web", "docs/ai", "docs/engineering", "docs/security", "docs/operations",
               "playbooks", "prompts", "memory", "research", "projects"]
AGENT_KIT = ("AGENTS.md", "CLAUDE.md", "opencode.json", "scaffold.py", ".claude", "playbooks", "prompts", "integrations")
AGENTS_MAX_CHARS = 20000  # Hermes startup-file floor; longer files may be truncated


def md_files(root):
    out = [root / n for n in ROOT_FILES if (root / n).exists()]
    for d in DOC_DIRS:
        if (root / d).is_dir():
            out += sorted((root / d).rglob("*.md"))
    reg = root / "projects" / "README.md"
    if reg.exists():
        out.append(reg)
    return out


def group_of(rel):
    parts = rel.split("/")
    if len(parts) == 1:
        return "Start here"
    if parts[0] == "docs":
        return f"docs/{parts[1]}" if len(parts) > 2 else "docs/core"
    return parts[0]


def scan_docs(root):
    items = []
    for p in md_files(root):
        rel = p.relative_to(root).as_posix()
        if rel == "README.md":
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        title = lines[0].replace("# Title: ", "") if lines else p.stem
        purpose = (lines[2] if len(lines) > 2 else "").replace("|", "/")
        status = next((l.split(":", 1)[1].strip() for l in lines[:10] if l.startswith("Status:")), "?")
        items.append((rel, p.stem, title, purpose, status, group_of(rel)))
    return items


def index_block(root):
    items = scan_docs(root)
    by = {}
    for it in items:
        by.setdefault(it[5], []).append(it)
    order = [g for g in GROUP_ORDER if g in by] + sorted(g for g in by if g not in GROUP_ORDER)
    rank = {n: i for i, n in enumerate(READ_ORDER)}
    out = [IDX_START, "", "## Documentation Index", ""]
    for g in order:
        rows = sorted(by[g], key=lambda x: (rank.get(x[1], 999), x[0]))
        out += [f"### {g}", "", "| Document | Purpose | Status |", "|---|---|---|"]
        for rel, _s, title, purpose, status, _g in rows:
            out.append(f"| [{title}]({rel}) | {purpose} | {status} |")
        out.append("")
    present = {stem for rel, stem, *_ in items if rel.startswith("docs/")}
    out += ["## Consolidation Map", "", "| Subject | Documented in |", "|---|---|"]
    any_row = False
    for d in CATALOG:
        if d["merged_into"] and d["name"] not in present and d["merged_into"] in present:
            out.append(f"| {d['name']} | {d['merged_into']}.md |")
            any_row = True
    if not any_row:
        out.append("| — | — |")
    out += ["", IDX_END]
    return "\n".join(out)


def readme_text(root, project, today):
    out = header(project, "Documentation", "Entry point and index for the project documentation set.", "Draft", today)
    for h, hint in [
        ("Project Overview", "What the project is, in two sentences. Source: owner."),
        ("Purpose and Scope", "What the documentation covers and what it deliberately does not."),
        ("Documentation Status", "Which documents are Draft, Proposed, or Confirmed. See the index below."),
        ("Recommended Reading Order", "AGENTS.md, BRIEF.md, project-intake, instructions, PRD, decisions, current state, then conditional documents."),
    ]:
        out += [f"## {h}", "", "**Status: Open**", "", f"> {hint}", ""]
    out += [index_block(root), ""]
    for h, hint in [
        ("Relationships Between Key Documents", "Example: prd.md requirements map to testing.md criteria; decisions.md governs technology.md."),
        ("Current Project Stage", "Mirror current-state.md; do not duplicate."),
        ("Open Questions", "Link to the authoritative list in prd.md, decisions.md, or memory/open-questions.md."),
        ("Critical Blockers", "Link to current-state.md."),
        ("Next Recommended Actions", "Ordered and concrete."),
    ]:
        out += [f"## {h}", "", "**Status: Open**", "", f"> {hint}", ""]
    return "\n".join(out)


def refresh_readme(root, today):
    p = root / "README.md"
    if not p.exists():
        sys.exit("README.md not found. Run init first.")
    text = p.read_text(encoding="utf-8")
    if IDX_START not in text or IDX_END not in text:
        sys.exit("README.md has no INDEX markers; cannot refresh safely.")
    pre, rest = text.split(IDX_START, 1)
    _, post = rest.split(IDX_END, 1)
    pre = re.sub(r"Last updated: \d{4}-\d{2}-\d{2}", f"Last updated: {today}", pre, count=1)
    p.write_text(pre + index_block(root) + post, encoding="utf-8")


def finish_readme(root, name, today, created):
    """README is always written or refreshed last."""
    if write_if_absent(root / "README.md", readme_text(root, name, today)):
        created.append("README.md")
    else:
        refresh_readme(root, today)


# ---------------------------------------------------------------- agent kit and memory
def copy_if_absent(src, dst):
    if not src.exists():
        return 0
    if src.is_file():
        if dst.exists():
            return 0
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return 1
    n = 0
    for f in sorted(src.rglob("*")):
        if not f.is_file() or "__pycache__" in f.parts:
            continue
        target = dst / f.relative_to(src)
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
        n += 1
    return n


def memory_files(name, today):
    readme = header(name, "Agent Memory", "Shared working memory any agent reads at session start and updates at session end.", "Draft", today) + [
        "## Files", "", "| File | Purpose | Edit rule |", "|---|---|---|",
        "| state.json | Structured status: phase, last verified commit, check results | Overwrite each session |",
        "| progress-log.md | Dated entries, one per session or iteration | Append only |",
        "| lessons.md | Learnings promoted from repeated findings | Add when a finding repeats |",
        "| open-questions.md | Questions awaiting the owner | Add and close; keep closed ones |", "",
        "## Protocol", "",
        "1. **Session start.** Read state.json, the last 20 lines of progress-log.md, lessons.md, open-questions.md, then docs/core/current-state.md and decisions.md. Compare with `git status`, `git log -5`, and the verification command. Reality wins over memory.",
        "2. **During work.** Log each finished task or costly discovery when it happens, not at the end.",
        "3. **Session end.** Append a log entry, update state.json, promote repeated findings to lessons.md, and update docs/core/current-state.md.", "",
        "## Rules", "",
        "- No secrets, tokens, passwords, private keys, personal records, or production data.",
        "- Tag entries: stated by owner, verified, or inferred. Treat inferred entries as Open.",
        "- Authority order: owner statement, Accepted decisions, AGENTS.md, other docs, this folder, tool native memory, model recall. When two disagree, fix the lower one and log the correction.",
        "- Full guidance: playbooks/context-and-memory.md.", "",
    ]
    log = header(name, "Progress Log", "Append-only record of sessions and iterations, newest last.", "Draft", today) + [
        f"### {today} | scaffold",
        "- Mode: DOCUMENT | Tier: T1",
        "- Changed: generated docs, memory, and agent adapter files with scaffold.py",
        "- Verified: not yet run. Run `python scaffold.py validate`.",
        "- Next: fill docs/core/project-intake.md",
        "- State: CONTINUE", "",
    ]
    lessons = header(name, "Lessons", "Learnings that should change future agent behavior on this project.", "Draft", today) + [
        "No lessons yet. Add one when a finding repeats or costs real time, in this form:", "",
        "```",
        f"- {today} [verified] <what to do or avoid>. Source: <file, command, or session>.",
        "```", "",
        "Keep this file under about 60 lines. Merge duplicates and prune anything the code or docs now enforce.", "",
    ]
    questions = header(name, "Open Questions", "Questions awaiting the owner, with impact.", "Open", today) + [
        "| ID | Question | Impact | Blocks work | Status |", "|---|---|---|---|---|",
        "| Q-001 | What is the project's purpose, and who are its primary users? Record the answer in docs/core/project-intake.md. | Shapes every decision | Yes | Open |", "",
    ]
    state = {"project": name, "created": today, "phase": "intake", "mode": "DOCUMENT",
             "last_verified_commit": None, "checks": {}, "open_task_ids": [],
             "notes": "Overwrite each session. Never store secrets or personal data."}
    return {
        "README.md": "\n".join(readme),
        "progress-log.md": "\n".join(log),
        "lessons.md": "\n".join(lessons),
        "open-questions.md": "\n".join(questions),
        "state.json": json.dumps(state, indent=2) + "\n",
    }


def generate(a, root, name, today):
    created = []
    selected, reasons = resolve(a)
    for d in selected:
        if write_if_absent(root / doc_path(d), render_doc(d, name, today)):
            created.append(str(doc_path(d)))
    if write_if_absent(root / "docs/core/selection-log.md", selection_log(name, reasons, today)):
        created.append("docs/core/selection-log.md")
    for item in AGENT_KIT:
        n = copy_if_absent(KIT / item, root / item)
        if n:
            created.append(item if n == 1 and (KIT / item).is_file() else f"{item}/ ({n} files)")
    for fname, text in memory_files(name, today).items():
        if write_if_absent(root / "memory" / fname, text):
            created.append(f"memory/{fname}")
    return created


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60].strip("-")
    if not s:
        sys.exit("Project name must contain letters or digits.")
    return s


def project_files(name, today):
    owner_hint = "> Owner: fill what you know. Blank is fine; the research prompt covers the rest."
    brief = header(name, "Owner Brief", "Owner-written starting facts; the research prompt reads this first.", "Open", today)
    for h in ("What I want built", "Audience", "Goals and success", "Links and existing assets",
              "Constraints (budget, deadline, stack, legal)", "Brand and taste (likes, dislikes, examples)",
              "Must not do", "Agent I will use (Claude Code, OpenCode, Hermes, other)"):
        brief += [f"## {h}", "", "**Status: Open**", "", owner_hint, ""]
    build = header(name, "Build Prompt", "Placeholder until the prompt generator writes the real build prompt.", "Open", today) + [
        "**Status: Open**", "",
        "This file has not been generated yet. To generate it:", "",
        "1. Optional: fill in BRIEF.md with anything you know.",
        "2. Give PROMPT-GENERATOR.md to an agent that has web search and file write access, in this folder.",
        "3. The agent writes research/sources.md, research/dossier.md, and replaces this file.",
        "4. Start a fresh session and give the agent the new BUILD-PROMPT.md to build.", "",
    ]
    sources = header(name, "Research Sources", "Evidence log for the research dossier.", "Open", today) + [
        "The prompt generator fills this file. Every material claim gets an ID, URL, access date, and confidence.", "",
        "| ID | Claim (paraphrased) | Source URL | Source type | Accessed | Confidence | Notes |",
        "|---|---|---|---|---|---|---|",
        "| — | — | — | — | — | — | — |", "",
    ]
    dossier = header(name, "Research Dossier", "Twelve-part research summary that feeds the build prompt.", "Open", today)
    areas = [
        ("Subject", "What is it, who runs it, what is its purpose and stage?"),
        ("Audience", "Who are the primary and secondary visitors, and what do they want and fear?"),
        ("Goals", "What should the site achieve and how is success measured?"),
        ("Landscape", "Who are the closest three to five comparable sites, and what do they do well and badly?"),
        ("Best in class", "Which sites in any field handle a similar job exceptionally, and why?"),
        ("Content", "What exists, what must be written, and which claims need evidence?"),
        ("Search demand", "Which terms, questions, and intents matter?"),
        ("Design signals", "Existing brand assets, tone of the field, conventions to follow or break on purpose."),
        ("Technical", "Stack options, integrations, hosting constraints, data handled."),
        ("Compliance", "Privacy, accessibility, licensing, and regional rules that apply."),
        ("Risks", "Reputational, legal, technical, and delivery risks."),
        ("Gaps", "What could not be established, with the queries tried."),
    ]
    for i, (h, q) in enumerate(areas, 1):
        dossier += [f"## {i}. {h}", "", "**Status: Open**", "", f"> {q}", "", "So what for the build: Open.", ""]
    return {"BRIEF.md": "\n".join(brief), "BUILD-PROMPT.md": "\n".join(build),
            "research/sources.md": "\n".join(sources), "research/dossier.md": "\n".join(dossier)}


def prompt_generator_text(name):
    src = KIT / "prompts" / "00-project-prompt-generator.md"
    if not src.exists():
        return None
    t = src.read_text(encoding="utf-8")
    t = t.replace("# Title: Project Doc Blueprint Project Prompt Generator", f"# Title: {name} Project Prompt Generator", 1)
    t = t.replace("PROJECT NAME HERE", name)
    t = t.replace("Replace the three fields in `<project>`. Only the name is required.",
                  "The project name is already filled in. Put any extra details in BRIEF.md.")
    return t


def register_project(base, name, slug, preset, today):
    base.mkdir(parents=True, exist_ok=True)
    reg = base / "README.md"
    if not reg.exists():
        head = header("Project Doc Blueprint", "Projects Registry",
                      "Registry of projects created with scaffold.py new; each row links to a self-contained project folder.",
                      "Draft", today) + [
            "Each project folder holds its own docs, memory, research, playbooks, prompts, and agent adapter files, so an agent started inside it needs nothing from outside.", "",
            "| Project | Folder | Created | Preset | Stage |", "|---|---|---|---|---|"]
        reg.write_text("\n".join(head) + "\n", encoding="utf-8")
    text = reg.read_text(encoding="utf-8")
    if f"({slug}/README.md)" not in text:
        safe = re.sub(r"[\[\]()|]", "", name)
        if not text.endswith("\n"):
            text += "\n"
        text += f"| [{safe}]({slug}/README.md) | `{slug}/` | {today} | {preset} | Intake |\n"
        reg.write_text(text, encoding="utf-8")


def kit_readme_has_markers():
    p = KIT / "README.md"
    return p.exists() and IDX_START in p.read_text(encoding="utf-8")


# ---------------------------------------------------------------- commands
def cmd_list(_a):
    print("TRIGGERS (use with --triggers a,b,c)")
    for k, v in TRIGGERS.items():
        docs = [d["name"] for d in CATALOG if k in doc_trigs(d)]
        print(f"  {k:<13} {v}\n  {'':<13} -> {', '.join(docs)}")
    print("\nPRESETS: " + ", ".join(f"{k} ({len(v)} triggers)" for k, v in PRESETS.items()) + ", all (every doc standalone)")


def cmd_init(a):
    root = pathlib.Path(a.out).resolve()
    today = a.date or datetime.date.today().isoformat()
    created = generate(a, root, a.name, today)
    finish_readme(root, a.name, today, created)
    print(f"Created {len(created)} item(s) in {root}")
    for c in created:
        print("  +", c)
    print("Next: fill docs/core/project-intake.md, then run: python scaffold.py validate")


def cmd_new(a):
    name = " ".join(a.name.split())
    slug = slugify(name)
    base = pathlib.Path(a.projects_dir).resolve() if a.projects_dir else KIT / "projects"
    root = base / slug
    if root.exists() and any(root.iterdir()):
        sys.exit(f"{root} already exists and is not empty. Choose another name, or add to it with: python scaffold.py init --out {root}")
    a.preset = a.preset or "site"
    today = a.date or datetime.date.today().isoformat()
    created = generate(a, root, name, today)
    for rel, text in project_files(name, today).items():
        if write_if_absent(root / rel, text):
            created.append(rel)
    gen = prompt_generator_text(name)
    if gen and write_if_absent(root / "PROMPT-GENERATOR.md", gen):
        created.append("PROMPT-GENERATOR.md")
    finish_readme(root, name, today, created)
    register_project(base, name, slug, a.preset, today)
    try:
        base.relative_to(KIT)
        if kit_readme_has_markers():
            refresh_readme(KIT, today)
    except ValueError:
        pass
    print(f"Project '{name}' created at {root} ({len(created)} items)")
    print("\nNext steps")
    print(f"  1. cd {root}")
    print("  2. Optional: fill in BRIEF.md")
    print("  3. Give PROMPT-GENERATOR.md to your agent (needs web search and file write). It writes research/ and BUILD-PROMPT.md.")
    print("  4. Fresh session: give the agent BUILD-PROMPT.md. AGENTS.md loads automatically in Claude Code, OpenCode, and Hermes.")
    print("  5. Check anytime: python scaffold.py validate")


def cmd_prompt(a):
    name = " ".join(a.name.split())
    text = prompt_generator_text(name)
    if text is None:
        sys.exit("prompts/00-project-prompt-generator.md not found next to scaffold.py.")
    if a.details:
        safe = " ".join(a.details.split()).replace("<", "&lt;").replace(">", "&gt;")
        old = "Anything else you know: audience, goals, links, brand, constraints. Leave blank if none."
        if old not in text:
            sys.exit("Could not find the details placeholder in the generator; edit it by hand.")
        text = text.replace(old, safe, 1)
    if a.out:
        out = pathlib.Path(a.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out} ({len(text)} characters). Give it to an agent that has web search and file write.")
    else:
        sys.stdout.write(text)


def cmd_readme(a):
    refresh_readme(pathlib.Path(a.out).resolve(), a.date or datetime.date.today().isoformat())
    print("README index refreshed.")


def cmd_graph(a):
    root = pathlib.Path(a.out).resolve()
    today = a.date or datetime.date.today().isoformat()
    if not (root / "docs").is_dir():
        sys.exit("No docs/ folder found.")
    skip = {"doc-graph", "selection-log"}
    docs = {p.stem: p for p in sorted((root / "docs").rglob("*.md")) if p.stem not in skip}
    out_e = {s: set() for s in docs}
    for s, p in docs.items():
        for m in re.finditer(r"\b([a-z0-9][a-z0-9-]*)\.md\b", p.read_text(encoding="utf-8")):
            t = m.group(1)
            if t in docs and t != s:
                out_e[s].add(t)
    in_e = {s: set() for s in docs}
    for s, ts in out_e.items():
        for t in ts:
            in_e[t].add(s)
    name = "Project"
    rp = root / "README.md"
    if rp.exists():
        m = re.match(r"# Title: (.+) Documentation$", rp.read_text(encoding="utf-8").splitlines()[0])
        if m:
            name = m.group(1)
    nid = lambda s: "n_" + s.replace("-", "_")
    lines = header(name, "Document Graph", "Which documents mention which others, generated from file-name mentions.", "Draft", today) + [
        "Generated by `python scaffold.py graph`. A mention shows coupling, not consistency. selection-log.md and this file are left out.",
        "**Open**: review every orphan and every unexpected link.", "",
        "## Diagram", "", "```mermaid", "flowchart LR"]
    lines += [f"  {nid(s)}[{s}]" for s in docs]
    lines += [f"  {nid(s)} --> {nid(t)}" for s in docs for t in sorted(out_e[s])]
    lines += ["```", "", "## Adjacency", "", "| Document | Mentions | Mentioned by |", "|---|---|---|"]
    for s in docs:
        lines.append(f"| {s} | {', '.join(sorted(out_e[s])) or '—'} | {', '.join(sorted(in_e[s])) or '—'} |")
    orphans = [s for s in docs if not in_e[s]]
    lines += ["", "## Orphans", "", "Documents no other document mentions."]
    lines += [""] + ([f"- {s}" for s in orphans] if orphans else ["None."]) + [""]
    target = root / "docs" / "ai" / "doc-graph.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    if rp.exists() and IDX_START in rp.read_text(encoding="utf-8"):
        refresh_readme(root, today)
    print(f"Wrote {target.relative_to(root)}: {len(docs)} documents, {sum(len(v) for v in out_e.values())} links, {len(orphans)} orphan(s).")


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")
HARD_SECRETS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\b(?:sk|pk)-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bghp_[A-Za-z0-9]{30,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
]
SOFT_SECRET = re.compile(
    r"(?i)\b(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*['\"]?"
    r"(?!YOUR_|<|\{\{|\.\.\.|\*{3}|placeholder|example|changeme)[^\s'\"|]{8,}")


def cmd_validate(a):
    root = pathlib.Path(a.out).resolve()
    errors, warns = [], []
    files = md_files(root)
    rp = root / "README.md"
    if not rp.exists():
        errors.append("README.md missing")
    readme = rp.read_text(encoding="utf-8") if rp.exists() else ""
    for p in files:
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        if not lines or not lines[0].startswith("# Title: "):
            errors.append(f"{rel}: line 1 must start with '# Title: '")
        if len(lines) < 3 or lines[1] != "" or not lines[2].strip() or lines[2].startswith("#"):
            errors.append(f"{rel}: line 3 must be a one-line purpose after a blank line")
        st = next((l for l in lines[:10] if l.startswith("Status:")), None)
        if not st or st.split(":", 1)[1].strip() not in STATUSES:
            errors.append(f"{rel}: header Status must be one of {', '.join(STATUSES)}")
        if not any(re.fullmatch(r"Last updated: \d{4}-\d{2}-\d{2}", l) for l in lines[:10]):
            errors.append(f"{rel}: header needs 'Last updated: YYYY-MM-DD'")
        if st and "Confirmed" in st and "**Status: Open**" in text:
            warns.append(f"{rel}: document marked Confirmed but contains Open sections")
        for m in LINK_RE.finditer(text):
            tgt = m.group(1)
            if re.match(r"^(https?:|mailto:)", tgt):
                continue
            if not (p.parent / tgt).resolve().exists():
                errors.append(f"{rel}: broken link -> {tgt}")
        for rx in HARD_SECRETS:
            if rx.search(text):
                errors.append(f"{rel}: possible real secret matches {rx.pattern[:28]}...")
        if SOFT_SECRET.search(text):
            warns.append(f"{rel}: text looks like a credential assignment; confirm it is a placeholder")
        if rel != "README.md" and f"]({rel})" not in readme:
            errors.append(f"{rel}: not indexed in README.md")
        if rel in ("AGENTS.md", "CLAUDE.md") and len(text) > AGENTS_MAX_CHARS:
            warns.append(f"{rel}: {len(text)} characters; Hermes may truncate startup files above {AGENTS_MAX_CHARS}")
    json_files = [root / "opencode.json", root / ".claude" / "settings.json", root / "memory" / "state.json"]
    if (root / "integrations").is_dir():
        json_files += sorted((root / "integrations").glob("*.json"))
    for jp in json_files:
        if jp.exists():
            try:
                json.loads(jp.read_text(encoding="utf-8"))
            except ValueError as e:
                errors.append(f"{jp.relative_to(root).as_posix()}: invalid JSON ({e})")
    cm, am = root / "CLAUDE.md", root / "AGENTS.md"
    if cm.exists() and am.exists() and "@AGENTS.md" not in cm.read_text(encoding="utf-8"):
        warns.append("CLAUDE.md does not import AGENTS.md; Claude Code ignores AGENTS.md when CLAUDE.md exists")
    if rp.exists():
        newer = [p.relative_to(root).as_posix() for p in files
                 if p != rp and p.stat().st_mtime > rp.stat().st_mtime + 1]
        if newer:
            warns.append(f"README.md older than {len(newer)} file(s); run 'readme' to refresh (README is updated last)")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"\n{len(files)} markdown file(s) checked: {len(errors)} error(s), {len(warns)} warning(s).")
    print("Not checked by this tool: factual accuracy, diagram correctness, design-reference review, whether Confirmed claims have real evidence.")
    sys.exit(1 if errors else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    presets = list(PRESETS) + ["all"]

    i = sub.add_parser("init", help="add docs, memory, and agent files to an existing folder")
    i.add_argument("--name", default="Project Name")
    i.add_argument("--out", default=".")
    i.add_argument("--preset", choices=presets)
    i.add_argument("--triggers", help="comma-separated trigger flags")
    i.add_argument("--also", help="comma-separated consolidated docs to generate standalone")
    i.add_argument("--date")
    i.set_defaults(fn=cmd_init)

    n = sub.add_parser("new", help="create a complete project folder under projects/")
    n.add_argument("name", help="project name, in quotes if it has spaces")
    n.add_argument("--projects-dir", help="where projects live (default: projects/ next to this script)")
    n.add_argument("--preset", choices=presets, help="default: site")
    n.add_argument("--triggers")
    n.add_argument("--also")
    n.add_argument("--date")
    n.set_defaults(fn=cmd_new)

    pr = sub.add_parser("prompt", help="print or save the attachable project-prompt generator for a name")
    pr.add_argument("name", help="project name, in quotes if it has spaces")
    pr.add_argument("--details", help="optional extra facts: audience, goals, links, brand, constraints")
    pr.add_argument("--out", help="write to this file instead of printing")
    pr.set_defaults(fn=cmd_prompt)

    for nm, fn in (("readme", cmd_readme), ("validate", cmd_validate), ("graph", cmd_graph)):
        s = sub.add_parser(nm)
        s.add_argument("--out", default=".")
        s.add_argument("--date")
        s.set_defaults(fn=fn)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
