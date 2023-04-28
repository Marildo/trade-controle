"""
 @author Marildo Cesar 22/04/2023
"""

from typing import List, Dict
from abc import ABC, abstractmethod

from fitz import Document
from src.utils.str_util import str_to_float, onnly_numbers


class Investiment(ABC):

    def __init__(self, document: Document):
        self.__document = document
        self._lines = []
        self.__operacaoes = []

    @abstractmethod
    def load(self):
        pass

    @property
    def document(self):
        return self.__document

    @property
    def lines(self):
        return self._lines

    def _add_operacao(self, operacaos: List[Dict]):
        self.__operacaoes += operacaos

    @property
    def operacoes(self) -> List[Dict]:
        return self.__operacaoes

    @staticmethod
    def parse_float(value: str) -> float:
        xvalue = onnly_numbers(value)
        xvalue = str_to_float(xvalue)
        xvalue = round(xvalue * 0.01, 2)
        return xvalue
