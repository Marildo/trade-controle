from pathlib import Path
from typing import Tuple, List

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from django.conf import settings

from ativos.models import Ativo, Setor, SubSetor, Segmento
from utils.enums import TipoAtivo
from utils.str_util import StrUtil


class StatusInvest:
    def __init__(self) -> None:
        pass

    def find_by_name(self, name) -> List[Ativo]:
        resp = requests.get(f'https://statusinvest.com.br/home/mainsearchquery?q={name}')
        data = resp.json()
        data = [i for i in data if i['type'] in TipoAtivo.values()]
        result = []
        if 1 == name:
            pass
        for item in data:
            ativo = Ativo(
                id=item['id'],
                parent_id=item['parentId'],
                tipo=item['type'],
                nome=item['name'],
                codigo=item['code'],
                cotacao=StrUtil.str_to_float(item['price']),
                variacao=StrUtil.str_to_float(item['variation'])
            )
            ativo = self._set_properties(ativo)
            result.append(ativo)
        return result

    def _set_properties(self, ativo: Ativo) -> Ativo:
        map_type = {
            1: 'acoes',
            2: 'fundos-imobiliarios'
        }
        url = f'https://statusinvest.com.br/{map_type[ativo.tipo]}/{ativo.codigo}'
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        if ativo.tipo == 1:
            ativo.setor = self._get_propertie(ativo, html, Setor)
            ativo.subsetor = self._get_propertie(ativo, html, SubSetor)
            ativo.segmento = self._get_propertie(ativo, html, Segmento)
        else:
            self._get_propertie(ativo, html, Setor)

        return ativo

    def _get_propertie(self, ativo, html: BeautifulSoup, a_class) -> Tuple[Setor, SubSetor, Segmento]:
        path_map = {
            'setor': 'div.top-info-md-n:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
            'subsetor': 'div.pl-md-2:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
            'segmento': 'div.pl-md-2:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)',
        }
        _id = 0
        name = 'N/A'

        class_name = a_class.__name__.lower()
        result: ResultSet = html.select(path_map[class_name])
        for row in result:
            _tag: Tag = row
            a = _tag.find('a')
            if a:
                href = a.get('href').split('/')
                numbers = [i for i in href if str(i).isnumeric()]
                _id = numbers[-1]
                name = a.find('strong', attrs={'class': 'value'}).text

                if ativo.tipo == 2:
                    ativo.segmento = Segmento(_id, name)

                    names = [i for i in href if not str(i).isnumeric()]

                    name = name if names[-1] == names[-2] else self._normalize_name(names[-2])
                    _id = numbers[-2]
                    ativo.subsetor = SubSetor(_id, name)

                    name = self._normalize_name(names[-3])
                    _id = numbers[-3]
                    ativo.setor = Setor(_id, name)

        return a_class(id=_id, nome=name)

    @staticmethod
    def _normalize_name(value: str) -> str:
        words = value.split('-')
        words = [str(i).title() if len(i) > 2 else i for i in words]
        result = " ".join(words) .replace('Imoveis', 'Imóveis')
        return result

    def download_images(self, ativo: Ativo):
        self._download_image(ativo.parent_id, 'avatar')
        self._download_image(ativo.parent_id, 'cover')

    @staticmethod
    def _download_image(_id: int, _type: str):
        image_name = Path().joinpath(
            settings.STATICFILES_DIRS[0], 'img', 'ativos', _type, f'{_id}.jpg'
        )
        image_data = requests.get(f'https://statusinvest.com.br/img/company/{_type}/{_id}.jpg').content
        with open(image_name, 'wb') as handler:
            handler.write(image_data)
