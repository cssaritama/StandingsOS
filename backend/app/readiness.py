from dataclasses import dataclass
from datetime import datetime, timezone

from app.models import Fixture, Season, Team

POLICY_VERSION = "ai-readiness-v1"
READY_THRESHOLD = 85.0
CONDITIONAL_THRESHOLD = 70.0


@dataclass(frozen=True)
class ReadinessAssessment:
    score: float
    status: str
    dimensions: dict[str, float]
    blockers: list[str]
    warnings: list[str]
    checked_at: datetime
    policy_version: str = POLICY_VERSION


def _percentage(valid: int, total: int, *, empty_score: float = 100.0) -> float:
    if total == 0:
        return empty_score
    return round(valid / total * 100, 1)


def assess_season_readiness(
    season: Season,
    teams: list[Team],
    fixtures: list[Fixture],
) -> ReadinessAssessment:
    """Evaluate whether a season is safe and useful enough for AI consumption.

    The score is intentionally deterministic. It is not produced by an LLM and
    it does not claim to measure every dimension of enterprise data quality.
    It is a transparent readiness gate for this product's evidence workflow.
    """

    enrolled_ids = {team.id for team in teams}
    completed = [fixture for fixture in fixtures if fixture.result is not None]

    schema_checks = []
    for fixture in fixtures:
        schema_checks.extend(
            [
                fixture.season_id == season.id,
                bool(fixture.scheduled_at),
                fixture.home_team_id != fixture.away_team_id,
            ]
        )
        if fixture.result is not None:
            schema_checks.extend(
                [
                    fixture.result.home_goals >= 0,
                    fixture.result.away_goals >= 0,
                    bool((fixture.result.source or "").strip()),
                    bool(fixture.result.recorded_at),
                ]
            )
    schema_compliance = _percentage(sum(schema_checks), len(schema_checks))

    integrity_checks = []
    for fixture in fixtures:
        integrity_checks.extend(
            [
                fixture.home_team_id in enrolled_ids,
                fixture.away_team_id in enrolled_ids,
                fixture.home_team_id != fixture.away_team_id,
            ]
        )
    referential_integrity = _percentage(sum(integrity_checks), len(integrity_checks))

    completeness_checks = [bool(team.name.strip()) for team in teams]
    for fixture in fixtures:
        completeness_checks.extend(
            [
                bool(fixture.home_team and fixture.home_team.name.strip()),
                bool(fixture.away_team and fixture.away_team.name.strip()),
                bool(fixture.scheduled_at),
            ]
        )
    completeness = _percentage(sum(completeness_checks), len(completeness_checks), empty_score=0.0)

    provenance_coverage = _percentage(
        sum(bool((fixture.result.source or "").strip()) for fixture in completed),
        len(completed),
        empty_score=0.0,
    )

    analytical_coverage = _percentage(len(completed), len(fixtures), empty_score=0.0)

    # The semantic catalog is versioned in data/semantics. The application only
    # exposes metrics that have definitions in that catalog.
    semantic_coverage = 100.0

    dimensions = {
        "schema_compliance": schema_compliance,
        "referential_integrity": referential_integrity,
        "completeness": completeness,
        "provenance_coverage": provenance_coverage,
        "analytical_coverage": analytical_coverage,
        "semantic_coverage": semantic_coverage,
    }
    weights = {
        "schema_compliance": 0.20,
        "referential_integrity": 0.20,
        "completeness": 0.20,
        "provenance_coverage": 0.15,
        "analytical_coverage": 0.15,
        "semantic_coverage": 0.10,
    }
    score = round(sum(dimensions[name] * weight for name, weight in weights.items()), 1)

    blockers: list[str] = []
    warnings: list[str] = []
    if len(teams) < 2:
        blockers.append("At least two enrolled teams are required.")
    if not fixtures:
        blockers.append("At least one fixture is required.")
    if not completed:
        blockers.append("At least one completed result is required before AI can summarize the season.")
    if referential_integrity < 100:
        blockers.append("Fixture/team referential integrity must be 100%.")
    if schema_compliance < 100:
        blockers.append("Persisted competition facts do not fully satisfy schema rules.")
    if provenance_coverage < 90 and completed:
        blockers.append("Result provenance coverage must be at least 90%.")
    if analytical_coverage < 60 and fixtures:
        warnings.append("Less than 60% of fixtures are completed; forecasts and summaries have limited evidence.")
    if 0 < len(completed) < 3:
        warnings.append("Fewer than three completed results are available; treat derived intelligence as early-stage evidence.")

    if not blockers and score >= READY_THRESHOLD:
        status = "ready"
    elif not blockers and score >= CONDITIONAL_THRESHOLD:
        status = "conditional"
    else:
        status = "not_ready"

    return ReadinessAssessment(
        score=score,
        status=status,
        dimensions=dimensions,
        blockers=blockers,
        warnings=warnings,
        checked_at=datetime.now(timezone.utc),
    )
