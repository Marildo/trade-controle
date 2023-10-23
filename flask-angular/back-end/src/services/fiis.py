# @author Marildo Cesar 12/10/2023
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from src.utils.str_util import onnly_numbers
from src.utils.date_util import str_date


def load_dividendos(codigo: str) -> List[Dict]:
    def str_to_float(value: str) -> float:
        value = onnly_numbers(value)
        value = round(float(value) * 0.01, 3)
        return value

    result = []
    url = f'https://fiis.com.br//{codigo}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    div = soup.find('div', class_='yieldChart__table__body')
    lines = div.find_all('div', class_='table__linha')
    if lines:
        i = 0
        row = {}
        map_row = {
            0: 'data_com',
            1: 'data_pgto',
            2: 'cotacao',
            3: 'div_yield',
            4: 'valor',
        }
        map_convert = {
            0: str_date,
            1: str_date,
            2: str_to_float,
            3: str_to_float,
            4: str_to_float
        }
        for line in lines:
            value = [c.get_text(strip=True) for c in line][0]
            row[map_row[i]] = map_convert[i](value)
            i += 1
            if i == 5:
                row['jcp'] = False
                result.append(row)
                row = {}
                i = 0

        return result
