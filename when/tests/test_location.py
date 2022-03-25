from zoneinfo import ZoneInfo

import pytest
from when.when import location_by_key


@pytest.mark.parametrize(
    "key, tz",
    [
        # defaults - mix upper/lower-case
        ("klu", ZoneInfo("Europe/Vienna")),
        ("Klu", ZoneInfo("Europe/Vienna")),
        ("els", ZoneInfo("America/Los_Angeles")),
        ("ELS", ZoneInfo("America/Los_Angeles")),
        # airports - IATA 3-letter code - mix upper/lower-case
        ("lax", ZoneInfo("America/Los_Angeles")),
        ("Lax", ZoneInfo("America/Los_Angeles")),
        ("jFk", ZoneInfo("America/New_York")),
        ("TXL", ZoneInfo("Europe/Berlin")),
        # airports - ICAO 4-alphanumeric code - mix upper/lower-case
        ("lowk", ZoneInfo("Europe/Vienna")),
        ("lOWk", ZoneInfo("Europe/Vienna")),
        # TZ names
        ("Europe/Vienna", ZoneInfo("Europe/Vienna")),
        ("Asia/Singapore", ZoneInfo("Asia/Singapore")),
    ],
)
def test_location_by_key(key, tz):
    assert location_by_key(key).tz == tz
