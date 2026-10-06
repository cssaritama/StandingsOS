# Azure deployment runbook

This directory documents the **Azure deployment path** for StandingsOS.

The repository does not store live credentials or claim that an Azure environment exists until the operator validates it in a subscription.

## Target resources

- Resource Group
- Azure Container Registry
- Azure Kubernetes Service
- Azure Database for PostgreSQL Flexible Server
- Azure Key Vault
- Log Analytics / Azure Monitor

Optional:
- Microsoft Foundry resource for evidence-grounded AI briefs

## Environment variables

Set these locally before provisioning:

```bash
export AZURE_LOCATION=westeurope
export RESOURCE_GROUP=standingsos-rg
export ACR_NAME=<globally-unique-acr-name>
export AKS_NAME=standingsos-aks
export POSTGRES_SERVER=<globally-unique-postgres-name>
export POSTGRES_ADMIN=<admin-user>
```

Do not commit passwords, connection strings or subscription identifiers.

## 1. Authenticate and select subscription

```bash
az login
az account show
```

## 2. Create resource group

```bash
az group create \
  --name "$RESOURCE_GROUP" \
  --location "$AZURE_LOCATION"
```

## 3. Create container registry

```bash
az acr create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ACR_NAME" \
  --sku Basic
```

## 4. Create AKS and attach ACR

```bash
az aks create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_NAME" \
  --node-count 2 \
  --generate-ssh-keys \
  --attach-acr "$ACR_NAME"

az aks get-credentials \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_NAME"
```

## 5. Create managed PostgreSQL

Create Azure Database for PostgreSQL Flexible Server through your preferred IaC or Azure CLI workflow. Use private networking for a production environment.

StandingsOS expects only a standard SQLAlchemy URL:

```text
postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
```

## 6. Build and push images

```bash
az acr login --name "$ACR_NAME"

docker build -t "$ACR_NAME.azurecr.io/standingsos-api:2.1.0" ./backend
docker build -t "$ACR_NAME.azurecr.io/standingsos-web:2.1.0" ./frontend

docker push "$ACR_NAME.azurecr.io/standingsos-api:2.1.0"
docker push "$ACR_NAME.azurecr.io/standingsos-web:2.1.0"
```

## 7. Supply runtime secret

Create the Kubernetes secret from a secure local source for the first validation:

```bash
kubectl create namespace standingsos --dry-run=client -o yaml | kubectl apply -f -

kubectl -n standingsos create secret generic standingsos-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL"
```

For a production implementation, replace this manual step with Key Vault + workload identity / CSI integration.

## 8. Point the overlay to ACR

Update the image names at deploy time with Kustomize or your release pipeline, then deploy:

```bash
kubectl apply -k infra/kubernetes/overlays/azure
kubectl -n standingsos rollout status deployment/backend
kubectl -n standingsos rollout status deployment/frontend
```

## 9. Validate

```bash
kubectl -n standingsos get pods
kubectl -n standingsos get services
```

Run the repository smoke test against the public endpoint after DNS/TLS is configured.

## 10. Production hardening

Before calling the environment production-ready, add and validate:

- private networking;
- managed identity / workload identity;
- Key Vault integration;
- TLS and DNS;
- Azure Monitor / Container Insights;
- resource quotas and autoscaling;
- backup / restore tests;
- vulnerability scanning;
- policy and RBAC;
- cost budgets and alerts;
- deployment rollback procedure.

## Evidence rule

After a real Azure deployment is validated, update the README status table from `Deployment-ready` to `Validated deployment` and include:

- deployment date;
- region;
- sanitized architecture screenshot;
- CI/deployment evidence;
- smoke-test evidence;
- cost notes.

Do not claim live Azure deployment before that evidence exists.
