export default function DataReadiness({ readiness }) {
  if (!readiness) return null;
  const label = readiness.status.replace("_", " ");
  const dimensions = Object.entries(readiness.dimensions ?? {});

  return (
    <section className="panel readiness-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">AI-ready data foundation</p>
          <h2>Data readiness</h2>
        </div>
        <span className={`readiness-chip ${readiness.status}`}>{label} · {readiness.score}%</span>
      </div>
      <p className="section-copy">
        Deterministic readiness gate for downstream AI. No LLM is used to calculate this score.
      </p>
      <div className="readiness-grid">
        {dimensions.map(([name, value]) => (
          <div className="readiness-metric" key={name}>
            <span>{name.replaceAll("_", " ")}</span>
            <strong>{value}%</strong>
          </div>
        ))}
      </div>
      {readiness.blockers?.length > 0 && (
        <div className="readiness-notes danger-note">
          <strong>AI gate blockers</strong>
          {readiness.blockers.map((item) => <span key={item}>{item}</span>)}
        </div>
      )}
      {readiness.warnings?.length > 0 && (
        <div className="readiness-notes">
          <strong>Readiness notes</strong>
          {readiness.warnings.map((item) => <span key={item}>{item}</span>)}
        </div>
      )}
      <small>Policy: {readiness.policy_version}</small>
    </section>
  );
}
