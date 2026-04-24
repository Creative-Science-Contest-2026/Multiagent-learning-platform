# Feature Pod Task: Suggested Learning Path Sequencing

Owner: Codex
Branch: `pod-a/t033-learning-paths`
GitHub Issue: `#88`

## Goal

Add a lightweight learning-path sequencing slice so the platform can suggest a sensible next order of topics based on current learner signals and pack metadata.

## User-visible outcome

- Student or teacher progress flows can surface a simple next-step sequence instead of isolated topic recommendations.
- Existing dashboard and assessment flows remain backward-compatible when no sequence is available.
- The first slice should prefer existing progress and metadata signals over introducing a heavy prerequisite engine.

## Owned files/modules

- `deeptutor/api/routers/dashboard.py` only if the selected slice extends current progress payloads
- `deeptutor/services/` for the selected sequencing helper/service
- `web/app/(workspace)/dashboard/student/` only if the first useful slice needs explicit UI
- `web/lib/dashboard-api.ts` only if API typing changes are required
- `tests/` covering the selected sequencing slice
- `docs/superpowers/tasks/2026-04-24-T033-learning-path-sequencing.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Marketplace, knowledge-pack versioning, tutor follow-up, and assessment review flows
- Unrelated API routers and session history code
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Preserve current student-progress and dashboard behavior when no learning path is generated.
- Prefer extending existing progress/analytics payloads over adding a separate route family for the first slice.
- Keep the first slice explainable from existing assessment and knowledge-pack metadata.

## Acceptance criteria

- The selected progress flow can return a useful ordered list of suggested next topics.
- Existing progress flows remain clean when no sequence is available.
- Regression coverage exists for the chosen sequencing behavior.

## Required tests

- Progress/dashboard regression coverage for the selected sequencing slice
- Frontend production build verification only if student dashboard UI or API typing changes are made

## Manual verification

- Seed recent assessment history with at least one weak topic and one stronger topic
- Confirm the selected progress flow surfaces a coherent next-step sequence

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T032` merged to `main` through PR `#86`.
- Start by reading the existing student-progress and dashboard analytics flow; keep the first sequencing slice small and deterministic before considering any prerequisite graph expansion.
