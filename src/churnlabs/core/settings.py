from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Database credentials loaded from environment variables.
    """

    db_host: str | None = None
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_sslmode: str = "require"
    db_channel_binding: str = "prefer"

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

    @property
    def db_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}/{self.db_name}"
            f"?sslmode={self.db_sslmode}"
            f"&channel_binding={self.db_channel_binding}"
        )
