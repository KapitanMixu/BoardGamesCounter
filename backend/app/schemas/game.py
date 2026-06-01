from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class GameCreate(BaseModel):
    name: str
    min_players: int = Field(default=2, ge=1)
    max_players: int = Field(default=4, ge=1)

    @model_validator(mode="after")
    def min_le_max(self) -> "GameCreate":
        if self.min_players > self.max_players:
            raise ValueError("min_players must be <= max_players")
        return self


class GameOut(BaseModel):
    id: int
    name: str
    min_players: int
    max_players: int
    times_played: int = 0
    last_played_at: datetime | None = None

    model_config = {"from_attributes": True}
