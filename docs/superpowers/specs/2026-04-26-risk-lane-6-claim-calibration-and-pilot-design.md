# Risk Lane 6 Claim Calibration And Pilot Design

## Metadata

- Date: 2026-04-26
- Task ID: `R6_CLAIM_CALIBRATION_PILOT`
- Commit tag: `R6`
- Branch: `docs/claim-calibration-pilot`
- Scope: claim calibration, prototype-status framing, and minimal pilot/external-feedback positioning

## Problem

The project is vulnerable to three related attacks:

1. the demo looks staged rather than validated
2. the product overclaims “multi-agent” relative to current shipped proof
3. reviewers may ask for real-user or teacher evidence that does not yet exist in a robust form

The goal of this lane is not to invent stronger proof. It is to present the current proof level honestly and consistently so the strongest existing artifacts carry the narrative without accidental overclaim.

## Goal

Tighten contest-facing wording around current proof, future direction, and pilot status so a skeptical judge can quickly distinguish:

- what is implemented now
- what is validated now
- what remains future architecture direction

## Non-Goals

- No runtime, API, or frontend feature changes
- No fabricated teacher quotes, pilot counts, or external validation claims
- No attempt to convert limited feedback into a research-study claim
- No rewrite of the whole repository narrative beyond contest-facing and compatibility surfaces

## Recommended Approach

Use a bounded `docs sweep + pilot-status artifact` approach:

1. sweep contest-facing docs for claim calibration
2. keep the word `multi-agent` only when explicitly scoped as design direction or role-separation intent
3. add one dedicated pilot/external-feedback artifact so the project has a single honest answer to “who used this?”
4. keep compatibility snapshots aligned so humans and future AI sessions do not reintroduce old wording

This is the smallest approach that reduces skepticism without pretending the project has stronger validation than it actually does.

## Wording Rules

### Current Proof Language

Use phrases like:

- `validated prototype`
- `smoke-backed evidence`
- `structured walkthrough validation`
- `bounded runtime-binding proof`
- `teacher-reviewed diagnosis`

### Future Architecture Language

Use phrases like:

- `multi-agent by design`
- `future direction`
- `prepared for role separation`
- `agent-native architecture`

Avoid wording that implies the current shipped product already has production-grade inter-agent autonomy.

### Pilot / External Feedback Language

If no real pilot artifact exists:

- say `no pilot evidence yet`
- explain that the strongest current evidence is structured walkthrough validation plus smoke-backed artifacts

If a small real artifact exists:

- describe it as `limited external feedback`
- keep the claim narrow and non-statistical

Never use wording like:

- `validated in classrooms`
- `proven learning outcomes`
- `user study`
- `production deployment`

unless an actual artifact in the repository supports that exact claim.

## File Set

### Contest / Submission Surface

- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/HUMAN_REVIEW_HANDOFF.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/PILOT_STATUS.md` (new)

### Competition / Narrative Surface

- `ai_first/competition/pitch-notes.md`
- `ai_first/competition/product-description.md`

### Compatibility / AI-first Surface

- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`

### Operating / Review Surface

- `docs/superpowers/pr-notes/*`
- daily log
- active assignment + task registry for lane start/finish

## Pilot Status Artifact

Preferred structure: create a dedicated file at `docs/contest/PILOT_STATUS.md`.

The file should answer:

1. What external or teacher feedback exists right now?
2. If none exists, what is the honest current state?
3. What evidence exists instead?
4. What would count as the next stronger validation step after the contest?

If the answer is “none yet,” that is acceptable and should be written plainly.

## Acceptance Criteria

1. Contest-facing docs consistently frame the product as a validated prototype, not a deployed school system.
2. Any use of `multi-agent` is scoped as present design intent or future direction, not current autonomous behavior.
3. The repository contains one explicit pilot/external-feedback artifact or one explicit no-pilot-yet note.
4. A skeptical reviewer can see, in one pass, the difference between:
   - current merged capabilities
   - validated evidence
   - future architecture direction
5. Compatibility snapshots do not contradict the contest docs.

## Manual Verification

Read the contest package as if you are a skeptical judge and ask:

1. Where is the proof?
2. Where is the limitation note?
3. Which lines talk about future direction rather than current capability?
4. If I ask “has a real teacher used this?”, is there one honest answer with no contradiction across files?

If any answer requires hand-waving, the docs are still too loose.

## Risks And Boundaries

- The main risk is turning calibration into under-selling. The fix is to be specific about current proof, not vague or apologetic.
- The second risk is leaving old wording behind in one compatibility or contest file, which creates contradictions.
- The third risk is quietly implying pilot validation through narrative tone even when the text avoids explicit claims.

## Architecture Note Requirement

The PR must include a note under `docs/superpowers/pr-notes/` with a Mermaid diagram. `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged unless shipped architecture language itself changes materially.
