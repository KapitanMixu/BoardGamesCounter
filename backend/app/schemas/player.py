from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.player import Player

PlayerOut = pydantic_model_creator(Player, name="PlayerOut")
PlayerIn = pydantic_model_creator(Player, name="PlayerIn", exclude_readonly=True)


class PlayerCreate(BaseModel):
    name: str
