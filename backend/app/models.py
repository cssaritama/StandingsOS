from datetime import date, datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Column,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


season_teams = Table(
    "season_teams",
    Base.metadata,
    Column("season_id", ForeignKey("seasons.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
)


class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    sport: Mapped[str] = mapped_column(String(40), default="football", nullable=False)
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    seasons: Mapped[list["Season"]] = relationship(
        back_populates="competition", cascade="all, delete-orphan"
    )


class Season(Base):
    __tablename__ = "seasons"
    __table_args__ = (
        UniqueConstraint("competition_id", "name", name="season_name_per_competition"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competition_id: Mapped[int] = mapped_column(
        ForeignKey("competitions.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    starts_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    ends_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    competition: Mapped[Competition] = relationship(back_populates="seasons")
    teams: Mapped[list["Team"]] = relationship(secondary=season_teams, back_populates="seasons")
    fixtures: Mapped[list["Fixture"]] = relationship(
        back_populates="season", cascade="all, delete-orphan"
    )


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    seasons: Mapped[list[Season]] = relationship(secondary=season_teams, back_populates="teams")


class Fixture(Base):
    __tablename__ = "fixtures"
    __table_args__ = (
        CheckConstraint("home_team_id != away_team_id", name="fixture_teams_must_differ"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False, index=True
    )
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    season: Mapped[Season] = relationship(back_populates="fixtures")
    home_team: Mapped[Team] = relationship(foreign_keys=[home_team_id])
    away_team: Mapped[Team] = relationship(foreign_keys=[away_team_id])
    result: Mapped["Result | None"] = relationship(
        back_populates="fixture", cascade="all, delete-orphan", uselist=False
    )


class Result(Base):
    """An immutable played-match fact.

    Results are not edited in place. A correction removes the recorded result
    and records a replacement, keeping standings derived from one authoritative
    fact per fixture.
    """

    __tablename__ = "results"
    __table_args__ = (
        CheckConstraint("home_goals >= 0", name="result_home_goals_non_negative"),
        CheckConstraint("away_goals >= 0", name="result_away_goals_non_negative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fixture_id: Mapped[int] = mapped_column(
        ForeignKey("fixtures.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    home_goals: Mapped[int] = mapped_column(Integer, nullable=False)
    away_goals: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(String(30), default="manual", nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    fixture: Mapped[Fixture] = relationship(back_populates="result")
