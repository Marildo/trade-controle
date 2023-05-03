"""
 @author Marildo Cesar 25/04/2023
"""

from typing import Dict, List, Tuple, Optional

from src.model import Ativo, Setor, SubSetor, Segmento

from src.services import StatusInvest


class AtivoController:

    @classmethod  # Dando BO quando cria e ja tenta utilizar
    def find_by_or_save(cls, source_nome: str):
        nome, tipo = cls.map_nome(source_nome)
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
                ativo.descricao = item['nome']
                ativo.setor = setor
                ativo.segmento = segmento
                ativo.save()

            ativos = Ativo.find_like_name(nome)
        ativo = [i for i in ativos if i.tipo_ativo == tipo]
        if ativo:
            return ativo[0]
        return None

    @staticmethod
    def map_nome(full_name: str) -> Tuple[str, Optional[str]]:
        _map_name = {
            'FII CSHG LOG': 'CGHG Logística',
            'FII VALOR HE': 'VALORA HEDGE',
            'FII MAXI REN': 'Maxi Renda',
            'VIAVAREJO': 'VIA S.A',
            'IRBBRASIL RE': 'IRBR',
            'CYRELA REALT': 'CYRELA',
            'SID NACIONAL': 'CSN',
            'MAGAZ LUIZA': 'MAGAZINE LUIZA',
            'P.ACUCAR-CBD': 'CIA BRASILEIRA DE DISTRIBUIÇÃO',
            'PETRORIO': 'PETRO RIO',
            'DEXCO': 'DURATEX',
            'SANTANDER': 'SANB',
            'AMERICANAS': 'LAME3',
            'M.DIASBRANCO': 'M.DIAS BRANCO',
            'LOG COM PROP': 'LOG COMMERCIAL',
            'OMEGAENERGIA': 'OMEGA ENERGIA'
        }
        _map_type = {
            'LAME3': 'ON'
        }
        nome, tipo = (full_name
                      .replace('S/A', '').replace('S.A.', '').replace('S.A', '').replace('SA/', '/')
                      .replace(' PART/', '/')
                      .replace(' METZ/', '/').replace(' MET/', '/')
                      .replace(' ATZ', '')
                      .replace(' BR/', '/')
                      .replace(' N2', '')
                      .replace(' EDJ', '').replace(' EJS', '').replace(' ERS', '')
                      .replace(' ED', '').replace(' EJ', '').replace(' ER', '').replace(' EC', '')
                      ).split('/')
        if nome in _map_name:
            nome = _map_name[nome]
        if nome in _map_type:
            tipo = _map_type[nome]

        return nome.strip(), tipo.strip()
