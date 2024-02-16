"""
 @author Marildo Cesar 28/06/2023
"""

from datetime import date, timedelta

from typing import List, Dict
import math
import yfinance as yf
from pandas import DataFrame


class YFinanceService:

    @staticmethod
    def update_price(ativos: List) -> List:
        codigos = [f'{item.codigo}.SA' for item in ativos]
        response = yf.download(codigos, period='1d')['Adj Close']
        for i in range(len(ativos)):
            # values = response[codigos[i]]
            # value = values[0]
            ativo = ativos[i]
            value = response[f'{ativo.codigo}.SA'].values[0]
            if not math.isnan(value):
                ativo.cotacao = value

        return ativos

    @staticmethod
    def get_prices(codigo: str, start: date) -> Dict:
        codigos = [f'{codigo}.SA']
        data = yf.download(codigos, period='1d', start=start)['Adj Close']
        return {k.date(): v for k, v in data.to_dict().items()}

    @staticmethod
    def get_data(codigo: str, start: date, end: date) -> DataFrame:
        codigos = [f'{codigo}.SA']
        data = yf.download(codigos, period='1d', start=start, end=end, timeout=60)
        return data
