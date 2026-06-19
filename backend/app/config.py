from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite://./db.sqlite3"
    TORTOISE_ORM: dict = {}

    BGG_API_TOKEN: str = ""

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "changeme"
    INVITE_CODE: str = "change-this-invite-code"

    @model_validator(mode="after")
    def build_tortoise_orm(self) -> "Settings":
        db_url = (
            self.DATABASE_URL
            .replace("postgresql://", "postgres://", 1)
            .replace("sslmode=require", "ssl=require")
        )
        self.TORTOISE_ORM = {
            "connections": {"default": db_url},
            "apps": {
                "models": {
                    "models": [
                        "app.models.game",
                        "app.models.player",
                        "app.models.session",
                        "app.models.expansion",
                        "app.models.wishlist",
                        "app.models.user",
                        "aerich.models",
                    ],
                    "default_connection": "default",
                }
            },
        }
        return self


settings = Settings()
