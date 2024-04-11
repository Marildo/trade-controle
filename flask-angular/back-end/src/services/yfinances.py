"""
 @author Marildo Cesar 28/06/2023
"""

from datetime import date, timedelta, datetime, time

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
    def update_indices(ativo):
        start = date.today() - timedelta(days=5)
        data = yf.download(ativo.codigo, period='1d', start=start)
        data['variation'] = round(data['Adj Close'].pct_change() * 100, 2)
        ativo.fechamento = data['Adj Close'].iloc[-1]
        ativo.abertura = data['Open'].iloc[-1]
        ativo.maxima = data['High'].iloc[-1]
        ativo.minima = data['Low'].iloc[-1]
        ativo.variacao = data['variation'].iloc[-1]
        ativo.update()

    @staticmethod
    def get_prices(codigo: str, start: date) -> Dict:
        codigos = [f'{codigo}.SA']
        data = yf.download(codigos, period='1d', start=start)['Adj Close']
        return {k.date(): v for k, v in data.to_dict().items()}

    @staticmethod
    def get_historic(codigo: str, start: date, end: date, interval: str) -> DataFrame:
        codigos = [f'{codigo}.SA']
        data = yf.download(codigos, start=start, end=end, timeout=60, interval=interval)
        return data

    @staticmethod
    def get_sp500_fut_data():
        ticker = "ES=F"
        end_date = date.today()
        start_date = end_date - timedelta(days=7)
        sp500_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

        sp500_data['variation'] = round(sp500_data['Close'].pct_change() * 100, 4)

        data = {}
        variation = sp500_data['variation'].iloc[-1]
        data['current_variation'] = variation

        variation = sp500_data['variation'].iloc[-2]
        data['variation'] = variation

        last_close = sp500_data['Close'].iloc[-2]
        data['close'] = last_close

        last_high = sp500_data['High'].iloc[-2]
        data['high'] = last_high

        last_low = sp500_data['Low'].iloc[-2]
        data['low'] = last_low

        return data

    @staticmethod
    def get_ibove_data(last_date: bool):
        ticker = "^BVSP"
        end_date = date.today()
        start_date = end_date - timedelta(days=7)
        sp500_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
        sp500_data['variation'] = round(sp500_data['Close'].pct_change() * 100, 4)

        data = {}

        last_reg = str(sp500_data.index[-1])[0:10]
        current_date = last_reg == str(end_date)
        p = -1 if last_date else -2 if current_date else -1
        variation = sp500_data['variation'].iloc[p]
        data['variation'] = variation

        last_close = sp500_data['Close'].iloc[p]
        data['close'] = last_close

        last_high = sp500_data['High'].iloc[p]
        data['high'] = last_high

        last_low = sp500_data['Low'].iloc[p]
        data['low'] = last_low

        variation = sp500_data['variation'].iloc[-1]
        data['current_variation'] = variation
        return data

    def get_historico_indice(self):
        start = date.today() - timedelta(days=150)
        data = yf.download('', period='1d', start=start)
        data['variation'] = round(data['Adj Close'].pct_change() * 100, 2)
        ativo.cotacao = data['Adj Close'].iloc[-1]
