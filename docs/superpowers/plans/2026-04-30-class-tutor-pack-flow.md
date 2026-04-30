# Class Tutor Pack Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the class tutor screen read like step 2 of the Knowledge Pack flow and persist one linked Knowledge Pack for each tutor.

**Architecture:** Add a thin `linked_knowledge_pack` field to the existing agent-spec metadata and expose it through the current agent-spec APIs. Then refactor the `/agents` tutor-authoring UI so that the selected Knowledge Pack becomes the first-class context for tutor setup, with teacher-facing summaries derived from current Knowledge Pack metadata.

**Tech Stack:** FastAPI, Python service layer, Next.js App Router, React, TypeScript, `react-i18next`, Node test runner, pytest

---

### Task 1: Persist one linked Knowledge Pack in the agent-spec contract

**Files:**
- Modify: `deeptutor/api/routers/agent_specs.py`
- Modify: `deeptutor/services/agent_spec/service.py`
- Modify: `tests/api/test_agent_specs_router.py`
- Modify: `tests/services/agent_spec/test_service.py`

- [ ] **Step 1: Write the failing Python tests**

Add a linked-pack field to the existing test payloads and assertions in:

```python
# tests/api/test_agent_specs_router.py
def _payload(agent_id: str = "fraction-coach") -> dict:
    return {
        "agent_id": agent_id,
        "display_name": "Fraction Coach",
        "description": "Teacher-authored fraction tutor",
        "linked_knowledge_pack": "fractions-pack",
        ...
    }
```

```python
# tests/services/agent_spec/test_service.py
payload = service.create_pack(
    agent_id="Fraction Coach",
    display_name="Fraction Coach",
    description="Middle-school fraction remediation",
    linked_knowledge_pack="fractions-pack",
    structured=_sample_structured(),
    files={"CURRICULUM.md": "# Curriculum\n\n- Fractions first.\n"},
)

assert payload["linked_knowledge_pack"] == "fractions-pack"
assert "linked_knowledge_pack" in (tmp_path / "agent_specs" / "fraction-coach" / "metadata.json").read_text()
```

- [ ] **Step 2: Run the failing backend tests**

Run:

```bash
pytest tests/services/agent_spec/test_service.py tests/api/test_agent_specs_router.py -q
```

Expected:
- FAIL because `create_pack`, `save_pack`, router payloads, and returned responses do not yet support `linked_knowledge_pack`

- [ ] **Step 3: Implement the minimal backend contract**

Make these bounded changes:

```python
# deeptutor/api/routers/agent_specs.py
class AgentSpecUpsertRequest(BaseModel):
    agent_id: str
    display_name: str
    description: str = ""
    linked_knowledge_pack: str | None = None
    structured: StructuredPayload = Field(default_factory=StructuredPayload)
    files: dict[str, str] = Field(default_factory=dict)
```

Pass that value through `create_pack(...)` and `save_pack(...)`.

```python
# deeptutor/services/agent_spec/service.py
def create_pack(..., linked_knowledge_pack: str | None = None, ...) -> dict[str, object]:
    metadata = {
        ...
        "linked_knowledge_pack": linked_knowledge_pack.strip() if linked_knowledge_pack else None,
    }
```

```python
def save_pack(..., linked_knowledge_pack: str | None = None, ...) -> dict[str, object]:
    metadata["linked_knowledge_pack"] = linked_knowledge_pack.strip() if linked_knowledge_pack else None
```

Return the same field from both `_build_summary(...)` and `_build_payload(...)`.

- [ ] **Step 4: Re-run backend tests and verify green**

Run:

```bash
pytest tests/services/agent_spec/test_service.py tests/api/test_agent_specs_router.py -q
```

Expected:
- PASS for both files

- [ ] **Step 5: Commit the backend contract slice**

Run:

```bash
git add deeptutor/api/routers/agent_specs.py deeptutor/services/agent_spec/service.py tests/api/test_agent_specs_router.py tests/services/agent_spec/test_service.py
git commit -m "feat(agent-spec): persist linked knowledge pack [UI-TUTOR-PACK]"
```

### Task 2: Add tutor-pack presenter coverage on the frontend

**Files:**
- Create: `web/components/agents/class-tutor-pack-presenters.ts`
- Create: `web/tests/class-tutor-pack-presenters.test.ts`
- Modify: `web/lib/agent-spec-api.ts`

- [ ] **Step 1: Write the failing frontend test**

Create a pure helper test:

```typescript
import test from "node:test";
import assert from "node:assert/strict";
import {
  buildLinkedKnowledgePackSummary,
  tutorPackStatusLabel,
} from "../components/agents/class-tutor-pack-presenters.ts";

test("linked knowledge pack summary prefers live pack metadata", () => {
  const summary = buildLinkedKnowledgePackSummary({
    linkedPackName: "fractions-pack",
    knowledgePack: {
      name: "fractions-pack",
      metadata: {
        subject: "Toan",
        difficulty: "beginner",
        curriculum: "Phan so",
        learning_objectives: ["Nhan dien phan so", "So sanh phan so"],
      },
    },
  });

  assert.equal(summary.packName, "fractions-pack");
  assert.equal(summary.subject, "Toan");
  assert.equal(summary.status, "Đã gắn gói kiến thức");
});
```

- [ ] **Step 2: Run the failing frontend test**

Run:

```bash
cd web && node --test tests/class-tutor-pack-presenters.test.ts
```

Expected:
- FAIL because the presenter helper does not exist yet

- [ ] **Step 3: Implement the minimal presenter and type extension**

Add `linked_knowledge_pack?: string | null` to `AgentSpecSummary`, `AgentSpecDetail`, and `AgentSpecUpsertPayload` in `web/lib/agent-spec-api.ts`.

Create:

```typescript
// web/components/agents/class-tutor-pack-presenters.ts
export function tutorPackStatusLabel(linkedPackName?: string | null): string {
  return linkedPackName ? "Đã gắn gói kiến thức" : "Chưa gắn gói kiến thức";
}
```

```typescript
export function buildLinkedKnowledgePackSummary(...) {
  return {
    packName: linkedPackName || "Chưa chọn gói kiến thức",
    subject: knowledgePack?.metadata?.subject || "Chưa chọn môn học",
    difficulty: knowledgePack?.metadata?.difficulty || "Chưa chọn độ khó",
    curriculum: knowledgePack?.metadata?.curriculum || "Chưa có chương trình học",
    objectiveCount: knowledgePack?.metadata?.learning_objectives?.length || 0,
    status: tutorPackStatusLabel(linkedPackName),
  };
}
```

- [ ] **Step 4: Re-run the frontend presenter test**

Run:

```bash
cd web && node --test tests/class-tutor-pack-presenters.test.ts
```

Expected:
- PASS

- [ ] **Step 5: Commit the presenter slice**

Run:

```bash
git add web/components/agents/class-tutor-pack-presenters.ts web/lib/agent-spec-api.ts web/tests/class-tutor-pack-presenters.test.ts
git commit -m "test(agents): add tutor-pack presenter coverage [UI-TUTOR-PACK]"
```

### Task 3: Refactor the class tutor flow around the linked Knowledge Pack

**Files:**
- Modify: `web/app/(workspace)/agents/page.tsx`
- Modify: `web/components/agents/SpecPackAuthoringTab.tsx`
- Modify: `web/lib/knowledge-api.ts`
- Modify: `web/locales/en/app.json`
- Modify: `web/locales/vi/app.json`
- Modify: `web/tests/contest-terminology.test.ts`

- [ ] **Step 1: Load Knowledge Pack options into the tutor-authoring tab**

In `SpecPackAuthoringTab.tsx`, import `listKnowledgeBases` and load the available packs alongside tutor packs.

Keep a selected linked-pack state driven by:
- the saved `draft.linked_knowledge_pack`
- or the teacher’s current selection before save

- [ ] **Step 2: Add the linked-pack UI layer before the tutor form**

Refactor the top of `SpecPackAuthoringTab.tsx` so the main flow becomes:

```text
linked pack card
-> tutor identity and description
-> support style
-> rules
-> manual markdown files
```

The new linked-pack card should show:
- current pack name
- subject
- difficulty
- objective count
- a select/dropdown to choose or change pack

- [ ] **Step 3: Make the left rail and summary rail reflect the linked pack**

Update tutor list items and the right summary rail so they display the linked Knowledge Pack instead of only tutor-only metadata.

The right rail should prioritize:
- linked pack
- student experience summary
- escalation / guardrail summary

Leave runtime policy audit available, but secondary.

- [ ] **Step 4: Save the linked pack through create/update**

When calling `createAgentSpec(...)` or `updateAgentSpec(...)`, include:

```typescript
linked_knowledge_pack: selectedLinkedPackName || null
```

- [ ] **Step 5: Add the bounded copy updates**

Extend locale files with the new teacher-facing copy such as:
- `Thiết lập gia sư cho gói kiến thức`
- `Bước 2: định nghĩa cách gia sư dạy gói này`
- `Gói kiến thức đang gắn`
- `Đổi gói kiến thức`
- `Chưa gắn gói kiến thức`

Update `web/tests/contest-terminology.test.ts` with a couple of exact-string assertions for the new tutor-flow keys.

- [ ] **Step 6: Run the focused frontend checks**

Run:

```bash
cd web && node --test tests/contest-terminology.test.ts tests/class-tutor-pack-presenters.test.ts
cd web && npx eslint "app/(workspace)/agents/page.tsx" "components/agents/SpecPackAuthoringTab.tsx" "components/agents/class-tutor-pack-presenters.ts"
cd web && npm run build
```

Expected:
- all commands pass

- [ ] **Step 7: Commit the UI slice**

Run:

```bash
git add web/app/\(workspace\)/agents/page.tsx web/components/agents/SpecPackAuthoringTab.tsx web/components/agents/class-tutor-pack-presenters.ts web/lib/agent-spec-api.ts web/lib/knowledge-api.ts web/locales/en/app.json web/locales/vi/app.json web/tests/contest-terminology.test.ts web/tests/class-tutor-pack-presenters.test.ts
git commit -m "fix(agents): tie class tutor flow to knowledge pack [UI-TUTOR-PACK]"
```

### Task 4: Record the lane and final verification

**Files:**
- Modify: `ai_first/daily/2026-04-30.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-class-tutor-pack-flow.md`

- [ ] **Step 1: Run the final repo-scoped checks for this lane**

Run:

```bash
pytest tests/services/agent_spec/test_service.py tests/api/test_agent_specs_router.py -q
cd web && node --test tests/contest-terminology.test.ts tests/class-tutor-pack-presenters.test.ts
cd web && npx eslint "app/(workspace)/agents/page.tsx" "components/agents/SpecPackAuthoringTab.tsx" "components/agents/class-tutor-pack-presenters.ts"
cd web && npm run build
git diff --check
```

Expected:
- PASS, or a clearly documented pre-existing blocker if something outside the lane fails

- [ ] **Step 2: Update the daily log**

Record:
- branch
- task id
- linked-pack contract decision
- tests run
- any intentionally unchanged areas

- [ ] **Step 3: Write the PR architecture note**

Create `docs/superpowers/pr-notes/2026-04-30-class-tutor-pack-flow.md` with:
- summary
- scope
- Mermaid diagram showing `Knowledge Pack -> Class Tutor Setup`
- validation
- whether `MAIN_SYSTEM_MAP` changed

- [ ] **Step 4: Commit the docs/handoff slice**

Run:

```bash
git add ai_first/daily/2026-04-30.md docs/superpowers/pr-notes/2026-04-30-class-tutor-pack-flow.md
git commit -m "docs(ai-first): record class tutor pack flow lane [UI-TUTOR-PACK]"
```
