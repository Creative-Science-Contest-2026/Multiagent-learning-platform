/* eslint-disable i18n/no-literal-ui-text */
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import type { IntroduceGalleryItem, IntroduceQuickFact } from "./introduce-content";

interface IntroduceHeroProps {
  quickFacts: IntroduceQuickFact[];
  heroImage: IntroduceGalleryItem;
}

export function IntroduceHero({ quickFacts, heroImage }: IntroduceHeroProps) {
  return (
    <section
      id="overview"
      className="overflow-hidden rounded-[28px] bg-[#0a1530] px-6 py-6 text-white shadow-[0_30px_80px_rgba(10,21,48,0.24)] lg:px-8 lg:py-8"
    >
      <div className="grid gap-8 lg:grid-cols-[minmax(0,1.1fr)_420px] lg:items-start">
        <div className="space-y-6">
          <div className="space-y-4">
            <span className="inline-flex rounded-full border border-white/16 bg-white/8 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-white/88">
              Judge-first briefing
            </span>
            <div className="space-y-3">
              <h1 className="max-w-3xl text-4xl font-semibold tracking-[-0.06em] text-white lg:text-6xl">
                Giới thiệu sản phẩm
              </h1>
              <p className="text-lg font-medium text-white/72 lg:text-xl">Product introduction</p>
              <p className="max-w-3xl text-base leading-8 text-white/84 lg:text-lg">
                Nền tảng hỗ trợ giáo viên thiết lập bối cảnh học liệu, tạo đánh giá, đồng hành cùng
                học sinh qua gia sư AI, theo dõi chẩn đoán và quyết định bước can thiệp tiếp theo.
              </p>
              <p className="max-w-3xl text-sm leading-7 text-white/68 lg:text-base">
                A teacher-controlled adaptive tutoring workflow that connects knowledge packs,
                assessments, tutoring, diagnosis, and intervention into one demonstrable prototype.
              </p>
            </div>
          </div>

          <div className="rounded-[24px] border border-white/12 bg-white/8 px-5 py-5">
            <div className="text-[11px] font-semibold uppercase tracking-[0.16em] text-white/60">
              Core loop
            </div>
            <div className="mt-3 flex flex-wrap items-center gap-2 text-sm font-medium text-white/88 lg:text-base">
              <span>Knowledge Pack</span>
              <ArrowRight className="h-4 w-4 text-[#f5d75e]" />
              <span>Assessment</span>
              <ArrowRight className="h-4 w-4 text-[#ff64c8]" />
              <span>Tutor</span>
              <ArrowRight className="h-4 w-4 text-[#2a9d99]" />
              <span>Diagnosis</span>
              <ArrowRight className="h-4 w-4 text-[#d6b6f6]" />
              <span>Intervention</span>
            </div>
            <p className="mt-4 text-sm leading-7 text-white/72">
              Knowledge Pack -&gt; Assessment -&gt; Tutor -&gt; Diagnosis -&gt; Intervention
            </p>
          </div>

          <div className="grid gap-3 md:grid-cols-3">
            {quickFacts.map((fact, index) => (
              <div
                key={fact.labelEn}
                className={`rounded-[20px] border px-4 py-4 ${
                  index === 0
                    ? "border-[#f5d75e]/40 bg-[#1a2a52]"
                    : index === 1
                      ? "border-[#2a9d99]/40 bg-[#0f213f]"
                      : "border-[#ff64c8]/30 bg-[#101b36]"
                }`}
              >
                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-white/56">
                  {fact.labelVi}
                </p>
                <p className="mt-2 text-sm font-medium leading-6 text-white">{fact.vi}</p>
                <p className="mt-1 text-xs leading-5 text-white/68">{fact.en}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-[24px] border border-white/10 bg-white/6 p-3 backdrop-blur">
          <div className="mb-3 flex items-center justify-between px-2 pt-2">
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-white/56">
                Hero evidence
              </p>
              <p className="mt-1 text-sm font-medium text-white">{heroImage.titleVi}</p>
            </div>
            <span className="rounded-full bg-white/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-white/72">
              {heroImage.tagEn}
            </span>
          </div>
          <div className="overflow-hidden rounded-[18px] border border-white/10 bg-[#091126]">
            <Image
              src={heroImage.src}
              alt={heroImage.titleVi}
              width={1600}
              height={1000}
              className="h-auto w-full object-cover"
              priority
            />
          </div>
          <div className="px-2 pb-2 pt-4">
            <p className="text-sm leading-7 text-white/84">{heroImage.captionVi}</p>
            <p className="mt-1 text-xs leading-6 text-white/60">{heroImage.captionEn}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
