from fastapi import APIRouter, HTTPException

from app.schemas.expansion import ExpansionCreate, ExpansionOut
from app.schemas.session import GameSessionOut
from app.services import expansion as expansion_service
from app.services import session as session_service

router = APIRouter()


@router.get("/{game_id}/sessions/", response_model=list[GameSessionOut])
async def list_game_sessions(game_id: int):
    return await session_service.get_sessions_by_game(game_id)


@router.get("/{game_id}/expansions/", response_model=list[ExpansionOut])
async def list_expansions(game_id: int):
    return await expansion_service.get_expansions(game_id)


@router.post("/{game_id}/expansions/", response_model=ExpansionOut, status_code=201)
async def create_expansion(game_id: int, data: ExpansionCreate):
    return await expansion_service.create_expansion(game_id, data)


@router.delete("/{game_id}/expansions/{expansion_id}", status_code=204)
async def delete_expansion(game_id: int, expansion_id: int):
    deleted = await expansion_service.delete_expansion(game_id, expansion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expansion not found")
