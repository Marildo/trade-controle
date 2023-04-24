"""
 @author Marildo Cesar 23/04/2023
"""

from typing import Dict, List
import PyPDF2
from PyPDF2 import PdfReader

from .investment import Investiment
from .bovespa import BovespaAnual


class ReadPDFCorretagem:

    def __init__(self):
        self._base_item: Investiment = None

    def read(self, file_name: str):
        with open(file_name, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            first_line = reader.pages[0].extract_text().split('\n')[0]

            map_class = {
                # 'COMPROVANTE BOVESPA AÇÕES': Bovespa,
                'NOTA DE CORRETAGEM': BovespaAnual,
                # 'COMPROVANTE BM&F': MiniIndice
            }

            aclass = map_class[first_line]
            self._base_item = aclass(reader)
            self._base_item.load()

    def operacoes(self) -> List[Dict]:
        return self._base_item.operacoes
