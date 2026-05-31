import pytest
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from app.main import app

TEST_DB_URL = "sqlite://:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    await Tortoise.init(
        db_url=TEST_DB_URL,
        modules={"models": ["app.models.game", "app.models.player", "app.models.session"]},
    )
    await Tortoise.generate_schemas()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    await Tortoise.close_connections()
