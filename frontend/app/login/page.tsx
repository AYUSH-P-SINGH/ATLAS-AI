"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";

export default function LoginPage() {
  const { login, loading } = useAuth();
  const [formData, setFormData] = useState({ usernameOrEmail: "", password: "" });
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrorMsg(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.usernameOrEmail || !formData.password) {
      setErrorMsg("Please fill in all credentials.");
      return;
    }

    try {
      await login(formData.usernameOrEmail, formData.password);
    } catch (err: any) {
      setErrorMsg(err.message || "Sign in failed. Check your credentials.");
    }
  };

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center bg-slate-950 px-4 py-12 sm:px-6 lg:px-8">
      {/* Background radial highlight */}
      <div className="absolute h-[500px] w-[500px] rounded-full bg-cyan-500/5 blur-[100px] pointer-events-none" />

      <div className="w-full max-w-md space-y-8 z-10">
        <div className="text-center">
          <Link href="/" className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-400 to-blue-600 font-extrabold text-white text-xl shadow-xl hover:scale-105 transition-transform duration-200">
            A
          </Link>
          <h2 className="mt-6 text-3xl font-extrabold tracking-tight text-white">
            Welcome back to Atlas AI
          </h2>
          <p className="mt-2 text-sm text-slate-400">
            Or{" "}
            <Link href="/register" className="font-semibold text-cyan-400 hover:text-cyan-300 transition-colors">
              create a new account
            </Link>
          </p>
        </div>

        <div className="rounded-2xl glass-panel p-8 shadow-2xl">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {errorMsg && (
              <div className="rounded-lg bg-red-950/50 border border-red-500/30 p-4 text-sm text-red-400 animate-pulse-slow">
                <span className="font-semibold">Error:</span> {errorMsg}
              </div>
            )}

            <div>
              <label htmlFor="usernameOrEmail" className="block text-sm font-medium text-slate-300">
                Username or Email
              </label>
              <div className="mt-1.5">
                <input
                  id="usernameOrEmail"
                  name="usernameOrEmail"
                  type="text"
                  required
                  value={formData.usernameOrEmail}
                  onChange={handleChange}
                  placeholder="enter username or email"
                  className="block w-full rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-white placeholder-slate-500 shadow-sm focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 focus:outline-none transition-all text-sm"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-300">
                Password
              </label>
              <div className="mt-1.5">
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  className="block w-full rounded-xl border border-slate-800 bg-slate-900/60 px-4 py-3 text-white placeholder-slate-500 shadow-sm focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 focus:outline-none transition-all text-sm"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="flex w-full justify-center rounded-xl btn-primary py-3.5 text-sm font-bold text-white shadow-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:opacity-50 transition-all cursor-pointer"
              >
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
