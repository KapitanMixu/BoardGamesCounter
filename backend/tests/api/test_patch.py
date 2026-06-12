import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _make_game(client: AsyncClient, name: str = "Catan") -> int:
    r = await client.post("/api/v1/games/", json={"name": name})
    return r.json()["id"]


async def _make_session(client: AsyncClient, game_id: int, **kwargs) -> int:
    r = await client.post("/api/v1/sessions/", json={"game_id": game_id, **kwargs})
    return r.json()["id"]


async def _make_expansion(client: AsyncClient, game_id: int, name: str = "Expansion") -> int:
    r = await client.post(f"/api/v1/games/{game_id}/expansions/", json={"name": name})
    return r.json()["id"]


# --- PATCH /api/v1/games/{id} ---

async def test_patch_game_name(client: AsyncClient):
    game_id = await _make_game(client, "Old Name")
    r = await client.patch(f"/api/v1/games/{game_id}", json={"name": "New Name"})
    assert r.status_code == 200
    assert r.json()["name"] == "New Name"


async def test_patch_game_players(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.patch(f"/api/v1/games/{game_id}", json={"min_players": 3, "max_players": 5})
    assert r.status_code == 200
    data = r.json()
    assert data["min_players"] == 3
    assert data["max_players"] == 5


async def test_patch_game_duration(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.patch(f"/api/v1/games/{game_id}", json={"duration_minutes": 60, "duration_type": "total"})
    assert r.status_code == 200
    data = r.json()
    assert data["duration_minutes"] == 60
    assert data["duration_type"] == "total"


async def test_patch_game_partial_no_unset_fields_change(client: AsyncClient):
    r = await client.post("/api/v1/games/", json={"name": "Chess", "min_players": 2, "max_players": 2})
    game_id = r.json()["id"]
    await client.patch(f"/api/v1/games/{game_id}", json={"name": "Chess Updated"})
    r = await client.get(f"/api/v1/games/{game_id}")
    data = r.json()
    assert data["name"] == "Chess Updated"
    assert data["min_players"] == 2
    assert data["max_players"] == 2


async def test_patch_game_min_gt_max_fails(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.patch(f"/api/v1/games/{game_id}", json={"min_players": 8, "max_players": 2})
    assert r.status_code == 422


async def test_patch_game_not_found(client: AsyncClient):
    r = await client.patch("/api/v1/games/9999", json={"name": "X"})
    assert r.status_code == 404


# --- PATCH /api/v1/sessions/{id} ---

async def test_patch_session_name(client: AsyncClient):
    game_id = await _make_game(client)
    session_id = await _make_session(client, game_id)
    r = await client.patch(f"/api/v1/sessions/{session_id}", json={"name": "Finał"})
    assert r.status_code == 200
    assert r.json()["name"] == "Finał"


async def test_patch_session_notes(client: AsyncClient):
    game_id = await _make_game(client)
    session_id = await _make_session(client, game_id)
    r = await client.patch(f"/api/v1/sessions/{session_id}", json={"notes": "Epic game!"})
    assert r.status_code == 200
    assert r.json()["notes"] == "Epic game!"


async def test_patch_session_preserves_scores(client: AsyncClient):
    game_id = await _make_game(client)
    p = (await client.post("/api/v1/players/", json={"name": "Alice"})).json()["id"]
    session_id = await _make_session(client, game_id, scores=[{"player_id": p, "points": 10, "winner": True}])
    r = await client.patch(f"/api/v1/sessions/{session_id}", json={"notes": "updated"})
    assert r.status_code == 200
    assert len(r.json()["scores"]) == 1


async def test_patch_session_not_found(client: AsyncClient):
    r = await client.patch("/api/v1/sessions/9999", json={"name": "X"})
    assert r.status_code == 404


# --- PATCH /api/v1/games/{id}/expansions/{exp_id} ---

async def test_patch_expansion_name(client: AsyncClient):
    game_id = await _make_game(client)
    exp_id = await _make_expansion(client, game_id, "Seafarers")
    r = await client.patch(f"/api/v1/games/{game_id}/expansions/{exp_id}", json={"name": "Cities & Knights"})
    assert r.status_code == 200
    assert r.json()["name"] == "Cities & Knights"


async def test_patch_expansion_not_found(client: AsyncClient):
    game_id = await _make_game(client)
    r = await client.patch(f"/api/v1/games/{game_id}/expansions/9999", json={"name": "X"})
    assert r.status_code == 404


async def test_patch_expansion_wrong_game(client: AsyncClient):
    g1 = await _make_game(client, "Catan")
    g2 = await _make_game(client, "Terraforming Mars")
    exp_id = await _make_expansion(client, g1, "Seafarers")
    r = await client.patch(f"/api/v1/games/{g2}/expansions/{exp_id}", json={"name": "X"})
    assert r.status_code == 404
