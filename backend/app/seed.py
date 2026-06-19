import asyncio
from tortoise import Tortoise

from app.auth import hash_password
from app.config import settings
from app.models.game import Game
from app.models.player import Player
from app.models.session import GameSession, Score
from app.models.user import User


async def ensure_admin():
    """Create/refresh the admin account from env (idempotent)."""
    admin = await User.get_or_none(username=settings.API_USERNAME)
    if admin is None:
        await User.create(
            username=settings.API_USERNAME,
            password_hash=hash_password(settings.API_PASSWORD),
            role="admin",
        )
        print(f"Seed: created admin '{settings.API_USERNAME}'.")
    elif admin.role != "admin":
        admin.role = "admin"
        await admin.save(update_fields=["role"])


async def seed():
    await Tortoise.init(config=settings.TORTOISE_ORM)

    await ensure_admin()

    if await Game.exists():
        print("Seed: data already present, skipping.")
        await Tortoise.close_connections()
        return

    catan = await Game.create(name="Catan", min_players=3, max_players=4)
    wingspan = await Game.create(name="Wingspan", min_players=1, max_players=5)
    ticket = await Game.create(name="Ticket to Ride", min_players=2, max_players=5)
    pandemic = await Game.create(name="Pandemic", min_players=2, max_players=4)

    alice = await Player.create(name="Alice")
    bob = await Player.create(name="Bob")
    charlie = await Player.create(name="Charlie")
    diana = await Player.create(name="Diana")

    # Session 1: Catan — Alice wins
    s1 = await GameSession.create(game=catan, notes="Alice dominant from turn 3")
    await Score.create(session=s1, player=alice, points=10, winner=True)
    await Score.create(session=s1, player=bob, points=7, winner=False)
    await Score.create(session=s1, player=charlie, points=5, winner=False)

    # Session 2: Wingspan — Bob wins
    s2 = await GameSession.create(game=wingspan, notes="Bob got the bird engine going")
    await Score.create(session=s2, player=bob, points=88, winner=True)
    await Score.create(session=s2, player=diana, points=72, winner=False)
    await Score.create(session=s2, player=alice, points=65, winner=False)

    # Session 3: Ticket to Ride — Diana wins
    s3 = await GameSession.create(game=ticket)
    await Score.create(session=s3, player=diana, points=142, winner=True)
    await Score.create(session=s3, player=charlie, points=118, winner=False)
    await Score.create(session=s3, player=bob, points=97, winner=False)
    await Score.create(session=s3, player=alice, points=89, winner=False)

    # Session 4: Pandemic — cooperative, no winner
    s4 = await GameSession.create(game=pandemic, notes="Lost on turn 12, ran out of cards")
    await Score.create(session=s4, player=alice, winner=False)
    await Score.create(session=s4, player=charlie, winner=False)

    print("Seed: inserted 4 games, 4 players, 4 sessions.")
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(seed())
