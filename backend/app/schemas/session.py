from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.session import GameSession, Score

GameSessionOut = pydantic_model_creator(GameSession, name="GameSessionOut")
ScoreOut = pydantic_model_creator(Score, name="ScoreOut")


class ScoreCreate(BaseModel):
    player_id: int
    points: int
    winner: bool = False


class GameSessionCreate(BaseModel):
    game_id: int
    notes: str | None = None
    scores: list[ScoreCreate] = []
