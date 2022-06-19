import fitz

from services.corretagem.base_ativo import AtivoBase
from services.corretagem.mini_indice import MiniIndice
from services.corretagem.bovespa import Bovespa
from typing import List, Dict


class ReadPDFCorretagem:

    def __init__(self):
        self._base_item: AtivoBase

    def read(self, file_name: str):
        with fitz.open(file_name) as doc:
            lines = []
            for page in doc:
                lines += page.get_text().split('\n')

        map_class = {
            'COMPROVANTE BOVESPA AÇÕES': Bovespa,
            'COMPROVANTE BM&F': MiniIndice
        }

        aclass = map_class[lines[0]]
        self._base_item = aclass(lines)
        self._base_item.calcule()

    def operacoes(self) -> List[Dict]:
        return self._base_item.operacoes
