#!/usr/bin/env python3
"""Drop ALL tables in the target DB (clean slate for aerich).

    DATABASE_URL="postgres://..." python backend/scripts/drop_all.py
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tortoise import Tortoise, connections


async def main():
    from app.config import _parse_db_connection

    db = _parse_db_connection(os.environ["DATABASE_URL"])
    await Tortoise.init(config={
        "connections": {"default": db},
        "apps": {"models": {"models": ["app.models.game"], "default_connection": "default"}},
    })
    conn = connections.get("default")
    await conn.execute_script("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
    """)
    print("Dropped all tables (schema public reset).")
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
