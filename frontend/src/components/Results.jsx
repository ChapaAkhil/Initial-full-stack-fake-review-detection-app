import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Results({ results }) {
  if (!results) {
    return null;
  }

  const data = {
    labels: ["Fake", "Genuine"],
    datasets: [
      {
        data: [results.fake_reviews_percentage, results.genuine_reviews_percentage],
        backgroundColor: ["#f97316", "#22c55e"],
        borderWidth: 0,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          color: "#e2e8f0",
          usePointStyle: true,
        },
      },
    },
  };

  return (
    <section className="mt-10">
      <div className="glass-card p-6">
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="section-subtitle">Results</p>
            <h3 className="section-title mt-2">Review Authenticity Overview</h3>
          </div>
          <span className="text-xs text-white/60">Total Reviews: {results.total_reviews}</span>
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="glass-card p-4">
              <p className="text-xs text-white/60">Fake Reviews Percentage</p>
              <p className="mt-2 text-2xl font-semibold text-white">
                {results.fake_reviews_percentage}%
              </p>
            </div>
            <div className="glass-card p-4">
              <p className="text-xs text-white/60">Genuine Reviews Percentage</p>
              <p className="mt-2 text-2xl font-semibold text-white">
                {results.genuine_reviews_percentage}%
              </p>
            </div>
            <div className="glass-card p-4">
              <p className="text-xs text-white/60">Total Reviews Analyzed</p>
              <p className="mt-2 text-2xl font-semibold text-white">
                {results.total_reviews}
              </p>
            </div>
          </div>
          <div className="glass-card p-4">
            <Pie data={data} options={options} />
          </div>
        </div>
      </div>
    </section>
  );
}
