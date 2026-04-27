# F122 Implementation Plan

## Objective

Add a bounded validation-ops seam for future pilot or external walkthrough feedback, while preserving the repository's explicit current `no_pilot_evidence_yet` stance.

## Steps

1. Add failing tests first
   - service tests for dedicated pilot-feedback persistence and validation
   - system API tests for honest empty-state status and record listing behavior
2. Isolate feedback ingestion logic
   - add a focused helper under `deeptutor/services/evidence/`
   - use a dedicated SQLite table or similarly isolated storage path managed by that helper
   - keep labels and required fields explicit and claim-safe
3. Expose a bounded ops surface
   - extend a non-dashboard router such as `system.py`
   - return a compact status payload that still says `no_pilot_evidence_yet` when there are zero records
4. Update bounded docs proof
   - refresh `docs/contest/PILOT_STATUS.md` and related handoff wording only as needed to reference the new seam
   - write the PR note with a Mermaid diagram
   - update `MAIN_SYSTEM_MAP.md` if the new validation-ops seam becomes a stable subsystem boundary
5. Verify
   - run targeted store/service and system API tests
   - run `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
   - run a registry consistency check
   - run `git diff --check`
