from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.game import Game

GameOut = pydantic_model_creator(Game, name="GameOut")
GameIn = pydantic_model_creator(Game, name="GameIn", exclude_readonly=True)


class GameCreate(BaseModel):
    name: str
    min_players: int = 2
    max_players: int = 4
