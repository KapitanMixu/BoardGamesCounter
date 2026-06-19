from fastapi import APIRouter, HTTPException

from app.schemas.player import PlayerCreate, PlayerOut, PlayerStatsOut
from app.services import player as player_service

router = APIRouter()


@router.get("/", response_model=list[PlayerOut])
async def list_players():
    return await player_service.get_all_players()


@router.get("/{player_id}/stats", response_model=PlayerStatsOut)
async def get_player_stats(player_id: int):
    stats = await player_service.get_player_stats(player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Player not found")
    return stats


@router.get("/{player_id}", response_model=PlayerOut)
async def get_player(player_id: int):
    player = await player_service.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.post("/", response_model=PlayerOut, status_code=201)
async def create_player(data: PlayerCreate):
    return await player_service.create_player(data)


@router.delete("/{player_id}", status_code=204)
async def delete_player(player_id: int):
    deleted = await player_service.delete_player(player_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Player not found")
