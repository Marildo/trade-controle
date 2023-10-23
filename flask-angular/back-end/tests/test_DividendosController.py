# @author Marildo Cesar 19/09/2023

from src.services.status_invest import StatusInvest

import requests

import yfinance as yf


def yahoo():
    data = yf.download('cyre3.SA', start='2021-12-01', end='2023-08-01', actions=True)
    dividendos = data.query("Dividends > 0")
    print(dividendos)
    for i, row in dividendos.iterrows():
        print(i, row.Dividends)


StatusInvest().load_dividendos('itsa4')
