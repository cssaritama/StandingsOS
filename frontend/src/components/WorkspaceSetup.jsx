import { useState } from "react";

export default function WorkspaceSetup({ competitionId, onCreateCompetition, onCreateSeason }) {
  const [competitionName, setCompetitionName] = useState("");
  const [country, setCountry] = useState("");
  const [seasonName, setSeasonName] = useState("");

  return (
    <section className="panel setup-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Workspace setup</p>
          <h2>Build a competition</h2>
        </div>
      </div>
      <p className="section-copy">
        Start a new competition or add a season to the selected competition.
      </p>
      <div className="admin-grid">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            if (!competitionName.trim()) return;
            onCreateCompetition({
              name: competitionName.trim(),
              sport: "football",
              country: country.trim() || null,
            });
            setCompetitionName("");
            setCountry("");
          }}
        >
          <label>New competition</label>
          <div className="stacked-fields">
            <input value={competitionName} onChange={(e) => setCompetitionName(e.target.value)} placeholder="Competition name" />
            <input value={country} onChange={(e) => setCountry(e.target.value)} placeholder="Country / region (optional)" />
            <button type="submit" disabled={!competitionName.trim()}>Create competition</button>
          </div>
        </form>

        <form
          onSubmit={(event) => {
            event.preventDefault();
            if (!competitionId || !seasonName.trim()) return;
            onCreateSeason({ name: seasonName.trim(), status: "active" });
            setSeasonName("");
          }}
        >
          <label>New season</label>
          <div className="stacked-fields">
            <input value={seasonName} onChange={(e) => setSeasonName(e.target.value)} placeholder="2026/27" />
            <button type="submit" disabled={!competitionId || !seasonName.trim()}>Create season</button>
          </div>
        </form>
      </div>
    </section>
  );
}
