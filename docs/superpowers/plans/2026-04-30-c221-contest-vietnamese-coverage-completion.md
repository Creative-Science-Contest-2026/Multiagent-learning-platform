# C221 Contest Vietnamese Coverage Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the remaining English leakage from the contest-path teacher workflow so the main demo reads fully Vietnamese across the cockpit, `/agents`, Knowledge, Marketplace, and Dashboard.

**Architecture:** Keep the sweep bounded to teacher-facing display copy. Move remaining hard-coded English labels or seed content into locale-backed display strings where appropriate, preserve technical filenames and attribution surfaces, and add one focused regression test for the new contest-path Vietnamese coverage.

**Tech Stack:** Next.js App Router, React, i18next locale JSON files, Node test runner, ESLint

---

### Task 1: Localize contest cockpit action content

**Files:**
- Modify: `web/components/contest/teacher-cockpit-content.ts`
- Modify only if needed: `web/components/contest/TeacherCockpit.tsx`
- Modify: `web/locales/en/app.json`
- Modify: `web/locales/vi/app.json`

- [ ] Replace remaining cockpit hard-coded English labels/descriptions with locale-backed keys or stable translatable strings.
- [ ] Ensure Vietnamese locale has exact keys for every contest action and helper string used on `/`.
- [ ] Preserve route targets and any non-display identifiers unchanged.

### Task 2: Localize `/agents` authoring flow

**Files:**
- Modify: `web/components/agents/SpecPackAuthoringTab.tsx`
- Modify: `web/app/(workspace)/agents/page.tsx`
- Modify: `web/locales/en/app.json`
- Modify: `web/locales/vi/app.json`

- [ ] Replace English fallback summaries and empty states that still leak in Vietnamese mode.
- [ ] Convert teacher-facing seeded markdown guidance to localized display content without renaming technical filenames like `IDENTITY.md` or `SOUL.md`.
- [ ] Keep exported/runtime contract fields stable while improving the teacher-facing authoring copy.

### Task 3: Spot-fix remaining contest-path copy and verify

**Files:**
- Modify only if needed: `web/app/(workspace)/dashboard/page.tsx`
- Modify only if needed: `web/app/(utility)/knowledge/page.tsx`
- Modify only if needed: `web/app/(utility)/marketplace/page.tsx`
- Add or modify: a focused contest-path localization regression test if needed
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-30.md`
- Modify: `docs/superpowers/pr-notes/2026-04-30-c221-contest-vietnamese-coverage-completion.md`

- [ ] Sweep the remaining contest-path pages for obvious English teacher-facing copy.
- [ ] Run `python3 -m json.tool` for the registry and both locale files.
- [ ] Run targeted eslint plus `cd web && npm run build`.
- [ ] Record any intentional non-translated identifiers that remain because they are technical or attribution-bearing.
