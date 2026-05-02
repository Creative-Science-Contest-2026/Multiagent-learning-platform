import AuthShell from "@/components/auth/AuthShell";
import SignupForm from "@/components/auth/SignupForm";

export default function SignupPage() {
  return (
    <AuthShell
      eyebrow="Create account"
      title="Tạo tài khoản / Create account"
      subtitle="Chọn vai trò ngay từ đầu để hệ thống mở đúng hành trình sản phẩm cho giáo viên hoặc học sinh."
    >
      <SignupForm />
    </AuthShell>
  );
}
