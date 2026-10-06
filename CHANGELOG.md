# Changelog

## [2.2.1] - 2026-10-06

### Fixed

- Restored CI by stabilizing FastAPI/Pydantic/Starlette versions used to generate the committed OpenAPI contract.
- Replaced the brittle text-diff OpenAPI check with a semantic contract check.
- Updated GitHub Actions to current action generations and pinned the runner to Ubuntu 24.04.
- Fixed the React hook dependency warning in the application shell.
- Corrected the repository clone command to use the public `StandingsOS` repository name.

### Added

- Product-first `At a glance` evidence section in the README.
- Portfolio claim-to-evidence map.
- Real-screenshot / demo-GIF capture checklist.
- Azure live-validation evidence gate.

### Notes

- Azure remains `deployment-ready`, not `validated deployment`, until the live evidence gate is completed.
- Screenshots are intentionally not fabricated; visual assets must come from a real running release.


## [2.2.0] - 2026-10-06

### Added

- deterministic AI-ready data assessment and `/data-readiness` API;
- AI readiness gate before optional LLM brief generation;
- versioned data contracts, quality policy and semantic metric catalog;
- frontend data-readiness panel;
- specification-driven feature record for the AI-ready data foundation;
- context-engineering and operating-discipline documentation.

### Changed

- AI evidence packs now include data-readiness evidence;
- product positioning now distinguishes AI-ready data, deterministic intelligence and bounded AI;
- frontend and API versions updated to 2.2.0.


## [2.1.0] - 2026-10-05

### Added

- Azure-first cloud architecture and deployment runbook.
- Executive architecture brief connecting product, data, AI, governance and platform decisions.
- Cloud strategy documenting portable vs provider-native boundaries.
- Explicit deployment-status language to separate implemented, deployment-ready and reference capabilities.
- Microsoft Foundry integration path documented as an optional Azure-native AI extension.

### Changed

- Azure is now the primary cloud target for StandingsOS.
- AWS and Google Cloud overlays are documented as portability references until validated.
- Repository positioning now emphasizes multicloud architecture without overstating deployment evidence.


## [2.0.0] - 2026-10-05

### Added

- Rebranded the portfolio product as StandingsOS.
- Added competitions and seasons as first-class product entities.
- Separated scheduled fixtures from immutable result facts.
- Added season analytics and a transparent Elo forecast baseline.
- Added CSV import/export for data portability.
- Added an optional Ollama-compatible, evidence-grounded AI briefing layer.
- Added a seeded fictional demo competition for Docker Compose.
- Added a provider-neutral Kubernetes base and local/AWS/GCP/Azure overlays.
- Added dedicated product, data, AI and multicloud documentation.
- Added OpenAPI contract verification in CI.

### Changed

- Repositioned the repository from a league-table exercise to a competition intelligence product reference implementation.
- Updated frontend information architecture around product, data and intelligence workflows.

## [1.0.3] - 2026-10-05

- Stabilized the original LeagueLedger portfolio CI workflow.
