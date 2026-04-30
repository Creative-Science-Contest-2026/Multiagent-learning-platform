# 2026-04-30 Settings Hide Runtime Config

- Task ID: `UI_SETTINGS_HIDE_RUNTIME_CONFIG`
- Commit tag: `UI-SETTINGS-HIDE`
- Branch: `fix/settings-hide-runtime-config`
- Worktree: `.worktrees/fix-settings-hide-runtime-config`
- Status: `implemented`

## Goal

Hide all end-user runtime configuration for LLM, embedding, and search from the `Cài đặt` screen, and keep the actual runtime credentials in the local backend `.env` file instead of the user-facing settings UI.

## User-visible outcome

- End users only see personal preferences on `/settings`, not provider, endpoint, model, or API key fields.
- The app still boots with the intended OpenAI LLM and embedding configuration because those values live in `.env`.
- No runtime secret is introduced into tracked files, docs, or PR notes.

## Owned files

- `web/app/(utility)/settings/page.tsx`
- `web/tests/settings-page-runtime-privacy.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-settings-hide-runtime-config.md`
- `docs/superpowers/specs/2026-04-30-settings-hide-runtime-config-design.md`
- `docs/superpowers/plans/2026-04-30-settings-hide-runtime-config.md`
- `docs/superpowers/pr-notes/2026-04-30-settings-hide-runtime-config.md`
- local-only `.env` at repo root (not tracked, do not mention secrets in tracked files)

## Do-not-touch

- `deeptutor/api/routers/settings.py`
- `deeptutor/services/config/**`
- tracked example env files
- lockfiles and generated files

## Required code reading

- `web/app/(utility)/settings/page.tsx`
- `deeptutor/api/routers/settings.py`
- `deeptutor/services/config/env_store.py`
- `deeptutor/services/config/model_catalog.py`
- `tests/api/test_settings_router.py`

## Design before implementation

### Current behavior

- `/settings` exposes service tabs and full profile/model editors for `llm`, `embedding`, and `search`.
- The page lets an end user see and edit provider names, base URLs, API keys, dimensions, diagnostics, and apply actions.
- Backend configuration already supports reading the active runtime from the local `.env` file.

### Intended behavior change

- `/settings` should become an end-user preference screen only.
- Runtime service configuration should no longer be visible or editable from the browser UI.
- The backend should continue to read the configured LLM and embedding settings from `.env`.

### Candidate approaches

1. **Hide only the tab strip**
   - Pros: smallest diff.
   - Cons: still leaves apply buttons, runtime badges, diagnostics, and sensitive fields reachable.

2. **Collapse `/settings` into a preference-only page and keep runtime config backend-only**
   - Pros: matches the security goal, keeps backend contract unchanged, and uses the already-supported `.env` path.
   - Cons: removes in-browser runtime editing completely for end users.

3. **Add a role-based admin mode**
   - Pros: best long-term access control.
   - Cons: much wider scope because the repo does not currently expose a bounded admin permission layer here.

### Chosen approach

- Use **Approach 2**.
- Keep backend settings APIs intact for now, but remove the runtime configuration surface from the end-user route.
- Store the requested OpenAI LLM and embedding settings only in the ignored `.env` file.

### Expected impact surface

- Likely change:
  - `web/app/(utility)/settings/page.tsx`
  - a focused source-structure test for the settings privacy shell
  - local root `.env`
- Reviewed but expected unchanged:
  - settings router and env rendering services
  - tracked `.env.example` files
  - other utility routes

### Validation paths

- `/settings` no longer renders `LLM`, `EMBEDDING`, `SEARCH`, `Save Draft`, `Apply`, or diagnostics controls.
- The local `.env` contains the intended LLM and embedding keys.
- No secret appears in tracked git diff output.

## Acceptance criteria

- End users cannot inspect or edit runtime service configuration from `/settings`.
- The requested LLM and embedding configuration exists in local `.env` only.
- The implementation does not commit or document secrets.

## Implementation notes

- Replaced the existing settings shell with a preference-only page that keeps `Theme` and `Language` controls but removes runtime badges, service tabs, profile editors, diagnostics, and apply/test actions from the source.
- Added `web/tests/settings-page-runtime-privacy.test.ts` to lock the page shell against regressions that would reintroduce runtime editor affordances.
- Created a local-only `.env` in the worktree root with the requested OpenAI LLM and embedding values so backend runtime stays configured without exposing secrets in tracked files.

## Verification

- Passed: `cd web && node --test tests/settings-page-runtime-privacy.test.ts`
- Could not run: `cd web && npx eslint 'app/(utility)/settings/page.tsx'`
  - blocker: this worktree cannot resolve `eslint-config-next` from `web/eslint.config.mjs`
