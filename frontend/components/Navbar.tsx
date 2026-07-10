"use client";

import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";

export default function Navbar() {
  const { user, logout, loading } = useAuth();

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border glass-panel">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2 group">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 font-bold text-white text-lg shadow-lg group-hover:scale-105 transition-transform duration-200">
                A
              </span>
              <span className="text-xl font-bold tracking-tight text-white group-hover:text-cyan-400 transition-colors">
                Atlas <span className="text-cyan-400 group-hover:text-white">AI</span>
              </span>
            </Link>
          </div>

          {/* Navigation link triggers */}
          <div className="flex items-center space-x-4">
            {!loading && (
              <>
                {user ? (
                  <>
                    <Link
                      href="/dashboard"
                      className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
                    >
                      Dashboard
                    </Link>
                    <div className="h-4 w-px bg-slate-800" />
                    <span className="text-sm text-slate-400">
                      Hi, <span className="font-semibold text-slate-200">{user.username}</span>
                    </span>
                    <button
                      onClick={logout}
                      className="rounded-lg bg-slate-900 border border-slate-800 px-3 py-1.5 text-xs font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition-all cursor-pointer"
                    >
                      Sign Out
                    </button>
                  </>
                ) : (
                  <>
                    <Link
                      href="/login"
                      className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
                    >
                      Sign In
                    </Link>
                    <Link
                      href="/register"
                      className="rounded-lg btn-primary px-4 py-2 text-sm font-semibold text-white tracking-wide cursor-pointer"
                    >
                      Get Started
                    </Link>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
