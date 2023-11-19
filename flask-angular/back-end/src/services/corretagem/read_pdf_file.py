"""
 @author Marildo Cesar 23/04/2023
"""

from typing import  List

from fitz import Document

from .investment import Investiment
from .bovespa import BovespaSinacor, BovespaDiaria
from .bmf import BMFSinacor, BMFDiaria


class ReadPDFCorretagem:

    def __init__(self):
        self._base_item: Investiment = None

    def read(self, file_name: str):
        with Document(file_name) as doc:
            page = doc[0]
            lines = page.get_text().split('\n')

            if 'WIN' in lines:
                aclass = BMFSinacor
            elif 'COMPROVANTE BM&F' in lines:
                aclass = BMFDiaria
            elif 'COMPROVANTE BOVESPA AÇÕES' in lines:
                aclass = BovespaDiaria
            elif 'NOTA DE CORRETAGEM' in lines:
                aclass = BovespaSinacor
            else:
                raise Exception('Não identificado o tipo da nota')

            self._base_item = aclass(doc)
            self._base_item.load()

    def notas(self) -> List:
        return self._base_item.notas
