from fastapi import APIRouter

router = APIRouter()


@router.get("/search-url")
async def bgg_search_url(q: str):
    return {"url": f"https://boardgamegeek.com/search/boardgame?q={q}"}
