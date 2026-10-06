import { useState } from "react";

export default function AdminPanel({ teams, onAddTeam, onCreateFixture }) {
  const [teamName, setTeamName] = useState("");
  const [home, setHome] = useState("");
  const [away, setAway] = useState("");
  const [scheduledAt, setScheduledAt] = useState("");

  return (
    <section className="panel admin-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Product workflow</p>
          <h2>Manage the season</h2>
        </div>
      </div>
      <div className="admin-grid">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            if (!teamName.trim()) return;
            onAddTeam(teamName.trim());
            setTeamName("");
          }}
        >
          <label>Enroll team</label>
          <div className="field-row">
            <input value={teamName} onChange={(e) => setTeamName(e.target.value)} placeholder="Team name" maxLength="80" />
            <button type="submit">Add</button>
          </div>
        </form>

        <form
          onSubmit={(event) => {
            event.preventDefault();
            if (!home || !away || home === away || !scheduledAt) return;
            onCreateFixture({
              home_team_id: Number(home),
              away_team_id: Number(away),
              scheduled_at: new Date(scheduledAt).toISOString(),
            });
            setHome("");
            setAway("");
            setScheduledAt("");
          }}
        >
          <label>Schedule fixture</label>
          <div className="stacked-fields">
            <select value={home} onChange={(e) => setHome(e.target.value)}>
              <option value="">Home team</option>
              {teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}
            </select>
            <select value={away} onChange={(e) => setAway(e.target.value)}>
              <option value="">Away team</option>
              {teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}
            </select>
            <input type="datetime-local" value={scheduledAt} onChange={(e) => setScheduledAt(e.target.value)} />
            <button type="submit" disabled={!home || !away || home === away || !scheduledAt}>Schedule</button>
          </div>
        </form>
      </div>
    </section>
  );
}
