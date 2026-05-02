export interface IntroduceQuickFact {
  labelVi: string;
  labelEn: string;
  vi: string;
  en: string;
}

export interface IntroduceSectionLink {
  id: string;
  labelVi: string;
  labelEn: string;
}

export interface IntroduceGalleryItem {
  id: string;
  src: string;
  titleVi: string;
  titleEn: string;
  captionVi: string;
  captionEn: string;
  tagVi: string;
  tagEn: string;
}

export interface IntroduceDocBlock {
  titleVi: string;
  titleEn: string;
  bodyVi: string;
  bodyEn: string;
}

export interface IntroduceResourceLink {
  labelVi: string;
  labelEn: string;
  href: string;
}

export const INTRODUCE_SECTIONS: IntroduceSectionLink[] = [
  { id: "overview", labelVi: "Tổng quan", labelEn: "Overview" },
  { id: "core-loop", labelVi: "Luồng sản phẩm", labelEn: "Core Loop" },
  { id: "evidence-gallery", labelVi: "Hình ảnh thực tế", labelEn: "Evidence Gallery" },
  {
    id: "for-educators",
    labelVi: "Dành cho người dùng không chuyên kỹ thuật",
    labelEn: "For Educators",
  },
  {
    id: "technical-documentation",
    labelVi: "Tài liệu kỹ thuật",
    labelEn: "Technical Documentation",
  },
  { id: "faq", labelVi: "Câu hỏi thường gặp", labelEn: "FAQ" },
  { id: "resources", labelVi: "Tài nguyên", labelEn: "Resources" },
];

export const INTRODUCE_QUICK_FACTS: IntroduceQuickFact[] = [
  {
    labelVi: "Giai đoạn hiện tại",
    labelEn: "Current stage",
    vi: "Prototype/demo đã có minh chứng chạy thử",
    en: "Validated prototype/demo with working proof",
  },
  {
    labelVi: "Lĩnh vực",
    labelEn: "Field",
    vi: "Giáo dục",
    en: "Education",
  },
  {
    labelVi: "Định vị sản phẩm",
    labelEn: "Product framing",
    vi: "Gia sư học tập thích ứng do giáo viên kiểm soát",
    en: "Teacher-controlled adaptive tutoring",
  },
];

export const INTRODUCE_GALLERY_ITEMS: IntroduceGalleryItem[] = [
  {
    id: "knowledge-pack",
    src: "/introduce/anh1_goi_kien_thuc.jpg",
    titleVi: "Gói kiến thức",
    titleEn: "Knowledge Pack",
    captionVi: "Giáo viên thiết lập nguồn tri thức và bối cảnh lớp học từ chính học liệu của mình.",
    captionEn: "Teachers establish trusted classroom context from their own learning materials.",
    tagVi: "Thiết lập giáo viên",
    tagEn: "Teacher setup",
  },
  {
    id: "teacher-dashboard",
    src: "/introduce/anh2_bang_dieu_khien_giao_vien.jpg",
    titleVi: "Bảng điều khiển giáo viên",
    titleEn: "Teacher dashboard",
    captionVi: "Giáo viên xem tín hiệu học tập, rà soát chẩn đoán và quyết định bước can thiệp tiếp theo.",
    captionEn: "Teachers review learning signals, inspect diagnosis cues, and choose the next intervention.",
    tagVi: "Bằng chứng",
    tagEn: "Evidence",
  },
  {
    id: "tutor",
    src: "/introduce/anh3_gia_su.jpg",
    titleVi: "Gia sư AI",
    titleEn: "AI tutor",
    captionVi: "Học sinh tiếp tục hỏi đáp trên cùng một ngữ cảnh học tập đã được giáo viên xác lập.",
    captionEn: "Students continue guided Q&A in the same teacher-defined learning context.",
    tagVi: "Học tập",
    tagEn: "Learning",
  },
  {
    id: "marketplace",
    src: "/introduce/anh4_thi_truong.jpg",
    titleVi: "Thị trường gói kiến thức",
    titleEn: "Knowledge marketplace",
    captionVi: "Giáo viên có thể duyệt, xem trước và nhập các gói kiến thức có thể tái sử dụng.",
    captionEn: "Teachers can browse, preview, and import reusable knowledge packs.",
    tagVi: "Tái sử dụng",
    tagEn: "Reuse",
  },
  {
    id: "chat-workspace",
    src: "/introduce/anh5_tro_chuyen.jpg",
    titleVi: "Không gian trò chuyện",
    titleEn: "Chat workspace",
    captionVi: "Không gian hỗ trợ hỏi đáp và theo dõi trao đổi học tập theo dạng hội thoại liên tục.",
    captionEn: "A conversational workspace for guided tutoring exchange and follow-up support.",
    tagVi: "Tương tác",
    tagEn: "Interaction",
  },
  {
    id: "memory-surface",
    src: "/introduce/anh6_bo_nho.jpg",
    titleVi: "Bề mặt bộ nhớ",
    titleEn: "Memory surface",
    captionVi: "Bề mặt mở rộng cho việc lưu dấu và rà soát ngữ cảnh học tập trong hệ thống.",
    captionEn: "An extended surface for preserving and reviewing learning context within the system.",
    tagVi: "Bổ trợ",
    tagEn: "Support",
  },
  {
    id: "settings",
    src: "/introduce/anh7_cai_dat.jpg",
    titleVi: "Cài đặt hệ thống",
    titleEn: "System settings",
    captionVi: "Khu vực cấu hình phục vụ vận hành kỹ thuật và chuẩn bị môi trường triển khai.",
    captionEn: "A configuration area for technical setup and deployment preparation.",
    tagVi: "Kỹ thuật",
    tagEn: "Technical",
  },
];

export const INTRODUCE_EDUCATOR_BLOCKS: IntroduceDocBlock[] = [
  {
    titleVi: "Tạo Gói kiến thức từ học liệu của mình",
    titleEn: "Create a Knowledge Pack from your own materials",
    bodyVi:
      "Tải học liệu lên, điền chủ đề, mức độ khó, chương trình học và mục tiêu học tập để tạo bối cảnh lớp học mà hệ thống sẽ dùng xuyên suốt.",
    bodyEn:
      "Upload classroom materials and define subject, difficulty, curriculum, and learning objectives to create the shared context used across the workflow.",
  },
  {
    titleVi: "Tạo bài đánh giá tự động từ Gói kiến thức",
    titleEn: "Generate an assessment from the Knowledge Pack",
    bodyVi:
      "Dùng cùng Gói kiến thức để tạo bài đánh giá bám sát nội dung giáo viên đã xác định trước đó, thay vì sinh câu hỏi rời rạc không có căn cứ.",
    bodyEn:
      "Use the same Knowledge Pack to generate an assessment grounded in teacher-approved materials rather than detached question generation.",
  },
  {
    titleVi: "Cho học sinh sử dụng gia sư AI để hỏi đáp",
    titleEn: "Let students use the AI tutor for follow-up questions",
    bodyVi:
      "Sau khi có bài đánh giá hoặc khi cần học bù, học sinh có thể tiếp tục hỏi đáp với gia sư AI trên cùng một chủ đề và bối cảnh lớp học.",
    bodyEn:
      "After assessment or during follow-up study, students can continue asking the AI tutor within the same topic and classroom context.",
  },
  {
    titleVi: "Xem chẩn đoán và xác định học sinh cần can thiệp",
    titleEn: "Review diagnosis and identify students needing intervention",
    bodyVi:
      "Giáo viên sử dụng dashboard để xem tín hiệu học tập, phát hiện nhóm học sinh cần hỗ trợ và chọn bước can thiệp phù hợp.",
    bodyEn:
      "Teachers use the dashboard to inspect learning signals, identify students needing support, and choose the next intervention step.",
  },
];

export const INTRODUCE_TECHNICAL_BLOCKS: IntroduceDocBlock[] = [
  {
    titleVi: "Yêu cầu môi trường",
    titleEn: "Environment requirements",
    bodyVi:
      "Khuyến nghị Python 3.11+, Node.js 18+, trình duyệt hiện đại và khả năng cấu hình dịch vụ AI qua biến môi trường. Các chi tiết cụ thể sẽ được trình bày trong tài liệu kỹ thuật đi kèm.",
    bodyEn:
      "Recommended: Python 3.11+, Node.js 18+, a modern browser, and environment-variable based AI service configuration. Deeper details belong in the technical runbooks.",
  },
  {
    titleVi: "Cài đặt và triển khai",
    titleEn: "Installation and deployment",
    bodyVi:
      "Hệ thống có thể chạy cục bộ để demo hoặc đóng gói để triển khai trên máy chủ. Hướng dẫn triển khai sẽ bao gồm cấu hình môi trường, API và cách khởi động frontend/backend.",
    bodyEn:
      "The system can run locally for demos or be packaged for server deployment. Deployment guidance covers environment configuration, APIs, and frontend/backend startup.",
  },
  {
    titleVi: "Tích hợp và vận hành",
    titleEn: "Integration and operations",
    bodyVi:
      "Tài liệu kỹ thuật cần hỗ trợ đội IT hoặc nhà phát triển tích hợp sản phẩm với quy trình vận hành hiện có, theo hướng thận trọng và phù hợp phạm vi prototype hiện tại.",
    bodyEn:
      "Technical documentation should help IT operators or developers integrate the product into existing workflows without overclaiming beyond the current prototype scope.",
  },
];

export const INTRODUCE_FAQ_BLOCKS: IntroduceDocBlock[] = [
  {
    titleVi: "Sản phẩm đã triển khai rộng rãi chưa?",
    titleEn: "Is the product already widely deployed?",
    bodyVi:
      "Chưa. Ở trạng thái hiện tại, đây là prototype/demo có minh chứng chạy thử, phù hợp cho trình diễn, đánh giá giải pháp và chuẩn bị cho các thử nghiệm tiếp theo.",
    bodyEn:
      "Not yet. The current product is a validated prototype/demo suitable for demonstration, solution review, and preparation for later pilot work.",
  },
  {
    titleVi: "AI có tự quyết định thay giáo viên không?",
    titleEn: "Does the AI make final decisions instead of the teacher?",
    bodyVi:
      "Không. Sản phẩm được định vị là hệ thống gia sư học tập thích ứng do giáo viên kiểm soát; phần chẩn đoán và gợi ý chỉ đóng vai trò hỗ trợ để giáo viên xem xét.",
    bodyEn:
      "No. The product is framed as teacher-controlled adaptive tutoring; diagnosis and recommendations remain support signals for teacher review.",
  },
  {
    titleVi: "Trang này dùng để làm gì?",
    titleEn: "What is this page for?",
    bodyVi:
      "Trang `/introduce` giúp ban giám khảo, đối tác và người vận hành hiểu nhanh sản phẩm, xem bằng chứng giao diện thật và truy cập các lớp tài liệu phù hợp với nhu cầu của họ.",
    bodyEn:
      "The `/introduce` page helps judges, partners, and operators understand the product quickly, inspect real interface proof, and reach the right documentation layer.",
  },
];

export const INTRODUCE_RESOURCE_LINKS: IntroduceResourceLink[] = [
  {
    labelVi: "Kho mã nguồn dự án",
    labelEn: "Project source repository",
    href: "https://github.com/Creative-Science-Contest-2026/Multiagent-learning-platform",
  },
  {
    labelVi: "Gói hồ sơ cuộc thi trong repo",
    labelEn: "Contest submission package in the repository",
    href: "https://github.com/Creative-Science-Contest-2026/Multiagent-learning-platform/tree/main/docs/contest",
  },
  {
    labelVi: "Hồ sơ email VnExpress",
    labelEn: "VnExpress email submission draft",
    href: "https://github.com/Creative-Science-Contest-2026/Multiagent-learning-platform/blob/main/docs/contest/VNEXPRESS_EMAIL_SUBMISSION_DRAFT.vi.md",
  },
];
