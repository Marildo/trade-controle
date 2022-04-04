"""
Created on 03/04/2022
by MarildoCesar
"""

from typing import List

import yfinance as yf


# https://analyzingalpha.com/blog/yfinance-python
class YFinanceService:

    @staticmethod
    def update_price(ativos: List) -> List:
        codigos = [f'{item.codigo}.SA' for item in ativos]
        response = yf.download(codigos, period='1d')['Adj Close']
        for i in range(len(ativos)):
            values = response[codigos[i]]
            ativos[i].cotacao = values[0]
            ativos[0].save()

        return ativos
