# Task Packet: Frontend Auth Cookie Hardening

- Task ID: `T054_FRONTEND_AUTH_COOKIE_HARDENING`
- Commit tag: `T054-AUTH-COOKIE`
- Date: 2026-05-06
- Branch: `fix/frontend-auth-cookie-hardening`
- Status: implemented, pending review

## Objective

Fix the post-auth `401` regressions on teacher-first frontend surfaces by ensuring protected API requests consistently include the `HttpOnly` session cookie and by preventing silent auth-failure masking.

## User-Approved Scope

- treat this as a systemic frontend hardening pass, not a one-off Knowledge patch
- over-engineer enough to prevent repeat regressions
- check adjacent protected surfaces for the same bug pattern
- add regression tests so legacy raw fetches do not quietly return

## Owned Files

- `web/lib/api.ts`
- `web/lib/knowledge-api.ts`
- `web/lib/dashboard-api.ts`
- `web/lib/marketplace-api.ts`
- `web/lib/notebook-api.ts`
- `web/lib/agent-spec-api.ts`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/memory/page.tsx`
- `web/app/(utility)/settings/page.tsx`
- `web/app/(workspace)/guide/hooks/useGuideHistory.ts`
- `web/app/(workspace)/guide/hooks/useGuideSession.ts`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/co-writer/page.tsx`
- `web/app/(workspace)/playground/page.tsx`
- `web/components/notebook/SaveToNotebookModal.tsx`
- `web/components/sidebar/TutorBotRecent.tsx`
- `web/tests/**`
- `docs/superpowers/specs/2026-05-06-frontend-auth-cookie-hardening-design.md`
- `docs/superpowers/plans/2026-05-06-frontend-auth-cookie-hardening.md`
- `docs/superpowers/tasks/2026-05-06-frontend-auth-cookie-hardening.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-06.md`

## Do-Not-Touch

- backend auth/session implementation under `deeptutor/**`
- public auth semantics unless needed for test reuse only
- unrelated UI polish or page redesign
- lockfiles unless a strict dependency change becomes necessary

## Design Before Implementation

- Approved design:
  - `docs/superpowers/specs/2026-05-06-frontend-auth-cookie-hardening-design.md`
- Root cause:
  - backend now trusts only the `deeptutor_session` cookie, but multiple protected frontend fetches still omit `credentials: "include"`
- Chosen approach:
  - introduce a shared protected API fetch helper, migrate the known protected surfaces, and add regression guards

## Required Code Reading

- `web/lib/api.ts`
- `web/lib/knowledge-api.ts`
- `web/lib/dashboard-api.ts`
- `web/lib/marketplace-api.ts`
- `web/lib/notebook-api.ts`
- `web/lib/agent-spec-api.ts`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/memory/page.tsx`
- `web/app/(utility)/settings/page.tsx`
- `web/app/(workspace)/guide/hooks/useGuideHistory.ts`
- `web/app/(workspace)/guide/hooks/useGuideSession.ts`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/co-writer/page.tsx`
- `web/app/(workspace)/playground/page.tsx`
- `web/components/notebook/SaveToNotebookModal.tsx`
- `web/components/sidebar/TutorBotRecent.tsx`

## Impact Surface And Stop Conditions

- likely changes:
  - protected frontend fetch helpers and direct page fetches
  - focused regression tests
  - lane docs/daily log
- stop when:
  - the known protected surfaces consistently use the shared cookie-auth fetch path
  - offline fallback no longer swallows `401` in Knowledge helpers
  - focused tests pass
  - `cd web && npm run build` passes
  - `git diff --check` is clean

## Required Tests

- focused Vitest commands for the new helper and protected API modules
- `cd web && npm run build`
- `git diff --check`
