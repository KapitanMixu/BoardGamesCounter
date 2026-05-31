import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _make_game(client: AsyncClient, name: str = "Catan") -> int:
    r = await client.post("/api/v1/games/", json={"name": name, "min_players": 2, "max_players": 6})
    return r.json()["id"]


async def _make_player(client: AsyncClient, name: str) -> int:
    r = await client.post("/api/v1/players/", json={"name": name})
    return r.json()["id"]


async def test_list_sessions_empty(client: AsyncClient):
    r = await client.get("/api/v1/sessions/")
    assert r.status_code == 200
    assert r.json() == []


async def test_create_session_no_scores(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.post("/api/v1/sessions/", json={"game_id": game_id})
    assert r.status_code == 201
    data = r.json()
    assert data["game_id"] == game_id
    assert data["scores"] == []


async def test_create_session_with_scores(client: AsyncClient):
    game_id = await _make_game(client)
    p1 = await _make_player(client, "Alice")
    p2 = await _make_player(client, "Bob")

    r = await client.post("/api/v1/sessions/", json={
        "game_id": game_id,
        "scores": [
            {"player_id": p1, "points": 10, "winner": True},
            {"player_id": p2, "points": 7, "winner": False},
        ],
    })
    assert r.status_code == 201
    data = r.json()
    assert len(data["scores"]) == 2
    winners = [s for s in data["scores"] if s["winner"]]
    assert len(winners) == 1
    assert winners[0]["player"]["name"] == "Alice"
    assert winners[0]["points"] == 10


async def test_create_session_multiple_winners(client: AsyncClient):
    game_id = await _make_game(client)
    p1 = await _make_player(client, "Alice")
    p2 = await _make_player(client, "Bob")

    r = await client.post("/api/v1/sessions/", json={
        "game_id": game_id,
        "scores": [
            {"player_id": p1, "points": 10, "winner": True},
            {"player_id": p2, "points": 10, "winner": True},
        ],
    })
    assert r.status_code == 201
    winners = [s for s in r.json()["scores"] if s["winner"]]
    assert len(winners) == 2


async def test_session_response_contains_player_data(client: AsyncClient):
    game_id = await _make_game(client)
    p1 = await _make_player(client, "Charlie")

    r = await client.post("/api/v1/sessions/", json={
        "game_id": game_id,
        "scores": [{"player_id": p1, "points": 5, "winner": True}],
    })
    score = r.json()["scores"][0]
    assert "player" in score
    assert score["player"]["name"] == "Charlie"
    assert score["player"]["id"] == p1


async def test_get_session(client: AsyncClient):
    game_id = await _make_game(client)
    create = await client.post("/api/v1/sessions/", json={"game_id": game_id})
    session_id = create.json()["id"]
    r = await client.get(f"/api/v1/sessions/{session_id}")
    assert r.status_code == 200
    assert r.json()["id"] == session_id


async def test_get_session_not_found(client: AsyncClient):
    r = await client.get("/api/v1/sessions/9999")
    assert r.status_code == 404


async def test_delete_session(client: AsyncClient):
    game_id = await _make_game(client)
    create = await client.post("/api/v1/sessions/", json={"game_id": game_id})
    session_id = create.json()["id"]
    r = await client.delete(f"/api/v1/sessions/{session_id}")
    assert r.status_code == 204
    r = await client.get(f"/api/v1/sessions/{session_id}")
    assert r.status_code == 404


async def test_delete_session_not_found(client: AsyncClient):
    r = await client.delete("/api/v1/sessions/9999")
    assert r.status_code == 404


async def test_session_with_notes(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.post("/api/v1/sessions/", json={"game_id": game_id, "notes": "Epic game!"})
    assert r.status_code == 201
    assert r.json()["notes"] == "Epic game!"
