import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_list_players_empty(client: AsyncClient):
    r = await client.get("/api/v1/players/")
    assert r.status_code == 200
    assert r.json() == []


async def test_create_player(client: AsyncClient):
    r = await client.post("/api/v1/players/", json={"name": "Alice"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Alice"
    assert "id" in data


async def test_player_list_includes_plays_and_wins(client: AsyncClient):
    game = (await client.post("/api/v1/games/", json={"name": "Catan"})).json()["id"]
    alice = (await client.post("/api/v1/players/", json={"name": "Alice"})).json()["id"]
    bob = (await client.post("/api/v1/players/", json={"name": "Bob"})).json()["id"]

    await client.post("/api/v1/sessions/", json={"game_id": game, "scores": [
        {"player_id": alice, "points": 10, "winner": True},
        {"player_id": bob, "points": 8, "winner": False},
    ]})
    await client.post("/api/v1/sessions/", json={"game_id": game, "scores": [
        {"player_id": alice, "points": 5, "winner": False},
    ]})

    players = {p["name"]: p for p in (await client.get("/api/v1/players/")).json()}
    assert players["Alice"]["total_plays"] == 2
    assert players["Alice"]["total_wins"] == 1
    assert players["Bob"]["total_plays"] == 1
    assert players["Bob"]["total_wins"] == 0


async def test_new_player_has_zero_stats(client: AsyncClient):
    r = await client.post("/api/v1/players/", json={"name": "Fresh"})
    data = r.json()
    assert data["total_plays"] == 0
    assert data["total_wins"] == 0


async def test_get_player(client: AsyncClient):
    create = await client.post("/api/v1/players/", json={"name": "Bob"})
    player_id = create.json()["id"]
    r = await client.get(f"/api/v1/players/{player_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "Bob"


async def test_get_player_not_found(client: AsyncClient):
    r = await client.get("/api/v1/players/9999")
    assert r.status_code == 404


async def test_list_players_returns_all(client: AsyncClient):
    await client.post("/api/v1/players/", json={"name": "Alice"})
    await client.post("/api/v1/players/", json={"name": "Bob"})
    r = await client.get("/api/v1/players/")
    assert len(r.json()) == 2


async def test_delete_player(client: AsyncClient):
    create = await client.post("/api/v1/players/", json={"name": "Carol"})
    player_id = create.json()["id"]
    r = await client.delete(f"/api/v1/players/{player_id}")
    assert r.status_code == 204
    r = await client.get(f"/api/v1/players/{player_id}")
    assert r.status_code == 404


async def test_delete_player_not_found(client: AsyncClient):
    r = await client.delete("/api/v1/players/9999")
    assert r.status_code == 404
