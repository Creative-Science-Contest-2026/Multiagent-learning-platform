# Frontend Test Coverage Gate Design

- Date: 2026-05-02
- Task ID: `T053_FRONTEND_TEST_COVERAGE_GATE`
- Target branch: `fix/frontend-test-coverage-gate`

## Goal

Establish a trustworthy frontend quality gate for this repository: the audited in-scope teacher-first contest path must have at least `80%` automated `unit/component` coverage, that same gate must run in CI, and any frontend logic that proves incorrect during test authoring should be corrected rather than defended by brittle specs.

## Current Behavior

- `web/package.json` exposes `next build`, lint, i18n scripts, and Playwright UI audits, but it does not define an authoritative frontend line-coverage command.
- `.github/workflows/tests.yml` currently treats the frontend job as a build-only check.
- The repository already has focused frontend tests under `web/tests/*.test.ts`, but most of them run with `node:test` and do not produce React/TSX line coverage suitable for a strict `80%` gate.
- Playwright is installed and used for UI audit flows, but Playwright is not an appropriate replacement for deterministic component-level line coverage.
- The frontend codebase includes the current teacher-first contest path plus hidden, optional, or non-primary surfaces that should not automatically count toward the first denominator.

## Intended Behavior Change

- The repository should have one explicit frontend coverage contract that developers and CI both use.
- The frontend denominator should reflect the teacher-first contest path rather than every dormant or hidden route in `web/`.
- Omitted frontend modules should be listed in one committed document with usage-based reasons, not hidden inside ad hoc coverage flags.
- Playwright should remain a complementary smoke/audit layer, not the mechanism used to satisfy the coverage percentage.
- When test expansion reveals incorrect frontend logic, the task should fix that logic inside the bounded impact surface instead of forcing tests to preserve the defect.

## Codebase Survey

### Entry points and handlers

- `.github/workflows/tests.yml`
  - current frontend CI contract and install path
- `web/package.json`
  - current test/build scripts and missing coverage command
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/marketplace/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/playground/page.tsx`
  - current teacher-first contest-path route surfaces

### Primary service or use-case modules

- `web/components/dashboard/**`
- `web/components/agents/**`
- `web/components/sidebar/**`
- `web/components/contest/**`
- `web/components/chat/home/**`
- `web/lib/**`
  - presenter, formatting, client, and UI state helpers that shape the teacher-first experience

### Shared contracts, schemas, or types

- frontend API client helpers under `web/lib/*.ts`
- route/layout boundaries under `web/app/(utility)` and `web/app/(workspace)`
- locale-driven and presenter-driven teacher-facing label helpers

### Adjacent or reused flows inspected

- current `node:test` files under `web/tests/*.test.ts`
- `web/playwright.config.ts` and `web/tests/e2e/**`
- non-primary frontend surfaces such as `guide`, `co-writer`, `memory`, `math-animator`, `research`, `visualize`, and notebook helpers that may be valid omit candidates

### Closest existing tests

- `web/tests/teacher-dashboard-copy.test.ts`
- `web/tests/teacher-dashboard-decision-flow.test.ts`
- `web/tests/knowledge-page-wizard-shell.test.ts`
- `web/tests/contest-terminology.test.ts`
- `web/tests/class-tutor-pack-presenters.test.ts`
- `web/tests/sidebar-nav-groups.test.ts`
- `web/tests/sidebar-shell-layout.test.ts`
- other current `web/tests/*.test.ts` helpers

## Candidate Approaches

### Approach A: Keep `node:test` and approximate coverage without a real React test runner

- Preserve the current style of frontend tests and try to derive coverage from helper-level or source-string checks.
- Pros:
  - minimal dependency churn
  - lowest setup cost
- Cons:
  - weak fit for TSX/component coverage
  - likely produces shallow tests instead of truthful UI behavior checks
  - difficult to make an honest `80%` line gate stable in CI

### Approach B: Add `vitest` for frontend coverage, audit the teacher-first path, document omissions, and raise tests on the in-scope surface

- Introduce `vitest` plus the minimum supporting config needed for React/Next-friendly frontend coverage, migrate or wrap the current frontend tests into a real coverage-producing runner, then add/expand tests on the audited teacher-first path while documenting omissions explicitly.
- Pros:
  - truthful line coverage for React/TSX code
  - stable CI contract
  - aligns with the approved teacher-first denominator
  - allows gradual migration from current `node:test` files
- Cons:
  - requires test-runner setup and likely some test harness utilities
  - broader up-front setup than a build-only job

### Approach C: Use Playwright as the main coverage mechanism

- Expand browser audits and rely on that for the frontend percentage.
- Pros:
  - exercises real rendered flows
  - useful as a smoke layer
- Cons:
  - poor fit for line coverage gates
  - slower and more fragile in CI
  - does not address presenter/helper/component-level regression confidence

## Chosen Approach

Approach B.

It is the only approach that satisfies all approved constraints simultaneously:

- `80%` frontend coverage must be a real gate in CI
- only `unit/component` coverage should count toward that percentage
- the denominator should stay bounded to the current teacher-first contest path
- omitted frontend modules may be excluded only through an explicit and reviewable audit

## Planned Changes

- add committed frontend coverage-scope documentation under `docs/testing/FRONTEND_COVERAGE_SCOPE.md`
- add `vitest` plus the minimum frontend coverage configuration under `web/`
- add an authoritative frontend coverage command in `web/package.json`
- update the frontend CI job in `.github/workflows/tests.yml` to run the same or stricter frontend gate used locally
- audit current frontend tests and migrate or expand the most important teacher-first coverage slices
- correct bounded frontend logic defects uncovered during truthful test authoring
- keep omitted frontend modules explicit and reviewable instead of relying on undocumented globs

## Expected Impact Surface

### Likely to change

- `web/package.json`
- `web/` test runner/config files such as `vitest.config.*`, setup files, or typed test helpers
- selected frontend modules under `web/app/**`, `web/components/**`, and `web/lib/**`
- selected tests under `web/tests/**`
- `.github/workflows/tests.yml`
- `docs/testing/FRONTEND_COVERAGE_SCOPE.md`

### Reviewed but expected to remain unchanged

- `deeptutor/**` backend runtime code
- contest docs and screenshot artifacts
- Playwright audit scripts except where a command reference or CI boundary needs clarification
- dependency lockfiles unless the coverage runner setup strictly requires lockfile updates

## In-Scope Denominator Policy

The first gated frontend denominator should follow the current teacher-first contest path:

- `Knowledge`
- `Marketplace`
- `Dashboard`
- `Agents`
- `Playground`
- shared shell, presenter, locale, and client helpers directly used by those surfaces

The denominator should prefer behavior-bearing frontend code, not every static or dormant route in the repository.

## Omit-List Policy

Frontend modules may be excluded from the first `80%` denominator only when all of the following are true:

- they are frontend modules
- they are not part of the current teacher-first contest path
- they are hidden, optional, dormant, admin-only, or otherwise outside the currently supported product flow
- the exclusion is documented in `docs/testing/FRONTEND_COVERAGE_SCOPE.md` with a concrete reason

Likely omit candidates to verify during implementation, not pre-approved blanket exclusions:

- `guide`
- `co-writer`
- `memory`
- `math-animator`
- `research`
- `visualize`
- notebook-related helpers and pickers not used on the current teacher-first path

## Test Strategy

- keep Playwright outside the coverage denominator
- prioritize presenter/helper/component tests that exercise actual behavior instead of source-text assertions wherever practical
- migrate existing frontend `node:test` coverage slices into `vitest` where that unlocks truthful line coverage
- add route-shell and state-logic regression tests only for the audited in-scope teacher-first surfaces
- if a current frontend test is purely a static-source guard and remains the best bounded check for a deliberate shell invariant, keep it only when there is no honest runtime alternative

## Tests To Run

- `cd web && npm run test:coverage:frontend`
- `cd web && npm run build`
- `git diff --check`

## Non-Goals

- no attempt to force every historical or hidden frontend surface into the first `80%` gate
- no replacement of Playwright audits with unit coverage
- no fake coverage achieved through broad undocumented exclusions
- no preservation of incorrect frontend behavior just because it existed before the test audit
