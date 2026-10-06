function pct(value) {
  return `${Math.round(value * 100)}%`;
}

export default function Forecasts({ forecasts }) {
  return (
    <section className="panel intelligence-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Predictive analytics</p>
          <h2>Upcoming match outlook</h2>
        </div>
        <span className="model-chip">Elo v1</span>
      </div>
      <p className="section-copy">
        Transparent baseline probabilities computed only from results in the selected season.
      </p>
      <div className="forecast-list">
        {forecasts.length === 0 && <p className="empty">Schedule a future fixture to see a forecast.</p>}
        {forecasts.map((item) => (
          <article key={item.fixture_id} className="forecast-card">
            <div className="forecast-teams">
              <strong>{item.home_team}</strong>
              <span>vs</span>
              <strong>{item.away_team}</strong>
            </div>
            <div className="probabilities">
              <span>H {pct(item.home_win_probability)}</span>
              <span>D {pct(item.draw_probability)}</span>
              <span>A {pct(item.away_win_probability)}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
