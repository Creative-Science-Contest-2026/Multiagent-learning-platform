"use client";

import {
  createContext,
  startTransition,
  useContext,
  useEffect,
  useState,
} from "react";
import type { AuthUser } from "@/lib/auth-api";
import { getCurrentUser, logout as logoutRequest } from "@/lib/auth-api";

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  refreshUser: () => Promise<AuthUser | null>;
  setUser: (user: AuthUser | null) => void;
  logout: () => Promise<void>;
}

const defaultAuthContext: AuthContextValue = {
  user: null,
  loading: false,
  refreshUser: async () => null,
  setUser: () => undefined,
  logout: async () => undefined,
};

const AuthContext = createContext<AuthContextValue>(defaultAuthContext);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUserState] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  const setUser = (nextUser: AuthUser | null) => {
    startTransition(() => {
      setUserState(nextUser);
    });
  };

  const refreshUser = async () => {
    const nextUser = await getCurrentUser();
    setUser(nextUser);
    setLoading(false);
    return nextUser;
  };

  const logout = async () => {
    await logoutRequest();
    setUser(null);
  };

  useEffect(() => {
    let cancelled = false;

    const loadUser = async () => {
      const nextUser = await getCurrentUser();
      if (cancelled) {
        return;
      }
      startTransition(() => {
        setUserState(nextUser);
        setLoading(false);
      });
    };

    void loadUser();

    return () => {
      cancelled = true;
    };
  }, []);

  const value: AuthContextValue = {
    user,
    loading,
    refreshUser,
    setUser,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  return useContext(AuthContext);
}
