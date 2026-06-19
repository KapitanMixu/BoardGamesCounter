from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" ADD "thumbnail_url" VARCHAR(500);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" DROP COLUMN "thumbnail_url";"""


MODELS_STATE = (
    "eJztm11z2jgUhv8Kw1U6k+0ENmk7eweEtGwTyADZdtrpeIQtjCe25NpyCdvhv68k29gSso"
    "spH2bxXTjSsaVHH+c9kvOz7mAD2v7r98CB9b9qP+so/EOwX9bqwHUTKzMQMLF5RZPW4BYw"
    "8YkHdEKNU2D7kJoM6Oue5RILI2pFgW0zI9ZpRQuZiSlA1vcAagSbkMygRwu+fqNmCxnwhT"
    "48+uk+a1ML2obQTstg7+Z2jSxcbushcscrsrdNNB3bgYOSyu6CzDBa1bYQYVYTIugBAtnj"
    "iRew5rPWRd2MexS2NKkSNjHlY8ApCGyS6u6GDHSMGD/aGp930GRv+aPZuH57/e7PN9fvaB"
    "XekpXl7TLsXtL30JET6I/rS14OCAhrcIwJNxQNrEiuMwOeGl1cX4JHmyzDi1Hl0YsNCb5k"
    "yuyInwNeNBsik8wYtJubHFr/tIadD63hBa31ivUG02kcTu5+VNQMyxjS1BKxkObaYAE9v8"
    "AclLx+PRl3xbN57MmYIkfHZgtyotfhyF2Xh5wR0M7RNmh0GgUEFsGnct2KYbTTHXIx74si"
    "73iBXXDNcavt8AgAxd3wapPN8Cp7L7ySt8KJaWqBZxdBmXI5SYg3V5tQpLUyMfIykSOZBc"
    "4EAcsuSnPNsWIaM9U9yHqsAbIO9JaWEMuBaqiip0TUiFxfx3+UVAfRPhgDZC+i4c3hO+49"
    "dEfj1sMj64nj+99tjqg17rKSJrcuJOvFG2koVg+pfeqNP9TYz9qXQb/LCWKfmB5/Y1Jv/K"
    "XO2gQCgjWE5xowUmo6tsZgliwPmD6nFC0zTID+PAeeoQklyQzwoe9TbIpg2Y487z4Ooc13"
    "dsVIp1KhUfikcg71Mp6/sTUZ8oQFfHEB2gGNbvycE2PB5gtu4qwZtF7kNB3ZAhAweavZu9"
    "mbIiaPXJzWFWl0VHKZl0inpG2VSpdPPVap9B5T6SpGn32M1rGnSmeLxKQRe0Y5h/go8Sit"
    "WDLOdlOCJv+IV0uLqCo+VfGppCnkXsITl2bbRCfBsQpOJQhO6WFFWHmCOoYvGZvKyuFElk"
    "beWHU/j4VhihfAxUPr8ythqO4H/fdx9dSC6dwP2tI64YGi0Dad8jjcef7xt+s1iSQyXAd4"
    "R5WNZaKPcME59miLANJV27R0cVs+fllSiJo9MF/F/fTUoN2jnYIkDFytUad1260vK1l5HF"
    "kZ8lAIyhWobCmZjEelIcu2KeVpSBfzN23OLnE40zvGuYVQeOQn7TwY2xAgNbXESaI2oV77"
    "2oKKLr/NRUZ7MLgXREa7J6uIp4d2d3jR4IqDVrLCPX4dZ3g6WkxcCD7nJC/S4KK8vRg50e"
    "mc0OUoMz85K9mBODvJqyRZo4nzRC3T1lfxDggmFyqnC0/YnopK3H0KvORuTyHyhIu/bKEn"
    "3jNWYq9s+1ye2KsutH77xLA6CalOQspwErLPMPHJ8me25ZMegY4qUgjlucFiHtXUqPx3qo"
    "BRBYySLdTDXDEh/1+Ii374KfudyM3EAb77rL5J3g3H6pZsx7dkE0gjnetZukrd2BhkYBXd"
    "JLZT5ndqdG8HT+37bu1x2O30Rr1BX7wg5oXiseCw27rPhKn5M+wWWu3rricyYw8Qj/B0Cj"
    "0KK0CKjx4yNZHkdaZH/+GcClxjy28aVf47+HikVGu/TN+KxN3O/Vik+kT1f/QVUIFPVPeZ"
    "QbcgXemzuiJ3jkou87JmkNSpsuXShYPsbPkH9NT3SNlSJeVS5cwrkGxpFIAYVT9NgI2NUr"
    "tGTmrXUPxrJEYEqgTe36NBPyOYJS4SyCdEO/jVsHRyWWOHed/KiTWHIut1frYnJ3ZSNGIP"
    "aKsOtQ8ZXpb/Ab5AZw0="
)
