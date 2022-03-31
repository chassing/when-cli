# Usage

```
$ when-cli [OPTIONS] TIME_STRING
```

# Examples

```shell
$ when-cli "17:00 in Lisbon" -l lax -l Berlin

```

#TODO screenshot

```shell
$ when-cli "30. September 17:00 to Oct 1st 2:3pm in LAX"
```
#TODO screenshot


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

Or self defined location (see CONFIG.md), e.g.:
* home 😁

> Location keys are not case-sensitive



# Options

| foo | bar |
| --- | --- |
| baz | bim |
