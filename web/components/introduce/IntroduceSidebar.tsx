/* eslint-disable i18n/no-literal-ui-text */
import Link from "next/link";
import type { IntroduceQuickFact, IntroduceSectionLink } from "./introduce-content";

interface IntroduceSidebarProps {
  sections: IntroduceSectionLink[];
  quickFacts: IntroduceQuickFact[];
}

export function IntroduceSidebar({ sections, quickFacts }: IntroduceSidebarProps) {
  return (
    <aside className="hidden border-r border-[rgba(10,21,48,0.08)] bg-[#f6f5f4] lg:block lg:w-[300px] lg:shrink-0">
      <div className="sticky top-0 flex h-screen flex-col overflow-y-auto px-6 py-8">
        <div className="space-y-4 border-b border-[rgba(10,21,48,0.08)] pb-6">
          <div className="space-y-2">
            <span className="inline-flex rounded-full bg-[#0a1530] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-white">
              Introduce
            </span>
            <div>
              <p className="text-[22px] font-semibold tracking-[-0.04em] text-[#0a1530]">
                Giới thiệu sản phẩm
              </p>
              <p className="mt-1 text-sm leading-6 text-[#50607d]">
                Product introduction for judges, partners, and deployment stakeholders.
              </p>
            </div>
          </div>
          <Link
            href="/"
            className="inline-flex items-center rounded-lg border border-[rgba(10,21,48,0.12)] bg-white px-3 py-2 text-sm font-medium text-[#0a1530] transition-colors hover:bg-[#eef3fb]"
          >
            Vào sản phẩm / Open app
          </Link>
        </div>

        <nav aria-label="Introduce sections" className="mt-6">
          <div className="mb-3 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7a869c]">
            Navigation
          </div>
          <div className="space-y-1">
            {sections.map((section) => (
              <a
                key={section.id}
                href={`#${section.id}`}
                className="block rounded-xl px-3 py-2 text-sm text-[#24324a] transition-colors hover:bg-white hover:text-[#0a1530]"
              >
                {section.labelVi} / {section.labelEn}
              </a>
            ))}
          </div>
        </nav>

        <div className="mt-8 space-y-3">
          <div className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7a869c]">
            Quick facts
          </div>
          {quickFacts.map((fact) => (
            <div
              key={fact.labelEn}
              className="rounded-2xl border border-[rgba(10,21,48,0.08)] bg-white px-4 py-4 shadow-[0_10px_30px_rgba(10,21,48,0.04)]"
            >
              <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7a869c]">
                {fact.labelVi}
              </p>
              <p className="mt-2 text-sm font-medium leading-6 text-[#0a1530]">{fact.vi}</p>
              <p className="mt-1 text-xs leading-5 text-[#50607d]">{fact.en}</p>
            </div>
          ))}
        </div>
      </div>
    </aside>
  );
}
