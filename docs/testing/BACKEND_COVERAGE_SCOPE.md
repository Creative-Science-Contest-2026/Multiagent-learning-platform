# Backend Coverage Scope

The authoritative backend quality gate for this repository is:

```bash
bash scripts/run_backend_coverage_gate.sh
```

That command is the single source of truth for:

- which backend tests must pass
- which backend modules count toward the coverage denominator
- the minimum accepted backend coverage threshold of `80%`
- the compile check that runs after the test pass

## In-Scope Backend Surface

The current gate measures the teacher-first contest path and the backend runtime that actively supports it:

- `deeptutor/api/main.py`
- `deeptutor/api/routers/agent_specs.py`
- `deeptutor/api/routers/assessment.py`
- `deeptutor/api/routers/dashboard.py`
- `deeptutor/api/routers/knowledge.py`
- `deeptutor/api/routers/marketplace.py`
- `deeptutor/api/routers/question.py`
- `deeptutor/api/routers/unified_ws.py`
- `deeptutor/services/agent_spec/service.py`
- `deeptutor/services/assessment/analysis.py`
- `deeptutor/services/assessment/recommendation_engine.py`
- `deeptutor/services/evidence/diagnosis.py`
- `deeptutor/services/evidence/diagnosis_feedback.py`
- `deeptutor/services/evidence/diagnosis_taxonomy.py`
- `deeptutor/services/evidence/evidence_sufficiency.py`
- `deeptutor/services/evidence/extractor.py`
- `deeptutor/services/evidence/intervention_assignments.py`
- `deeptutor/services/evidence/intervention_effectiveness.py`
- `deeptutor/services/evidence/recommendation_acks.py`
- `deeptutor/services/evidence/recommendation_feedback.py`
- `deeptutor/services/evidence/teacher_actions.py`
- `deeptutor/services/evidence/teacher_insights.py`
- `deeptutor/services/evidence/teacher_overrides.py`
- `deeptutor/services/runtime_policy/compiler.py`
- `deeptutor/services/session/sqlite_store.py`
- `deeptutor/services/session/turn_runtime.py`

These files remain in scope even where coverage is still lower than the strongest modules. The gate is intentionally not hiding active surfaces such as:

- `knowledge` CRUD and upload flows
- question generation and mimic WebSocket flows
- unified WebSocket turn orchestration
- session persistence and runtime event replay

## Authoritative Test Inventory

The gate currently requires these test slices:

- `tests/api/test_main_app.py`
- `tests/api/test_agent_specs_router.py`
- `tests/api/test_assessment_router.py`
- `tests/api/test_dashboard_router.py`
- `tests/api/test_knowledge_router.py`
- `tests/api/test_marketplace_router.py`
- `tests/api/test_question_router.py`
- `tests/api/test_unified_ws_turn_runtime.py`
- `tests/knowledge/test_kb_metadata_normalization.py`
- `tests/knowledge/test_progress_tracker.py`
- `tests/services/agent_spec/test_service.py`
- `tests/services/evidence/test_intervention_effectiveness.py`
- `tests/services/runtime_policy/test_compiler.py`
- `tests/services/session`

## Explicitly Omitted Backend Areas

The following backend areas do not count toward the `80%` gate yet because they are not part of the currently audited contest-path product flow or they still depend on optional integrations without deterministic local fixtures:

- `deeptutor/api/routers/chat.py`, `solve.py`, `co_writer.py`, `guide.py`, `memory.py`, `notebook.py`, `plugins_api.py`, `sessions.py`, `settings.py`, `system.py`, `tutorbot.py`, `vision_solver.py`, `agent_config.py`
  Reason: these are side-surface, admin, playground, authoring, or alternate entry flows not required by the current teacher-first contest path covered by this gate.
- backend modules that only exercise optional external-provider behavior beyond the audited `llamaindex` path
  Reason: current CI does not provide stable credentials, models, or embeddings for those integrations, and the product path being gated today does not require them.
- plugin and playground capability code under optional or experimental backend paths
  Reason: these features are not part of the supported MVP runtime contract being enforced in this task.

Omission is temporary, not permanent. A backend file must move into the denominator when any of the following becomes true:

- the route is linked from the supported UI or CLI flow
- the feature becomes part of the contest-path or post-contest supported product contract
- deterministic fixtures are added so the module can be tested in CI without live external dependencies

## Audit Notes From This Task

Truthful test authoring exposed two backend behavior issues that were corrected instead of being encoded as false expectations:

- `deeptutor/api/routers/unified_ws.py`
  Invalid `after_seq` and `seq` values now return structured WebSocket errors instead of crashing through an unhandled `ValueError`.
- `deeptutor/api/routers/question.py`
  Parsed-mode mimic generation now rejects whitespace-only `paper_path` values after normalization instead of accepting them as if a real directory path was supplied.

## Change Policy

When updating this scope:

1. update this document first
2. update `scripts/run_backend_coverage_gate.sh` to match
3. update CI so GitHub Actions runs the same command
4. do not remove an in-scope module only to rescue the percentage; document the product-path reason or add tests instead
