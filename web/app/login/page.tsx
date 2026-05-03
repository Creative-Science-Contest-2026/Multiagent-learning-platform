import { Suspense } from "react";
import AuthShell from "@/components/auth/AuthShell";
import LoginForm from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <AuthShell
      eyebrow="Sign in"
      title="Đăng nhập / Sign in"
      subtitle="Đăng nhập để đi vào đúng không gian giáo viên, học sinh hoặc quản trị viên của bạn."
    >
      <Suspense
        fallback={
          <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
            Đang tải biểu mẫu đăng nhập...
          </div>
        }
      >
        <LoginForm />
      </Suspense>
    </AuthShell>
  );
}
