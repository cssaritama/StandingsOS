# Demo guide

## Five-minute product demo

1. Run `docker compose up --build -d --wait`.
2. Open `http://localhost:8080`.
3. Show the seeded Global City League season.
4. Point out that completed results generate the standings and metrics.
5. Record a score for one upcoming fixture and show the table update immediately.
6. Use **Correct** to remove the result and show the derived state return.
7. Export the season CSV.
8. Show the Elo forecast cards and explain that they use only season results.
9. If Ollama is available, enable AI and generate a brief; otherwise show that the product remains fully functional with AI disabled.
10. Open `/docs` and show the versioned API contract.

## Screenshots worth adding to the repository

After running the product, capture:

- full desktop dashboard;
- standings + metrics;
- forecasts + AI panel;
- GitHub Actions green workflow;
- optional kind pods ready.

A real screenshot is preferable to a rendered mockup because it proves the interface actually runs.
