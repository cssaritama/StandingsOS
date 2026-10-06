const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, options);
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      if (body?.detail) detail = body.detail;
    } catch {
      // Keep the HTTP status when there is no JSON body.
    }
    throw new Error(detail);
  }
  if (response.status === 204) return null;
  return response;
}

async function json(path, options = {}) {
  const response = await request(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  return response.json();
}

export const api = {
  listCompetitions: () => json("/api/v1/competitions"),
  createCompetition: (payload) =>
    json("/api/v1/competitions", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  listSeasons: (competitionId) => json(`/api/v1/competitions/${competitionId}/seasons`),
  createSeason: (competitionId, payload) =>
    json(`/api/v1/competitions/${competitionId}/seasons`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  listTeams: (seasonId) => json(`/api/v1/seasons/${seasonId}/teams`),
  addTeam: (seasonId, name) =>
    json(`/api/v1/seasons/${seasonId}/teams`, {
      method: "POST",
      body: JSON.stringify({ name }),
    }),
  listFixtures: (seasonId) => json(`/api/v1/seasons/${seasonId}/fixtures`),
  createFixture: (seasonId, payload) =>
    json(`/api/v1/seasons/${seasonId}/fixtures`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  recordResult: (fixtureId, payload) =>
    json(`/api/v1/fixtures/${fixtureId}/result`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  removeResult: (fixtureId) =>
    request(`/api/v1/fixtures/${fixtureId}/result`, { method: "DELETE" }),
  standings: (seasonId) => json(`/api/v1/seasons/${seasonId}/standings`),
  analytics: (seasonId) => json(`/api/v1/seasons/${seasonId}/analytics`),
  forecasts: (seasonId) => json(`/api/v1/seasons/${seasonId}/forecasts`),
  dataReadiness: (seasonId) => json(`/api/v1/seasons/${seasonId}/data-readiness`),
  aiBrief: (seasonId) => json(`/api/v1/seasons/${seasonId}/ai-brief`),
  exportUrl: (seasonId) => `${BASE_URL}/api/v1/seasons/${seasonId}/export.csv`,
  importCsv: async (seasonId, file) => {
    const body = new FormData();
    body.append("file", file);
    const response = await request(`/api/v1/seasons/${seasonId}/import.csv`, {
      method: "POST",
      body,
    });
    return response.json();
  },
};
