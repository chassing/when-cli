import pytest
from when.when import when


@pytest.mark.parametrize(
    "time_string, location_keys, times_count",
    [
        ("6:00", ["klu"], 1),
        ("6:00 in LAX", ["klu"], 1),
        ("6:00 - 10:00", ["sin", "klu"], 5),
        ("6:00 - 10:00 in KLU", ["sin", "klu"], 5),
        ("1. January 6:00 - 1st January 8:00", ["sin", "klu"], 3),
        ("2nd January 6:00 - 3rd January 8:00 @LAX", ["sin", "klu"], 24 + 3),
    ],
)
def test_when(time_string, location_keys, times_count):
    """Full integration test."""
    zones = when(time_string, location_keys)
    assert len(zones) == len(location_keys)
    for i, loc in enumerate(location_keys):
        assert zones[i].name == loc
        assert zones[i].tz
        assert len(zones[i].times) == times_count
