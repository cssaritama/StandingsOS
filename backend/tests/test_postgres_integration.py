import os

import pytest
from sqlalchemy import select

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_TESTS") != "1",
    reason="PostgreSQL integration test is enabled only in CI or explicitly by the developer.",
)


def test_postgres_can_persist_competition_domain():
    from app.db import Base, SessionLocal, engine
    from app.models import Competition, Season

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        competition = Competition(name="Integration League", sport="football")
        competition.seasons.append(Season(name="2026/27"))
        db.add(competition)
        db.commit()

    with SessionLocal() as db:
        stored = db.scalar(select(Competition).where(Competition.name == "Integration League"))
        assert stored is not None
        assert stored.seasons[0].name == "2026/27"
