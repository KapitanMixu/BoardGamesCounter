from app.models.player import Player
from app.schemas.player import PlayerCreate


async def get_all_players() -> list[Player]:
    return await Player.all()


async def get_player(player_id: int) -> Player | None:
    return await Player.get_or_none(id=player_id)


async def create_player(data: PlayerCreate) -> Player:
    return await Player.create(**data.model_dump())


async def delete_player(player_id: int) -> bool:
    deleted = await Player.filter(id=player_id).delete()
    return deleted > 0
