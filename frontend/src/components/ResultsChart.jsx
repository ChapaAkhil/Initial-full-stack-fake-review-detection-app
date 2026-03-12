import { Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const chartColors = {
  fake: "#ef4444",
  genuine: "#22c55e",
};

export default function ResultsChart({ fakePct, genuinePct }) {
  const data = {
    labels: ["Fake", "Genuine"],
    datasets: [
      {
        data: [fakePct, genuinePct],
        backgroundColor: [chartColors.fake, chartColors.genuine],
        borderWidth: 0,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          usePointStyle: true,
        },
      },
    },
    cutout: "65%",
  };

  return (
    <div className="chart-card">
      <h3>Review Authenticity</h3>
      <Doughnut data={data} options={options} />
    </div>
  );
}
