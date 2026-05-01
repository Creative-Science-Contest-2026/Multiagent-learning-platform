# Backend Test Coverage Gate Design

- Date: 2026-05-01
- Task ID: `T052_BACKEND_TEST_COVERAGE_GATE`
- Target branch: `fix/backend-test-coverage-gate`

## Goal

Establish a trustworthy backend quality gate for this repository: the audited in-scope backend surface must have at least `80%` automated test coverage, that same gate must run in CI, and any backend logic that proves incorrect during test authoring should be corrected rather than defended by brittle specs.

## Current Behavior

- `pyproject.toml` configures pytest markers and options, but it does not define an authoritative coverage scope or threshold.
- `.github/workflows/tests.yml` installs `pytest-cov` but the backend job only runs a hand-picked slice of backend tests plus `compileall`.
- The repository already has meaningful backend tests under `tests/api`, `tests/core`, `tests/knowledge`, `tests/services`, and other folders, but there is no single pass/fail backend contract that combines coverage and correctness.
- The backend codebase includes currently served routes and services, plus optional agents, plugins, adapters, and playground-oriented modules that may not belong in the immediate `80%` denominator.
- The current control plane does not yet document which backend modules are intentionally out of scope for the present product path.

## Intended Behavior Change

- The repository should have one explicit backend coverage contract that developers and CI both use.
- The in-scope backend denominator should reflect the current supported product path rather than every dormant or optional backend module in the repository.
- Omitted backend modules should be listed in one committed document with usage-based reasons, not hidden inside ad hoc coverage flags.
- When test expansion reveals incorrect backend logic, the task should fix the logic inside the bounded impact surface instead of forcing tests to preserve the defect.

## Codebase Survey

### Entry points and handlers

- `.github/workflows/tests.yml`
  - current CI backend contract and install path
- `deeptutor/api/main.py`
  - mounted backend application entry point
- `deeptutor/api/routers/*.py`
  - current HTTP and WebSocket route surfaces that define the product path

### Primary service or use-case modules

- `deeptutor/services/**/*.py`
  - current service layer for settings, runtime policy, session, evidence, assessment, agent spec, and knowledge flows
- `deeptutor/runtime/**/*.py`
  - runtime bootstrap and registry paths that may need explicit coverage
- `deeptutor/knowledge/**/*.py`
  - knowledge-pack lifecycle and progress logic already partially covered by tests

### Shared contracts, schemas, or types

- `deeptutor/core/**/*.py`
  - shared protocols, request contracts, stream events, and cross-cutting runtime helpers
- request/response models flowing between routers and service helpers

### Adjacent or reused flows inspected

- CLI and WebSocket flows that reuse backend services and may need to remain in scope
- optional or inactive surfaces under agents, plugins, and certain adapters that may be valid omit candidates only after explicit audit
- existing scripts and test helpers that already exercise parts of the supported backend path

### Closest existing tests

- `tests/api/*.py`
- `tests/core/*.py`
- `tests/knowledge/*.py`
- `tests/services/*.py`
- `tests/scripts/*.py`

## Candidate Approaches

### Approach A: Apply `80%` to all Python backend-adjacent files immediately

- Count every backend-side module under `deeptutor/` toward the threshold with no exclusions.
- Pros:
  - simple to explain
  - no omit-list governance work
- Cons:
  - likely punishes inactive or optional surfaces that are not part of the current supported product path
  - encourages artificial tests or broad exemptions later
  - conflicts with the request to avoid forcing spec around the wrong target

### Approach B: Audit the supported backend path, document justified omissions, then gate the in-scope surface at `80%`

- Inventory the currently supported backend routes and services, identify inactive or currently unused backend modules, document the omit list, then raise test coverage and fix any uncovered logic defects on the in-scope surface before wiring the threshold into CI.
- Pros:
  - matches the current product reality
  - keeps the quality number honest
  - supports bounded logic fixes when tests reveal defects
  - gives future workers a documented path for moving omitted modules back into scope
- Cons:
  - requires an upfront audit and a maintained scope document
  - more review work than a pure config change

### Approach C: Keep the current slice tests and add only a non-blocking coverage report

- Preserve the current CI structure, emit coverage information, but do not fail the build on threshold.
- Pros:
  - lowest immediate disruption
  - easier to merge quickly
- Cons:
  - does not satisfy the request
  - preserves the gap between local expectations and CI enforcement
  - leaves correctness and coverage drift ungoverned

## Chosen Approach

Approach B.

It is the only approach that satisfies all three user constraints simultaneously:

- `80%` coverage must be a real gate in CI
- tests must reflect correct logic rather than preserving bad behavior
- backend modules not used on the current supported path may be excluded, but only through an explicit and reviewable audit

## Planned Changes

- add committed backend coverage-scope documentation under `docs/testing/BACKEND_COVERAGE_SCOPE.md`
- add authoritative coverage configuration in `pyproject.toml`
- update the backend CI job in `.github/workflows/tests.yml` to run the same or stricter backend gate used locally
- audit existing backend tests and fill the most important coverage gaps on in-scope modules
- correct bounded backend logic defects uncovered during truthful test authoring
- keep omitted backend modules explicit and reviewable instead of relying on undocumented glob drift

## Expected Impact Surface

### Likely to change

- `pyproject.toml`
- `.github/workflows/tests.yml`
- selected backend modules under `deeptutor/**/*.py`
- selected tests under `tests/**/*.py`
- `docs/testing/BACKEND_COVERAGE_SCOPE.md`

### Reviewed but expected to remain unchanged

- `web/**`
- contest docs and screenshot artifacts
- dependency lockfiles unless tooling changes prove strictly necessary
- omitted backend modules whose only required change is documentation and coverage exclusion

## Omit-List Policy

Modules may be excluded from the `80%` denominator only when all of the following are true:

- they are backend modules
- they are not part of the current supported product path
- they are not required by the current CI-backed CLI, REST, or WebSocket flows
- the exclusion is documented in `docs/testing/BACKEND_COVERAGE_SCOPE.md` with a concrete reason

Likely omit candidates to verify during implementation, not pre-approved blanket exclusions:

- playground-only or dormant plugin modules
- optional agent surfaces not used in the current teacher-first workflow
- machine-specific or optional integration adapters that are not reachable on the current product path

## Tests To Run

- `pytest --collect-only -q`
- `pytest --cov=deeptutor --cov-report=term-missing --cov-fail-under=80 -q`
- `python -m compileall deeptutor`
- `git diff --check`

## Non-Goals

- no frontend redesign or frontend coverage gate changes in this task
- no fake coverage achieved through broad undocumented omissions
- no attempt to force every historical or experimental backend module into the first `80%` gate
- no preservation of incorrect backend behavior just because it existed before the test audit
