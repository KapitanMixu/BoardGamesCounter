from app.models.session import GameSession, Score
from app.schemas.session import GameSessionCreate


async def get_all_sessions() -> list[GameSession]:
    return await GameSession.all().prefetch_related("scores__player")


async def get_session(session_id: int) -> GameSession | None:
    return await GameSession.filter(id=session_id).prefetch_related("scores__player").first()


async def create_session(data: GameSessionCreate) -> GameSession:
    session = await GameSession.create(game_id=data.game_id, notes=data.notes)
    for score_data in data.scores:
        await Score.create(session=session, **score_data.model_dump())
    return await GameSession.filter(id=session.id).prefetch_related("scores__player").first()


async def delete_session(session_id: int) -> bool:
    deleted = await GameSession.filter(id=session_id).delete()
    return deleted > 0
