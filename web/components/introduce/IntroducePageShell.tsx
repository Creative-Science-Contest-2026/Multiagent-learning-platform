/* eslint-disable i18n/no-literal-ui-text */
import Link from "next/link";
import { ExternalLink } from "lucide-react";
import {
  INTRODUCE_EDUCATOR_BLOCKS,
  INTRODUCE_FAQ_BLOCKS,
  INTRODUCE_GALLERY_ITEMS,
  INTRODUCE_QUICK_FACTS,
  INTRODUCE_RESOURCE_LINKS,
  INTRODUCE_SECTIONS,
  INTRODUCE_TECHNICAL_BLOCKS,
} from "./introduce-content";
import { IntroduceCoreLoop } from "./IntroduceCoreLoop";
import { IntroduceGallery } from "./IntroduceGallery";
import { IntroduceHero } from "./IntroduceHero";
import { IntroduceSection } from "./IntroduceSection";
import { IntroduceSidebar } from "./IntroduceSidebar";

function ResourceLink({ href, label }: { href: string; label: string }) {
  const external = href.startsWith("http://") || href.startsWith("https://");

  if (external) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noreferrer"
        className="inline-flex items-center gap-2 rounded-xl border border-[rgba(10,21,48,0.08)] bg-white px-4 py-3 text-sm font-medium text-[#0a1530] transition-colors hover:bg-[#eef3fb]"
      >
        {label}
        <ExternalLink className="h-4 w-4 text-[#50607d]" />
      </a>
    );
  }

  return (
    <Link
      href={href}
      className="inline-flex items-center gap-2 rounded-xl border border-[rgba(10,21,48,0.08)] bg-white px-4 py-3 text-sm font-medium text-[#0a1530] transition-colors hover:bg-[#eef3fb]"
    >
      {label}
    </Link>
  );
}

export function IntroducePageShell() {
  const heroImage = INTRODUCE_GALLERY_ITEMS[0];

  return (
    <div className="h-screen overflow-hidden bg-[linear-gradient(180deg,#ffffff_0%,#f7f5f2_36%,#f4f1ee_100%)] text-[#0a1530]">
      <div className="mx-auto flex h-full max-w-[1680px] overflow-hidden">
        <IntroduceSidebar sections={INTRODUCE_SECTIONS} quickFacts={INTRODUCE_QUICK_FACTS} />

        <main className="min-w-0 flex-1 overflow-y-auto">
          <div className="sticky top-0 z-20 border-b border-[rgba(10,21,48,0.08)] bg-[rgba(255,255,255,0.92)] backdrop-blur lg:hidden">
            <div className="flex items-center justify-between gap-3 px-4 py-3">
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7a869c]">
                  Introduce
                </p>
                <p className="text-sm font-semibold text-[#0a1530]">Giới thiệu sản phẩm</p>
              </div>
              <Link
                href="/"
                className="rounded-lg border border-[rgba(10,21,48,0.12)] bg-white px-3 py-2 text-sm font-medium text-[#0a1530]"
              >
                Vào app
              </Link>
            </div>
          </div>

          <div className="mx-auto flex max-w-[1120px] flex-col gap-12 px-4 py-6 lg:px-8 lg:py-8">
            <IntroduceHero quickFacts={INTRODUCE_QUICK_FACTS} heroImage={heroImage} />

            <IntroduceSection
              id="core-loop"
              eyebrow="Workflow"
              titleVi="Luồng sản phẩm"
              titleEn="Core product loop"
              descriptionVi="Sản phẩm được tổ chức theo một vòng làm việc giáo viên có thể kiểm soát và giải thích được."
              descriptionEn="The product is organized as an explainable teacher-controlled workflow rather than isolated AI features."
            >
              <IntroduceCoreLoop />
            </IntroduceSection>

            <IntroduceSection
              id="evidence-gallery"
              eyebrow="Evidence"
              titleVi="Hình ảnh thực tế"
              titleEn="Evidence gallery"
              descriptionVi="Các ảnh dưới đây là bằng chứng trực tiếp từ giao diện desktop hiện tại của sản phẩm."
              descriptionEn="The screenshots below are direct desktop captures from the current product build."
            >
              <IntroduceGallery items={INTRODUCE_GALLERY_ITEMS} />
            </IntroduceSection>

            <IntroduceSection
              id="for-educators"
              eyebrow="Educators"
              titleVi="Dành cho người dùng không chuyên kỹ thuật"
              titleEn="For educators and operations staff"
              descriptionVi="Khối tài liệu này ưu tiên giáo viên và nhân sự quản lý cần sử dụng sản phẩm mà không phải đi qua chi tiết kỹ thuật triển khai."
              descriptionEn="This section prioritizes teachers and operators who need to use the product without going through infrastructure details first."
            >
              <div className="grid gap-4 lg:grid-cols-2">
                {INTRODUCE_EDUCATOR_BLOCKS.map((block, index) => (
                  <article
                    key={block.titleEn}
                    className={`rounded-[24px] border border-[rgba(10,21,48,0.08)] px-5 py-5 shadow-[0_12px_36px_rgba(10,21,48,0.05)] ${
                      index % 2 === 0 ? "bg-[#fff8ef]" : "bg-white"
                    }`}
                  >
                    <h3 className="text-xl font-semibold tracking-[-0.03em] text-[#0a1530]">
                      {block.titleVi}
                    </h3>
                    <p className="mt-1 text-sm font-medium text-[#50607d]">{block.titleEn}</p>
                    <p className="mt-4 text-sm leading-7 text-[#24324a]">{block.bodyVi}</p>
                    <p className="mt-3 text-sm leading-7 text-[#50607d]">{block.bodyEn}</p>
                  </article>
                ))}
              </div>
            </IntroduceSection>

            <IntroduceSection
              id="technical-documentation"
              eyebrow="Technical"
              titleVi="Tài liệu kỹ thuật"
              titleEn="Technical documentation"
              descriptionVi="Phần này đóng vai trò lớp chuyển tiếp cho đội IT hoặc nhà phát triển trước khi đọc runbook chi tiết, API và hướng dẫn triển khai đầy đủ."
              descriptionEn="This section acts as the entry layer for IT teams or developers before deeper runbooks, API docs, and deployment guides."
            >
              <div className="grid gap-4 lg:grid-cols-3">
                {INTRODUCE_TECHNICAL_BLOCKS.map((block, index) => (
                  <article
                    key={block.titleEn}
                    className={`rounded-[24px] border border-[rgba(10,21,48,0.08)] px-5 py-5 shadow-[0_12px_36px_rgba(10,21,48,0.05)] ${
                      index === 0 ? "bg-[#eef3fb]" : index === 1 ? "bg-[#f8f5e8]" : "bg-white"
                    }`}
                  >
                    <h3 className="text-lg font-semibold tracking-[-0.03em] text-[#0a1530]">
                      {block.titleVi}
                    </h3>
                    <p className="mt-1 text-sm font-medium text-[#50607d]">{block.titleEn}</p>
                    <p className="mt-4 text-sm leading-7 text-[#24324a]">{block.bodyVi}</p>
                    <p className="mt-3 text-sm leading-7 text-[#50607d]">{block.bodyEn}</p>
                  </article>
                ))}
              </div>
            </IntroduceSection>

            <IntroduceSection
              id="faq"
              eyebrow="FAQ"
              titleVi="Câu hỏi thường gặp"
              titleEn="Frequently asked questions"
              descriptionVi="Một lớp FAQ ngắn cho ban giám khảo, đối tác hoặc người vận hành cần xác nhận phạm vi thực tế của prototype."
              descriptionEn="A short FAQ layer for judges, partners, or operators who need to validate the honest scope of the current prototype."
            >
              <div className="space-y-4">
                {INTRODUCE_FAQ_BLOCKS.map((block) => (
                  <article
                    key={block.titleEn}
                    className="rounded-[24px] border border-[rgba(10,21,48,0.08)] bg-white px-5 py-5 shadow-[0_12px_36px_rgba(10,21,48,0.05)]"
                  >
                    <h3 className="text-lg font-semibold tracking-[-0.03em] text-[#0a1530]">
                      {block.titleVi}
                    </h3>
                    <p className="mt-1 text-sm font-medium text-[#50607d]">{block.titleEn}</p>
                    <p className="mt-4 text-sm leading-7 text-[#24324a]">{block.bodyVi}</p>
                    <p className="mt-3 text-sm leading-7 text-[#50607d]">{block.bodyEn}</p>
                  </article>
                ))}
              </div>
            </IntroduceSection>

            <IntroduceSection
              id="resources"
              eyebrow="Resources"
              titleVi="Tài nguyên"
              titleEn="Resources"
              descriptionVi="Các liên kết này dùng để nối sang hồ sơ dự thi, kho mã nguồn và những tài liệu mở rộng sẽ được bổ sung sau."
              descriptionEn="These links connect the docs page to the contest package, repository, and additional resources that can be published later."
            >
              <div className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-[#0a1530] px-6 py-6 text-white shadow-[0_30px_80px_rgba(10,21,48,0.18)]">
                <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-start">
                  <div>
                    <h3 className="text-2xl font-semibold tracking-[-0.04em] text-white">
                      Hồ sơ tiếp theo / Next materials
                    </h3>
                    <p className="mt-3 max-w-2xl text-sm leading-7 text-white/78">
                      Video hướng dẫn, PDF thao tác từng bước, tài liệu triển khai chi tiết, API
                      schema và runbook cloud có thể được gắn thêm vào section này mà không phải đổi
                      cấu trúc trang.
                    </p>
                  </div>
                  <div className="grid gap-3">
                    {INTRODUCE_RESOURCE_LINKS.map((resource) => (
                      <ResourceLink
                        key={resource.labelEn}
                        href={resource.href}
                        label={`${resource.labelVi} / ${resource.labelEn}`}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </IntroduceSection>
          </div>
        </main>
      </div>
    </div>
  );
}
