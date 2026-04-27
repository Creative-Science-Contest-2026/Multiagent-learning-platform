# F121 Class Roster And Group Foundation

- Task ID: `F121_CLASS_ROSTER_AND_GROUP_FOUNDATION`
- Commit tag: `F121`
- Status: `Implementation`
- Branch recommendation: `pod-b/class-roster-group-foundation`

## Goal

Add the smallest backend-first class roster and ownership foundation needed to move dashboard and future classroom workflows away from globally pooled `student_id` assumptions.

## Owned Files

- `deeptutor/services/session/`
- bounded dashboard ownership contracts and related helpers
- optional new minimal roster service module if needed
- `tests/services/session/`
- bounded `tests/api/test_dashboard_router.py`
- `docs/superpowers/tasks/`
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files unless packet scope is explicitly expanded
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- runtime-policy and agent-spec surfaces
- broad classroom workflow UX beyond bounded verification

## Constraints

- keep the first slice backend-first and ownership-contract-first
- prefer additive schema and explicit ownership joins over implicit global filters
- any frontend change must be strictly bounded to verification if unavoidable
- do not widen this slice into attendance, grading, or full classroom management
