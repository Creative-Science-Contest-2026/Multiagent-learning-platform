# T045 Marketplace and Knowledge Polish

## Scope

- Improve marketplace filter/card/preview hierarchy using existing frontend state.
- Improve knowledge-pack upload and metadata-edit feedback without changing API contracts.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` not updated because route structure is unchanged.

## Architecture Note

```mermaid
flowchart LR
  Marketplace[Marketplace page] --> Preview[Pack preview modal]
  Marketplace --> Import[Import feedback]
  Knowledge[Knowledge page] --> Upload[Upload section]
  Knowledge --> Metadata[Metadata editor]
```
