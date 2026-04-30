# Class Tutor Pack Flow Design

## Goal

Make the class tutor route feel like the next teacher-facing step after Knowledge Pack setup by binding each class tutor to exactly one active Knowledge Pack and surfacing that link throughout the screen.

## Current behavior

- `/knowledge` already reads like a bounded classroom setup wizard.
- `/agents` still reads like a generic spec editor with tabs, file sections, and side summaries that are not anchored to a specific Knowledge Pack.
- Teachers must mentally connect “this tutor should use that pack” on their own.
- The current UI emphasizes tutor files and runtime audit more than the classroom relationship between pack content and tutor teaching style.

## Assumption for this lane

- One class tutor links to exactly one active Knowledge Pack at a time.
- Multi-pack tutor support is explicitly out of scope for this lane.

## Chosen UX direction

Keep `/agents` as the class tutor route, but redesign it as **Step 2: define how this tutor teaches the selected Knowledge Pack**.

This preserves route boundaries while fixing the mental model.

## Approaches considered

### 1. Minimal linked-pack badge

- Smallest implementation.
- Rejected because it keeps the core disconnected editor layout intact.

### 2. Tutor route as step 2 of the Knowledge Pack flow

- Reuses the existing route while making the relationship explicit.
- Chosen because it solves the user problem without needing a broad route merge.

### 3. Merge tutor setup into the Knowledge Pack route

- Strongest single-flow experience.
- Rejected for this lane because it widens state, ownership, and validation too much.

## Intended experience

### Header

- Replace the generic tutor setup framing with wording that makes the route read as a follow-up to pack creation.
- Show a clear step relationship such as:
  - Step 1: Gói kiến thức
  - Step 2: Gia sư lớp học

### Primary linked-pack card

- Add a top “Gói kiến thức đang gắn” surface inside the tutor screen.
- It should show:
  - pack name
  - subject
  - difficulty
  - key objectives or a short objective count
  - status: linked / not linked
- It should include a teacher-facing CTA:
  - `Chọn gói kiến thức`
  - or `Đổi gói kiến thức`

### Tutor list rail

- The left rail should still list tutor packs/specs.
- Each item should also show which Knowledge Pack it belongs to.
- Unsaved or unlinked tutors should be visibly marked as not yet linked.

### Main editor hierarchy

- Reorder the center column so the teacher sees:
  1. linked Knowledge Pack context
  2. how this tutor teaches the pack
  3. support style
  4. rules and escalation boundaries
- De-emphasize the feeling of editing arbitrary markdown files first.

### Right summary rail

- Replace the current mostly technical summary emphasis with teacher-facing answers:
  - tutor is linked to which pack
  - what students will experience
  - what the tutor will and will not do
  - when the tutor sends the situation back to teacher review
- Keep runtime audit available, but visually secondary to the pack+tutor relationship.

## Data and contract direction

- First inspect whether the current agent-spec payload can carry a pack link through:
  - existing summary fields,
  - manual markdown files,
  - or a bounded metadata extension exposed by existing agent-spec APIs.
- Prefer a lightweight frontend-friendly link field over inventing a broad new relationship model.
- If a thin API extension is unavoidable, it must stay bounded to “one tutor references one knowledge pack” and must not widen into session binding, retrieval rewrites, or multi-pack orchestration in this lane.

## Data contract choice

- Persist a thin `linked_knowledge_pack` field in agent-spec metadata.
- The stored value should be the pack name only.
- The tutor screen can then use `listKnowledgeBases()` to resolve subject, difficulty, curriculum, and objectives dynamically from current pack metadata.
- This keeps the backend change minimal and avoids duplicating Knowledge Pack metadata inside every tutor record.

## Expected files and responsibilities

- `web/app/(workspace)/agents/page.tsx`
  - refresh top-level page framing and step language
- `web/components/agents/SpecPackAuthoringTab.tsx`
  - own the linked-pack card, tutor-flow layout changes, and teacher-facing summary updates
- `web/components/agents/class-tutor-pack-presenters.ts`
  - derive teacher-facing linked-pack summaries and empty-state labels
- `web/lib/agent-spec-api.ts`
  - carry the thin linked-pack field in the frontend type and upsert payload
- `web/lib/knowledge-api.ts`
  - only if the tutor screen needs a bounded list/shape helper for pack selection
- `deeptutor/api/routers/agent_specs.py`
  - accept and return the linked-pack reference in create/update/detail responses
- `deeptutor/services/agent_spec/service.py`
  - persist the linked-pack reference in metadata.json and return it in list/detail payloads
- `web/locales/en/app.json`
  - add bounded English fallback copy
- `web/locales/vi/app.json`
  - add bounded Vietnamese teacher-facing copy
- `tests/api/test_agent_specs_router.py`
  - lock create/update/detail API behavior for the linked-pack field
- `tests/services/agent_spec/test_service.py`
  - lock persistence/version behavior for the linked-pack field

## Tests to add or update

- Add or update focused tests for tutor-flow wording or presenter helpers if the new pack-link summary is computed in a pure helper.
- Extend existing terminology coverage if the new step-copy and linked-pack labels need protection.
- Run route-scoped eslint and a full `web` build.

## Impact surface review

- Reviewed and expected unchanged:
  - `/knowledge` wizard behavior
  - tutor runtime chat route
  - backend runtime compiler
- Changed:
  - teacher-facing tutor setup presentation, summary, and pack-link visibility
