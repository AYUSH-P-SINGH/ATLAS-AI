export default function Footer() {
  return (
    <footer className="w-full border-t border-border bg-slate-950/60 py-8 backdrop-blur-sm">
      <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
        <p className="text-sm text-slate-500">
          &copy; {new Date().getFullYear()} Atlas AI. All rights reserved.
        </p>
        <p className="mt-2 text-xs text-slate-600">
          Engineered for Deep Code Semantics and Architectural Insights.
        </p>
      </div>
    </footer>
  );
}
