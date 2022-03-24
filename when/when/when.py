try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from datetime import datetime
from typing import Dict, List

import airportsdata
import arrow
from dateutil.parser import parse

from .config import Location, settings


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

    # ok than it must be a TZ name
    if key not in zoneinfo.available_timezones():
        raise zoneinfo.ZoneInfoNotFoundError(key)

    return Location(key="", description="", tz=key)


def when(time_string, location_keys) -> Dict:
    tzone = Tzone(time_string=time_string)
    zones = []
    for key in location_keys:
        location = location_by_key(key)
        zones.append(
            dict(
                name=location.key,
                description=location.description,
                tz=str(location.tz),
                offset=tzone.utc_offset(location.tz),
                times=[dt.isoformat() for dt in tzone.convert(tz=location.tz)],
            )
        )
    return zones


class Tzone:
    def __init__(self, time_string) -> None:
        self.time_string = time_string
        t1, t2, tz = self.split_time_string(time_string)
        if not tz:
            tz = settings.default_tz
        else:
            tz = location_by_key(tz).tz

        self.t1 = self.parse_time_string(t1, tz)
        self.t2 = self.parse_time_string(t2, tz) if t2 else self.t1

    def convert(self, tz) -> List[datetime]:
        t1 = self.t1.to(tz)
        t2 = self.t2.to(tz)
        return [t.datetime for t in arrow.Arrow.range("hour", t1, t2)]

    def utc_offset(self, tz):
        return arrow.now(tz).utcoffset().total_seconds()

    def split_time_string(self, time_string):
        """Split time range string into start, end, tz."""
        # TODO replace with regex
        try:
            t1 = t2 = tz = ""
            # TZ
            if "@" in time_string:
                time_string, tz = time_string.split("@")
            if " in " in time_string.lower():
                time_string, tz = time_string.split(" in ")

            # T1 - T2
            t1 = time_string
            if " to " in time_string.lower():
                t1, t2 = time_string.split("to")

            return t1.strip(), t2.strip(), tz.strip()
        except Exception as e:  # noqa
            raise Exception(f"can't parse {time_string}")

    def parse_time_string(self, time_string, tz):
        return arrow.get(parse(time_string, ignoretz=True), tz)
