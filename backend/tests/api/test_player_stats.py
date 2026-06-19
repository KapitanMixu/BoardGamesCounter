import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _game(client, name="Catan"):
    return (await client.post("/api/v1/games/", json={"name": name})).json()["id"]


async def _player(client, name):
    return (await client.post("/api/v1/players/", json={"name": name})).json()["id"]


async def test_player_stats_not_found(client: AsyncClient):
    r = await client.get("/api/v1/players/9999/stats")
    assert r.status_code == 404


async def test_player_stats_empty(client: AsyncClient):
    pid = await _player(client, "Alice")
    r = await client.get(f"/api/v1/players/{pid}/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["total_plays"] == 0
    assert data["total_wins"] == 0
    assert data["top_games"] == []
    assert data["session_history"] == []


async def test_player_stats_aggregates_wins_and_plays(client: AsyncClient):
    g1 = await _game(client, "Catan")
    g2 = await _game(client, "Wingspan")
    alice = await _player(client, "Alice")

    # 2 plays of Catan (1 win), 1 play of Wingspan (0 wins)
    await client.post("/api/v1/sessions/", json={"game_id": g1, "scores": [{"player_id": alice, "points": 10, "winner": True}]})
    await client.post("/api/v1/sessions/", json={"game_id": g1, "scores": [{"player_id": alice, "points": 5, "winner": False}]})
    await client.post("/api/v1/sessions/", json={"game_id": g2, "scores": [{"player_id": alice, "points": 60, "winner": False}]})

    r = await client.get(f"/api/v1/players/{alice}/stats")
    data = r.json()
    assert data["total_plays"] == 3
    assert data["total_wins"] == 1
    assert len(data["session_history"]) == 3

    top = {g["game_name"]: g for g in data["top_games"]}
    assert top["Catan"]["plays"] == 2
    assert top["Catan"]["wins"] == 1
    assert top["Wingspan"]["plays"] == 1
    # most-played game ranks first
    assert data["top_games"][0]["game_name"] == "Catan"


async def test_player_stats_isolated_per_player(client: AsyncClient):
    g = await _game(client)
    alice = await _player(client, "Alice")
    bob = await _player(client, "Bob")
    await client.post("/api/v1/sessions/", json={"game_id": g, "scores": [
        {"player_id": alice, "points": 10, "winner": True},
        {"player_id": bob, "points": 8, "winner": False},
    ]})

    a = (await client.get(f"/api/v1/players/{alice}/stats")).json()
    b = (await client.get(f"/api/v1/players/{bob}/stats")).json()
    assert a["total_wins"] == 1
    assert b["total_wins"] == 0
    assert b["total_plays"] == 1
