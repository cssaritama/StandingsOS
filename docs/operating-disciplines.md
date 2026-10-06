# Operating disciplines

StandingsOS is intentionally small enough to understand end to end, but its engineering model reflects broader enterprise disciplines.

| Discipline | Repository signal |
| --- | --- |
| DevOps | CI, containers, Kubernetes, health/readiness probes, deployment runbooks |
| DataOps | data contracts, quality policy, provenance, import/export and semantic definitions |
| MLOps | versioned transparent forecast baseline and explicit model role |
| LLMOps / AgentOps | bounded evidence, readiness gate, model/provider configuration, AI policy and optional runtime |
| FinOps | cloud architecture docs require cost evidence before promoting a deployment to production-ready |
| SecOps / governance | secrets excluded from source, runtime configuration, least-privilege architecture direction |
| Spec-driven delivery | versioned feature specs, acceptance criteria and verification gates |

The goal is not to claim a full enterprise implementation of every discipline. It is to make the boundaries and extension path explicit and testable.
