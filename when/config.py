from typing import List

from pydantic import BaseSettings
from tzlocal import get_localzone

from .model import Location


class Settings(BaseSettings):
    default_tz: str = str(get_localzone())
    locations: List[Location] = [
        Location(key="klu", description="Klagenfurt, Austria", tz="Europe/Vienna"),
        Location(key="els", description="El Segundo, USA", tz="America/Los_Angeles"),
        Location(key="sin", description="Singapore", tz="Asia/Singapore"),
        Location(key="utc", description="Greenwich, UK", tz="UTC"),
    ]

    def get(self):
        """."""
        return self

    class Config:
        env_prefix = "when_config_"


settings = Settings()
