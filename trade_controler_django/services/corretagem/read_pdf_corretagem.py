import fitz

from services.corretagem.base_ativo import AtivoBase
from services.corretagem.mini_indice import MiniIndice
from typing import List, Dict


class ReadPDFCorretagem:

    def __init__(self):
        self._base_item: AtivoBase

    def read(self, file_name: str):
        with fitz.open(file_name) as doc:
            lines = []
            for page in doc:
                lines += page.get_text().split('\n')

        self._base_item = MiniIndice(lines)
        self._base_item.calcule()

    def operacoes(self) -> List[Dict]:
        return self._base_item.operacoes
