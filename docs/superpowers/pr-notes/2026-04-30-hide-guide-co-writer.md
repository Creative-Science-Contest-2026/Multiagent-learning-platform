# PR Note: Hide Guided Learning and Co-Writer

## Summary

- Removed `Guided Learning` and `Co-Writer` from the visible sidebar navigation.
- Redirected direct access to `/guide` and `/co-writer` back to `/playground` through route-level layouts.
- Kept feature implementation code intact and only removed public frontend entry points.

## Architecture

```mermaid
flowchart LR
  A["Sidebar navigation"] --> B["Visible routes"]
  B --> C["/playground"]
  B --> D["/memory"]
  E["Hidden legacy routes"] --> F["/guide"]
  E --> G["/co-writer"]
  F --> H["redirect /playground"]
  G --> H
  I["Knowledge saved records"] --> J["chat records can reopen session"]
  I --> K["guided-learning records remain view-only"]
```

## Main System Map

- `ai_first/architecture/MAIN_SYSTEM_MAP.md` not updated.
- Reason: this lane only narrows visible frontend entry points and adds reversible route redirects; it does not change the underlying system architecture or backend contracts.
