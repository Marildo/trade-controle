from enum import IntEnum

class TipoAtivo(IntEnum):
    ACOES = 1
    FIIS = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]