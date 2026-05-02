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
      </div>
    </main>
  );
}
