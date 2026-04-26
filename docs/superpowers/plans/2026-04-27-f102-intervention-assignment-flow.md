# Intervention Assignment Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let teachers convert an existing `teacher_action` into a bounded `intervention_assignment` that appears back in the dashboard flow for student and small-group remediation.

**Architecture:** This feature adds a lightweight `intervention_assignments` store inside the existing dashboard/evidence boundary, linked to the `teacher_actions` created in `F101`. The backend exposes create/update routes and attaches assignment summaries back onto student and group insight payloads, while the frontend adds a compact assignment composer and readback surfaces without introducing delivery, due dates, or completion semantics.

**Tech Stack:** FastAPI, SQLite-backed evidence helpers, pytest, Next.js App Router, React client components, TypeScript, Tailwind CSS, existing dashboard REST client

---

### Task 1: Add The Intervention Assignment Store And Failing Tests

**Files:**
- Create: `deeptutor/services/evidence/intervention_assignments.py`
- Modify: `deeptutor/services/evidence/__init__.py`
- Test: `tests/api/test_dashboard_router.py`

- [ ] **Step 1: Write failing backend tests for intervention assignment create/read/update**

Add tests to `tests/api/test_dashboard_router.py` that assert:
- a student teacher action can be converted into an assignment
- a small-group teacher action can be converted into an assignment
- assignment summaries round-trip back into dashboard insight payloads
- assignment status updates persist

Use these target test names:

```python
async def test_dashboard_intervention_assignment_create_round_trip(...)
async def test_dashboard_intervention_assignment_attaches_to_student_payload(...)
async def test_dashboard_group_intervention_assignment_summary_attaches_to_group_card(...)
async def test_dashboard_intervention_assignment_status_update_round_trip(...)
```

- [ ] **Step 2: Run the targeted tests and confirm they fail**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k intervention_assignment -q
```

Expected:
- failures for missing routes, payload keys, or helper functions

- [ ] **Step 3: Implement the SQLite helper for intervention assignments**

Create `deeptutor/services/evidence/intervention_assignments.py` with:

```python
_ALLOWED_ASSIGNMENT_TYPES = {
    "practice_set",
    "reteach_session",
    "prerequisite_review",
    "small_group_activity",
}
_ALLOWED_ASSIGNMENT_STATUSES = {"draft", "planned", "done", "dismissed"}
```

and bounded functions:

```python
def create_intervention_assignment(
    store: Any,
    *,
    teacher_action_id: str,
    assignment_type: str,
    title: str,
    teacher_note: str,
    practice_note: str,
) -> dict[str, Any]:
    ...

def update_intervention_assignment_status(
    store: Any,
    assignment_id: str,
    *,
    status: str,
) -> dict[str, Any]:
    ...

def list_intervention_assignments(store: Any) -> list[dict[str, Any]]:
    ...
```

Use the linked `teacher_action` row to inherit:
- `target_type`
- `target_id`
- `topic`

- [ ] **Step 4: Export the helper from `deeptutor/services/evidence/__init__.py`**

Add explicit imports alongside the teacher-action helper so the router can use the new store functions.

- [ ] **Step 5: Run the targeted tests again**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k intervention_assignment -q
```

Expected:
- route tests still fail, but helper-level failures are gone

- [ ] **Step 6: Commit the backend helper slice**

```bash
git add deeptutor/services/evidence/intervention_assignments.py deeptutor/services/evidence/__init__.py tests/api/test_dashboard_router.py
git commit -m "feat(evidence): add intervention assignment store [F102]"
```

### Task 2: Extend Dashboard Routes And Insight Payload Assembly

**Files:**
- Modify: `deeptutor/api/routers/dashboard.py`
- Modify: `deeptutor/services/evidence/teacher_insights.py`
- Test: `tests/api/test_dashboard_router.py`

- [ ] **Step 1: Add request models for assignment create and status update**

Inside `deeptutor/api/routers/dashboard.py`, add:

```python
class InterventionAssignmentCreateRequest(BaseModel):
    teacher_action_id: str
    assignment_type: str
    title: str
    teacher_note: str
    practice_note: str


class InterventionAssignmentStatusUpdateRequest(BaseModel):
    status: str
```

- [ ] **Step 2: Add the create and update routes**

Implement:

```python
@router.post("/intervention-assignments")
async def create_dashboard_intervention_assignment(
    payload: InterventionAssignmentCreateRequest,
) -> dict[str, Any]:
    ...


@router.patch("/intervention-assignments/{assignment_id}")
async def update_dashboard_intervention_assignment_status(
    assignment_id: str,
    payload: InterventionAssignmentStatusUpdateRequest,
) -> dict[str, Any]:
    ...
```

Translate:
- invalid linked action -> `400`
- missing row -> `404`

- [ ] **Step 3: Attach assignment summaries into insight payloads**

Extend `deeptutor/services/evidence/teacher_insights.py` so:
- each student row can expose `intervention_assignments`
- each small-group row can expose the newest linked assignment summary as `intervention_assignment`

Keep this bounded:
- use latest assignment summary only on overview cards
- keep full per-student assignment list on detail payloads

- [ ] **Step 4: Run the targeted dashboard tests**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "teacher_action or intervention_assignment or dashboard_insights" -q
```

Expected:
- all targeted dashboard API tests pass

- [ ] **Step 5: Commit the route/payload slice**

```bash
git add deeptutor/api/routers/dashboard.py deeptutor/services/evidence/teacher_insights.py tests/api/test_dashboard_router.py
git commit -m "feat(dashboard): add intervention assignment routes [F102]"
```

### Task 3: Extend The Dashboard API Client Types

**Files:**
- Modify: `web/lib/dashboard-api.ts`

- [ ] **Step 1: Define assignment types and request contracts**

Add:

```ts
export type InterventionAssignmentType =
  | "practice_set"
  | "reteach_session"
  | "prerequisite_review"
  | "small_group_activity";

export type InterventionAssignmentStatus = "draft" | "planned" | "done" | "dismissed";

export interface InterventionAssignmentRecord {
  id: string;
  teacher_action_id: string;
  target_type: "student" | "small_group";
  target_id: string;
  assignment_type: InterventionAssignmentType;
  topic: string;
  title: string;
  teacher_note: string;
  practice_note: string;
  status: InterventionAssignmentStatus;
  created_at: number;
  updated_at: number;
}
```

- [ ] **Step 2: Extend dashboard payload types**

Add:
- `intervention_assignments?: InterventionAssignmentRecord[]` to `TeacherInsightStudent`
- `intervention_assignment?: InterventionAssignmentRecord | null` to small-group rows

- [ ] **Step 3: Add API helpers**

Create:

```ts
export async function createInterventionAssignment(...)
export async function updateInterventionAssignmentStatus(...)
```

using `/api/v1/dashboard/intervention-assignments`.

- [ ] **Step 4: Run targeted frontend lint for the API client**

Run:

```bash
cd web && ./node_modules/.bin/eslint --config eslint.config.mjs lib/dashboard-api.ts
```

Expected:
- pass

- [ ] **Step 5: Commit the client contract slice**

```bash
git add web/lib/dashboard-api.ts
git commit -m "feat(dashboard): add intervention assignment client contracts [F102]"
```

### Task 4: Add The Assignment Composer And Overview Surfaces

**Files:**
- Create: `web/components/dashboard/InterventionAssignmentComposer.tsx`
- Modify: `web/components/dashboard/StudentInsightCard.tsx`
- Modify: `web/components/dashboard/SmallGroupInsightCard.tsx`

- [ ] **Step 1: Create the assignment composer**

Implement a client component that:
- takes a `teacherAction` record
- prefills `assignment_type`, `title`, `teacher_note`, `practice_note`
- posts to `createInterventionAssignment`
- returns the created record through `onCreated`

Use a compact UI parallel to `TeacherActionComposer.tsx`.

- [ ] **Step 2: Render the composer from student cards**

On `StudentInsightCard.tsx`:
- keep the existing `TeacherActionComposer`
- when a latest teacher action exists, show `Convert to assignment`
- after create, show a summary box:
  - assignment type
  - title
  - status

- [ ] **Step 3: Render the composer from small-group cards**

On `SmallGroupInsightCard.tsx`:
- show `Convert to assignment` only after a group teacher action exists
- show latest assignment summary after create

- [ ] **Step 4: Run targeted frontend lint**

Run:

```bash
cd web && ./node_modules/.bin/eslint --config eslint.config.mjs components/dashboard/InterventionAssignmentComposer.tsx components/dashboard/StudentInsightCard.tsx components/dashboard/SmallGroupInsightCard.tsx
```

Expected:
- pass

- [ ] **Step 5: Commit the overview UI slice**

```bash
git add web/components/dashboard/InterventionAssignmentComposer.tsx web/components/dashboard/StudentInsightCard.tsx web/components/dashboard/SmallGroupInsightCard.tsx
git commit -m "feat(dashboard): add intervention assignment composer [F102]"
```

### Task 5: Extend Student Detail And Task Packet/PR Note

**Files:**
- Modify: `web/components/dashboard/StudentInsightDetail.tsx`
- Create: `docs/superpowers/tasks/2026-04-27-f102-intervention-assignment-flow.md`
- Create: `docs/superpowers/pr-notes/2026-04-27-f102-intervention-assignment-flow.md`
- Modify: `ai_first/daily/2026-04-26.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`

- [ ] **Step 1: Add the `Intervention assignments` section to student detail**

Render:
- assignment type
- title
- topic
- teacher note
- practice note
- status select using `updateInterventionAssignmentStatus`

- [ ] **Step 2: Create the task packet**

Add a packet that records:
- task ID `F102_INTERVENTION_ASSIGNMENT_FLOW`
- commit tag `F102`
- goal
- owned files
- do-not-touch files
- validations

- [ ] **Step 3: Create the PR note with Mermaid diagram**

Add a note showing:
- recommendation
- teacher action
- intervention assignment
- dashboard/detail surfaces

- [ ] **Step 4: Run final targeted validation**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "teacher_action or intervention_assignment or dashboard_insights" -q
cd web && ./node_modules/.bin/eslint --config eslint.config.mjs components/dashboard/InterventionAssignmentComposer.tsx components/dashboard/StudentInsightCard.tsx components/dashboard/SmallGroupInsightCard.tsx components/dashboard/StudentInsightDetail.tsx lib/dashboard-api.ts
git diff --check
```

Expected:
- targeted pytest passes
- targeted eslint passes
- diff check clean

- [ ] **Step 5: Update daily log and assignment status**

Record:
- implementation done
- validations run
- next likely follow-up (`F103`, `F107`, or `F120`)

- [ ] **Step 6: Commit the final slice**

```bash
git add web/components/dashboard/StudentInsightDetail.tsx docs/superpowers/tasks/2026-04-27-f102-intervention-assignment-flow.md docs/superpowers/pr-notes/2026-04-27-f102-intervention-assignment-flow.md ai_first/daily/2026-04-26.md ai_first/ACTIVE_ASSIGNMENTS.md
git commit -m "feat(dashboard): show intervention assignments in detail [F102]"
```

## Spec Coverage Check

- linked assignment object: covered by Tasks 1 and 2
- student + small-group create flow: covered by Task 4
- student detail assignment section: covered by Task 5
- bounded API/status update contract: covered by Tasks 2, 3, and 5
- non-goals (no delivery/due date/completion): enforced by file scope and omitted route/data fields

