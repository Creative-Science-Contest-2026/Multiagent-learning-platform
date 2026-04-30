# 2026-04-30 C218 Contest Brand And Classroom Terminology

- Task ID: `C218_CONTEST_BRAND_AND_CLASSROOM_TERMINOLOGY`
- Commit tag: `C218`
- Branch: `fix/contest-brand-classroom-terminology`
- Worktree: `.worktrees/contest-brand-classroom-terminology`
- Status: `in_progress`

## Goal

Add a bounded contest-facing brand and classroom-first terminology layer so judges see a Vietnamese classroom product instead of raw DeepTutor naming and generic AI workspace labels across the primary demo path.

## User-visible outcome

- The contest-facing shell and headers read like classroom software rather than a framework demo.
- Key primary-path labels use consistent classroom terminology across English and Vietnamese.
- DeepTutor naming remains preserved where upstream credit or clearly secondary technical context requires it, but it stops dominating the first product impression.

## Owned files

- `web/components/sidebar/SidebarShell.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-c218-contest-brand-and-classroom-terminology.md`
- `docs/superpowers/pr-notes/2026-04-30-c218-contest-brand-and-classroom-terminology.md`

## Do-not-touch

- `web/app/(workspace)/page.tsx`
- `web/app/(workspace)/guide/`
- `web/app/(workspace)/co-writer/`
- `web/app/(utility)/marketplace/page.tsx`
- `deeptutor/`
- `README.md`
- `AGENTS.md`
- `LICENSE`
- contest submission docs under `docs/contest/`
- lockfiles and generated files

## Execution notes

- Keep the task wording-only plus shell/header brand presentation. Do not change routing, runtime logic, or API/data contracts.
- Preserve Apache 2.0 and HKUDS/DeepTutor attribution by leaving upstream credit in repo-level docs and license surfaces untouched.
- Focus the copy pass on the primary contest path:
  - shell header and primary nav labels;
  - `/agents` teacher authoring headers and action labels;
  - Knowledge and Dashboard contest-facing headings and helper text;
  - the matching `en` and `vi` locale keys those surfaces depend on.
- Prefer terminology that matches the differentiation note:
  - `Knowledge Pack` or `Gói học liệu` over generic knowledge-base language where the screen is clearly contest-facing;
  - `Class tutor`, `Gia sư của lớp`, or equivalent teacher-centered tutor naming over generic `TutorBot` where possible;
  - `Teacher dashboard`, `Bảng điều khiển giáo viên`, `Điểm cần can thiệp`, and other classroom-action language over generic system jargon.
- Leave secondary or clearly non-contest technical surfaces alone if changing them would widen the sweep into a repo-wide rebrand.
- If a label change would require route restructuring or feature hiding, stop and keep that need inside `C216` or `C217` instead of widening this packet.

## Acceptance criteria

- The sidebar header and primary contest-path labels no longer make DeepTutor the dominant product identity on first read.
- Contest-facing English and Vietnamese wording is internally consistent across shell, Knowledge, Dashboard, and `/agents`.
- Upstream DeepTutor attribution remains intact in repo/legal surfaces.
- No route, behavior, or API changes are required.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `python3 -m json.tool web/locales/en/app.json >/dev/null`
- `python3 -m json.tool web/locales/vi/app.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "components/sidebar/SidebarShell.tsx" "app/(workspace)/agents/page.tsx" "app/(workspace)/dashboard/page.tsx" "app/(utility)/knowledge/page.tsx"`
- `cd web && npm run build`

## Manual verification

- Open the shell and confirm the header, nav, and first-read labels feel classroom-first.
- Open Knowledge, `/agents`, and Dashboard and confirm the terminology is consistent in the same language.
- Check at least one retained repo-level DeepTutor credit surface and confirm attribution still exists unchanged.

## Parallel-work notes

- This packet assumes `C216` may reduce shell clutter and `C217` may change the default landing, but it must remain valid even if those tasks merge before or after it.
- Do not widen into a full repo-wide rename; this is a contest-path terminology pass only.
- If the worker discovers the real gap is not wording but missing case-study framing or metrics, split that need into `C219`.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not expected to change because this task is wording and presentation only.

## Handoff

- The next expected follow-up after this packet is `C219_CLASSROOM_CASE_STUDY_AND_BOUNDED_METRIC_CARD`, which can assume the product wording already reads like a bounded classroom offering.
- This lane keeps `DeepTutor` intact on attribution-facing brand surfaces and limits the sweep to classroom-first terminology across the contest path.
