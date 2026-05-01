# Task Packet: Backend Test Coverage Gate

- Task ID: `T052_BACKEND_TEST_COVERAGE_GATE`
- Commit tag: `T052-COVERAGE`
- Date: 2026-05-01
- Branch: `fix/backend-test-coverage-gate`
- Status: spec written

## Objective

Raise the backend quality bar so the repository has one authoritative backend test command that must both pass and report at least 80% coverage on the in-scope backend surface, with that gate enforced in CI and backed by a documented omit list for backend modules not used on the current product path.

## User-Approved Scope

- add a backend coverage gate of at least `80%`
- make the backend CI job fail when tests fail or in-scope coverage drops below `80%`
- review backend logic while adding or expanding tests; if the current logic is wrong, fix the logic instead of forcing tests to encode the bug
- define a documented backend omit list for services, features, adapters, or modules that are not used in the current supported product path
- ensure omitted backend files do not count toward the `80%` target only when the omission has a concrete justification tied to current usage
- keep the scope backend-first; frontend build/lint flow is out of scope except for preserving the existing CI workflow structure

## Owned Files

- `pyproject.toml`
- `.github/workflows/tests.yml`
- `deeptutor/api/**/*.py`
- `deeptutor/core/**/*.py`
- `deeptutor/knowledge/**/*.py`
- `deeptutor/runtime/**/*.py`
- `deeptutor/services/**/*.py`
- any additional backend module under `deeptutor/**/*.py` that is corrected after test-driven audit during this task
- `tests/**/*.py`
- `docs/testing/BACKEND_COVERAGE_SCOPE.md`
- `docs/superpowers/tasks/2026-05-01-backend-test-coverage-gate.md`
- `docs/superpowers/specs/2026-05-01-backend-test-coverage-gate-design.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-01.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if the merged implementation changes repo-level operating rules

## Do-Not-Touch

- `web/**` frontend runtime files
- contest evidence bundles and screenshot artifacts under `docs/contest/**` and `ai_first/competition/**`
- dependency lockfiles unless a dependency change is strictly required for the coverage gate
- broad product-scope feature work unrelated to backend correctness or testability
- omitted backend modules that are intentionally out of scope for the current supported product path, except for documenting and configuring their exclusion

## Design Before Implementation

- Runtime behavior change: no direct end-user feature is required, but this task can change backend logic where test audit proves the current behavior is incorrect
- Approved spec:
  - `docs/superpowers/specs/2026-05-01-backend-test-coverage-gate-design.md`
- Current behavior:
  - CI runs a small set of backend test slices and compile checks, but there is no authoritative full backend pass/fail command with a coverage threshold
- Intended behavior change:
  - one reproducible backend command enforces both green tests and `>=80%` coverage on the audited in-scope backend surface
- Candidate approach A:
  - apply `80%` coverage to every backend-adjacent Python file with no exclusions
- Candidate approach B:
  - audit the currently used backend surface, document justified omissions, raise tests on the in-scope code, and fix any incorrect backend logic uncovered during the audit
- Chosen approach and reason:
  - approach B; it matches the request to avoid fake spec pressure, keeps the quality gate honest for the currently supported product path, and still allows explicit exclusion of inactive backend areas

## Required Code Reading

- Entry points/handlers to inspect:
  - `.github/workflows/tests.yml`
  - `deeptutor/api/main.py`
  - `deeptutor/api/routers/*.py`
- Primary logic/service/use-case modules to inspect:
  - `deeptutor/services/**/*.py`
  - `deeptutor/runtime/**/*.py`
  - `deeptutor/knowledge/**/*.py`
- Shared contracts/schemas/types to inspect:
  - `deeptutor/core/**/*.py`
  - request/response contracts touched by the currently routed API and WebSocket flows
- Adjacent or reused flows to inspect:
  - CLI, WebSocket, and teacher-first REST flows that currently represent the supported backend surface
  - optional agents, plugins, and playground-only modules that may be valid omit candidates
- Existing tests to inspect:
  - `tests/api/*.py`
  - `tests/core/*.py`
  - `tests/knowledge/*.py`
  - `tests/services/*.py`

## Impact Surface And Stop Conditions

- Expected affected areas:
  - backend coverage configuration
  - backend CI execution contract
  - backend test inventory and missing regression coverage
  - bounded backend logic fixes uncovered while writing truthful tests
  - the omit-list documentation for inactive or unsupported backend modules
- Files/modules likely to change:
  - `pyproject.toml`
  - `.github/workflows/tests.yml`
  - selected `tests/**/*.py`
  - selected `deeptutor/**/*.py`
  - `docs/testing/BACKEND_COVERAGE_SCOPE.md`
- Files/modules that must be reviewed even if they remain unchanged:
  - backend modules proposed for omission
  - supported routers and services that must stay inside the `80%` denominator
  - current CLI and WebSocket entry points
- Minimum validation paths before the task can stop:
  - the authoritative backend coverage command passes locally
  - CI runs the same or stricter backend command
  - omitted files are listed in one committed scope document with a usage-based reason for each omission
  - no currently supported backend route or service is silently excluded from coverage accounting
  - any logic bug discovered while writing tests is either fixed in scope or explicitly documented as a blocker
- What would count as a shallow fix for this task:
  - adding a global omit pattern that hides large parts of `deeptutor/` without a product-path audit
  - writing tests around obviously wrong logic just to raise the number
  - keeping CI on narrow slices while only local commands enforce coverage

## Acceptance Criteria

- backend CI fails if the in-scope backend test command fails
- backend CI fails if in-scope backend coverage is below `80%`
- the repository contains one committed document that defines:
  - which backend modules are in scope for the `80%` gate
  - which backend modules are omitted
  - why each omitted module is not part of the current supported product path
- tests added for this task reflect intended backend behavior, not current bugs
- any backend logic corrected during the audit remains bounded to the tested impact surface

## Required Tests

- `pytest --collect-only -q`
- `pytest --cov=deeptutor --cov-report=term-missing --cov-fail-under=80 -q`
- `python -m compileall deeptutor`
- `git diff --check`

## Manual Verification

- compare the omit list against the current served routes and supported teacher-first flows
- confirm any omitted adapter/plugin/service is genuinely inactive, optional, or not yet supported in the current product path
- confirm the final CI backend job uses the same coverage contract documented for local development

## Parallel-Work Notes

- create a dedicated runtime lane from `origin/main` before implementation starts
- record that runtime lane in `ai_first/ACTIVE_ASSIGNMENTS.md`
- do not mix this hardening task with unrelated product feature changes

## PR Architecture Note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should be updated only if the implementation changes the documented backend control flow or supported product-path boundaries.

## Handoff Notes

- This task is intentionally allowed to fix backend logic when truthful tests reveal defects.
- The omit list must be a first-class deliverable, not an inline comment hidden inside coverage config.
