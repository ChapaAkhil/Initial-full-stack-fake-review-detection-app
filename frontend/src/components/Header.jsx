export default function Header() {
  return (
    <header className="flex flex-col gap-6 border-b border-white/10 pb-10 md:flex-row md:items-center md:justify-between">
      <div>
        <p className="section-subtitle">Final Year Project</p>
        <h1 className="mt-3 text-3xl font-semibold text-white md:text-4xl">
          Fake Product Review Detection System
        </h1>
        <p className="mt-2 max-w-2xl text-sm text-white/70 md:text-base">
          Machine Learning Based Detection of Genuine and Fake Reviews
        </p>
      </div>
      <nav className="flex flex-wrap gap-3 text-sm text-white/70">
        <span className="rounded-full border border-white/10 px-4 py-2">Overview</span>
        <span className="rounded-full border border-white/10 px-4 py-2">Analyze URL</span>
        <span className="rounded-full border border-white/10 px-4 py-2">Manual Reviews</span>
        <span className="rounded-full border border-white/10 px-4 py-2">Results</span>
      </nav>
    </header>
  );
}
