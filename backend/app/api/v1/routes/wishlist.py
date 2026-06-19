import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.wishlist import (
    WishlistItemCreate,
    WishlistItemOut,
    WishlistItemUpdate,
)
from app.services import wishlist as wishlist_service

router = APIRouter()


@router.get("/", response_model=list[WishlistItemOut])
async def list_items():
    return await wishlist_service.get_all()


@router.post("/", response_model=WishlistItemOut, status_code=201)
async def create_item(data: WishlistItemCreate):
    return await wishlist_service.create(data)


@router.patch("/{item_id}", response_model=WishlistItemOut)
async def update_item(item_id: int, data: WishlistItemUpdate):
    item = await wishlist_service.update(item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    deleted = await wishlist_service.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Wishlist item not found")


@router.post("/{item_id}/refresh-price", response_model=WishlistItemOut)
async def refresh_price(item_id: int):
    item = await wishlist_service.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    if not item.planszeo_url:
        raise HTTPException(status_code=400, detail="Brak linku Planszeo dla tej pozycji")
    try:
        return await wishlist_service.refresh_price(item_id)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Błąd pobierania z Planszeo: {e}")
