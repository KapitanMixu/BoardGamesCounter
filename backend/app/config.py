from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite://./db.sqlite3"
    TORTOISE_ORM: dict = {}

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "changeme"

    @model_validator(mode="after")
    def build_tortoise_orm(self) -> "Settings":
        self.TORTOISE_ORM = {
            "connections": {"default": self.DATABASE_URL},
            "apps": {
                "models": {
                    "models": [
                        "app.models.game",
                        "app.models.player",
                        "app.models.session",
                        "app.models.expansion",
                        "aerich.models",
                    ],
                    "default_connection": "default",
                }
            },
        }
        return self


settings = Settings()
