from app.models.expansion import Expansion
from app.schemas.expansion import ExpansionCreate


async def get_expansions(game_id: int) -> list[Expansion]:
    return await Expansion.filter(game_id=game_id).all()


async def create_expansion(game_id: int, data: ExpansionCreate) -> Expansion:
    return await Expansion.create(game_id=game_id, name=data.name)


async def delete_expansion(game_id: int, expansion_id: int) -> bool:
    deleted = await Expansion.filter(id=expansion_id, game_id=game_id).delete()
    return deleted > 0
