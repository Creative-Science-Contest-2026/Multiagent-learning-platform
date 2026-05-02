import type { ReactNode } from "react";

interface IntroduceSectionProps {
  id: string;
  eyebrow: string;
  titleVi: string;
  titleEn: string;
  descriptionVi?: string;
  descriptionEn?: string;
  children: ReactNode;
}

export function IntroduceSection({
  id,
  eyebrow,
  titleVi,
  titleEn,
  descriptionVi,
  descriptionEn,
  children,
}: IntroduceSectionProps) {
  return (
    <section
      id={id}
      className="scroll-mt-20 border-b border-[rgba(10,21,48,0.08)] pb-12 last:border-b-0 lg:pb-16"
    >
      <div className="mb-6 space-y-3">
        <span className="inline-flex rounded-full border border-[rgba(10,21,48,0.12)] bg-white/80 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#50607d]">
          {eyebrow}
        </span>
        <div className="space-y-2">
          <h2 className="text-3xl font-semibold tracking-[-0.04em] text-[#0a1530] lg:text-4xl">
            {titleVi}
          </h2>
          <p className="text-base font-medium text-[#50607d] lg:text-lg">{titleEn}</p>
        </div>
        {descriptionVi || descriptionEn ? (
          <div className="grid gap-3 text-sm leading-7 text-[#2d3b57] lg:grid-cols-2">
            {descriptionVi ? <p>{descriptionVi}</p> : null}
            {descriptionEn ? <p>{descriptionEn}</p> : null}
          </div>
        ) : null}
      </div>
      {children}
    </section>
  );
}
