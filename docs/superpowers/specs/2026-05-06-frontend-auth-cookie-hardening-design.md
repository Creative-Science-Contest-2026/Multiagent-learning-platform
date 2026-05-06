# Frontend Auth Cookie Hardening Design

- Date: 2026-05-06
- Task ID: `T054_FRONTEND_AUTH_COOKIE_HARDENING`
- Target branch: `fix/frontend-auth-cookie-hardening`

## Goal

Eliminate `401 Unauthorized` regressions on authenticated teacher-first frontend surfaces after the move to `HttpOnly` auth sessions by ensuring protected API calls always include the session cookie and by preventing silent fallback paths from masking auth failures.

## Current Behavior

- Backend protected routers now resolve the signed-in user exclusively from the `deeptutor_session` cookie in `deeptutor/services/auth/deps.py`.
- Many newer frontend auth/session flows already send `credentials: "include"`.
- Several older frontend surfaces still call `fetch(apiUrl(...))` directly without credentials, including:
  - Knowledge creation/config/list
  - Dashboard data helpers
  - Marketplace data/import helpers
  - Notebook list/detail/save flows
  - Memory and settings pages
  - Legacy guide and tutorbot/agents reads and mutations
- `web/lib/knowledge-api.ts` also catches broadly and falls back to offline cached packs, which can hide a real `401` as if the API merely failed transiently.

## User-Visible Failure

- A signed-in teacher can appear authenticated in the shell, but protected requests like creating or uploading a knowledge pack return `401`.
- Similar failures are likely on other legacy teacher-first screens that still use raw fetches without cookie forwarding.

## Approaches Considered

### Approach A: Patch only the Knowledge page

- Pros:
  - fastest path for the reported upload bug
- Cons:
  - leaves the same defect pattern in multiple nearby surfaces
  - guarantees repeat regressions as soon as users touch other protected pages

### Approach B: Protected frontend cookie-auth hardening pass `recommended`

- Add a shared authenticated fetch helper for internal protected API calls.
- Migrate teacher-first helper modules and direct page fetches to that helper.
- Add regression tests that guard both behavior and source-level usage on the protected surfaces.
- Tighten offline fallback so `401` is not swallowed.

### Approach C: Rework auth transport to bearer tokens in frontend memory

- Cons:
  - contradicts the new backend-auth-first `HttpOnly` session design
  - expands scope into an auth architecture rollback instead of a hardening pass

## Chosen Approach

Approach B.

The defect is systemic: legacy frontend code paths were written before cookie-backed auth became authoritative. The fix should centralize protected fetch behavior rather than sprinkling one-off `credentials` patches without guardrails.

## Design

### 1. Shared protected fetch helper

- Extend `web/lib/api.ts` with a helper for internal protected API calls.
- The helper should:
  - build the full URL from `apiUrl`
  - default `credentials` to `"include"`
  - preserve caller overrides such as `method`, `headers`, `body`, `cache`, and `signal`
- Public auth endpoints may keep using explicit fetches if desired, but protected surfaces should converge on the helper.

### 2. Protected surfaces to migrate in this pass

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

This pass is intentionally broader than the single reported Knowledge bug because all of these surfaces are protected or teacher-first and can fail the same way.

### 3. Do not mask auth failures as offline fallback

- `web/lib/knowledge-api.ts` should only fall back to offline imported packs for genuine transport/network failures.
- `401` and other valid HTTP responses from the backend should not be swallowed into offline state.

### 4. Regression tests

- Add behavioral tests for the shared protected fetch helper.
- Add targeted tests for helper modules most likely to regress:
  - knowledge API
  - marketplace API
  - agent-spec or notebook API
- Add a source invariant test that the known protected frontend files no longer use raw `fetch(apiUrl(...))` directly for their authenticated API calls.

## Expected Impact Surface

### Likely to change

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
- `docs/superpowers/tasks/2026-05-06-frontend-auth-cookie-hardening.md`
- `docs/superpowers/plans/2026-05-06-frontend-auth-cookie-hardening.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-06.md`

### Reviewed but expected to remain unchanged

- backend auth/session services
- auth public forms and redirects
- websocket auth transport

## Tests To Run

- focused Vitest tests for the new helper and migrated protected API helpers
- `cd web && npm run build`
- `git diff --check`

## Non-Goals

- no rollback from `HttpOnly` cookie auth to frontend-stored bearer tokens
- no backend auth model changes
- no product-flow redesign outside the fetch/auth hardening pass
