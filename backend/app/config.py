from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite://./db.sqlite3"

    TORTOISE_ORM: dict = {
        "connections": {"default": DATABASE_URL},
        "apps": {
            "models": {
                "models": [
                    "app.models.game",
                    "app.models.player",
                    "app.models.session",
                    "aerich.models",
                ],
                "default_connection": "default",
            }
        },
    }


settings = Settings()
