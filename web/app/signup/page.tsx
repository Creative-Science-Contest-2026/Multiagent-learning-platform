import { Suspense } from "react";
import AuthShell from "@/components/auth/AuthShell";
import SignupForm from "@/components/auth/SignupForm";

export default function SignupPage() {
  return (
    <AuthShell
      eyebrow="Create account"
      title="Tạo tài khoản / Create account"
      subtitle="Chọn vai trò ngay từ đầu để hệ thống mở đúng hành trình sản phẩm cho giáo viên hoặc học sinh."
    >
      <Suspense
        fallback={
          <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
            Đang tải biểu mẫu tạo tài khoản...
          </div>
        }
      >
        <SignupForm />
      </Suspense>
    </AuthShell>
  );
}
