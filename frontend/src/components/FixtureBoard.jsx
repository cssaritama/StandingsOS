import { useState } from "react";

function ResultForm({ fixture, onRecord }) {
  const [homeGoals, setHomeGoals] = useState(0);
  const [awayGoals, setAwayGoals] = useState(0);

  return (
    <form
      className="inline-score"
      onSubmit={(event) => {
        event.preventDefault();
        onRecord(fixture.id, Number(homeGoals), Number(awayGoals));
      }}
    >
      <input aria-label="Home goals" type="number" min="0" max="99" value={homeGoals} onChange={(e) => setHomeGoals(e.target.value)} />
      <span>–</span>
      <input aria-label="Away goals" type="number" min="0" max="99" value={awayGoals} onChange={(e) => setAwayGoals(e.target.value)} />
      <button type="submit" className="small">Record</button>
    </form>
  );
}

export default function FixtureBoard({ fixtures, onRecord, onRemove }) {
  const upcoming = fixtures.filter((fixture) => !fixture.result);
  const completed = fixtures.filter((fixture) => fixture.result).reverse();

  return (
    <div className="fixture-grid">
      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Operations</p>
            <h2>Upcoming fixtures</h2>
          </div>
          <span className="count-badge">{upcoming.length}</span>
        </div>
        <div className="fixture-list">
          {upcoming.length === 0 && <p className="empty">No scheduled fixtures.</p>}
          {upcoming.map((fixture) => (
            <article key={fixture.id} className="fixture-card">
              <div>
                <time>{new Date(fixture.scheduled_at).toLocaleDateString()}</time>
                <p>{fixture.home_team} <span>vs</span> {fixture.away_team}</p>
              </div>
              <ResultForm fixture={fixture} onRecord={onRecord} />
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Facts</p>
            <h2>Recorded results</h2>
          </div>
          <span className="count-badge">{completed.length}</span>
        </div>
        <div className="fixture-list">
          {completed.length === 0 && <p className="empty">No results recorded.</p>}
          {completed.map((fixture) => (
            <article key={fixture.id} className="result-row">
              <div>
                <p>{fixture.home_team} <strong>{fixture.result.home_goals}–{fixture.result.away_goals}</strong> {fixture.away_team}</p>
                <small>source: {fixture.result.source}</small>
              </div>
              <button className="link-button" onClick={() => onRemove(fixture.id)}>Correct</button>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
