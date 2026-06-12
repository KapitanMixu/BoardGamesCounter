from tortoise.functions import Count, Max

from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate


def _with_stats():
    return Game.all().annotate(
        times_played=Count("sessions"),
        last_played_at=Max("sessions__played_at"),
    )


async def get_all_games() -> list[Game]:
    return await _with_stats()


async def get_game(game_id: int) -> Game | None:
    return await _with_stats().get_or_none(id=game_id)


async def create_game(data: GameCreate) -> Game:
    return await Game.create(**data.model_dump())


async def update_game(game_id: int, data: GameUpdate) -> Game | None:
    game = await Game.get_or_none(id=game_id)
    if not game:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        game.update_from_dict(update_data)
        await game.save(update_fields=list(update_data.keys()))
    return await get_game(game_id)


async def delete_game(game_id: int) -> bool:
    deleted = await Game.filter(id=game_id).delete()
    return deleted > 0
