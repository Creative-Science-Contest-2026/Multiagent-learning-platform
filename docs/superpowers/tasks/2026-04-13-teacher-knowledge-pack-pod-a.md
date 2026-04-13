# Feature Pod Task: Teacher Knowledge Pack MVP

Owner: Pod A AI worker
Branch: `pod-a/teacher-knowledge-pack-mvp`
GitHub Issue: `#2`

## Goal

Add the first teacher-owned Knowledge Pack workflow on top of the existing knowledge base flow so a teacher can create, edit, and view pack metadata needed for the contest demo.

## User-visible outcome

Teachers can open the Knowledge area, set or edit pack metadata such as subject, grade, curriculum, learning objectives, owner, and sharing status, then retrieve that metadata through the API and UI.

## Owned files/modules

- `deeptutor/api/routers/knowledge.py`
- `deeptutor/services/rag/`
- `deeptutor/knowledge/`
- `web/app/(utility)/knowledge/page.tsx`
- `web/lib/knowledge-api.ts`
- `tests/api/test_knowledge_router.py`
- `tests/knowledge/`

## Do-not-touch files/modules

- `deeptutor/api/routers/question.py`
- `deeptutor/api/routers/unified_ws.py`
- `deeptutor/capabilities/deep_question.py`
- `deeptutor/capabilities/chat.py`
- `web/app/(workspace)/page.tsx`
- `web/components/quiz/`
- `web/lib/unified-ws.ts`
- `tests/api/test_question_router.py`
- `tests/api/test_unified_ws_turn_runtime.py`

## API/data contract

- Extend knowledge-pack storage with metadata fields: `subject`, `grade`, `curriculum`, `learning_objectives`, `owner`, and `sharing_status`.
- Keep existing knowledge base identifiers stable.
- Add minimal read/write API support in the knowledge router without breaking current upload and list behavior.
- Return metadata in a shape that frontend code can consume without guessing field names.

## Acceptance criteria

- A teacher can create or update Knowledge Pack metadata from the Knowledge UI.
- The backend persists and returns the metadata through the knowledge API.
- Existing knowledge upload/list behavior continues to work.
- Metadata names are documented in the implementation PR and remain consistent across API and UI.

## Required tests

- `pytest tests/api/test_knowledge_router.py -v`
- `pytest tests/knowledge -v`
- `python3 -m compileall deeptutor`

## Manual verification

- Start the backend and frontend.
- Open the Knowledge page.
- Create or edit a Knowledge Pack with the required metadata.
- Reload the page and confirm the metadata still appears.
- Confirm existing knowledge listing still works.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- If this task introduces shared API types used by Pod B, isolate that contract in a small follow-up PR or coordinate before Pod B changes the same fields.
- Keep Teacher Dashboard work out of this packet unless the task packet is explicitly expanded.
