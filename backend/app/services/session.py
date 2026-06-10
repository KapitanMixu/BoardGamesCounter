from app.models.session import GameSession, Score
from app.schemas.session import GameSessionCreate


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


async def delete_session(session_id: int) -> bool:
    deleted = await GameSession.filter(id=session_id).delete()
    return deleted > 0
