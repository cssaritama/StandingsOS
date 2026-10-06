# Data and intelligence design

## Data model

StandingsOS models data by semantic responsibility.

- **Competition**: product container such as a league or tournament.
- **Season**: time-bounded competition instance.
- **Team**: reusable participant identity.
- **Fixture**: planned operational event.
- **Result**: recorded factual outcome with a `source` field.

The `source` value is intentionally simple (`manual`, `csv`, `demo`, or another caller-provided label). It demonstrates lineage awareness without pretending to provide a full enterprise data catalog.

## Derived standings

Standings are pure derived state. They are sorted by:

1. points;
2. goal difference;
3. goals scored;
4. team name as a deterministic final tie-breaker for display.

## Descriptive analytics

The analytics endpoint computes:

- scheduled vs completed fixtures;
- completion rate;
- total and average goals;
- home/draw/away outcome rates;
- current leader;
- strongest attack;
- strongest defense.

These values are calculated from recorded results, not copied into reporting tables.

## Forecast baseline

The forecast layer is intentionally transparent. `elo-v1`:

- starts every team at the same rating;
- updates ratings only from recorded season results;
- includes a small home advantage;
- uses observed draw rate within bounded limits;
- returns probabilities that sum to approximately one.

It is a baseline for decision-support architecture, not a claim of predictive superiority. A production forecasting project should add backtesting, calibration, benchmark models and model monitoring.

## CSV boundary

CSV import/export provides a low-friction bridge to the spreadsheet workflows the product is intended to replace incrementally.
