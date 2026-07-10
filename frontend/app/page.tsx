import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function Home() {
  const features = [
    {
      title: "Repository Analyzer",
      description: "Index large codebases (10k+ files), auto-detect language structures, and parse repo file trees.",
      icon: "📦",
    },
    {
      title: "Dependency Graph Builder",
      description: "Map visual flows from Frontends to APIs, services, handlers, models, and databases.",
      icon: "🌐",
    },
    {
      title: "GraphRAG Architecture Chat",
      description: "Ask deep structural questions and retrieve exact context across dependencies with file citations.",
      icon: "💬",
    },
    {
      title: "Diagram Generator",
      description: "Auto-generate system architecture, database ERD schemas, sequence diagrams, and class maps.",
      icon: "📊",
    },
    {
      title: "SOLID & Smell Auditor",
      description: "Pinpoint God classes, long routines, circular links, high coupling, and SOLID code smells.",
      icon: "🔍",
    },
    {
      title: "Impact & Performance Analyst",
      description: "Map blast radius: see files, APIs, and tests affected before deleting services or changing schemas.",
      icon: "⚡",
    },
  ];

  return (
    <div className="relative flex min-h-screen flex-col overflow-hidden bg-slate-950">
      {/* Dynamic Background Blobs */}
      <div className="absolute top-[-20%] left-[-10%] h-[600px] w-[600px] rounded-full bg-cyan-500/10 blur-[120px] animate-blob-1 pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] h-[600px] w-[600px] rounded-full bg-blue-600/10 blur-[150px] animate-blob-2 pointer-events-none" />

      <Navbar />

      {/* Main Hero Section */}
      <main className="flex-grow flex flex-col justify-center">
        <section className="mx-auto max-w-7xl px-4 py-20 text-center sm:px-6 lg:px-8 lg:py-28 relative">
          <div className="mx-auto max-w-3xl">
            {/* Tagline pill */}
            <div className="inline-flex items-center rounded-full border border-cyan-500/30 bg-cyan-950/40 px-3 py-1 text-xs font-semibold text-cyan-400 backdrop-blur-sm mb-6">
              ✨ Phase 1: Foundation & Auth Ready
            </div>
            
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-6xl">
              Understand and Improve <br />
              <span className="text-gradient">Software Architecture</span>
            </h1>
            
            <p className="mx-auto mt-6 max-w-xl text-lg text-slate-400 leading-relaxed">
              GitHub Copilot helps write code. <br />
              <span className="font-semibold text-slate-200">Atlas AI</span> maps, analyzes, and audit-checks your codebase architecture semantically.
            </p>
            
            <div className="mt-10 flex justify-center gap-4">
              <Link
                href="/register"
                className="rounded-xl btn-primary px-8 py-3.5 text-base font-semibold text-white tracking-wide shadow-xl cursor-pointer"
              >
                Start Analysing
              </Link>
              <Link
                href="/login"
                className="rounded-xl border border-slate-800 bg-slate-900/60 px-8 py-3.5 text-base font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition-all backdrop-blur-sm cursor-pointer"
              >
                Sign In
              </Link>
            </div>
          </div>
        </section>

        {/* Feature Grid Section */}
        <section className="border-t border-slate-900 bg-slate-950/40 py-24 backdrop-blur-sm">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                Built-in Intelligence Modules
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-base text-slate-400">
                A multi-agent semantic platform designed to resolve complex dependency structures.
              </p>
            </div>

            <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {features.map((feature, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl glass-card p-8 flex flex-col justify-between"
                >
                  <div>
                    <div className="text-4xl mb-6">{feature.icon}</div>
                    <h3 className="text-xl font-bold text-white tracking-wide">
                      {feature.title}
                    </h3>
                    <p className="mt-4 text-sm text-slate-400 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                  <div className="mt-6 flex items-center text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition-colors pointer-events-none">
                    Phase 2 Core Module &rarr;
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
