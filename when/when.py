import json
import zoneinfo
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import airportsdata
import arrow
from dateutil.parser import parse

from .config import settings
from .model import Location, Zone


def location_by_key(key: str) -> Location:
    """Get a location by key/name"""
    # user self defined locations first
    for location in settings.locations:
        if location.key.lower() == key.lower():
            return location

    # IATA 3-letter code
    # ICAO 4-alphanumeric code or FAA/TD LID prefaced by “K”
    for code in ["IATA", "ICAO"]:
        airports = airportsdata.load(code)
        if key.upper() in airports:
            entry = airports[key.upper()]
            return Location(key=key, description=f"{entry['name']}, {entry['country']}", tz=entry["tz"])

    # city name?
    cities = json.loads((Path(__file__).parent / "data" / "cities.json").read_text())
    try:
        city = cities[key.lower()]
        return Location(key="", description=f"{city['name']}, {city['country']}", tz=city["tz"])
    except KeyError:
        pass

    # ok than it must be a TZ name
    if key not in zoneinfo.available_timezones():
        raise zoneinfo.ZoneInfoNotFoundError(key)

    return Location(key="", description="", tz=key)


def when(time_string: str, location_keys: list[str]) -> list[Zone]:
    tzone = Tzone(time_string=time_string)
    zones = []
    for key in location_keys:
        location = location_by_key(key)
        zones.append(
            Zone(
                name=location.key,
                description=location.description,
                tz=str(location.tz),
                offset=tzone.utc_offset(location.tz),
                times=[dt.isoformat() for dt in tzone.convert(tz=location.tz)],
            )
        )
    return zones


class Tzone:
    def __init__(self, time_string: str) -> None:
        self.time_string = time_string

        t1, t2, tz = split_time_string(self.time_string)
        tz = location_by_key(tz if tz else settings.default_tz).tz

        self.t1 = parse_time_string(t1, tz)
        self.t2 = parse_time_string(t2, tz) if t2 else self.t1

    def convert(self, tz: ZoneInfo | str) -> list[datetime]:
        t1 = self.t1.to(tz)
        t2 = self.t2.to(tz)
        return [t.datetime for t in arrow.Arrow.range("hour", t1, t2)]

    def utc_offset(self, tz) -> int:
        if offset := arrow.now(tz).utcoffset():
            return int(offset.total_seconds())
        return 0


def split_time_string(time_string: str) -> tuple[str, str, str]:
    """Split time range string into start, end, tz."""
    t1 = t2 = tz = ""
    try:
        # TZ
        for sep in ["@", " in ", " IN "]:
            if sep in time_string:
                time_string, tz = time_string.split(sep)
                break

        # T1 - T2
        t1 = time_string
        for sep in [" to ", " TO ", " - "]:
            if sep in time_string:
                t1, t2 = time_string.split(sep)
                break

        return t1.strip(), t2.strip(), tz.strip()
    except Exception as e:  # noqa
        raise Exception(f"can't parse {time_string}")


def parse_time_string(time_string: str, tz: ZoneInfo | str) -> arrow.Arrow:
    return arrow.get(parse(time_string, ignoretz=True), tz)
