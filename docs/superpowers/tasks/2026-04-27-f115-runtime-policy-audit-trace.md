# F115 Runtime Policy Audit Trace

- Task ID: `F115_RUNTIME_POLICY_AUDIT_TRACE`
- Commit tag: `F115`
- Status: `Ready for Review`
- Branch recommendation: `pod-b/runtime-policy-audit-trace`

## Goal

Provide a bounded, inspectable runtime-policy trace for debugging and future teacher-trust surfaces without changing teacher-facing dashboard or `/agents` UX.

## Owned Files

- `deeptutor/services/runtime_policy/`
- bounded `deeptutor/api/routers/agent_specs.py` changes or a sibling debug route if needed
- `tests/services/runtime_policy/`
- bounded API tests for the chosen audit surface
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- broad `/agents` UX changes
- unrelated evidence or student-model features outside runtime-policy audit scope

## Constraints

- keep the API/debug surface bounded and inspectable
- do not expose more internal state than needed for runtime-policy audit
- preserve the existing `F113` and `F114` runtime behavior
- avoid inventing teacher-facing provenance UX in this task
