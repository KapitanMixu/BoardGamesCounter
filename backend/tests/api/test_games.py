import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_list_games_empty(client: AsyncClient):
    r = await client.get("/api/v1/games/")
    assert r.status_code == 200
    assert r.json() == []


async def test_create_game(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "Catan", "min_players": 3, "max_players": 6})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Catan"
    assert data["min_players"] == 3
    assert data["max_players"] == 6
    assert "id" in data


async def test_create_game_defaults(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "Chess"})
    assert r.status_code == 201
    data = r.json()
    assert data["min_players"] == 2
    assert data["max_players"] == 4


async def test_create_game_min_gt_max_fails(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "X", "min_players": 6, "max_players": 2})
    assert r.status_code == 422


async def test_create_game_zero_players_fails(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "X", "min_players": 0, "max_players": 4})
    assert r.status_code == 422


async def test_get_game(client: AsyncClient):
    create = await client.post("/api/v1/games/", json={"name": "Go", "min_players": 2, "max_players": 2})
    game_id = create.json()["id"]
    r = await client.get(f"/api/v1/games/{game_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "Go"


async def test_get_game_not_found(client: AsyncClient):
    r = await client.get("/api/v1/games/9999")
    assert r.status_code == 404


async def test_list_games_returns_all(client: AsyncClient):
    await client.post("/api/v1/games/", json={"name": "A"})
    await client.post("/api/v1/games/", json={"name": "B"})
    r = await client.get("/api/v1/games/")
    assert len(r.json()) == 2


async def test_delete_game(client: AsyncClient):
    create = await client.post("/api/v1/games/", json={"name": "Deleted"})
    game_id = create.json()["id"]
    r = await client.delete(f"/api/v1/games/{game_id}")
    assert r.status_code == 204
    r = await client.get(f"/api/v1/games/{game_id}")
    assert r.status_code == 404


async def test_delete_game_not_found(client: AsyncClient):
    r = await client.delete("/api/v1/games/9999")
    assert r.status_code == 404
