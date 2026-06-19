from datetime import datetime

from pydantic import BaseModel


class PlayerCreate(BaseModel):
    name: str


class PlayerOut(BaseModel):
    id: int
    name: str
    total_plays: int = 0
    total_wins: int = 0

    model_config = {"from_attributes": True}


class GameStat(BaseModel):
    game_id: int
    game_name: str
    plays: int
    wins: int


class SessionHistoryItem(BaseModel):
    session_id: int
    game_id: int
    game_name: str
    session_name: str | None
    played_at: datetime
    points: int | None
    winner: bool


class PlayerStatsOut(BaseModel):
    id: int
    name: str
    total_plays: int
    total_wins: int
    top_games: list[GameStat]
    session_history: list[SessionHistoryItem]
