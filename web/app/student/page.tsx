import Link from "next/link";

export default function StudentHomePage() {
  return (
    <main className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#eef3fb_100%)] px-4 py-8 text-[#0a1530]">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="rounded-[32px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_24px_60px_rgba(10,21,48,0.08)]">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7a869c]">Student workspace</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-[-0.05em]">Học tập với gia sư AI theo tiến độ của riêng bạn</h1>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-[#50607d]">
            Đây là không gian học sinh: hỏi đáp với gia sư AI, làm bài đánh giá, xem phản hồi và theo dõi sự tiến bộ của chính mình.
          </p>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          <Link href="/playground" className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_20px_50px_rgba(10,21,48,0.06)]">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#7a869c]">Start here</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.04em]">Vào gia sư AI</h2>
            <p className="mt-3 text-sm leading-7 text-[#50607d]">
              Hỏi đáp theo gói tri thức, nhận giải thích từng bước và câu hỏi follow-up.
            </p>
          </Link>
          <Link href="/dashboard/student" className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_20px_50px_rgba(10,21,48,0.06)]">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#7a869c]">Progress</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.04em]">Xem tiến độ học</h2>
            <p className="mt-3 text-sm leading-7 text-[#50607d]">
              Theo dõi điểm số gần đây, chủ đề cần ôn lại và lộ trình học gợi ý tiếp theo.
            </p>
          </Link>
          <Link href="/introduce" className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_20px_50px_rgba(10,21,48,0.06)]">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#7a869c]">Docs</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.04em]">Mở tài liệu hướng dẫn</h2>
            <p className="mt-3 text-sm leading-7 text-[#50607d]">
              Xem tổng quan sản phẩm, ảnh minh họa và tài liệu sử dụng khi cần hỗ trợ thêm.
            </p>
          </Link>
        </section>
      </div>
    </main>
  );
}
