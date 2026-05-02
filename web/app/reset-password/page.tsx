import AuthShell from "@/components/auth/AuthShell";

export default function ResetPasswordPage() {
  return (
    <AuthShell
      eyebrow="Recovery"
      title="Đặt lại mật khẩu / Reset password"
      subtitle="Trang này sẽ hoàn tất đặt lại mật khẩu sau khi email recovery được nối đủ ở bước backend kế tiếp."
    >
      <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
        Liên kết đặt lại mật khẩu sẽ mở trang này cùng token bảo mật để xác nhận mật khẩu mới.
      </div>
    </AuthShell>
  );
}
