# PR Note: Knowledge Pack Wizard Redesign

This PR redesigns `/knowledge` into a wizard-first teacher flow and removes the leftover notebook/provider branching from the visible FE path. It also extends KB progress persistence so the completion step can show both overall and per-file indexing status.

## What changed

- replaced the old dual-card create/upload shell with a 3-step wizard: `Thông tin -> Tài liệu -> Hoàn tất`
- removed visible `Notebooks` and provider/model selection from the knowledge screen
- changed the route’s authoring semantics from ambiguous `Grade/Cấp độ` input to `Mức độ khó`
- kept backend indexing on the system-default pipeline instead of inventing a new `openai` provider id
- added persisted `file_statuses` progress so the FE can render real completion-state rows per uploaded document

```mermaid
flowchart LR
  A["Wizard: Thông tin"] --> B["Wizard: Tài liệu"]
  B --> C["POST /api/v1/knowledge/create"]
  C --> D["Default KB pipeline (system-configured)"]
  D --> E["ProgressTracker"]
  E --> F["KB progress + file_statuses"]
  F --> G["Wizard: Hoàn tất"]
  F --> H["Danh sách gói kiến thức"]
```

## Architecture impact

- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was updated.
- The subsystem boundary did not change, but the teacher-facing Knowledge Pack flow now has two explicit product surfaces:
  - wizard-first authoring flow
  - persisted pack-level and per-file ingest status surface

## Verification

- `pytest tests/api/test_knowledge_router.py tests/knowledge/test_progress_tracker.py -q`
- `cd web && node --test tests/knowledge-page-wizard-shell.test.ts tests/contest-vietnamese-coverage.test.ts`
- `cd web && npm run lint -- --file 'app/(utility)/knowledge/page.tsx'`
  - blocked in this worktree because `eslint` is not installed or not available in PATH
