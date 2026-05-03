import { Suspense } from "react";
import AuthShell from "@/components/auth/AuthShell";
import VerifyEmailPanel from "@/components/auth/VerifyEmailPanel";

export default function VerifyEmailPage() {
  return (
    <AuthShell
      eyebrow="Verification"
      title="Xác minh email / Verify email"
      subtitle="Mở liên kết từ email để xác minh ngay, hoặc yêu cầu gửi lại liên kết khi bạn đang có phiên đăng nhập hợp lệ."
    >
      <Suspense
        fallback={
          <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
            Đang tải trạng thái xác minh email...
          </div>
        }
      >
        <VerifyEmailPanel />
      </Suspense>
    </AuthShell>
  );
}
