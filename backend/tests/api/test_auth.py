from types import SimpleNamespace

import pytest
from httpx import AsyncClient

from app.auth import get_current_user, hash_password, verify_password
from app.config import settings
from app.main import app

ADMIN = SimpleNamespace(username="testadmin", role="admin")

pytestmark = pytest.mark.anyio

ADMIN = SimpleNamespace(username="testadmin", role="admin")
READER = SimpleNamespace(username="friend", role="reader")


# --- password hashing ---

async def test_password_hash_roundtrip():
    h = hash_password("secret123")
    assert h != "secret123"
    assert verify_password("secret123", h)
    assert not verify_password("wrong", h)


# --- registration ---

async def test_register_success(client: AsyncClient):
    r = await client.post("/auth/register", json={
        "username": "friend", "password": "secret123", "invite_code": settings.INVITE_CODE,
    })
    assert r.status_code == 201
    data = r.json()
    assert data["role"] == "reader"
    assert data["username"] == "friend"
    assert "access_token" in data


async def test_register_wrong_code(client: AsyncClient):
    r = await client.post("/auth/register", json={
        "username": "friend", "password": "secret123", "invite_code": "WRONG",
    })
    assert r.status_code == 403


async def test_register_short_password(client: AsyncClient):
    r = await client.post("/auth/register", json={
        "username": "friend", "password": "x", "invite_code": settings.INVITE_CODE,
    })
    assert r.status_code == 422


async def test_register_duplicate_username(client: AsyncClient):
    body = {"username": "friend", "password": "secret123", "invite_code": settings.INVITE_CODE}
    await client.post("/auth/register", json=body)
    r = await client.post("/auth/register", json=body)
    assert r.status_code == 409


# --- login ---

async def test_login_after_register(client: AsyncClient):
    await client.post("/auth/register", json={
        "username": "friend", "password": "secret123", "invite_code": settings.INVITE_CODE,
    })
    r = await client.post("/auth/token", data={"username": "friend", "password": "secret123"})
    assert r.status_code == 200
    assert r.json()["role"] == "reader"


async def test_login_wrong_password(client: AsyncClient):
    await client.post("/auth/register", json={
        "username": "friend", "password": "secret123", "invite_code": settings.INVITE_CODE,
    })
    r = await client.post("/auth/token", data={"username": "friend", "password": "nope"})
    assert r.status_code == 401


# --- role-based gating ---

async def test_reader_cannot_write(client: AsyncClient):
    app.dependency_overrides[get_current_user] = lambda: READER
    try:
        r = await client.post("/api/v1/games/", json={"name": "X"})
        assert r.status_code == 403
    finally:
        app.dependency_overrides[get_current_user] = lambda: ADMIN


async def test_reader_can_read(client: AsyncClient):
    app.dependency_overrides[get_current_user] = lambda: READER
    try:
        r = await client.get("/api/v1/games/")
        assert r.status_code == 200
    finally:
        app.dependency_overrides[get_current_user] = lambda: ADMIN


async def test_admin_can_write(client: AsyncClient):
    # default override is admin
    r = await client.post("/api/v1/games/", json={"name": "AdminGame"})
    assert r.status_code == 201


# --- player linking via /auth/link-player ---

async def test_register_returns_null_player_id(client: AsyncClient):
    r = await client.post("/auth/register", json={
        "username": "friend", "password": "secret123", "invite_code": settings.INVITE_CODE,
    })
    assert r.status_code == 201
    assert r.json()["player_id"] is None


async def test_link_player_existing(client: AsyncClient):
    from app.models.player import Player
    p = await Player.create(name="Janusz")
    r = await client.post("/auth/register", json={
        "username": "friend2", "password": "secret123", "invite_code": settings.INVITE_CODE,
    })
    token = r.json()["access_token"]
    saved = app.dependency_overrides.pop(get_current_user)
    try:
        r2 = await client.post("/auth/link-player", json={"player_id": p.id},
                               headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides[get_current_user] = saved
    assert r2.status_code == 200
    assert r2.json()["player_id"] == p.id


async def test_link_player_new(client: AsyncClient):
    r = await client.post("/auth/register", json={
        "username": "friend3", "password": "secret123", "invite_code": settings.INVITE_CODE,
    })
    token = r.json()["access_token"]
    saved = app.dependency_overrides.pop(get_current_user)
    try:
        r2 = await client.post("/auth/link-player", json={"player_name": "Nowy"},
                               headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides[get_current_user] = saved
    assert r2.status_code == 200
    from app.models.player import Player
    assert await Player.get_or_none(name="Nowy") is not None


async def test_link_player_invalid_id(client: AsyncClient):
    r = await client.post("/auth/register", json={
        "username": "friend4", "password": "secret123", "invite_code": settings.INVITE_CODE,
    })
    token = r.json()["access_token"]
    saved = app.dependency_overrides.pop(get_current_user)
    try:
        r2 = await client.post("/auth/link-player", json={"player_id": 9999},
                               headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides[get_current_user] = saved
    assert r2.status_code == 404


async def test_login_returns_player_id(client: AsyncClient):
    from app.models.player import Player
    from app.models.user import User
    from app.auth import hash_password
    p = await Player.create(name="Linked")
    await User.create(username="withplayer", password_hash=hash_password("secret123"), role="reader", player=p)
    r = await client.post("/auth/token", data={"username": "withplayer", "password": "secret123"})
    assert r.status_code == 200
    assert r.json()["player_id"] == p.id
