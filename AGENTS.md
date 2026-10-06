# AGENTS.md

Repository conventions for coding agents and contributors.

## Product rule

StandingsOS separates planned fixtures from factual results. Standings, analytics and forecasts are derived from results. AI may explain a bounded evidence pack but must not become the source of truth.

**Never introduce a mutable stored standings table.**

## Boundaries

- `backend/app/standings.py`: pure standings rules.
- `backend/app/analytics.py`: deterministic descriptive metrics.
- `backend/app/forecasting.py`: transparent forecast baseline.
- `backend/app/ai.py`: evidence packaging and optional LLM adapter.
- `backend/app/models.py`: persistence model.
- `backend/app/main.py`: HTTP and orchestration adapter.
- `frontend/src/api/client.js`: frontend network boundary.
- `infra/kubernetes/`: runtime portability layer.

## Development rules

1. Keep product claims aligned with implemented behavior.
2. Add tests when domain rules change.
3. Keep deterministic calculations outside the LLM.
4. Do not hardcode production credentials.
5. Keep `/health` independent from external dependencies.
6. Keep `/ready` representative of database availability.
7. Keep local infrastructure clearly distinguished from production reference architecture.
8. Do not claim cloud deployment that has not been validated.

## Specification-driven changes

For material features, create or update a file under `specs/` before implementation. The spec should define the problem, interfaces, constraints, acceptance criteria, non-goals and verification plan. Coding agents must treat the spec and tests as the contract, not infer product behavior from implementation alone.
