"use client";

import { useEffect, useState } from "react";
import Button from "@/components/ui/Button";
import { createAdminUser, listAdminUsers, type AdminUserRecord, type AppRole } from "@/lib/auth-api";

const PUBLIC_ADMIN_ROLES: AppRole[] = ["teacher", "student", "admin"];

export default function AdminUsersPanel() {
  const [users, setUsers] = useState<AdminUserRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<AppRole>("teacher");

  const loadUsers = async () => {
    const payload = await listAdminUsers();
    setUsers(payload.users);
    setLoading(false);
  };

  useEffect(() => {
    void loadUsers().catch((loadError) => {
      setError(loadError instanceof Error ? loadError.message : "Không thể tải danh sách tài khoản.");
      setLoading(false);
    });
  }, []);

  const handleCreateUser = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      const result = await createAdminUser({
        display_name: displayName.trim(),
        email: email.trim(),
        password,
        role,
      });
      setUsers((current) => [...current, result.user]);
      setDisplayName("");
      setEmail("");
      setPassword("");
      setRole("teacher");
    } catch (saveError) {
      setError(saveError instanceof Error ? saveError.message : "Không thể tạo tài khoản.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1.1fr)_360px]">
      <section className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_24px_60px_rgba(10,21,48,0.08)]">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold tracking-[-0.03em] text-[#0a1530]">Danh sách tài khoản</h2>
            <p className="mt-2 text-sm leading-7 text-[#50607d]">
              Kiểm tra nhanh vai trò, trạng thái và email của các tài khoản đã có trong hệ thống.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="mt-6 rounded-2xl bg-[#f4f4f7] px-4 py-5 text-sm text-[#50607d]">Đang tải danh sách tài khoản...</div>
        ) : (
          <div className="mt-6 overflow-hidden rounded-2xl border border-[rgba(10,21,48,0.08)]">
            <table className="min-w-full divide-y divide-[rgba(10,21,48,0.08)] text-sm">
              <thead className="bg-[#f8f5ef] text-left text-[#50607d]">
                <tr>
                  <th className="px-4 py-3 font-medium">Người dùng</th>
                  <th className="px-4 py-3 font-medium">Vai trò</th>
                  <th className="px-4 py-3 font-medium">Trạng thái</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[rgba(10,21,48,0.08)] bg-white text-[#0a1530]">
                {users.map((user) => (
                  <tr key={user.id}>
                    <td className="px-4 py-4">
                      <div className="font-medium">{user.display_name}</div>
                      <div className="mt-1 text-xs text-[#50607d]">{user.email}</div>
                    </td>
                    <td className="px-4 py-4 capitalize">{user.role}</td>
                    <td className="px-4 py-4 capitalize">{user.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 shadow-[0_24px_60px_rgba(10,21,48,0.08)]">
        <h2 className="text-xl font-semibold tracking-[-0.03em] text-[#0a1530]">Tạo tài khoản nội bộ</h2>
        <p className="mt-2 text-sm leading-7 text-[#50607d]">
          Tạo giáo viên, học sinh hoặc quản trị viên nội bộ trực tiếp từ khu vực admin.
        </p>

        <form onSubmit={handleCreateUser} className="mt-6 space-y-4">
          <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
            Họ và tên
            <input value={displayName} onChange={(event) => setDisplayName(event.target.value)} className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3" />
          </label>
          <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
            Email
            <input value={email} onChange={(event) => setEmail(event.target.value)} type="email" className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3" />
          </label>
          <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
            Mật khẩu tạm thời
            <input value={password} onChange={(event) => setPassword(event.target.value)} type="password" className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3" />
          </label>
          <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
            Vai trò
            <select value={role} onChange={(event) => setRole(event.target.value as AppRole)} className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3">
              {PUBLIC_ADMIN_ROLES.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </label>

          {error ? (
            <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
              {error}
            </div>
          ) : null}

          <Button type="submit" loading={saving} className="w-full justify-center rounded-2xl py-3">
            Tạo tài khoản
          </Button>
        </form>
      </section>
    </div>
  );
}
