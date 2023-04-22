"""
 @author Marildo Cesar 22/04/2023
"""

from datetime import datetime, date

from dateutil.parser import parse as parse_date


def str_datetime(value: str) -> datetime:
    return parse_date(value)


def str_date(value: str) -> date:
    return parse_date(value, dayfirst=True).date()
