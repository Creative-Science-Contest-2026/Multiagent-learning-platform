import AuthShell from "@/components/auth/AuthShell";

export default function ForgotPasswordPage() {
  return (
    <AuthShell
      eyebrow="Recovery"
      title="Quên mật khẩu / Forgot password"
      subtitle="Luồng khôi phục mật khẩu sẽ gửi liên kết đặt lại qua email ở bước backend tiếp theo."
    >
      <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
        Nhập email tài khoản ở phiên bản tiếp theo để nhận liên kết đặt lại mật khẩu.
      </div>
    </AuthShell>
  );
}
