.PHONY: test backend-test frontend-check openapi build up down smoke kind

test: backend-test frontend-check

backend-test:
	cd backend && uv sync && uv run ruff check app tests && uv run pytest -q

frontend-check:
	cd frontend && npm ci && npm run lint && npm run build

openapi:
	cd backend && uv run python ../scripts/export_openapi.py

build:
	docker compose build

up:
	docker compose up --build -d --wait

down:
	docker compose down

smoke:
	./scripts/smoke-test.sh

kind:
	./scripts/kind-deploy.sh
