"""
 @author Marildo Cesar 28/04/2023
"""
from typing import List, Dict
from datetime import date
from model import TipoNota


class Nota:
    def __init__(self, comprovante: int, data_operacao: date, tipo_nota: TipoNota, operacoes: List[Dict]):
        self.comprovante = comprovante
        self.data_operacao = data_operacao
        self.tipo_nota = tipo_nota
        self.operacoes = operacoes
