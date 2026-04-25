# Feature Pod Task: Marketplace and Knowledge Pack Screen Polish

Owner:
Branch: `pod-a/t045-marketplace-knowledge-polish`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Make the marketplace and knowledge-pack teacher surfaces feel less prototype-like while staying inside the existing page architecture.

## User-visible outcome

- Marketplace discovery feels clearer and more intentional.
- Preview, import, and empty states communicate progress and outcomes better.
- Knowledge Pack metadata editing exposes clearer labels, hints, and status feedback.

## Owned files/modules

- `web/app/(utility)/marketplace/page.tsx`
- `web/app/(utility)/marketplace/error.tsx`
- `web/app/(utility)/knowledge/page.tsx`

## Do-not-touch files/modules

- `deeptutor/api/routers/`
- `web/lib/`
- `web/locales/vi/`
- `ai_first/`

## API/data contract

Use existing UI contracts only. No backend contract expansion in this slice.

## Acceptance criteria

- Marketplace filters, cards, and preview feel intentionally labeled and organized.
- Knowledge metadata editing flow provides clearer status and guidance.
- No backend or API-client changes are required to finish the slice.

## Required tests

- `cd web && npm run build`
- `git diff --check`

## Manual verification

- Open marketplace and confirm search, filters, cards, preview, and import feedback read clearly.
- Open the knowledge page and confirm metadata edit flow feels coherent and contest-demo ready.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Do not modify `web/lib/marketplace-api.ts` or `web/lib/knowledge-api.ts` in this slice.
- If missing API data blocks the UX, stop and convert that gap into a Lane 2 contract task.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not updated unless route structure changes.

## Handoff notes
