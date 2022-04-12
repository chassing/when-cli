"""
Based on:

* original code from rich-cli, by @willmcgugan.
  https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py

* rich-click
  https://github.com/ewels/rich-click

* and rich-click PR for typer supprt
  https://github.com/ewels/rich-click/pull/26

Replace this hack if https://github.com/ewels/rich-click as full Typer support
"""
import re
from typing import Tuple

import click.core
import click.types
import rich_click as click
import rich_click.rich_click
import typer  # noqa: F401
import typer.core
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich_click import RichCommand, RichGroup
from rich_click.rich_click import _get_help_text, _make_command_help, _make_rich_rext, highlighter

rich_click.rich_click.STYLE_HELPTEXT = ""


def rich_format_help(obj, ctx, formatter):
    """Print nicely formatted help text using rich

    Based on original code from rich-cli, by @willmcgugan.
    https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py#L162-L236

    Replacement for the click function format_help().
    Takes a command or group and builds the help text output.

    Args:
        obj (click.Command or click.Group): Command or group to build help text for
        ctx (click.Context): Click Context object
        formatter (click.HelpFormatter): Click HelpFormatter object
    """

    console = Console(
        theme=Theme(
            {
                "option": rich_click.rich_click.STYLE_OPTION,
                "switch": rich_click.rich_click.STYLE_SWITCH,
                "metavar": rich_click.rich_click.STYLE_METAVAR,
                "usage": rich_click.rich_click.STYLE_USAGE,
            }
        ),
        highlighter=highlighter,
        color_system=rich_click.rich_click.COLOR_SYSTEM,
    )

    # Header text if we have it
    if rich_click.rich_click.HEADER_TEXT:
        console.print(
            Padding(
                _make_rich_rext(rich_click.rich_click.HEADER_TEXT, rich_click.rich_click.STYLE_HEADER_TEXT),
                (1, 1, 0, 1),
            )
        )

    # Print usage
    console.print(Padding(highlighter(obj.get_usage(ctx)), 1), style=rich_click.rich_click.STYLE_USAGE_COMMAND)

    # Print command / group help if we have some
    if obj.help:

        # Print with a max width and some padding
        console.print(
            Padding(
                Align(_get_help_text(obj), width=rich_click.rich_click.MAX_WIDTH, pad=False),
                (0, 1, 1, 1),
            )
        )

    # Look through OPTION_GROUPS for this command
    # stick anything unmatched into a default group at the end
    option_groups = rich_click.rich_click.OPTION_GROUPS.get(ctx.command_path, []).copy()
    option_groups.append({"options": []})
    argument_groups = {"name": rich_click.rich_click.ARGUMENTS_PANEL_TITLE, "options": []}
    for param in obj.get_params(ctx):

        # Skip positional arguments - they don't have opts or helptext and are covered in usage
        # See https://click.palletsprojects.com/en/8.0.x/documentation/#documenting-arguments
        if type(param) in [click.core.Argument, typer.core.TyperArgument] and not rich_click.rich_click.SHOW_ARGUMENTS:
            continue

        # Skip if option is hidden
        if getattr(param, "hidden", False):
            continue

        # Already mentioned in a config option group
        for option_group in option_groups:
            if any([opt in option_group.get("options", []) for opt in param.opts]):
                break
        # No break, no mention - add to the default group
        else:
            if (
                type(param) in [click.core.Argument, typer.core.TyperArgument]
                and not rich_click.rich_click.GROUP_ARGUMENTS_OPTIONS
            ):
                argument_groups["options"].append(param.opts[0])
            else:
                option_groups[-1]["options"].append(param.opts[0])  # type: ignore

    # If we're not grouping arguments and we got some, prepend before default options
    if len(argument_groups["options"]) > 0:
        option_groups.insert(len(option_groups) - 1, argument_groups)

    # Print each option group panel
    for option_group in option_groups:

        options_rows = []
        for opt in option_group.get("options", []):

            # Get the param
            for param in obj.get_params(ctx):
                if any([opt in param.opts]):
                    break
            # Skip if option is not listed in this group
            else:
                continue

            # Short and long form
            opt_long_strs = []
            opt_short_strs = []
            for idx, opt in enumerate(param.opts):
                opt_str = opt
                if param.secondary_opts and idx in param.secondary_opts:
                    opt_str += "/" + param.secondary_opts[idx]
                if "--" in opt:
                    opt_long_strs.append(opt_str)
                else:
                    opt_short_strs.append(opt_str)

            # Column for a metavar, if we have one
            metavar = Text(style=rich_click.rich_click.STYLE_METAVAR)
            metavar_str = param.make_metavar()
            # Do it ourselves if this is a positional argument
            if type(param) in [click.core.Argument, typer.core.TyperArgument] and metavar_str == param.name.upper():
                metavar_str = param.type.name.upper()
            # Skip booleans
            if metavar_str != "BOOLEAN":
                metavar.append(metavar_str)

            # Range - from https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706
            try:
                if (
                    isinstance(param.type, click.types._NumberRangeBase)
                    # skip count with default range type
                    and not (param.count and param.type.min == 0 and param.type.max is None)
                ):
                    range_str = param.type._describe_range()
                    if range_str:
                        metavar.append(rich_click.rich_click.RANGE_STRING.format(range_str))
            except AttributeError:
                # click.types._NumberRangeBase is only in Click 8x onwards
                pass

            # Required asterisk
            required = ""
            if param.required:
                required = Text(
                    rich_click.rich_click.REQUIRED_SHORT_STRING, style=rich_click.rich_click.STYLE_REQUIRED_SHORT
                )

            rows = [
                required,
                highlighter(highlighter(",".join(opt_long_strs))),
                highlighter(highlighter(",".join(opt_short_strs))),
                metavar,
                _get_parameter_help(param, ctx),
            ]

            # Remove metavar if specified in config
            if not rich_click.rich_click.SHOW_METAVARS_COLUMN:
                rows.pop(3)

            options_rows.append(rows)

        if len(options_rows) > 0:
            options_table = Table(highlight=True, box=None, show_header=False)
            # Strip the required column if none are required
            if all([x[0] == "" for x in options_rows]):
                options_rows = [x[1:] for x in options_rows]
            for row in options_rows:
                options_table.add_row(*row)
            console.print(
                Panel(
                    options_table,
                    border_style=rich_click.rich_click.STYLE_OPTIONS_PANEL_BORDER,
                    title=option_group.get("name", rich_click.rich_click.OPTIONS_PANEL_TITLE),  # type: ignore
                    title_align=rich_click.rich_click.ALIGN_OPTIONS_PANEL,
                    width=rich_click.rich_click.MAX_WIDTH,
                )
            )

    #
    # Groups only:
    # List click command groups
    #
    if hasattr(obj, "list_commands"):
        # Look through COMMAND_GROUPS for this command
        # stick anything unmatched into a default group at the end
        cmd_groups = rich_click.rich_click.COMMAND_GROUPS.get(ctx.command_path, []).copy()
        cmd_groups.append({"commands": []})
        for command in obj.list_commands(ctx):
            for cmd_group in cmd_groups:
                if command in cmd_group.get("commands", []):
                    break
            else:
                cmd_groups[-1]["commands"].append(command)  # type: ignore

        # Print each command group panel
        for cmd_group in cmd_groups:
            commands_table = Table(highlight=False, box=None, show_header=False)
            # Define formatting in first column, as commands don't match highlighter regex
            commands_table.add_column(style="bold cyan", no_wrap=True)
            for command in cmd_group.get("commands", []):
                # Skip if command does not exist
                if command not in obj.list_commands(ctx):
                    continue
                cmd = obj.get_command(ctx, command)
                # Use the truncated short text as with vanilla text if requested
                if rich_click.rich_click.USE_CLICK_SHORT_HELP:
                    helptext = cmd.get_short_help_str()
                else:
                    # Use short_help function argument if used, or the full help
                    helptext = cmd.short_help or cmd.help or ""
                commands_table.add_row(command, _make_command_help(helptext))
            if commands_table.row_count > 0:
                console.print(
                    Panel(
                        commands_table,
                        border_style=rich_click.rich_click.STYLE_COMMANDS_PANEL_BORDER,
                        title=cmd_group.get("name", rich_click.rich_click.COMMANDS_PANEL_TITLE),  # type: ignore
                        title_align=rich_click.rich_click.ALIGN_COMMANDS_PANEL,
                        width=rich_click.rich_click.MAX_WIDTH,
                    )
                )

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        console.print(Padding(Align(highlighter(epilogue), width=rich_click.rich_click.MAX_WIDTH, pad=False), 1))

    # Footer text if we have it
    if rich_click.rich_click.FOOTER_TEXT:
        console.print(rich_click.rich_click.FOOTER_TEXT, justify="right")


def _get_parameter_help(param, ctx):
    """Build primary help text for a click option or argument.

    Returns the prose help text for an option or argument, rendered either
    as a Rich Text object or as Markdown.
    Additional elements are appended to show the default and required status if applicable.

    Args:
        param (click.Option or click.Argument): Option or argument to build help text for
        ctx (click.Context): Click Context object

    Returns:
        Columns: A columns element with multiple styled objects (help, default, required)
    """

    items = []

    if getattr(param, "help", None):
        paragraphs = param.help.split("\n\n")
        # Remove single linebreaks
        if not rich_click.rich_click.USE_MARKDOWN:
            paragraphs = [
                x.replace("\n", " ").strip() if not x.startswith("\b") else "{}\n".format(x.strip("\b\n"))
                for x in paragraphs
            ]
        items.append(_make_rich_rext("\n".join(paragraphs).strip(), rich_click.rich_click.STYLE_OPTION_HELP))

    # Append metavar if requested
    if rich_click.rich_click.APPEND_METAVARS_HELP:
        metavar_str = param.make_metavar()
        # Do it ourselves if this is a positional argument
        if type(param) in [click.core.Argument, typer.core.TyperArgument] and metavar_str == param.name.upper():
            metavar_str = param.type.name.upper()
        # Skip booleans
        if metavar_str != "BOOLEAN":
            metavar_str = metavar_str.replace("[", "").replace("]", "")
            items.append(
                Text(
                    rich_click.rich_click.APPEND_METAVARS_HELP_STRING.format(metavar_str),
                    style=rich_click.rich_click.STYLE_METAVAR_APPEND,
                )
            )

    # Default value
    if getattr(param, "show_default", None):
        # param.default is the value, but click is a bit clever in choosing what to show here
        # eg. --debug/--no-debug, default=False will show up as [default: no-debug] instead of [default: False]
        # To avoid duplicating loads of code, let's just pull out the string from click with a regex
        default_str_match = re.search(r"default: (.*)\]", param.get_help_record(ctx)[-1])
        if default_str_match:
            # Don't show the required string, as we show that afterwards anyway
            default_str = default_str_match.group(1).replace("; required", "")
            items.append(
                Text(
                    rich_click.rich_click.DEFAULT_STRING.format(default_str),
                    style=rich_click.rich_click.STYLE_OPTION_DEFAULT,
                )
            )

    envvar = getattr(param, "envvar")
    # allow_from_autoenv is currently not supported in Typer for CLI Arguments
    if envvar is not None:
        var_str = ", ".join(str(d) for d in envvar) if isinstance(envvar, (list, tuple)) else envvar
        items.append(Text(f"[env var: {var_str}]", style="dim"))  # noqa: W605
    # Required?
    if param.required:
        items.append(Text(rich_click.rich_click.REQUIRED_LONG_STRING, style=rich_click.rich_click.STYLE_REQUIRED_LONG))

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)


def blend_text(message: str, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> Text:
    """Blend text from one color to another."""
    text = Text(message)
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    dr = r2 - r1
    dg = g2 - g1
    db = b2 - b1
    size = len(text)
    for index in range(size):
        blend = index / size
        color = f"#{int(r1 + dr * blend):2X}{int(g1 + dg * blend):2X}{int(b1 + db * blend):2X}"
        text.stylize(color, index, index + 1)
    return text


RichCommand.format_help = rich_format_help  # type: ignore
RichGroup.format_help = rich_format_help  # type: ignore
