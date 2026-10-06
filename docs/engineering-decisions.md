# Product and engineering decisions

## 1. Rebrand from LeagueLedger to StandingsOS

The new name describes the core product behavior more directly and gives the portfolio project a distinct identity. It should still receive a formal trademark/domain review before any commercial use.

## 2. Fixtures and results are separate entities

A schedule is not a result. Separating them allows upcoming fixtures, completed matches and corrections without overloading one record with conflicting meanings.

## 3. No stored standings table

Persisting both results and aggregate standings creates two competing sources of truth. StandingsOS derives the table from results. A future high-scale version could introduce a rebuildable read model without changing the authoritative source.

## 4. AI does not calculate the table

LLMs are useful for explanation and prioritization, not arithmetic that can be deterministic and tested. The AI layer consumes an evidence pack produced by code.

## 5. Forecasting starts with an explainable baseline

An Elo baseline is easier to inspect and backtest than a prematurely complex model. It creates a clear benchmark for future ML work.

## 6. CSV is a product feature

For the target user, spreadsheet interoperability reduces migration friction. Import/export therefore belongs to the product, not only to developer tooling.

## 7. Multicloud means portable contracts

The project demonstrates a provider-neutral application boundary. It does not claim production parity across AWS, GCP and Azure without provider-specific validation.
