"use client";

import Link from "next/link";
import { useState } from "react";
import Button from "@/components/ui/Button";
import { requestPasswordReset } from "@/lib/auth-api";

export default function ForgotPasswordForm() {
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [debugUrl, setDebugUrl] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    setSuccess("");
    setDebugUrl("");

    try {
      const result = await requestPasswordReset(email);
      setSuccess("Nếu email tồn tại, hệ thống đã chuẩn bị liên kết khôi phục mật khẩu.");
      setDebugUrl(result.debug_url ?? "");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể gửi liên kết khôi phục.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
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

      {error ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      {success ? (
        <div className="space-y-3 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
          <p>{success}</p>
          {debugUrl ? (
            <Link href={debugUrl} className="font-semibold underline" aria-label="Mở liên kết khôi phục">
              Mở liên kết khôi phục
            </Link>
          ) : null}
        </div>
      ) : null}

      <Button type="submit" loading={submitting} className="w-full justify-center rounded-2xl py-3">
        Gửi liên kết / Send link
      </Button>
    </form>
  );
}
