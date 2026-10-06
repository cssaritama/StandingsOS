from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class CompetitionCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    sport: str = Field(default="football", min_length=2, max_length=40)
    country: str | None = Field(default=None, max_length=80)


class CompetitionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sport: str
    country: str | None


class SeasonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    status: str = Field(default="active", pattern="^(planned|active|completed)$")
    starts_on: date | None = None
    ends_on: date | None = None


class SeasonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_id: int
    name: str
    status: str
    starts_on: date | None
    ends_on: date | None


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)


class TeamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class FixtureCreate(BaseModel):
    home_team_id: int
    away_team_id: int
    scheduled_at: datetime


class ResultCreate(BaseModel):
    home_goals: int = Field(ge=0, le=99)
    away_goals: int = Field(ge=0, le=99)
    source: str = Field(default="manual", max_length=30)


class ResultOut(BaseModel):
    id: int
    home_goals: int
    away_goals: int
    source: str
    recorded_at: datetime


class FixtureOut(BaseModel):
    id: int
    season_id: int
    home_team_id: int
    home_team: str
    away_team_id: int
    away_team: str
    scheduled_at: datetime
    status: str
    result: ResultOut | None


class StandingOut(BaseModel):
    position: int
    team: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int


class AnalyticsOut(BaseModel):
    season_id: int
    fixtures_total: int
    fixtures_completed: int
    completion_rate: float
    goals_total: int
    average_goals_per_match: float
    home_win_rate: float
    draw_rate: float
    away_win_rate: float
    leader: str | None
    strongest_attack: str | None
    strongest_defense: str | None


class ForecastOut(BaseModel):
    fixture_id: int
    home_team: str
    away_team: str
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    model: str
    explanation: str


class ImportSummary(BaseModel):
    rows_processed: int
    teams_created: int
    fixtures_created: int
    results_recorded: int


class AIBriefOut(BaseModel):
    provider: str
    model: str
    generated_at: datetime
    summary: str
    evidence: dict

class DataReadinessOut(BaseModel):
    season_id: int
    score: float
    status: str
    policy_version: str
    checked_at: datetime
    dimensions: dict[str, float]
    blockers: list[str]
    warnings: list[str]
