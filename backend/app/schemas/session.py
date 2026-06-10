from datetime import date, datetime

from pydantic import BaseModel, field_validator

from app.schemas.player import PlayerOut


class ScoreCreate(BaseModel):
    player_id: int
    points: int | None = None
    winner: bool = False


class GameSessionCreate(BaseModel):
    game_id: int
    name: str | None = None
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
    name: str | None
    played_at: date
    notes: str | None
    scores: list[ScoreOut] = []

    @field_validator("played_at", mode="before")
    @classmethod
    def coerce_to_date(cls, v: object) -> date:
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, str):
            return datetime.fromisoformat(v).date()
        return v

    model_config = {"from_attributes": True}
