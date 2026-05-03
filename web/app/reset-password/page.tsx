import { Suspense } from "react";
import AuthShell from "@/components/auth/AuthShell";
import ResetPasswordForm from "@/components/auth/ResetPasswordForm";

export default function ResetPasswordPage() {
  return (
    <AuthShell
      eyebrow="Recovery"
      title="Đặt lại mật khẩu / Reset password"
      subtitle="Liên kết khôi phục sẽ mở trang này với token bảo mật để xác nhận mật khẩu mới."
    >
      <Suspense
        fallback={
          <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
            Đang tải liên kết đặt lại mật khẩu...
          </div>
        }
      >
        <ResetPasswordForm />
      </Suspense>
    </AuthShell>
  );
}
