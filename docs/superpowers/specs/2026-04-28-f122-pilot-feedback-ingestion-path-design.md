# F122 Design: Pilot Feedback Ingestion Path

## Problem

The repository already has honest contest wording that says no pilot evidence is currently bundled, but it does not have a bounded product-side place to ingest and preserve future walkthrough or pilot feedback once that feedback exists. Without an explicit seam, the likely failure modes are scattered notes, claim drift across contest docs, or ad hoc storage mixed into unrelated teacher/product surfaces.

## Design Direction

Keep this slice narrow and ops-facing. The system should add a dedicated feedback-ingestion seam that can safely hold future external walkthrough or pilot feedback records, while keeping the current empty state explicit and reviewable. The feature should improve future evidence hygiene, not imply that real pilot evidence already exists.

Recommended record shape:

- feedback id
- evidence tier such as `walkthrough`, `limited_external_feedback`, or `pilot`
- source label and optional participant role
- activity date or date range
- short scope note
- bounded findings or recommendation notes
- claim-safety metadata such as `verified_by`, `artifact_ref`, or `status`

## Proposed Contract

1. Add a focused feedback store/helper under `deeptutor/services/evidence/` with explicit validation and list/read behavior.
2. Persist records in a dedicated SQLite table or similarly isolated storage seam rather than hiding them in generic session preferences.
3. Expose a bounded system/ops surface that can:
   - report the current pilot-feedback status
   - remain explicit about `no_pilot_evidence_yet` when no records exist
   - list stored records without turning them into teacher-facing product UX
4. Update contest and human-review docs so they point to the new status/ingestion seam while keeping claims calibrated.

## Approach Options

### Option A — Docs-only placeholder

Keep `PILOT_STATUS.md` as the only source of truth and add no backend path.

Pros:
- smallest change
- zero runtime risk

Cons:
- future real feedback still has no structured storage path
- encourages manual drift between docs and actual evidence records

### Option B — Dedicated validation-ops feedback seam

Add a small storage/helper layer plus a bounded system-facing API/status surface.

Pros:
- honest empty state today, usable ingestion path later
- keeps evidence handling separate from dashboard and tutoring flows
- testable without inventing real pilot data

Cons:
- adds one small persistence/API seam to maintain

### Option C — Reuse generic session preferences or dashboard metadata

Store pilot notes inside existing session or dashboard data models.

Pros:
- fewer new files

Cons:
- wrong boundary
- easy to couple future external evidence with teacher product workflow
- harder to reason about claim safety

## Recommendation

Use **Option B**. It gives the repository a real ingestion path without broadening into classroom UX or making unsupported evidence claims.

## Scope Boundary

- in scope: dedicated feedback storage/helper, bounded system-facing status or ingestion API, contest/handoff wording updates, tests that prove empty-state honesty and record persistence
- out of scope: teacher dashboard UX, public pilot claims, analytics over feedback, or synthetic/example pilot data presented as real evidence

## Proof Plan

- service or store tests prove the system can persist and return feedback records with explicit validation
- system API tests prove empty state remains `no_pilot_evidence_yet` when no records exist and becomes structured only when real records are stored
- bounded docs updates prove the contest read path points to the seam without changing the underlying no-pilot-yet claim
