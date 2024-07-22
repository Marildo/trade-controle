# @author Marildo Cesar 03/05/2024

from datetime import date, datetime, timedelta, time

import requests
from bs4 import BeautifulSoup
from dateutil import parser as parse_date

from src.utils.number_util import only_numeric


class BCBService:

    @classmethod
    def get_last_ptax(cls):
        url = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=consultarBoletim"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        today = datetime.today()
        last_day = today.time() < time(hour=10, minute=10)
        today.weekday()
        if last_day:
            today = today - timedelta(days=1)

        if today.isoweekday() in (6, 7):
            wd = 7 - today.isoweekday()
            today = today - timedelta(days=wd)

        dataini = today.strftime('%d/%m/%Y')

        data = {
            'RadOpcao': 3,
            'DATAINI': dataini,
            'DATAFIM': '',
            'ChkMoeda': 61
        }
        response = requests.post(url, headers=headers, data=data)
        html = BeautifulSoup(response.text, 'html.parser')

        table = html.find('table', {'class': 'tabela'})
        if not table:
            return None
        body = table.find('tbody')
        trs = body.find_all('tr')

        if last_day:
            i = 4
        else:
            if today.time() < time(hour=11, minute=10):
                i = 0
            elif today.time() < time(hour=12, minute=10):
                i = 1
            elif today.time() < time(hour=13, minute=10):
                i = 2
            else:
                i = 4

        tds = trs[i].find_all('td')
        value = tds[3].text

        return value.replace(',', '.')
