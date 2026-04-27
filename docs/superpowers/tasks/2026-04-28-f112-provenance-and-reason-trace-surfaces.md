# Task Packet: F112_PROVENANCE_AND_REASON_TRACE_SURFACES

- Task ID: `F112_PROVENANCE_AND_REASON_TRACE_SURFACES`
- Commit tag: `F112`
- Owner: `Codex Session A`
- Status: `in-progress`
- Branch: `pod-a/provenance-reason-traces`

## Objective

Expose bounded provenance and reason traces for teacher-facing trust without overclaiming full explainability.

## Scope

- Reuse existing runtime-policy audit data for `/agents`.
- Reuse existing diagnosis evidence and teacher-review framing for dashboard trust surfaces.
- Add only bounded read-only payload shaping where current APIs do not provide enough structure.

## Owned Files

- `web/components/dashboard/`
- `web/components/agents/`
- `web/app/(workspace)/agents/`
- `web/lib/dashboard-api.ts`
- `web/lib/agent-spec-api.ts`
- `deeptutor/services/evidence/teacher_insights.py`
- bounded read-only dashboard/agent-spec API tests
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- `docs/superpowers/pr-notes/`
- `ai_first/daily/2026-04-28.md`

## Do-Not-Touch

- `deeptutor/services/session/`
- mutable runtime execution semantics
- class-roster lifecycle or teacher-ownership write paths
- broader `/agents` authoring workflow beyond a bounded audit/trust surface

## Acceptance Criteria

1. `/agents` can show a bounded runtime-policy audit surface for the selected spec pack.
2. Student insight detail shows a bounded trust trace built from real evidence fields and teacher-review framing.
3. Small-group cards show a bounded reason trace derived from existing grouped evidence, not generic copy only.
4. No new claim implies full explainability or autonomous correctness.
5. `MAIN_SYSTEM_MAP.md` and PR note describe the new trust surfaces.

## Validation

- targeted dashboard/agent-spec API tests
- targeted frontend lint for touched files
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
