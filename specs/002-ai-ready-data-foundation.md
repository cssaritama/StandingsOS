# Spec 002 — AI-ready data foundation

## Problem

The product can derive analytics and build an AI evidence pack, but it previously had no explicit contract proving that the underlying season data was fit for AI consumption.

## Goal

Introduce a deterministic, inspectable readiness layer between operational data and AI.

## Requirements

- versioned data contracts for fixtures and results;
- deterministic quality/readiness dimensions;
- semantic definitions for metrics exposed to AI;
- API endpoint exposing readiness evidence;
- AI brief generation blocked when readiness policy fails;
- readiness result visible in the product UI;
- no LLM involved in calculating the readiness score.

## API

`GET /api/v1/seasons/{season_id}/data-readiness`

Returns score, status, policy version, dimensions, blockers, warnings and timestamp.

## Acceptance criteria

1. A season with no completed results is `not_ready`.
2. The seeded demo season is `ready`.
3. Result provenance coverage is measured deterministically.
4. AI brief generation returns `409` when the readiness gate is not ready.
5. Readiness evidence is included in the AI evidence pack after the gate passes.
6. Unit/API tests cover the score and gate behavior.

## Non-goals

- pretending the score is a universal enterprise data-quality standard;
- automatic remediation of bad source systems;
- LLM-based data-quality scoring;
- streaming data quality in this release.

## Verification

- Python unit tests;
- API integration tests;
- OpenAPI export;
- frontend build/lint in CI;
- Docker/container build in CI.
