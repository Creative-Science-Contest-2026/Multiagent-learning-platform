# F114 Spec Version Pinning Per Session

- Task ID: `F114_SPEC_VERSION_PINNING_PER_SESSION`
- Commit tag: `F114`
- Status: `Planning`
- Branch recommendation: `pod-b/spec-version-pinning`

## Goal

Pin each learning session to the exact teacher-spec version first resolved at runtime so later debugging, audit, and teacher-trust surfaces can reconstruct the same spec context instead of drifting to the latest saved pack.

## Owned Files

- `deeptutor/services/agent_spec/`
- `deeptutor/services/session/`
- `deeptutor/services/runtime_policy/`
- bounded session/runtime tests
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- broad `/agents` UX changes unless the packet is explicitly expanded

## Constraints

- preserve current `F113` runtime-binding behavior
- pin by exact spec version or version snapshot metadata, not by mutable latest pack lookup
- avoid changing teacher-facing flows in the same branch
- keep the first persisted session contract inspectable and testable
