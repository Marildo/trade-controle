"""
 @author Marildo Cesar 28/06/2023
"""
from datetime import date
from typing import List, Dict
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

        return ativos

    @staticmethod
    def get_prices(codigo: str, start: date) -> Dict:
        codigos = [f'{codigo}.SA']
        data = yf.download(codigos, period='1d', start=start)['Adj Close']
        return {k.date(): v for k, v in data.to_dict().items()}
