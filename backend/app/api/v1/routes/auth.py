from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.config import settings
from app.models.player import Player
from app.models.user import User

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    password: str
    invite_code: str


class LinkPlayerRequest(BaseModel):
    player_id: int | None = None
    player_name: str | None = None


async def _player_id_for(user: User) -> int | None:
    await user.fetch_related("player")
    return user.player.id if user.player else None


def _token_response(user: User, player_id: int | None = None) -> dict:
    return {
        "access_token": create_access_token(user.username, user.role),
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "player_id": player_id,
    }


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _token_response(user, await _player_id_for(user))


@router.post("/register", status_code=201)
async def register(data: RegisterRequest):
    if data.invite_code != settings.INVITE_CODE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nieprawidłowy kod zaproszenia")
    username = data.username.strip()
    if len(username) < 3:
        raise HTTPException(status_code=422, detail="Nazwa użytkownika min. 3 znaki")
    if len(data.password) < 6:
        raise HTTPException(status_code=422, detail="Hasło min. 6 znaków")
    if await User.get_or_none(username=username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nazwa użytkownika zajęta")
    user = await User.create(
        username=username,
        password_hash=hash_password(data.password),
        role="reader",
    )
    return _token_response(user, None)


@router.post("/link-player")
async def link_player(data: LinkPlayerRequest, current_user: User = Depends(get_current_user)):
    player: Player | None = None
    if data.player_id is not None:
        player = await Player.get_or_none(id=data.player_id)
        if player is None:
            raise HTTPException(status_code=404, detail="Gracz nie istnieje")
    elif data.player_name:
        name = data.player_name.strip()
        if not name:
            raise HTTPException(status_code=422, detail="Nazwa gracza nie może być pusta")
        player = await Player.create(name=name)
    else:
        raise HTTPException(status_code=422, detail="Podaj player_id lub player_name")

    current_user.player = player
    await current_user.save()
    return {"player_id": player.id, "player_name": player.name}
