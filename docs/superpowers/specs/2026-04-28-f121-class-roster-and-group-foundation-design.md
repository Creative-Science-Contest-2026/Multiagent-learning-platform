# F121 Design: Class Roster And Group Foundation

## Problem

The current dashboard and evidence flows derive student records from session preferences and observation rows alone. That works for contest-demo data, but it has no explicit class roster or teacher-owned student list. As a result, future classroom workflows would have to infer ownership from loose metadata like `cohort`, and dashboard aggregation cannot defend who a teacher is actually responsible for.

## Design Direction

Keep this slice minimal and backend-first. Introduce explicit roster/ownership primitives that can answer:

- which teacher or class owns a student record
- which student ids belong to a named class roster
- which dashboard rows should be included for a bounded teacher/class scope

The first pass should not build full classroom UX. It should instead establish a small storage seam and a bounded query contract that later UI work can consume.

## Proposed Contract

1. Add a minimal roster persistence seam, likely in the SQLite session store or a narrowly scoped companion helper.
2. Model classes and student membership explicitly enough to support:
   - class id
   - teacher id or owner key
   - student ids
   - lightweight class metadata such as title
3. Add a bounded dashboard ownership filter or lookup path that can restrict student rows to a specific owned roster instead of global session history.
4. Keep current no-roster behavior available as a fallback until teacher/class scope is explicitly supplied.

## Approach Options

### Option A — Cohort-only reuse

Treat the existing `cohort` session preference as the class roster.

Pros:
- cheapest implementation

Cons:
- no explicit ownership
- weak data contract
- hard to evolve safely

### Option B — Minimal explicit roster storage

Add small class-roster tables or JSON-backed records with explicit teacher ownership and student membership.

Pros:
- clean contract
- future-proof for teacher-scoped queries
- still bounded

Cons:
- requires migration and test coverage

### Option C — Full classroom management slice

Add roster CRUD, membership editing, teacher UI, and richer classroom operations now.

Pros:
- more complete

Cons:
- exceeds the current bounded task
- conflicts with Session A teacher-facing scope

## Recommendation

Use **Option B**. It adds the explicit backend contract the product lacks today while avoiding UI expansion.

## Scope Boundary

- in scope: minimal roster storage, teacher/class ownership contract, bounded dashboard API proof, additive tests
- out of scope: full classroom management UI, attendance, grading, or broad teacher dashboard redesign

## Proof Plan

- service tests prove roster create/read or equivalent ownership lookup behavior
- dashboard API tests prove student insight payloads can be constrained to a supplied class/owner scope
- PR note documents the ownership boundary and why the first slice remains backend-first
