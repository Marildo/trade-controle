"""
Created on 03/04/2022
by MarildoCesar
"""

from typing import List
import math
import yfinance as yf


class YFinanceService:

    @staticmethod
    def update_price(ativos: List) -> List:
        codigos = [f'{item.codigo}.SA' for item in ativos]
        response = yf.download(codigos, period='1d')['Adj Close']
        for i in range(len(ativos)):
            values = response[codigos[i]]
            value = values[0]
            if not math.isnan(value):
                ativo = ativos[i]
                ativo.cotacao = value
                ativo.save()

        return ativos
