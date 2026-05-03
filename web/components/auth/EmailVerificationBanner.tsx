"use client";

import Link from "next/link";
import { useState } from "react";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { sendVerificationEmail } from "@/lib/auth-api";

export default function EmailVerificationBanner() {
  const { user, refreshUser } = useAuth();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [debugUrl, setDebugUrl] = useState("");

  if (!user || user.email_verified_at) {
    return null;
  }

  const handleResend = async () => {
    setSubmitting(true);
    setError("");
    setSuccess("");
    setDebugUrl("");
    try {
      const result = await sendVerificationEmail();
      setSuccess("Email xác minh đã được gửi lại cho tài khoản hiện tại.");
      setDebugUrl(result.debug_url ?? "");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể gửi lại email xác minh.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleRefresh = async () => {
    setSubmitting(true);
    setError("");
    try {
      const nextUser = await refreshUser();
      if (nextUser?.email_verified_at) {
        setSuccess("Trạng thái tài khoản đã được cập nhật. Email của bạn đã được xác minh.");
        setDebugUrl("");
        return;
      }
      setSuccess("Tài khoản vẫn chưa có dấu xác minh. Hãy kiểm tra email rồi tải lại trạng thái.");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể tải lại trạng thái xác minh.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="rounded-[28px] border border-amber-200 bg-[linear-gradient(180deg,#fff9ec_0%,#fff4d9_100%)] px-5 py-5 shadow-[0_16px_40px_rgba(191,124,0,0.08)]">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="space-y-2">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-amber-800/80">Email verification</p>
          <h2 className="text-xl font-semibold tracking-[-0.03em] text-[#0a1530]">
            Xác minh email để tăng độ tin cậy và phục hồi tài khoản an toàn hơn
          </h2>
          <p className="max-w-3xl text-sm leading-7 text-[#6a5423]">
            Tài khoản <span className="font-semibold text-[#0a1530]">{user.email}</span> chưa có dấu xác minh. Bạn vẫn có
            thể dùng sản phẩm, nhưng nên xác minh sớm để giảm rủi ro với đăng nhập Google, khôi phục mật khẩu và kiểm soát truy cập.
          </p>
        </div>

        <div className="flex flex-col gap-3 lg:min-w-[320px]">
          <Button type="button" loading={submitting} className="w-full justify-center rounded-2xl py-3" onClick={handleResend}>
            Gửi lại email xác minh
          </Button>
          <Button
            type="button"
            variant="secondary"
            className="w-full justify-center rounded-2xl py-3"
            onClick={handleRefresh}
          >
            Tôi đã xác minh xong, tải lại trạng thái
          </Button>
          <Link
            href="/verify-email"
            className="inline-flex justify-center rounded-2xl border border-[rgba(10,21,48,0.12)] px-4 py-3 text-sm font-medium text-[#0a1530] transition-colors hover:bg-white/70"
          >
            Mở trang xác minh
          </Link>
        </div>
      </div>

      {error ? (
        <div className="mt-4 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>
      ) : null}

      {success ? (
        <div className="mt-4 space-y-3 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
          <p>{success}</p>
          {debugUrl ? (
            <Link href={debugUrl} className="font-semibold underline">
              Mở liên kết xác minh cục bộ
            </Link>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}
