# Portfolio evidence map

This document maps claims in the public README to repository evidence.

| Claim | Evidence |
| --- | --- |
| Source-of-truth competition model | domain models, standings engine, tests |
| AI-ready data contracts | `data/contracts/`, readiness engine |
| Semantic definitions | `data/semantics/` |
| Specification-driven development | `specs/`, `AGENTS.md` |
| Grounded AI | bounded evidence pack + AI adapter + tests |
| Transparent forecasting | Elo implementation + forecast API |
| Docker delivery | Dockerfiles + `compose.yaml` |
| Kubernetes portability | `infra/kubernetes/base` + overlays |
| Azure-first architecture | Azure docs + Azure overlay + runbook |
| CI quality gates | `.github/workflows/ci.yml` |
| OpenAPI contract | `openapi.yaml` + semantic CI check |

The purpose is to make the repository auditable: a reviewer should be able to move from a claim to implementation evidence quickly.
