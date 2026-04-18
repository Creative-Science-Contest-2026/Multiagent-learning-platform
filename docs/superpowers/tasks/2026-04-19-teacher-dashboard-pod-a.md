# Feature Pod Task: Teacher Dashboard MVP

Owner: Pod A AI worker
Branch: `pod-a/teacher-dashboard-mvp`
GitHub Issue: `#9`

## Goal

Add the first teacher-facing dashboard that summarizes recent Knowledge Pack, assessment, and student tutoring activity for the contest demo.

## User-visible outcome

Teachers can open a Dashboard page and see a compact overview of recent learning activity: active Knowledge Packs, generated assessments, student tutoring sessions, and simple progress/status indicators.

## Owned files/modules

- `deeptutor/api/routers/dashboard.py`
- `deeptutor/api/routers/sessions.py`
- `deeptutor/services/session/`
- `web/app/(workspace)/dashboard/`
- `web/lib/session-api.ts`
- `web/lib/dashboard-api.ts`
- `web/components/dashboard/`
- `tests/api/test_dashboard_router.py`
- `tests/services/session/`

## Do-not-touch files/modules

- `deeptutor/api/routers/knowledge.py`
- `deeptutor/api/routers/question.py`
- `deeptutor/api/routers/unified_ws.py`
- `deeptutor/capabilities/deep_question.py`
- `deeptutor/capabilities/chat.py`
- `web/app/(utility)/knowledge/page.tsx`
- `web/components/quiz/`
- `web/lib/knowledge-api.ts`
- `web/lib/quiz-types.ts`
- `tests/api/test_knowledge_router.py`
- `tests/api/test_question_router.py`
- `tests/api/test_unified_ws_turn_runtime.py`

## API/data contract

- Extend or reuse the existing dashboard API to return:
  - recent sessions grouped by capability or activity type;
  - counts for tutoring sessions, generated assessments, and running/failed/completed activity;
  - Knowledge Pack references from session preferences when available;
  - timestamps and short summaries suitable for UI cards and tables.
- Keep existing session identifiers stable.
- Do not invent new persistence if SQLite session data already contains the needed information.

## Acceptance criteria

- A teacher can open the Dashboard page from the workspace navigation or direct route.
- The dashboard shows recent activity from the unified session store.
- The dashboard distinguishes assessment generation from student tutoring/chat activity.
- The dashboard shows Knowledge Pack references when sessions used a selected Knowledge Pack.
- Empty state is useful when no activity exists.
- Existing session APIs and chat persistence continue to work.

## Required tests

- `pytest tests/api/test_dashboard_router.py -v`
- `pytest tests/services/session -v`
- `python3 -m compileall deeptutor`
- `cd web && npm run build`

## Manual verification

- Start backend and frontend.
- Generate an assessment from a Knowledge Pack.
- Ask a student tutor question with a selected Knowledge Pack.
- Open the Dashboard page.
- Confirm recent assessment and tutoring activity appear with Knowledge Pack context where available.
- Confirm empty/loading/error states are readable.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if dashboard routes, API shape, or session aggregation changes.

## Handoff notes

- Keep this task focused on read-only dashboard aggregation and display.
- Do not add teacher analytics models, grading workflows, or long-term reporting unless this packet is explicitly expanded.
- If the dashboard needs fields not present in session data, add the smallest session metadata extension and document it in the PR.
