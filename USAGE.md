# Usage

```
$ when-cli [OPTIONS] TIME_STRING
```

# Examples

```shell
$ when-cli "17:00 in Lisbon" -l lax -l Berlin

```
<img src="https://raw.githubusercontent.com/chassing/when-cli/master/media/usage-example1.png" width="50%" />

```shell
$ when-cli "30. September 17:00 to Oct 1st 2:3pm in LAX"
```

<img src="https://raw.githubusercontent.com/chassing/when-cli/master/media/usage-example2.png" width="50%" />


# TIME_STRING Syntax

The required argument (`TIME_STRING`) is basically a human readable date time string with this structure:

[`DATE`] `TIME` [to [`TO_DATE`] `TO_TIME`] [in `TIMEZONE_OR_LOCATION`]

* `DATE` is the start date. *[Default: **today**]*
* `TIME` is the start time. **required**
* `TO_DATE` is the end date. *[Default: **end date = start date**]*
* `TO_TIME` is the end time. *[Default: **end time = start time**]*
* `TIMEZONE_OR_LOCATION` interpret dates and times in this timezone. *[Default: **host timezone**]*


## `DATE` format

* YYYY-MM-DD, YYYY.MM.DD (e.g. 2021-09-30) - English locale
* DD.MM.YYYY (e.g. 30.09.1979) - German locale
* Day Month [Year] (e.g. 30. September) - German locale
* [Year] Month Day (e.g. September 30th) - English locale
* Month can be an abbreviation too (e.g Sep vs September)
* Day can be english or german local (e.g. 1st vs 1.)

> This parameter is not case-sensitive (September vs september)


## `TIME` format

* HH:MM (e.g. 16:30) - 24 hours format
* HH:MM am/pm (e.g. 2:30am) - 12 hours format

> This parameter is not case-sensitive (am vs AM)


## `TIMEZONE_OR_LOCATION` format

This can be either a name of a city, a time zone name, or an airport code or a custom defined location.

Cites with a population than 15000 (~24113) are supported, e.g.:

* Los Angeles (US)
* Erfurt (Germany)
* Torrance (US)

> City names are in english and not case-sensitive

All standard timezones are supported, e.g.:
* Europe/Vienna
* UTC
* America/Los_Angeles

> Timezone names are case-sensitiv

International airport codes (IATA 3-letter code, ICAO 4-alphanumeric code), e.g.:
* klu (Klagenfurt Airport)
* lax (Los Angeles International Airport)
* KJFK (John F Kennedy International Airport)

> Airport codes are not case-sensitive

Or self defined location (see [Configuration](https://github.com/chassing/when-cli/blob/master/USAGE.md#Configuration)), e.g.:
* home 🏡

> Location keys are not case-sensitive


# Options

| Option long          | Option short | Metavar          | Default                | Description                                           | Environment variable |
| -------------------- | ------------ | ---------------- | ---------------------- | ----------------------------------------------------- | -------------------- |
| --locations          | -l           | LOCATION_KEY     | **klu, els, sin, utc** | Display these locations. Can be given multiple times. | WHEN_LOCATIONS       |
| --table-color        |              | COLOR            | **deep_sky_blue2**     | Table border color ([Rich Colors])                    | WHEN_TABLE_COLOR     |
| --row-padding        |              | INTEGER          | **0**                  | Row padding                                           | WHEN_ROW_PADDING     |
| --header-color       |              | COLOR            | **green**              | Header font color ([Rich Colors])                     | WHEN_HEADER_COLOR    |
| --date-format        |              | FORMAT_DIRECTIVE | **%x**                 | Date format ([Python format codes])                   | WHEN_DATE_FORMAT     |
| --date-color         |              | COLOR            | **deep_pink4**         | Date font color ([Rich Colors])                       | WHEN_DATE_COLOR      |
| --time-format        |              | FORMAT_DIRECTIVE | **%H:%M**              | Time format ([Python format codes])                   | WHEN_TIME_FORMAT     |
| --time-color         |              | COLOR            | **spring_green3**      | Time font color ([Rich Colors])                       | WHEN_TIME_COLOR      |
| --tz-format          |              | FORMAT_DIRECTIVE | **%Z**                 | Timezone format ([Python format codes])               | WHEN_TZ_FORMAT       |
| --tz-color           |              | COLOR            | **grey27**             | Timezone font color ([Rich Colors])                   | WHEN_TZ_COLOR        |
| --info-columns       | -i           | COL_NAME         | **date, time, tz**     | Display these columns in this order.                  | WHEN_INFO_COLUMNS    |
| --usage              |              |                  |                        | Show usage.                                           | |
| --install-completion |              |                  |                        | Install completion for the specified shell.           | |
| --show-completion    |              |                  |                        | Show completion for the specified shell.              | |
| --help               |              |                  |                        | Show this message and exit.                           | |

Instead of specifying your preferred option via command line again and again you can use environment variables.

with command line options:
```bash
$ when-cli "17:00 in Europe/Berlin" -l lax -l pmi --row-padding 1 --table-color red1 --header-color gold1
```

instead with environment variables:

```bash
$ export WHEN_LOCATIONS="lax pmi"
$ export WHEN_ROW_PADDING=1
$ export WHEN_TABLE_COLOR=red1
$ export WHEN_HEADER_COLOR=gold1
$ when-cli "17:00 in Europe/Berlin"

```

both will print

<img src="https://raw.githubusercontent.com/chassing/when-cli/master/media/usage-example3.png" width="50%" />


[Python format codes]: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
[Rich Colors]:         https://rich.readthedocs.io/en/latest/appendix/colors.html


# Configuration

Adapt **when-cli** configs via additional environment variables.

## Default timezone

Set the timezone which will be used if not timezone is given in *TIME_STRING*.

**WHEN_CONFIG_DEFAULT_TZ**

default: host timezone

example
```
$ export WHEN_CONFIG_DEFAULT_TZ="UTC"
```

## Custom locations

You can define your own locations  with a custom location key (e.g. **home**), description, and timezone (tz). Those locations definition will be used also if no location is specified on the command line (--location).

It's a JSON list of dictionaries in this format:

```json
[{
    "key": "location-key",
    "description": "long description",
    "tz": "timezone name"
},{
    "key": "other-location-key",
    "description": "long description",
    "tz": "timezone name"
}]
```

**WHEN_CONFIG_LOCATIONS**

example:
```
$ export WHEN_CONFIG_LOCATIONS='[{ "key": "🏠", "description": "On my couch", "tz": "Europe/Vienna" },{ "key": "ron", "description": "Buddies home", "tz": "America/New_York" }]'
$ when-cli '17:00'
```
<img src="https://raw.githubusercontent.com/chassing/when-cli/master/media/usage-example4.png" width="50%" />

