"""
 @author Marildo Cesar 25/04/2023
"""

from typing import Dict, List, Tuple, Optional

from src.model import Ativo, Setor, SubSetor, Segmento

from src.services import StatusInvest


class AtivoController:

    @classmethod
    def find_by_or_save(cls, nome: str):
        nome, tipo = cls.map_nome(nome)
        ativos = Ativo.find_like_name(nome)
        if not ativos:
            st_invent = StatusInvest()
            data = st_invent.find_by_name(nome)
            st_invent.download_images(data[0]['parent_id'])
            for item in data:
                setor = item['setor']
                subsetor = None
                if 'subsetor' in setor:
                    subsetor = SubSetor(**setor['subsetor'])
                    subsetor.setor_id = setor['id']
                    subsetor.save()
                    del setor['subsetor']

                setor = Setor(**setor)
                setor.subsetor = subsetor
                setor.save()

                segmento = Segmento(**item['segmento'])
                segmento.save()

                if 'tipo_ativo' not in item:
                    item['tipo_ativo'] = tipo

                ativo = Ativo(**item)
                ativo.nome = nome
                ativo.setor = setor
                ativo.segmento = segmento
                ativo.save()

        ativo = [i for i in ativos if i.tipo_ativo == tipo]
        if ativo:
            return ativo[0]
        return None

    @staticmethod
    def map_nome(full_name: str) -> Tuple[str, Optional[str]]:
        _map = {
            'FII CSHG LOG': 'CGHG Logística',
            'FII VALOR HE': 'VALORA HEDGE',
            'VIAVAREJO': 'VIA S.A',
            'IRBBRASIL RE': 'IRBR',
            'CYRELA REALT': 'CYRELA',
            'SID NACIONAL': 'CSN',
            'MAGAZ LUIZA': 'MAGAZINE LUIZA',
            'P.ACUCAR-CBD': 'CIA BRASILEIRA DE DISTRIBUIÇÃO',
            'PETRORIO': 'PETRO RIO',
            'DEXCO': 'DURATEX'
        }
        nome, tipo = (full_name
                      .replace('S/A', '')
                      .replace('S.A.', '')
                      .replace('S.A', '')
                      .replace(' PART', '')
                      .replace(' METZ', '')
                      .replace(' MET', '')
                      .replace(' N2', '')
                      ).split('/')
        if nome in _map:
            nome = _map[nome]
        return nome.strip(), tipo.strip()
