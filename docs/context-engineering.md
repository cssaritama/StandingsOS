# Context engineering

The AI brief is treated as a context-engineering problem, not a prompt-writing trick.

The runtime context is assembled from explicit layers:

```text
AI-ready data
  -> semantic definitions
  -> deterministic analytics
  -> forecast outputs
  -> readiness evidence
  -> policy instructions
  -> model
```

The model does not receive unrestricted database access. It receives a bounded evidence pack with known provenance and an instruction contract that prevents it from inventing external facts or recalculating deterministic state.

## Context contract

The evidence pack includes:

- season identity;
- data-readiness assessment;
- deterministic analytics;
- top standings rows;
- forecast outputs;
- AI policy metadata.

## Why this matters

Prompt text is only one part of reliable AI behavior. Context selection, data quality, semantics, tools, permissions, model configuration, evaluation and runtime observability together define the system's behavior.
