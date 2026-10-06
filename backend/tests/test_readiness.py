from datetime import datetime, timezone
from types import SimpleNamespace

from app.readiness import assess_season_readiness


def _team(team_id: int, name: str):
    return SimpleNamespace(id=team_id, name=name)


def _fixture(fid, season_id, home, away, result=None):
    return SimpleNamespace(
        id=fid,
        season_id=season_id,
        home_team_id=home.id,
        away_team_id=away.id,
        home_team=home,
        away_team=away,
        scheduled_at=datetime.now(timezone.utc),
        result=result,
    )


def _result(home=1, away=0, source="manual"):
    return SimpleNamespace(
        home_goals=home,
        away_goals=away,
        source=source,
        recorded_at=datetime.now(timezone.utc),
    )


def test_readiness_requires_completed_evidence():
    season = SimpleNamespace(id=1)
    atlas, aurora = _team(1, "Atlas"), _team(2, "Aurora")
    assessment = assess_season_readiness(
        season,
        [atlas, aurora],
        [_fixture(1, 1, atlas, aurora)],
    )
    assert assessment.status == "not_ready"
    assert any("completed result" in item for item in assessment.blockers)


def test_readiness_is_ready_with_quality_and_provenance():
    season = SimpleNamespace(id=1)
    teams = [_team(i, name) for i, name in enumerate(["Atlas", "Aurora", "Harbor"], start=1)]
    fixtures = [
        _fixture(1, 1, teams[0], teams[1], _result()),
        _fixture(2, 1, teams[1], teams[2], _result(2, 2, "csv")),
        _fixture(3, 1, teams[2], teams[0], _result(0, 1, "demo")),
        _fixture(4, 1, teams[0], teams[2]),
    ]
    assessment = assess_season_readiness(season, teams, fixtures)
    assert assessment.status == "ready"
    assert assessment.score >= 85
    assert assessment.dimensions["provenance_coverage"] == 100.0
