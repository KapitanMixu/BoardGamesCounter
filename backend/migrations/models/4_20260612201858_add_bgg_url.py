from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" ADD "bgg_url" VARCHAR(500);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" DROP COLUMN "bgg_url";"""


MODELS_STATE = (
    "eJztmmFvmzgYx78K4lUn5aY012xT3yVduuXWJlOT3U07TcgBl1gzNjXmmqiX7z7ZQIwJcK"
    "FLWrjyquljP9j+2X6ePzYPpkcdiIPXH4AHzXPjwSTRD83eMUzg+8oqDBwssKzoAg9KC1gE"
    "nAGbm+fGLcAB7BimAwObIZ8jSsxzg4QYCyO1A84QcZUpJOguhBanLuRLyMxz4+/vHcNExI"
    "ErGCT/+j+sWwSxo/UTOaJtabf42pe2MeGXsqJobWHZFIceUZX9NV9Ssq2NCBdWFxLIAIfi"
    "8ZyFovuid/EwkxFFPVVVoi6mfBx4C0LMU8Pdk4FNieCHCBcDfjBd0cpvvdOzt2fvfn9z9q"
    "5jmLInW8vbTTQ8NfbIURKYzM2NLAccRDUkRsVN/t0hd7EELB9dUj8DL+AsCy9BVUYvMSh8"
    "askciJ8HVhaGxOVLAa3fL6H15+Dm4uPg5qTX778So6EM2NHinsRFvahMIE1tEUQsH4M1ZE"
    "GFNZjx+u/FeCievedejClyYPUYcrrX05E7qw85J2RA9MHyEAk5rIIvz/VRDONI95Sb+VgU"
    "5cArRMEdx0eFw2cAqEfD7j7BsFscC7vZULhwXStkuArKlEsjIfa7+1Dsd4sxyjKdo82gGL"
    "EF+C7K94BDjjyYj1P3zBB1YtfXyY+a5mwGgTMleB1Pbwnf+fh6NJsPrj+LkXhBcIclosF8"
    "JEp60rrOWE/eZKZi+xDjr/H8oyH+Nb5NJyNJkAbcZbJFVW/+zRR9AiGnFqH3FnBSyi+xJm"
    "A2QrPexpp1K2IXwP5xD5hjaSVqBQQwCBAlOYF9GHtefrqBWEahnJlOyfZZ9KR6TnU8tcqq"
    "plyxgCsfkAPQGCXPaRgLsV5ojxatoN0ir+dlLYAAV/ZatC1aipl8lkIq75UvLil96UvJsP"
    "a1r35Kp33tO+JrX5ujX3yOtqlo9Zdy0kw8o55T/Cz5KK1YCs4hU4Km/DjSSouoNj+1+amm"
    "r5BHSU9Smj0mO2mObXKqQXJKTyuhuad9c7gqCCpbh4ZsjbK5Gn2da9OUbICT68HXV9pUXU"
    "0nH5LqqQ1zcTUdZvaJTBSVwnTK4+nOnp8/XO9IJJ3hLsBLyiByySe4lhzHJOCA2HlhOnPJ"
    "2Bwp1DFMBu63eT+9NCixHIghjxLXYHYxeD8yJcRWVj69rIx45AjKLahiKanmo9WQTdKQPp"
    "Ut7c9OObzQ+7B7REh05JeJPJRiCEg+NeWUobagFB8rBFXdfvuLjOF0eqWJjOE4qyK+XA9H"
    "NyenUnEEdxhFMX4XZ3Q6Wk1caD4vSV6kwcXv7dXI6U4vCV2JMouhHEicNfIqKavR9HWSL9"
    "N2d/EBCKoLlebC08JTVYl7TIGn7vZyRJ528Vcs9PR7xlbs1S3O1ebA8P95odWehLQnIXU4"
    "CTlmmhhAhuxlXo6IS0oTBFB12uTQoOTwD2T5Krg4P6Rc2hSxBSm2RgWIcfVmAjzd68PO05"
    "IPO2VZ5qMRSjiM9qAO8Y/ZdFLwtYhyyd7GIZsb/xoYBTVNtptifmK85Xc52WubzF2aeIC4"
    "y6nw5cbhE8vmJ9o/Fe4="
)
