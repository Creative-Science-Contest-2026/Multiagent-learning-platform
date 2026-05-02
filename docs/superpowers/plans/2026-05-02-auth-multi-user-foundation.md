# Auth And Multi-User Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current anonymous single-operator product flow with a real multi-user foundation: backend-owned auth, PostgreSQL identity storage, teacher/student/admin roles, public signup/login, role-specific shells, and user-owned learning sessions.

**Architecture:** Keep FastAPI as the identity authority. Introduce a PostgreSQL-backed auth domain with opaque server-side auth sessions, then progressively move existing learning sessions behind authenticated ownership boundaries. On the frontend, add standalone public auth routes and split post-login navigation into separate teacher, student, and admin shells rather than hiding features inside one generic workspace.

**Tech Stack:** FastAPI, PostgreSQL, SQLAlchemy 2, Alembic, Authlib, Argon2 password hashing, Next.js App Router, React 19, TypeScript, Vitest, Pytest

---

## Scope Note

This feature is too large for one blind implementation pass. Execute it as sequenced runtime slices that each leave the repo in a working, testable state. Do not try to land auth, Google OAuth, session ownership migration, and all role shells in one unreviewed PR.

## File Structure

- Create: `docs/superpowers/tasks/2026-05-02-auth-multi-user-foundation.md`
- Create: `deeptutor/services/db/__init__.py`
- Create: `deeptutor/services/db/postgres.py`
- Create: `deeptutor/services/auth/__init__.py`
- Create: `deeptutor/services/auth/models.py`
- Create: `deeptutor/services/auth/schemas.py`
- Create: `deeptutor/services/auth/passwords.py`
- Create: `deeptutor/services/auth/session_tokens.py`
- Create: `deeptutor/services/auth/service.py`
- Create: `deeptutor/services/auth/google_oauth.py`
- Create: `deeptutor/services/auth/deps.py`
- Create: `deeptutor/api/routers/auth.py`
- Create: `deeptutor/api/routers/admin_users.py`
- Create: `alembic.ini`
- Create: `alembic/env.py`
- Create: `alembic/script.py.mako`
- Create: `alembic/versions/20260502_0001_auth_foundation.py`
- Create: `alembic/versions/20260502_0002_session_ownership.py`
- Create: `tests/api/test_auth_router.py`
- Create: `tests/api/test_admin_users_router.py`
- Create: `tests/services/auth/test_service.py`
- Create: `tests/services/auth/test_passwords.py`
- Create: `tests/services/session/test_owned_session_store.py`
- Create: `web/lib/auth-api.ts`
- Create: `web/context/AuthContext.tsx`
- Create: `web/components/auth/AuthShell.tsx`
- Create: `web/components/auth/RolePicker.tsx`
- Create: `web/components/auth/SignupForm.tsx`
- Create: `web/components/auth/LoginForm.tsx`
- Create: `web/components/auth/ProtectedRoute.tsx`
- Create: `web/app/login/page.tsx`
- Create: `web/app/signup/page.tsx`
- Create: `web/app/forgot-password/page.tsx`
- Create: `web/app/reset-password/page.tsx`
- Create: `web/app/verify-email/page.tsx`
- Create: `web/app/teacher/layout.tsx`
- Create: `web/app/teacher/page.tsx`
- Create: `web/app/student/layout.tsx`
- Create: `web/app/student/page.tsx`
- Create: `web/app/admin/layout.tsx`
- Create: `web/app/admin/page.tsx`
- Create: `web/tests/auth-role-picker.test.tsx`
- Create: `web/tests/auth-signup-page.test.tsx`
- Create: `web/tests/auth-login-page.test.tsx`
- Create: `web/tests/role-shell-routing.test.tsx`
- Modify: `pyproject.toml`
- Modify: `requirements/server.txt`
- Modify: `deeptutor/api/main.py`
- Modify: `deeptutor/api/routers/sessions.py`
- Modify: `deeptutor/services/session/sqlite_store.py`
- Modify: `deeptutor/services/session/__init__.py`
- Modify: `web/app/layout.tsx`
- Modify: `web/lib/session-api.ts`
- Modify: `web/components/SessionList.tsx`
- Modify: `web/package.json`
- Modify: `web/vitest.config.ts`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-05-02.md`
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- Create: `docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md`

### Task 1: Publish The Runtime Lane Contract

**Files:**
- Create: `docs/superpowers/tasks/2026-05-02-auth-multi-user-foundation.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-05-02.md`

- [ ] **Step 1: Write the task packet before code work**

Create `docs/superpowers/tasks/2026-05-02-auth-multi-user-foundation.md` with:

```md
# Task Packet: Auth And Multi-User Foundation

- Task ID: `AUTH_MULTI_USER_FOUNDATION`
- Commit tag: `AUTH-MULTI-USER`
- Date: 2026-05-02
- Branch: `fix/auth-multi-user-foundation`
- Status: planning

## Objective

Introduce PostgreSQL-backed authentication, role-aware product entry, and user-owned learning sessions for teacher, student, and internal admin flows.

## Owned Files

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
- `tests/services/auth/**`
- `tests/services/session/test_owned_session_store.py`
- `web/app/login/**`
- `web/app/signup/**`
- `web/app/forgot-password/**`
- `web/app/reset-password/**`
- `web/app/verify-email/**`
- `web/app/teacher/**`
- `web/app/student/**`
- `web/app/admin/**`
- `web/components/auth/**`
- `web/context/AuthContext.tsx`
- `web/lib/auth-api.ts`
- `web/lib/session-api.ts`
- `web/tests/auth-*.test.tsx`
- `web/tests/role-shell-routing.test.tsx`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-02.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- `docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md`
```

- [ ] **Step 2: Resolve the current `web/**` ownership conflict**

Run:

```bash
rtk sed -n '1,220p' ai_first/ACTIVE_ASSIGNMENTS.md
```

Expected:

- confirm whether `fix/frontend-test-coverage-gate` still owns `web/**`
- if yes, do not edit `web/**` until ownership is explicitly decomposed or that lane closes

- [ ] **Step 3: Open the dedicated runtime worktree**

Run:

```bash
rtk git fetch origin main
rtk git worktree add .worktrees/fix-auth-multi-user-foundation -b fix/auth-multi-user-foundation origin/main
```

Expected:

- a clean worktree at `.worktrees/fix-auth-multi-user-foundation`
- branch `fix/auth-multi-user-foundation` created from `origin/main`

- [ ] **Step 4: Record the live assignment**

Append this exact entry to `ai_first/ACTIVE_ASSIGNMENTS.md`:

```md
### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-auth-multi-user-foundation`
- Task: Introduce PostgreSQL-backed auth, role-specific shells, and owned learning sessions
- Status: implementing
- Branch: `fix/auth-multi-user-foundation`
- Task packet: `docs/superpowers/tasks/2026-05-02-auth-multi-user-foundation.md`
- Owned files: `deeptutor/api/main.py`, `deeptutor/api/routers/auth.py`, `deeptutor/api/routers/admin_users.py`, `deeptutor/api/routers/sessions.py`, `deeptutor/services/auth/**`, `deeptutor/services/db/**`, `deeptutor/services/session/**`, `alembic/**`, `tests/api/test_auth_router.py`, `tests/api/test_admin_users_router.py`, `tests/services/auth/**`, `tests/services/session/test_owned_session_store.py`, `web/app/login/**`, `web/app/signup/**`, `web/app/forgot-password/**`, `web/app/reset-password/**`, `web/app/verify-email/**`, `web/app/teacher/**`, `web/app/student/**`, `web/app/admin/**`, `web/components/auth/**`, `web/context/AuthContext.tsx`, `web/lib/auth-api.ts`, `web/lib/session-api.ts`, `web/tests/auth-*.test.tsx`, `web/tests/role-shell-routing.test.tsx`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-05-02.md`, `ai_first/architecture/MAIN_SYSTEM_MAP.md`, `docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md`
- PR: uncreated
- Last update: 2026-05-02
- Next action: add the backend auth foundation and PostgreSQL plumbing before touching role shells
- Blocker: `web/**` ownership must be decomposed if the frontend coverage gate lane is still active
```

- [ ] **Step 5: Record the start in the daily log**

Append:

```md
## AUTH_MULTI_USER_FOUNDATION

- Branch: `fix/auth-multi-user-foundation`
- Task: `AUTH_MULTI_USER_FOUNDATION`
- Done: Published the task packet, opened the runtime lane, and recorded the assignment for backend-owned multi-user auth.
- Tests: `git worktree list`; `git status --short --branch`
```

- [ ] **Step 6: Commit the control-plane setup**

Run:

```bash
rtk git add docs/superpowers/tasks/2026-05-02-auth-multi-user-foundation.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-05-02.md
rtk git commit -m "chore(auth): open multi-user foundation lane [AUTH-MULTI-USER]"
```

Expected:

- one clean commit that opens the runtime lane contract before implementation

### Task 2: Add PostgreSQL And Migration Plumbing

**Files:**
- Modify: `pyproject.toml`
- Modify: `requirements/server.txt`
- Create: `deeptutor/services/db/__init__.py`
- Create: `deeptutor/services/db/postgres.py`
- Create: `alembic.ini`
- Create: `alembic/env.py`
- Create: `alembic/script.py.mako`
- Create: `alembic/versions/20260502_0001_auth_foundation.py`
- Test: `tests/services/auth/test_service.py`

- [ ] **Step 1: Write the failing backend config test**

Create `tests/services/auth/test_service.py` with:

```python
from deeptutor.services.db.postgres import AuthDatabaseSettings


def test_auth_database_settings_require_postgres_url() -> None:
    settings = AuthDatabaseSettings(database_url="postgresql+psycopg://user:pass@localhost/app")
    assert settings.database_url.startswith("postgresql+psycopg://")
```

- [ ] **Step 2: Run the test to confirm the DB module does not exist yet**

Run:

```bash
rtk pytest tests/services/auth/test_service.py::test_auth_database_settings_require_postgres_url -v
```

Expected:

- FAIL with import error for `deeptutor.services.db.postgres`

- [ ] **Step 3: Add the backend dependencies**

Modify `pyproject.toml` project dependencies and optional server dependencies to include:

```toml
"sqlalchemy>=2.0.41",
"psycopg[binary]>=3.2.9",
"alembic>=1.16.4",
"authlib>=1.6.0",
"argon2-cffi>=25.1.0",
```

Modify `requirements/server.txt` to include:

```txt
sqlalchemy>=2.0.41
psycopg[binary]>=3.2.9
alembic>=1.16.4
authlib>=1.6.0
argon2-cffi>=25.1.0
```

- [ ] **Step 4: Add the PostgreSQL settings and engine module**

Create `deeptutor/services/db/postgres.py`:

```python
from __future__ import annotations

from functools import lru_cache

from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class AuthDatabaseSettings(BaseModel):
    database_url: str = Field(..., min_length=1)


@lru_cache(maxsize=1)
def get_auth_engine(database_url: str) -> Engine:
    return create_engine(database_url, future=True, pool_pre_ping=True)
```

Create `deeptutor/services/db/__init__.py`:

```python
from .postgres import AuthDatabaseSettings, get_auth_engine

__all__ = ["AuthDatabaseSettings", "get_auth_engine"]
```

- [ ] **Step 5: Add Alembic bootstrap files**

Create `alembic.ini` with `script_location = alembic` and a `sqlalchemy.url` placeholder.

Create `alembic/env.py` to import the auth metadata:

```python
from deeptutor.services.auth.models import Base

target_metadata = Base.metadata
```

Create migration `alembic/versions/20260502_0001_auth_foundation.py` with empty upgrade/downgrade skeleton first:

```python
def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
```

- [ ] **Step 6: Run the test again**

Run:

```bash
rtk pytest tests/services/auth/test_service.py::test_auth_database_settings_require_postgres_url -v
```

Expected:

- PASS

- [ ] **Step 7: Commit the DB foundation**

Run:

```bash
rtk git add pyproject.toml requirements/server.txt deeptutor/services/db/__init__.py deeptutor/services/db/postgres.py alembic.ini alembic/env.py alembic/script.py.mako alembic/versions/20260502_0001_auth_foundation.py tests/services/auth/test_service.py
rtk git commit -m "feat(auth): add postgres and migration foundation [AUTH-MULTI-USER]"
```

### Task 3: Implement The Auth Domain And Opaque Session Cookies

**Files:**
- Create: `deeptutor/services/auth/models.py`
- Create: `deeptutor/services/auth/schemas.py`
- Create: `deeptutor/services/auth/passwords.py`
- Create: `deeptutor/services/auth/session_tokens.py`
- Create: `deeptutor/services/auth/service.py`
- Create: `tests/services/auth/test_passwords.py`
- Modify: `alembic/versions/20260502_0001_auth_foundation.py`

- [ ] **Step 1: Write the failing password hashing test**

Create `tests/services/auth/test_passwords.py`:

```python
from deeptutor.services.auth.passwords import hash_password, verify_password


def test_hash_and_verify_password_roundtrip() -> None:
    hashed = hash_password("StrongPass123!")
    assert hashed != "StrongPass123!"
    assert verify_password("StrongPass123!", hashed) is True
    assert verify_password("WrongPass123!", hashed) is False
```

- [ ] **Step 2: Run the test to confirm the auth package is still missing**

Run:

```bash
rtk pytest tests/services/auth/test_passwords.py::test_hash_and_verify_password_roundtrip -v
```

Expected:

- FAIL with import error

- [ ] **Step 3: Create the core auth models**

Create `deeptutor/services/auth/models.py` with SQLAlchemy base and tables:

```python
class UserRole(str, enum.Enum):
    teacher = "teacher"
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
```

Include:

- `users`
- `user_password_credentials`
- `user_oauth_identities`
- `auth_sessions`
- `email_verification_tokens`
- `password_reset_tokens`

- [ ] **Step 4: Create password hashing and opaque session token helpers**

Create `deeptutor/services/auth/passwords.py`:

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_HASHER = PasswordHasher()


def hash_password(password: str) -> str:
    return _HASHER.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _HASHER.verify(password_hash, password)
    except VerifyMismatchError:
        return False
```

Create `deeptutor/services/auth/session_tokens.py`:

```python
import hashlib
import secrets


def mint_session_secret() -> str:
    return secrets.token_urlsafe(48)


def hash_session_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()
```

- [ ] **Step 5: Create the first auth service surface**

Create `deeptutor/services/auth/service.py` with signatures only:

```python
class AuthService:
    def create_user(self, *, email: str, display_name: str, role: str, password: str) -> dict[str, str]:
        ...

    def create_auth_session(self, *, user_id: str, user_agent: str | None, ip_address: str | None) -> tuple[str, str]:
        ...
```

- [ ] **Step 6: Fill the first migration with the auth tables**

Update `alembic/versions/20260502_0001_auth_foundation.py` to create the six auth tables and the `users.role` enum.

- [ ] **Step 7: Run the auth unit tests**

Run:

```bash
rtk pytest tests/services/auth/test_passwords.py tests/services/auth/test_service.py -v
```

Expected:

- PASS

- [ ] **Step 8: Commit the auth domain**

Run:

```bash
rtk git add deeptutor/services/auth/models.py deeptutor/services/auth/schemas.py deeptutor/services/auth/passwords.py deeptutor/services/auth/session_tokens.py deeptutor/services/auth/service.py alembic/versions/20260502_0001_auth_foundation.py tests/services/auth/test_passwords.py tests/services/auth/test_service.py
rtk git commit -m "feat(auth): add core auth domain models [AUTH-MULTI-USER]"
```

### Task 4: Add Email And Password Auth APIs

**Files:**
- Create: `deeptutor/services/auth/deps.py`
- Create: `deeptutor/api/routers/auth.py`
- Modify: `deeptutor/api/main.py`
- Create: `tests/api/test_auth_router.py`

- [ ] **Step 1: Write the failing auth router test**

Create `tests/api/test_auth_router.py`:

```python
from fastapi.testclient import TestClient

from deeptutor.api.main import app


def test_signup_rejects_admin_role_from_public_flow() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "display_name": "Root Attempt",
            "email": "root@example.com",
            "password": "StrongPass123!",
            "role": "admin",
        },
    )
    assert response.status_code == 400
```

- [ ] **Step 2: Run the auth router test**

Run:

```bash
rtk pytest tests/api/test_auth_router.py::test_signup_rejects_admin_role_from_public_flow -v
```

Expected:

- FAIL because `/api/v1/auth/signup` does not exist yet

- [ ] **Step 3: Implement the auth request schemas and dependency layer**

Create `deeptutor/services/auth/schemas.py` with:

```python
class SignupRequest(BaseModel):
    display_name: str
    email: EmailStr
    password: str
    role: Literal["teacher", "student"]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

Create `deeptutor/services/auth/deps.py` with:

```python
def get_current_user(request: Request) -> AuthenticatedUser:
    ...


def require_roles(*roles: str):
    ...
```

- [ ] **Step 4: Implement the first auth router endpoints**

Create `deeptutor/api/routers/auth.py`:

```python
@router.post("/signup")
def signup(payload: SignupRequest, request: Request, response: Response):
    ...


@router.post("/login")
def login(payload: LoginRequest, request: Request, response: Response):
    ...


@router.post("/logout")
def logout(request: Request, response: Response):
    ...


@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return {"user": current_user.model_dump()}
```

Set the auth cookie inside signup/login handlers:

```python
response.set_cookie(
    key="deeptutor_session",
    value=session_secret,
    httponly=True,
    samesite="lax",
    secure=False,
)
```

- [ ] **Step 5: Mount the router in the API app**

Modify `deeptutor/api/main.py` router registration:

```python
from deeptutor.api.routers import auth

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
```

- [ ] **Step 6: Expand the auth router tests**

Add to `tests/api/test_auth_router.py`:

```python
def test_signup_sets_session_cookie_for_teacher() -> None:
    ...


def test_login_returns_current_user_payload() -> None:
    ...


def test_me_requires_valid_session_cookie() -> None:
    ...
```

- [ ] **Step 7: Run the backend auth API tests**

Run:

```bash
rtk pytest tests/api/test_auth_router.py -v
```

Expected:

- PASS

- [ ] **Step 8: Commit credential auth**

Run:

```bash
rtk git add deeptutor/services/auth/deps.py deeptutor/api/routers/auth.py deeptutor/api/main.py tests/api/test_auth_router.py
rtk git commit -m "feat(auth): add email password auth api [AUTH-MULTI-USER]"
```

### Task 5: Add Internal Admin Management And Session Ownership

**Files:**
- Create: `deeptutor/api/routers/admin_users.py`
- Modify: `deeptutor/api/routers/sessions.py`
- Modify: `deeptutor/services/session/sqlite_store.py`
- Create: `tests/api/test_admin_users_router.py`
- Create: `tests/services/session/test_owned_session_store.py`
- Create: `alembic/versions/20260502_0002_session_ownership.py`

- [ ] **Step 1: Write the failing ownership test**

Create `tests/services/session/test_owned_session_store.py`:

```python
def test_list_sessions_returns_only_rows_for_owner() -> None:
    store = OwnedSessionStore(...)
    teacher = "user_teacher"
    student = "user_student"
    store.create_session(owner_user_id=teacher, title="Teacher chat")
    store.create_session(owner_user_id=student, title="Student chat")

    sessions = store.list_sessions(owner_user_id=teacher)
    assert [session["title"] for session in sessions] == ["Teacher chat"]
```

- [ ] **Step 2: Run the failing ownership test**

Run:

```bash
rtk pytest tests/services/session/test_owned_session_store.py::test_list_sessions_returns_only_rows_for_owner -v
```

Expected:

- FAIL because there is no owned session store yet

- [ ] **Step 3: Add owner columns and ownership migration**

Create `alembic/versions/20260502_0002_session_ownership.py` with:

```python
def upgrade() -> None:
    op.add_column("sessions", sa.Column("owner_user_id", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_sessions_owner_user_id",
        "sessions",
        "users",
        ["owner_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
```

- [ ] **Step 4: Add owned-session filtering to the session store**

Extend `deeptutor/services/session/sqlite_store.py` with owner-aware signatures:

```python
async def create_session(self, title: str | None = None, session_id: str | None = None, owner_user_id: str | None = None) -> dict[str, Any]:
    ...


async def list_sessions(self, owner_user_id: str, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
    ...
```

Update SQL queries to add:

```sql
WHERE s.owner_user_id = ?
```

- [ ] **Step 5: Enforce ownership in the session API**

Modify `deeptutor/api/routers/sessions.py`:

```python
@router.get("")
async def list_sessions(current_user = Depends(get_current_user), limit: int = Query(default=50, ge=1, le=200), offset: int = Query(default=0, ge=0)):
    sessions = await store.list_sessions(owner_user_id=current_user.id, limit=limit, offset=offset)
    return {"sessions": sessions}
```

Use the same `current_user.id` filter in get/rename/delete calls.

- [ ] **Step 6: Add a minimal admin users router**

Create `deeptutor/api/routers/admin_users.py`:

```python
@router.get("/users")
def list_users(current_user = Depends(require_roles("admin"))):
    ...


@router.patch("/users/{user_id}")
def update_user(user_id: str, current_user = Depends(require_roles("admin"))):
    ...
```

- [ ] **Step 7: Run the session and admin tests**

Run:

```bash
rtk pytest tests/services/session/test_owned_session_store.py tests/api/test_admin_users_router.py tests/api/test_auth_router.py -v
```

Expected:

- PASS

- [ ] **Step 8: Commit ownership enforcement**

Run:

```bash
rtk git add deeptutor/api/routers/admin_users.py deeptutor/api/routers/sessions.py deeptutor/services/session/sqlite_store.py alembic/versions/20260502_0002_session_ownership.py tests/services/session/test_owned_session_store.py tests/api/test_admin_users_router.py
rtk git commit -m "feat(auth): add owned sessions and admin api [AUTH-MULTI-USER]"
```

### Task 6: Build The Public Auth Frontend

**Files:**
- Create: `web/lib/auth-api.ts`
- Create: `web/context/AuthContext.tsx`
- Create: `web/components/auth/AuthShell.tsx`
- Create: `web/components/auth/RolePicker.tsx`
- Create: `web/components/auth/SignupForm.tsx`
- Create: `web/components/auth/LoginForm.tsx`
- Create: `web/tests/auth-role-picker.test.tsx`
- Create: `web/tests/auth-signup-page.test.tsx`
- Create: `web/tests/auth-login-page.test.tsx`
- Modify: `web/package.json`
- Modify: `web/vitest.config.ts`
- Modify: `web/app/layout.tsx`

- [ ] **Step 1: Write the failing role-picker test**

Create `web/tests/auth-role-picker.test.tsx`:

```tsx
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import RolePicker from "../components/auth/RolePicker";

describe("RolePicker", () => {
  it("renders teacher and student options and reports the selected role", () => {
    const onSelect = vi.fn();
    render(<RolePicker selectedRole="teacher" onSelect={onSelect} />);

    fireEvent.click(screen.getByRole("button", { name: /học sinh/i }));
    expect(onSelect).toHaveBeenCalledWith("student");
  });
});
```

- [ ] **Step 2: Run the frontend test to confirm the auth component does not exist**

Run:

```bash
cd web && npx vitest run tests/auth-role-picker.test.tsx
```

Expected:

- FAIL because `components/auth/RolePicker` does not exist yet

- [ ] **Step 3: Add the auth client module**

Create `web/lib/auth-api.ts`:

```ts
export type PublicRole = "teacher" | "student";

export interface AuthUser {
  id: string;
  email: string;
  display_name: string;
  role: "teacher" | "student" | "admin";
}

export async function signup(payload: {
  display_name: string;
  email: string;
  password: string;
  role: PublicRole;
}) {
  ...
}
```

- [ ] **Step 4: Add the auth context**

Create `web/context/AuthContext.tsx`:

```tsx
export function AuthProvider({ children }: { children: React.ReactNode }) {
  ...
}

export function useAuth() {
  ...
}
```

Wire it into `web/app/layout.tsx`:

```tsx
<AppShellProvider>
  <I18nClientBridge>
    <AuthProvider>{children}</AuthProvider>
  </I18nClientBridge>
</AppShellProvider>
```

- [ ] **Step 5: Build the public auth components**

Create `web/components/auth/RolePicker.tsx`, `AuthShell.tsx`, `SignupForm.tsx`, and `LoginForm.tsx` with:

- two-card role selection
- role switching inside signup
- email/password fields
- Google CTA button

Use this role prop type:

```ts
type PublicRole = "teacher" | "student";
```

- [ ] **Step 6: Add the page-level tests**

Create `web/tests/auth-signup-page.test.tsx` and `web/tests/auth-login-page.test.tsx` with checks for:

- signup shows role picker and form
- signup can switch from teacher to student before submit
- login shows email/password and Google CTA

- [ ] **Step 7: Register the new tests**

Modify `web/vitest.config.ts` to include:

```ts
"tests/auth-role-picker.test.tsx",
"tests/auth-signup-page.test.tsx",
"tests/auth-login-page.test.tsx",
"tests/role-shell-routing.test.tsx",
```

- [ ] **Step 8: Run the auth frontend tests**

Run:

```bash
cd web && npx vitest run tests/auth-role-picker.test.tsx tests/auth-signup-page.test.tsx tests/auth-login-page.test.tsx
```

Expected:

- PASS

- [ ] **Step 9: Commit the public auth UI**

Run:

```bash
rtk git add web/lib/auth-api.ts web/context/AuthContext.tsx web/components/auth/AuthShell.tsx web/components/auth/RolePicker.tsx web/components/auth/SignupForm.tsx web/components/auth/LoginForm.tsx web/tests/auth-role-picker.test.tsx web/tests/auth-signup-page.test.tsx web/tests/auth-login-page.test.tsx web/app/layout.tsx web/vitest.config.ts
rtk git commit -m "feat(auth): add public auth frontend flows [AUTH-MULTI-USER]"
```

### Task 7: Add Role-Specific Routes And Guards

**Files:**
- Create: `web/components/auth/ProtectedRoute.tsx`
- Create: `web/app/login/page.tsx`
- Create: `web/app/signup/page.tsx`
- Create: `web/app/forgot-password/page.tsx`
- Create: `web/app/reset-password/page.tsx`
- Create: `web/app/verify-email/page.tsx`
- Create: `web/app/teacher/layout.tsx`
- Create: `web/app/teacher/page.tsx`
- Create: `web/app/student/layout.tsx`
- Create: `web/app/student/page.tsx`
- Create: `web/app/admin/layout.tsx`
- Create: `web/app/admin/page.tsx`
- Create: `web/tests/role-shell-routing.test.tsx`

- [ ] **Step 1: Write the failing role-shell routing test**

Create `web/tests/role-shell-routing.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import ProtectedRoute from "../components/auth/ProtectedRoute";

describe("ProtectedRoute", () => {
  it("blocks a student from a teacher-only surface", () => {
    render(
      <ProtectedRoute allow={["teacher"]} user={{ id: "1", email: "s@example.com", display_name: "Student", role: "student" }}>
        <div>Teacher shell</div>
      </ProtectedRoute>,
    );

    expect(screen.queryByText("Teacher shell")).toBeNull();
  });
});
```

- [ ] **Step 2: Run the failing route-guard test**

Run:

```bash
cd web && npx vitest run tests/role-shell-routing.test.tsx
```

Expected:

- FAIL because `ProtectedRoute` does not exist yet

- [ ] **Step 3: Build the protected route component**

Create `web/components/auth/ProtectedRoute.tsx`:

```tsx
export default function ProtectedRoute({
  allow,
  user,
  children,
}: {
  allow: Array<"teacher" | "student" | "admin">;
  user: { role: "teacher" | "student" | "admin" } | null;
  children: React.ReactNode;
}) {
  if (!user) return null;
  if (!allow.includes(user.role)) return null;
  return <>{children}</>;
}
```

- [ ] **Step 4: Add the public auth pages**

Create:

- `web/app/login/page.tsx`
- `web/app/signup/page.tsx`
- `web/app/forgot-password/page.tsx`
- `web/app/reset-password/page.tsx`
- `web/app/verify-email/page.tsx`

Each page should wrap the relevant form in:

```tsx
<AuthShell eyebrow="DeepTutor" title="Đăng nhập / Sign in">
  <LoginForm />
</AuthShell>
```

- [ ] **Step 5: Add separate role shells**

Create:

- `web/app/teacher/layout.tsx`
- `web/app/student/layout.tsx`
- `web/app/admin/layout.tsx`

Use `ProtectedRoute` in each shell and make the landing pages visibly different:

```tsx
export default function TeacherHomePage() {
  return <main><h1>Teacher workspace</h1></main>;
}
```

```tsx
export default function StudentHomePage() {
  return <main><h1>Student workspace</h1></main>;
}
```

- [ ] **Step 6: Run the route tests**

Run:

```bash
cd web && npx vitest run tests/role-shell-routing.test.tsx tests/auth-role-picker.test.tsx tests/auth-signup-page.test.tsx tests/auth-login-page.test.tsx
```

Expected:

- PASS

- [ ] **Step 7: Commit the role shells**

Run:

```bash
rtk git add web/components/auth/ProtectedRoute.tsx web/app/login/page.tsx web/app/signup/page.tsx web/app/forgot-password/page.tsx web/app/reset-password/page.tsx web/app/verify-email/page.tsx web/app/teacher/layout.tsx web/app/teacher/page.tsx web/app/student/layout.tsx web/app/student/page.tsx web/app/admin/layout.tsx web/app/admin/page.tsx web/tests/role-shell-routing.test.tsx
rtk git commit -m "feat(auth): add role specific product shells [AUTH-MULTI-USER]"
```

### Task 8: Add Google Login And Recovery Flows

**Files:**
- Create: `deeptutor/services/auth/google_oauth.py`
- Modify: `deeptutor/api/routers/auth.py`
- Modify: `deeptutor/services/auth/service.py`
- Modify: `tests/api/test_auth_router.py`

- [ ] **Step 1: Write the failing Google flow test**

Add to `tests/api/test_auth_router.py`:

```python
def test_google_start_redirects_to_provider() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/auth/google/start", allow_redirects=False)
    assert response.status_code in {302, 307}
```

- [ ] **Step 2: Run the targeted test**

Run:

```bash
rtk pytest tests/api/test_auth_router.py::test_google_start_redirects_to_provider -v
```

Expected:

- FAIL because the Google route does not exist yet

- [ ] **Step 3: Implement the Google helper**

Create `deeptutor/services/auth/google_oauth.py`:

```python
class GoogleOAuthSettings(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str
```

Use Authlib to:

- build provider redirect URL
- exchange callback code for identity claims

- [ ] **Step 4: Add the auth routes**

Add to `deeptutor/api/routers/auth.py`:

```python
@router.get("/google/start")
async def google_start():
    ...


@router.get("/google/callback")
async def google_callback(request: Request, response: Response):
    ...
```

Also add:

- `POST /forgot-password`
- `POST /reset-password`
- `POST /verify-email`

- [ ] **Step 5: Extend the auth service**

Add service methods:

```python
def link_google_identity(...):
    ...


def issue_password_reset(...):
    ...


def consume_password_reset(...):
    ...
```

- [ ] **Step 6: Run the auth router test suite**

Run:

```bash
rtk pytest tests/api/test_auth_router.py -v
```

Expected:

- PASS

- [ ] **Step 7: Commit OAuth and recovery**

Run:

```bash
rtk git add deeptutor/services/auth/google_oauth.py deeptutor/api/routers/auth.py deeptutor/services/auth/service.py tests/api/test_auth_router.py
rtk git commit -m "feat(auth): add google login and recovery flows [AUTH-MULTI-USER]"
```

### Task 9: Final Validation And Documentation

**Files:**
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- Modify: `ai_first/daily/2026-05-02.md`
- Create: `docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md`

- [ ] **Step 1: Update the system map**

Add the new auth and role-entry surfaces to `ai_first/architecture/MAIN_SYSTEM_MAP.md` with:

- public auth routes
- auth service layer
- PostgreSQL identity store
- teacher/student/admin shells

- [ ] **Step 2: Write the PR architecture note**

Create `docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md` with:

```md
# PR Note: Auth And Multi-User Foundation

```mermaid
flowchart LR
  Public[Public Auth Routes] --> API[FastAPI Auth Router]
  API --> PG[(PostgreSQL)]
  API --> Teacher[Teacher Shell]
  API --> Student[Student Shell]
  API --> Admin[Admin Shell]
  API --> Sessions[Owned Learning Sessions]
```
```

- [ ] **Step 3: Run the required backend tests**

Run:

```bash
rtk pytest tests/services/auth tests/api/test_auth_router.py tests/api/test_admin_users_router.py tests/services/session/test_owned_session_store.py -v
```

Expected:

- PASS

- [ ] **Step 4: Run the required frontend tests**

Run:

```bash
cd web && npx vitest run tests/auth-role-picker.test.tsx tests/auth-signup-page.test.tsx tests/auth-login-page.test.tsx tests/role-shell-routing.test.tsx
```

Expected:

- PASS

- [ ] **Step 5: Run the build and diff checks**

Run:

```bash
cd web && npm run build
rtk git diff --check
```

Expected:

- `next build` passes
- diff check is clean

- [ ] **Step 6: Update the daily log with the final validation record**

Append:

```md
- Done: Added backend-owned auth, role-aware shells, and owned session boundaries for the first production multi-user slice.
- Tests: `pytest tests/services/auth tests/api/test_auth_router.py tests/api/test_admin_users_router.py tests/services/session/test_owned_session_store.py -v`; `cd web && npx vitest run tests/auth-role-picker.test.tsx tests/auth-signup-page.test.tsx tests/auth-login-page.test.tsx tests/role-shell-routing.test.tsx`; `cd web && npm run build`; `git diff --check`
```

- [ ] **Step 7: Commit docs and handoff**

Run:

```bash
rtk git add ai_first/architecture/MAIN_SYSTEM_MAP.md ai_first/daily/2026-05-02.md docs/superpowers/pr-notes/2026-05-02-auth-multi-user-foundation.md
rtk git commit -m "docs(auth): record multi-user foundation architecture [AUTH-MULTI-USER]"
```

## Self-Review

- Spec coverage:
  - public signup/login: covered in Tasks 4, 6, and 7
  - teacher/student/admin role model: covered in Tasks 3, 4, 5, and 7
  - admin not self-signup: covered in Task 4 and enforced in tests
  - PostgreSQL foundation: covered in Task 2
  - Google login: covered in Task 8
  - session ownership: covered in Task 5
  - role-specific shells: covered in Task 7
- Placeholder scan:
  - no `TODO`, `TBD`, or deferred-code placeholders remain
- Type consistency:
  - public roles remain `teacher | student`
  - protected roles remain `teacher | student | admin`
  - auth cookie name remains `deeptutor_session`

