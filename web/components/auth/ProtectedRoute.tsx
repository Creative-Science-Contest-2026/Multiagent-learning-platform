"use client";

import { useAuth } from "@/context/AuthContext";
import type { AppRole, AuthUser } from "@/lib/auth-api";

export default function ProtectedRoute({
  allow,
  user,
  children,
  fallback = null,
}: {
  allow: AppRole[];
  user?: AuthUser | null;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}) {
  const auth = useAuth();
  const resolvedUser = user === undefined ? auth.user : user;
  const loading = user === undefined ? auth.loading : false;

  if (loading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center text-sm text-[#50607d]">
        Đang tải phiên đăng nhập...
      </div>
    );
  }

  if (!resolvedUser || !allow.includes(resolvedUser.role)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}
