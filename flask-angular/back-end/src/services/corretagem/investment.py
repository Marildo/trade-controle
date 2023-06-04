"""
 @author Marildo Cesar 22/04/2023
"""

from typing import List, Dict
from abc import ABC, abstractmethod
from datetime import date

from fitz import Document

from src.utils.str_util import str_to_float, onnly_numbers
from src.model.dtos import Nota


class Investiment(ABC):
    MINI_INDICE = 'WIN/800000'
    DOLAR = 'WDO/900000'

    def __init__(self, document: Document):
        self.__document = document
        self._lines = []
        self._notas = []

    @abstractmethod
    def load(self):
        pass

    @property
    def document(self):
        return self.__document

    @property
    def lines(self):
        return self._lines

    def _add_notas(self,
                   comprovante: int, data_operacao: date, tipo_nota, operacoes: List[Dict],
                   irfp: float = 0, custos: float = 0):
        nota = Nota(comprovante, data_operacao, tipo_nota, operacoes, irfp, custos)
        self._notas.append(nota)

    @property
    def notas(self):
        return self._notas

    @staticmethod
    def parse_float(value: str) -> float:
        xvalue = onnly_numbers(value)
        xvalue = str_to_float(xvalue)
        xvalue = round(xvalue * 0.01, 2)
        return xvalue
