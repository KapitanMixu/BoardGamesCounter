from app.models.session import GameSession, Score
from app.schemas.session import GameSessionCreate


async def get_all_sessions() -> list[GameSession]:
    return await GameSession.all().prefetch_related("game", "scores__player")


async def get_session(session_id: int) -> GameSession | None:
    return await GameSession.get_or_none(id=session_id).prefetch_related("game", "scores__player")


async def create_session(data: GameSessionCreate) -> GameSession:
    session = await GameSession.create(game_id=data.game_id, notes=data.notes)
    for score_data in data.scores:
        await Score.create(session=session, **score_data.model_dump())
    return session
