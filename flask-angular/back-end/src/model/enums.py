"""
 @author Marildo Cesar 24/04/2023
"""

from enum import IntEnum
from typing import List, Tuple


class BaseIntEnum(IntEnum):
    @classmethod
    def values(cls) -> List:
        return [key.value for key in cls]


class TipoAtivo(BaseIntEnum):
    ACOES = 1
    FIIS = 2
    INDICE = 3


class TipoCarteira(BaseIntEnum):
    VARIAVEL = 1
    FIXA = 2


class TipoNota(BaseIntEnum):
    NA = 0
    ACOES = 1
    FUTURO = 2
