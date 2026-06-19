#!/usr/bin/env python3
"""
Backfill BGG url + thumbnail for games by searching BGG by name.

    DATABASE_URL="postgres://..." python backend/scripts/backfill_bgg.py [--force]

--force  re-fetch even for games that already have a bgg_url
"""

import asyncio
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from tortoise import Tortoise


# Polish title -> English BGG search term (high-confidence only)
NAME_MAP = {
    "Zaginiona Wyspa Arnak": "Lost Ruins of Arnak",
    "Biały Zamek": "The White Castle",
    "Brzdęk! w kosmosie": "Clank! In! Space!",
    "Diuna Imperium": "Dune: Imperium",
    "Fudżi": "Fuji",
    "Gloomheaven Jaws of the Lion": "Gloomhaven: Jaws of the Lion",
    "Great Western Trail Argentyna": "Great Western Trail: Argentina",
    "Teraformacja Marsa": "Terraforming Mars",
    "Wsiąść do Pociągu": "Ticket to Ride",
    "Wyspa Dinozaurów": "Dinosaur Island",
    "Zatoka Kupców": "Merchants Cove",
    "Slay the Spire": "Slay the Spire: The Board Game",
    "Coatl": "Cóatl",
    "Destylaty": "Distilled",
    "Na dnie morza": "Deep Sea Adventure",
    "Posiadłość Szaleństwa": "Mansions of Madness",
    "Zakazana Pustynia": "Forbidden Desert",
    "Cirkadians Ład Chaosu": "Circadians: Chaos Order",
    "Cyklady": "Cyclades",
    "Na skrzydłach": "Wingspan",
    "Na skrzydłach smoków": "Wyrmspan",
    "Wrath of the Lich King": "World of Warcraft: Wrath of the Lich King",
    "Frost Punk": "Frostpunk: The Board Game",
    "Moje Miasto": "My City",
    "Kameleon": "The Chameleon",
    "Kojot": "Coyote",
    "Oath": "Oath: Chronicles of Empire and Exile",
    "Pałac Jabby": "Star Wars: Jabba's Palace",
    "Betrayal": "Betrayal at House on the Hill",
    "Eksplodujące kotki": "Exploding Kittens",
    "Odjechane jednorożnce": "Unstable Unicorns",
    "Liście": "Leaf",
    "Zapomniane morza": "Forgotten Waters",
    "List miłosny": "Love Letter",
    "Sabotażysta - zaginione kopalnie": "Saboteur: The Lost Mines",
    "Sabotażysta": "Saboteur",
    "Diamenty": "Diamant",
    "Kroniki Zbrodni 2400": "Chronicles of Crime: 2400",
    "Warhammer 40k Kill team": "Warhammer 40,000: Kill Team",
    "Mysia Straż": "Mouse Guard",
    "Wyprawa Darwina": "Darwin's Journey",
}


def _headers():
    from app.config import settings
    h = {"User-Agent": "BoardGamesCounter/1.0"}
    if settings.BGG_API_TOKEN:
        h["Authorization"] = f"Bearer {settings.BGG_API_TOKEN}"
    return h


async def search_bgg(client: httpx.AsyncClient, name: str) -> str | None:
    """Return best-match BGG boardgame id for a name, or None."""
    resp = await client.get(
        "https://boardgamegeek.com/xmlapi2/search",
        params={"query": name, "type": "boardgame"},
        headers=_headers(),
        timeout=15,
    )
    if resp.status_code != 200:
        return None
    root = ET.fromstring(resp.text)
    q = name.strip().lower()
    best = None
    best_rank = 99
    for item in root.findall("item"):
        primary = item.find("name[@type='primary']")
        if primary is None:
            continue
        n = primary.get("value", "").lower()
        if n == q:
            rank = 0
        elif n.startswith(q):
            rank = 1
        elif q in n:
            rank = 2
        else:
            rank = 3
        if rank < best_rank:
            best_rank = rank
            best = item.get("id")
    return best


async def fetch_thumbnail(client: httpx.AsyncClient, bgg_id: str) -> str | None:
    # BGG returns 202 while queuing the request; retry a few times.
    for attempt in range(4):
        resp = await client.get(
            "https://boardgamegeek.com/xmlapi2/thing",
            params={"id": bgg_id},
            headers=_headers(),
            timeout=15,
        )
        if resp.status_code == 202:
            await asyncio.sleep(2)
            continue
        if resp.status_code != 200:
            return None
        root = ET.fromstring(resp.text)
        thumb = root.find("item/thumbnail")
        return thumb.text.strip() if thumb is not None and thumb.text else None
    return None


_BGG_ID_RE = re.compile(r"/boardgame/(\d+)")


async def thumbs_only(client: httpx.AsyncClient):
    from app.models.game import Game
    games = await Game.filter(bgg_url__isnull=False, thumbnail_url__isnull=True)
    print(f"Thumbnail backfill: {len(games)} games")
    found = 0
    for game in games:
        m = _BGG_ID_RE.search(game.bgg_url or "")
        if not m:
            continue
        try:
            thumb = await fetch_thumbnail(client, m.group(1))
        except (httpx.HTTPError, ET.ParseError):
            thumb = None
        if thumb:
            game.thumbnail_url = thumb
            await game.save(update_fields=["thumbnail_url"])
            found += 1
            print(f"  OK {game.name}")
        else:
            print(f"  - {game.name}: no thumb")
        await asyncio.sleep(3)
    print(f"\nThumbnails filled: {found}/{len(games)}.")


async def main(force: bool, thumbs: bool):
    from app.config import _parse_db_connection
    from app.models.game import Game

    db = _parse_db_connection(os.environ.get("DATABASE_URL", "sqlite://./db.sqlite3"))
    await Tortoise.init(config={
        "connections": {"default": db},
        "apps": {"models": {"models": [
            "app.models.game", "app.models.player", "app.models.session",
            "app.models.expansion", "app.models.wishlist", "app.models.user",
        ], "default_connection": "default"}},
    })

    if thumbs:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            await thumbs_only(client)
        await Tortoise.close_connections()
        return

    if force:
        games = await Game.all()
    else:
        # missing link, OR linked but no thumbnail yet
        from tortoise.expressions import Q
        games = await Game.filter(Q(bgg_url__isnull=True) | Q(thumbnail_url__isnull=True))

    print(f"Games to process: {len(games)}")
    found = 0

    async with httpx.AsyncClient(follow_redirects=True) as client:
        for game in games:
            query = NAME_MAP.get(game.name, game.name)
            try:
                bgg_id = await search_bgg(client, query)
            except (httpx.HTTPError, ET.ParseError) as e:
                print(f"  ! {game.name}: search error {e}")
                await asyncio.sleep(2)
                continue

            if not bgg_id:
                print(f"  - {game.name}: no match (query={query!r})")
                await asyncio.sleep(1)
                continue

            try:
                thumb = await fetch_thumbnail(client, bgg_id)
            except (httpx.HTTPError, ET.ParseError):
                thumb = None

            game.bgg_url = f"https://boardgamegeek.com/boardgame/{bgg_id}"
            game.thumbnail_url = thumb
            await game.save(update_fields=["bgg_url", "thumbnail_url"])
            found += 1
            print(f"  OK {game.name} -> {bgg_id} {'(thumb)' if thumb else '(no thumb)'}")
            await asyncio.sleep(1)  # BGG rate limit courtesy

    await Tortoise.close_connections()
    print(f"\nDone. Linked {found}/{len(games)}.")


if __name__ == "__main__":
    args = sys.argv[1:]
    asyncio.run(main("--force" in args, "--thumbs-only" in args))
