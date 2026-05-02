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
      </div>
    </main>
  );
}
