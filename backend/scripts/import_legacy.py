#!/usr/bin/env python3
"""
Import legacy data from Google Sheets CSV.

Run from repo root:
    DATABASE_URL="postgres://..." python backend/scripts/import_legacy.py "Gry Mixa - Arkusz1.csv"

Flags:
    --clear   delete all existing games/players/sessions before import
"""

import asyncio
import csv
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tortoise import Tortoise


NAME_MAP = {
    "mix": "Mix",
    "mikuś": "Mix",
    "agacia": "Agata",
    "arti": "Artur",
    "konrad śwagier": "Konrad",
}


def normalize(name: str) -> str:
    n = name.strip()
    return NAME_MAP.get(n.lower(), n)


def parse_winners(raw: str) -> list[str]:
    if not raw:
        return []
    parts = []
    for segment in raw.split(","):
        segment = segment.strip()
        if " i " in segment.lower():
            parts.extend(s.strip() for s in segment.split(" i "))
        else:
            parts.append(segment)
    return [normalize(p) for p in parts if p]


def parse_max_players(raw: str) -> int:
    try:
        return int(raw.strip())
    except (ValueError, AttributeError):
        return 4


def parse_date(raw: str) -> datetime:
    raw = raw.strip()
    if not raw:
        return datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    try:
        d = datetime.strptime(raw, "%Y-%m-%d")
        return d.replace(hour=12, tzinfo=timezone.utc)
    except ValueError:
        return datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)


async def clear_data():
    from app.models.session import Score, GameSession
    from app.models.expansion import Expansion
    from app.models.player import Player
    from app.models.game import Game

    print("Clearing existing data...")
    await Score.all().delete()
    await GameSession.all().delete()
    await Expansion.all().delete()
    await Player.all().delete()
    await Game.all().delete()
    print("Done clearing.")


async def main(csv_path: str, clear: bool):
    raw_url = os.environ.get("DATABASE_URL", "sqlite://./db.sqlite3")
    db_url = raw_url.replace("postgresql://", "postgres://", 1).replace("sslmode=require", "ssl=require")

    await Tortoise.init(
        db_url=db_url,
        modules={"models": [
            "app.models.game", "app.models.player", "app.models.session",
            "app.models.expansion", "app.models.wishlist", "app.models.user",
        ]},
    )
    await Tortoise.generate_schemas(safe=True)

    if clear:
        await clear_data()

    from app.models.game import Game
    from app.models.player import Player
    from app.models.session import GameSession, Score
    from app.models.expansion import Expansion

    rows = []
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Nazwa"].strip():
                rows.append(row)

    print(f"Rows to import: {len(rows)}")

    # Collect all unique player names from ROZEGRANA rows
    all_names: set[str] = set()
    for row in rows:
        if row["Czy grana w tym roku"] == "ROZEGRANA":
            for name in parse_winners(row["Zwycięzcy"]):
                all_names.add(name)

    # Create players
    player_map: dict[str, Player] = {}
    for name in sorted(all_names):
        p, created = await Player.get_or_create(name=name)
        player_map[name] = p
        if created:
            print(f"  + Player: {name}")

    # Import games
    for row in rows:
        name = row["Nazwa"].strip()
        played = row["Czy grana w tym roku"] == "ROZEGRANA"
        max_p = parse_max_players(row["Max ilość graczy"])
        expansions_raw = row["Dodatki"].strip()

        game, created = await Game.get_or_create(
            name=name,
            defaults={"min_players": 2, "max_players": max_p},
        )
        if created:
            print(f"  + Game: {name}")

        # Expansions
        if expansions_raw:
            for exp_name in expansions_raw.split(","):
                exp_name = exp_name.strip()
                if exp_name:
                    await Expansion.get_or_create(name=exp_name, game=game)

        if not played:
            continue

        # Legacy session
        plays_raw = row["Ilość rozegranych gier od 01.01.2024"].strip()
        plays = int(plays_raw) if plays_raw.isdigit() else 1
        last_played = parse_date(row["Data ostatniej gry"])
        winners = parse_winners(row["Zwycięzcy"])
        win_counts = Counter(winners)

        session = await GameSession.create(
            game=game,
            played_at=last_played,
            name="Legacy",
            notes=f"Zaimportowane z arkusza. Łącznie rozegrań: {plays}.",
        )

        for winner_name, count in win_counts.items():
            player = player_map.get(winner_name)
            if player:
                await Score.create(
                    session=session,
                    player=player,
                    winner=True,
                    points=count if count > 1 else None,
                )

        print(f"  OK {name} ({plays}x) -> {list(win_counts.keys())}")

    await Tortoise.close_connections()
    print("\nImport complete.")


if __name__ == "__main__":
    args = sys.argv[1:]
    do_clear = "--clear" in args
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("Usage: python backend/scripts/import_legacy.py <file.csv> [--clear]")
        sys.exit(1)
    asyncio.run(main(files[0], do_clear))
