from fastapi import APIRouter, HTTPException

from app.schemas.session import GameSessionCreate, GameSessionOut, GameSessionUpdate
from app.services import session as session_service

router = APIRouter()


@router.get("/", response_model=list[GameSessionOut])
async def list_sessions():
    return await session_service.get_all_sessions()


@router.get("/{session_id}", response_model=GameSessionOut)
async def get_session(session_id: int):
    session = await session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/", response_model=GameSessionOut, status_code=201)
async def create_session(data: GameSessionCreate):
    return await session_service.create_session(data)


@router.patch("/{session_id}", response_model=GameSessionOut)
async def update_session(session_id: int, data: GameSessionUpdate):
    session = await session_service.update_session(session_id, data)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/{session_id}", status_code=204)
async def delete_session(session_id: int):
    deleted = await session_service.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
