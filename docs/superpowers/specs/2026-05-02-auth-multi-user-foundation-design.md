# Auth And Multi-User Foundation

- Date: 2026-05-02
- Task ID: `AUTH_MULTI_USER_FOUNDATION`
- Branch: `docs/auth-multi-user-foundation-design`

## Goal

Turn the current single-operator, anonymous-session contest product into a real multi-user product with:

- public signup and login
- email/password auth
- Google login
- role-aware product entry
- separate teacher and student product shells
- internal-only admin creation
- PostgreSQL-backed user and session ownership

This work is not a cosmetic auth overlay. It is the foundation required to stop the product from behaving like a local prototype and start behaving like a real education platform.

## Current Behavior

### Product state

- The web product currently assumes an anonymous operator.
- There is no signup flow.
- There is no login flow.
- There is no current-user concept in the web app.
- There is no route guard by role.
- There is no teacher shell versus student shell split.

### Session and data state

- Unified chat sessions already exist, but they are anonymous and stored in SQLite under the local runtime data directory.
- The existing session store is centered on one shared SQLite database at `data/user/chat_history.db`.
- Session APIs expose and mutate session history without any account ownership boundary.

### Codebase evidence

- `deeptutor/services/session/sqlite_store.py`
  - defines the current SQLite session store and shared `sessions`, `messages`, `turns`, `turn_events`, and evidence-related tables
- `deeptutor/api/routers/sessions.py`
  - exposes list/get/rename/delete session endpoints without user authentication
- `web/lib/session-api.ts`
  - fetches sessions directly from `/api/v1/sessions`
- `web/components/SessionList.tsx`
  - renders a single shared session list with no user identity boundary
- `web/app/(workspace)/layout.tsx`
  - provides one workspace shell
- `web/app/(utility)/layout.tsx`
  - provides one utility shell

Conclusion:

- the repo already has multi-conversation support
- it does not yet have multi-user product support

## User-Approved Product Decisions

- This is no longer a demo-only direction. The target is a real product foundation.
- Public signup is allowed.
- Public login is allowed.
- Supported public roles:
  - `teacher`
  - `student`
- Internal-only role:
  - `admin`
- `admin` must not be selectable from public signup.
- Signup and login support both:
  - email + password
  - Google
- Before entering the signup form, the user should see a role-selection surface with two clear choices:
  - `Giáo viên`
  - `Học sinh`
- The role may still be changed inside the signup flow before submission.
- Users do not need to join a school, organization, or class during initial signup.
- Teacher and student should enter clearly different product spaces after login.
- The data layer should move to PostgreSQL for real multi-user support.

## Codebase Survey

### Backend entry and middleware layer

- `deeptutor/api/main.py`
  - owns the FastAPI app, middleware, CORS, static mounting, and router registration
  - currently has no auth middleware, no identity dependency layer, and permissive `allow_origins=["*"]`

Conclusion:

- backend auth should be introduced here through new auth routers, auth dependencies, and tighter production-oriented session handling

### Existing storage model

- `deeptutor/services/session/sqlite_store.py`
  - manages conversation/session persistence today
- `deeptutor/services/path_service.py`
  - roots runtime state in local `data/user/`

Conclusion:

- the current storage model is explicitly local-runtime oriented
- a real multi-user product cannot keep user identity and ownership anchored to one anonymous local SQLite file

### Existing frontend route architecture

- `web/app/layout.tsx`
  - root layout with fonts, theme, and app-level providers
- `web/app/(workspace)/**`
  - current interactive workspace routes
- `web/app/(utility)/**`
  - current utility routes
- `web/app/introduce/page.tsx`
  - existing public standalone route pattern

Conclusion:

- the app already supports standalone public routes outside the internal shells
- new public auth routes can live directly under `web/app/`
- teacher and student shells should not be bolted into the existing generic workspace without role separation

### Existing dependency situation

- `pyproject.toml`
  - includes FastAPI and runtime server dependencies, but no production-grade auth/ORM stack is wired in today
- `web/package.json`
  - includes Next.js and UI dependencies, but no auth framework is currently installed

Conclusion:

- the repo does not yet have an existing auth framework that should be preserved
- we can choose a clean backend-owned auth approach without fighting an incumbent identity stack

### Parallel-lane constraint

- `ai_first/ACTIVE_ASSIGNMENTS.md` currently lists `fix/frontend-test-coverage-gate` with ownership over `web/**`

Conclusion:

- implementation cannot begin in `web/**` until ownership is explicitly decomposed or that lane clears
- this spec is still valid and should define the future runtime lane cleanly

## Candidate Approaches

### Approach A: Next.js-owned auth with backend trust bridge

- Next.js handles login/signup/session state.
- FastAPI trusts forwarded identity from the frontend.

Pros:

- fast to get public auth screens working
- many ready-made frontend patterns exist

Cons:

- splits authority between frontend auth state and backend data ownership
- complicates role enforcement for API routes
- makes chat/session/evidence ownership harder to reason about
- increases the chance of another prototype-grade integration

### Approach B: FastAPI-owned auth and identity, Next.js as client

- FastAPI owns users, credentials, OAuth identities, sessions, and authorization.
- Next.js consumes auth/session APIs and renders role-specific UX.

Pros:

- one source of truth for identity and authorization
- naturally fits the existing backend-heavy product architecture
- easiest path to secure ownership for sessions, learning evidence, and future class data
- best long-term fit for teacher/student/admin separation

Cons:

- larger backend change
- requires proper migration and route-guard design

### Approach C: Managed auth provider first, internal domain later

- Use an external auth platform for signup/login and map users into the product later.

Pros:

- fast initial UI and OAuth

Cons:

- introduces platform coupling before the product core is stable
- still leaves ownership mapping and authorization integration unfinished
- weak fit for the current repo architecture

## Chosen Approach

Approach B.

This keeps identity, role, and resource ownership in one authoritative backend domain. That is the cleanest path from anonymous prototype to real product.

## Proposed Product Architecture

### Public routes

Add public, standalone routes outside the current workspace/utility shells:

- `/`
  - product entry and role-aware CTA
- `/signup`
  - signup flow with role preselection and in-form role switching
- `/login`
  - email/password login and Google login
- `/forgot-password`
  - password reset request
- `/reset-password`
  - password reset completion
- `/verify-email`
  - email verification completion or status

These routes should use a dedicated public auth layout rather than the current internal shell.

### Role-specific product entry

After authentication:

- `teacher` -> `/teacher`
- `student` -> `/student`
- `admin` -> `/admin`

The product must not keep one generic post-login shell and merely hide tabs by role. Teacher and student should feel like different products with different goals and navigation.

### Signup flow

#### Step 1: role choice

- show two large cards before the form:
  - `Giáo viên`
  - `Học sinh`
- store the selected role as draft auth state

#### Step 2: account creation

- allow:
  - full name
  - email
  - password
  - Google signup
- allow switching role inside the form before submission
- do not expose `admin`
- school / organization / class fields are optional or omitted in the first release

### Login flow

- email + password
- Google login
- forgot password entry point
- redirect authenticated users to the route for their role

### Admin flow

- admin is not self-service
- admin accounts are created by:
  - a backend management command, or
  - an internal-only admin bootstrap path

The public signup UI must not contain any path that creates an admin.

## Identity And Session Model

Separate two concepts clearly:

### 1. Auth sessions

These represent logged-in browser/device sessions.

Responsibilities:

- track login state
- support logout
- support refresh or renewal
- provide current user identity to API requests

### 2. Learning sessions

These are product-domain sessions such as:

- chat sessions
- assessment sessions
- tutoring history
- future class-bound work

Responsibilities:

- hold conversation and learning records
- belong to a specific user
- later support teacher-owned versus student-owned workflows

This distinction is mandatory. Reusing the current anonymous chat session concept as the authentication session would be a category error.

## Proposed Backend Domain Model

### Core identity tables

- `users`
  - `id`
  - `email`
  - `display_name`
  - `role`
  - `status`
  - `email_verified_at`
  - `created_at`
  - `updated_at`
- `user_password_credentials`
  - `user_id`
  - `password_hash`
  - `password_updated_at`
- `user_oauth_identities`
  - `id`
  - `user_id`
  - `provider`
  - `provider_subject`
  - `email_at_link_time`
  - `created_at`
- `auth_sessions`
  - `id`
  - `user_id`
  - `refresh_token_hash` or equivalent session secret
  - `user_agent`
  - `ip_address`
  - `expires_at`
  - `revoked_at`
  - `created_at`
  - `last_seen_at`
- `email_verification_tokens`
- `password_reset_tokens`

### User role enum

- `teacher`
- `student`
- `admin`

### Learning/session ownership changes

The current anonymous session tables should evolve so that:

- every session has `owner_user_id`
- every message and turn remains attached through its parent session
- teacher-owned and student-owned data can later be queried safely without global mixing

At minimum, the following existing concepts need ownership review:

- `sessions`
- `messages`
- `turns`
- `turn_events`
- `observations`
- `student_states`

Some of these may remain domain-specific rather than directly user-owned, but the implementation lane must explicitly model who owns them and who may read them.

## Persistence Strategy

### Database

- move auth and user-backed product state to PostgreSQL
- do not keep production user identity on the existing local SQLite path

### Migration strategy

Use a staged migration rather than a risky big-bang rewrite:

#### Phase 1

- introduce PostgreSQL connection layer
- introduce user/auth tables
- keep existing anonymous SQLite learning sessions untouched
- gate authenticated users into the new auth flow

#### Phase 2

- introduce PostgreSQL-backed owned learning sessions
- migrate session APIs from anonymous global store to user-owned store
- add ownership filtering to session list/get/update/delete operations

#### Phase 3

- migrate or retire remaining SQLite-only session/evidence paths
- narrow SQLite to local development fallback only, if retained at all

This phased approach reduces blast radius and lets the product become multi-user before every historical contest path is rewritten.

## Auth Transport And Security

### Chosen direction

- backend-issued auth session
- browser receives secure session credentials via `HttpOnly` cookies
- frontend fetches `/me` or equivalent identity endpoint to hydrate app state

### Security requirements

- hash passwords using a production-grade password hashing algorithm
- do not store raw refresh tokens
- require email verification for newly registered email/password users unless an explicit onboarding exception is approved
- support logout by revoking the server-side auth session
- use role checks on protected API routes
- do not expose admin creation in public flows

### Google login

- support Google as an OAuth identity provider
- link or create the local user record on first successful OAuth login
- keep the local role explicit in our own user table

The Google account must not be treated as the whole identity model; it is only one login method.

## Frontend Information Architecture

### Public auth layer

Add a public auth UI system with:

- role selection card pair
- signup form
- login form
- OAuth CTA
- password reset flow
- email verification status

This UI should feel company-grade and product-grade, not like a bare internal admin form.

### Teacher shell

Teacher routes should center on:

- knowledge packs
- assessments
- tutor setup
- dashboard and diagnosis
- intervention actions

### Student shell

Student routes should center on:

- assigned or chosen learning entry points
- tutoring
- assessments
- personal progress

### Admin shell

Admin can begin as a minimal internal surface:

- user list
- role/status management
- account disable or recovery actions

It does not need full school-management scope in the first release.

## API Surface Changes

Add new backend surface, likely under `/api/v1/auth` and `/api/v1/admin`.

Expected auth endpoints:

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`
- `POST /api/v1/auth/verify-email`
- `GET /api/v1/auth/google/start`
- `GET /api/v1/auth/google/callback`

Expected admin endpoints:

- `GET /api/v1/admin/users`
- `PATCH /api/v1/admin/users/{user_id}`
- optional internal bootstrap endpoint or command for first admin creation

Existing session and product endpoints must gain auth/role checks incrementally.

## Route Protection Model

### Public-only routes

- `/`
- `/introduce`
- `/login`
- `/signup`
- `/forgot-password`
- `/reset-password`
- `/verify-email`

### Authenticated role-gated routes

- `/teacher/**` for `teacher`
- `/student/**` for `student`
- `/admin/**` for `admin`

### Transitional handling

Legacy internal routes under the current shells may need:

- redirect to the correct role shell when authenticated
- block anonymous access
- eventually be refactored or retired

The implementation lane must explicitly decide which current routes are:

- migrated
- aliased
- redirected
- deprecated

## Testing Strategy

### Backend tests

Add or update tests for:

- signup success and validation failure
- login success and failure
- Google callback account creation/linking
- public signup role restrictions
- admin non-self-signup enforcement
- `/me` identity resolution
- logout and revoked-session behavior
- route guards by role
- session list ownership filtering

### Frontend tests

Add or update tests for:

- role selection before signup
- role switching inside signup form
- login form behavior
- post-login redirects by role
- teacher shell guard
- student shell guard
- admin shell guard

### Integration checks

- authenticated browser session bootstrap
- teacher cannot enter student-only route if disallowed
- student cannot enter teacher-only route
- anonymous users cannot access protected routes

## Impact Surface

### Files or modules expected to change in the future runtime lane

- `deeptutor/api/main.py`
- new auth routers under `deeptutor/api/routers/`
- new auth/service modules under `deeptutor/services/`
- current session persistence modules under `deeptutor/services/session/`
- `web/app/layout.tsx`
- new public auth routes under `web/app/`
- new role shells under `web/app/teacher/`, `web/app/student/`, `web/app/admin/`
- auth/session client modules under `web/lib/`
- route guards, identity context, and shell navigation components

### Files reviewed now but expected to remain unchanged until implementation proves otherwise

- `web/app/introduce/page.tsx`
- most contest submission docs under `docs/contest/`
- evidence and screenshot assets

## Out Of Scope For The First Runtime Lane

- school or organization onboarding during signup
- class invitation and join-code flows
- billing
- deep admin analytics
- parent accounts
- SSO beyond Google
- full migration of every historical contest path in one PR

## Main Risks

### Risk 1: Fake auth over anonymous data

If the implementation adds login screens but keeps learning data globally shared underneath, the result will still be a prototype.

Mitigation:

- require explicit ownership mapping for every session-related surface touched in the first runtime lane

### Risk 2: Split authority between frontend and backend

If auth lives mostly in Next.js while ownership lives in FastAPI, bugs and security drift will follow.

Mitigation:

- keep backend as the identity authority

### Risk 3: Trying to migrate the whole product in one pass

A total rewrite of every route and session path will slow the project and increase regression risk.

Mitigation:

- use staged migration with bounded runtime lanes

## Recommended Execution Order

1. Add auth domain and PostgreSQL plumbing.
2. Add public signup/login and `/me`.
3. Add role-aware post-login redirects.
4. Add teacher/student/admin shells.
5. Move session ownership onto authenticated users.
6. Migrate legacy routes and tighten role guards.

## Implementation Constraint For The Next Lane

The next runtime lane must not start editing `web/**` from this checkout until the active `fix/frontend-test-coverage-gate` ownership is resolved or decomposed. The implementation plan should therefore either:

- claim a narrower `web/auth/**` + specific route scope with explicit approval, or
- wait until the current `web/**` lane clears.
