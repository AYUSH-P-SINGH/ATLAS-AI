"use client";

import React, { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useAuth } from "@/hooks/useAuth";

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const [mockRepos] = useState([
    {
      id: "1",
      name: "atlas-ai",
      url: "https://github.com/AYUSH-P-SINGH/ATLAS-AI",
      branch: "main",
      status: "Ready",
      language: "TypeScript / Python",
      smells: 0,
      coverage: "92%",
    },
    {
      id: "2",
      name: "jobflow-backend",
      url: "https://github.com/AYUSH-P-SINGH/jobflow-backend",
      branch: "develop",
      status: "Analyzing",
      language: "Go / TypeScript",
      smells: 12,
      coverage: "78%",
    },
  ]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        <div className="text-center space-y-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-cyan-500 border-t-transparent mx-auto" />
          <p className="text-sm font-medium text-slate-400">Loading user session...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will be redirected by useAuth hook
  }

  return (
    <div className="relative flex min-h-screen flex-col bg-slate-950">
      {/* Background decoration */}
      <div className="absolute top-[10%] right-[10%] h-[400px] w-[400px] rounded-full bg-cyan-500/5 blur-[100px] pointer-events-none" />

      <Navbar />

      <main className="flex-grow max-w-7xl w-full mx-auto px-4 py-12 sm:px-6 lg:px-8 z-10">
        {/* Welcome Banner */}
        <div className="rounded-2xl glass-panel p-8 md:flex md:items-center md:justify-between shadow-xl mb-12">
          <div className="space-y-2">
            <h1 className="text-3xl font-extrabold text-white tracking-tight">
              Developer Console
            </h1>
            <p className="text-slate-400 text-sm">
              Manage semantic indexing, dependency graphs, and architecture audits.
            </p>
          </div>
          <button className="mt-6 md:mt-0 rounded-xl btn-primary px-6 py-3 text-sm font-bold text-white shadow-md cursor-pointer">
            + Index New Repository
          </button>
        </div>

        {/* User stats */}
        <div className="grid gap-6 md:grid-cols-3 mb-12">
          <div className="rounded-xl border border-slate-950 bg-slate-900/40 p-6 glass-panel">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Account Identity</p>
            <p className="mt-2 text-lg font-bold text-white truncate">{user.email}</p>
            <p className="mt-1 text-xs text-cyan-400">Verified User</p>
          </div>
          <div className="rounded-xl border border-slate-950 bg-slate-900/40 p-6 glass-panel">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Repositories</p>
            <p className="mt-2 text-3xl font-black text-white">{mockRepos.length}</p>
            <p className="mt-1 text-xs text-slate-500">Connected Codebases</p>
          </div>
          <div className="rounded-xl border border-slate-950 bg-slate-900/40 p-6 glass-panel">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Architecture Audits</p>
            <p className="mt-2 text-3xl font-black text-white">4</p>
            <p className="mt-1 text-xs text-green-400">100% Health Score</p>
          </div>
        </div>

        {/* Repositories Table */}
        <div className="rounded-2xl glass-panel shadow-2xl overflow-hidden">
          <div className="border-b border-border bg-slate-900/50 px-6 py-4 flex items-center justify-between">
            <h2 className="text-lg font-bold text-white tracking-wide">Connected Codebases</h2>
            <span className="rounded-full bg-cyan-950/80 border border-cyan-800/40 px-2.5 py-0.5 text-xs text-cyan-400 font-semibold">
              Live Systems
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-800/60">
              <thead className="bg-slate-950/40">
                <tr>
                  <th className="px-6 py-3.5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Name</th>
                  <th className="px-6 py-3.5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Branch</th>
                  <th className="px-6 py-3.5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Languages</th>
                  <th className="px-6 py-3.5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3.5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Smells</th>
                  <th className="px-6 py-3.5 text-right text-xs font-bold text-slate-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 bg-transparent">
                {mockRepos.map((repo) => (
                  <tr key={repo.id} className="hover:bg-slate-900/30 transition-colors">
                    <td className="whitespace-nowrap px-6 py-4">
                      <div className="font-semibold text-slate-100 text-sm">{repo.name}</div>
                      <div className="text-xs text-slate-500 truncate max-w-xs">{repo.url}</div>
                    </td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-300 font-mono">
                      {repo.branch}
                    </td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-400">
                      {repo.language}
                    </td>
                    <td className="whitespace-nowrap px-6 py-4">
                      <span
                        className={`inline-flex rounded-full px-2 py-0.5 text-xs font-bold ${
                          repo.status === "Ready"
                            ? "bg-green-950/60 border border-green-800/40 text-green-400"
                            : "bg-amber-950/60 border border-amber-800/40 text-amber-400 animate-pulse-slow"
                        }`}
                      >
                        {repo.status}
                      </span>
                    </td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-300">
                      {repo.smells === 0 ? (
                        <span className="text-green-400 font-semibold">Clean</span>
                      ) : (
                        <span className="text-amber-400 font-bold">{repo.smells} smells</span>
                      )}
                    </td>
                    <td className="whitespace-nowrap px-6 py-4 text-right text-sm">
                      <button className="text-cyan-400 hover:text-cyan-300 font-semibold cursor-pointer">
                        Open Graph
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
