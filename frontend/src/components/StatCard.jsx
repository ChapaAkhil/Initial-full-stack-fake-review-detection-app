export default function StatCard({ label, value, tone }) {
  return (
    <div className={`stat-card ${tone}`}>
      <p className="stat-label">{label}</p>
      <p className="stat-value">{value}</p>
    </div>
  );
}
