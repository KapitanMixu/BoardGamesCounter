from app.models.session import GameSession, Score
from app.schemas.session import GameSessionCreate, GameSessionUpdate


async def get_sessions_by_game(game_id: int) -> list[GameSession]:
    return await GameSession.filter(game_id=game_id).prefetch_related("scores__player").order_by("-played_at")


async def get_all_sessions() -> list[GameSession]:
    return await GameSession.all().prefetch_related("scores__player")


async def get_session(session_id: int) -> GameSession | None:
    return await GameSession.filter(id=session_id).prefetch_related("scores__player").first()


async def create_session(data: GameSessionCreate) -> GameSession:
    if data.name:
        name = data.name
    else:
        count = await GameSession.filter(game_id=data.game_id).count()
        name = f"Rozgrywka#{count + 1}"
    session = await GameSession.create(game_id=data.game_id, name=name, notes=data.notes)
    for score_data in data.scores:
        await Score.create(session=session, **score_data.model_dump())
    return await GameSession.filter(id=session.id).prefetch_related("scores__player").first()


async def update_session(session_id: int, data: GameSessionUpdate) -> GameSession | None:
    session = await GameSession.get_or_none(id=session_id)
    if not session:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        session.update_from_dict(update_data)
        await session.save(update_fields=list(update_data.keys()))
    return await get_session(session_id)


async def delete_session(session_id: int) -> bool:
    deleted = await GameSession.filter(id=session_id).delete()
    return deleted > 0
