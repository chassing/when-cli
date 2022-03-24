import locale
import sys
from datetime import datetime as dt
from typing import List

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

import rich.box
from rich import print
from rich.style import Style
from rich.table import Table
from rich.text import Text

from when.config import settings
from when.rich_typer import blend_text, click, typer
from when.when import when

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = False
click.rich_click.SHOW_METAVARS_COLUMN = True
click.rich_click.SHOW_ENVVARS_COLUMN = True
click.rich_click.FOOTER_TEXT = blend_text(
    "Made with ♥ by https://github.com/chassing/when-cli", (32, 32, 255), (255, 32, 255)
)
click.rich_click.STYLE_FOOTER_TEXT = "#D920FF"

locale.setlocale(locale.LC_ALL, "")
locale.setlocale(locale.LC_TIME, "")


INFO_COLS = [
    ("date", "Date column"),
    ("time", "Time column"),
    ("tz", "Timezone column"),
]

VERSION = "2.0"


def complete_info_columns(ctx: typer.Context, incomplete: str):
    for name, help_text in INFO_COLS:
        if name.startswith(incomplete) and name not in ctx.params.get("info-columns", []):
            yield (name, help_text)


def show_usage(value: bool):
    if not value:
        return
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
    table_color: str = typer.Option("deep_sky_blue2", envvar="WHEN_TABLE_COLOR", metavar="COLOR", show_default=True),
    table_padding: int = typer.Option(0, envvar="WHEN_TABLE_PADDING", metavar="INTEGER"),
    header_color: str = typer.Option("green", envvar="WHEN_HEADER_COLOR", metavar="COLOR"),
    date_format: str = typer.Option("%x", envvar="WHEN_DATE_FORMAT", metavar="FORMAT_DIRECTIVE"),
    date_color: str = typer.Option("deep_pink4", envvar="WHEN_DATE_COLOR", metavar="COLOR"),
    time_format: str = typer.Option("%H:%M", envvar="WHEN_TIME_FORMAT", metavar="FORMAT_DIRECTIVE"),
    time_color: str = typer.Option("spring_green3", envvar="WHEN_TIME_COLOR", metavar="COLOR"),
    tz_format: str = typer.Option("%Z", envvar="WHEN_TZ_FORMAT", metavar="FORMAT_DIRECTIVE"),
    tz_color: str = typer.Option("grey27", envvar="WHEN_TZ_COLOR", metavar="COLOR"),
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
    """[b yellow]when-cli[/] is a small timezone conversation tool. It takes as input a natural given time string
    (can also be a time range) and converts it into different timezone at specific locations.

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
    [#2020FF]C[/][#4520FF]o[/][#6A20FF]l[/][#8F20FF]o[/][#B420FF]r[/][#D920FF]s[/]
    See [link]https://rich.readthedocs.io/en/latest/appendix/colors.html[/] for all available color codes.
    """
    try:
        r = when(time_string=time_string, location_keys=locations)
    except zoneinfo.ZoneInfoNotFoundError as e:
        print(f"[b red]Unknown timezone[/]: {e}")
        sys.exit(1)

    zones = sorted(r, key=lambda x: x["offset"])
    table = Table(title="Time table", style=table_color, box=rich.box.ROUNDED, padding=table_padding)
    for zone in zones:
        text = ""
        if zone["description"]:
            text += zone["description"]
        if zone["name"]:
            text += zone["name"]
        if zone["description"] or zone["name"]:
            text += "\n"
        text += zone["tz"]
        table.add_column(Text(text, justify="center", style=header_color))

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

    print(table)


if __name__ == "__main__":
    typer.run(main)
