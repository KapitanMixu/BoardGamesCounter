import pytest
from httpx import AsyncClient

from app.services.wishlist import parse_planszeo_offers

pytestmark = pytest.mark.anyio


# --- API CRUD ---

async def test_wishlist_empty(client: AsyncClient):
    r = await client.get("/api/v1/wishlist/")
    assert r.status_code == 200
    assert r.json() == []


async def test_create_wishlist_item(client: AsyncClient):
    r = await client.post("/api/v1/wishlist/", json={"name": "Arcs", "planszeo_url": "https://planszeo.pl/gry-planszowe/arcs/oferty"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Arcs"
    assert data["best_price"] is None
    assert data["price_updated_at"] is None


async def test_update_wishlist_item(client: AsyncClient):
    item = (await client.post("/api/v1/wishlist/", json={"name": "Arcs"})).json()
    r = await client.patch(f"/api/v1/wishlist/{item['id']}", json={"notes": "prezent"})
    assert r.status_code == 200
    assert r.json()["notes"] == "prezent"


async def test_delete_wishlist_item(client: AsyncClient):
    item = (await client.post("/api/v1/wishlist/", json={"name": "Arcs"})).json()
    r = await client.delete(f"/api/v1/wishlist/{item['id']}")
    assert r.status_code == 204
    assert (await client.get("/api/v1/wishlist/")).json() == []


async def test_delete_wishlist_not_found(client: AsyncClient):
    r = await client.delete("/api/v1/wishlist/9999")
    assert r.status_code == 404


async def test_refresh_price_without_url_fails(client: AsyncClient):
    item = (await client.post("/api/v1/wishlist/", json={"name": "No link"})).json()
    r = await client.post(f"/api/v1/wishlist/{item['id']}/refresh-price")
    assert r.status_code == 400


async def test_refresh_price_not_found(client: AsyncClient):
    r = await client.post("/api/v1/wishlist/9999/refresh-price")
    assert r.status_code == 404


# --- Planszeo HTML parser (pure, no network) ---

SAMPLE_HTML = """
<div>
  <a href="/oferta/111">
    <img src="https://planszeo.pl/rails/x/tantis.png" />
  </a>
  30,41  zł
  Wysyłka od 5,99  zł
  <a href="/oferta/222">
    <img src="https://planszeo.pl/rails/y/rebel.png" />
  </a>
  84,95  zł
  Wysyłka od 9,99  zł
</div>
"""


async def test_parse_planszeo_offers_picks_cheapest():
    result = parse_planszeo_offers(SAMPLE_HTML)
    assert result["best_price"] == 30.41
    assert result["best_price_shop"] == "Tantis"
    assert result["offer_count"] == 2


async def test_parse_planszeo_offers_empty():
    result = parse_planszeo_offers("<div>no offers here</div>")
    assert result["best_price"] is None
    assert result["offer_count"] == 0


async def test_parse_planszeo_thousands_separator():
    html = '<a href="/oferta/1"><img src="/x/foo.png" /></a> 1 299,00  zł'
    result = parse_planszeo_offers(html)
    assert result["best_price"] == 1299.0
