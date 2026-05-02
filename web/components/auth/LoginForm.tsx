"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { appHomeForRole, googleLoginUrl, login } from "@/lib/auth-api";

export default function LoginForm() {
  const router = useRouter();
  const { setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      const result = await login({
        email: email.trim(),
        password,
      });
      setUser(result.user);
      router.push(appHomeForRole(result.user.role));
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể đăng nhập.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4">
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
          Đăng nhập / Sign in
        </Button>
        <Button
          type="button"
          variant="secondary"
          className="w-full justify-center rounded-2xl py-3"
          onClick={() => {
            window.location.assign(googleLoginUrl("student"));
          }}
        >
          Tiếp tục với Google / Continue with Google
        </Button>
      </div>

      <div className="flex items-center justify-between gap-4 text-sm text-[#50607d]">
        <Link href="/forgot-password" className="transition-colors hover:text-[#0a1530]">
          Quên mật khẩu?
        </Link>
        <Link href="/signup" className="font-medium text-[#0a1530] transition-colors hover:text-[#233b73]">
          Tạo tài khoản mới
        </Link>
      </div>
    </form>
  );
}
