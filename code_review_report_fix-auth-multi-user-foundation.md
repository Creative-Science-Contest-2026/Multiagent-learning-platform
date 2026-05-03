# Executive summary

- Branch reviewed: `fix/auth-multi-user-foundation`
- Base reviewed against: `origin/main`
- Review scope: auth foundation, owned session enforcement, public auth UI, signed-in shell UX, admin lifecycle surface, migrations, and control-plane docs
- Overall risk after fixes: `Medium`
- Final verdict: `Pass after fixes`

This branch now has a coherent multi-user auth foundation with materially better correctness than the pre-review state. I fixed the only concrete blocking issues I found inside the owned auth/session scope. The remaining risk is not a hidden bug inside the reviewed slices, but incomplete authorization depth outside the current owned router set and a still-thin mail-provider operational layer.

# Change summary

The branch introduces a backend-owned authentication system with PostgreSQL and Alembic, public signup/login flows for `teacher` and `student`, internal-only `admin`, Google OAuth, password reset, email verification, owned auth sessions, signed-in shell surfaces, and backend ownership checks for session-related review flows.

During review I made three corrective changes:

1. Prevented admin self-lockout by rejecting self-demotion and self-suspension.
2. Fixed stale local state in the admin roster UI after a failed lifecycle save.
3. Removed repeated auth schema initialization overhead from request-scoped service construction.

# Detailed findings

## 1. [Fixed] Admin could lock out the only privileged operator

- Severity: `High`
- Files:
  - `deeptutor/api/routers/admin_users.py`
  - `tests/api/test_admin_users_router.py`

Before the fix, an authenticated admin could use the lifecycle update endpoint to demote themselves out of `admin` or suspend their own account. That creates an avoidable self-lockout path in the exact surface responsible for access control. I fixed this at the router boundary and added test coverage for both self-demotion and self-suspension rejection.

## 2. [Fixed] Admin lifecycle form could present unsaved values as if they were saved

- Severity: `Medium`
- Files:
  - `web/components/auth/AdminUsersPanel.tsx`
  - `web/tests/auth-admin-page.test.tsx`

The roster UI updates local row state immediately when a role or status select changes. If the save request fails, the old implementation could keep showing the optimistic values even though the backend rejected them. That is a trust issue for an admin surface. I fixed it by reloading the canonical roster after a failed lifecycle update and added frontend coverage for the recovery path.

## 3. [Fixed] Auth schema bootstrap was repeated too often

- Severity: `Medium`
- Files:
  - `deeptutor/services/db/postgres.py`

`AuthService()` construction triggered `init_auth_schema()` repeatedly. Because the service is resolved in request-scoped dependencies, the branch was paying unnecessary metadata/bootstrap work far more often than needed. I added a cached initialization guard so the schema bootstrap runs once per effective database URL instead of on every service creation.

## 4. [Residual risk] Authorization is still shallower than the product surface

- Severity: `Medium`
- Files:
  - outside the current owned auth/session subset

The owned-session boundary is now materially better, but many product routers outside the current session/auth slice still do not enforce owner or role deeply enough. This is the next real engineering risk after the current review pass. It is a scope gap, not a newly found branch-local bug.

## 5. [Residual risk] Mail delivery seam is functional but still operationally thin

- Severity: `Low`
- Files:
  - `deeptutor/services/auth/mailer.py`
  - `deeptutor/api/routers/auth.py`

The branch now has a usable SMTP seam plus debug-link fallback, which is a valid step forward. But it still lacks stronger provider-level operational behavior such as richer error classification, delivery telemetry, bounce/provider response capture, and clearer production-mode policy. This is the most valuable follow-up inside the current auth-owned scope.

# Suggested fixes

- Keep the self-lockout guard in the admin router and preserve the new backend test as a non-regression check.
- Keep the admin roster failure recovery path authoritative by reloading from the backend after failed lifecycle updates.
- Keep the cached auth schema bootstrap; do not regress to per-request initialization behavior.
- Next in the auth lane, either:
  - deepen authorization across additional product routers, after task ownership is expanded, or
  - harden the SMTP/provider seam inside the current auth scope with production-mode rules and delivery observability.

# Recommended test cases

- Backend non-regression:
  - admin cannot suspend self
  - admin cannot demote self out of `admin`
  - suspended users cannot continue through password login, existing session lookup, or Google callback
- Frontend non-regression:
  - failed admin lifecycle update restores canonical roster state
  - account bar and verification banner render correctly for signed-in roles
  - teacher-first legacy shells redirect `student` away from teacher surfaces
- Operational follow-up:
  - mail delivery behavior when SMTP is misconfigured
  - production-mode behavior when no mail transport is configured
  - provider error path does not leak reset/verification existence semantics

# Verification run

Commands run during this review/fix pass:

```bash
git -C .worktrees/fix-auth-multi-user-foundation status --short --branch
git -C .worktrees/fix-auth-multi-user-foundation diff --stat origin/main...HEAD
git -C .worktrees/fix-auth-multi-user-foundation diff --name-only origin/main...HEAD
python -m pytest .worktrees/fix-auth-multi-user-foundation/tests/api/test_admin_users_router.py .worktrees/fix-auth-multi-user-foundation/tests/api/test_auth_router.py -v
python -m pytest .worktrees/fix-auth-multi-user-foundation/tests/api/test_admin_users_router.py .worktrees/fix-auth-multi-user-foundation/tests/api/test_auth_router.py .worktrees/fix-auth-multi-user-foundation/tests/services/auth/test_service.py -v
cd .worktrees/fix-auth-multi-user-foundation/web && node node_modules/vitest/vitest.mjs run tests/auth-admin-page.test.tsx
cd .worktrees/fix-auth-multi-user-foundation/web && node node_modules/vitest/vitest.mjs run tests/auth-admin-page.test.tsx tests/auth-signed-in-account-bar.test.tsx tests/auth-email-verification-banner.test.tsx tests/auth-teacher-surface-gate.test.tsx tests/auth-shell-layout-source.test.ts
cd .worktrees/fix-auth-multi-user-foundation/web && npm run build
git -C .worktrees/fix-auth-multi-user-foundation diff --check
```

All commands above passed after the fixes were applied.

# Per-file review coverage

The files below were reviewed as part of the branch diff against `origin/main`.

- `ai_first/ACTIVE_ASSIGNMENTS.md` — Review confidence: `9/10`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` — Review confidence: `9/10`
- `ai_first/daily/2026-05-02.md` — Review confidence: `9/10`
- `ai_first/daily/2026-05-03.md` — Review confidence: `9/10`
- `alembic.ini` — Review confidence: `8/10`
- `alembic/env.py` — Review confidence: `8/10`
- `alembic/script.py.mako` — Review confidence: `8/10`
- `alembic/versions/20260502_0001_auth_foundation.py` — Review confidence: `8/10`
- `alembic/versions/20260502_0002_session_ownership.py` — Review confidence: `8/10`
- `deeptutor/api/main.py` — Review confidence: `8/10`
- `deeptutor/api/routers/__init__.py` — Review confidence: `8/10`
- `deeptutor/api/routers/admin_users.py` — Review confidence: `9/10`
- `deeptutor/api/routers/auth.py` — Review confidence: `8/10`
- `deeptutor/api/routers/sessions.py` — Review confidence: `9/10`
- `deeptutor/services/auth/__init__.py` — Review confidence: `8/10`
- `deeptutor/services/auth/deps.py` — Review confidence: `8/10`
- `deeptutor/services/auth/google_oauth.py` — Review confidence: `8/10`
- `deeptutor/services/auth/mailer.py` — Review confidence: `8/10`
- `deeptutor/services/auth/models.py` — Review confidence: `8/10`
- `deeptutor/services/auth/passwords.py` — Review confidence: `8/10`
- `deeptutor/services/auth/schemas.py` — Review confidence: `8/10`
- `deeptutor/services/auth/service.py` — Review confidence: `9/10`
- `deeptutor/services/auth/session_tokens.py` — Review confidence: `8/10`
- `deeptutor/services/db/__init__.py` — Review confidence: `8/10`
- `deeptutor/services/db/postgres.py` — Review confidence: `9/10`
- `deeptutor/services/session/sqlite_store.py` — Review confidence: `8/10`
- `docs/superpowers/plans/2026-05-02-auth-multi-user-foundation.md` — Review confidence: `9/10`
- `docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md` — Review confidence: `9/10`
- `docs/superpowers/specs/2026-05-02-auth-multi-user-foundation-design.md` — Review confidence: `9/10`
- `docs/superpowers/tasks/2026-05-02-auth-multi-user-foundation.md` — Review confidence: `9/10`
- `pyproject.toml` — Review confidence: `8/10`
- `requirements/server.txt` — Review confidence: `8/10`
- `tests/api/test_admin_users_router.py` — Review confidence: `9/10`
- `tests/api/test_auth_router.py` — Review confidence: `8/10`
- `tests/api/test_session_review_router.py` — Review confidence: `8/10`
- `tests/services/auth/test_mailer.py` — Review confidence: `8/10`
- `tests/services/auth/test_passwords.py` — Review confidence: `8/10`
- `tests/services/auth/test_service.py` — Review confidence: `8/10`
- `tests/services/session/test_owned_session_store.py` — Review confidence: `8/10`
- `web/app/(utility)/layout.tsx` — Review confidence: `8/10`
- `web/app/(workspace)/layout.tsx` — Review confidence: `8/10`
- `web/app/admin/layout.tsx` — Review confidence: `8/10`
- `web/app/admin/page.tsx` — Review confidence: `8/10`
- `web/app/forgot-password/page.tsx` — Review confidence: `8/10`
- `web/app/layout.tsx` — Review confidence: `8/10`
- `web/app/login/page.tsx` — Review confidence: `8/10`
- `web/app/reset-password/page.tsx` — Review confidence: `8/10`
- `web/app/signup/page.tsx` — Review confidence: `8/10`
- `web/app/student/layout.tsx` — Review confidence: `8/10`
- `web/app/student/page.tsx` — Review confidence: `8/10`
- `web/app/teacher/layout.tsx` — Review confidence: `8/10`
- `web/app/teacher/page.tsx` — Review confidence: `8/10`
- `web/app/verify-email/page.tsx` — Review confidence: `8/10`
- `web/components/auth/AdminUsersPanel.tsx` — Review confidence: `9/10`
- `web/components/auth/AuthShell.tsx` — Review confidence: `8/10`
- `web/components/auth/EmailVerificationBanner.tsx` — Review confidence: `8/10`
- `web/components/auth/ForgotPasswordForm.tsx` — Review confidence: `8/10`
- `web/components/auth/LoginForm.tsx` — Review confidence: `8/10`
- `web/components/auth/ProtectedRoute.tsx` — Review confidence: `8/10`
- `web/components/auth/ResetPasswordForm.tsx` — Review confidence: `8/10`
- `web/components/auth/RolePicker.tsx` — Review confidence: `8/10`
- `web/components/auth/SignedInAccountBar.tsx` — Review confidence: `8/10`
- `web/components/auth/SignupForm.tsx` — Review confidence: `8/10`
- `web/components/auth/TeacherSurfaceGate.tsx` — Review confidence: `8/10`
- `web/components/auth/VerifyEmailPanel.tsx` — Review confidence: `8/10`
- `web/context/AuthContext.tsx` — Review confidence: `8/10`
- `web/lib/auth-api.ts` — Review confidence: `8/10`
- `web/lib/session-api.ts` — Review confidence: `8/10`
- `web/package-lock.json` — Review confidence: `6/10`
- `web/package.json` — Review confidence: `8/10`
- `web/tests/auth-admin-page.test.tsx` — Review confidence: `9/10`
- `web/tests/auth-email-verification-banner.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-login-page.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-recovery-pages.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-role-hubs.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-role-picker.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-shell-layout-source.test.ts` — Review confidence: `8/10`
- `web/tests/auth-signed-in-account-bar.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-signup-page.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-teacher-surface-gate.test.tsx` — Review confidence: `8/10`
- `web/tests/auth-verify-page.test.tsx` — Review confidence: `8/10`
- `web/tests/role-shell-routing.test.tsx` — Review confidence: `8/10`
- `web/tests/setup-vitest.ts` — Review confidence: `8/10`
- `web/vitest.config.ts` — Review confidence: `8/10`

`web/package-lock.json` still deserves a human dependency-tree audit before release if package updates continue, but that is not a correctness blocker for this branch.

# Final verdict

No blocking bug remains in the reviewed auth/session scope after the fixes above. The branch is acceptable to continue from. The highest-value next step is to harden the auth mail-provider seam further inside the current owned scope, or expand task ownership and then deepen authorization across additional product routers.
