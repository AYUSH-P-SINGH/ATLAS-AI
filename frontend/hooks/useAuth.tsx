"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";
import { apiClient, APIError } from "../services/api";

export interface UserProfile {
  id: string;
  email: string;
  username: string;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: UserProfile | null;
  loading: boolean;
  login: (usernameOrEmail: string, checkPassword: string) => Promise<void>;
  register: (emailStr: string, usernameStr: string, checkPassword: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const fetchProfile = async () => {
    try {
      const data = await apiClient<UserProfile>("/api/users/me");
      setUser(data);
    } catch (err) {
      // Clear user if authentication is invalid
      setUser(null);
      if (err instanceof APIError && err.status === 401) {
        localStorage.removeItem("token");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  // Redirect client if accessing dashboard without session
  useEffect(() => {
    if (!loading) {
      const isProtectedRoute = pathname.startsWith("/dashboard");
      const isAuthRoute = pathname === "/login" || pathname === "/register";
      
      if (isProtectedRoute && !user) {
        router.push("/login");
      } else if (isAuthRoute && user) {
        router.push("/dashboard");
      }
    }
  }, [user, loading, pathname, router]);

  const login = async (usernameOrEmail: string, checkPassword: string) => {
    setLoading(true);
    try {
      const res = await apiClient<{ access_token: string }>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ username_or_email: usernameOrEmail, password: checkPassword }),
      });
      
      // Store token in localStorage as local fallback
      localStorage.setItem("token", res.access_token);
      
      // Fetch user profile
      const profile = await apiClient<UserProfile>("/api/users/me");
      setUser(profile);
      router.push("/dashboard");
    } catch (err) {
      setLoading(false);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (emailStr: string, usernameStr: string, checkPassword: string) => {
    setLoading(true);
    try {
      await apiClient<UserProfile>("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({ email: emailStr, username: usernameStr, password: checkPassword }),
      });
      // Automatically log in after registration
      await login(usernameStr, checkPassword);
    } catch (err) {
      setLoading(false);
      throw err;
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await apiClient("/api/auth/logout", { method: "POST" });
    } catch (err) {
      console.error("Logout API failed:", err);
    } finally {
      localStorage.removeItem("token");
      setUser(null);
      setLoading(false);
      router.push("/login");
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser: fetchProfile }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
