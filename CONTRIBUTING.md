# Contributing

1. Create a focused branch from `main`.
2. Update `docs/product-spec.md` when observable behavior changes.
3. Add or update tests before changing domain, analytics, forecasting or AI evidence rules.
4. Run `make backend-test` and `make frontend-check` before opening a pull request.
5. Keep standings derived from result facts; do not introduce a mutable standings table.
6. Keep deterministic calculations outside the LLM.
7. Label cloud reference architecture honestly when it has not been deployed and validated.

A change is ready when backend tests pass, frontend lint/build succeeds, OpenAPI is current and the Docker stack passes `./scripts/smoke-test.sh` when infrastructure is affected.

## How this repository is run

Profile `product`. Data class Public. State Active. Owner Carlos Saritama.
README.md states what is deployed and what is not.

Before starting work, read:

1. `README.md`
2. `openapi.yaml`
3. The active specification in `specs/`
4. `docs/standards/PROJECT_STANDARDS.md` and `docs/standards/PROFILE.md`

Then follow links only as far as the change needs. Do not read `archive/`, `past_version/` and raw match data in `data/`
unless the change needs that evidence.

Rules:

- OpenAPI contract changes, schema migrations and forecasting model changes need recorded evidence: the test run and contract validation.
- `docs/standards/` is a verified copy of the Systems Studio Engineering Standard. Do not edit it; start specifications, decisions and verification records from `docs/standards/templates/`.
- Work on a focused branch and open a pull request. Keep `main` working.
