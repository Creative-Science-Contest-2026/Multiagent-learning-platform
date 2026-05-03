import AdminUsersPanel from "@/components/auth/AdminUsersPanel";

export default function AdminHomePage() {
  return (
    <main className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f4f4f7_100%)] px-4 py-8 text-[#0a1530]">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="rounded-[32px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_24px_60px_rgba(10,21,48,0.08)]">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7a869c]">Admin workspace</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-[-0.05em]">Quản lý tài khoản và kiểm soát truy cập</h1>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-[#50607d]">
            Đây là không gian quản trị tối thiểu cho việc kiểm tra tình trạng tài khoản, vai trò và khả năng truy cập hệ thống.
          </p>
        </header>
        <AdminUsersPanel />
      </div>
    </main>
  );
}
