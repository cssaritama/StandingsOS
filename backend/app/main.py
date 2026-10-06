import csv
import io
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import httpx
from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.ai import AIUnavailable, build_evidence_payload, generate_brief
from app.analytics import compute_analytics
from app.config import (
    APP_NAME,
    APP_VERSION,
    AUTO_CREATE_SCHEMA,
    CORS_ORIGINS,
    SEED_DEMO_DATA,
)
from app.db import SessionLocal, get_db, init_db
from app.forecasting import forecast_match
from app.readiness import assess_season_readiness
from app.models import Competition, Fixture, Result, Season, Team
from app.schemas import (
    AIBriefOut,
    AnalyticsOut,
    CompetitionCreate,
    CompetitionOut,
    DataReadinessOut,
    FixtureCreate,
    FixtureOut,
    ForecastOut,
    ImportSummary,
    ResultCreate,
    ResultOut,
    SeasonCreate,
    SeasonOut,
    StandingOut,
    TeamCreate,
    TeamOut,
)
from app.seed import seed_demo
from app.standings import MatchResult, compute_standings


@asynccontextmanager
async def lifespan(_: FastAPI):
    if AUTO_CREATE_SCHEMA:
        init_db()
    if SEED_DEMO_DATA:
        with SessionLocal() as db:
            seed_demo(db)
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Competition intelligence API: schedules are operational state, results are facts, "
        "standings and analytics are derived, and optional AI briefs are grounded in evidence."
    ),
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "standingsos-api", "version": APP_VERSION}


@app.get("/ready", tags=["meta"])
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=503, detail="Database is not ready") from exc
    return {"status": "ready"}


def _season_or_404(db: Session, season_id: int) -> Season:
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


def _fixture_or_404(db: Session, fixture_id: int) -> Fixture:
    fixture = db.scalar(
        select(Fixture)
        .where(Fixture.id == fixture_id)
        .options(joinedload(Fixture.home_team), joinedload(Fixture.away_team), joinedload(Fixture.result))
    )
    if fixture is None:
        raise HTTPException(status_code=404, detail="Fixture not found")
    return fixture


def _fixture_out(fixture: Fixture) -> FixtureOut:
    result = None
    if fixture.result is not None:
        result = ResultOut(
            id=fixture.result.id,
            home_goals=fixture.result.home_goals,
            away_goals=fixture.result.away_goals,
            source=fixture.result.source,
            recorded_at=fixture.result.recorded_at,
        )
    return FixtureOut(
        id=fixture.id,
        season_id=fixture.season_id,
        home_team_id=fixture.home_team_id,
        home_team=fixture.home_team.name,
        away_team_id=fixture.away_team_id,
        away_team=fixture.away_team.name,
        scheduled_at=fixture.scheduled_at,
        status="completed" if fixture.result else "scheduled",
        result=result,
    )


def _season_data(db: Session, season_id: int):
    season = _season_or_404(db, season_id)
    teams = sorted(season.teams, key=lambda team: team.name.casefold())
    fixtures = db.scalars(
        select(Fixture)
        .where(Fixture.season_id == season_id)
        .options(joinedload(Fixture.home_team), joinedload(Fixture.away_team), joinedload(Fixture.result))
        .order_by(Fixture.scheduled_at, Fixture.id)
    ).unique().all()
    matches = [
        MatchResult(
            home_team=fixture.home_team.name,
            away_team=fixture.away_team.name,
            home_goals=fixture.result.home_goals,
            away_goals=fixture.result.away_goals,
        )
        for fixture in fixtures
        if fixture.result is not None
    ]
    table = compute_standings([team.name for team in teams], matches)
    return season, teams, fixtures, matches, table


# --- Competitions and seasons ---------------------------------------------


@app.get("/api/v1/competitions", response_model=list[CompetitionOut], tags=["competitions"])
def list_competitions(db: Session = Depends(get_db)):
    return db.scalars(select(Competition).order_by(Competition.name)).all()


@app.post(
    "/api/v1/competitions",
    response_model=CompetitionOut,
    status_code=status.HTTP_201_CREATED,
    tags=["competitions"],
)
def create_competition(payload: CompetitionCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    sport_name = payload.sport.strip().lower()
    if not name or not sport_name:
        raise HTTPException(status_code=422, detail="Competition name and sport cannot be blank")
    competition = Competition(
        name=name,
        sport=sport_name,
        country=payload.country.strip() if payload.country and payload.country.strip() else None,
    )
    db.add(competition)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Competition already exists") from exc
    db.refresh(competition)
    return competition


@app.get(
    "/api/v1/competitions/{competition_id}/seasons",
    response_model=list[SeasonOut],
    tags=["seasons"],
)
def list_seasons(competition_id: int, db: Session = Depends(get_db)):
    if db.get(Competition, competition_id) is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    return db.scalars(
        select(Season)
        .where(Season.competition_id == competition_id)
        .order_by(Season.created_at.desc())
    ).all()


@app.post(
    "/api/v1/competitions/{competition_id}/seasons",
    response_model=SeasonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["seasons"],
)
def create_season(competition_id: int, payload: SeasonCreate, db: Session = Depends(get_db)):
    competition = db.get(Competition, competition_id)
    if competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    if payload.starts_on and payload.ends_on and payload.ends_on < payload.starts_on:
        raise HTTPException(status_code=422, detail="Season end date cannot precede start date")
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Season name cannot be blank")
    season = Season(
        competition=competition,
        name=name,
        status=payload.status,
        starts_on=payload.starts_on,
        ends_on=payload.ends_on,
    )
    db.add(season)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Season already exists") from exc
    db.refresh(season)
    return season


# --- Teams ----------------------------------------------------------------


@app.get("/api/v1/seasons/{season_id}/teams", response_model=list[TeamOut], tags=["teams"])
def list_season_teams(season_id: int, db: Session = Depends(get_db)):
    season = _season_or_404(db, season_id)
    return sorted(season.teams, key=lambda team: team.name.casefold())


@app.post(
    "/api/v1/seasons/{season_id}/teams",
    response_model=TeamOut,
    status_code=status.HTTP_201_CREATED,
    tags=["teams"],
)
def add_team_to_season(season_id: int, payload: TeamCreate, db: Session = Depends(get_db)):
    season = _season_or_404(db, season_id)
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Team name cannot be blank")
    team = db.scalar(select(Team).where(Team.name == name))
    if team is None:
        team = Team(name=name)
        db.add(team)
        db.flush()
    if team in season.teams:
        raise HTTPException(status_code=409, detail="Team is already enrolled in this season")
    season.teams.append(team)
    db.commit()
    db.refresh(team)
    return team


# --- Fixtures and immutable results ---------------------------------------


@app.get(
    "/api/v1/seasons/{season_id}/fixtures",
    response_model=list[FixtureOut],
    tags=["fixtures"],
)
def list_fixtures(season_id: int, db: Session = Depends(get_db)):
    _season_or_404(db, season_id)
    fixtures = db.scalars(
        select(Fixture)
        .where(Fixture.season_id == season_id)
        .options(joinedload(Fixture.home_team), joinedload(Fixture.away_team), joinedload(Fixture.result))
        .order_by(Fixture.scheduled_at, Fixture.id)
    ).unique().all()
    return [_fixture_out(fixture) for fixture in fixtures]


@app.post(
    "/api/v1/seasons/{season_id}/fixtures",
    response_model=FixtureOut,
    status_code=status.HTTP_201_CREATED,
    tags=["fixtures"],
)
def create_fixture(season_id: int, payload: FixtureCreate, db: Session = Depends(get_db)):
    season = _season_or_404(db, season_id)
    if payload.home_team_id == payload.away_team_id:
        raise HTTPException(status_code=422, detail="A team cannot play itself")
    home = db.get(Team, payload.home_team_id)
    away = db.get(Team, payload.away_team_id)
    if home is None or away is None:
        raise HTTPException(status_code=404, detail="Team not found")
    enrolled = {team.id for team in season.teams}
    if home.id not in enrolled or away.id not in enrolled:
        raise HTTPException(status_code=422, detail="Both teams must be enrolled in the season")
    fixture = Fixture(
        season=season,
        home_team=home,
        away_team=away,
        scheduled_at=payload.scheduled_at,
    )
    db.add(fixture)
    db.commit()
    fixture = _fixture_or_404(db, fixture.id)
    return _fixture_out(fixture)


@app.post(
    "/api/v1/fixtures/{fixture_id}/result",
    response_model=FixtureOut,
    status_code=status.HTTP_201_CREATED,
    tags=["results"],
)
def record_result(fixture_id: int, payload: ResultCreate, db: Session = Depends(get_db)):
    fixture = _fixture_or_404(db, fixture_id)
    if fixture.result is not None:
        raise HTTPException(
            status_code=409,
            detail="A result already exists. Remove it before recording a correction.",
        )
    fixture.result = Result(
        home_goals=payload.home_goals,
        away_goals=payload.away_goals,
        source=payload.source.strip() or "manual",
    )
    db.commit()
    fixture = _fixture_or_404(db, fixture_id)
    return _fixture_out(fixture)


@app.delete(
    "/api/v1/fixtures/{fixture_id}/result",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["results"],
)
def remove_result(fixture_id: int, db: Session = Depends(get_db)):
    fixture = _fixture_or_404(db, fixture_id)
    if fixture.result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(fixture.result)
    db.commit()


# --- AI-ready data -------------------------------------------------------

@app.get(
    "/api/v1/seasons/{season_id}/data-readiness",
    response_model=DataReadinessOut,
    tags=["data"],
)
def get_data_readiness(season_id: int, db: Session = Depends(get_db)):
    season, teams, fixtures, _, _ = _season_data(db, season_id)
    assessment = assess_season_readiness(season, teams, fixtures)
    return DataReadinessOut(
        season_id=season_id,
        score=assessment.score,
        status=assessment.status,
        policy_version=assessment.policy_version,
        checked_at=assessment.checked_at,
        dimensions=assessment.dimensions,
        blockers=assessment.blockers,
        warnings=assessment.warnings,
    )


# --- Derived intelligence --------------------------------------------------


@app.get(
    "/api/v1/seasons/{season_id}/standings",
    response_model=list[StandingOut],
    tags=["intelligence"],
)
def get_standings(season_id: int, db: Session = Depends(get_db)):
    _, _, _, _, table = _season_data(db, season_id)
    return [
        StandingOut(
            position=index,
            team=row.team,
            played=row.played,
            won=row.won,
            drawn=row.drawn,
            lost=row.lost,
            goals_for=row.goals_for,
            goals_against=row.goals_against,
            goal_difference=row.goal_difference,
            points=row.points,
        )
        for index, row in enumerate(table, start=1)
    ]


@app.get(
    "/api/v1/seasons/{season_id}/analytics",
    response_model=AnalyticsOut,
    tags=["intelligence"],
)
def get_analytics(season_id: int, db: Session = Depends(get_db)):
    _, _, fixtures, matches, table = _season_data(db, season_id)
    analytics = compute_analytics(table, matches, len(fixtures))
    return AnalyticsOut(season_id=season_id, **analytics.__dict__)


@app.get(
    "/api/v1/seasons/{season_id}/forecasts",
    response_model=list[ForecastOut],
    tags=["intelligence"],
)
def get_forecasts(season_id: int, db: Session = Depends(get_db)):
    _, teams, fixtures, matches, _ = _season_data(db, season_id)
    names = [team.name for team in teams]
    forecasts = []
    for fixture in fixtures:
        if fixture.result is not None:
            continue
        forecast = forecast_match(fixture.home_team.name, fixture.away_team.name, names, matches)
        forecasts.append(
            ForecastOut(
                fixture_id=fixture.id,
                home_team=fixture.home_team.name,
                away_team=fixture.away_team.name,
                home_win_probability=forecast.home_win_probability,
                draw_probability=forecast.draw_probability,
                away_win_probability=forecast.away_win_probability,
                model=forecast.model,
                explanation=(
                    "Transparent Elo-based baseline using only results recorded in this season. "
                    "It is a decision aid, not a betting model."
                ),
            )
        )
    return forecasts


@app.get(
    "/api/v1/seasons/{season_id}/ai-brief",
    response_model=AIBriefOut,
    tags=["ai"],
)
async def get_ai_brief(season_id: int, db: Session = Depends(get_db)):
    season, teams, fixtures, matches, table = _season_data(db, season_id)
    readiness = assess_season_readiness(season, teams, fixtures)
    if readiness.status != "ready":
        reasons = readiness.blockers or readiness.warnings or ["Readiness score is below the AI threshold."]
        raise HTTPException(
            status_code=409,
            detail=f"AI readiness gate blocked this brief: {'; '.join(reasons)}",
        )
    analytics = compute_analytics(table, matches, len(fixtures))
    standings = [
        {
            "position": index,
            "team": row.team,
            "played": row.played,
            "goal_difference": row.goal_difference,
            "points": row.points,
        }
        for index, row in enumerate(table, start=1)
    ]
    forecasts = [item.model_dump() for item in get_forecasts(season_id, db)]
    evidence = build_evidence_payload(
        season={
            "id": season.id,
            "name": season.name,
            "competition": season.competition.name,
        },
        analytics=AnalyticsOut(season_id=season_id, **analytics.__dict__).model_dump(),
        standings=standings,
        forecasts=forecasts,
        readiness=DataReadinessOut(
            season_id=season_id,
            score=readiness.score,
            status=readiness.status,
            policy_version=readiness.policy_version,
            checked_at=readiness.checked_at,
            dimensions=readiness.dimensions,
            blockers=readiness.blockers,
            warnings=readiness.warnings,
        ).model_dump(mode="json"),
    )
    try:
        return await generate_brief(evidence)
    except AIUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except httpx.HTTPError as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail="AI provider request failed") from exc


# --- Data portability ------------------------------------------------------


@app.get("/api/v1/seasons/{season_id}/export.csv", tags=["data"])
def export_season_csv(season_id: int, db: Session = Depends(get_db)):
    _, _, fixtures, _, _ = _season_data(db, season_id)
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "scheduled_at",
            "home_team",
            "away_team",
            "home_goals",
            "away_goals",
            "result_source",
        ],
    )
    writer.writeheader()
    for fixture in fixtures:
        writer.writerow(
            {
                "scheduled_at": fixture.scheduled_at.isoformat(),
                "home_team": fixture.home_team.name,
                "away_team": fixture.away_team.name,
                "home_goals": fixture.result.home_goals if fixture.result else "",
                "away_goals": fixture.result.away_goals if fixture.result else "",
                "result_source": fixture.result.source if fixture.result else "",
            }
        )
    return Response(
        output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="season-{season_id}.csv"'},
    )


@app.post(
    "/api/v1/seasons/{season_id}/import.csv",
    response_model=ImportSummary,
    tags=["data"],
)
async def import_season_csv(
    season_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    season = _season_or_404(db, season_id)
    raw = (await file.read()).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(raw))
    required = {"scheduled_at", "home_team", "away_team"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise HTTPException(
            status_code=422,
            detail="CSV requires scheduled_at, home_team and away_team columns",
        )

    rows_processed = teams_created = fixtures_created = results_recorded = 0
    for row in reader:
        rows_processed += 1
        home_name = (row.get("home_team") or "").strip()
        away_name = (row.get("away_team") or "").strip()
        if not home_name or not away_name or home_name == away_name:
            raise HTTPException(status_code=422, detail=f"Invalid teams on row {rows_processed}")

        teams = []
        for name in (home_name, away_name):
            team = db.scalar(select(Team).where(Team.name == name))
            if team is None:
                team = Team(name=name)
                db.add(team)
                db.flush()
                teams_created += 1
            if team not in season.teams:
                season.teams.append(team)
            teams.append(team)

        try:
            scheduled_at = datetime.fromisoformat((row.get("scheduled_at") or "").replace("Z", "+00:00"))
            if scheduled_at.tzinfo is None:
                scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)
        except ValueError as exc:
            raise HTTPException(
                status_code=422, detail=f"Invalid scheduled_at on row {rows_processed}"
            ) from exc

        fixture = Fixture(
            season=season,
            home_team=teams[0],
            away_team=teams[1],
            scheduled_at=scheduled_at,
        )
        db.add(fixture)
        db.flush()
        fixtures_created += 1

        home_goals = (row.get("home_goals") or "").strip()
        away_goals = (row.get("away_goals") or "").strip()
        if (home_goals == "") != (away_goals == ""):
            raise HTTPException(
                status_code=422,
                detail=f"Both goal columns must be present or blank on row {rows_processed}",
            )
        if home_goals != "" and away_goals != "":
            try:
                home_value = int(home_goals)
                away_value = int(away_goals)
            except ValueError as exc:
                raise HTTPException(
                    status_code=422, detail=f"Invalid goal value on row {rows_processed}"
                ) from exc
            if home_value < 0 or away_value < 0:
                raise HTTPException(
                    status_code=422, detail=f"Goal values cannot be negative on row {rows_processed}"
                )
            fixture.result = Result(
                home_goals=home_value,
                away_goals=away_value,
                source=(row.get("result_source") or "csv").strip() or "csv",
            )
            results_recorded += 1

    db.commit()
    return ImportSummary(
        rows_processed=rows_processed,
        teams_created=teams_created,
        fixtures_created=fixtures_created,
        results_recorded=results_recorded,
    )
