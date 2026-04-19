# Smoke Runbook

This runbook verifies the contest MVP path in the same order as the demo story:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

Stop the lane on the first hard failure. Record the result in `ai_first/EXECUTION_QUEUE.md` and `ai_first/daily/YYYY-MM-DD.md`.

## Stage 1: Backend

- Command: use the existing backend startup path for local validation.
- Success: the API starts cleanly and the Knowledge, question, unified workspace, and dashboard routes are reachable.
- Stop condition: backend does not start or required routes fail.

## Stage 2: Frontend

- Command: use the existing frontend startup path or production build path for local validation.
- Success: the workspace routes render and the app can reach the backend using the expected local base URL.
- Stop condition: frontend does not build or cannot start.

## Stage 3: Knowledge Pack

- Action: confirm Knowledge Pack metadata is visible and matches the expected demo data shape.
- Success: metadata is present after load or reload.
- Stop condition: Knowledge Pack metadata is missing or broken.

## Stage 4: Assessment

- Action: generate assessment content from a selected Knowledge Pack.
- Success: generated questions appear with answer, explanation, and common-mistake content when available.
- Stop condition: assessment generation fails or loses Knowledge Pack grounding.

## Stage 5: Tutor

- Action: ask a Tutor workspace question using the same Knowledge Pack context.
- Success: the tutor answer reflects the selected Knowledge Pack context.
- Stop condition: the Tutor response ignores or loses context.

## Stage 6: Dashboard

- Action: open the Dashboard after the assessment and tutor steps.
- Success: recent activity reflects assessment and tutor usage with Knowledge Pack context where available.
- Stop condition: dashboard activity is empty, broken, or missing the expected context.

## Result handling

- If all stages pass: refresh any affected contest evidence docs, then move to the next queued task.
- If a product/runtime stage fails: create or update a follow-up task packet before starting broad new work.
- If an environment or credential blocker prevents completion: record the blocker clearly and do not report smoke as passing.
