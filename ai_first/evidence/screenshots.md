# Screenshots and Video Checklist

## Judge-facing order

Use the existing screenshot set in this order when a reviewer wants the shortest visual proof path:

1. Teacher control on `/agents`
2. Knowledge Pack grounding
3. Assessment generation and feedback
4. Tutor support
5. Dashboard review and next action

Keep the narration at validated-prototype scope. The screenshots support teacher control, adaptive support, and teacher-reviewed follow-up. They do not support classroom outcome claims or autonomous teacher replacement.

## Screenshot freshness

| Artifact | Status | Last real capture | Judge-facing caption | Notes |
| --- | --- | --- | --- |
| `/agents` authoring proof | Current | 2026-04-26 | Teacher defines who the tutor is for, how it coaches, and what boundaries it must follow. | Pair with bounded runtime-binding automated proof. |
| Knowledge Pack creation | Current | 2026-04-25 | Teacher sets the learning context and sharing boundary before any AI step begins. | No Session B recapture on 2026-04-28. |
| Assessment Builder result | Current | 2026-04-25 | The assessment is grounded in the same teacher-approved knowledge pack. | Uses demo-safe local session content. |
| Student Tutor conversation | Current | 2026-04-25 | The tutor gives adaptive help while staying inside the same classroom loop. | Uses seeded demo response. |
| Teacher Dashboard | Current | 2026-04-26 | The teacher reviews signals and chooses the next classroom move. | Evidence-first dashboard workflow recaptured after the dashboard polish merge. |
| Main architecture Mermaid map rendered | Pending review | N/A | Architecture/read path exists if a reviewer asks how the system is organized. | Session A owns the narrative/submission package refresh. |

## Video freshness

| Artifact | Status | Notes |
| --- | --- | --- |
| End-to-end demo under 3 minutes | Deferred | Capture only if the final submission requires video. |
| Short technical walkthrough under 2 minutes | Deferred | Capture only if the final submission requires video. |

## Storage

Store final images and video outside the repository unless the files are small and explicitly needed for docs.
