# Changelog

All notable changes to hmbirmingham.me are documented here.
Format: **Phase · What · Why**.

---

## 2026-11-07

### Phase 4 · Accessibility pass (`fix(a11y)`)

**What changed**
- Added `aria-hidden="true"` to every decorative SVG in the page (nav icons,
  project card icons, all button/link icons, contact card icons).
- Added `rel="noopener"` to every `target="_blank"` anchor that was missing it.

**Why**
Screen readers announced decorative icon SVGs as unlabeled images, polluting
navigation for keyboard users. `noopener` prevents the opened tab from accessing
`window.opener` (security) and allows the browser to free resources sooner (perf).

---

### Phase 3 · Structured project modals + accuracy fix (`feat(p1)`)

**What changed**
- Replaced the single-block "Overview" modal with a four-part structure:
  **Problem / Approach / Results / Status + Next**.
- Added a stat-chip row to each project modal:
  - Colony Counter: pooled F1 · precision · count error
  - STM32: flash image size · HAL calls · target chip
- Fixed STM32 card description: removed the false claim that USART2 transmit
  is working. Correct state: GPIO (blinky) is logic-analyzer verified; USART2
  has a known baud-rate bug being debugged. Roadmap unchanged.
- Tightened hero description to one punchy line + support sentence + status
  line (UConn BME+CS · Class of 2029 · targeting embedded/firmware roles).

**Why**
Hiring managers discard modals that are dense text walls. The structured format
lets a reviewer scan in ~10 seconds: metrics say what it did, Problem says why,
Approach says how, Results say how well it worked, Next signals maturity.
The accuracy fix removes a claim that a recruiter could disprove by running the
repo.

---

### Phase 2 · P0: resume section, hero CTA, motion/JS fallbacks (`feat(p0)`)

**What changed**
- Added a full `#resume` section with an embedded PDF viewer, a Download PDF
  button, and an Open in new tab link. Section sits between Skills and Contact.
- Added a "Résumé" nav link in the sidebar (between Skills and Contact).
- Added a "Download Résumé" ghost CTA alongside the hero "View My Projects"
  button so a recruiter can reach the PDF from the first screen.
- Added `@media (prefers-reduced-motion: reduce)` rule: `.fade-up` elements are
  immediately visible with no animation for users who request it.
- Added `<noscript>` style block so `.fade-up` content is never invisible when
  JavaScript is blocked or fails.
- Added `aria-hidden="true"` to decorative SVGs touched in this pass.

**Why**
The resume PDF was in the repo but unreachable from the site. Any recruiter
doing a 20-second scan needs one click to get to the resume. The motion/JS
fallbacks prevent a situation where the entire page is blank (all content was
at `opacity: 0` with no non-JS fallback).

---

### Phase 1 · Repo hygiene (`chore`)

**What changed**
- Added `assets/resume/HynesB_Resume(10.26).pdf` to git tracking (it was
  untracked despite being a site deliverable).
- Added `assets/resume/Resume/` to `.gitignore` (docx source files, not for
  public repo).
- Added `.claude/` to `.gitignore` (tool config dir, not site content).

**Why**
Clean repo: only site-deliverable files tracked, no editor or tool config
directories, no binary source formats that don't belong in a public repo.

---

## Earlier

See git log for changes prior to 2026-11-07.
