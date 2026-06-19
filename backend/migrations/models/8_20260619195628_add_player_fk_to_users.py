from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "player_id" INT;
        ALTER TABLE "users" ADD CONSTRAINT "fk_users_players_468bdc26" FOREIGN KEY ("player_id") REFERENCES "players" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP FOREIGN KEY "fk_users_players_468bdc26";
        ALTER TABLE "users" DROP COLUMN "player_id";"""


MODELS_STATE = (
    "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"
    "n4BI5hoSykc8QCQgTnri8fovFVYgMQ=="
)
