"use client";

import Link from "next/link";
import { useState } from "react";
import { useSearchParams } from "next/navigation";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { sendVerificationEmail, verifyEmailToken } from "@/lib/auth-api";

export default function VerifyEmailPanel() {
  const { user } = useAuth();
  const searchParams = useSearchParams();
  const token = searchParams.get("token")?.trim() ?? "";
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [debugUrl, setDebugUrl] = useState("");

  const handleVerifyToken = async () => {
    if (!token) {
      return;
    }
    setSubmitting(true);
    setError("");
    setSuccess("");

    try {
      await verifyEmailToken(token);
      setSuccess("Email đã được xác minh. Bạn có thể quay lại đăng nhập hoặc tiếp tục vào sản phẩm.");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể xác minh email.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleSendVerification = async () => {
    setSubmitting(true);
    setError("");
    setSuccess("");
    setDebugUrl("");

    try {
      const result = await sendVerificationEmail();
      setSuccess("Liên kết xác minh đã được chuẩn bị cho tài khoản hiện tại.");
      setDebugUrl(result.debug_url ?? "");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Không thể gửi lại email xác minh.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {token ? (
        <>
          <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
            Nhấn nút bên dưới để xác minh email bằng token trong liên kết bạn vừa mở.
          </div>
          <Button type="button" loading={submitting} className="w-full justify-center rounded-2xl py-3" onClick={handleVerifyToken}>
            Xác minh email
          </Button>
        </>
      ) : user ? (
        <>
          <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
            Tài khoản hiện tại có thể yêu cầu gửi lại email xác minh để tăng độ tin cậy và hỗ trợ phục hồi an toàn hơn.
          </div>
          <Button type="button" loading={submitting} className="w-full justify-center rounded-2xl py-3" onClick={handleSendVerification}>
            Gửi lại email xác minh
          </Button>
        </>
      ) : (
        <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
          Hãy mở trang này bằng liên kết xác minh trong email, hoặc <Link href="/login" className="font-semibold underline">đăng nhập</Link> để yêu cầu gửi lại email xác minh.
        </div>
      )}

      {error ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      {success ? (
        <div className="space-y-3 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
          <p>{success}</p>
          {debugUrl ? (
            <Link href={debugUrl} className="font-semibold underline">
              Mở liên kết xác minh cục bộ
            </Link>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
