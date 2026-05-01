# Task Packet: Frontend Test Coverage Gate

- Task ID: `T053_FRONTEND_TEST_COVERAGE_GATE`
- Commit tag: `T053-COVERAGE`
- Date: 2026-05-02
- Branch: `fix/frontend-test-coverage-gate`
- Status: implemented locally

## Objective

Raise the frontend quality bar so the repository has one authoritative frontend test command that must both pass and report at least `80%` coverage on the in-scope teacher-first contest path, with that gate enforced in CI and backed by a documented omit list for frontend modules not used on the current supported product path.

## User-Approved Scope

- add a frontend coverage gate of at least `80%`
- count only frontend `unit/component` coverage in the gate; keep Playwright UI audits outside the coverage denominator
- make the frontend CI job fail when tests fail or in-scope coverage drops below `80%`
- review frontend logic while adding or expanding tests; if the current logic is wrong, fix the logic instead of forcing tests to encode the bug
- define a documented frontend omit list for routes, components, helpers, or features not used on the current teacher-first contest path
- use the teacher-first contest path as the frontend denominator for the first gated slice
- default to excluding non-path frontend surfaces only when the omission has a concrete usage-based reason
- adding `vitest` for truthful frontend line coverage is approved

## Owned Files

- `web/**`
- `.github/workflows/tests.yml`
- `docs/testing/FRONTEND_COVERAGE_SCOPE.md`
- `docs/superpowers/tasks/2026-05-02-frontend-test-coverage-gate.md`
- `docs/superpowers/specs/2026-05-02-frontend-test-coverage-gate-design.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-02.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if the merged implementation changes repo-level operating rules

## Do-Not-Touch

- `deeptutor/**` backend runtime files unless frontend test authoring proves a current contract bug that blocks truthful FE coverage and the task packet is updated first
- contest evidence bundles and screenshot artifacts under `docs/contest/**` and `ai_first/competition/**`
- dependency lockfiles unless a dependency change is strictly required for the frontend coverage gate
- broad product-scope feature work unrelated to frontend correctness or testability
- omitted frontend modules that are intentionally out of scope for the current supported product path, except for documenting and configuring their exclusion

## Design Before Implementation

- Runtime behavior change: no direct end-user feature is required, but this task can change frontend logic where test audit proves the current behavior is incorrect
- Approved spec:
  - `docs/superpowers/specs/2026-05-02-frontend-test-coverage-gate-design.md`
- Current behavior:
  - CI only verifies `next build` for the frontend job and the repository has no authoritative frontend line-coverage gate
- Intended behavior change:
  - one reproducible frontend command enforces both green tests and `>=80%` coverage on the audited in-scope teacher-first contest path
- Candidate approach A:
  - keep `node --test` and approximate frontend coverage without a real component-test runner
- Candidate approach B:
  - add `vitest`, audit the current teacher-first frontend path, document justified omissions, raise tests on the in-scope surface, and fix any incorrect frontend logic uncovered during the audit
- Chosen approach and reason:
  - approach B; it is the only path that gives truthful line coverage for React/Next frontend code, matches the approved teacher-first denominator, and keeps the number honest through a committed omit list

## Required Code Reading

- Entry points/handlers to inspect:
  - `.github/workflows/tests.yml`
  - `web/package.json`
  - `web/app/**/*.tsx`
- Primary logic/service/use-case modules to inspect:
  - `web/components/**/*.tsx`
  - `web/lib/**/*.ts`
  - any frontend presenter or state helper directly used on the teacher-first contest path
- Shared contracts/schemas/types to inspect:
  - shared frontend data types and API client helpers under `web/lib/**`
  - route/layout boundaries used by `Knowledge`, `Marketplace`, `Dashboard`, `Agents`, and `Playground`
- Adjacent or reused flows to inspect:
  - current `node:test` frontend tests under `web/tests`
  - Playwright UI audit coverage, but only as an adjacent non-denominator validation path
  - inactive or hidden frontend surfaces that may be valid omit candidates
- Existing tests to inspect:
  - `web/tests/*.test.ts`
  - any existing Playwright audit under `web/tests/e2e/**`

## Impact Surface And Stop Conditions

- Expected affected areas:
  - frontend test runner and coverage configuration
  - frontend CI execution contract
  - frontend test inventory and missing regression coverage
  - bounded frontend logic fixes uncovered while writing truthful tests
  - the omit-list documentation for inactive or unsupported frontend modules
- Files/modules likely to change:
  - `web/package.json`
  - frontend test runner/config files under `web/`
  - selected `web/**/*.ts` and `web/**/*.tsx`
  - selected frontend tests under `web/tests/**`
  - `.github/workflows/tests.yml`
  - `docs/testing/FRONTEND_COVERAGE_SCOPE.md`
- Files/modules that must be reviewed even if they remain unchanged:
  - frontend modules proposed for omission
  - the teacher-first contest-path routes and components that must stay inside the `80%` denominator
  - current Playwright audit and build hooks that should remain complementary, not replaced
- Minimum validation paths before the task can stop:
  - the authoritative frontend coverage command passes locally
  - CI runs the same or stricter frontend command
  - omitted files are listed in one committed scope document with a usage-based reason for each omission
  - no currently supported teacher-first frontend route or shared component is silently excluded from coverage accounting
  - any logic bug discovered while writing tests is either fixed in scope or explicitly documented as a blocker
- What would count as a shallow fix for this task:
  - adding a broad global omit pattern that hides large parts of `web/` without a product-path audit
  - writing source-string tests that inflate the number without exercising component or presenter behavior
  - keeping CI on `next build` only while local commands enforce coverage

## Acceptance Criteria

- frontend CI fails if the in-scope frontend test command fails
- frontend CI fails if in-scope frontend coverage is below `80%`
- the repository contains one committed document that defines:
  - which frontend modules are in scope for the `80%` gate
  - which frontend modules are omitted
  - why each omitted module is not part of the current supported product path
- tests added for this task reflect intended frontend behavior, not current bugs
- any frontend logic corrected during the audit remains bounded to the tested impact surface
- Playwright audit coverage remains a separate validation layer and is not used to satisfy the line-coverage denominator

## Required Tests

- `cd web && npm run test:coverage:frontend`
- `cd web && npm run build`
- `git diff --check`

## Manual Verification

- compare the omit list against the current teacher-first contest flow in the frontend shell
- confirm any omitted route/component/helper is genuinely inactive, hidden, optional, or outside the current supported product path
- confirm the final CI frontend job uses the same coverage contract documented for local development

## Parallel-Work Notes

- create a dedicated runtime lane from `origin/main` before implementation starts
- record that runtime lane in `ai_first/ACTIVE_ASSIGNMENTS.md`
- do not mix this hardening task with unrelated product feature changes

## PR Architecture Note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should be updated only if the implementation changes the documented teacher-first frontend flow or supported product-path boundaries.

## Handoff Notes

- This task is intentionally allowed to fix frontend logic when truthful tests reveal defects.
- The omit list must be a first-class deliverable, not an inline comment hidden inside coverage config.
- Local implementation lane reached `33 passed` with `88.35%` in-scope frontend coverage through `cd web && npm run test:coverage:frontend`, while preserving `cd web && npm run build` as a separate required frontend validation step.
