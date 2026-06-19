from tortoise.expressions import Q
from tortoise.functions import Count

from app.models.player import Player
from app.models.session import Score
from app.schemas.player import PlayerCreate


def _with_stats():
    return Player.all().annotate(
        total_plays=Count("scores"),
        total_wins=Count("scores", _filter=Q(scores__winner=True)),
    )


async def get_all_players() -> list[Player]:
    return await _with_stats()


async def get_player(player_id: int) -> Player | None:
    return await _with_stats().get_or_none(id=player_id)


async def create_player(data: PlayerCreate) -> Player:
    return await Player.create(**data.model_dump())


async def delete_player(player_id: int) -> bool:
    deleted = await Player.filter(id=player_id).delete()
    return deleted > 0


async def get_player_stats(player_id: int) -> dict | None:
    player = await Player.get_or_none(id=player_id)
    if not player:
        return None

    scores = (
        await Score.filter(player_id=player_id)
        .prefetch_related("session__game")
        .order_by("-session__played_at")
    )

    total_plays = len(scores)
    total_wins = sum(1 for s in scores if s.winner)

    per_game: dict[int, dict] = {}
    history: list[dict] = []
    for s in scores:
        session = s.session
        game = session.game
        bucket = per_game.setdefault(
            game.id, {"game_id": game.id, "game_name": game.name, "plays": 0, "wins": 0}
        )
        bucket["plays"] += 1
        if s.winner:
            bucket["wins"] += 1
        history.append(
            {
                "session_id": session.id,
                "game_id": game.id,
                "game_name": game.name,
                "session_name": session.name,
                "played_at": session.played_at,
                "points": s.points,
                "winner": s.winner,
            }
        )

    top_games = sorted(
        per_game.values(), key=lambda g: (g["plays"], g["wins"]), reverse=True
    )[:10]

    return {
        "id": player.id,
        "name": player.name,
        "total_plays": total_plays,
        "total_wins": total_wins,
        "top_games": top_games,
        "session_history": history,
    }
