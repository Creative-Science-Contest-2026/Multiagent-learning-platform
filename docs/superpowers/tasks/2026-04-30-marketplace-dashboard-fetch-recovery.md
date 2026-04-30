# 2026-04-30 Marketplace Dashboard Fetch Recovery

- Task ID: `UI_MARKETPLACE_DASHBOARD_FETCH_RECOVERY`
- Commit tag: `UI-FETCH-RECOVERY`
- Branch: `fix/marketplace-dashboard-fetch-recovery`
- Worktree: `.worktrees/fix-marketplace-dashboard-fetch-recovery`
- Status: `in_progress`

## Goal

Restore the teacher-facing marketplace and dashboard screens when their fetch paths currently collapse into generic `Failed to fetch` behavior, and remove the layout breakage visible in the affected fallback UI.

## User-visible outcome

- `Chợ Gói kiến thức` loads or fails with a stable, actionable in-product state instead of a generic browser fetch failure.
- `Bảng điều khiển giáo viên` loads or fails with a bounded in-product state instead of a generic browser fetch failure.
- The affected fallback or settings shell no longer shows overlapping toggle controls or clipped copy on the reported viewport.

## Owned files

- `web/app/(utility)/marketplace/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/components/agents/SpecPackAuthoringTab.tsx` for the reported `Tutor rules` toggle layout defect only
- `web/lib/marketplace-api.ts`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/marketplace.py` only if the root cause is server-side for these fetch paths
- `deeptutor/api/routers/dashboard.py` only if the root cause is server-side for these fetch paths
- targeted marketplace/dashboard tests added or updated for this regression
- `web/tests/api-base-url.test.ts`
- `web/tests/agents-boolean-field-layout.test.ts`
- `tests/api/test_marketplace_router.py`
- `tests/api/test_dashboard_router.py`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-marketplace-dashboard-fetch-recovery.md`
- `docs/superpowers/pr-notes/2026-04-30-marketplace-dashboard-fetch-recovery.md`

## Do-not-touch

- unrelated `/playground` work
- knowledge-pack wizard redesign outside the direct error-state fix
- `/agents` and class-tutor flows
- lockfiles unless dependency changes are strictly required

## Design before implementation

### Current behavior

- The marketplace action flow and dashboard overview fetch can collapse into generic `Failed to fetch` behavior, which suggests the client is not recovering cleanly from an API URL, transport, or response-shape problem.
- The reported UI screenshot shows a visible shell/layout defect in the linked tutor rules toggle, so that teacher-facing control is not holding its layout under real copy length.

### Intended behavior change

- Marketplace and dashboard fetch paths should either succeed normally or surface a controlled app-level error state with stable copy and no layout breakage.
- The fetch clients should distinguish between transport failure and non-OK HTTP responses well enough for the UI to render deterministic recovery messaging.

### Candidate approaches

1. **Frontend-only catch-and-mask**
   - Pros: fast.
   - Cons: risks hiding a server-side contract bug and leaves the real root cause unresolved.

2. **Trace both client fetch wrappers and the corresponding API routes, then fix the failing boundary and harden the UI fallback**
   - Pros: addresses root cause and the visible UX regression together.
   - Cons: may require coordinated frontend and backend edits.

### Chosen approach

- Use **Approach 2**.
- Reproduce first, identify whether the failure is at the client URL/fetch layer or the API route/response layer, then add the smallest fix that restores deterministic behavior and stable UI.

### Required code reading

- Entry points/handlers:
  - `web/app/(utility)/marketplace/page.tsx`
  - `web/app/(workspace)/dashboard/page.tsx`
- Primary service/use-case modules:
  - `web/lib/marketplace-api.ts`
  - `web/lib/dashboard-api.ts`
- Shared contracts/types:
  - marketplace list/import response shapes
  - dashboard overview response shape
- Adjacent flows:
  - page-level loading and error states
  - existing offline/cache behavior in marketplace fetches
- Closest existing tests:
  - `tests/api/test_marketplace_router.py`
  - `tests/api/test_dashboard_router.py`
  - current frontend marketplace/dashboard tests, if present

### Expected impact surface

- Likely change:
  - fetch wrappers
  - page-level error handling
  - bounded teacher-facing fallback layout
  - the `Tutor rules` boolean control layout in `SpecPackAuthoringTab.tsx`
  - API routes only if root cause is server-side
- Reviewed but expected unchanged:
  - unrelated dashboard child routes
  - knowledge management backend
  - tutor and playground runtime

### Validation paths

- `/marketplace`
- marketplace import action path
- `/dashboard`
- the specific UI shell state shown in the screenshot

## Acceptance criteria

- Marketplace no longer fails with an unhandled generic fetch error under the reproduced scenario.
- Teacher dashboard no longer fails with an unhandled generic fetch error under the reproduced scenario.
- The affected UI fallback or shell state no longer overlaps controls or clips copy at the reported width.

## Validation

- targeted failing tests first for the reproduced boundary
- `git diff --check`
- relevant frontend test command(s)
- relevant Python API test command(s) if backend code changes

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is expected to remain unchanged unless the fetch recovery requires a route or workflow change rather than a bounded behavior fix.
