# Azure validation evidence

StandingsOS is Azure-first at the architecture level. The repository must not call the environment "deployed" until a real subscription validation is complete.

## Validation gate

A deployment may be described as **validated on Azure** only after all of the following have evidence:

- application images pushed to Azure Container Registry;
- workloads running successfully on Azure Kubernetes Service;
- application connected to Azure Database for PostgreSQL;
- secrets handled outside source control;
- health and readiness probes passing;
- public or private endpoint tested according to the intended architecture;
- Azure Monitor / Container Insights receiving runtime telemetry;
- rollback procedure tested;
- sanitized evidence captured;
- approximate runtime cost documented.

## Evidence record

Record:

```text
Date:
Azure region:
AKS version:
Application version:
Database service:
Deployment workflow:
Smoke-test result:
Rollback test:
Monitoring evidence:
Approximate monthly cost:
Known limitations:
```

## Status vocabulary

- `Implemented` — code exists and is tested in repository-controlled environments.
- `Deployment-ready` — architecture/runbook exists but has not completed the live gate above.
- `Validated deployment` — the live gate above has passed.
- `Reference architecture` — design mapping only.

This language protects the credibility of the portfolio.
