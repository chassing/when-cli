from typing import List

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from pydantic import BaseModel, BaseSettings, validator


class Location(BaseModel):
    name: str
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
    default_tz: str = "UTC"
    locations: List[Location] = [
        Location(name="klu", description="Klagenfurt, Austria", tz="Europe/Vienna"),
        Location(name="els", description="El Segundo, USA", tz="America/Los_Angeles"),
        Location(name="sin", description="Singapore", tz="Asia/Singapore"),
        Location(name="utc", description="Greenwich, UK", tz="UTC"),
    ]

    def get(self):
        """."""
        return self

    def location_by_name(self, name):
        for location in self.locations:
            if location.name.lower() == name.lower():
                return location
        raise KeyError(f"{name} not found")

    class Config:
        env_prefix = "when_config_"


settings = Settings()
