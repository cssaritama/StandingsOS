from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Competition, Fixture, Result, Season, Team


DEMO_TEAMS = [
    "Atlas United",
    "Aurora FC",
    "Cobalt Athletic",
    "Harbor Rovers",
    "Northbridge FC",
    "Riverside City",
]


def seed_demo(db: Session) -> bool:
    existing = db.scalar(select(Competition).where(Competition.name == "Global City League"))
    if existing is not None:
        return False

    competition = Competition(name="Global City League", sport="football", country="International")
    season = Season(name="2026/27", status="active")
    competition.seasons.append(season)
    db.add(competition)

    teams = []
    for name in DEMO_TEAMS:
        team = db.scalar(select(Team).where(Team.name == name)) or Team(name=name)
        season.teams.append(team)
        teams.append(team)

    db.flush()
    now = datetime.now(timezone.utc).replace(hour=18, minute=0, second=0, microsecond=0)
    pairings = [
        (0, 1, -18, (2, 1)),
        (2, 3, -17, (1, 1)),
        (4, 5, -16, (0, 2)),
        (1, 2, -10, (3, 0)),
        (3, 4, -9, (2, 2)),
        (5, 0, -8, (1, 0)),
        (0, 2, 2, None),
        (1, 3, 3, None),
        (4, 0, 5, None),
        (5, 2, 6, None),
    ]

    for home_index, away_index, day_offset, score in pairings:
        fixture = Fixture(
            season=season,
            home_team=teams[home_index],
            away_team=teams[away_index],
            scheduled_at=now + timedelta(days=day_offset),
        )
        if score is not None:
            fixture.result = Result(
                home_goals=score[0],
                away_goals=score[1],
                source="demo",
            )
        db.add(fixture)

    db.commit()
    return True
