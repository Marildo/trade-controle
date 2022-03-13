from typing import Tuple

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from acoes.models import Acao, Setor, SubSetor, Segmento
from utils.str_util import StrUtil

class StatusInvest:
    def __init__(self) -> None:
        pass

    def find_by_name(self, name) -> Acao:
        resp = requests.get(f'https://statusinvest.com.br/home/mainsearchquery?q={name}')
        data = resp.json()[0]
        acao = Acao(
            id=data['parentId'],
            nome=data['name'],
            codigo=data['code'],
            cotacao=StrUtil.str_to_float(data['price']),
            variacao=StrUtil.str_to_float(data['variation'])
        )
        acao = self._set_properties(acao)

        return acao

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
