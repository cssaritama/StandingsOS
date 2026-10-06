#!/usr/bin/env sh
set -eu
BASE_URL=${BASE_URL:-http://localhost:8000}

curl --fail --silent "$BASE_URL/health"
curl --fail --silent "$BASE_URL/ready"
curl --fail --silent "$BASE_URL/api/v1/competitions" >/dev/null

echo "Smoke test passed for $BASE_URL"
