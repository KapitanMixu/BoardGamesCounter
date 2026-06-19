from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(150) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "role" VARCHAR(20) NOT NULL DEFAULT 'reader',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "users";"""


MODELS_STATE = (
    "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"
)
