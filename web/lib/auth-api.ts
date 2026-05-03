import { apiUrl } from "@/lib/api";

export type PublicRole = "teacher" | "student";
export type AppRole = PublicRole | "admin";

export interface AuthUser {
  id: string;
  email: string;
  display_name: string;
  role: AppRole;
  email_verified_at?: string | null;
}

interface AuthResponse {
  user: AuthUser;
}

interface GenericAuthActionResponse {
  ok: boolean;
  debug_token?: string;
  debug_url?: string;
}

export interface AdminUserRecord {
  id: string;
  email: string;
  display_name: string;
  role: AppRole;
  status: string;
}

interface AdminUsersResponse {
  users: AdminUserRecord[];
}

async function expectJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Auth request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function appHomeForRole(role: AppRole): string {
  return `/${role}`;
}

export function postAuthRedirect(role: AppRole, nextPath?: string | null): string {
  const candidate = (nextPath ?? "").trim();
  if (!candidate.startsWith("/") || candidate.startsWith("//")) {
    return appHomeForRole(role);
  }
  if (role === "student" && !candidate.startsWith("/student")) {
    return appHomeForRole(role);
  }
  return candidate;
}

export function googleLoginUrl(role: PublicRole = "student", nextPath?: string | null): string {
  const query = new URLSearchParams({ role });
  const normalizedNext = (nextPath ?? "").trim();
  if (normalizedNext.startsWith("/") && !normalizedNext.startsWith("//")) {
    query.set("next", normalizedNext);
  }
  return apiUrl(`/api/v1/auth/google/start?${query.toString()}`);
}

export async function signup(payload: {
  display_name: string;
  email: string;
  password: string;
  role: PublicRole;
}): Promise<AuthResponse> {
  const response = await fetch(apiUrl("/api/v1/auth/signup"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  return expectJson<AuthResponse>(response);
}

export async function login(payload: {
  email: string;
  password: string;
}): Promise<AuthResponse> {
  const response = await fetch(apiUrl("/api/v1/auth/login"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  return expectJson<AuthResponse>(response);
}

export async function logout(): Promise<void> {
  const response = await fetch(apiUrl("/api/v1/auth/logout"), {
    method: "POST",
    credentials: "include",
  });
  await expectJson<{ ok: boolean }>(response);
}

export async function requestPasswordReset(email: string): Promise<GenericAuthActionResponse> {
  const response = await fetch(apiUrl("/api/v1/auth/forgot-password"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email.trim() }),
  });
  return expectJson<GenericAuthActionResponse>(response);
}

export async function resetPassword(payload: {
  token: string;
  password: string;
}): Promise<GenericAuthActionResponse> {
  const response = await fetch(apiUrl("/api/v1/auth/reset-password"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<GenericAuthActionResponse>(response);
}

export async function sendVerificationEmail(): Promise<GenericAuthActionResponse> {
  const response = await fetch(apiUrl("/api/v1/auth/send-verification"), {
    method: "POST",
    credentials: "include",
  });
  return expectJson<GenericAuthActionResponse>(response);
}

export async function verifyEmailToken(token: string): Promise<GenericAuthActionResponse> {
  const response = await fetch(apiUrl("/api/v1/auth/verify-email"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token }),
  });
  return expectJson<GenericAuthActionResponse>(response);
}

export async function getCurrentUser(): Promise<AuthUser | null> {
  const response = await fetch(apiUrl("/api/v1/auth/me"), {
    credentials: "include",
    cache: "no-store",
  });
  if (response.status === 401) {
    return null;
  }
  const payload = await expectJson<AuthResponse>(response);
  return payload.user;
}

export async function listAdminUsers(): Promise<AdminUsersResponse> {
  const response = await fetch(apiUrl("/api/v1/admin/users"), {
    credentials: "include",
    cache: "no-store",
  });
  return expectJson<AdminUsersResponse>(response);
}

export async function createAdminUser(payload: {
  display_name: string;
  email: string;
  password: string;
  role: AppRole;
}): Promise<{ user: AdminUserRecord }> {
  const response = await fetch(apiUrl("/api/v1/admin/users"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  });
  return expectJson<{ user: AdminUserRecord }>(response);
}
