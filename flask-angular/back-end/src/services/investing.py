# @author Marildo Cesar 10/04/2024

import requests
from bs4 import BeautifulSoup
from dateutil import parser as parse_date

from src.utils.number_util import only_numeric


class InvestingService:

    @staticmethod
    def __execute(url: str):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        full_url = 'https://br.investing.com/' + url
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return response

    @classmethod
    def get_winfut_values(cls):
        url = "indices/bovespa-win-futures"
        response = cls.__execute(url)
        html = BeautifulSoup(response.text, 'html.parser')

        node = html.find('span', {'data-test': 'instrument-price-change-percent'})
        value = node.text.replace('(', '').replace(')', '').replace('%', '').replace(',', '.')
        variarion = float(value)

        node = html.find('div', {'data-test': 'instrument-price-last'})
        current = float(only_numeric(node.text))

        node = html.find('dd', {'data-test': 'prevClose'})
        close = node.find('span').findAll('span')[1].text

        node = html.find('dd', {'data-test': 'open'})
        _open = node.find('span').findAll('span')[1].text

        node = html.find('dd', {'data-test': 'dailyRange'})
        _range = node.findAll('span', {'class': 'key-info_dd-numeric__ZQFIs'})
        low = _range[0].findAll('span')[1].text
        high = _range[1].findAll('span')[1].text

        node = html.find('time', {'data-test': 'trading-time-label'})
        cdate = node.attrs['datetime']
        cdate = parse_date.parse(cdate)

        return {'day_variation': variarion,
                'open': float(only_numeric(_open)),
                'close': float(only_numeric(close)),
                'low': float(only_numeric(low)),
                'high': float(only_numeric(high)),
                'current': current,
                'date': cdate
                }

    @classmethod
    def get_sp500fut_values(cls):
        url = "indices/us-spx-500-futures"
        response = cls.__execute(url)
        html = BeautifulSoup(response.text, 'html.parser')

        node = html.find('span', {'data-test': 'instrument-price-change-percent'})
        value = node.text.replace('(', '').replace(')', '').replace('%', '').replace(',', '.')
        variarion = float(value)

        node = html.find('div', {'data-test': 'instrument-price-last'})
        current = float(only_numeric(node.text))

        node = html.find('dd', {'data-test': 'prevClose'})
        close = node.find('span').findAll('span')[1].text

        node = html.find('dd', {'data-test': 'open'})
        _open = node.find('span').findAll('span')[1].text

        node = html.find('dd', {'data-test': 'dailyRange'})
        _range = node.findAll('span', {'class': 'key-info_dd-numeric__ZQFIs'})
        low = _range[0].findAll('span')[1].text
        high = _range[1].findAll('span')[1].text

        node = html.find('time', {'data-test': 'trading-time-label'})
        cdate = node.attrs['datetime']
        cdate = parse_date.parse(cdate)

        return {'day_variation': variarion,
                'open': float(only_numeric(_open)),
                'close': float(only_numeric(close)),
                'low': float(only_numeric(low)),
                'high': float(only_numeric(high)),
                'current': current,
                'date': cdate
                }
