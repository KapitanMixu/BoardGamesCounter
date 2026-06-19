import re
import xml.etree.ElementTree as ET

import httpx
from tortoise.functions import Count, Max

from app.config import settings
from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate

_BGG_ID_RE = re.compile(r"/boardgame/(\d+)")


def _with_stats():
    return Game.all().annotate(
        times_played=Count("sessions"),
        last_played_at=Max("sessions__played_at"),
    )


async def fetch_bgg_thumbnail(bgg_url: str | None) -> str | None:
    """Derive BGG id from a boardgame URL and fetch its thumbnail. Non-fatal."""
    if not bgg_url:
        return None
    match = _BGG_ID_RE.search(bgg_url)
    if not match:
        return None
    bgg_id = match.group(1)
    headers = {
        "Authorization": f"Bearer {settings.BGG_API_TOKEN}",
        "User-Agent": "BoardGamesCounter/1.0",
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(
                "https://boardgamegeek.com/xmlapi2/thing",
                params={"id": bgg_id},
                headers=headers,
                timeout=10,
            )
        if resp.status_code != 200:
            return None
        root = ET.fromstring(resp.text)
        thumb = root.find("item/thumbnail")
        if thumb is not None and thumb.text:
            return thumb.text.strip()
    except (httpx.HTTPError, ET.ParseError):
        return None
    return None


async def get_all_games() -> list[Game]:
    return await _with_stats()


async def get_game(game_id: int) -> Game | None:
    return await _with_stats().get_or_none(id=game_id)


async def create_game(data: GameCreate) -> Game:
    payload = data.model_dump()
    payload["thumbnail_url"] = await fetch_bgg_thumbnail(payload.get("bgg_url"))
    return await Game.create(**payload)


async def update_game(game_id: int, data: GameUpdate) -> Game | None:
    game = await Game.get_or_none(id=game_id)
    if not game:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if "bgg_url" in update_data:
        update_data["thumbnail_url"] = await fetch_bgg_thumbnail(update_data["bgg_url"])
    if update_data:
        game.update_from_dict(update_data)
        await game.save(update_fields=list(update_data.keys()))
    return await get_game(game_id)


async def delete_game(game_id: int) -> bool:
    deleted = await Game.filter(id=game_id).delete()
    return deleted > 0


async def backfill_thumbnails() -> int:
    """Fetch thumbnails for games that have a bgg_url but no thumbnail. Returns count updated."""
    games = await Game.filter(bgg_url__isnull=False, thumbnail_url__isnull=True)
    updated = 0
    for game in games:
        thumb = await fetch_bgg_thumbnail(game.bgg_url)
        if thumb:
            game.thumbnail_url = thumb
            await game.save(update_fields=["thumbnail_url"])
            updated += 1
    return updated
