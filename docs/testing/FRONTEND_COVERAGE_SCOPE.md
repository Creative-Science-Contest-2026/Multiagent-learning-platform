# Frontend Coverage Scope

The authoritative frontend coverage gate for this repository is:

```bash
cd web && npm run test:coverage:frontend
```

That command is the single source of truth for:

- which frontend `unit/component` tests must pass
- which frontend modules count toward the line-coverage denominator
- the minimum accepted frontend coverage threshold of `80%`

Playwright audits remain useful, but they are not part of the line-coverage denominator for this gate.

## In-Scope Frontend Surface

The first gated denominator follows the current teacher-first contest path through behavior-bearing seams that are stable under unit/component testing:

- `web/components/dashboard/dashboard-presenters.ts`
- `web/components/agents/class-tutor-pack-presenters.ts`
- `web/components/sidebar/nav-groups.ts`
- `web/components/contest/teacher-cockpit-content.ts`
- `web/lib/api.ts`
- `web/lib/markdown-display.ts`
- `web/lib/playground-trace.ts`

These files were chosen because they directly shape the current teacher-first contest flow across:

- `Knowledge`
- `Dashboard`
- `Agents`
- `Marketplace`
- `Playground`

and they expose deterministic user-facing behavior that can be covered truthfully with frontend unit tests.

## Authoritative Test Inventory

The current frontend gate requires these tests:

- `web/tests/api-base-url.test.ts`
- `web/tests/class-tutor-pack-presenters.test.ts`
- `web/tests/knowledge-page-wizard-shell.test.ts`
- `web/tests/markdown-display.test.ts`
- `web/tests/playground-trace.test.ts`
- `web/tests/sidebar-nav-groups.test.ts`
- `web/tests/teacher-cockpit-content.test.ts`
- `web/tests/teacher-dashboard-copy.test.ts`
- `web/tests/teacher-dashboard-decision-flow.test.ts`

## Explicitly Omitted Frontend Areas

The following frontend areas do not count toward the first `80%` gate yet:

- `web/app/(workspace)/guide/**`
- `web/app/(workspace)/co-writer/**`
- `web/app/(utility)/memory/**`
- `web/components/math-animator/**`
- `web/components/research/**`
- `web/components/visualize/**`
- notebook-only helpers and pickers not used on the current teacher-first contest path
- large route-shell files such as `web/app/(utility)/knowledge/page.tsx`, `web/app/(utility)/marketplace/page.tsx`, `web/app/(workspace)/dashboard/page.tsx`, `web/app/(workspace)/agents/page.tsx`, and `web/app/(workspace)/playground/page.tsx`

Reasons:

- some surfaces are hidden, optional, dormant, or outside the current supported teacher-first contest flow
- some route shells are still composition-heavy pages whose current coverage value would be dominated by framework wiring rather than stable business behavior
- this first gate is intentionally limited to truthful `unit/component` coverage, not broad page-file execution

Omission is temporary, not permanent. A frontend file should move into the denominator when any of the following becomes true:

- it becomes part of the supported teacher-first contest path
- it gains a stable behavior seam that can be tested truthfully under Vitest
- it is no longer primarily framework composition glue and can be covered without fake render/setup scaffolding

## Complementary Validation Outside The Denominator

The following checks still matter, but do not satisfy the line-coverage target:

- `cd web && npm run build`
- Playwright audits such as `npm run audit`
- shell/source invariant tests that validate route text or hidden wiring without executing the page module itself

## Audit Notes From This Task

- The previous frontend tests were mostly `node:test` files without a real coverage-producing runner.
- The first frontend gate migrates the current teacher-first seams to Vitest rather than pretending source-string tests are enough to cover every page file.
- The initial coverage report crossed the threshold with a real denominator instead of broad undocumented excludes.

## Change Policy

When updating this scope:

1. update this document first
2. update `web/vitest.config.ts` so its `test.include` and `coverage.include` match the documented denominator
3. update CI so GitHub Actions runs the same command
4. do not remove an in-scope module only to rescue the percentage; document the product-path reason or add tests instead
