# Settings Hide Runtime Config Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hide all runtime service configuration from the end-user settings screen while keeping the requested OpenAI LLM and embedding values in local `.env`.

**Architecture:** The implementation stays frontend-first. `page.tsx` becomes a preferences-only screen, a focused source test locks the privacy shell, and the backend runtime continues to read configuration from ignored `.env` keys already supported by `EnvStore`.

**Tech Stack:** Next.js App Router, React, TypeScript, Node test runner, local `.env`

---

### Task 1: Lock the privacy shell in a focused test

**Files:**
- Create: `web/tests/settings-page-runtime-privacy.test.ts`
- Modify later: `web/app/(utility)/settings/page.tsx`

- [ ] Add a source-structure test that fails while `LLM`, `EMBEDDING`, `SEARCH`, `Save Draft`, `Apply`, `Run test`, and `Run Terminal Tour` are still present in the settings shell source.
- [ ] Run `cd web && node --test tests/settings-page-runtime-privacy.test.ts` and confirm it fails first.

### Task 2: Reduce `/settings` to safe end-user preferences

**Files:**
- Modify: `web/app/(utility)/settings/page.tsx`
- Test: `web/tests/settings-page-runtime-privacy.test.ts`

- [ ] Remove the runtime status row, service configuration tabs, runtime editor forms, diagnostics controls, and tour relaunch action from the render output.
- [ ] Keep the page title plus theme/language controls intact.
- [ ] Re-run `cd web && node --test tests/settings-page-runtime-privacy.test.ts` and confirm it passes.

### Task 3: Persist runtime config only in local `.env`

**Files:**
- Modify local-only: `.env`
- Reference only: `deeptutor/services/config/env_store.py`

- [ ] Update the ignored root `.env` with the requested OpenAI LLM and embedding keys using the exact variable names consumed by `EnvStore`.
- [ ] Confirm `.env` remains untracked with `git status --short .env`.

### Task 4: Validate and record the lane

**Files:**
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-04-30.md`
- Modify: `docs/superpowers/pr-notes/2026-04-30-settings-hide-runtime-config.md`

- [ ] Run `cd web && node --test tests/settings-page-runtime-privacy.test.ts`.
- [ ] Run `cd web && npx eslint "app/(utility)/settings/page.tsx"`.
- [ ] Run `cd web && npm run build`.
- [ ] Run `git diff --check -- web/app/"(utility)"/settings/page.tsx web/tests/settings-page-runtime-privacy.test.ts docs/superpowers/tasks/2026-04-30-settings-hide-runtime-config.md docs/superpowers/specs/2026-04-30-settings-hide-runtime-config-design.md docs/superpowers/plans/2026-04-30-settings-hide-runtime-config.md docs/superpowers/pr-notes/2026-04-30-settings-hide-runtime-config.md ai_first/daily/2026-04-30.md ai_first/ACTIVE_ASSIGNMENTS.md`.
- [ ] Record that `.env` was updated locally but intentionally left untracked.
