# Screenshots and Video Checklist

## Judge-facing order

Use the existing screenshot set in this order when a reviewer wants the shortest visual proof path:

1. Teacher control on `/agents`
2. Knowledge Pack grounding
3. Assessment generation and feedback
4. Tutor support
5. Dashboard review and next action

Keep the narration at validated-prototype scope. The screenshots support teacher control, adaptive support, and teacher-reviewed follow-up. They do not support classroom outcome claims or autonomous teacher replacement.

Browser evidence status note on 2026-04-30:

- command-backed smoke proof remains current from the 2026-04-28 Session B run;
- browser screenshots below were refreshed on 2026-04-30 against the current merged contest-facing UI;
- recapture is no longer an active blocker and only needs to happen again after the next visible UI change.

## Screenshot freshness

| Artifact | Status | Last real capture | Judge-facing caption | Notes |
| --- | --- | --- | --- |
| `/agents` authoring proof | Current | 2026-04-30 | Teacher defines who the tutor is for, how it coaches, and what boundaries it must follow. | Refreshed in `docs/browser-recapture-refresh-20260430`. |
| Knowledge Pack creation | Current | 2026-04-30 | Teacher sets the learning context and sharing boundary before any AI step begins. | Refreshed in `docs/browser-recapture-refresh-20260430`. |
| Assessment Builder result | Current | 2026-04-25 | The assessment is grounded in the same teacher-approved knowledge pack. | No post-polish assessment-specific UI change was merged in Phase 2. |
| Student Tutor conversation | Current | 2026-04-30 | The tutor gives adaptive help while staying inside the same classroom loop. | Refreshed from the teacher-facing replay surface for `contest-tutor-demo`. |
| Teacher Dashboard | Current | 2026-04-30 | The teacher reviews signals and chooses the next classroom move. | Refreshed in `docs/browser-recapture-refresh-20260430`. |
| Main architecture Mermaid map rendered | Pending review | N/A | Architecture/read path exists if a reviewer asks how the system is organized. | Session A owns the narrative/submission package refresh. |

## Video freshness

| Artifact | Status | Notes |
| --- | --- | --- |
| End-to-end demo under 3 minutes | Deferred | Capture only if the final submission requires video. |
| Short technical walkthrough under 2 minutes | Deferred | Capture only if the final submission requires video. |

## Storage

Store final images and video outside the repository unless the files are small and explicitly needed for docs.
