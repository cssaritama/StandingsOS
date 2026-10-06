# Product vision

## Product thesis

Competition operators should not have to reconcile fixtures, result sheets and league tables by hand. StandingsOS turns recorded match facts into a reliable operational and intelligence layer.

## Target user

The first user is a competition administrator running a small or mid-sized league, tournament or recurring season that has outgrown spreadsheets but does not need a heavyweight federation platform.

## Jobs to be done

- schedule who should play and when;
- record what actually happened;
- publish a table that cannot drift from those results;
- move data into and out of spreadsheets cleanly;
- understand the state of the season without manually calculating it;
- communicate the current situation in plain language without giving an AI permission to invent facts.

## Product wedge

The wedge is not "another sports dashboard". It is **data integrity plus explainable competition intelligence**.

The product separates:

1. operational state — fixtures;
2. factual state — results;
3. derived state — standings and analytics;
4. probabilistic state — forecasts;
5. narrative state — optional AI explanation.

Each layer can be inspected independently.

## What this release proves

- a coherent domain model beyond CRUD;
- an end-to-end workflow a user can interact with;
- data portability and lineage awareness;
- deterministic intelligence before generative AI;
- a cloud-portable deployment boundary.

## What it does not claim

- commercial traction;
- production deployments across three cloud providers;
- calibrated betting-grade predictions;
- live match ingestion;
- enterprise identity, billing or tenancy.
