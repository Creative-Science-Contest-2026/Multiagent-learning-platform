# Executive summary

Branch reviewed: `fix/auth-multi-user-foundation` against `origin/main`.

This lane is materially stronger now than at the start of the review. I found two production-impacting issues in the auth/session foundation and fixed both in-review:

1. `High`: Google OAuth callback trusted caller-supplied `state` without any browser-bound nonce, which allowed login CSRF.
2. `High`: legacy JSON session managers still enforced `MAX_SESSIONS` globally, so one authenticated owner could evict another owner's older chat/solve sessions.

After fixing those issues and rerunning the targeted regression suite, I do not see an open blocker inside the branch scope reviewed here. Residual risk is now mostly around breadth: the branch touches many surfaces, so confidence is highest in the auth/session boundaries and lower in presentation-only files not materially changed in this review pass.

# Change summary

- Reviewed diff scope with emphasis on:
  - `deeptutor/api/routers/auth.py`
  - `deeptutor/services/auth/*`
  - `deeptutor/services/session/base_session_manager.py`
  - auth/session regression tests
- Fixed in-review:
  - browser-bound nonce cookie for Google OAuth start/callback
  - owner-scoped trimming for legacy shared JSON session files
- Added regression coverage:
  - Google callback rejects forged or missing state cookie
  - legacy session trimming preserves other owners' sessions

Reviewed files and confidence:

| File | Review confidence | Notes |
| --- | --- | --- |
| `deeptutor/api/routers/auth.py` | 9/10 | Critical auth entrypoint; reread end-to-end with callback/state flow and delivery behavior in mind. |
| `deeptutor/services/auth/service.py` | 8/10 | Identity/session lifecycle reviewed closely; no new blocker found after second pass. |
| `deeptutor/services/session/base_session_manager.py` | 9/10 | Small but high-risk ownership boundary; behavior fix is straightforward and covered by new test. |
| `tests/api/test_auth_router.py` | 9/10 | Good coverage for auth entry flow after adding nonce-cookie checks. |
| `tests/services/session/test_base_session_manager.py` | 8/10 | New focused regression test; enough for the owner-trimming contract. |

Watchouts outside the high-risk reread set:

- `⚠️ web/app/**` and `web/components/auth/**`: not reread line-by-line in this pass because this review focused on backend auth/session correctness rather than presentation polish.
- `⚠️ deeptutor/api/routers/*` outside the auth/session cluster: already regression-tested, but this pass did not reopen every router in the branch for a fresh manual reread.

# Detailed findings

## Fixed in review

### High
- File: `deeptutor/api/routers/auth.py`
- Area: Google OAuth start/callback state handling
- Problem: the callback accepted JSON `state` from the query string and used it for role/redirect decisions without proving that the browser initiating the callback was the same browser that started the OAuth flow. That is a login CSRF vector: an attacker can complete Google auth for their own account and force a victim browser onto the callback URL, causing the victim to be logged into the attacker-controlled account.
- Fix direction: issue a nonce at `/google/start`, persist it in an HttpOnly cookie, include it in `state`, and require an exact nonce match in `/google/callback` before session creation. Clear the cookie after successful callback.
- Status: fixed in branch.

### High
- File: `deeptutor/services/session/base_session_manager.py`
- Area: shared legacy chat/solve session retention
- Problem: once legacy sessions became owner-aware, the old `MAX_SESSIONS` truncation still sliced the global shared list. That meant one teacher or student creating many legacy sessions could evict another owner's older sessions even though list/get/delete were already owner-filtered.
- Fix direction: trim only the current owner's session subset while preserving unrelated owners' records in the same shared JSON file.
- Status: fixed in branch.

## Open findings

No new open `Critical` or `High` blocker remains from this review pass.

# Suggested fixes

- Keep the Google OAuth nonce cookie contract as part of the permanent auth surface. Future changes to `/google/start` or `/google/callback` should treat the nonce check as non-optional.
- Preserve the owner-scoped session trimming rule if legacy JSON stores survive future migrations; otherwise the same cross-owner eviction bug will reappear.
- If a later pass reopens branch-wide review, prioritize:
  - password-reset / verification token invalidation policy
  - student access to non-teacher utility APIs that still intentionally expose read-only config
  - cleanup of dead helper paths such as the unused `_stream_react_edit()` placeholder

# Recommended test cases

- Google callback with:
  - valid nonce cookie
  - missing nonce cookie
  - mismatched nonce cookie
- Multiple legacy owners creating more than `MAX_SESSIONS` entries in the same shared session file.
- Regression suite for:
  - auth routers
  - legacy chat/solve routers
  - unified websocket ownership
  - auth UI shells and build

# Final verdict

Result: `Pass after fixes`.

Commands actually run during this review:

```bash
git fetch origin main
git branch --show-current
git diff --name-only origin/main...HEAD
git diff --stat origin/main...HEAD
python -m pytest tests/api/test_auth_router.py tests/services/session/test_base_session_manager.py -q
python -m pytest tests/services/auth tests/services/session/test_base_session_manager.py tests/services/session/test_owned_session_store.py tests/services/session/test_sqlite_store.py tests/api/test_auth_router.py tests/api/test_chat_router.py tests/api/test_solve_router.py tests/api/test_unified_ws_turn_runtime.py tests/api/test_memory_router.py tests/api/test_dashboard_router.py tests/api/test_marketplace_router.py tests/api/test_knowledge_router.py tests/api/test_assessment_router.py tests/api/test_guide_router.py tests/api/test_tutorbot_router.py tests/api/test_notebook_router.py tests/api/test_settings_router.py tests/api/test_agent_specs_router.py tests/api/test_question_router.py tests/api/test_co_writer_router.py tests/api/test_system_router.py tests/api/test_vision_solver_router.py tests/api/test_plugins_api_router.py tests/api/test_agent_config_router.py tests/api/test_admin_users_router.py tests/api/test_session_review_router.py -q
cd web && node node_modules/vitest/vitest.mjs run tests/auth-login-page.test.tsx tests/auth-role-picker.test.tsx tests/auth-signup-page.test.tsx tests/role-shell-routing.test.tsx tests/auth-recovery-pages.test.tsx tests/auth-verify-page.test.tsx tests/auth-teacher-surface-gate.test.tsx tests/auth-shell-layout-source.test.ts tests/auth-admin-page.test.tsx tests/auth-role-hubs.test.tsx tests/auth-signed-in-account-bar.test.tsx tests/auth-email-verification-banner.test.tsx
cd web && npm run build
git diff --check
```

Observed status:

- backend regression suite: pass
- frontend auth vitest suite: pass
- `web` production build: pass
- `git diff --check`: pass
