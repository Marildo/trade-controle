"""
 @author Marildo Cesar 23/04/2023
"""

from typing import Dict, List

import fitz
from fitz import Document

from .investment import Investiment
from .bovespa import BovespaAnual, BMF


class ReadPDFCorretagem:

    def __init__(self):
        self._base_item: Investiment = None

    def read(self, file_name: str):
        with Document(file_name) as doc:
            page = doc[0]
            lines = page.get_text().split('\n')

            if 'WIN' in lines:
                aclass = BMF
            else:
                aclass = BovespaAnual

            self._base_item = aclass(doc)
            self._base_item.load()

    def notas(self) -> List:
        return self._base_item.notas
