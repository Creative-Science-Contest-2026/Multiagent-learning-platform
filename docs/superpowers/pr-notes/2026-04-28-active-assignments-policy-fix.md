# PR Note: Active Assignments Policy Fix

## Summary

- redefine `ai_first/ACTIVE_ASSIGNMENTS.md` as a board for live non-terminal lanes only
- remove merged submission-close lanes from the active board to stop recursive terminal-sync churn
- keep merged history in the daily log and packet/PR-note chain instead of the active board

## Mermaid Diagram

```mermaid
flowchart LR
  A["Merged lane stays in ACTIVE_ASSIGNMENTS"] --> B["Board becomes stale"]
  B --> C["Another repair lane opens"]
  C --> D["Recursive loop"]
  A2["Live non-terminal lanes only in ACTIVE_ASSIGNMENTS"] --> E["Merged history stays in daily logs and task notes"]
  E --> F["Stable terminal state"]
```

## Architecture Impact

`ai_first/architecture/MAIN_SYSTEM_MAP.md` is not updated. This change only fixes the AI-first coordination policy and mirror behavior.
