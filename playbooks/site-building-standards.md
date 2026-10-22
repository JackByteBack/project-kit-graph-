# Title: Project Doc Blueprint Site Building Standards

Quality bars and craft rules for building an excellent, fast, accessible, findable website.

Status: Proposed
Last updated: 2026-10-20

All budgets and thresholds are **Proposed** defaults based on widely published web performance and accessibility guidance. They were not re-verified in this session; confirm against current standards when you adopt them in a project's `docs/web/performance.md`. Design advice follows the Anthropic prompting guide read 2026-10-20 for the points marked **Confirmed**.

## 1. Strategy before pixels

Answer in writing, in `docs/web/site-brief.md`, before any design or code:

1. **The job:** the single thing the site must get a visitor to do or understand.
2. **The visitor:** who, in what state of mind, on what device.
3. **The proof:** what makes the claim believable.
4. **The one bold idea:** one distinctive decision in type, color, layout, or interaction. Everything else stays quiet.
5. **Measures:** how you will know it worked.

## 2. Information architecture

- One job per page. Every page has one primary action.
- Name navigation by what visitors recognize, not by internal structure.
- Keep depth shallow: most content within two clicks of the home page.
- Plan 404, empty, loading, and error states as real pages.
- Write the sitemap in `docs/web/information-architecture.md` and keep URLs short, lowercase, and stable.

## 3. Content

- Write real copy or mark placeholders clearly. Never ship lorem ipsum.
- Lead with the visitor's need; put proof next to claims.
- Active voice, plain words, short sentences. A control says exactly what it does.
- Every image has a purpose and alt text that conveys it (empty alt for decoration).
- Keep a content owner and review date for every page that states facts.

## 4. Design system

- Define a token set first: 4 to 6 named colors, type roles, spacing scale, radii, shadows, motion durations.
- **Both themes:** light and dark defined as tokens, with contrast checked in each.
- **Type:** pair a characterful display face with a readable body face; keep body lines near 65 characters; use a fixed type scale. **Confirmed** advice: avoid default faces such as Inter, Roboto, Arial when you want a distinctive result.
- **Color:** a deliberate neutral set biased toward the accent; accent used sparingly. **Confirmed**: use cohesive themes through CSS variables.
- **Motion:** one orchestrated moment beats scattered effects. **Confirmed**: a single staggered load sequence is a high-impact choice. Respect `prefers-reduced-motion`.
- **Components:** consistent states (default, hover, focus, active, disabled, loading, error).
- Record choices and the getdesign.md review status in `docs/design/design-system.md`.

Avoid the template look: purple-to-blue gradient heroes, everything centered, the same rounded card for every block, emoji as section markers.

## 5. Accessibility (target WCAG 2.2 AA, Proposed)

| Area | Requirement |
|---|---|
| Contrast | Text 4.5:1; large text and UI components 3:1 |
| Keyboard | Everything operable; visible focus; logical order; no traps |
| Structure | One `h1`; headings in order; landmarks; skip link |
| Names | Every control has an accessible name; form fields have labels |
| Motion | Honor reduced motion; no flashing content |
| Targets | Pointer targets at least 24 by 24 CSS px |
| Media | Captions or transcripts; alt text |
| Zoom | Usable at 200 percent and with reflow at 320 CSS px |

Automated tools catch only some failures. Add a keyboard pass and, for important flows, a screen reader pass.

## 6. Performance budgets (Proposed)

| Metric | Target | Notes |
|---|---|---|
| Largest Contentful Paint | 2.5 s or less, mobile, p75 | The usual published "good" threshold |
| Interaction to Next Paint | 200 ms or less | Same |
| Cumulative Layout Shift | 0.1 or less | Reserve space for media and fonts |
| Total JavaScript on a content page | As small as the job allows; justify anything over about 100 KB compressed | Prefer static rendering for content sites |
| Images | Modern formats, responsive `srcset`, explicit dimensions, lazy-load below the fold | Hero image preloaded if it is the LCP element |
| Fonts | Few families and weights, `font-display: swap`, subset where possible | Fallback stacks required |

Measure with a lab tool and, after launch, real-user data. Record the environment with every number.

## 7. SEO

- Unique `title` (about 50 to 60 characters) and `meta description` per page.
- Canonical URLs, `sitemap.xml`, and `robots.txt`.
- Open Graph and social card metadata with a real image.
- Structured data where it matches real content (organization, article, event, FAQ).
- Semantic HTML, descriptive link text, and internal links between related pages.
- Don't write for keywords at the expense of clarity. Map target terms to pages in `docs/web/seo.md` using the research dossier.

## 8. Security and privacy for sites

- HTTPS everywhere; HSTS once stable.
- Security headers considered per project: Content-Security-Policy, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, frame protections.
- Forms: validate on the server, rate limit, avoid exposing addresses to scrapers, protect against spam without harming accessibility.
- Third-party scripts are dependencies and data flows: each needs a decision entry and owner approval (Rule 7).
- Collect the minimum data; state what is collected and why; honor regional consent rules. Record in `docs/web/analytics-privacy.md`.
- No secrets in client code or in the repository.

## 9. Responsive and resilient

- Design at about 400 px first, then widen; no horizontal page scroll at any width.
- Fluid type and spacing; wrap or stack rows; give flex and grid children room to shrink.
- Works without JavaScript for core content where feasible.
- Handles slow networks, missing images, and failed requests gracefully.

## 10. Engineering practices

- Choose the stack in `docs/architecture/technology.md` as a decision. Content-led sites usually favor static rendering. **Open** per project.
- Keep dependencies few and pinned.
- Automate build, lint, link check, and audits in CI when one exists.
- Component and file naming follow `docs/engineering/code-style.md`.
- Keep a changelog in `memory/progress-log.md`.

## 11. Launch checklist

Tick only after verifying each item. Copy into `docs/web/launch-checklist.md`.

- [ ] Content proofread; no placeholders
- [ ] All pages have unique titles and descriptions
- [ ] Sitemap and robots live; canonical URLs correct
- [ ] Accessibility scan and keyboard pass done
- [ ] Performance budgets met on mobile
- [ ] Both themes checked
- [ ] 404 and error pages designed
- [ ] Forms tested end to end, including failure paths
- [ ] Analytics and consent behavior reviewed
- [ ] Security headers set; dependencies audited
- [ ] Redirects from old URLs in place (if any)
- [ ] Backups and rollback understood
- [ ] Owner approval recorded for production release (T4)

## 12. After launch

Monitor uptime, errors, and real-user performance; review search queries monthly; fix in small releases; log lessons in `memory/lessons.md`.
