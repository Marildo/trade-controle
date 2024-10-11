"""
 @author Marildo Cesar 25/04/2023
"""
import threading
import time
from datetime import datetime
from typing import Tuple, Optional

from webargs import fields
from webargs.flaskparser import parser
from flask import request

from src.settings import logger
from src.model import Ativo, Setor, SubSetor, Segmento, TipoInvestimento, AtivosRepository
from ..services import StatusInvest, YFinanceService, RapidAPI
from .schemas import AtivoSchema


class AtivoController:

    @classmethod
    def readAll(cls):
        data = Ativo().read_by_params({'orderBy': 'nome'})
        response = AtivoSchema().dump(data, many=True)
        return response

    @classmethod  # Dando BO quando cria e ja tenta utilizar
    def find_by_or_save(cls, source_nome: str):
        nome, tipo_id, nome_mapead = cls.map_nome(source_nome)
        if tipo_id.isnumeric():
            ativo = Ativo().read_by_id(tipo_id)
            if not ativo:
                ativo = Ativo(id=tipo_id, nome=nome, codigo=nome, tipo_investimento=TipoInvestimento.INDICE)
                ativo.update()
            return ativo
        else:
            ativo = Ativo.find_by_codigo(nome)
            if ativo:
                return ativo

        ativos = Ativo.find_like_name(nome)
        ativo = [i for i in ativos if i.tipo_ativo == tipo_id]
        if ativo:
            return ativo[0]

        st_invent = StatusInvest()
        logger.info(f'Search by {nome}')
        data = st_invent.find_by_name(nome)
        st_invent.download_images(data[0]['parent_id'])
        for item in data:
            setor = item['setor']
            subsetor = None
            if 'subsetor' in setor:
                subsetor = SubSetor(**setor['subsetor'])
                subsetor.setor_id = setor['id']
                del setor['subsetor']

            setor = Setor(**setor)
            setor.subsetor = subsetor
            setor.update()

            if subsetor:
                subsetor.update()

            segmento = Segmento(**item['segmento'])
            segmento.update()

            if 'tipo_ativo' not in item:
                item['tipo_ativo'] = tipo_id

            del item['segmento']
            del item['setor']
            ativo = Ativo(**item)
            ativo.nome = nome if nome_mapead else item['nome']
            ativo.descricao = item['descricao']
            ativo.setor_id = setor.id
            ativo.segmento_id = segmento.id
            ativo.update()
            logger.info(f'Saved {ativo}')

            ativos = Ativo.find_like_name(nome)
            ativo = [i for i in ativos if i.tipo_ativo == tipo_id]
            if ativo:
                return ativo[0]

            ativo = Ativo.find_by_codigo(nome)
            if ativo:
                return ativo

        raise Exception(f'{source_nome} not found')

    @staticmethod
    def map_nome(full_name: str) -> Tuple[str, Optional[str], bool]:
        _map_name = {
            'FII CSHG LOG': 'CGHG Logística',
            'FII VALOR HE': 'VALORA HEDGE',
            'FII MAXI REN': 'Maxi Renda',
            'VIAVAREJO': 'VIA S.A',
            'IRBBRASIL RE': 'IRBR',
            'CYRELA REALT': 'CYRE3',
            'SID NACIONAL': 'CSN',
            'MAGAZ LUIZA': 'MAGAZINE LUIZA',
            'P.ACUCAR-CBD': 'CIA BRASILEIRA DE DISTRIBUIÇÃO',
            'PETRORIO': 'PETRO RIO',
            'DEXCO': 'DURATEX',
            'SANTANDER': 'SANB',
            'AMERICANAS': 'LAME3',
            'M.DIASBRANCO': 'M.DIAS BRANCO',
            'LOG COM PROP': 'LOG COMMERCIAL',
            'OMEGAENERGIA': 'OMEGA ENERGIA',
            'B3': 'B3SA3',
        }
        _map_type = {'LAME3': 'ON'
                     }
        mapead = False
        splited_name = (full_name
                        .replace('S/A', '').replace('S.A.', '').replace('S.A', '').replace(' SA/', '/')
                        .replace(' PART/', '/')
                        .replace(' METZ/', '/').replace(' MET/', '/')
                        .replace(' ATZ', '')
                        .replace(' BR/', '/')
                        .replace(' N2', '')
                        .replace(' EDJ', '').replace(' EJS', '').replace(' ERS', '')
                        .replace(' ED', '').replace(' EJ', '').replace(' ER', '').replace(' EC', '').replace(' CI', '')
                        ).split('/')
        nome, tipo = splited_name if len(splited_name) > 1 else (splited_name[0], '')
        if nome in _map_name:
            nome = _map_name[nome]
            mapead = True
        if nome in _map_type:
            tipo = _map_type[nome]

        return nome.strip(), tipo.strip(), mapead

    @classmethod
    def register(cls):
        input_schema = {
            'tickers': fields.List(fields.Str(), required=False),
        }
        args = parser.parse(input_schema, request, location='json')
        tickers = args.get('tickers')

        def check_and_register():
            for i in tickers:
                cls.find_by_or_save(i)

        thread = threading.Thread(target=check_and_register)
        thread.start()

        return 200

    @classmethod
    def load_fundamental_data(cls):

        def __load():
            data = Ativo().read_by_params({'tipo_investimento': TipoInvestimento.ACOES})
            rp = RapidAPI()
            for ativo in data:
                try:
                    info = rp.buscar_dados_fundamentalistas(ativo.codigo)
                    if info:
                        ativo = Ativo().read_by_id(ativo.id)
                        ativo.roe = info['roe']
                        ativo.margem_liquida = info['margem_lucro']
                        ativo.preco_lucro = info['preco_lucro']
                        ativo.save()
                except Exception as ex:
                    print(ex)

        thread = threading.Thread(target=__load)
        thread.start()

        return 200

    @classmethod
    def get_top_by_fundamentals(cls):
        data = Ativo().find_top_by_fundamentals()
        response = AtivoSchema().dump(data, many=True)
        return response
