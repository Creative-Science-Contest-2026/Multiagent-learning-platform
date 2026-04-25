# T046 Dashboard Review Polish

## Scope

- Improve dashboard hierarchy and next-step framing.
- Improve assessment review and tutoring replay readability without changing contracts.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` not updated because route behavior is unchanged.

## Architecture Note

```mermaid
flowchart LR
  Dashboard[Teacher dashboard] --> Review[Assessment review]
  Dashboard --> Replay[Tutoring replay]
  Review --> Summary[Progress and journey summaries]
  Replay --> FollowUp[Teacher follow-up reading]
```
