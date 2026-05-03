# PR Note: Auth And Multi-User Foundation

## Summary

- adds a PostgreSQL-backed auth foundation with SQLAlchemy and Alembic
- introduces backend-owned email/password login, Google OAuth entry, admin-only user listing, and opaque auth sessions
- adds internal admin account creation so `/admin` can list and create teacher/student/admin accounts
- adds password-reset and email-verification token issue/consume flows with SMTP-backed delivery when configured plus explicit debug-link fallback for local/test flows
- binds learning-session list/get/rename/delete behavior to `owner_user_id`
- enforces session ownership on assessment review, rubric review, and quiz-result write endpoints so review flows no longer bypass the auth boundary
- makes the auth session cookie production-configurable for `secure`, `samesite`, and `max-age` instead of hardcoding demo defaults
- preserves safe `next` redirects across login/signup and Google auth entry so protected teacher surfaces now bounce users back to the route they originally requested
- adds public auth routes, recovery/verification pages, and role-specific `/teacher`, `/student`, and `/admin` shells in the approved frontend auth scope
- upgrades `/teacher` and `/student` from placeholder shells into role hubs that link into the current teacher-first and student-facing routes
- gates the legacy teacher-first `(workspace)` and `(utility)` shells behind authenticated teacher/admin access

## Architecture

```mermaid
flowchart TD
  Public["Public auth routes"] --> Signup["/signup"]
  Public --> Login["/login"]
  Public --> Recovery["/forgot-password · /reset-password · /verify-email"]
  Login --> AuthAPI["/api/v1/auth"]
  Signup --> AuthAPI
  Recovery --> AuthAPI
  Login --> NextRedirect["Safe next redirect + Google role selection"]
  AuthAPI --> Users["PostgreSQL users + credentials + oauth identities"]
  AuthAPI --> Sessions["HttpOnly deeptutor_session"]
  AuthAPI --> OneTimeTokens["Password-reset + email-verification tokens"]
  OneTimeTokens --> AuthMailer["SMTP auth mailer seam + debug fallback"]
  AdminShell --> AdminUsersAPI["/api/v1/admin/users GET/POST"]
  AdminUsersAPI --> AdminPanel["Roster + internal account creation"]
  Sessions --> Me["GET /api/v1/auth/me"]
  Me --> TeacherShell["/teacher"]
  Me --> StudentShell["/student"]
  Me --> AdminShell["/admin"]
  NextRedirect --> TeacherShell
  NextRedirect --> StudentShell
  TeacherShell --> TeacherHub["Knowledge · Dashboard · Agents entry links"]
  StudentShell --> StudentHub["Playground · Student progress · Docs entry links"]
  Me --> TeacherGate["TeacherSurfaceGate for legacy shells"]
  TeacherGate --> LegacyShells["(workspace) + (utility) layouts"]
  TeacherShell --> OwnedSessionAPI["/api/v1/sessions scoped by owner_user_id"]
  StudentShell --> OwnedSessionAPI
  OwnedSessionAPI --> SQLiteStore["SQLite learning-session store with owner boundary"]
  OwnedSessionAPI --> ReviewFlows["assessment-review + rubric-review + quiz-results now owner-scoped"]
```

## Scope Notes

- `admin` is internal-only and blocked from public signup
- password reset and email verification now issue and consume real backend tokens
- delivery now uses SMTP when `DEEPTUTOR_AUTH_SMTP_*` and `DEEPTUTOR_AUTH_FROM_*` are configured, with debug-link fallback preserved for local/test environments
- assessment review write/read flows now require the authenticated owner instead of only the session id
- unrelated `web/**` surfaces remain outside scope because this lane only owns the decomposed auth frontend subset
