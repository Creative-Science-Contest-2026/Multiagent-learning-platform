"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import EmailVerificationBanner from "./EmailVerificationBanner";

export default function TeacherSurfaceGate({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname() || "/";

  useEffect(() => {
    if (loading) {
      return;
    }
    if (!user) {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
      return;
    }
    if (user.role === "student") {
      router.replace("/student");
    }
  }, [loading, pathname, router, user]);

  if (loading || !user || user.role === "student") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--background)] px-4 text-sm text-[#50607d]">
        Đang xác thực quyền truy cập...
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-[var(--background)]">
      <div className="px-4 pt-4">
        <EmailVerificationBanner />
      </div>
      <div className="min-h-0 flex-1">{children}</div>
    </div>
  );
}
