from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class GameCreate(BaseModel):
    name: str
    min_players: int = Field(default=2, ge=1)
    max_players: int = Field(default=4, ge=1)
    duration_minutes: int | None = Field(default=None, ge=1)
    duration_type: str | None = None

    @model_validator(mode="after")
    def validate(self) -> "GameCreate":
        if self.min_players > self.max_players:
            raise ValueError("min_players must be <= max_players")
        if self.duration_minutes is not None and self.duration_type not in ("total", "per_player"):
            raise ValueError("duration_type must be 'total' or 'per_player'")
        return self


class GameUpdate(BaseModel):
    name: str | None = None
    min_players: int | None = Field(default=None, ge=1)
    max_players: int | None = Field(default=None, ge=1)
    duration_minutes: int | None = Field(default=None, ge=1)
    duration_type: str | None = None

    @model_validator(mode="after")
    def validate(self) -> "GameUpdate":
        if self.min_players is not None and self.max_players is not None:
            if self.min_players > self.max_players:
                raise ValueError("min_players must be <= max_players")
        if self.duration_minutes is not None and self.duration_type is not None:
            if self.duration_type not in ("total", "per_player"):
                raise ValueError("duration_type must be 'total' or 'per_player'")
        return self


class GameOut(BaseModel):
    id: int
    name: str
    min_players: int
    max_players: int
    duration_minutes: int | None = None
    duration_type: str | None = None
    times_played: int = 0
    last_played_at: date | None = None

    @field_validator("last_played_at", mode="before")
    @classmethod
    def coerce_to_date(cls, v: object) -> date | None:
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, str):
            return datetime.fromisoformat(v).date()
        return v

    model_config = {"from_attributes": True}
