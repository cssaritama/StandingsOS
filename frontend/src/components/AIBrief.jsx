export default function AIBrief({ brief, loading, error, onGenerate, readiness }) {
  return (
    <section className="panel ai-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Grounded AI</p>
          <h2>Competition brief</h2>
        </div>
        <span className="model-chip">optional</span>
      </div>
      <p className="section-copy">
        The model receives a bounded evidence pack. Standings, analytics and probabilities remain deterministic code.
      </p>
      {brief ? (
        <div className="ai-output">
          <p>{brief.summary}</p>
          <small>{brief.provider} · {brief.model}</small>
        </div>
      ) : (
        <button onClick={onGenerate} disabled={loading || readiness?.status !== "ready"}>
          {loading ? "Generating…" : readiness?.status === "ready" ? "Generate evidence-grounded brief" : "AI brief blocked by readiness gate"}
        </button>
      )}
      {error && <p className="note">{error}</p>}
    </section>
  );
}
