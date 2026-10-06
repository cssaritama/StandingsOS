# Kubernetes deployment model

StandingsOS uses one Kubernetes base and thin environment overlays.

- `overlays/local` is runnable with kind and includes PostgreSQL.
- `overlays/aws`, `overlays/gcp`, and `overlays/azure` keep the application layer portable and expect a managed PostgreSQL connection through the `standingsos-secrets` Secret.

The cloud overlays are reference deployment configurations, not a claim that this repository is continuously deployed to all three clouds. Production cloud provisioning, IAM, DNS, TLS, private networking and managed database lifecycle belong in environment-specific infrastructure repositories.
