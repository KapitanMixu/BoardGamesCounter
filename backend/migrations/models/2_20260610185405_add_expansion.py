from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "expansions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "game_id" INT NOT NULL REFERENCES "games" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "expansions";"""


MODELS_STATE = (
    "eJztmtFu2zYUhl9F0FUKeIXjJW2ROzt1Wq+JXcTeVnQYBFpiZKIU6VBUYyPzuw+kJFOkJc"
    "3K7ERCdBXnkEckP5Ln/CL1aAfUgzh8+wkE0L6wHm0S/9DsHcsGy6WyCgMHcywr+iCA0gLm"
    "IWfA5faFdQdwCDuW7cHQZWjJESX2hUUijIWRuiFniPjKFBF0H0GHUx/yBWT2hfXX3x3LRs"
    "SDKxim/y5/OHcIYk/rJ/JE29Lu8PVS2kaEX8mKorW541IcBURVXq75gpJtbUS4sPqQQAY4"
    "FI/nLBLdF71LhpmOKO6pqhJ3MePjwTsQYZ4Z7p4MXEoEP0S4GPCj7YtWfumdnr0/+/Dru7"
    "MPHcuWPdla3m/i4amxx46SwHhmb2Q54CCuITEqbvLvDrnLBWD56NL6BryQMxNeiqqMXmpQ"
    "+NSSORC/AKwcDInPFwLa+XkJrT/6t5ef+7cnvfPzN2I0lAE3XtzjpKgXlwmkmS2CiLPEYA"
    "1ZWGENGl7/vRgPxbP30osxQw6snkJO93o+cmf1IedFDIg+OAEiEYdV8OW5PolhEumeczMf"
    "i6IceIUouOP4pHD4AgD1aNjdJxh2i2Nh1wyFLoNiuA7guzQ/Ag45CmA+Ud3TwOklrm/THz"
    "XNNQwCb0LwOpnbErqz0c1wOuvffBUjCcLwHktE/dlQlPSkdW1YT94ZM7F9iPXnaPbZEv9a"
    "3yfjoSRIQ+4z2aKqN/tuiz6BiFOH0AcHeBnFklpTMBuhte4SrbUVX3Pg/ngAzHO0ErUCQh"
    "iGiJKcgDRIPK++3EIsd0/OTGfk5jR+Uj2nOplaZVVTrljA1RKQA9AYps9pGAuxXmiPFq2g"
    "3aKgF5gWQIAvey3aFi0lTL5KAZD3qpKUlL6sZORD+7pSvwzdvq4c8XWlzdGvPke7VLT6v3"
    "LSVDyjnlP8Ivkoq1gKzs8ygqb8GM3Jiqg2PzUpP0lh8ZTYqjm2obUGoTWbMwnNPWOZwVXB"
    "ltg6NORgoGyuht9m2jSl6uLkpv/tjTZV15Pxp7R6Ro1cXk8GhgiRYa5SkMl4PN+J38sHm5"
    "0ErzPcBXhFGUQ++QLXkuOIhBwQN08EG1c7zUnkHctm4GGbtbJLgxLHgxjy+LWgP73sfxza"
    "EmIrip5fFMU8cuTQFlSxEFLz0SqgRikgKlvan51yeKW3EA+IkPjAyog8lGIISD415WRQm1"
    "OKjxWCqm6//UXGYDK51kTGYGSqiN9vBsPbk1OpOMJ7jOIYv4szPturJi40n9ckL7LgkrfO"
    "auR0p9eErkSZJVAOJM4aeRFiajR9neTLtN1dfACC6jqgufC08FRV4h5T4KmbqRyRp11bFQ"
    "s9/ZasFXt1i3PtdcxRr2Pak5D2JKQOJyHHTBN9yJC7yMsRSUlpggCqTpscGpQcfkKWr4KL"
    "80PGpU0RW5Bia1SAmFRvJsDT7j4fJZ52i79KlGXGJw+UcBjvQR3ib9PJuOBbB+Vi3sYhl1"
    "v/WBiFNU22m2J+YrzldznmtY1xlyYeIO5yKnx3cPjEsvkXT51ICA=="
)
