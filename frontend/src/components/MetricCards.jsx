export default function MetricCards({ analytics }) {
  const items = [
    ["Leader", analytics?.leader || "—"],
    ["Completed", analytics ? `${analytics.fixtures_completed}/${analytics.fixtures_total}` : "—"],
    ["Goals", analytics?.goals_total ?? "—"],
    ["Avg goals", analytics?.average_goals_per_match ?? "—"],
  ];

  return (
    <div className="metrics">
      {items.map(([label, value]) => (
        <article key={label} className="metric-card">
          <span>{label}</span>
          <strong>{value}</strong>
        </article>
      ))}
    </div>
  );
}
