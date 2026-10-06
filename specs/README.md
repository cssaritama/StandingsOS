# Specification-driven development

StandingsOS uses small versioned specifications before implementation. A spec records the problem, constraints, interfaces, acceptance criteria, non-goals and verification plan.

Flow:

```text
problem -> spec -> acceptance criteria -> implementation -> tests/evals -> deployment evidence -> feedback
```

This is intentionally compatible with human engineers and coding agents: `AGENTS.md` defines repository-wide rules while feature specs define the local contract for a change.
