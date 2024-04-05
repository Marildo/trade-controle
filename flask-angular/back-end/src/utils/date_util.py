"""
 @author Marildo Cesar 22/04/2023
"""

from datetime import datetime, date, timedelta

from dateutil.parser import parse as parse_date


def str_datetime(value: str) -> datetime:
    return parse_date(value)


def str_date(value: str) -> date:
    return parse_date(value, dayfirst=True).date()


def ptbr_to_date(value: str) -> date:

    months_map = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Abr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    day, month_name, year = value.split()
    month_number = months_map[month_name]
    day = int(day)
    year = int(year)
    return date(year, month_number, day)


def uteis_days(start_date: date, end_date: date, holidays: list):
    """
    Calcula o número de dias úteis entre duas datas.

    Args:
        data_inicial (Date): Data inicial .
        data_final (Date): Data final .
        data_final (List): Lista de feriados.

    Returns:
        int: Número de dias úteis entre as duas datas.
    """

    dias_uteis = 0
    data_atual = start_date
    while data_atual <= end_date:
        if data_atual.weekday() not in [5, 6] and data_atual not in holidays:
            dias_uteis += 1
        data_atual += timedelta(days=1)
    return dias_uteis
