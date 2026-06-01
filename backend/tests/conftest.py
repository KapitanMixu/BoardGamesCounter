from contextlib import asynccontextmanager

import pytest
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from app.auth import get_current_user
from app.main import app

app.dependency_overrides[get_current_user] = lambda: "testuser"

TEST_DB_URL = "sqlite://:memory:"


@asynccontextmanager
async def noop_lifespan(app):
    yield


app.router.lifespan_context = noop_lifespan


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    await Tortoise.init(
        db_url=TEST_DB_URL,
        modules={"models": ["app.models.game", "app.models.player", "app.models.session"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.fixture(autouse=True)
async def clean_db(init_db):
    yield
    from app.models.session import Score, GameSession
    from app.models.player import Player
    from app.models.game import Game

    await Score.all().delete()
    await GameSession.all().delete()
    await Player.all().delete()
    await Game.all().delete()


@pytest.fixture
async def client(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
