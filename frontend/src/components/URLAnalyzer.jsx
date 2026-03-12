import { useState } from "react";

export default function URLAnalyzer({ onAnalyze, isLoading }) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!url.trim()) {
      setError("Please paste a valid product URL.");
      return;
    }
    setError("");
    await onAnalyze(url.trim()).catch((err) => {
      const detail = err?.response?.data?.detail;
      setError(detail || err?.message || "Failed to analyze URL.");
    });
  };

  return (
    <section className="mt-10">
      <div className="glass-card p-6">
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="section-subtitle">Product URL Analysis</p>
            <h3 className="section-title mt-2">Analyze Product Reviews</h3>
          </div>
          <span className="text-xs text-white/60">
            Future scraping support for multiple marketplaces
          </span>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-[1fr_auto]">
          <input
            className="input-field"
            placeholder="Paste Product URL"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
          />
          <button className="primary-button" onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? "Analyzing..." : "Analyze Reviews"}
          </button>
        </div>
        {error && <p className="mt-3 text-sm text-red-300">{error}</p>}
      </div>
    </section>
  );
}
