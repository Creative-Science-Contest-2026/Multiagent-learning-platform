import AuthShell from "@/components/auth/AuthShell";

export default function VerifyEmailPage() {
  return (
    <AuthShell
      eyebrow="Verification"
      title="Xác minh email / Verify email"
      subtitle="Trang xác minh email sẽ hoàn tất kết nối khi backend token verification được triển khai ở slice kế tiếp."
    >
      <div className="rounded-[24px] border border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] px-5 py-5 text-sm leading-7 text-[#24324a]">
        Người dùng sẽ xác nhận email để tăng độ tin cậy và phục hồi tài khoản an toàn hơn.
      </div>
    </AuthShell>
  );
}
