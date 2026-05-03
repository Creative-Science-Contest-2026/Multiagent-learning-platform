"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { googleLoginUrl, postAuthRedirect, signup, type PublicRole } from "@/lib/auth-api";
import RolePicker from "./RolePicker";

export default function SignupForm({ initialRole = "teacher" }: { initialRole?: PublicRole }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setUser } = useAuth();
  const [role, setRole] = useState<PublicRole>(initialRole);
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const nextPath = searchParams.get("next");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      const result = await signup({
        display_name: displayName.trim(),
        email: email.trim(),
        password,
        role,
      });
      setUser(result.user);
      router.push(postAuthRedirect(result.user.role, nextPath));
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể tạo tài khoản.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-3">
        <p className="text-sm font-semibold text-[#0a1530]">Chọn vai trò trước khi tạo tài khoản</p>
        <RolePicker selectedRole={role} onSelect={setRole} />
      </div>

      <div className="grid gap-4">
        <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
          Họ và tên / Full name
          <input
            value={displayName}
            onChange={(event) => setDisplayName(event.target.value)}
            className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3 outline-none transition-shadow focus:shadow-[0_0_0_4px_rgba(10,21,48,0.08)]"
            placeholder="Nguyễn Văn A"
          />
        </label>
        <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
          Email
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            type="email"
            className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3 outline-none transition-shadow focus:shadow-[0_0_0_4px_rgba(10,21,48,0.08)]"
            placeholder="you@example.com"
          />
        </label>
        <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
          Mật khẩu / Password
          <input
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3 outline-none transition-shadow focus:shadow-[0_0_0_4px_rgba(10,21,48,0.08)]"
            placeholder="StrongPass123!"
          />
        </label>
      </div>

      {error ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      <div className="grid gap-3">
        <Button type="submit" loading={submitting} className="w-full justify-center rounded-2xl py-3">
          Tạo tài khoản / Create account
        </Button>
        <Button
          type="button"
          variant="secondary"
          className="w-full justify-center rounded-2xl py-3"
          onClick={() => {
            window.location.assign(googleLoginUrl(role, nextPath));
          }}
        >
          Tiếp tục với Google / Continue with Google
        </Button>
      </div>
    </form>
  );
}
