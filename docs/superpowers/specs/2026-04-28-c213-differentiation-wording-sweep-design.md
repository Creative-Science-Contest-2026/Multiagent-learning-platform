# C213 Differentiation Wording Sweep Design

## Goal

Tighten contest-facing product copy so the web app consistently reads as a teacher-controlled adaptive tutoring workflow rather than a fully autonomous tutor.

## Scope

- Contest-facing wording only on already-merged UI surfaces.
- No route changes, no data-model changes, no runtime behavior changes.
- Small AI-first control-plane updates required to record `C212` completion and `C213` activation.

## Owned files

- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/components/contest/CoreLoopVisibilityStrip.tsx`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-c213-differentiation-wording-sweep.md`
- `docs/superpowers/pr-notes/2026-04-28-c213-differentiation-wording-sweep.md`

## Do-not-touch

- Backend/runtime code outside the listed frontend files
- Contest submission package docs
- Lockfiles, generated files, and screenshots

## Copy strategy

1. Keep existing information architecture and component placement.
2. Replace broad or generic tutoring language with teacher-guided, classroom-loop framing.
3. Emphasize that tutoring output is evidence inside a larger review-and-intervention workflow.
4. Avoid stronger product claims than the submission package already supports.

## Surface decisions

### Dashboard

- Reframe the hero from generic workflow language to teacher-reviewed adaptive action language.
- Keep the loop strip, but sharpen helper text around teacher judgment.

### Tutor chat

- Reframe the empty state and loop helper so the tutor is positioned as guided practice, not the final decision-maker.

### Knowledge

- Reframe the loop helper so Knowledge Packs read as teacher-owned grounding for later adaptive steps.

### Spec pack authoring

- Reframe setup copy so teachers are clearly shaping an adaptive tutor for a class with explicit boundaries.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "app/(utility)/knowledge/page.tsx" "app/(workspace)/dashboard/page.tsx" "app/(workspace)/agents/[botId]/chat/page.tsx" "components/agents/SpecPackAuthoringTab.tsx" "components/contest/CoreLoopVisibilityStrip.tsx"`
- `cd web && npm run build`
