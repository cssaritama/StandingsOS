# Multicloud architecture

## Goal

The goal is **deliberate portability**, not pretending that AWS, Google Cloud and Azure are interchangeable.

StandingsOS uses **Azure as the primary cloud architecture target**. AWS and Google Cloud remain documented portability references.

## Portable contract

- OCI containers;
- HTTP services;
- PostgreSQL connection string;
- Kubernetes Deployment / Service primitives;
- health and readiness probes;
- runtime configuration through environment variables and Secrets.

## Provider mapping

| Concern | Azure — primary target | AWS — reference | Google Cloud — reference |
| --- | --- | --- | --- |
| Kubernetes | AKS | EKS | GKE |
| Container registry | ACR | ECR | Artifact Registry |
| Managed PostgreSQL | Azure Database for PostgreSQL | RDS PostgreSQL / Aurora PostgreSQL | Cloud SQL for PostgreSQL |
| Secrets | Key Vault | Secrets Manager | Secret Manager |
| Observability | Azure Monitor / Container Insights | CloudWatch | Cloud Monitoring |
| AI extension | Microsoft Foundry | Bedrock / SageMaker patterns | Vertex AI patterns |

## Repository implementation

`infra/kubernetes/base` contains the provider-neutral application layer.

`infra/kubernetes/overlays/azure` is the primary cloud overlay.

`infra/kubernetes/overlays/aws` and `infra/kubernetes/overlays/gcp` demonstrate the same application boundary but remain reference configurations until validated in live cloud accounts.

`infra/kubernetes/overlays/local` includes PostgreSQL and local credentials so the architecture can be reproduced with kind.

## Why one primary cloud

Real multicloud engineering requires understanding provider differences in:

- identity;
- networking;
- managed databases;
- load balancing;
- secret management;
- monitoring;
- policy;
- cost.

Implementing one primary cloud deeply is more credible than publishing three shallow, unvalidated stacks.

## Status

| Environment | Status |
| --- | --- |
| Docker Compose | Implemented |
| kind / local Kubernetes | Implemented |
| Azure AKS | Deployment-ready architecture |
| AWS EKS | Reference architecture |
| Google GKE | Reference architecture |

See [Azure architecture](azure-architecture.md), [Cloud strategy](cloud-strategy.md) and [`infra/azure`](../infra/azure/README.md).
