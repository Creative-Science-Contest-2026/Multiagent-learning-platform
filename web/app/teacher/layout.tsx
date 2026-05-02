"use client";

import Link from "next/link";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

export default function TeacherLayout({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute
      allow={["teacher"]}
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-[#f6f1e8] px-4">
          <div className="max-w-lg rounded-[28px] border border-[rgba(10,21,48,0.08)] bg-white px-6 py-6 text-center shadow-[0_20px_60px_rgba(10,21,48,0.12)]">
            <p className="text-sm font-semibold uppercase tracking-[0.16em] text-[#7a869c]">Teacher only</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-[-0.04em] text-[#0a1530]">
              Không gian giáo viên
            </h1>
            <p className="mt-4 text-sm leading-7 text-[#50607d]">
              Chỉ tài khoản giáo viên mới được vào khu vực thiết kế học liệu, đánh giá và dashboard lớp học.
            </p>
            <Link
              href="/login"
              className="mt-6 inline-flex rounded-2xl bg-[#0a1530] px-4 py-3 text-sm font-medium text-white"
            >
              Quay lại đăng nhập
            </Link>
          </div>
        </div>
      }
    >
      {children}
    </ProtectedRoute>
  );
}
