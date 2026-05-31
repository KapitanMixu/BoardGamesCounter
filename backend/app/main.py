from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from app.api.v1.routes import games, players, sessions
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.game", "app.models.player", "app.models.session"]},
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(title="BoardGamesCounter API", lifespan=lifespan)

app.include_router(games.router, prefix="/api/v1/games", tags=["games"])
app.include_router(players.router, prefix="/api/v1/players", tags=["players"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
