from app.models.expansion import Expansion
from app.schemas.expansion import ExpansionCreate, ExpansionUpdate


async def get_expansions(game_id: int) -> list[Expansion]:
    return await Expansion.filter(game_id=game_id).all()


async def create_expansion(game_id: int, data: ExpansionCreate) -> Expansion:
    return await Expansion.create(game_id=game_id, name=data.name)


async def update_expansion(game_id: int, expansion_id: int, data: ExpansionUpdate) -> Expansion | None:
    expansion = await Expansion.get_or_none(id=expansion_id, game_id=game_id)
    if not expansion:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if update_data:
        expansion.update_from_dict(update_data)
        await expansion.save(update_fields=list(update_data.keys()))
    return expansion


async def delete_expansion(game_id: int, expansion_id: int) -> bool:
    deleted = await Expansion.filter(id=expansion_id, game_id=game_id).delete()
    return deleted > 0
