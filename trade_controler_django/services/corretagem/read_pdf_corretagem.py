import fitz

from services.corretagem.base_ativo import AtivoBase
from services.corretagem.mini_indice import MiniIndice
from services.corretagem.bovespa import Bovespa
from services.corretagem.bovespa_anual import BovespaAnual
from typing import List, Dict


class ReadPDFCorretagem:

    def __init__(self):
        self._base_item: AtivoBase

    def read(self, file_name: str):
        with fitz.open(file_name) as doc:
            document = doc
            first_line = doc[0].get_text().split('\n')[0]

            map_class = {
                'COMPROVANTE BOVESPA AÇÕES': Bovespa,
                'NOTA DE CORRETAGEM': BovespaAnual,
                'COMPROVANTE BM&F': MiniIndice
            }

            aclass = map_class[first_line]
            self._base_item = aclass(document)
            self._base_item.calcule()

    def operacoes(self) -> List[Dict]:
        return self._base_item.operacoes
