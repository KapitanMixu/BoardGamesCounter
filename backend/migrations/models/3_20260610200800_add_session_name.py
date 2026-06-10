from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game_sessions" ADD "name" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game_sessions" DROP COLUMN "name";"""


MODELS_STATE = (
    "eJztmtFu2zYUhl9F0FUKeIXjJW2ROzt1Wq+JXcTeVnQYBFpiZKIUqVDUYiPzuw+kJFOkJc"
    "3K7ERedBXnkEckP5Ln/CL1aAfUgzh6+wkE0L6wHm2S/NDsHcsGYaiswsDBHMuKPgigtIB5"
    "xBlwuX1h3QEcwY5lezByGQo5osS+sEiMsTBSN+IMEV+ZYoLuY+hw6kO+gMy+sP74s2PZiH"
    "hwCaPs3/CHc4cg9rR+Ik+0Le0OX4XSNiL8SlYUrc0dl+I4IKpyuOILSja1EeHC6kMCGeBQ"
    "PJ6zWHRf9C4dZjaipKeqStLFnI8H70CMeW64OzJwKRH8EOFiwI+2L1r5qXd69v7sw8/vzj"
    "50LFv2ZGN5v06Gp8aeOEoC45m9luWAg6SGxKi4yb9b5C4XgBWjy+ob8CLOTHgZqip6mUHh"
    "U0tmT/wCsHQwJD5fCGjn5xW0fuvfXn7u3570zs/fiNFQBtxkcY/Tol5SJpDmtggiTojBCr"
    "Koxho0vP59Me6LZ++lF2OOHFg+hZzu9XzkzppDzosZEH1wAkRiDuvgK3J9EsM00j3nZj4U"
    "RTnwGlFwy/FJ4fAFAOrRsLtLMOyWx8KuGQpdBsVwHcC3aX4EHHIUwGKiuqeB00td32Y/Gp"
    "prGATehOBVOrcVdGejm+F01r/5KkYSRNE9loj6s6Eo6UnryrCevDNmYvMQ6/fR7LMl/rW+"
    "T8ZDSZBG3GeyRVVv9t0WfQIxpw6hDw7wcools2Zg1kJr3aVaayO+5sD98QCY52glagVEMI"
    "oQJQUBaZB6Xn25hVjunoKZzsnNafKkZk51OrXKqqZcsYDLEJA90BhmzzkyFmK90B4tW0Hb"
    "RUEvMC2AAF/2WrQtWkqZfJUCoOhVJS2pfFnJyYf2daV5Gbp9XTng60qbo199jnapaPU/5a"
    "SpeEYzp/hF8lFesZScn+UETfUxmpMXUW1+avNTU98fD5GepDR7SnbSHNvk1IDklJ9WQgtP"
    "qWZwWRJUNg5HsjWq5mr4baZNU7YBTm76395oU3U9GX/Kquc2zOX1ZGDsE5koaoXpnMfznZ"
    "m+fLjekkg6w22AV5RB5JMvcCU5jkjEAXGLwrRxOXY8Uqhj2Qw8bPJ+fmlQ4ngQQ54krv70"
    "sv9xaEuIrax8flmZ8CgQlBtQ5VJSzUerIY9JQ4ZUtrQ7O+XwSu9xHhAhyZGfEXkoxRCQYm"
    "rKyaA2pxQfKgTV3X67i4zBZHKtiYzByFQRv94Mhrcnp1JxRPcYJTF+G2dyOlpPXGg+r0le"
    "5MGl7+31yOlOrwldhTJLoexJnB3lVZKp0fR1UizTtnfxHgiqC5XjhaeFp7oS95ACT93tFY"
    "g87eKvXOjp94yt2GtanGvMgeH/80KrPQlpT0KacBJyyDTRhwy5i6IckZZUJgig6rTJ4YiS"
    "w1+QFavg8vyQc2lTxAak2Bo1IKbVjxPgaXeXzzpPu+Xfdcoy46MRSjhM9qAO8ZfpZFzytY"
    "hyMW/jkMutvy2MooYm23U5PzHe6rsc89rGuEsTDxB3OTW+3Nh/Yln/A43wrb0="
)
