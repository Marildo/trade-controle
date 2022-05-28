from typing import List, Dict
from services.corretagem.base_ativo import AtivoBase


class Bovespa(AtivoBase):
    DATA_OPERACAO = -5

    def calcule(self):
        begin = self.__locate_index('C/V', self.__lines)
        end = self.__locate_index('PREÇO DE EXERCÍCIO', self.__lines)

        data_operacao = self.__data_operacao()

        while begin > 0:
            cutting = self.__lines[begin - 1: end]

            ativo = self.find_nome_ativo(cutting)
            qtd_compra = self.__find_qtd_compra(cutting)
            qtd_venda = self.__find_qtd_venda(cutting)
            pm_compra = self.__find_preco_medio_compra(cutting)
            pm_venda = self.__find_preco_medio_venda(cutting)

            operacao = dict(ativo=ativo, qtd_compra=qtd_compra, qtd_venda=qtd_venda, pm_compra=pm_compra,
                            pm_venda=pm_venda, data_operacao=data_operacao)

            self._add_operacao(operacao)

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

    def find_nome_ativo(self, cutting: List) -> str:
        value = cutting[0]
        value = value.split('-')[1]
        value = value.split(' ')[1]
        return value

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

    def __data_operacao(self):
        return self.__lines[self.DATA_OPERACAO]
