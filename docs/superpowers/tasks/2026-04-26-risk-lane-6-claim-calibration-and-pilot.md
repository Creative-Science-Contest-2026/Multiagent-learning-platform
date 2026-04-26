# Feature Pod Task: Risk Lane 6 Claim Calibration And Pilot Evidence

Task ID: `R6_CLAIM_CALIBRATION_PILOT`
Commit tag: `R6`
Owner: Session-specific
Branch: `docs-or-pod/claim-calibration-pilot`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Reduce vulnerability to judge skepticism by tightening product claims, clarifying prototype status, and adding the smallest credible pilot or human-feedback evidence available.

## User-visible outcome

- Project wording no longer overclaims “multi-agent” or production readiness.
- Reviewers can see what is validated, what is prototype, and what remains future work.
- Even limited external feedback or pilot evidence is packaged honestly if available.

## Owned files/modules

- `docs/contest/`
- `ai_first/competition/`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `docs/superpowers/tasks/2026-04-26-risk-lane-6-claim-calibration-and-pilot.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/`
- `deeptutor/api/`
- `web/app/`
- `web/components/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless shipped architecture language materially changes

## API/data contract

- All wording must distinguish:
  - validated prototype
  - current merged capability
  - future multi-agent design direction
- Do not fabricate pilot data, teacher quotes, or user counts.
- If no real pilot evidence exists, say so plainly and frame the current evidence as structured walkthrough validation instead.

## Acceptance criteria

- Contest-facing wording is calibrated around current proof, not intended future architecture.
- Any “multi-agent” language is either tightened or explicitly scoped.
- A minimal pilot-feedback artifact or an explicit no-pilot-yet note is included.
- The submission package can defend itself against “staged demo” skepticism with honest framing.

## Required tests

- `rg` checks across contest and competition docs for overclaim terms or stale wording
- `git diff --check`

## Manual verification

- Re-read the main contest docs as a skeptical judge.
- Check that every strong claim has either:
  - an artifact
  - a test
  - a screenshot
  - a careful limitation note
- Confirm no wording implies classroom deployment or inter-agent autonomy beyond current proof.

## Parallel-work notes

- This lane is docs-and-positioning heavy.
- If a real teacher pilot becomes available, fold it in carefully without expanding into a research-study claim.
- Coordinate with every other risk lane so the final wording reflects the actual proof level achieved.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged unless architecture-facing language in shipped docs changes materially.

## Handoff notes

- Primary attacks being addressed:
  - “This looks staged.”
  - “This is overclaiming multi-agent.”
  - “Where is the real user evidence?”
- Preferred defense: honest calibration plus the strongest real artifact currently available.
