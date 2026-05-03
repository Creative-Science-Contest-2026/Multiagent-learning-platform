# Task Packet: Auth And Multi-User Foundation

- Task ID: `AUTH_MULTI_USER_FOUNDATION`
- Commit tag: `AUTH-MULTI-USER`
- Date: 2026-05-02
- Branch: `fix/auth-multi-user-foundation`
- Status: implementing

## Objective

Introduce PostgreSQL-backed authentication, role-aware product entry, and user-owned learning sessions for teacher, student, and internal admin flows.

## User-Approved Scope

- public signup is allowed
- public login is allowed
- public roles:
  - `teacher`
  - `student`
- internal-only role:
  - `admin`
- support both:
  - email + password
  - Google login
- split post-login entry into:
  - `/teacher`
  - `/student`
  - `/admin`
- move user identity and session ownership toward PostgreSQL

## Owned Files

### Backend and control-plane scope open now

- `deeptutor/api/main.py`
- `deeptutor/api/routers/auth.py`
- `deeptutor/api/routers/admin_users.py`
- `deeptutor/api/routers/sessions.py`
- `deeptutor/api/routers/unified_ws.py`
- `deeptutor/api/routers/memory.py`
- `deeptutor/api/routers/dashboard.py`
- `deeptutor/api/routers/marketplace.py`
- `deeptutor/api/routers/knowledge.py`
- `deeptutor/api/routers/assessment.py`
- `deeptutor/api/routers/chat.py`
- `deeptutor/api/routers/solve.py`
- `deeptutor/api/routers/guide.py`
- `deeptutor/api/routers/tutorbot.py`
- `deeptutor/services/auth/**`
- `deeptutor/services/db/**`
- `deeptutor/services/session/**`
- `deeptutor/services/evidence/**`
- `deeptutor/services/memory/**`
- `deeptutor/agents/chat/session_manager.py`
- `deeptutor/agents/solve/session_manager.py`
- `deeptutor/agents/guide/guide_manager.py`
- `deeptutor/services/tutorbot/**`
- `alembic/**`
- `tests/api/test_auth_router.py`
- `tests/api/test_admin_users_router.py`
- `tests/api/test_session_review_router.py`
- `tests/api/test_unified_ws_turn_runtime.py`
- `tests/api/test_memory_router.py`
- `tests/api/test_dashboard_router.py`
- `tests/api/test_marketplace_router.py`
- `tests/api/test_knowledge_router.py`
- `tests/api/test_assessment_router.py`
- `tests/api/test_chat_router.py`
- `tests/api/test_solve_router.py`
- `tests/api/test_guide_router.py`
- `tests/api/test_tutorbot_router.py`
- `tests/services/auth/**`
- `tests/services/memory/**`
- `tests/services/session/test_owned_session_store.py`
- `pyproject.toml`
- `requirements/server.txt`
- `docs/superpowers/tasks/2026-05-02-auth-multi-user-foundation.md`
- `docs/superpowers/specs/2026-05-02-auth-multi-user-foundation-design.md`
- `docs/superpowers/plans/2026-05-02-auth-multi-user-foundation.md`
- `docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-02.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

### Frontend scope now approved by decomposed ownership

- `web/app/login/**`
- `web/app/signup/**`
- `web/app/forgot-password/**`
- `web/app/reset-password/**`
- `web/app/verify-email/**`
- `web/app/teacher/**`
- `web/app/student/**`
- `web/app/admin/**`
- `web/app/(workspace)/layout.tsx`
- `web/app/(utility)/layout.tsx`
- `web/components/auth/**`
- `web/context/AuthContext.tsx`
- `web/lib/auth-api.ts`
- `web/lib/session-api.ts`
- `web/tests/auth-*.test.tsx`
- `web/tests/role-shell-routing.test.tsx`
- `web/tests/teacher-surface-gate.test.tsx`
- `web/tests/auth-shell-layout-source.test.ts`
- `web/tests/setup-vitest.ts`
- `web/vitest.config.ts`
- `web/app/layout.tsx`
- `web/package.json`
- `web/package-lock.json`

## Do-Not-Touch

- any `web/**` file outside the decomposed frontend auth scope above, except the two shared shell layouts explicitly opened for auth gating
- unrelated contest documentation under `docs/contest/**`
- unrelated runtime/product features outside auth, admin, and session ownership
- lockfiles unless dependency changes require them

## Design Before Implementation

- Approved spec:
  - `docs/superpowers/specs/2026-05-02-auth-multi-user-foundation-design.md`
- Approved plan:
  - `docs/superpowers/plans/2026-05-02-auth-multi-user-foundation.md`
- Current behavior:
  - anonymous single-operator runtime with shared SQLite-backed learning sessions and no auth
- Intended behavior:
  - backend-owned auth domain, PostgreSQL identity foundation, and owned learning sessions
- Chosen approach:
  - FastAPI-owned auth and identity, Next.js as a client
- Current auth-delivery behavior:
  - password reset and email verification now issue real backend tokens and use an explicit auth-mail delivery policy: `auto` sends through SMTP when configured, `disabled` suppresses delivery, and `required` treats missing or broken transport as a production misconfiguration while preserving privacy-safe forgot-password semantics
- Intended auth-delivery change:
  - add a bounded SMTP-backed auth mailer seam that sends reset and verification emails when configured, while preserving explicit debug-link behavior for local development and tests
- Current verification UX behavior:
  - `email_verified_at` exists in the auth contract, but signed-in teacher, student, and admin shells do not yet surface any inline verification state or resend path unless the user manually navigates to `/verify-email`
- Intended verification UX change:
  - add a shared non-blocking verification banner across signed-in shells and owned teacher-first layouts, with resend action and local refresh of auth state after successful verification
- Current signed-in shell UX behavior:
  - authenticated role shells still lack a unified account surface for role, email, verification status, and sign-out, which makes the auth foundation feel unfinished despite the backend being real
- Intended signed-in shell UX change:
  - add a shared signed-in account bar across owned auth shells and teacher-first legacy surfaces so users can always see identity, verification state, and logout affordances
- Current admin account-lifecycle behavior:
  - admin can list and create users, but cannot yet change role/status, and non-active account states are not enforced deeply enough across auth entry points
- Intended admin account-lifecycle change:
  - allow admin to update owned user role/status from the roster, and enforce non-active account states in email-password login, session lookup, and Google auth entry
- Current backend product-router behavior:
  - `dashboard`, `knowledge`, `marketplace`, and `assessment` still expose teacher-first product data and mutations without authenticated role enforcement, and assessment/dashboard support signals are still global rather than bound to the authenticated owner
- Intended backend product-router change:
  - require authenticated `teacher` or `admin` access on the teacher-first backend routers, scope session-backed dashboard and assessment reads to the authenticated owner for teachers, scope assessment/dashboard evidence rows to the authenticated owner, and stamp/import knowledge-pack ownership metadata so new auth-era records stop leaking across users
- Current dashboard-signal persistence behavior:
  - `observations` and `student_states` in the SQLite learning-session store still key only on `student_id` or `observation_id`, so repeated identifiers across teachers can collide or overwrite after multi-user auth lands
- Intended dashboard-signal persistence change:
  - rebuild those tables onto owner-aware composite keys and thread `owner_user_id` through dashboard rollup/save/read paths so teacher-specific diagnosis state stays isolated even when teachers reuse the same student identifiers
- Current tutoring-runtime signal behavior:
  - even after backend auth and dashboard hardening, live tutoring turns and context-building still materialize observations/state through ownerless store calls, which can repopulate the anonymous bucket during authenticated use
- Intended tutoring-runtime signal change:
  - carry the owning session's `owner_user_id` through tutoring observation persistence, student-state rollups, and context-builder lookups so authenticated chat and dashboard diagnostics share the same owner-scoped evidence model
- Current unified WebSocket behavior:
  - `/api/v1/ws` accepts connections and starts/subscribes/cancels turns without binding the socket to the authenticated user, so the owner-scoped session model can still be bypassed from the primary chat transport
- Intended unified WebSocket change:
  - resolve the authenticated user from the WS cookie at connect time, then propagate owner scope into start-turn, subscribe-session, subscribe-turn, and cancel-turn paths so websocket traffic cannot access or mutate another user's sessions
- Current shared memory behavior:
  - the lightweight `SUMMARY.md` / `PROFILE.md` memory system is still global, unauthenticated, and refreshed from whichever session is requested, so authenticated teacher/student traffic can leak profile and summary context across accounts
- Intended shared memory change:
  - require auth on the memory router, scope read/write/refresh/clear operations to the current user, and move persisted memory files under owner-specific paths so runtime memory context and refresh writes stop crossing user boundaries
- Current legacy chat/solve behavior:
  - the older `/chat` and `/solve` routes are still mounted publicly and store session history in shared JSON files without `owner_user_id`, so authenticated product users can bypass the new auth/session foundation through those legacy entrypoints
- Intended legacy chat/solve change:
  - require auth on the legacy chat and solve REST/websocket entrypoints, extend their shared `BaseSessionManager` records with optional `owner_user_id`, and filter list/get/update/delete/create flows by the authenticated owner so those fallback transports stop leaking sessions across accounts
- Current guided-learning behavior:
  - `/api/v1/guide` still exposes session creation, mutation, page reads, and websocket control without auth or owner binding, so guided-learning sessions can bypass the new account/session model entirely
- Intended guided-learning change:
  - require auth on `guide` REST/websocket entrypoints, persist `owner_user_id` on guided-learning session files, and ensure all create/get/list/reset/delete/chat/page flows only resolve sessions owned by the authenticated user unless the caller is admin
- Current tutorbot behavior:
  - `/api/v1/tutorbot` exposes bot lifecycle, bot files, history, souls, and bot websocket chat without auth, and bot configs/workspaces do not yet carry ownership metadata
- Intended tutorbot change:
  - require authenticated teacher/admin access on tutorbot routes, persist bot owner metadata for newly created bots, filter normal teacher access to owned bots/workspaces/history/websockets, and keep admin with cross-bot visibility for internal support
- Candidate approaches:
  - router-level role gates only, leaving underlying dashboard evidence tables global
  - full per-user isolation by extending router auth plus owner scoping into dashboard evidence services and auth-era knowledge-pack metadata
  - chosen: combine explicit role gates with owner-aware dashboard/evidence filtering and ownership metadata for auth-era knowledge packs/imports
- Chosen reason:
  - shallow route guards alone would still leak global teacher analytics rows and mutable teacher actions across accounts, while full data-model ownership for every legacy KB is too large for this lane; this hybrid approach hardens the current product surfaces without rewriting the entire knowledge subsystem

## Required Code Reading

- `deeptutor/api/main.py`
- `deeptutor/api/routers/auth.py`
- `deeptutor/api/routers/sessions.py`
- `deeptutor/api/routers/unified_ws.py`
- `deeptutor/api/routers/memory.py`
- `deeptutor/api/routers/chat.py`
- `deeptutor/api/routers/solve.py`
- `deeptutor/api/routers/guide.py`
- `deeptutor/api/routers/tutorbot.py`
- `deeptutor/api/routers/dashboard.py`
- `deeptutor/api/routers/marketplace.py`
- `deeptutor/api/routers/knowledge.py`
- `deeptutor/services/session/sqlite_store.py`
- `deeptutor/services/evidence/teacher_actions.py`
- `deeptutor/services/evidence/recommendation_acks.py`
- `deeptutor/services/evidence/recommendation_feedback.py`
- `deeptutor/services/evidence/teacher_overrides.py`
- `deeptutor/services/evidence/diagnosis_feedback.py`
- `deeptutor/services/evidence/intervention_assignments.py`
- `deeptutor/services/memory/service.py`
- `deeptutor/services/session/base_session_manager.py`
- `deeptutor/agents/chat/session_manager.py`
- `deeptutor/agents/solve/session_manager.py`
- `deeptutor/agents/guide/guide_manager.py`
- `deeptutor/services/tutorbot/manager.py`
- `deeptutor/services/path_service.py`
- `deeptutor/tutorbot/channels/email.py`
- `pyproject.toml`
- `requirements/server.txt`

## Impact Surface And Stop Conditions

- required first stop:
  - PostgreSQL/auth foundation exists
  - email/password auth API exists
  - admin and owned-session backend enforcement exists
- current stop condition for frontend:
  - stay inside the decomposed auth/frontend-gating scope and do not broaden into unrelated `web/**`
- current stop condition for delivery:
  - SMTP-configured environments send reset/verification emails through the new auth mailer seam
  - local/debug environments still expose explicit debug links for development and tests
- current stop condition for authorization depth inside owned session scope:
  - assessment review read/write endpoints and quiz-result writes enforce the authenticated owner boundary, not only the session id
- current stop condition for authorization depth across teacher-first product routers:
  - `dashboard`, `knowledge`, `marketplace`, and `assessment` require authenticated `teacher` or `admin`
  - teacher-scoped dashboard and assessment reads stop returning other users' sessions and support signals
  - new imported or created knowledge-pack records carry auth-era ownership metadata for later filtering and audits
- current stop condition for owner-scoped runtime context:
  - unified websocket traffic is bound to the authenticated owner at connect/start/subscribe/cancel time
  - lightweight memory context and refresh writes are isolated per authenticated user instead of living in a global shared file pair
- current stop condition for legacy transport hardening:
  - `/api/v1/chat*` and `/api/v1/solve*` reject unauthenticated requests and websockets
  - legacy chat/solve session CRUD and websocket resume paths use `owner_user_id` so one authenticated user cannot read or mutate another user's legacy JSON-backed sessions
- current stop condition for guided-learning/tutorbot hardening:
  - `/api/v1/guide*` rejects unauthenticated REST and websocket access and binds guided-learning session files to `owner_user_id`
  - `/api/v1/tutorbot*` rejects unauthenticated access, and non-admin teachers can only access bots/workspaces/history/websockets they own

## Required Tests

- `pytest tests/services/auth tests/api/test_auth_router.py tests/api/test_admin_users_router.py tests/services/session/test_owned_session_store.py -v`
- `git diff --check`

## Parallel-Work Notes

- use the dedicated worktree `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-auth-multi-user-foundation`
- frontend auth UI work is approved only for the decomposed auth-only frontend scope listed above
