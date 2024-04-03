# @author Marildo Cesar 31/03/2024

import requests
from bs4 import BeautifulSoup


class ADVFNService:

    def __init__(self):
        pass

    def __execute(self, url: str):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36'}

        full_url = 'https://br.advfn.com/' + url
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return response

    def get_winfut_values(self, wind_code: str):
        url = f"bolsa-de-valores/bmf/{wind_code}/cotacao"
        response = self.__execute(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrando o elemento com base nos id
        close = soup.select('#quoteElementPiece8')[0].text
        close = int(float(close.replace('.', '').replace(',', '.')))

        low = soup.select('#quoteElementPiece11')[0].text
        low = low if low else '0'
        low = int(float(low.replace('.', '').replace(',', '.')))

        high = soup.select('#quoteElementPiece12')[0].text
        high = high if high else '0'
        high = int(float(high.replace('.', '').replace(',', '.')))

        return {'close': close, 'low': low, 'high': high}

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

        return {'code': code, 'value': di}

    def get_ibove_variation(self):
        url = "bolsa-de-valores/bmf/indice-bovespa-IBOV/cotacao"
        response = self.__execute(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrando o elemento com base nos id
        variation = soup.select('#quoteElementPiece4')[0].text
        variation = float(variation.replace('.', '').replace(',', '.').replace("%", ''))
        return variation

    def get_sp500fut_variation(self):
        url = "https://www.cnbc.com/quotes/@SP.1"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        sl = '#quote-page-strip > div.QuoteStrip-dataContainer > div.QuoteStrip-lastTimeAndPriceContainer ' \
             '> div.QuoteStrip-lastPriceStripContainer'
        node = soup.select(sl)[0]
        spans = node.findAll('span')
        value = spans[3].text
        value = value.replace(',', '.').replace('(', '').replace(')', '').replace('%', '').replace(' UNCH', '0')
        return float(value)
