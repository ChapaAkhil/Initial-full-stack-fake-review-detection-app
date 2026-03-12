import { useState } from "react";
import Header from "../components/Header.jsx";
import Overview from "../components/Overview.jsx";
import URLAnalyzer from "../components/URLAnalyzer.jsx";
import ManualReviewInput from "../components/ManualReviewInput.jsx";
import Results from "../components/Results.jsx";
import { analyzeUrl, analyzeReviews } from "../api.js";

export default function Dashboard() {
  const [results, setResults] = useState(null);
  const [loadingUrl, setLoadingUrl] = useState(false);
  const [loadingManual, setLoadingManual] = useState(false);
  const [globalError, setGlobalError] = useState("");

  const handleAnalyzeUrl = async (url) => {
    setLoadingUrl(true);
    setGlobalError("");
    try {
      const data = await analyzeUrl(url);
      setResults(data);
    } catch (error) {
      const message = error?.response?.data?.detail || "Failed to analyze the product URL.";
      setGlobalError(message);
      throw error;
    } finally {
      setLoadingUrl(false);
    }
  };

  const handleAnalyzeManual = async (reviews) => {
    setLoadingManual(true);
    setGlobalError("");
    try {
      const data = await analyzeReviews(reviews);
      setResults(data);
    } catch (error) {
      const message = error?.response?.data?.detail || "Failed to analyze manual reviews.";
      setGlobalError(message);
      throw error;
    } finally {
      setLoadingManual(false);
    }
  };

  return (
    <div className="min-h-screen bg-night-900 bg-grid">
      <main className="mx-auto flex w-full max-w-6xl flex-col px-6 pb-16 pt-12">
        <Header />
        <Overview />
        <URLAnalyzer onAnalyze={handleAnalyzeUrl} isLoading={loadingUrl} />
        <ManualReviewInput onRun={handleAnalyzeManual} isLoading={loadingManual} />
        {globalError && (
          <div className="mt-6 rounded-xl border border-red-400/30 bg-red-500/10 p-4 text-sm text-red-200">
            {globalError}
          </div>
        )}
        <Results results={results} />

        <footer className="mt-12 border-t border-white/10 pt-6 text-xs text-white/50">
          Final Year Project - Fake Product Review Detection using Machine Learning | Developer | 2026 | University
        </footer>
      </main>
    </div>
  );
}
