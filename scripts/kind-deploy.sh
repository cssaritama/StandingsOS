#!/usr/bin/env sh
set -eu

CLUSTER_NAME=${CLUSTER_NAME:-standingsos}

if ! kind get clusters | grep -qx "$CLUSTER_NAME"; then
  kind create cluster --name "$CLUSTER_NAME"
fi

docker build -t standingsos-api:local ./backend
docker build --build-arg VITE_API_BASE_URL= -t standingsos-web:local ./frontend
kind load docker-image standingsos-api:local --name "$CLUSTER_NAME"
kind load docker-image standingsos-web:local --name "$CLUSTER_NAME"

kubectl apply -k infra/kubernetes/overlays/local
kubectl -n standingsos rollout status deployment/postgres --timeout=120s
kubectl -n standingsos rollout status deployment/backend --timeout=120s
kubectl -n standingsos exec deployment/backend -- /app/.venv/bin/python -c \
  "from app.db import SessionLocal; from app.seed import seed_demo; db=SessionLocal(); seed_demo(db); db.close()"
kubectl -n standingsos rollout status deployment/frontend --timeout=120s

echo "StandingsOS is ready. Run: kubectl -n standingsos port-forward service/frontend 8080:80"
