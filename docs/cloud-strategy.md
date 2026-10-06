# Cloud strategy

## Principle

Multicloud should describe an **architecture and operating capability**, not a list of logos.

StandingsOS follows a simple model:

1. keep application contracts portable;
2. choose one cloud as the primary implementation target;
3. use provider-native services where they create real operational value;
4. document reference mappings for the other clouds;
5. never describe a reference architecture as a deployed environment.

## Portfolio role

StandingsOS is the portfolio's **Azure-first product and competition-intelligence system**.

- **Azure:** primary cloud architecture target.
- **Google Cloud:** portability reference; other portfolio systems carry deeper GCP emphasis.
- **AWS:** portability reference and future enterprise-platform work.

## Decision framework

A cloud-specific service is justified when it improves one or more of:

- security;
- reliability;
- operability;
- governance;
- developer productivity;
- cost transparency;
- data / AI integration.

The portable application layer remains intentionally small:

```text
container image
+ HTTP contract
+ PostgreSQL contract
+ environment configuration
+ Kubernetes workload
```

Everything else can be provider-specific without coupling domain logic to the cloud.

## Multicloud is not active-active by default

This project does not propose simultaneous active-active deployment across three providers. That would add substantial networking, data-consistency, identity, observability and cost complexity without a demonstrated business requirement.

The portfolio goal is to demonstrate the ability to:

- design provider-neutral application boundaries;
- select provider-native platform services deliberately;
- reason about migration and portability;
- distinguish business continuity requirements from technology fashion.
