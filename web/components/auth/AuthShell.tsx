import Link from "next/link";

export default function AuthShell({
  eyebrow,
  title,
  subtitle,
  children,
}: {
  eyebrow: string;
  title: string;
  subtitle: string;
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#fffdf9_0%,#f6f1e8_48%,#eef3fb_100%)] px-4 py-8 text-[#0a1530]">
      <div className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-6xl items-center justify-center">
        <div className="grid w-full overflow-hidden rounded-[32px] border border-[rgba(10,21,48,0.08)] bg-white shadow-[0_30px_80px_rgba(10,21,48,0.12)] lg:grid-cols-[minmax(0,1.05fr)_520px]">
          <section className="hidden flex-col justify-between bg-[#0a1530] px-10 py-10 text-white lg:flex">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-white/58">
                DeepTutor Auth
              </p>
              <h1 className="mt-6 text-4xl font-semibold tracking-[-0.05em]">
                Học tập có kiểm soát. Tài khoản có chủ sở hữu.
              </h1>
              <p className="mt-5 max-w-md text-sm leading-7 text-white/72">
                Từ bản prototype ẩn danh sang nền tảng nhiều người dùng thật:
                giáo viên, học sinh và quản trị viên đi vào các không gian khác nhau
                với dữ liệu, phiên học và quyền truy cập rõ ràng.
              </p>
            </div>
            <div className="space-y-4">
              <div className="rounded-[24px] border border-white/10 bg-white/6 px-5 py-4">
                <p className="text-sm font-semibold text-white">Teacher workspace</p>
                <p className="mt-2 text-sm leading-6 text-white/68">
                  Gói kiến thức, đánh giá, dashboard, chẩn đoán, can thiệp.
                </p>
              </div>
              <div className="rounded-[24px] border border-white/10 bg-white/6 px-5 py-4">
                <p className="text-sm font-semibold text-white">Student workspace</p>
                <p className="mt-2 text-sm leading-6 text-white/68">
                  Gia sư AI, bài đánh giá, tiến độ cá nhân và hỗ trợ học tập.
                </p>
              </div>
            </div>
          </section>

          <section className="px-5 py-6 sm:px-8 sm:py-8 lg:px-10 lg:py-10">
            <div className="mb-8 flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7a869c]">
                  {eyebrow}
                </p>
                <h2 className="mt-3 text-3xl font-semibold tracking-[-0.04em] text-[#0a1530]">
                  {title}
                </h2>
                <p className="mt-3 max-w-lg text-sm leading-7 text-[#50607d]">{subtitle}</p>
              </div>
              <Link
                href="/introduce"
                className="rounded-xl border border-[rgba(10,21,48,0.12)] px-3 py-2 text-sm font-medium text-[#0a1530] transition-colors hover:bg-[#eef3fb]"
              >
                Giới thiệu
              </Link>
            </div>

            {children}
          </section>
        </div>
      </div>
    </div>
  );
}
