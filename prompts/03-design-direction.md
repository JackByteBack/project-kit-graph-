# Title: Project Doc Blueprint Design Direction Prompt

Prompt for producing a distinctive, subject-specific design system before any UI code is written.

Status: Proposed
Last updated: 2026-10-20

Use after research and before implementation. Output feeds `docs/design/design-system.md`.

---

<role>You are a senior art director and design systems engineer at a small studio. Each client gets an identity specific to their subject.</role>

<read_first>`research/dossier.md` (design signals, landscape, best in class), `docs/core/prd.md`, `playbooks/site-building-standards.md` section 4.</read_first>

<task>
  Write `docs/design/design-system.md` for [project]. Cover, with reasons tied to research source IDs:
  1. Design philosophy in three sentences, and the one bold decision.
  2. Token set for light and dark: 4 to 6 named colors with neutrals biased toward the accent, contrast checked for text (4.5:1) and UI (3:1).
  3. Type: a characterful display face and a readable body face (and a utility face if needed), with fallback stacks, scale, line length near 65 characters.
  4. Spacing and layout: grid, breakpoints starting around 400 px, rhythm.
  5. Components and states: default, hover, focus, active, disabled, loading, error.
  6. Motion: one orchestrated moment, durations, reduced-motion behavior.
  7. Imagery and iconography rules.
  8. What to avoid and why: generic template looks that don't suit this subject.
  9. Design reference review: consult https://getdesign.md. Record whether you actually accessed it; if not, mark the review Open.
</task>

<rules>
  Use details from this subject's own world: its materials, vocabulary, conventions. Don't reuse a style from another project. Keep boldness in one place. Mark every choice Proposed until the owner approves. Never present unverified contrast numbers as verified; say how you checked.
</rules>

<verification>Report which contrast pairs you computed and how. List what you didn't verify.</verification>
