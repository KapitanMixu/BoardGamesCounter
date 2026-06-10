from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" ADD "duration_type" VARCHAR(20);
        ALTER TABLE "games" ADD "duration_minutes" INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "games" DROP COLUMN "duration_type";
        ALTER TABLE "games" DROP COLUMN "duration_minutes";"""


MODELS_STATE = (
    "eJztmmFT2jAYx79Kr6/0ju2Q6eb5DhQ3NgVP2Oa52/VCG0tuaYJJOuUc332XtCVtaDvqUO"
    "HsK+BJnib5JXmefxMe7IB6EPO3H0EA7SPrwSbRl4y9YdlgOtVWaRBgjFVFHwRQWcCYCwZc"
    "YR9ZNwBz2LBsD3KXoalAlNhHFgkxlkbqcsEQ8bUpJOg2hI6gPhQTyOwj68fPhmUj4sF7yJ"
    "Of01/ODYLYy/QTebJtZXfEbKpsPSJOVUXZ2thxKQ4DoitPZ2JCyaI2IkJafUggAwLKxwsW"
    "yu7L3sXDTEYU9VRXibqY8vHgDQixSA13RQYuJZIfIkIO+MH2ZStvWnv7H/YP373fP2xYtu"
    "rJwvJhHg1Pjz1yVAT6I3uuyoEAUQ2FUXNTn0vkjieA5aNL6hvwuGAmvARVGb3EoPHpJbMm"
    "fgG4dzAkvphIaAcHJbS+tS+PP7Uvd1oHB7tyNJQBN1rc/bioFZVJpKktgogzxWAGGa+wBg"
    "2vfy/GdfFsvfRiTJED948hl/V6PnL7m0POCxmQfXACREIBq+DLc30UwzjSPedmfiqKauAV"
    "ouCS46PC4QsAzEbD5irBsFkcC5tmKHQZlMN1gFimeQIEFCiA+USzngZOL3Z9m3zZ0FzDIP"
    "AGBM/iuS2hO+qdd4ej9vmFHEnA+S1WiNqjrixpKevMsO68N2Zi8RDre2/0yZI/retBv6sI"
    "Ui58plrU9UbXtuwTCAV1CL1zgJdSLIk1ATOXWusm1loL8TUG7q87wDwnU6JXAIecI0pyAl"
    "In9jz9cgmx2j05M52Sm8PoSZs51fHUamsy5ZIRbdEiastFQSswLYAAX/Vati1biqlcqKSX"
    "J8/jklKBnkqZtUTfvKxUS/QnlOh1Xnr1ecmlstX/ykpD+YzNnOIXyUfpLF1wZpRK4uVHR0"
    "5aONT5aZvykxIWj4mtGcc6tG5AaE3nTEJzzxVG8L5gSywctuRluGyuulejzDQl6mLnvH21"
    "m5mqs0H/Y1I9pUaOzwYdQ4SoMFcpyKQ8nu+U6+WDzVKCzzJcBnhKGUQ++QJnimOPcAGImy"
    "eCjeuM7UnkDctm4G6RtdJLgxLHgxiK6LWgPTxun3RtBbEWRc8viiIeOXJoAapYCOn5qBXQ"
    "VikgqlpanZ12eKUn73eIkOjAyog8lGIISD417WRQG1OKnyoEVd1+q4uMzmBwlhEZnZ6pIr"
    "6ed7qXO3tKcfBbjKIYv4wzOturJi4yPq9JXqTBxW+d1chlnV4TuhJlFkNZkzjbysN/U6Nl"
    "10m+TFvexWsgqK8DthdeJjxVlbhPKfDakCF3kqfw4pJSiQd0nVribZHE+w1ZfngrvodJud"
    "RXMQuQcmtUgBhX306Ae81V/mGx1yz+i4UqM+6yKBEw2oNZiJ+Hg37BJZZ2MY9ZkSusPxZG"
    "fENVy7yYnxxv+SGdeR5nHJLKB8hDugoXSutPLPO/0Uz0Qw=="
)
