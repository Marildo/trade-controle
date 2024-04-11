# @author Marildo Cesar 31/03/2024

from datetime import date
import requests
from bs4 import BeautifulSoup

from src.utils.date_util import ptbr_to_date


class ADVFNService:

    def __init__(self):
        pass

    def __execute(self, url: str):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36'}

        full_url = 'https://br.advfn.com/' + url
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return response

    def get_di(self):
        url = "/investimentos/futuros/di-depositos-interfinanceiros/cotacoes"
        response = self.__execute(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.select('#id_lista-futuros')[0]
        tr = table.select('tr')[1]
        td = tr.select('td')[2]
        value = td.text
        if value == '-':
            tr = table.select('tr')[2]
            td = tr.select('td')[2]
            value = td.text

        di = float(value.replace('.', '').replace(',', '.'))
        code = tr.select('td')[0].text

        return {'di_code': code, 'di_current': di}

    def get_ibove_current(self):
        url = "bolsa-de-valores/bmf/indice-bovespa-IBOV/cotacao"
        response = self.__execute(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrando o elemento com base nos id
        variation = soup.select('#quoteElementPiece4')[0].text
        variation = float(variation.replace('.', '').replace(',', '.').replace("%", ''))

        current = soup.select('#quoteElementPiece5')[0].text
        current = float(current.replace('.', '').replace(',', '.'))

        data = {
            'day_variation': variation,
            'current': current
        }
        return data
