import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = ""

    @property
    def cors_origins(self) -> List[str]:
        """Return ALLOWED_ORIGINS as a cleaned list."""
        if not self.ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = {
        "env_file": ".env" if not os.getenv("RENDER") else None,
        "case_sensitive": True,
        "extra": "ignore",
    }


settings = Settings()
