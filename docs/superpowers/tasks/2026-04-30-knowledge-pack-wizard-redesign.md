# Task Packet: Knowledge Pack Wizard Redesign

- Task ID: `UI_KNOWLEDGE_PACK_WIZARD_REDESIGN`
- Date: 2026-04-30
- Branch: `fix/knowledge-pack-wizard-redesign`
- Status: Implemented, pending PR

## Objective

Redesign the `Gói kiến thức` screen into a Vietnamese-first wizard with `Thông tin -> Tài liệu -> Hoàn tất`, hide notebooks and model/provider selection from FE, and route indexing through a default OpenAI-backed path.

## User-Approved Scope

- replace the current top create/upload layout with a wizard
- remove `Notebooks` from FE on this screen
- hide provider/model selection from end users
- redefine `Grade/Cấp độ` as `Mức độ khó`
- support file upload only in this version
- show overall and per-file indexing status in the completion step

## Owned Files

- `web/app/(utility)/knowledge/page.tsx`
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- `web/lib/notebook-api.ts`
- `web/tests/contest-vietnamese-coverage.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-knowledge-pack-wizard-redesign.md`
- `docs/superpowers/specs/2026-04-30-knowledge-pack-wizard-redesign-design.md`
- `docs/superpowers/plans/2026-04-30-knowledge-pack-wizard-redesign.md`
- `docs/superpowers/pr-notes/2026-04-30-knowledge-pack-wizard-redesign.md`

## Do-Not-Touch

- unrelated `/playground` runtime lanes
- unrelated contest-control-plane lanes
- global OpenAI/Codex machine configuration files

## API/data contract

- The FE should stop asking the user for provider/model.
- The backend should resolve the indexing path to a default OpenAI-backed provider.
- The screen needs enough status data to render:
  - overall indexing state
  - per-file status in step `Hoàn tất`

## Design before implementation

- Runtime behavior change: yes
- If yes: confirm `.github/skills/brainstorming/SKILL.md` was read before implementation.
- Current behavior:
  - the page mixes create, upload, list, edit, and notebook flows in one surface
  - the page exposes provider choice and ambiguous `Grade` metadata
- Intended behavior change:
  - wizard-first pack creation flow with Vietnamese-first wording and FE notebook/provider removal
- Candidate approach A:
  - shallow label cleanup on the existing page shell
- Candidate approach B:
  - wizard redesign inside the existing route with a status panel and simplified pack cards
- Chosen approach and reason:
  - approach B; it is the smallest redesign that meaningfully simplifies the teacher flow without a broader route split
- Concrete files/modules expected to change:
  - `web/app/(utility)/knowledge/page.tsx`
  - locale files under `web/locales/`
  - adjacent FE helpers/tests as needed
- Tests to add or update:
  - FE coverage for hidden notebook/provider UI, difficulty control, Vietnamese labels, and completion-state rendering
  - backend or contract coverage for default provider/index path if missing

## Required code reading

- Entry points/handlers to inspect:
  - `web/app/(utility)/knowledge/page.tsx`
- Primary logic/service/use-case modules to inspect:
  - current FE create/upload handlers and the backend handlers they call
- Shared contracts/schemas/types to inspect:
  - metadata fields for `Grade`
  - pack progress/status payloads
  - provider selection flow
- Adjacent or reused flows to inspect:
  - locale coverage in `web/locales/vi/app.json` and `web/locales/en/app.json`
  - notebook FE entry points that are visible on this screen
- Existing tests to inspect:
  - `web/tests/contest-vietnamese-coverage.test.ts`
- Notes from codebase survey:
  - the current screen is monolithic and likely needs smaller FE units during implementation

## Impact surface and stop conditions

- Expected affected areas:
  - knowledge page shell
  - localized copy
  - FE upload/index status rendering
- Files/modules likely to change:
  - `web/app/(utility)/knowledge/page.tsx`
  - extracted FE components/helpers if created during refactor
- Files/modules that must be reviewed even if they may remain unchanged:
  - `web/lib/notebook-api.ts`
  - backend handlers that currently set pack provider/status
- Minimum validation paths before the task can stop:
  - create a pack through the wizard
  - upload files
  - view overall and per-file status
  - confirm notebook/provider controls are gone from visible FE
- What would count as a shallow fix for this task:
  - only renaming labels while leaving the old dual-card layout and notebook tab in place
- Conditions that must be checked before marking done:
  - runtime path really defaults provider/model
  - Vietnamese-first copy is visible on the route
  - completion step shows status with real data rather than placeholder text

## Acceptance criteria

- `Gói kiến thức` uses a wizard-first top section
- `Notebooks` is no longer visible on this screen
- provider/model selection is not visible to the end user
- `Mức độ khó` replaces `Grade/Cấp độ`
- `Hoàn tất` shows overall and per-file status

## Required tests

- focused FE tests for wizard labels and hidden controls
- focused backend/contract tests if the default provider path or status contract changes
- targeted lint/build on touched FE files

## Manual verification

- open the knowledge page and step through all wizard states
- confirm the right panel tracks the active pack
- confirm the existing pack cards are simplified and mostly Vietnamese

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- This lane is in a dedicated worktree under `.worktrees/fix-knowledge-pack-wizard-redesign`.
- Sync `origin/main` inside this lane before any further substantial edit if `main` advances again.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if the runtime workflow change materially changes the documented product structure.

## Handoff notes

- The user will provide an OpenAI key later if the current project credential path is not usable.
- Runtime nuance confirmed during implementation: the repo does not expose a separate KB provider named `openai`; the knowledge-base pipeline remains the single default `llamaindex` path, while the FE now hides provider/model selection entirely.
- The completion step now relies on backend `progress.file_statuses` published from initialization and incremental-upload flows.
- Focused verification passed for backend router/progress tests and FE shell/source tests, but eslint could not run in this worktree because the local binary is unavailable.
