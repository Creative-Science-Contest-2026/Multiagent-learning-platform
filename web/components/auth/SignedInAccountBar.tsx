"use client";

import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";

const roleLabel: Record<string, string> = {
  teacher: "Giáo viên",
  student: "Học sinh",
  admin: "Quản trị viên",
};

export default function SignedInAccountBar() {
  const router = useRouter();
  const { user, logout } = useAuth();

  if (!user) {
    return null;
  }

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <section className="rounded-[24px] border border-[rgba(10,21,48,0.08)] bg-white px-5 py-4 shadow-[0_14px_34px_rgba(10,21,48,0.06)]">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-[#eef3fb] px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-[#233b73]">
              {roleLabel[user.role] ?? user.role}
            </span>
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${
                user.email_verified_at
                  ? "bg-emerald-100 text-emerald-800"
                  : "bg-amber-100 text-amber-800"
              }`}
            >
              {user.email_verified_at ? "Email đã xác minh" : "Chưa xác minh email"}
            </span>
          </div>
          <div>
            <p className="text-lg font-semibold tracking-[-0.03em] text-[#0a1530]">{user.display_name}</p>
            <p className="text-sm text-[#50607d]">{user.email}</p>
          </div>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <Button
            type="button"
            variant="secondary"
            className="justify-center rounded-2xl px-4 py-3"
            onClick={() => router.push("/verify-email")}
          >
            Quản lý xác minh email
          </Button>
          <Button type="button" className="justify-center rounded-2xl px-4 py-3" onClick={handleLogout}>
            Đăng xuất
          </Button>
        </div>
      </div>
    </section>
  );
}
