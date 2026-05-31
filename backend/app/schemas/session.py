from datetime import datetime

from pydantic import BaseModel

from app.schemas.player import PlayerOut


class ScoreCreate(BaseModel):
    player_id: int
    points: int | None = None
    winner: bool = False


class GameSessionCreate(BaseModel):
    game_id: int
    notes: str | None = None
    scores: list[ScoreCreate] = []


class ScoreOut(BaseModel):
    id: int
    player: PlayerOut
    points: int | None
    winner: bool

    model_config = {"from_attributes": True}


class GameSessionOut(BaseModel):
    id: int
    game_id: int
    played_at: datetime
    notes: str | None
    scores: list[ScoreOut] = []

    model_config = {"from_attributes": True}
