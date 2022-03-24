try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from datetime import datetime
from typing import Dict, List

import arrow
from dateutil.parser import parse

from .config import settings


def when(time_string, locations) -> Dict:
    locations = [s.lower() for s in locations] or [s.name for s in settings.locations]
    tzone = Tzone(time_string=time_string)
    zones = []
    for name in locations:
        location = settings.location_by_name(name)
        zones.append(
            dict(
                name=location.name,
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
        try:
            tz = settings.location_by_name(tz).tz
        except KeyError:
            # not a custom location key ... treat as timezone string
            if tz not in zoneinfo.available_timezones():
                raise zoneinfo.ZoneInfoNotFoundError(tz)

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
        try:
            t1 = t2 = ""
            tz = "UTC"
            # TZ
            if "@" in time_string:
                time_string, tz = time_string.split("@")
            if " in " in time_string:
                time_string, tz = time_string.split(" in ")

            # T1 - T2
            t1 = time_string
            if "to" in time_string:
                t1, t2 = time_string.split("to")

            return t1.strip(), t2.strip(), tz.strip()
        except Exception as e:  # noqa
            raise Exception(f"can't parse {time_string}: {e}")

    def parse_time_string(self, time_string, tz):
        return arrow.get(parse(time_string, ignoretz=True), tz)
