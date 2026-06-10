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


async def test_new_game_has_zero_times_played(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "Catan"})
    assert r.status_code == 201
    data = r.json()
    assert data["times_played"] == 0
    assert data["last_played_at"] is None


async def test_times_played_increments_after_session(client: AsyncClient):
    game_r = await client.post("/api/v1/games/", json={"name": "Catan"})
    game_id = game_r.json()["id"]

    await client.post("/api/v1/sessions/", json={"game_id": game_id})

    r = await client.get(f"/api/v1/games/{game_id}")
    assert r.json()["times_played"] == 1


async def test_times_played_counts_multiple_sessions(client: AsyncClient):
    game_r = await client.post("/api/v1/games/", json={"name": "Catan"})
    game_id = game_r.json()["id"]

    await client.post("/api/v1/sessions/", json={"game_id": game_id})
    await client.post("/api/v1/sessions/", json={"game_id": game_id})
    await client.post("/api/v1/sessions/", json={"game_id": game_id})

    r = await client.get(f"/api/v1/games/{game_id}")
    assert r.json()["times_played"] == 3


async def test_last_played_at_set_after_session(client: AsyncClient):
    game_r = await client.post("/api/v1/games/", json={"name": "Catan"})
    game_id = game_r.json()["id"]

    await client.post("/api/v1/sessions/", json={"game_id": game_id})

    r = await client.get(f"/api/v1/games/{game_id}")
    assert r.json()["last_played_at"] is not None


async def test_times_played_isolated_per_game(client: AsyncClient):
    g1 = (await client.post("/api/v1/games/", json={"name": "A"})).json()["id"]
    g2 = (await client.post("/api/v1/games/", json={"name": "B"})).json()["id"]

    await client.post("/api/v1/sessions/", json={"game_id": g1})
    await client.post("/api/v1/sessions/", json={"game_id": g1})

    r1 = await client.get(f"/api/v1/games/{g1}")
    r2 = await client.get(f"/api/v1/games/{g2}")
    assert r1.json()["times_played"] == 2
    assert r2.json()["times_played"] == 0


async def test_create_game_with_total_duration(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "Catan", "duration_minutes": 90, "duration_type": "total"})
    assert r.status_code == 201
    data = r.json()
    assert data["duration_minutes"] == 90
    assert data["duration_type"] == "total"


async def test_create_game_with_per_player_duration(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "Chess", "duration_minutes": 20, "duration_type": "per_player"})
    assert r.status_code == 201
    data = r.json()
    assert data["duration_minutes"] == 20
    assert data["duration_type"] == "per_player"


async def test_create_game_without_duration(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "Go"})
    assert r.status_code == 201
    data = r.json()
    assert data["duration_minutes"] is None
    assert data["duration_type"] is None


async def test_create_game_duration_without_type_fails(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "X", "duration_minutes": 60})
    assert r.status_code == 422


async def test_create_game_invalid_duration_type_fails(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "X", "duration_minutes": 60, "duration_type": "unknown"})
    assert r.status_code == 422
