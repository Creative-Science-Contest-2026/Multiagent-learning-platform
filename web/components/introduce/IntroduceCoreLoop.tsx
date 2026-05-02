/* eslint-disable i18n/no-literal-ui-text */
const CORE_LOOP_STEPS = [
  {
    key: "01",
    titleVi: "Tạo Gói kiến thức",
    titleEn: "Create a Knowledge Pack",
    bodyVi: "Giáo viên chuẩn hóa học liệu và mục tiêu học tập thành một bối cảnh dùng chung.",
    bodyEn: "Teachers normalize learning materials and objectives into one trusted context.",
    tint: "bg-[#ffe8d4]",
  },
  {
    key: "02",
    titleVi: "Tạo bài đánh giá",
    titleEn: "Generate an assessment",
    bodyVi: "Bài đánh giá được sinh từ cùng ngữ cảnh học liệu thay vì các câu hỏi rời rạc.",
    bodyEn: "Assessments are generated from the same context instead of detached question prompts.",
    tint: "bg-[#dcecfa]",
  },
  {
    key: "03",
    titleVi: "Gia sư AI đồng hành",
    titleEn: "Run the AI tutor",
    bodyVi: "Học sinh tiếp tục hỏi đáp trên cùng một chủ đề sau đánh giá hoặc trong quá trình học bù.",
    bodyEn: "Students continue guided follow-up within the same topic after assessment or remediation.",
    tint: "bg-[#d9f3e1]",
  },
  {
    key: "04",
    titleVi: "Rà soát chẩn đoán",
    titleEn: "Review diagnosis",
    bodyVi: "Dashboard hiển thị tín hiệu học tập để giáo viên rà soát mức độ hiểu và vùng rủi ro.",
    bodyEn: "The dashboard surfaces learning signals for teacher review of understanding and risk.",
    tint: "bg-[#fde0ec]",
  },
  {
    key: "05",
    titleVi: "Quyết định can thiệp",
    titleEn: "Choose intervention",
    bodyVi: "Giáo viên vẫn là người quyết định hỗ trợ tiếp theo cho từng học sinh hoặc nhóm học sinh.",
    bodyEn: "Teachers remain responsible for choosing the next intervention for each student or cohort.",
    tint: "bg-[#e6e0f5]",
  },
];

export function IntroduceCoreLoop() {
  return (
    <div className="grid gap-4 lg:grid-cols-5">
      {CORE_LOOP_STEPS.map((step) => (
        <article
          key={step.key}
          className={`rounded-[24px] border border-[rgba(10,21,48,0.08)] ${step.tint} px-5 py-5 shadow-[0_12px_36px_rgba(10,21,48,0.06)]`}
        >
          <div className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[#50607d]">
            Step {step.key}
          </div>
          <h3 className="mt-4 text-lg font-semibold tracking-[-0.03em] text-[#0a1530]">
            {step.titleVi}
          </h3>
          <p className="mt-1 text-sm font-medium text-[#50607d]">{step.titleEn}</p>
          <p className="mt-4 text-sm leading-7 text-[#24324a]">{step.bodyVi}</p>
          <p className="mt-2 text-xs leading-6 text-[#50607d]">{step.bodyEn}</p>
        </article>
      ))}
    </div>
  );
}
