# @author Marildo Cesar 10/04/2024
from datetime import date, datetime, timedelta

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
        close = float(only_numeric(close))

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
                'close': close,
                'low': float(only_numeric(low)),
                'high': float(only_numeric(high)),
                'current': current,
                'date': cdate
                }

    @classmethod
    def get_dx_values(cls):
        url = "currencies/us-dollar-index"
        response = cls.__execute(url)
        html = BeautifulSoup(response.text, 'html.parser')

        div = html.find('div', {'id': 'quotes_summary_current_data'})
        span = div.find('span', {'class': 'pid-8827-pcp'})
        value = span.text.replace('(', '').replace(')', '').replace('%', '').replace(',', '.')
        variarion = float(value)

        span = div.find('span', {'class': 'pid-8827-last'})
        current = float(only_numeric(span.text)) * 0.001

        node = html.find('div', {'class': 'overviewDataTable'})
        divs = node.findAll('div', {'class': 'first'})
        close = divs[0].findAll('span')[1].text
        close = float(close.replace(',', '.'))
        _open = divs[1].findAll('span')[1].text
        _open = float(_open.replace(',', '.'))

        _range = divs[2].findAll('span')[1].text
        low, high = _range.replace(',', '.').split('-')

        cdate = date.today() - timedelta(days=1)

        return {'day_variation': variarion,
                'open': _open,
                'close': close,
                'low': float(low),
                'high': float(high),
                'current': current,
                'date': cdate
                }

    @classmethod
    def get_usd_brl_fut_values(cls):
        def format_number(value: str) -> float:
            value = only_numeric(value)
            value = value.ljust(6, '0')
            value = float(value) * 0.01
            return value

        url = "currencies/usd-brl-bmf-futures"
        response = cls.__execute(url)
        html = BeautifulSoup(response.text, 'html.parser')

        div = html.find('div', {'id': 'quotes_summary_current_data'})
        span = div.find('span', {'class': 'pid-1161472-pcp'})
        value = span.text.replace('(', '').replace(')', '').replace('%', '').replace(',', '.')
        variarion = float(value)

        span = div.find('span', {'class': 'pid-1161472-last'})
        current = float(span.text.replace('.', '').replace(',', '.'))

        node = html.find('div', {'class': 'overviewDataTable'})
        divs = node.findAll('div', {'class': 'first'})
        close = divs[0].findAll('span')[1].text
        close = format_number(close)
        _open = divs[1].findAll('span')[1].text
        _open = format_number(_open)

        _range = divs[2].findAll('span')[1].text
        low, high = _range.split('-')

        cdate = date.today() - timedelta(days=1)

        node = html.find('span', {'class': 'pid-1161472-time'})
        value = node.text
        if value.__contains__('/'):
            d, m = value.split('/')
            if int(d) == cdate.day:
                close = current

        return {'day_variation': variarion,
                'open': _open,
                'close': close,
                'low': format_number(low),
                'high': format_number(high),
                'current': current,
                'date': cdate
                }

    @classmethod
    def get_usd_brl_values(cls):
        def format_number(value: str) -> float:
            value = only_numeric(value)
            value = value.ljust(5, '0')
            value = round(float(value) * 0.0001, 4)
            return value

        url = "currencies/usd-brl"
        response = cls.__execute(url)
        html = BeautifulSoup(response.text, 'html.parser')

        node = html.find('span', {'data-test': 'instrument-price-change-percent'})
        value = node.text.replace('(', '').replace(')', '').replace('%', '').replace(',', '.')
        variarion = float(value)

        node = html.find('div', {'data-test': 'instrument-price-last'})
        current = format_number(node.text)

        node = html.find('dd', {'data-test': 'prevClose'})
        close = node.find('span').findAll('span')[1].text
        close = format_number(close)

        node = html.find('dd', {'data-test': 'open'})
        _open = node.find('span').findAll('span')[1].text
        _open = format_number(_open)

        node = html.find('dd', {'data-test': 'dailyRange'})
        _range = node.findAll('span', {'class': 'key-info_dd-numeric__ZQFIs'})
        low = _range[0].findAll('span')[1].text
        high = _range[1].findAll('span')[1].text

        node = html.find('time', {'data-test': 'trading-time-label'})
        cdate = node.attrs['datetime']
        cdate = parse_date.parse(cdate)

        return {'day_variation': variarion,
                'open': _open,
                'close': close,
                'low': format_number(low),
                'high': format_number(high),
                'current': current,
                'date': cdate
                }
