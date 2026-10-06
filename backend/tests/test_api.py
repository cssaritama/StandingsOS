"""HTTP tests against an isolated in-memory SQLite database."""

import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["AUTO_CREATE_SCHEMA"] = "false"
os.environ["SEED_DEMO_DATA"] = "false"
os.environ["AI_PROVIDER"] = "disabled"

from app.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_demo_context():
    competition = client.post(
        "/api/v1/competitions",
        json={"name": "Test League", "sport": "football", "country": "Global"},
    ).json()
    season = client.post(
        f"/api/v1/competitions/{competition['id']}/seasons",
        json={"name": "2026/27"},
    ).json()
    atlas = client.post(
        f"/api/v1/seasons/{season['id']}/teams", json={"name": "Atlas"}
    ).json()
    aurora = client.post(
        f"/api/v1/seasons/{season['id']}/teams", json={"name": "Aurora"}
    ).json()
    harbor = client.post(
        f"/api/v1/seasons/{season['id']}/teams", json={"name": "Harbor"}
    ).json()
    return competition, season, atlas, aurora, harbor


def test_health_and_readiness():
    assert client.get("/health").status_code == 200
    assert client.get("/ready").json() == {"status": "ready"}


def test_end_to_end_competition_flow():
    _, season, atlas, aurora, harbor = create_demo_context()

    played = client.post(
        f"/api/v1/seasons/{season['id']}/fixtures",
        json={
            "home_team_id": atlas["id"],
            "away_team_id": aurora["id"],
            "scheduled_at": "2026-10-01T18:00:00+00:00",
        },
    ).json()
    future = client.post(
        f"/api/v1/seasons/{season['id']}/fixtures",
        json={
            "home_team_id": harbor["id"],
            "away_team_id": atlas["id"],
            "scheduled_at": "2026-10-10T18:00:00+00:00",
        },
    ).json()

    recorded = client.post(
        f"/api/v1/fixtures/{played['id']}/result",
        json={"home_goals": 2, "away_goals": 1, "source": "manual"},
    )
    assert recorded.status_code == 201

    readiness = client.get(f"/api/v1/seasons/{season['id']}/data-readiness").json()
    assert readiness["policy_version"] == "ai-readiness-v1"
    assert "schema_compliance" in readiness["dimensions"]

    standings = client.get(f"/api/v1/seasons/{season['id']}/standings").json()
    assert standings[0]["team"] == "Atlas"
    assert standings[0]["points"] == 3

    analytics = client.get(f"/api/v1/seasons/{season['id']}/analytics").json()
    assert analytics["fixtures_total"] == 2
    assert analytics["fixtures_completed"] == 1
    assert analytics["leader"] == "Atlas"

    forecasts = client.get(f"/api/v1/seasons/{season['id']}/forecasts").json()
    assert forecasts[0]["fixture_id"] == future["id"]
    assert forecasts[0]["model"] == "elo-v1"

    duplicate = client.post(
        f"/api/v1/fixtures/{played['id']}/result",
        json={"home_goals": 9, "away_goals": 9},
    )
    assert duplicate.status_code == 409

    assert client.delete(f"/api/v1/fixtures/{played['id']}/result").status_code == 204
    standings_after_delete = client.get(
        f"/api/v1/seasons/{season['id']}/standings"
    ).json()
    assert standings_after_delete[0]["played"] == 0


def test_csv_import_and_export():
    competition = client.post(
        "/api/v1/competitions",
        json={"name": "CSV League", "sport": "football"},
    ).json()
    season = client.post(
        f"/api/v1/competitions/{competition['id']}/seasons",
        json={"name": "2026"},
    ).json()

    csv_body = (
        "scheduled_at,home_team,away_team,home_goals,away_goals,result_source\n"
        "2026-10-01T18:00:00+00:00,North,South,1,0,import\n"
        "2026-10-08T18:00:00+00:00,East,West,,,\n"
    )
    response = client.post(
        f"/api/v1/seasons/{season['id']}/import.csv",
        files={"file": ("fixtures.csv", csv_body, "text/csv")},
    )
    assert response.status_code == 200
    assert response.json() == {
        "rows_processed": 2,
        "teams_created": 4,
        "fixtures_created": 2,
        "results_recorded": 1,
    }

    exported = client.get(f"/api/v1/seasons/{season['id']}/export.csv")
    assert exported.status_code == 200
    assert "North,South,1,0,import" in exported.text


def test_ai_brief_requires_ready_data_before_provider():
    _, season, *_ = create_demo_context()
    response = client.get(f"/api/v1/seasons/{season['id']}/ai-brief")
    assert response.status_code == 409
    assert "AI readiness gate blocked" in response.json()["detail"]


def test_ai_brief_is_explicitly_optional_after_readiness_passes():
    competition = client.post(
        "/api/v1/competitions",
        json={"name": "AI Ready League", "sport": "football"},
    ).json()
    season = client.post(
        f"/api/v1/competitions/{competition['id']}/seasons",
        json={"name": "2026"},
    ).json()
    csv_body = (
        "scheduled_at,home_team,away_team,home_goals,away_goals,result_source\n"
        "2026-10-01T18:00:00+00:00,North,South,1,0,import\n"
        "2026-10-02T18:00:00+00:00,East,West,2,1,import\n"
        "2026-10-03T18:00:00+00:00,North,East,0,0,import\n"
        "2026-10-08T18:00:00+00:00,South,West,,,\n"
    )
    client.post(
        f"/api/v1/seasons/{season['id']}/import.csv",
        files={"file": ("fixtures.csv", csv_body, "text/csv")},
    )
    readiness = client.get(f"/api/v1/seasons/{season['id']}/data-readiness").json()
    assert readiness["status"] == "ready"
    response = client.get(f"/api/v1/seasons/{season['id']}/ai-brief")
    assert response.status_code == 503
    assert "AI briefing is disabled" in response.json()["detail"]
