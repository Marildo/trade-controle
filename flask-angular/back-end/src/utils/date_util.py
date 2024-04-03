"""
 @author Marildo Cesar 22/04/2023
"""

from datetime import datetime, date, timedelta

from dateutil.parser import parse as parse_date


def str_datetime(value: str) -> datetime:
    return parse_date(value)


def str_date(value: str) -> date:
    return parse_date(value, dayfirst=True).date()


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
