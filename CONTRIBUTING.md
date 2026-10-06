# Contributing

1. Create a focused branch from `main`.
2. Update `docs/product-spec.md` when observable behavior changes.
3. Add or update tests before changing domain, analytics, forecasting or AI evidence rules.
4. Run `make backend-test` and `make frontend-check` before opening a pull request.
5. Keep standings derived from result facts; do not introduce a mutable standings table.
6. Keep deterministic calculations outside the LLM.
7. Label cloud reference architecture honestly when it has not been deployed and validated.

A change is ready when backend tests pass, frontend lint/build succeeds, OpenAPI is current and the Docker stack passes `./scripts/smoke-test.sh` when infrastructure is affected.
