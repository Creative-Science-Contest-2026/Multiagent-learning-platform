# Optional Video Capture Runbook

Use this runbook only if the final VnExpress Sáng kiến Khoa học 2026 submission requires a video artifact.

## Target Outcome

Produce one short external video, ideally between 3 and 5 minutes, that shows the complete MVP story:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Recommended Structure

### Clip 1. Opening context

- duration: 10 to 15 seconds
- show: project title or submission package intro
- say: this is an AI-first learning platform for Vietnamese teachers and students

### Clip 2. Knowledge Pack setup

- duration: 35 to 45 seconds
- show:
  - Knowledge Pack metadata page
  - demo-safe subject, curriculum, objectives, and teacher metadata
- say:
  - the teacher owns the source learning materials
  - the Knowledge Pack is the grounding source for later assessment and tutoring

### Clip 3. Assessment generation

- duration: 40 to 50 seconds
- show:
  - assessment configuration
  - generated questions
  - one feedback or common-mistake section
- say:
  - AI generates practice from the teacher-approved pack
  - the workflow can surface feedback and review signals

### Clip 4. Tutor Agent follow-up

- duration: 40 to 50 seconds
- show:
  - tutor session with a student follow-up question
  - tutor response with pack context
- say:
  - tutoring stays grounded in the same approved learning source
  - this reduces hallucinated or off-topic support

### Clip 5. Teacher dashboard review

- duration: 35 to 45 seconds
- show:
  - dashboard summary cards
  - recent activity with pack/session references
- say:
  - the teacher can review learning activity, assessment evidence, and tutoring traces in one place

### Clip 6. Validation close

- duration: 20 to 30 seconds
- show:
  - `docs/contest/VALIDATION_REPORT.md`
  - screenshot bundle or evidence checklist
- say:
  - the demo path is backed by smoke validation, screenshots, and a demo-safe reset workflow

## Recording Guidance

- use the existing demo-safe flow described in `docs/contest/DEMO_SCRIPT.md`
- start from a clean local state if needed with `docs/contest/DEMO_DATA_RESET.md`
- avoid recording credentials, browser tabs with private data, or local filesystem paths that expose personal information
- keep zoom level readable on a 1080p export
- prefer one continuous take unless a shorter edited cut is necessary

## Suggested Voiceover Notes

- keep narration factual and concrete
- avoid claims that exceed the current repository evidence
- describe the practical classroom workflow more than the underlying implementation details
- keep the main message aligned with `ai_first/competition/product-description.md`

## Capture Checklist

- [ ] Recording environment is clean and demo-safe
- [ ] Knowledge Pack clip captured
- [ ] Assessment clip captured
- [ ] Tutor clip captured
- [ ] Dashboard clip captured
- [ ] Validation close captured
- [ ] Final export link stored outside the repository

## Storage

Store the final video outside the repository, then paste the external link into:

- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md` only if the final submission uses the video as active evidence
- any manual submission form that requires the video URL

## When To Skip This

If the final contest submission does not require video, keep the video status deferred and do not spend time recording it.
