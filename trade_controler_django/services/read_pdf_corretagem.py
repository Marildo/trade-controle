import fitz
from typing import List, Dict
from abc import ABC, abstractmethod, abstractproperty
from decimal import Decimal
from utils import StrUtil


class AtivoBase(ABC):

    def __init__(self, lines: List):
        self.__lines = lines

    @property
    def lines(self):
        return self.__lines

    @abstractmethod
    def calcule(self):
        pass

    @abstractmethod
    def operacoes(self) -> List[Dict]:
        pass


class MiniIndice(AtivoBase):

    def calcule(self):
        for i in self.lines:
            print(i)

        operacao = {}

        value = self.__get_value_by_next('Total de negócios')
        resultado = StrUtil.str_to_float(value.replace('R$ ', ''))

        operacao['pm_compra'] = StrUtil.str_to_float(self.__get_value_by_next('Preço médio compra: R$ '))
        operacao['pm_venda'] = operacao['pm_compra'] + resultado

        value = StrUtil.onnly_numbers(self.__get_value_by_next('IRRF Day Trade (Projeção)'))
        operacao['IRRF'] = StrUtil.str_to_float(value) * -0.01

        value = StrUtil.onnly_numbers(self.__get_value_by_next('Custos'))
        operacao['custos'] = StrUtil.str_to_float(value) * -0.01

        key = 'Quant. total de venda:'
        qtd = max([int(StrUtil.onnly_numbers(item)) for item in self.lines if item.startswith(key)])
        operacao['qtd_compra'] = qtd
        operacao['qtd_venda'] = qtd

        index = self.lines.index('Data de referência')
        operacao['data_operacao'] = self.lines[index - 1]

        operacao['ativo'] = 'WINFUT'

        print('Resultado :', operacao['pm_venda'] - operacao['pm_compra'] + operacao['custos'] + operacao['IRRF'])
        print(operacao)

    def __get_value_by_next(self, key):
        index = self.lines.index(key)
        return self.lines[index + 1]

    def operacoes(self) -> List[Dict]:
        pass


class Acoes(AtivoBase):

    def calcule(self):
        begin = self.__locate_index('C/V', self.__lines)
        end = self.__locate_index('PREÇO DE EXERCÍCIO', self.__lines)

        while begin > 0:
            cutting = self.__lines[begin - 1: end]

            ativo = self.find_nome_ativo(cutting)
            qtd_compra = self.__find_qtd_compra(cutting)
            qtd_venda = self.__find_qtd_venda(cutting)
            pm_compra = self.__find_preco_medio_compra(cutting)
            pm_venda = self.__find_preco_medio_venda(cutting)

            # self.__add_operacao(ativo=ativo, pm_compra=pm_compra, pm_venda=pm_venda, qtd_compra=qtd_compra, qtd_venda=qtd_venda)

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


class ReadPDFCorretagem:
    DATA_OPERACAO = -5

    def __init__(self):
        self.__operacoes = []

    def read(self, file_name: str):
        with fitz.open(file_name) as doc:
            lines = []
            for page in doc:
                lines += page.get_text().split('\n')

        ativo = MiniIndice(lines)
        ativo.calcule()

    def __add_operacao(self, ativo: str, pm_compra: float, pm_venda: float, qtd_compra: float, qtd_venda: float):
        # ativo = Ativo.search(ativo)[0]
        # operacao = Operacao()
        # operacao.ativo = ativo
        # operacao.pm_compra = pm_compra
        # operacao.pm_venda = pm_venda
        # operacao.qtd_compra = qtd_compra
        # operacao.qtd_venda = qtd_venda
        # operacao.data_compra = self.data_operacao
        # operacao.daytrade = qtd_compra == qtd_venda
        self.__operacoes.append({})

    # @property
    # def data_operacao(self):
    #     return self.__lines[self.DATA_OPERACAO]
    #
    #   @property
    #   def operacoes(self) -> List[Dict]:
    #      return self.__operacoes
