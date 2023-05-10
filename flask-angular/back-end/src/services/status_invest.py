"""
 @author Marildo Cesar 25/04/2023
"""
import os
from pathlib import Path
from typing import Tuple, List, Dict

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from src.utils.str_util import str_to_float


class StatusInvest:
    def __init__(self) -> None:

        pass

    def find_by_name(self, name: str) -> List[Dict]:
        print()
        url = f'https://statusinvest.com.br/home/mainsearchquery?q={name}&country='
        data = self._request(url).json()
        data = [i for i in data if i['type'] in (1, 2)]
        result = []
        if 1 == name:
            pass

        for item in data:
            ativo = dict(
                id=item['id'],
                parent_id=item['parentId'],
                tipo_investimento=item['type'],
                nome=item['name'],
                codigo=item['code'],
                cotacao=str_to_float(item['price']),
                variacao=str_to_float(item['variation'])
            )
            ativo = self._set_properties(ativo)
            result.append(ativo)
        return result

    def _set_properties(self, ativo: Dict) -> Dict:
        map_type = {1: 'acoes', 2: 'fundos-imobiliarios'}
        url = f'https://statusinvest.com.br/{map_type[ativo["tipo_investimento"]]}/{ativo["codigo"]}'
        response = self._request(url)
        html = BeautifulSoup(response.text, 'html.parser')

        ativo['descricao'] = self._get_descricao(html, ativo['tipo_investimento'])
        if ativo['tipo_investimento'] == 1:
            ativo['tipo_ativo'] = self.get_tipo(html)

        ativo['setor'] = self._get_propertie(ativo, 'Setor', html)
        ativo['setor']['subsetor'] = self._get_propertie(ativo, 'SubSetor', html)
        ativo['segmento'] = self._get_propertie(ativo, 'Segmento', html)

        return ativo

    def get_tipo(self, html: BeautifulSoup) -> str:
        select = '#main-2 > div:nth-child(4) > div > div:nth-child(5) > div > div > div:nth-child(1) > div > div > strong'
        _tag: Tag = html.select(select)
        if _tag:
            return _tag[0].text

        return None

    def _get_propertie(self, ativo: Dict, name_item: str, html: BeautifulSoup) -> Dict:
        path_map = {
            'Setor': 'div.top-info-md-n:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
            'SubSetor': 'div.pl-md-2:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
            'Segmento': 'div.pl-md-2:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
        }
        _id = 0
        name = 'N/A'
        item = dict(id=_id, nome=name)

        tipo = ativo['tipo_investimento']
        item_busca = name_item if tipo == 1 else 'Setor'

        result = html.select(path_map[item_busca])
        if len(result) > 0:
            _tag: Tag = result[0]
            a = _tag.find('a')
            if a:
                href = a.get('href').split('/')
                numbers = [i for i in href if str(i).isnumeric()]

                if tipo == 1:
                    _id = numbers[-1]
                    name = a.find('strong', attrs={'class': 'value'}).text
                elif tipo == 2:
                    map_fiis = {'Setor': 3, 'SubSetor': 5, 'Segmento': 7}
                    _id = href[map_fiis[name_item]]
                    name = href[map_fiis[name_item] + 1]

        return dict(id=_id, nome=self._normalize_name(name))

    @staticmethod
    def _get_descricao(html: BeautifulSoup, tipo) -> str:
        if tipo == 1:
            data = html.select("#company-section")[0].find('span', {'class': 'd-block fw-600 text-main-green-dark'})
        else:
            data = html.select("#fund-section")[0].find_all('strong', {'class': 'value'})[1]
        return data.text

    @staticmethod
    def _request(url: str):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/112.0.0.0 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp

    @staticmethod
    def _normalize_name(value: str) -> str:
        words = value.split('-')
        words = [str(i).title() if len(i) > 2 else i for i in words]
        result = " ".join(words).replace('Imoveis', 'Imóveis')
        return result

    def download_images(self, parent_id: int):
        self._download_image(parent_id, 'avatar')
        self._download_image(parent_id, 'cover')

    @staticmethod
    def _download_image(_id: int, _type: str):
        image_name = Path().joinpath('..').joinpath('images').joinpath('ativos').joinpath(f'{_id}.jpg')
        image_data = requests.get(f'https://statusinvest.com.br/img/company/{_type}/{_id}.jpg').content
        image_name.parent.parent.mkdir(exist_ok=True)
        image_name.parent.mkdir(exist_ok=True)
        with open(image_name, 'wb') as handler:
            handler.write(image_data)
