import datetime

from dateutil.parser import parse as parse_date


def str_datetime(value: str) -> datetime.datetime:
    return parse_date(value)


def str_date(value: str) -> datetime.date:
    return parse_date(value, dayfirst=True).date()
