"""
 @author Marildo Cesar 25/04/2023
"""
from datetime import datetime
from typing import Tuple, Optional

from src.settings import logger
from src.model import Ativo, Setor, SubSetor, Segmento, TipoInvestimento

from src.services import StatusInvest, YFinanceService
from .schemas import AtivoSchema


class AtivoController:

    @classmethod
    def readAll(cls):
        data = Ativo().read_by_params({})
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

    def updateIndices(self):
        def dif_time(dt0, dt1):
            diff = dt0 - dt1
            time_diff = diff.total_seconds() / 3600
            return time_diff

        ativos = Ativo.find_like_name('INDICE')
        ativos = [i for i in ativos if dif_time(datetime.today(), i.update_at) > 1]
        for a in ativos:
            YFinanceService.update_indices(a)
