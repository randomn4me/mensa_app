# Mensa App
Small python commandline application which leverages the [OpenMensa API](https://doc.openmensa.org/api/v2/).

## Dependencies
This app depends on `python3`.

## Usage

```
usage: mensa_app.py [-h] [-i ID] [-m] [-c CITY] ...

positional arguments:
  name                  Get infos about mensas filtered by the given name

optional arguments:
  -h, --help            show this help message and exit
  -i ID, --id ID        Get infos about mensa with given id
  -m, --meals           Requires -i : prints meals for today
  -c CITY, --city CITY  Get infos about mensas in the given city
```
