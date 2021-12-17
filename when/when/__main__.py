import locale
from datetime import datetime as dt
from typing import List
from urllib.parse import urljoin

import httpx
import rich.box
import typer
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text

console = Console()
locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_TIME, "")

SITES = [
    ("auc", "Austin"),
    ("brs", "Bristol"),
    ("blr", "Bengalore"),
    ("els", "El Segundo"),
    ("kac", "Kozoji"),
    ("sin", "Singapore"),
    ("tdc", "Andover"),
    ("vih", "Villach"),
    ("klu", "Klagenfurt"),
]
INFO_COLS = [
    ("date", "Date column"),
    ("time", "Time column"),
    ("tz", "Timezone column"),
]


def complete_sites(ctx: typer.Context, incomplete: str):
    for name, help_text in SITES:
        if name.startswith(incomplete) and name not in ctx.params.get("sites", []):
            yield (name, help_text)


def complete_info_columns(ctx: typer.Context, incomplete: str):
    for name, help_text in INFO_COLS:
        if name.startswith(incomplete) and name not in ctx.params.get("info-columns", []):
            yield (name, help_text)


def main(
    time_string: str,
    sites: List[str] = typer.Option(
        None,
        "--sites",
        "-s",
        help="Use IFX site abbreviation. Can be given multiple times.",
        autocompletion=complete_sites,
        envvar="WHEN_SITES",
    ),
    url: str = typer.Option("https://when.icp.infineon.com", "--url", "-u", help="WHEN API Url."),
    table_color: str = "deep_sky_blue2",
    table_padding: int = 0,
    header_color: str = "green",
    date_format: str = "%x",
    date_color: str = "deep_pink4",
    time_format: str = "%H:%M",
    time_color: str = "spring_green3",
    tz_format: str = "%Z",
    tz_color: str = "grey27",
    info_columns: List[str] = typer.Option(
        [k for k, v in INFO_COLS],
        "--info-columns",
        "-i",
        help="Display these columns in this order.",
        autocompletion=complete_info_columns,
    ),
):
    """Convert your given time string into different timezones.

    TIME_STRING must be in the following format:

    [DATE] [TIME] [to [DATE] [TIME]] [in SITE]

    ---- DATE ----


    * YYYY-MM-DD, YYYY.MM.DD (e.g. 2021-09-30)

    * Day Month [Year] (e.g. 30. September) - German locale

    * [Year] Month Day (e.g. September 30th) - English locale

    * Month can be an abbreviation too (e.g Sep vs September)

    * Day can be english or german local (e.g. 1st vs 1.)

    ---- TIME ----

    * HH:MM (e.g. 16:30) - 24 hours format

    * HH:MM am/pm (e.g. 2:30am) - 12 hours format

    ---- RANGE ----

    * use "to" keyword followed by another date/time argument to span a time range

    ---- TIMEZONE ----

    * use "in" keyword followed by IFX sites abbreviation to specify a timezone

    * e.g. "in ELS"

    ---- EXAMPLES ----

    * 30. September 17:00 to Oct 1st 2:3pm in ELS

    ---- COLORS ----

    See https://rich.readthedocs.io/en/latest/appendix/colors.html for all available color codes.
    """
    r = httpx.get(urljoin(url, "/tz"), params={"time_string": time_string, "sites": sites})
    zones = sorted(r.json(), key=lambda x: x["offset"])
    table = Table(title="Zones", style=table_color, box=rich.box.ROUNDED, padding=table_padding)
    for zone in zones:
        table.add_column(Text(f"{zone['name']}\n{zone['tz']}", justify="center", style=header_color))

    p_times = None
    for times in zip(*[zone["times"] for zone in zones]):
        row = []
        times = [dt.fromisoformat(t) for t in times]

        for i, t in enumerate(times):
            r = Text()
            date_col = Text(
                t.strftime(date_format),
                style=Style(color=date_color, bgcolor="yellow" if p_times and p_times[i].date() < t.date() else None),
            )

            time_col = Text(t.strftime(time_format), style=time_color)
            tz_col = Text(t.strftime(tz_format), style=tz_color)

            for i in info_columns:
                if i == "date":
                    r += date_col
                if i == "time":
                    r += time_col
                if i == "tz":
                    r += tz_col
                r += " "
            row.append(r)

        p_times = times
        table.add_row(*row)

    console.print(table)


if __name__ == "__main__":
    typer.run(main)
