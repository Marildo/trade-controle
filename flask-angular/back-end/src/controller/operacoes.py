"""
 @author Marildo Cesar 25/04/2023
"""

from typing import Dict, List

from .ativos import AtivoController


class OperacaoController:

    @classmethod
    def save_operacoes(cls, operacoes: List[Dict]):
        for item in operacoes:
            ativo = AtivoController.find_by_or_save(item['ativo'])
