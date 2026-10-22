# Title: Project Doc Blueprint Evals and Verification Playbook

How to test prompts, loops, and finished sites so "done" means verified.

Status: Proposed
Last updated: 2026-10-20

Method guidance only. Thresholds are proposals until you adopt them in a project's `testing.md`.

## 1. Principle

Report what ran, not what should work. Every claim of completion cites a command, a result, or a reviewed artifact. Anything unrun is listed as not verified.

## 2. Three things to evaluate

| Subject | Question | Evidence |
|---|---|---|
| Prompt | Does it produce the right output across varied inputs? | Eval set results |
| Loop or graph | Does it finish, stay in scope, and stop safely? | Run logs, caps respected |
| Product | Does the site meet its quality bars? | Build, audits, screenshots, review |

## 3. Prompt evals

1. **Build a small eval set** of 5 to 10 inputs: typical, edge, empty, adversarial, and one that tempts the model to invent facts.
2. **Write a rubric** before running. Score each criterion 0, 1, or 2.
3. **Run the prompt** on each input, ideally twice to see variance.
4. **Record** results in `docs/ai/prompt-registry.md`.
5. **Change one thing**, rerun, compare. Keep the old version.

Example rubric for a project-prompt generator:

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Research grounded | Claims without sources | Some sources | Every material claim has URL and date |
| Unknowns flagged | Gaps filled with guesses | Some gaps flagged | All gaps marked Open |
| Output contract met | Wrong files or format | Partial | Exact files and schema |
| Scope discipline | Invents features | Minor drift | Matches brief |
| Actionability | Vague | Mixed | Agent could start building with no questions |

An LLM can score a rubric, but treat its scores as a screening step, not proof. Spot-check by hand, and don't let the same model grade its own output without a human sample.

## 4. Loop and graph evals

- Did it stop in a defined state (DONE, CAPPED, STUCK, BLOCKED)?
- Were the iteration and time caps respected?
- Did the diff stay inside the per-iteration scope?
- Were tests left untouched?
- Is every log entry's "verified" line backed by a command that was actually run?
- Can a fresh agent resume from `memory/` alone? Test this once by starting a clean session.

## 5. Site verification

Run in this order. Record each result in `docs/engineering/testing.md`.

| # | Check | How | Pass bar (Proposed) |
|---|---|---|---|
| 1 | Build | Project build command | Exit 0, no warnings that matter |
| 2 | Types and lint | Project check command | Zero errors |
| 3 | Links | Link checker over the build output | Zero broken internal links |
| 4 | Accessibility | Automated scan plus keyboard pass | Zero serious or critical issues; focus visible everywhere |
| 5 | Performance | Lighthouse or equivalent on key pages, mobile profile | Meets budgets in `site-building-standards.md` |
| 6 | SEO | Metadata, sitemap, robots, structured data review | Every page has a unique title and description |
| 7 | Responsive | Screenshots at about 400, 768, 1280 px | No horizontal scroll, no clipped text |
| 8 | Themes | Screenshots in light and dark | Contrast holds in both |
| 9 | Content | Read every page aloud once | No placeholder text left unmarked |
| 10 | Security | Headers, forms, dependencies audit | No known high severity issue |

Automated scans catch only part of accessibility problems. Say so in the report.

## 6. Verification report template

```markdown
## Verification report, 2026-10-20
| Check | Ran | Result | Evidence |
|---|---|---|---|
| Build | Yes | PASS | `npm run build` exit 0 |
| Accessibility scan | Yes | 2 moderate issues | report path |
| Keyboard pass | No | Not verified | |
| Lighthouse mobile | Yes | Perf 91, A11y 100 | report path |

Not verified: dark theme on /contact, screen reader pass.
```

## 7. Regression discipline

- Every bug fixed gets a test, or a note in `lessons.md` explaining why it can't.
- Never weaken a check to pass it. If a check is wrong, record a decision that changes it and say why.
- Keep eval sets under version control next to the prompts they test.

## 8. Known limits

- Eval sets this small show failures, not reliability.
- Model graders drift and prefer their own style.
- Performance numbers vary by machine and network; record the environment.
