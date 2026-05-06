# Task Packet: L1 Build Hygiene Productization

- Task ID: `L1_BUILD_HYGIENE`
- Commit tag: `L1-BUILD`
- Branch: `fix/build-hygiene-productization`
- Worktree: `.worktrees/fix-build-hygiene-productization`
- Depends on: none

## Goal

Make the web app build clean on a clean machine and remove test/dev configuration bleed-through from the production compile path.

## Why This Lane Exists

Current `main` is blocked by build hygiene issues, including `vitest.config.ts` being included in the app compile path. This must be fixed before the wider beta-productization train can proceed safely.

## Owned Files

- `web/tsconfig.json`
- `web/vitest.config.ts`
- `web/package.json`
- `web/package-lock.json` only if dependency changes are truly required
- `web/next.config.*`
- `web/next-env.d.ts` only if required by the build fix
- `docs/superpowers/pr-notes/2026-05-06-l1-build-hygiene-productization.md`
- `ai_first/daily/2026-05-06.md`

## Do Not Touch

- product route structure
- backend routers/services
- auth/runtime logic
- classroom/assignment domain files

## Required Outcomes

- `cd web && npm run build` passes on this lane
- production compile path excludes Vitest-only config/types
- dependency boundaries between runtime and dev/test tooling are explicit
- any root/workspace lockfile ambiguity that affects Next build is either fixed or intentionally documented

## Validation

- `cd web && npm run build`
- `git diff --check`

## PR Scope

This PR must stay strictly about build/release hygiene. No product feature work.
