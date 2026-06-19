import re
from datetime import datetime, timezone

import httpx

from app.models.wishlist import WishlistItem
from app.schemas.wishlist import WishlistItemCreate, WishlistItemUpdate

# one offer block starts at each /oferta/<id> link; the first price in the
# block is the product price (shipping "Wysyłka od ... zł" comes after it)
_PRICE_RE = re.compile(r"(\d{1,3}(?:[  ]?\d{3})*,\d{2})\s*zł")
_SHOP_RE = re.compile(r"/([a-zA-Z0-9_]+)\.(?:png|webp|jpg|jpeg|svg)\"")


def _parse_price(raw: str) -> float:
    return float(raw.replace(" ", "").replace(" ", "").replace(",", "."))


def parse_planszeo_offers(html: str) -> dict:
    """Return cheapest offer: {best_price, best_price_shop, offer_count}."""
    blocks = html.split('href="/oferta/')[1:]
    offers: list[tuple[float, str | None]] = []
    for block in blocks:
        price_match = _PRICE_RE.search(block)
        if not price_match:
            continue
        price = _parse_price(price_match.group(1))
        shop_match = _SHOP_RE.search(block)
        shop = shop_match.group(1).capitalize() if shop_match else None
        offers.append((price, shop))

    if not offers:
        return {"best_price": None, "best_price_shop": None, "offer_count": 0}

    best_price, best_shop = min(offers, key=lambda o: o[0])
    return {
        "best_price": best_price,
        "best_price_shop": best_shop,
        "offer_count": len(offers),
    }


async def get_all() -> list[WishlistItem]:
    return await WishlistItem.all().order_by("-created_at")


async def get(item_id: int) -> WishlistItem | None:
    return await WishlistItem.get_or_none(id=item_id)


async def create(data: WishlistItemCreate) -> WishlistItem:
    return await WishlistItem.create(**data.model_dump())


async def update(item_id: int, data: WishlistItemUpdate) -> WishlistItem | None:
    item = await WishlistItem.get_or_none(id=item_id)
    if not item:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        item.update_from_dict(update_data)
        await item.save(update_fields=list(update_data.keys()))
    return item


async def delete(item_id: int) -> bool:
    deleted = await WishlistItem.filter(id=item_id).delete()
    return deleted > 0


async def refresh_price(item_id: int) -> WishlistItem | None:
    item = await WishlistItem.get_or_none(id=item_id)
    if not item or not item.planszeo_url:
        return None
    headers = {"User-Agent": "BoardGamesCounter/1.0 (hobby wishlist)"}
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(item.planszeo_url, headers=headers, timeout=15)
    resp.raise_for_status()
    parsed = parse_planszeo_offers(resp.text)
    item.best_price = parsed["best_price"]
    item.best_price_shop = parsed["best_price_shop"]
    item.offer_count = parsed["offer_count"]
    item.price_updated_at = datetime.now(timezone.utc)
    await item.save(
        update_fields=["best_price", "best_price_shop", "offer_count", "price_updated_at"]
    )
    return item
