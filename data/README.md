# AI-ready data assets

This directory contains the machine-readable contracts, quality rules and semantic definitions that describe the evidence StandingsOS exposes to analytics and AI.

The files are intentionally separate from runtime database migrations. They document the **meaning and fitness of data for downstream use**, not only how columns are stored.

- `contracts/` — expected data-product schemas and ownership intent.
- `quality/` — deterministic validation policy.
- `semantics/` — metric definitions and business vocabulary.

The runtime `/api/v1/seasons/{season_id}/data-readiness` endpoint applies the corresponding product-level readiness policy before AI brief generation.
