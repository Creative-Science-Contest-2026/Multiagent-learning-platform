# L1 Build Hygiene Productization Design

- Date: 2026-05-06
- Lane: `L1_BUILD_HYGIENE`
- Status: approved for implementation inside this lane

## Current Behavior

- `web/tsconfig.json` includes all `**/*.ts` and `**/*.tsx` under `web/`
- `web/vitest.config.ts` therefore participates in the app TypeScript compile path
- on a machine with `web` dependencies installed, `next build` reaches TypeScript and fails trying to resolve `vitest/config`
- in a fresh isolated worktree, `web` dependencies are absent until installed, so the first failure can present as `next: command not found`

## Intended Behavior Change

- production build should compile only app/runtime-relevant files
- Vitest-only config should not be part of the Next app compile path
- the lane should preserve existing frontend test behavior while making `cd web && npm run build` pass on a clean machine after dependencies are installed

## Candidate Approaches

### Approach A: Exclude test config from app tsconfig

- narrow `web/tsconfig.json` include/exclude so `vitest.config.ts` and other test-only config files do not enter the Next compile path
- keep Vitest config file name and location unchanged

Pros:

- minimal and explicit
- low risk to existing test commands
- preserves current dev ergonomics

Cons:

- requires careful include/exclude hygiene so no runtime files are accidentally excluded

### Approach B: Move or rename Vitest config into a separate config namespace

- move `vitest.config.ts` to a location or name outside the default Next app compile path
- adjust scripts if needed

Pros:

- strong separation between app and test config

Cons:

- larger mechanical change
- more likely to affect test tooling, docs, and future lanes unnecessarily

## Chosen Approach

Chosen: `Approach A`

Reason:

- this lane should fix the blocker with the smallest useful surface area
- the problem is compile-path leakage, not the existence of Vitest itself
- adjusting `tsconfig` boundaries is sufficient unless investigation reveals a second root cause

## Expected Files To Change

- `web/tsconfig.json`
- `web/package.json` only if build/test commands need bounded clarification
- `web/vitest.config.ts` only if a minimal companion tweak is necessary
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-06.md`

## Files Reviewed But Expected To Remain Unchanged

- `web/app/**`
- backend services and routers
- product route shells
- auth/session/classroom domain modules

## Validation Plan

- install dependencies in the isolated `web` worktree
- reproduce failing `cd web && npm run build`
- apply the smallest compile-path fix
- rerun `cd web && npm run build`
- run a focused frontend test command to ensure Vitest config still works
- run `git diff --check`
