import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _create_game(client: AsyncClient, name: str = "Catan") -> int:
    r = await client.post("/api/v1/games/", json={"name": name})
    return r.json()["id"]


async def test_list_expansions_empty(client: AsyncClient):
    game_id = await _create_game(client)
    r = await client.get(f"/api/v1/games/{game_id}/expansions/")
    assert r.status_code == 200
    assert r.json() == []


async def test_create_expansion(client: AsyncClient):
    game_id = await _create_game(client)
    r = await client.post(f"/api/v1/games/{game_id}/expansions/", json={"name": "Seafarers"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Seafarers"
    assert "id" in data


async def test_list_expansions_returns_all(client: AsyncClient):
    game_id = await _create_game(client)
    await client.post(f"/api/v1/games/{game_id}/expansions/", json={"name": "Seafarers"})
    await client.post(f"/api/v1/games/{game_id}/expansions/", json={"name": "Cities & Knights"})
    r = await client.get(f"/api/v1/games/{game_id}/expansions/")
    assert len(r.json()) == 2


async def test_expansions_isolated_per_game(client: AsyncClient):
    g1 = await _create_game(client, "Catan")
    g2 = await _create_game(client, "Terraforming Mars")
    await client.post(f"/api/v1/games/{g1}/expansions/", json={"name": "Seafarers"})
    r = await client.get(f"/api/v1/games/{g2}/expansions/")
    assert r.json() == []


async def test_delete_expansion(client: AsyncClient):
    game_id = await _create_game(client)
    create_r = await client.post(f"/api/v1/games/{game_id}/expansions/", json={"name": "Seafarers"})
    exp_id = create_r.json()["id"]
    r = await client.delete(f"/api/v1/games/{game_id}/expansions/{exp_id}")
    assert r.status_code == 204
    r = await client.get(f"/api/v1/games/{game_id}/expansions/")
    assert r.json() == []


async def test_delete_expansion_not_found(client: AsyncClient):
    game_id = await _create_game(client)
    r = await client.delete(f"/api/v1/games/{game_id}/expansions/9999")
    assert r.status_code == 404


async def test_delete_expansion_wrong_game(client: AsyncClient):
    g1 = await _create_game(client, "Catan")
    g2 = await _create_game(client, "Terraforming Mars")
    create_r = await client.post(f"/api/v1/games/{g1}/expansions/", json={"name": "Seafarers"})
    exp_id = create_r.json()["id"]
    r = await client.delete(f"/api/v1/games/{g2}/expansions/{exp_id}")
    assert r.status_code == 404
