# F121 Implementation Plan

## Objective

Add a minimal explicit class-roster and ownership foundation that later classroom-facing features can rely on, without opening a full teacher-facing classroom UI slice.

## Steps

1. Add failing tests first
   - service tests for roster persistence or ownership lookup
   - bounded dashboard API tests for roster-scoped student visibility
2. Isolate the storage seam
   - add minimal schema or helper methods for class rosters and memberships
   - keep ownership fields explicit and inspectable
3. Thread into bounded dashboard logic
   - allow dashboard insight queries to consume explicit roster/class scope
   - preserve current fallback behavior when no scope is provided
4. Update docs proof
   - write the required PR note with Mermaid diagram
   - update `MAIN_SYSTEM_MAP.md` only if a new shared class-ownership seam becomes explicit
5. Verify
   - run targeted session-store and dashboard tests
   - run `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
   - run a registry consistency check
   - run `git diff --check`
