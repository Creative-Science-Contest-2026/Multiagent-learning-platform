# Feature Pod Task: Teacher Assessment Review MVP

Owner: Pod A + Pod B coordinated AI workers
Branch: `pod-a/teacher-assessment-review-mvp`
GitHub Issue: create or link after opening the implementation PR

## Goal

Add a teacher-facing review flow from Dashboard into a dedicated assessment session review page.

## User-visible outcome

Teachers can open Dashboard, identify assessment sessions, and drill into one review page that shows score, correct/incorrect counts, question-level results, and Knowledge Pack context.

## Owned files/modules

- `deeptutor/api/routers/dashboard.py`
- `deeptutor/api/routers/sessions.py`
- `deeptutor/services/session/assessment_review.py`
- `deeptutor/services/session/__init__.py`
- `tests/api/test_dashboard_router.py`
- `tests/api/test_session_review_router.py`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
- `web/lib/dashboard-api.ts`
- `docs/superpowers/pr-notes/teacher-assessment-review-*.md`
- `ai_first/daily/YYYY-MM-DD.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` if route/API structure changes materially

## Do-not-touch files/modules

- `deeptutor/knowledge/`
- `deeptutor/services/rag/`
- `web/app/(utility)/knowledge/page.tsx`
- lockfiles unless dependency installation proves they must change
- `.env*`
- `data/`

## Acceptance criteria

- Dashboard keeps summary-first behavior.
- Assessment rows link to a dedicated review page.
- Review page shows score, correct count, incorrect count, per-question results, and Knowledge Pack names when available.
- Legacy sessions without structured review data fail gracefully.
- Existing Dashboard and session persistence tests stay green.

## Required validation

- `pytest tests/api/test_dashboard_router.py tests/api/test_session_review_router.py -v`
- `python3 -m compileall deeptutor`
- `cd web && NEXT_PUBLIC_API_BASE=http://localhost:8001 npm run build`
- `git diff --check`
- `rg -n "Assessment Review|assessment-review|dashboard/assessments|Mermaid" docs/superpowers/pr-notes ai_first web deeptutor tests`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- Keep Dashboard compact; per-question detail belongs on the review page.
- Use one backend extraction path for Dashboard summary and the dedicated review endpoint.
- Do not add class roster, assignments, or multi-student management in this task.
