import xml.etree.ElementTree as ET

import httpx
from fastapi import APIRouter, HTTPException

from app.config import settings

router = APIRouter()


@router.get("/search")
async def bgg_search(q: str):
    if not q.strip():
        return []
    headers = {
        "Authorization": f"Bearer {settings.BGG_API_TOKEN}",
        "User-Agent": "BoardGamesCounter/1.0",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://boardgamegeek.com/xmlapi2/search",
            params={"query": q, "type": "boardgame"},
            headers=headers,
            timeout=10,
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"BGG API error: {resp.status_code}")
    root = ET.fromstring(resp.text)
    q_lower = q.strip().lower()

    results = []
    for item in root.findall("item"):
        primary = item.find("name[@type='primary']")
        if primary is None:
            continue
        bgg_id = item.get("id")
        name = primary.get("value")
        year_el = item.find("yearpublished")
        year = year_el.get("value") if year_el is not None else None
        results.append({
            "id": bgg_id,
            "name": name,
            "year": year,
            "url": f"https://boardgamegeek.com/boardgame/{bgg_id}",
        })

    def rank(r: dict) -> tuple:
        name_lower = r["name"].lower()
        if name_lower == q_lower:
            tier = 0
        elif name_lower.startswith(q_lower):
            tier = 1
        elif q_lower in name_lower.split():
            tier = 2
        elif q_lower in name_lower:
            tier = 3
        else:
            tier = 4
        # within a tier: shorter name (closer match) first, then newer games
        return (tier, len(r["name"]), -int(r["year"]) if r["year"] else 0)

    results.sort(key=rank)
    return results[:10]
