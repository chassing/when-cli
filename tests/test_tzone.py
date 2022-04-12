from datetime import date
from datetime import datetime as dt
from datetime import time
from zoneinfo import ZoneInfo

import pytest
from when.when import parse_time_string, split_time_string

DATES = [
    ("", date.today()),
    ("30.09.79", date(1979, 9, 30)),
    ("30.09.1979", date(1979, 9, 30)),
    ("1979.09.30", date(1979, 9, 30)),
    ("1979-09-30", date(1979, 9, 30)),
    ("30. September", date.today().replace(month=9, day=30)),
    ("30. Sep", date.today().replace(month=9, day=30)),
    ("30th Sep", date.today().replace(month=9, day=30)),
    ("30. September 1979", date(1979, 9, 30)),
    ("30. Sep 1979", date(1979, 9, 30)),
    ("30th Sep 1979", date(1979, 9, 30)),
]
TIMES = [
    # 24
    ("6:5", time(6, 5)),
    ("6:05", time(6, 5)),
    ("6:15", time(6, 15)),
    ("20:15", time(20, 15)),
    # 12
    ("2pm", time(14, 00)),
    ("2am", time(2, 00)),
    ("2:0pm", time(14, 00)),
    ("2:00pm", time(14, 00)),
    ("2:3am", time(2, 3)),
    ("2:03am", time(2, 3)),
    ("2:30am", time(2, 30)),
]

TIMEZONES = [
    "",
    "America/Los_Angeles",
    "Europe/Berlin",
]


@pytest.mark.parametrize("datum_str, datum", DATES)
@pytest.mark.parametrize("t1_str, t1", TIMES)
@pytest.mark.parametrize("t2_str, t2", TIMES)
@pytest.mark.parametrize("tz", TIMEZONES)
@pytest.mark.parametrize("times_sep", [" to ", " TO ", " - "])
@pytest.mark.parametrize("tz_sep", [" @", " IN ", " in "])
def test_split_time_string(datum_str, datum, t1_str, t1, t2_str, t2, tz, times_sep, tz_sep):
    time_string = t1_str
    t1_test = t1_str
    t2_test = t2_str

    if datum_str:
        time_string += " " + datum_str
        t1_test += " " + datum_str
    if t2_str:
        time_string += times_sep + t2_str
        if datum_str:
            time_string += " " + datum_str
            t2_test += " " + datum_str
    if tz:
        time_string += tz_sep + tz
    assert split_time_string(time_string) == (t1_test, t2_test, tz)


@pytest.mark.parametrize("datum_str, datum", DATES)
@pytest.mark.parametrize("uhrzeit_str, uhrzeit", TIMES)
@pytest.mark.parametrize("tz", TIMEZONES)
def test_parse_time_string(datum_str, datum, uhrzeit_str, uhrzeit, tz):
    if not tz:
        # ignore empty tz
        return
    assert parse_time_string(datum_str + " " + uhrzeit_str, tz).datetime == dt.combine(
        datum, uhrzeit, tzinfo=ZoneInfo(tz)
    )
    assert parse_time_string(uhrzeit_str + " " + datum_str, tz).datetime == dt.combine(
        datum, uhrzeit, tzinfo=ZoneInfo(tz)
    )
