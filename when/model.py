from pydantic import BaseModel, validator

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo


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


class Zone(BaseModel):
    name: str = ""
    description: str = ""
    tz: str
    offset: int
    times: list[str]
