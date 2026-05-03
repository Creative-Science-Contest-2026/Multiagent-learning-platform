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
- `deeptutor/services/auth/**`
- `deeptutor/services/db/**`
- `deeptutor/services/session/**`
- `alembic/**`
- `tests/api/test_auth_router.py`
- `tests/api/test_admin_users_router.py`
- `tests/api/test_session_review_router.py`
- `tests/services/auth/**`
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
  - password reset and email verification now issue real backend tokens and can send SMTP email when configured, while preserving explicit debug-link behavior for local development and tests
- Intended auth-delivery change:
  - add a bounded SMTP-backed auth mailer seam that sends reset and verification emails when configured, while preserving explicit debug-link behavior for local development and tests
- Candidate approaches:
  - reuse the full `tutorbot` email channel implementation directly
  - add ad-hoc `smtplib` calls inside auth routers
  - chosen: add a focused `deeptutor/services/auth/mailer.py` module with SMTP settings, message builders, and a small delivery API used by the auth router
- Chosen reason:
  - this keeps auth delivery isolated from the larger tutorbot subsystem, avoids scattered mail logic in routers, and stays dependency-light by reusing stdlib email/SMTP primitives

## Required Code Reading

- `deeptutor/api/main.py`
- `deeptutor/api/routers/auth.py`
- `deeptutor/api/routers/sessions.py`
- `deeptutor/services/session/sqlite_store.py`
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

## Required Tests

- `pytest tests/services/auth tests/api/test_auth_router.py tests/api/test_admin_users_router.py tests/services/session/test_owned_session_store.py -v`
- `git diff --check`

## Parallel-Work Notes

- use the dedicated worktree `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-auth-multi-user-foundation`
- frontend auth UI work is approved only for the decomposed auth-only frontend scope listed above
