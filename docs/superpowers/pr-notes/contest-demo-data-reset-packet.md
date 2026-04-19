# PR Note: Contest Demo Data Reset Packet

## Summary

This PR queues the next short docs/workflow lane for making contest demo data reproducible after the smoke and evidence-refresh work.

## Mermaid Diagram

```mermaid
flowchart LR
  Smoke["Smoke + Evidence State"]
  Gap["Demo Data Still Local-only"]
  Packet["Demo Data Reset Packet"]
  Future["Future reset lane"]

  Smoke --> Gap
  Gap --> Packet
  Packet --> Future
```

## Architecture Impact

`ai_first/architecture/MAIN_SYSTEM_MAP.md` is not updated. This PR adds docs/workflow guidance for the next queue step without changing product/runtime architecture.
