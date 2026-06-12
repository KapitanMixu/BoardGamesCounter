import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _make_game(client: AsyncClient, name: str = "Catan") -> int:
    r = await client.post("/api/v1/games/", json={"name": name})
    return r.json()["id"]


async def _make_player(client: AsyncClient, name: str = "Alice") -> int:
    r = await client.post("/api/v1/players/", json={"name": name})
    return r.json()["id"]


# --- GET /api/v1/games/{id}/sessions/ ---

async def test_list_game_sessions_empty(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.get(f"/api/v1/games/{game_id}/sessions/")
    assert r.status_code == 200
    assert r.json() == []


async def test_list_game_sessions_returns_sessions(client: AsyncClient):
    game_id = await _make_game(client)
    await client.post("/api/v1/sessions/", json={"game_id": game_id})
    await client.post("/api/v1/sessions/", json={"game_id": game_id})

    r = await client.get(f"/api/v1/games/{game_id}/sessions/")
    assert r.status_code == 200
    assert len(r.json()) == 2


async def test_list_game_sessions_isolated_per_game(client: AsyncClient):
    g1 = await _make_game(client, "Catan")
    g2 = await _make_game(client, "Terraforming Mars")

    await client.post("/api/v1/sessions/", json={"game_id": g1})
    await client.post("/api/v1/sessions/", json={"game_id": g1})

    r = await client.get(f"/api/v1/games/{g2}/sessions/")
    assert r.json() == []


async def test_list_game_sessions_contains_scores(client: AsyncClient):
    game_id = await _make_game(client)
    player_id = await _make_player(client)

    await client.post("/api/v1/sessions/", json={
        "game_id": game_id,
        "scores": [{"player_id": player_id, "points": 15, "winner": True}],
    })

    r = await client.get(f"/api/v1/games/{game_id}/sessions/")
    sessions = r.json()
    assert len(sessions) == 1
    assert len(sessions[0]["scores"]) == 1
    assert sessions[0]["scores"][0]["points"] == 15


async def test_list_game_sessions_ordered_newest_first(client: AsyncClient):
    game_id = await _make_game(client)
    await client.post("/api/v1/sessions/", json={"game_id": game_id, "notes": "first"})
    await client.post("/api/v1/sessions/", json={"game_id": game_id, "notes": "second"})

    r = await client.get(f"/api/v1/games/{game_id}/sessions/")
    sessions = r.json()
    assert sessions[0]["id"] > sessions[1]["id"]


# --- Session name auto-generation ---

async def test_session_auto_name_first(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.post("/api/v1/sessions/", json={"game_id": game_id})
    assert r.status_code == 201
    assert r.json()["name"] == "Rozgrywka#1"


async def test_session_auto_name_increments(client: AsyncClient):
    game_id = await _make_game(client)
    await client.post("/api/v1/sessions/", json={"game_id": game_id})
    r = await client.post("/api/v1/sessions/", json={"game_id": game_id})
    assert r.json()["name"] == "Rozgrywka#2"


async def test_session_custom_name_overrides_auto(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.post("/api/v1/sessions/", json={"game_id": game_id, "name": "Finał"})
    assert r.json()["name"] == "Finał"


async def test_session_auto_name_isolated_per_game(client: AsyncClient):
    g1 = await _make_game(client, "Catan")
    g2 = await _make_game(client, "Terraforming Mars")

    await client.post("/api/v1/sessions/", json={"game_id": g1})
    await client.post("/api/v1/sessions/", json={"game_id": g1})

    r = await client.post("/api/v1/sessions/", json={"game_id": g2})
    assert r.json()["name"] == "Rozgrywka#1"
