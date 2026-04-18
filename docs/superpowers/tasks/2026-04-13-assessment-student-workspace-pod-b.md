# Feature Pod Task: Assessment Builder and Student Tutor Workspace MVP

Owner: Pod B AI worker
Branch: `pod-b/assessment-student-workspace-mvp`
GitHub Issue: `#3`

## Goal

Add the first teacher-facing assessment builder and student-facing tutor workspace flow grounded in a selected Knowledge Pack.

## User-visible outcome

Teachers can generate exercises from a selected Knowledge Pack with Vietnamese-friendly controls for topic, subject, count, difficulty, and question type. Students can learn in the chat workspace with the selected Knowledge Pack attached to the tutoring context.

## Owned files/modules

- `deeptutor/api/routers/question.py`
- `deeptutor/api/routers/unified_ws.py`
- `deeptutor/capabilities/deep_question.py`
- `deeptutor/capabilities/chat.py`
- `deeptutor/capabilities/request_contracts.py`
- `web/app/(workspace)/page.tsx`
- `web/components/quiz/`
- `web/components/chat/`
- `web/lib/unified-ws.ts`
- `web/lib/quiz-types.ts`
- `tests/api/test_question_router.py`
- `tests/api/test_unified_ws_turn_runtime.py`

## Do-not-touch files/modules

- `deeptutor/api/routers/knowledge.py`
- `deeptutor/services/rag/`
- `deeptutor/knowledge/`
- `web/app/(utility)/knowledge/page.tsx`
- `web/lib/knowledge-api.ts`
- `tests/api/test_knowledge_router.py`
- `tests/knowledge/`

## API/data contract

- Question generation requests must accept Knowledge Pack context plus `topic`, `subject`, `count`, `difficulty`, and `question_type`.
- Question generation responses must include answer content, explanations, and common mistakes when available.
- Student tutor requests must pass the selected Knowledge Pack identifier into the chat context without breaking existing session persistence.
- Shared field names with Pod A must stay stable once agreed.

## Acceptance criteria

- The assessment UI lets a teacher choose a Knowledge Pack and generate questions with the required controls.
- Generated output shows answers and explanations, with common mistakes when available.
- The student workspace can select a Knowledge Pack and use it during tutoring.
- Existing SQLite-backed session persistence still works.

## Required tests

- `pytest tests/api/test_question_router.py -v`
- `pytest tests/api/test_unified_ws_turn_runtime.py -v`
- `python3 -m compileall deeptutor`
- `cd web && npm run build`

## Manual verification

- Start the backend and frontend.
- Generate an assessment from a selected Knowledge Pack.
- Confirm answer and explanation output renders in the UI.
- Open the student workspace, select the same Knowledge Pack, and ask a grounded question.
- Confirm the session persists across refresh or reload.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- Do not invent or rename Knowledge Pack metadata fields owned by Pod A without coordination.
- If a shared request/response contract needs to move into a common type module, isolate that contract change before broad frontend edits.
