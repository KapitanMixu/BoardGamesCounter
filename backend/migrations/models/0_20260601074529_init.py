from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "games" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "min_players" INT NOT NULL DEFAULT 2,
    "max_players" INT NOT NULL DEFAULT 4,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "players" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "game_sessions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "played_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT,
    "game_id" INT NOT NULL REFERENCES "games" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "scores" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "points" INT,
    "winner" BOOL NOT NULL DEFAULT False,
    "player_id" INT NOT NULL REFERENCES "players" ("id") ON DELETE CASCADE,
    "session_id" INT NOT NULL REFERENCES "game_sessions" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztme9P4jAYx/8VwitMPKMc/si9G4jKKWBg3hmNWcpWxuJocSuHxPC/X9tttBvbDjiEEf"
    "cOnj7P2n7aPs933UdxiA1ou0fXYAiLPwofReT9CNkPC0UwGgkrMxDQs7mjST24BfRc4gCd"
    "UGMf2C6kJgO6umONiIURtaKxbTMj1qmjhUxhGiPrbQw1gk1IBtChDc8v1GwhA77Th/t/R6"
    "9a34K2ERqnZbC+uV0j0xG3NRC54o6st56mY3s8RMJ5NCUDjObeFiLMakIEHUAgezxxxmz4"
    "bHT+NIMZeSMVLt4QpRgD9sHYJtJ0l2SgY8T40dG4fIIm6+Vb+aRyXrn4fla5oC58JHPL+c"
    "ybnpi7F8gJtNTijLcDAjwPjlFwQ/7ChsnVBsCJRxf4R+DRIUfhBajS6AUGgU9smQ3xG4J3"
    "zYbIJAMG7fQ0hdYvpVO7UTol6nXAZoPpNvY2d8tvKnttDKl0RCykjWwwhY67wh6MRP17M2"
    "6KZ3nXm1EiR9dmDXLhqO2Rq2SHnO5ANjkNkEVwl7SFWEMYTy8cGYFn+KFHwY+MHmo6B6ON"
    "7Kmfb1PQqY1mvasqzXs2k6HrvtkckaLWWUuZW6cRa+kscvznDyn8bqg3Bfa38NRu1TlB7B"
    "LT4T0KP/WpyMYExgRrCE80YEilIbAGYGasqPVfpfTMDD2gv06AY2ihFrEDXOi6FFvMwan6"
    "kVe3HWgDznZxpaW63vWelM2lngX7N7AGS84Y4TJOorbYNCwPoxaAgMlHzfpmPflU7nl2id"
    "NBfkuqEpJyU66Fci2UnbO0BS2U16UvX5d07MD/rEpd9oxsLvFO6pFcpRNezqUinv6OrsnC"
    "Ia9P+1SfuLBYJ7eGAvPUmoHUKtdMhElcwlThe8KRmAesJTz8IW0/Z8auVf1RDS1ToC5KTe"
    "XxILRUd+3WdeAuqZHaXbsaESE8za2UZKSI7V0n7D7ZLBT4MMNFgFe0LlsmuoVTzrFBRwSQ"
    "HieCI/fG2eOXVMip2QGTedWStwadHp0UJN5rgdKtKZf14iwXRbsRRR6PGDk0B5UshMR65A"
    "ooa0kpVQFh3tPy7ETAWnl9+7Vy0xfFEwsh78IqknkwtiFA8dREUIRaj0Z9Vgpa9fgtLzKq"
    "7fZdSGRUG1EV8dCs1julE644qJPl5fhFnN7d3mriIhTzleSFDM5/61yNXDjoK6FLUWaueN"
    "PfgDjby8v/qEYL75N4mbZ4ijdAUHwO2F94ofS0qsT9TIGnQMfSB3EKz29JlXhA+OQSL2PZ"
    "LU3i/YFOfHpL/g4jheSfYuYg2dFYAaLvvp8AT46PlwBIvRIB8rbItyyMCEQxl60/u+1Wwk"
    "csERIB+YDoBJ8NSyeHBdtyyUs2saZQZLNOv6qL3sodhq9K2QOqcdpmm+Vl9hf3BSEu"
)
