"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Button from "@/components/ui/Button";
import { resetPassword } from "@/lib/auth-api";

export default function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token")?.trim() ?? "";
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!token) {
      setError("Thiếu token đặt lại mật khẩu.");
      return;
    }
    setSubmitting(true);
    setError("");
    setSuccess("");

    try {
      await resetPassword({ token, password });
      setSuccess("Mật khẩu đã được cập nhật. Bạn có thể đăng nhập lại ngay bây giờ.");
      router.push("/login");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể đặt lại mật khẩu.");
    } finally {
      setSubmitting(false);
    }
  };

  if (!token) {
    return (
      <div className="rounded-[24px] border border-amber-200 bg-amber-50 px-5 py-5 text-sm leading-7 text-amber-900">
        Liên kết đặt lại mật khẩu không hợp lệ hoặc đã thiếu token bảo mật.
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <label className="grid gap-2 text-sm font-medium text-[#0a1530]">
        Mật khẩu mới / New password
        <input
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          type="password"
          className="rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3 outline-none transition-shadow focus:shadow-[0_0_0_4px_rgba(10,21,48,0.08)]"
          placeholder="EvenStronger456!"
        />
      </label>

      {error ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      {success ? (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
          {success}
        </div>
      ) : null}

      <Button type="submit" loading={submitting} className="w-full justify-center rounded-2xl py-3">
        Đặt lại mật khẩu
      </Button>
    </form>
  );
}
