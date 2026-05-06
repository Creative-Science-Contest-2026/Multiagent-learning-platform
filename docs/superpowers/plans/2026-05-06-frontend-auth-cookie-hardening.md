# Frontend Auth Cookie Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix authenticated frontend `401` regressions by routing protected teacher-first API calls through a shared cookie-aware fetch path and locking the behavior with regression tests.

**Architecture:** Add a shared protected API helper in `web/lib/api.ts`, migrate protected helper modules and direct page fetches to that helper, then add focused behavioral and source-invariant tests. Keep backend auth untouched; this is a frontend transport hardening pass aligned with the existing `HttpOnly` cookie design.

**Tech Stack:** Next.js App Router, browser `fetch`, Vitest, source-invariant tests

---

### Task 1: Add the shared protected API fetch helper

**Files:**
- Modify: `web/lib/api.ts`
- Modify: `web/tests/api-base-url.test.ts`

- [ ] Add an `apiFetch(path, init?)` helper that wraps `fetch(apiUrl(path), ...)` and defaults `credentials` to `"include"`.
- [ ] Keep `apiUrl` and `wsUrl` behavior unchanged.
- [ ] Extend `web/tests/api-base-url.test.ts` to assert the helper builds the right URL, defaults credentials to `"include"`, and preserves explicit overrides.

### Task 2: Migrate protected helper modules to the shared helper

**Files:**
- Modify: `web/lib/knowledge-api.ts`
- Modify: `web/lib/dashboard-api.ts`
- Modify: `web/lib/marketplace-api.ts`
- Modify: `web/lib/notebook-api.ts`
- Modify: `web/lib/agent-spec-api.ts`

- [ ] Replace direct `fetch(apiUrl(...))` calls on protected endpoints with `apiFetch(...)`.
- [ ] In `web/lib/knowledge-api.ts`, narrow the offline fallback so only true network/transport failures fall back; rethrow `401`/HTTP failures.
- [ ] Add focused Vitest coverage for the migrated helper modules.

### Task 3: Migrate protected direct page/component fetches

**Files:**
- Modify: `web/app/(utility)/knowledge/page.tsx`
- Modify: `web/app/(utility)/memory/page.tsx`
- Modify: `web/app/(utility)/settings/page.tsx`
- Modify: `web/app/(workspace)/guide/hooks/useGuideHistory.ts`
- Modify: `web/app/(workspace)/guide/hooks/useGuideSession.ts`
- Modify: `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- Modify: `web/app/(workspace)/agents/page.tsx`
- Modify: `web/app/(workspace)/co-writer/page.tsx`
- Modify: `web/app/(workspace)/playground/page.tsx`
- Modify: `web/components/notebook/SaveToNotebookModal.tsx`
- Modify: `web/components/sidebar/TutorBotRecent.tsx`

- [ ] Replace direct protected `fetch(apiUrl(...))` calls with `apiFetch(...)`.
- [ ] Leave public auth flows and websocket URL construction unchanged.
- [ ] Keep page behavior the same aside from the authenticated transport fix.

### Task 4: Add regression guards against future raw protected fetches

**Files:**
- Create: `web/tests/protected-api-fetches-source.test.ts`

- [ ] Add a source-invariant test that the known protected files in this lane do not use raw `fetch(apiUrl(` for authenticated API paths anymore.
- [ ] Keep the file list explicit so regressions are easy to understand when the test fails.

### Task 5: Verify and update lane docs

**Files:**
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-05-06.md`
- Modify: `docs/superpowers/tasks/2026-05-06-frontend-auth-cookie-hardening.md`

- [ ] Run focused Vitest coverage for the new helper and migration tests.
- [ ] Run `cd web && npm run build`.
- [ ] Run `git diff --check`.
- [ ] Record the auth-cookie hardening pass and verification evidence in the daily log and lane packet.
