from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from app.api.v1.routes import auth, games, players, sessions, expansions
from app.auth import get_current_user
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.game", "app.models.player", "app.models.session", "app.models.expansion"]},
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(title="BoardGamesCounter API", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

_protected = [Depends(get_current_user)]
app.include_router(games.router, prefix="/api/v1/games", tags=["games"], dependencies=_protected)
app.include_router(players.router, prefix="/api/v1/players", tags=["players"], dependencies=_protected)
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"], dependencies=_protected)
app.include_router(expansions.router, prefix="/api/v1/games", tags=["expansions"], dependencies=_protected)
