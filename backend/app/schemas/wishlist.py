from datetime import datetime

from pydantic import BaseModel


class WishlistItemCreate(BaseModel):
    name: str
    planszeo_url: str | None = None
    bgg_url: str | None = None
    notes: str | None = None


class WishlistItemUpdate(BaseModel):
    name: str | None = None
    planszeo_url: str | None = None
    bgg_url: str | None = None
    notes: str | None = None


class WishlistItemOut(BaseModel):
    id: int
    name: str
    planszeo_url: str | None
    bgg_url: str | None
    notes: str | None
    best_price: float | None
    best_price_shop: str | None
    offer_count: int | None
    price_updated_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
