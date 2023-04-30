"""
 @author Marildo Cesar 23/04/2023
"""

from typing import Dict, List

import fitz
from fitz import Document


from .investment import Investiment
from .bovespa import BovespaAnual


class ReadPDFCorretagem:

    def __init__(self):
        self._base_item: Investiment = None

    def read(self, file_name: str):
        with Document(file_name) as doc:
            page = doc[0]
            title = page.get_text().split('\n')[0].strip()

            map_class = {
                # 'COMPROVANTE BOVESPA AÇÕES': Bovespa,
                'NOTA DE CORRETAGEM': BovespaAnual,
                # 'COMPROVANTE BM&F': MiniIndice
            }

            print(title)

            aclass = map_class[title]
            self._base_item = aclass(doc)
            self._base_item.load()

    def notas(self) -> List:
        return self._base_item.notas
