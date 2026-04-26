# Feature Pod Task: Lane 6 Evaluation, Evidence, and Contest Readiness

Owner: Session-specific
Branch: `docs/evaluation-evidence-readiness`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Prepare the hybrid proof for repeated demo, validation, and contest evidence without changing product logic outside the validation contract.

## User-visible outcome

- The team has a repeatable acceptance flow for the hybrid teacher-authoring plus evidence-loop story.
- Demo artifacts, validation notes, and fallback runbooks stay current.
- Contest-facing materials do not overclaim beyond what the product actually proves.

## Owned files/modules

- `docs/contest/`
- `ai_first/evidence/`
- `docs/superpowers/pr-notes/`
- `docs/superpowers/tasks/2026-04-26-lane-6-evaluation-evidence-readiness.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/daily/2026-04-26.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`

## Do-not-touch files/modules

- `deeptutor/services/`
- `deeptutor/api/routers/`
- `web/app/`
- `web/components/`
- `ai_first/AI_OPERATING_PROMPT.md` unless the human explicitly requests an operating-layer update in this lane

## API/data contract

- This lane consumes the shipped behavior from other lanes and documents its proof.
- Demo and evidence artifacts must reflect actual repo-backed behavior, not aspirational roadmap claims.

## Acceptance criteria

- End-to-end hybrid-proof validation steps are documented and reproducible.
- Demo data, screenshots, checklist items, and fallback notes stay aligned.
- Contest artifacts explain limitations honestly.
- This lane does not mutate runtime/product code.

## Required tests

- Doc consistency checks as appropriate
- Any scripted smoke or reset command relevant to updated evidence
- `git diff --check`

## Manual verification

- Walk through the teacher-authoring plus evidence-loop demo story using current `main`.
- Confirm screenshots/checklists map to the current product.
- Confirm fallback notes cover incomplete lanes without misleading reviewers.

## Parallel-work notes

- This lane is docs/evidence-only.
- If product behavior appears inconsistent with docs, ask the human whether to block on the relevant product lane or document the current limitation explicitly.
- Do not “fix” runtime gaps from this lane.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is usually not updated in this lane unless a docs correction reveals the map is already stale.

## Handoff notes

- This is Session = Lane 6.
- Use current `main` as the only source of truth for contest evidence.
- Document reality, not desired future behavior.
