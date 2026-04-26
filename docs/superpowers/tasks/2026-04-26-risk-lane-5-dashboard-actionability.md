# Feature Pod Task: Risk Lane 5 Dashboard Actionability

Task ID: `R5_DASHBOARD_ACTIONABILITY`
Commit tag: `R5`
Owner: Session-specific
Branch: `docs-or-pod/dashboard-actionability`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Make the teacher dashboard’s recommendations feel concrete, specific, and classroom-actionable rather than generic or decorative.

## User-visible outcome

- Reviewers can follow at least 2-3 student stories from signal to teacher action.
- The dashboard can be defended as a decision aid, not just an analytics page.
- Recommendation examples feel specific enough to justify the product’s evidence-loop thesis.

## Owned files/modules

- `web/app/(workspace)/dashboard/`
- `web/components/dashboard/`
- `web/lib/dashboard-api.ts`
- `docs/contest/`
- `ai_first/competition/`
- `docs/superpowers/tasks/2026-04-26-risk-lane-5-dashboard-actionability.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/agent_spec/`
- `web/app/(workspace)/agents/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless the shipped dashboard workflow changes materially

## API/data contract

- Preserve the existing hierarchy:
  - `Observed`
  - `Inferred`
  - `Recommended Action`
- Do not smuggle new diagnosis claims into the UI layer.
- If examples are seeded or curated for demo use, label them as demo-safe and non-private.

## Acceptance criteria

- At least 2-3 dashboard story cards or equivalent artifacts exist.
- Each story shows a concrete teacher move, not just a generic recommendation label.
- Small-group action examples are available if the grouped-signal path is part of the contest narrative.

## Required tests

- Focused frontend lint/build checks for any touched dashboard files
- `git diff --check`

## Manual verification

- Walk through each prepared student story from observation to action.
- Confirm a teacher could say what they would do next without extra explanation from the team.
- Confirm the examples remain aligned with current diagnosis and insight payloads.

## Parallel-work notes

- This lane may be delivered through UI tightening, seeded examples, or docs/story artifacts depending on the real gap.
- Avoid turning it into a full redesign of the dashboard.
- Coordinate with the diagnosis-credibility lane so story cards reuse the same examples.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if dashboard flow boundaries materially change.

## Handoff notes

- Primary attack being addressed: “The dashboard looks smart, but what should a teacher actually do?”
- Preferred defense: student stories and teacher actions, not abstract labels alone.
