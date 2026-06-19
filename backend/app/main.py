from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import RegisterTortoise

from app.api.v1.routes import auth, games, players, sessions, expansions, bgg, wishlist
from app.auth import read_or_admin
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        db_url=settings.DATABASE_URL.replace("postgresql://", "postgres://", 1),
        modules={"models": ["app.models.game", "app.models.player", "app.models.session", "app.models.expansion", "app.models.wishlist", "app.models.user"]},
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(title="BoardGamesCounter API", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

_protected = [Depends(read_or_admin)]
app.include_router(games.router, prefix="/api/v1/games", tags=["games"], dependencies=_protected)
app.include_router(players.router, prefix="/api/v1/players", tags=["players"], dependencies=_protected)
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"], dependencies=_protected)
app.include_router(expansions.router, prefix="/api/v1/games", tags=["expansions"], dependencies=_protected)
app.include_router(bgg.router, prefix="/api/v1/bgg", tags=["bgg"], dependencies=_protected)
app.include_router(wishlist.router, prefix="/api/v1/wishlist", tags=["wishlist"], dependencies=_protected)

_spa_dir = Path(__file__).parent.parent.parent / "frontend_dist"
if _spa_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(_spa_dir), html=True), name="spa")
