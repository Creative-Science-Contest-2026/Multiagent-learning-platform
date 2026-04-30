# 2026-04-30 C219 Classroom Case Study And Bounded Metric Card

- Task ID: `C219_CLASSROOM_CASE_STUDY_AND_BOUNDED_METRIC_CARD`
- Commit tag: `C219`
- Branch: `docs/classroom-case-study-metric-card`
- Worktree: `.worktrees/classroom-case-study-metric-card`
- Status: `pending`

## Goal

Package one explicit classroom case study plus one compact, non-overclaim metric card so the contest story stays anchored to a single teacher workflow instead of a long feature list.

## User-visible outcome

- Judges and human reviewers can follow one concrete classroom scenario end to end.
- The repo exposes a small, safe metric set that clarifies what is actually evidenced today.
- The contest narrative becomes easier to present without inventing outcome claims or benchmark language.

## Owned files

- `docs/contest/DEMO_SCRIPT.md`
- `docs/contest/README.md`
- `docs/contest/CASEPACK_AND_EVALUATION_DATASET.md`
- `docs/contest/VALIDATION_REPORT.md`
- `ai_first/competition/product-description.md`
- `ai_first/competition/pitch-notes.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-c219-classroom-case-study-and-bounded-metric-card.md`
- `docs/superpowers/pr-notes/2026-04-30-c219-classroom-case-study-and-bounded-metric-card.md`

## Do-not-touch

- `web/`
- `deeptutor/`
- `ai_first/evidence/casepack.json`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `README.md`
- `AGENTS.md`
- lockfiles and generated files

## Execution notes

- Keep the task docs-only. Do not modify runtime code, seeded demo data, screenshots, or machine-readable evidence artifacts.
- Reuse the existing demo-safe classroom scenario centered on `contest-demo-quadratics` unless the current docs already prove a cleaner single case without adding new claims.
- The target output is not a benchmark section. It is a bounded presenter/reviewer aid that answers:
  - what one teacher is teaching;
  - what one student weakness pattern looks like;
  - what the tutor and dashboard contribute inside the same loop;
  - what narrow metrics are currently backed by repo evidence.
- Prefer metric language that is operational and evidence-backed, for example:
  - demo loop stages completed in the current smoke run;
  - count of demo-safe sessions verified;
  - whether Knowledge Pack grounding was present in verified session payloads;
  - whether teacher recommendation/intervention surfaces are present in the documented flow.
- Explicitly reject metrics that would overclaim, such as diagnosis accuracy, learning gain, classroom outcome improvement, or pilot-scale effectiveness.
- If a stronger metric would require new runtime instrumentation or refreshed browser captures, record that as a future note instead of widening this packet.

## Acceptance criteria

- `DEMO_SCRIPT.md` contains one explicit classroom case-study framing that presenters can reuse consistently.
- `README.md`, `pitch-notes.md`, and `product-description.md` no longer rely only on abstract loop language; they also point to one bounded scenario.
- `CASEPACK_AND_EVALUATION_DATASET.md` and/or `VALIDATION_REPORT.md` expose a compact metric card or equivalent section that states what is evidenced today and what is intentionally not claimed.
- No benchmark, outcome-study, or autonomous-accuracy wording is introduced.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `rg -n "case study|metric|bounded|non-overclaim|grounding|contest-demo-quadratics|validated prototype|not a benchmark|not a classroom outcome" docs/contest ai_first/competition docs/superpowers/tasks docs/superpowers/pr-notes`

## Manual verification

- Read `docs/contest/README.md` top to bottom and confirm a reviewer can repeat one classroom story without needing oral explanation.
- Read `docs/contest/DEMO_SCRIPT.md` and confirm the presenter can point to one scenario, one weakness pattern, and one teacher action.
- Read the metric section and confirm every line is backed by existing smoke or casepack evidence rather than desired future proof.

## Parallel-work notes

- This packet should assume `C216-C218` may independently improve shell, entry, and wording, but it must remain valid even if those tasks are not yet executed.
- Do not recapture screenshots or rewrite evidence freshness state here; that remains separate from this narrative packaging pass.
- If the worker concludes that the current docs already contain enough case-study material but it is scattered, solve that by consolidation and cross-linking, not by inventing new examples.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not expected to change because this task is documentation and evidence framing only.

## Handoff

- After this packet, the differentiation follow-up set is fully packetized: `C216`, `C217`, `C218`, and `C219` can now be executed independently with bounded scope.
