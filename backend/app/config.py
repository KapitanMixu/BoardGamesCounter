from urllib.parse import urlparse, uses_netloc

for _scheme in ("postgres", "postgresql"):
    if _scheme not in uses_netloc:
        uses_netloc.append(_scheme)

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_db_connection(database_url: str) -> str | dict:
    if database_url.startswith("sqlite"):
        return database_url

    use_ssl = "sslmode=require" in database_url or "ssl=" in database_url
    clean = (
        database_url
        .replace("postgresql://", "postgres://", 1)
        .split("?")[0]
    )
    p = urlparse(clean)
    creds: dict = {
        "host": p.hostname,
        "port": p.port or 5432,
        "user": p.username,
        "password": p.password,
        "database": p.path.lstrip("/"),
    }
    if use_ssl:
        creds["ssl"] = True
    return {
        "engine": "tortoise.backends.asyncpg",
        "credentials": creds,
    }


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
        self.TORTOISE_ORM = {
            "connections": {"default": _parse_db_connection(self.DATABASE_URL)},
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
