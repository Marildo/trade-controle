from typing import List, Dict
from abc import ABC, abstractmethod


class AtivoBase(ABC):

    def __init__(self, lines: List):
        self.__lines = lines
        self.__operacaoes = []

    @property
    def lines(self):
        return self.__lines

    @abstractmethod
    def calcule(self):
        pass

    def _add_operacao(self, operacao: Dict):
        self.__operacaoes.append(operacao)

    @property
    def operacoes(self) -> List[Dict]:
        return self.__operacaoes
