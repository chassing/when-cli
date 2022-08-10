import locale
import sys
import zoneinfo
from datetime import datetime as dt
from typing import List

import rich.box
import rich_click.rich_click
import rich_click.typer as typer
from rich import print
from rich.markdown import Markdown
from rich.style import Style
from rich.table import Table
from rich.text import Text

from when import rich_typer
from when.config import settings
from when.when import when

rich_click.rich_click.USE_RICH_MARKUP = True
rich_click.rich_click.SHOW_ARGUMENTS = True
rich_click.rich_click.GROUP_ARGUMENTS_OPTIONS = False
rich_click.rich_click.SHOW_METAVARS_COLUMN = True
rich_click.rich_click.FOOTER_TEXT = rich_typer.blend_text(
    "Made with ♥ by https://github.com/chassing/when-cli", (32, 32, 255), (255, 32, 255)
)
rich_click.rich_click.STYLE_FOOTER_TEXT = "#D920FF"

locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_TIME, "")


INFO_COLS = [
    ("date", "Date column"),
    ("time", "Time column"),
    ("tz", "Timezone column"),
]

VERSION = "2.0"

SHORT_USAGE = """

# Usage

```
$ when-cli [OPTIONS] TIME_STRING
```

# TIME_STRING Syntax

[`DATE`] `TIME` [to [`TO_DATE`] `TO_TIME`] [in `TIMEZONE_OR_LOCATION`]

* `DATE` is the start date. *[Default: **today**]*
* `TIME` is the start time. **required**
* `TO_DATE` is the end date. *[Default: **end date = start date**]*
* `TO_TIME` is the end time. *[Default: **end time = start time**]*
* `TIMEZONE_OR_LOCATION` interpret dates and times in this timezone. *[Default: **host timezone**]*

## `DATE`

* YYYY-MM-DD, YYYY.MM.DD (e.g. 2021-09-30) - English locale
* DD.MM.YYYY (e.g. 30.09.1979) - German locale
* Day Month [Year] (e.g. 30. September) - German locale
* [Year] Month Day (e.g. September 30th) - English locale
* Month can be an abbreviation too (e.g Sep vs September)
* Day can be english or german local (e.g. 1st vs 1.)

## `TIME`

* HH:MM (e.g. 16:30) - 24 hours format
* HH:MM am/pm (e.g. 2:30am) - 12 hours format

## `TIMEZONE_OR_LOCATION`

* City name
    * Los Angeles (US)
    * Erfurt (Germany)
    * Torrance (US)
* timezones
    * Europe/Vienna
    * UTC
    * America/Los_Angeles
* airport codes
    * klu (Klagenfurt Airport)
    * lax (Los Angeles International Airport)
    * KJFK (John F Kennedy International Airport)
* self defined locations via WHEN_CONFIG_LOCATIONS

# Examples

```shell
$ when-cli "07.05.2022 06:15 in PMI" -l lax -l Berlin

```

```shell
$ when-cli "30. September 17:00 to Oct 1st 2:3pm in LAX"
```

---
Complete usage guide can be found at [https://github.com/chassing/when-cli/blob/master/USAGE.md](https://github.com/chassing/when-cli/blob/master/USAGE.md)
"""


def complete_info_columns(ctx: typer.Context, incomplete: str):
    for name, help_text in INFO_COLS:
        if name.startswith(incomplete) and name not in ctx.params.get("info-columns", []):
            yield (name, help_text)


def show_usage(value: bool):
    if not value:
        return
    print(Markdown(SHORT_USAGE))
    sys.exit(0)


def main(
    time_string: str,
    locations: List[str] = typer.Option(
        [loc.key for loc in settings.locations],
        "--locations",
        "-l",
        help="Display these locations. Can be given multiple times.",
        metavar="LOCATION_KEY",
        envvar="WHEN_LOCATIONS",
    ),
    table_color: str = typer.Option(
        "deep_sky_blue2", envvar="WHEN_TABLE_COLOR", metavar="COLOR", help="Table border color"
    ),
    row_padding: int = typer.Option(0, envvar="WHEN_ROW_PADDING", metavar="INTEGER", help="Row padding"),
    header_color: str = typer.Option("green", envvar="WHEN_HEADER_COLOR", metavar="COLOR", help="Header font color"),
    date_format: str = typer.Option("%x", envvar="WHEN_DATE_FORMAT", metavar="FORMAT_DIRECTIVE", help="Date format"),
    date_color: str = typer.Option("deep_pink4", envvar="WHEN_DATE_COLOR", metavar="COLOR", help="Date font color"),
    time_format: str = typer.Option("%H:%M", envvar="WHEN_TIME_FORMAT", metavar="FORMAT_DIRECTIVE", help="Time format"),
    time_color: str = typer.Option("spring_green3", envvar="WHEN_TIME_COLOR", metavar="COLOR", help="Time font color"),
    tz_format: str = typer.Option("%Z", envvar="WHEN_TZ_FORMAT", metavar="FORMAT_DIRECTIVE", help="Timezone format"),
    tz_color: str = typer.Option("grey27", envvar="WHEN_TZ_COLOR", metavar="COLOR", help="Timezone font color"),
    info_columns: List[str] = typer.Option(
        [k for k, v in INFO_COLS],
        "--info-columns",
        "-i",
        help="Display these columns in this order.",
        autocompletion=complete_info_columns,
        envvar="WHEN_INFO_COLUMNS",
        metavar="COL_NAME",
    ),
    usage: bool = typer.Option(
        None, is_flag=True, is_eager=True, expose_value=False, callback=show_usage, help="Show usage."
    ),
):
    """[b yellow]when-cli[/] is a timezone conversion tool. It takes as input a natural time string, can also be a time range,
    and converts it into different timezone(s) at specific location(s).

    \b
    ---
    Examples:

    \b
    $ when-cli "30. September 17:00 to Oct 1st 2:3pm in LAX"
    $ when-cli "17:00 in Europe/Berlin" -l lax -l klu

    \b
    [b white]Syntax[/]
    The required argument ([b cyan]TIME_STRING[/]) is basically a human readable date time string in this syntax:
    [[b green]DATE[/]] [b red]TIME[/] [TO [b green]TO_DATE[/] [red]TO_TIME[/]] [IN [b blue]TIMEZONE_OR_LOCATION[/]]

    \b
    [b white]Usage[/]
    Get detailed information and more examples:
    $ when-cli --usage

    \b
    [b white]Strftime[/]
    Standard datetime format codes [link]https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes[/]

    \b
    [#2020FF]C[/][#4520FF]o[/][#6A20FF]l[/][#8F20FF]o[/][#B420FF]r[/][#D920FF]s[/]
    See [link]https://rich.readthedocs.io/en/latest/appendix/colors.html[/] for all available color codes.
    """
    try:
        zones = when(time_string=time_string, location_keys=locations)
    except zoneinfo.ZoneInfoNotFoundError as e:
        print(f"[b red]Unknown timezone[/]: {e}")
        sys.exit(1)

    zones = sorted(zones, key=lambda x: x.offset)
    table = Table(title="Time table", style=table_color, box=rich.box.ROUNDED, padding=row_padding)
    for zone in zones:
        text = zone.description + (f" ({zone.name})" if zone.name else "")
        if text:
            text += "\n"
        text += zone.tz
        table.add_column(Text(text, justify="center", style=header_color))

    p_times = None
    for _times in zip(*[zone.times for zone in zones]):
        row = []
        times = [dt.fromisoformat(t) for t in _times]

        for i, time in enumerate(times):
            row_text = Text()
            date_col = Text(
                time.strftime(date_format),
                style=Style(
                    color=date_color, bgcolor="yellow" if p_times and p_times[i].date() < time.date() else None
                ),
            )

            time_col = Text(time.strftime(time_format), style=time_color)
            tz_col = Text(time.strftime(tz_format), style=tz_color)

            for info_col in info_columns:
                if info_col == "date":
                    row_text += date_col
                if info_col == "time":
                    row_text += time_col
                if info_col == "tz":
                    row_text += tz_col
                row_text += " "
            row.append(row_text)

        p_times = times
        table.add_row(*row)

    print(table)


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
