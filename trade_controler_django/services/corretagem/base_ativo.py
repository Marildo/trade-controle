from typing import List, Dict
from abc import ABC, abstractmethod


class AtivoBase(ABC):

    def __init__(self, document):
        self.__document = document
        self._lines = []
        self.__operacaoes = []

    @property
    def document(self):
        return self.__document

    @property
    def lines(self):
        return self._lines

    def load_lines(self):
        for page in self.__document:
            self._lines += page.get_text().split('\n')

    @abstractmethod
    def calcule(self):
        pass

    def _add_operacao(self, operacao: Dict):
        same_op = lambda i: i['ativo'] == operacao['ativo'] and i['comprovante'] == operacao['comprovante'] \
                            and i['qtd_compra'] != i['qtd_venda'] and operacao['qtd_compra'] != operacao['qtd_venda']
        ops = [item for item in self.__operacaoes if same_op(item)]
        if ops:
            item = ops[-1]
            if operacao['pm_compra'] > 0:
                total = operacao['pm_compra'] * operacao['qtd_compra'] + item['pm_compra'] * item['qtd_compra']
                item['qtd_compra'] += operacao['qtd_compra']
                item['pm_compra'] = round(total / item['qtd_compra'], 3)
            elif operacao['pm_venda'] > 0:
                total = operacao['pm_venda'] * operacao['qtd_venda'] + item['pm_venda'] * item['qtd_venda']
                item['qtd_venda'] += operacao['qtd_venda']
                item['pm_venda'] = round(total / item['qtd_venda'], 3)
        else:
            self.__operacaoes.append(operacao)

    @property
    def operacoes(self) -> List[Dict]:
        return self.__operacaoes
