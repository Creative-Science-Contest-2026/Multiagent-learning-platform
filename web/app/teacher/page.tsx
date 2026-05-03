import Link from "next/link";

export default function TeacherHomePage() {
  return (
    <main className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f6f1e8_100%)] px-4 py-8 text-[#0a1530]">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="rounded-[32px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_24px_60px_rgba(10,21,48,0.08)]">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7a869c]">Teacher workspace</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-[-0.05em]">Điều phối lớp học với AI có kiểm soát</h1>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-[#50607d]">
            Đây là không gian giáo viên: tạo gói kiến thức, sinh bài đánh giá, cấu hình gia sư, theo dõi chẩn đoán và ra quyết định can thiệp.
          </p>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          <Link href="/knowledge" className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_20px_50px_rgba(10,21,48,0.06)]">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#7a869c]">Step 1</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.04em]">Gói kiến thức</h2>
            <p className="mt-3 text-sm leading-7 text-[#50607d]">
              Nhập học liệu, quản lý metadata và theo dõi tiến độ indexing cho từng pack.
            </p>
          </Link>
          <Link href="/dashboard" className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_20px_50px_rgba(10,21,48,0.06)]">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#7a869c]">Step 2</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.04em]">Dashboard lớp học</h2>
            <p className="mt-3 text-sm leading-7 text-[#50607d]">
              Xem tín hiệu chẩn đoán, phản hồi khuyến nghị và theo dõi hành động can thiệp.
            </p>
          </Link>
          <Link href="/agents" className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_20px_50px_rgba(10,21,48,0.06)]">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#7a869c]">Step 3</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.04em]">Gia sư lớp học</h2>
            <p className="mt-3 text-sm leading-7 text-[#50607d]">
              Cấu hình pack gia sư, quy tắc hỗ trợ và bối cảnh dạy học cho từng lớp.
            </p>
          </Link>
        </section>
      </div>
    </main>
  );
}
