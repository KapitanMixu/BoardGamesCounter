import pytest

from app.services.game import fetch_bgg_thumbnail, _BGG_ID_RE

pytestmark = pytest.mark.anyio


async def test_bgg_id_regex_extracts_id():
    assert _BGG_ID_RE.search("https://boardgamegeek.com/boardgame/13/catan").group(1) == "13"
    assert _BGG_ID_RE.search("https://boardgamegeek.com/boardgame/266192").group(1) == "266192"


async def test_bgg_id_regex_no_match():
    assert _BGG_ID_RE.search("https://planszeo.pl/gry-planszowe/catan") is None


async def test_fetch_thumbnail_none_url_no_network():
    # returns immediately without an HTTP call
    assert await fetch_bgg_thumbnail(None) is None


async def test_fetch_thumbnail_bad_url_no_network():
    assert await fetch_bgg_thumbnail("https://example.com/not-a-bgg-url") is None
