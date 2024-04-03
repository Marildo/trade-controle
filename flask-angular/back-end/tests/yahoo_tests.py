# @author Marildo Cesar 02/11/2023
from datetime import date

import pytest as pytest

from model import Ativo
from src.services.yfinances import YFinanceService


def test_get_prices():
    test = YFinanceService.get_prices('WEGE3', date(day=1, month=7, year=2020))
    print(test)


def test_update_prices():
    data = Ativo.find_like_name('RANDON')
    YFinanceService.update_price(data)


def test_update_indices():
    datas = Ativo.find_like_name('INDICE')
    for d in datas:
        YFinanceService.update_indices(d)


if __name__ == '__main__':
    pytest.main()
