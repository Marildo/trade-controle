from enum import IntEnum
from typing import List, Tuple


class TipoAtivo(IntEnum):
    ACOES = 1
    FIIS = 2

    @classmethod
    def choices(cls) -> List[Tuple]:
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values(cls) -> List:
        return [key.value for key in cls]
