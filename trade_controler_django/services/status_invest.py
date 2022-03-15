from pathlib import Path
from typing import Tuple, List

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from django.conf import settings

from acoes.models import Acao, Setor, SubSetor, Segmento
from utils.str_util import StrUtil


class StatusInvest:
    def __init__(self) -> None:
        pass

    def find_by_name(self, name) -> List[Acao]:
        resp = requests.get(f'https://statusinvest.com.br/home/mainsearchquery?q={name}')
        data = resp.json()
        data = [i for i in data if i['type'] == 1]
        result = []
        for item in data:
            acao = Acao(
                id=item['id'],
                parent_id=item['parentId'],
                nome=item['name'],
                codigo=item['code'],
                cotacao=StrUtil.str_to_float(item['price']),
                variacao=StrUtil.str_to_float(item['variation'])
            )
            acao = self._set_properties(acao)
            result.append(acao)
        return result

    def _set_properties(self, acao: Acao) -> Acao:
        url = f'https://statusinvest.com.br/acoes/{acao.codigo}'
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        acao.setor = self._get_propertie(html, Setor)
        acao.subsetor = self._get_propertie(html, SubSetor)
        acao.segmento = self._get_propertie(html, Segmento)
        return acao

    @staticmethod
    def _get_propertie(html: BeautifulSoup, a_class) -> Tuple[Setor, SubSetor, Segmento]:
        path_map = {
            'setor': 'div.top-info-md-n:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
            'subsetor': 'div.pl-md-2:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
            'segmento': 'div.pl-md-2:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
        }

        class_name = a_class.__name__.lower()
        result: ResultSet = html.select(path_map[class_name])
        _tag: Tag = result.pop()
        a = _tag.find('a')
        name = a.find('strong', attrs={'class': 'value'}).text

        href = a.get('href').split('/')
        numbers = [i for i in href if str(i).isnumeric()]
        _id = numbers[-1]

        return a_class(id=_id, nome=name)

    def download_images(self, acao: Acao):
        self._download_image(acao.parent_id, 'avatar')
        self._download_image(acao.parent_id, 'cover')

    @staticmethod
    def _download_image(_id: int, _type: str):
        image_name = Path().joinpath(
            settings.STATICFILES_DIRS[0], 'img', 'acoes', _type, f'{_id}.jpg'
        )
        image_data = requests.get(f'https://statusinvest.com.br/img/company/{_type}/{_id}.jpg').content
        with open(image_name, 'wb') as handler:
            handler.write(image_data)
