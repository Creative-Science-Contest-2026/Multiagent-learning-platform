# Task Packet: Code Review Graph Integration

- Task ID: `OPS_CODE_REVIEW_GRAPH_INTEGRATION`
- Date: 2026-04-30
- Branch: `fix/code-review-graph-integration`
- Status: Spec written

## Objective

Install `code-review-graph`, configure this repository for Codex, and commit the repo-local integration files plus `.code-review-graph/` if the tool creates that artifact during the initial build.

## User-Approved Scope

- integrate `code-review-graph` directly into this repository on a dedicated lane
- use a separate worktree and branch
- commit generated `.code-review-graph/` if it appears
- keep the integration bounded to Codex-facing repo configuration and initial graph build

## Owned Files

- `.gitignore`
- `.claude/skills/`
- `.code-review-graph/`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-code-review-graph-integration.md`
- `docs/superpowers/specs/2026-04-30-code-review-graph-integration-design.md`
- `docs/superpowers/plans/2026-04-30-code-review-graph-integration.md`
- `docs/superpowers/pr-notes/2026-04-30-code-review-graph-integration.md`

## Do-Not-Touch

- unrelated runtime/product files
- the active `/playground` lane in the repo root worktree
- dependency lockfiles unless the installation path forces a tracked change inside this repo

## Design Before Implementation

- `docs/superpowers/specs/2026-04-30-code-review-graph-integration-design.md`

## Validation Plan

- `~/Library/Python/3.12/bin/code-review-graph install --platform codex`
- `~/Library/Python/3.12/bin/code-review-graph build`
- `~/Library/Python/3.12/bin/code-review-graph status`
- `git diff --check`
