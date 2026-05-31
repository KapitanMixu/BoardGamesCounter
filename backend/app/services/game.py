from app.models.game import Game
from app.schemas.game import GameCreate


async def get_all_games() -> list[Game]:
    return await Game.all()


async def get_game(game_id: int) -> Game | None:
    return await Game.get_or_none(id=game_id)


async def create_game(data: GameCreate) -> Game:
    return await Game.create(**data.model_dump())


async def delete_game(game_id: int) -> bool:
    deleted = await Game.filter(id=game_id).delete()
    return deleted > 0
