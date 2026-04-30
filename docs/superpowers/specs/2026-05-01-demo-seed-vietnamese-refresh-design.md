# Demo Seed Vietnamese Refresh Design

Date: 2026-05-01
Task packet: `docs/superpowers/tasks/2026-05-01-demo-seed-vietnamese-refresh.md`
Branch: `fix/demo-seed-vietnamese-refresh`

## Objective

Keep the richer local demo seed shape intact while translating visible mock content into natural Vietnamese and making the cleanup-before-reseed step explicit to operators.

## Scope

In scope:

- `scripts/contest/reset_demo_data.py`
- `tests/scripts/test_reset_demo_data.py`
- `docs/contest/DEMO_DATA_RESET.md`

Out of scope:

- changing the seeded table counts
- frontend/runtime code changes
- changing the local API safety gate

## Chosen approach

Translate all visible seeded metadata, questions, answers, and tutor transcripts that teachers or students might see in the demo, while preserving parser-required wrapper tokens such as `[Quiz Performance]`, `Q:`, `Answered:`, `Correct`, and `Incorrect`.

Expose cleanup explicitly in two places:

- the script result payload should state that old demo data was cleared before reseeding;
- the reset runbook should state that the command first deletes demo-owned seed data, then writes the new dataset.

## Validation

- `pytest tests/scripts/test_reset_demo_data.py -v`
- run the reset command once and inspect its result payload
- run the reset command a second time to confirm the same stable shape remains
