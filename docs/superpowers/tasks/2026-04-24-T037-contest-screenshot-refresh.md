# Feature Pod Task: Contest Screenshot Evidence Refresh

Owner: Codex
Branch: `docs/t037-contest-screenshot-refresh`
GitHub Issue: `#97`

## Goal

Refresh the contest screenshot bundle so `docs/contest/EVIDENCE_CHECKLIST.md` can move screenshot evidence from `Stale` back to `Current`.

## User-visible outcome

- Knowledge, Assessment, Tutor, and Dashboard screenshots reflect the latest merged UI.
- Contest evidence docs can honestly mark screenshot entries as `Current`.
- The evidence packet no longer depends on an outdated screenshot bundle.

## Owned files/modules

- `docs/contest/screenshots/*`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/superpowers/tasks/2026-04-24-T037-contest-screenshot-refresh.md`
- `docs/superpowers/pr-notes/` for the screenshot-refresh PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Product/runtime source files unless screenshot capture exposes a real product defect that must be fixed first
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless the screenshot lane unexpectedly changes runtime/product architecture
- Root license and upstream attribution files

## Evidence contract

- Reuse the latest command-backed smoke baseline from `T036`.
- Capture or regenerate the screenshot bundle for:
  - Knowledge metadata
  - Knowledge after reload
  - Assessment config
  - Assessment generated questions
  - Assessment common mistakes
  - Tutor answer
  - Dashboard summary and activity
- Update screenshot statuses only after fresh files are produced and reviewed.

## Acceptance criteria

- Every screenshot linked from `docs/contest/EVIDENCE_CHECKLIST.md` is freshly captured against the latest merged UI.
- Screenshot status can move from `Stale` to `Current`.
- Contest validation docs mention the screenshot refresh date and source lane.
- AI-first tracking reflects `T037` as the active short task.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T037|Current|Stale|screenshot" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## Manual verification

- Open each linked screenshot and confirm it matches the current UI.
- Confirm all screenshot links in `EVIDENCE_CHECKLIST.md` point at refreshed files.
- Confirm no private data or credentials appear in the new captures.

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T036` merged to `main` through PR `#96` and refreshed command-backed smoke evidence.
- Screenshot freshness was picked up again on 2026-04-25 in `docs/t037-contest-screenshot-refresh-pass` after the `T044` through `T051` UI rollout changed the contest-facing screens.
- The refreshed `07` and `08` captures use demo-safe local session content in the worktree data store because provider-backed quiz generation was unavailable with the placeholder local API key.
