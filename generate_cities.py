"""
Generate city to time zone mapping file.

Based on https://github.com/mitsuhiko/when-data
Thank you Armin :)
"""
from pathlib import Path

import click
from pydantic import BaseModel


class Location(BaseModel):
    name: str
    country: str
    tz: str
    sort_key: tuple

    class Config:
        fields = {"sort_key": {"exclude": True}}


class Locations(BaseModel):
    __root__: dict[str, Location] = {}


DATA_PATH = Path(__file__).parent / "dump"

# geonames
GEONAMEID = 0
NAME = 1
ASCIINAME = 2
ALTERNATENAMES = 3
LATITUDE = 4
LONGITUDE = 5
FEATURE_CLASS = 6
FEATURE_CODE = 7
COUNTRY_CODE = 8
CC2 = 9
ADMIN1_CODE = 10
ADMIN2_CODE = 11
ADMIN3_CODE = 12
ADMIN4_CODE = 13
POPULATION = 14
ELEVATION = 15
DEM = 16
TIMEZONE = 17
MODIFICATION_DATE = 18


memoized = {}


def find_locations() -> Locations:
    locations = Locations()
    cities = DATA_PATH / "cities15000.txt"

    with click.progressbar(length=cities.stat().st_size, label="[1] Finding cities", update_min_steps=10) as pb:
        for line in cities.read_bytes().splitlines():
            pb.update(len(line))
            line = line.rstrip()
            if line.startswith(b"#"):
                continue
            pieces = line.split(b"\t")

            tz = pieces[TIMEZONE]
            if not tz:
                continue

            feature_code = pieces[FEATURE_CODE]
            if feature_code in (b"PPLA", b"PPLC") or feature_code[:1]:
                name = pieces[ASCIINAME].decode("utf-8")
                locations.__root__[name.lower()] = Location(
                    name=name,
                    country=pieces[COUNTRY_CODE].decode("utf-8"),
                    tz=tz.decode("utf-8"),
                    sort_key=(
                        pieces[FEATURE_CODE] != b"PPLC",
                        pieces[COUNTRY_CODE] != b"US",
                        -int(pieces[POPULATION].decode("utf-8")),
                    ),
                )

    return locations


@click.command()
def main():
    locations = find_locations()
    click.echo("[2] Writing cities")
    Path("when/when/data/cities.json").write_text(locations.json())
    click.echo(f"[3] {len(locations.__root__)} written")


if __name__ == "__main__":
    main()
