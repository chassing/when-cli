from typing import List

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from pydantic import BaseModel, BaseSettings, validator
from tzlocal import get_localzone


class Location(BaseModel):
    key: str
    description: str
    tz: str

    @validator("tz")
    def tz_as_zoneinfo(cls, v):
        try:
            return zoneinfo.ZoneInfo(v)
        except:  # noqa
            raise ValueError(f"Unknown timezone '{v}'")


class Settings(BaseSettings):
    debug: bool = False
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
