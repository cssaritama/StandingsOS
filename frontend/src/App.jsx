import { useCallback, useEffect, useState } from "react";
import { api } from "./api/client";
import AdminPanel from "./components/AdminPanel";
import AIBrief from "./components/AIBrief";
import DataPortability from "./components/DataPortability";
import DataReadiness from "./components/DataReadiness";
import FixtureBoard from "./components/FixtureBoard";
import Forecasts from "./components/Forecasts";
import MetricCards from "./components/MetricCards";
import StandingsTable from "./components/StandingsTable";
import WorkspaceSetup from "./components/WorkspaceSetup";
import "./App.css";

export default function App() {
  const [competitions, setCompetitions] = useState([]);
  const [competitionId, setCompetitionId] = useState("");
  const [seasons, setSeasons] = useState([]);
  const [seasonId, setSeasonId] = useState("");
  const [teams, setTeams] = useState([]);
  const [fixtures, setFixtures] = useState([]);
  const [standings, setStandings] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [forecasts, setForecasts] = useState([]);
  const [brief, setBrief] = useState(null);
  const [readiness, setReadiness] = useState(null);
  const [briefError, setBriefError] = useState("");
  const [briefLoading, setBriefLoading] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const loadCompetitions = useCallback(async (preferredId = "") => {
    const next = await api.listCompetitions();
    setCompetitions(next);
    if (next.length) {
      setCompetitionId(preferredId || competitionId || String(next[0].id));
    } else {
      setCompetitionId("");
      setSeasons([]);
      setSeasonId("");
      setLoading(false);
    }
  }, [competitionId]);

  const loadSeasonList = useCallback(async (id, preferredId = "") => {
    if (!id) return;
    const next = await api.listSeasons(id);
    setSeasons(next);
    setSeasonId(preferredId || (next.length ? String(next[0].id) : ""));
    if (!next.length) setLoading(false);
  }, []);

  const refreshSeason = useCallback(async (id = seasonId) => {
    if (!id) return;
    try {
      const [nextTeams, nextFixtures, nextStandings, nextAnalytics, nextForecasts, nextReadiness] = await Promise.all([
        api.listTeams(id),
        api.listFixtures(id),
        api.standings(id),
        api.analytics(id),
        api.forecasts(id),
        api.dataReadiness(id),
      ]);
      setTeams(nextTeams);
      setFixtures(nextFixtures);
      setStandings(nextStandings);
      setAnalytics(nextAnalytics);
      setForecasts(nextForecasts);
      setReadiness(nextReadiness);
      setBrief(null);
      setBriefError("");
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [seasonId]);

  // oxlint-disable-next-line react/set-state-in-effect
  useEffect(() => {
    loadCompetitions().catch((err) => {
      setError(err.message);
      setLoading(false);
    });
  }, [loadCompetitions]);

  // oxlint-disable-next-line react/set-state-in-effect
  useEffect(() => {
    loadSeasonList(competitionId).catch((err) => setError(err.message));
  }, [competitionId, loadSeasonList]);

  // oxlint-disable-next-line react/set-state-in-effect
  useEffect(() => {
    if (seasonId) refreshSeason(seasonId);
  }, [seasonId, refreshSeason]);

  async function mutate(action) {
    try {
      await action();
      await refreshSeason();
    } catch (err) {
      setError(err.message);
    }
  }

  async function createCompetition(payload) {
    try {
      const created = await api.createCompetition(payload);
      setLoading(true);
      await loadCompetitions(String(created.id));
    } catch (err) {
      setError(err.message);
    }
  }

  async function createSeason(payload) {
    try {
      const created = await api.createSeason(competitionId, payload);
      setLoading(true);
      await loadSeasonList(competitionId, String(created.id));
    } catch (err) {
      setError(err.message);
    }
  }

  async function generateBrief() {
    setBriefLoading(true);
    setBriefError("");
    try {
      setBrief(await api.aiBrief(seasonId));
    } catch (err) {
      setBriefError(err.message);
    } finally {
      setBriefLoading(false);
    }
  }

  const selectedCompetition = competitions.find((item) => String(item.id) === competitionId);
  const selectedSeason = seasons.find((item) => String(item.id) === seasonId);

  return (
    <div className="app-shell">
      <header className="hero">
        <div className="brand-row">
          <div className="brand-mark">S</div>
          <div>
            <p className="eyebrow">Competition intelligence platform</p>
            <h1>StandingsOS</h1>
          </div>
        </div>
        <p className="hero-copy">
          One source of truth for fixtures and results. AI-ready data contracts, deterministic readiness,
          derived intelligence and optional AI explanations grounded in evidence.
        </p>
        <div className="capability-row">
          <span>Product workflow</span><span>AI-ready data</span><span>Semantic context</span><span>Predictive analytics</span><span>Grounded AI</span><span>Azure-first</span>
        </div>
      </header>

      <main>
        <section className="workspace-bar">
          <label>
            Competition
            <select value={competitionId} onChange={(e) => { setLoading(true); setSeasonId(""); setCompetitionId(e.target.value); }}>
              {competitions.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
            </select>
          </label>
          <label>
            Season
            <select value={seasonId} onChange={(e) => { setLoading(true); setSeasonId(e.target.value); }}>
              {seasons.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
            </select>
          </label>
          <div className="workspace-context">
            <strong>{selectedCompetition?.name || "No competition"}</strong>
            <span>{selectedSeason ? `${selectedSeason.name} · ${selectedSeason.status}` : "Create a season below"}</span>
          </div>
        </section>

        {error && <p className="error-banner">{error}</p>}
        {loading ? <p className="loading">Loading competition intelligence…</p> : null}

        {!loading && (!competitions.length || !seasonId) && (
          <WorkspaceSetup
            competitionId={competitionId}
            onCreateCompetition={createCompetition}
            onCreateSeason={createSeason}
          />
        )}

        {seasonId && !loading && (
          <>
            <DataReadiness readiness={readiness} />
            <MetricCards analytics={analytics} />

            <section className="panel standings-panel">
              <div className="section-heading">
                <div>
                  <p className="eyebrow">Derived state</p>
                  <h2>Standings</h2>
                </div>
                <span className="truth-chip">results → table</span>
              </div>
              <StandingsTable standings={standings} />
            </section>

            <FixtureBoard
              fixtures={fixtures}
              onRecord={(fixtureId, homeGoals, awayGoals) => mutate(() => api.recordResult(fixtureId, { home_goals: homeGoals, away_goals: awayGoals, source: "manual" }))}
              onRemove={(fixtureId) => mutate(() => api.removeResult(fixtureId))}
            />

            <div className="intelligence-grid">
              <Forecasts forecasts={forecasts} />
              <AIBrief brief={brief} loading={briefLoading} error={briefError} onGenerate={generateBrief} readiness={readiness} />
            </div>

            <div className="lower-grid">
              <DataPortability
                exportUrl={api.exportUrl(seasonId)}
                onImport={async (file) => {
                  const result = await api.importCsv(seasonId, file);
                  await refreshSeason();
                  return result;
                }}
              />
              <AdminPanel
                teams={teams}
                onAddTeam={(name) => mutate(() => api.addTeam(seasonId, name))}
                onCreateFixture={(payload) => mutate(() => api.createFixture(seasonId, payload))}
              />
            </div>

            <WorkspaceSetup
              competitionId={competitionId}
              onCreateCompetition={createCompetition}
              onCreateSeason={createSeason}
            />
          </>
        )}
      </main>

      <footer>
        <span>StandingsOS v2.2</span>
        <span>Facts → derived intelligence → bounded AI</span>
      </footer>
    </div>
  );
}
