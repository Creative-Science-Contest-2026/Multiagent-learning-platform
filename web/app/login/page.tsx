import AuthShell from "@/components/auth/AuthShell";
import LoginForm from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <AuthShell
      eyebrow="Sign in"
      title="Đăng nhập / Sign in"
      subtitle="Đăng nhập để đi vào đúng không gian giáo viên, học sinh hoặc quản trị viên của bạn."
    >
      <LoginForm />
    </AuthShell>
  );
}
