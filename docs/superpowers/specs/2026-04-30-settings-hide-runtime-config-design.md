# Settings Hide Runtime Config Design

## Summary

Turn `/settings` into a bounded end-user preferences page and remove the browser-visible runtime service editor. Persist the requested OpenAI LLM and embedding values in the ignored root `.env` file so backend runtime stays configured without exposing provider or credential details to end users.

## Current behavior

- `web/app/(utility)/settings/page.tsx` renders theme/language controls plus runtime status badges, service tabs, profile/model editors, diagnostics, and apply/test actions.
- The page reveals base URLs, API keys, model IDs, dimensions, and provider labels.
- Backend settings code already supports loading and applying the active configuration from `.env` via `EnvStore`.

## Intended behavior

- Keep only user-safe preferences on `/settings`.
- Remove all end-user UI access to runtime configuration.
- Maintain runtime config through local `.env` values:
  - `LLM_BINDING=openai`
  - `LLM_MODEL=gpt-4.1`
  - `LLM_API_KEY=<provided secret>`
  - `LLM_HOST=https://api.openai.com/v1`
  - `LLM_API_VERSION=`
  - `EMBEDDING_BINDING=openai`
  - `EMBEDDING_MODEL=text-embedding-3-small`
  - `EMBEDDING_API_KEY=<provided secret>`
  - `EMBEDDING_HOST=https://api.openai.com/v1/embeddings`
  - `EMBEDDING_DIMENSION=1536`
  - `EMBEDDING_API_VERSION=`

## Architecture decision

- Leave backend settings router and env rendering unchanged.
- Implement privacy at the page-shell layer only: do not render runtime status, service tabs, profile editors, apply buttons, diagnostics, or tour relaunch on the end-user settings page.
- Keep `.env` local and ignored; do not mirror secrets into tracked task/spec/PR documents.

## Files

- Modify `web/app/(utility)/settings/page.tsx`
  - reduce the page to preferences-only UI
  - remove or gate the runtime configuration sections from render output
- Create `web/tests/settings-page-runtime-privacy.test.ts`
  - source-structure test that asserts the hidden runtime editor affordances are absent from the rendered settings shell source
- Update local `.env`
  - set the requested LLM and embedding variables without committing the file
- Update task/daily/pr-note artifacts

## Risks and controls

- Risk: hiding too much and losing language/theme preferences.
  - Control: keep the top preference controls and page title unchanged.
- Risk: runtime stops working if `.env` keys are wrong.
  - Control: use the exact env keys consumed by `EnvStore` and existing settings router tests.
- Risk: secrets leak into git.
  - Control: do not place secrets in tracked files, logs, or final summary; verify `.env` stays untracked.

## Validation

- Source test for the settings shell passes.
- Relevant frontend lint/build passes.
- `git status --short` shows no tracked secret file changes.
