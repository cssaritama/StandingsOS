# Security

This repository contains local-development defaults only. Never commit real credentials, production connection strings, access tokens or private keys.

## Secrets

- Docker Compose reads local settings from `.env`.
- The kind overlay generates demo-only local database credentials.
- Cloud Kubernetes overlays expect the `standingsos-secrets` Secret to be supplied by the target environment.
- Production environments should integrate the cloud provider's secret manager and workload identity mechanism.

## AI endpoint

The optional AI brief sends the bounded evidence payload to the configured model endpoint. Do not enable an external model provider for sensitive competition data without reviewing its data handling and retention terms.

## Reporting

If you discover a vulnerability in a deployed copy of this project, report it privately to the operator of that deployment rather than publishing credentials or exploit details in an issue.
