import fitz
from typing import List
from datetime import date


class ReadPDFCorretagem:
    DATA_OPERACAO = -5

    def __init__(self):
        self.__lines = []

    def read(self, file_name: str):
        with fitz.open(file_name) as doc:
            for page in doc:
                self.__lines += page.get_text().split('\n')

        begin = self.__locate_index('C/V', self.__lines)
        end = self.__locate_index('PREÇO DE EXERCÍCIO', self.__lines)

        while begin > 0:
            cutting = self.__lines[begin: end]

            ativo = self.__lines[begin - 1]

            qtd_compra = self.__find_qtd_compra(cutting)
            qtd_venda = self.__find_qtd_venda(cutting)
            pm_compra = self.__find_preco_medio_compra(cutting)
            pm_venda = self.__find_preco_medio_venda(cutting)

            print(ativo, qtd_venda, qtd_compra, pm_venda, pm_compra)

            begin = self.__locate_index('C/V', self.__lines, end + 1)
            end = self.__locate_index('PREÇO DE EXERCÍCIO', self.__lines, begin)

    def __locate_index(self, value, cutting: List, start: int = 0) -> int:
        try:
            items = [item for item in cutting if item.startswith(value)]
            return cutting.index(items[0], start)
        except Exception as e:
            return 0

    def __locate_value(self, value, cutting: List) -> str:
        index = self.__locate_index(value, cutting)
        return None if index == 0 else cutting[index]

    def __find_qtd_compra(self, cutting: List) -> int:
        return self.__find_qtd(cutting, 'compra')

    def __find_qtd_venda(self, cutting: List) -> int:
        return self.__find_qtd(cutting, 'venda')

    def __find_qtd(self, cutting: List, tipo: str) -> int:
        value = self.__locate_value(f'Quant. total de {tipo}:', cutting)
        if value:
            return int(value.split(':')[1])

    def __find_preco_medio_compra(self, cutting: List) -> float:
        return self.__find_preco_medio(cutting, 'compra')

    def __find_preco_medio_venda(self, cutting: List) -> float:
        return self.__find_preco_medio(cutting, 'venda')

    def __find_preco_medio(self, cutting: List, tipo: str) -> float:
        index = self.__locate_index(f'Preço médio {tipo}: R$', cutting)
        if index:
            value = cutting[index + 1].replace(',', '.')
            try:
                return float(value)
            except ValueError:
                pass
        return 0

    @property
    def data_operacao(self):
        return self.__lines[self.DATA_OPERACAO]
