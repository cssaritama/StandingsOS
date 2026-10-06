# Roadmap

## 2.0 — current portfolio release

- competition / season domain;
- team enrollment;
- fixtures separated from results;
- derived standings;
- descriptive analytics;
- Elo forecast baseline;
- CSV portability;
- optional grounded AI brief;
- Docker, kind and cloud-portable Kubernetes overlays;
- CI quality gates.

## 2.1 — product hardening

- authentication and competition ownership;
- stronger result correction audit trail;
- fixture pagination and filters;
- browser-level tests;
- accessible empty/error/loading states review.

## 2.2 — data platform evolution

- event/export stream for analytical storage;
- data quality checks;
- historical season comparison;
- model backtesting dataset;
- forecast calibration metrics.

## 3.0 — validated AI and cloud deployment

- provider abstraction beyond local Ollama;
- prompt/model version capture;
- evaluation dataset and groundedness scoring;
- OpenTelemetry instrumentation;
- one fully deployed cloud environment with Terraform;
- cost, latency and SLO reporting.


## Azure validation milestone

Before promoting Azure from `deployment-ready` to `validated deployment`:

- provision ACR + AKS + managed PostgreSQL;
- use secure identity / secret integration;
- enable Azure Monitor / Container Insights;
- configure TLS and DNS;
- run smoke and rollback tests;
- capture sanitized deployment evidence;
- document cost and operational trade-offs.

Only after these checks should the public README claim a live Azure environment.
