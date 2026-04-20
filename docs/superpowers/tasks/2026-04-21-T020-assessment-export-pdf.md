# Feature Pod Task: Assessment Results Export to PDF

Owner: Codex
Branch: `pod-a/t020-assessment-export-pdf`
GitHub Issue: `#65`

## Goal

Add PDF export for assessment review results so teachers and students can download a shareable report.

## User-visible outcome

- Assessment review pages expose an Export PDF action.
- Users can download a PDF report containing score, questions, answers, explanations, and recommendations.
- Existing assessment review behavior remains unchanged when export is not used.

## Owned files/modules

- `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/tasks/2026-04-21-T020-assessment-export-pdf.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-21.md`

## Do-not-touch files/modules

- Marketplace, tutor, knowledge, and settings files
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Add an export endpoint under the dashboard router for assessment sessions.
- Keep existing session/review payloads backward-compatible.
- Prefer a self-contained PDF response contract suitable for direct browser download.

## Acceptance criteria

- Assessment review page shows an Export PDF action.
- Export endpoint returns a downloadable PDF for a valid assessment session.
- PDF includes score, question content, learner answers, explanations, and recommendation summary.

## Required tests

- API regression coverage for the export endpoint
- Frontend build verification if client/page wiring changes

## Manual verification

- Open an assessment review page
- Trigger Export PDF
- Confirm browser downloads a readable PDF with expected report content

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T019` merged to `main` through PR `#64`.
- Start by inspecting the current assessment review page and dashboard router before choosing a PDF generation strategy.
