import AuthShell from "@/components/auth/AuthShell";
import ForgotPasswordForm from "@/components/auth/ForgotPasswordForm";

export default function ForgotPasswordPage() {
  return (
    <AuthShell
      eyebrow="Recovery"
      title="Quên mật khẩu / Forgot password"
      subtitle="Nhập email tài khoản để chuẩn bị liên kết đặt lại mật khẩu. Với môi trường local, hệ thống có thể hiển thị liên kết debug để tự kiểm tra nhanh."
    >
      <ForgotPasswordForm />
    </AuthShell>
  );
}
