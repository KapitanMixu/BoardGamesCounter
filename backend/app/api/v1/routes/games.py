from fastapi import APIRouter, HTTPException

from app.schemas.game import GameCreate, GameOut
from app.services import game as game_service

router = APIRouter()


@router.get("/", response_model=list[GameOut])
async def list_games():
    return await game_service.get_all_games()


@router.get("/{game_id}", response_model=GameOut)
async def get_game(game_id: int):
    game = await game_service.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/", response_model=GameOut, status_code=201)
async def create_game(data: GameCreate):
    return await game_service.create_game(data)


@router.delete("/{game_id}", status_code=204)
async def delete_game(game_id: int):
    deleted = await game_service.delete_game(game_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Game not found")
