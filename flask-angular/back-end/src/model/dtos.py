"""
 @author Marildo Cesar 28/04/2023
"""
from typing import List, Dict
from datetime import date
from model.enums import TipoNota


class Nota:
    def __init__(self,
                 comprovante: int, data_operacao: date, tipo_nota: TipoNota, operacoes: List[Dict],
                 irfp: float = 0, custos: float = 0):
        self.comprovante = comprovante
        self.data_operacao = data_operacao
        self.tipo_nota = tipo_nota
        self.operacoes = operacoes
        self.file = None
        self.irfp = irfp
        self.custos = custos

    def __str__(self):
        return f'Comprovante: {self.comprovante} - data: {self.data_operacao}'
