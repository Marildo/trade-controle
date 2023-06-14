"""
 @author Marildo Cesar 20/05/2023
"""
import uuid
from typing import List

from src.utils.date_util import str_date
from src.utils.str_util import str_to_float, onnly_numbers
from src.model import TipoNota

from ..investment import Investiment


class BMFSinacor(Investiment):
    DATA_OPERACAO = 5
    COMPROVANTE = 6

    def load(self):

        buffer = []
        _id = 0
        for page in self.document:
            self._lines = page.get_text().split('\n')
            if len(self._lines) == 1:
                continue

            operacoes = buffer

            # j = 0
            # for i in self.lines:
            #     print(j, i)
            #     j += 1

            data_operacao = self.__data_operacao()
            comprovante = self.__find_comprovante()
            tipo_nota = TipoNota.MERCADO_FUTURO

            print(page.number, data_operacao, comprovante)

            begin = self.__locate_index('DAY TRADE', self.lines) - 1
            end = begin + 8

            while begin > 0:
                cutting = self.lines[begin - 1: end]
                _id += 1
                ativo = self.__find_nome_ativo(cutting)
                qtd = self.__find_qtd(cutting)
                pm = self.__find_preco_medio(cutting)
                tipo = cutting[8]

                operacao = dict(id=_id, ativo=ativo, tipo=tipo, qtd=qtd, preco=pm, irpf=0, custos=0, daytrade=True)
                # print(operacao)
                operacoes.append(operacao)

                begin = self.__locate_index('DAY TRADE', self.lines, end + 1) - 1
                end = begin + 8

            if 'C O N T I N U A . . .' in self.lines:
                buffer = operacoes
                continue
            else:
                buffer = []
                _id = 0

            custos = self.__get_custos(operacoes)
            irfp = self.__get_irrf(operacoes)
            self._add_notas(comprovante, data_operacao, tipo_nota, operacoes, irfp, custos)

        print('finish read')

    @staticmethod
    def __locate_index(value, cutting: List, start: int = 0) -> int:
        try:
            items = [item for item in cutting if str(item).__contains__(value)]
            return cutting.index(items[0], start)
        except:
            return -1

    def __data_operacao(self):
        return str_date(self.lines[self.DATA_OPERACAO])

    def __find_comprovante(self) -> int:
        return int(onnly_numbers(self.lines[self.COMPROVANTE]))

    def __get_irrf(self, operacoes: List) -> float:
        irrf_total = 0
        index = self.__locate_index('IRRF Day Trade ( Projeção )', self.lines)
        value = self.lines[index + 5]
        irrf_total = self.parse_float(value)
        return irrf_total

    def __get_custos(self, operacoes: List) -> float:
        taxa_liquidacao = self.__find_taxas(self.lines)
        outras = self.__find_outras_despesas(self.lines)
        custos_total = taxa_liquidacao + outras
        return custos_total

    @staticmethod
    def __find_nome_ativo(cutting: List) -> str:
        _map = {
            'WDO': Investiment.DOLAR,
            'WIN': Investiment.MINI_INDICE
        }
        return _map[cutting[7]]

    @staticmethod
    def __find_qtd(cutting: List) -> int:
        value = cutting[4]
        return int(value.strip(''))

    @staticmethod
    def __find_preco_medio(cutting: List) -> float:
        value = cutting[3]
        value = onnly_numbers(value)
        value = str_to_float(value)
        value = value * 0.0001
        return round(value, 4)

    def __find_taxas(self, cutting: List) -> float:
        index = self.__locate_index('Taxa registro BM&F', cutting)
        value = cutting[index + 5]
        v0 = self.parse_float(value)  # taxa registro
        value = cutting[index + 6]
        v1 = self.parse_float(value)  # taxas BM&F
        value = cutting[index + 4]
        v2 = self.parse_float(value)  # taxa operacional
        return v0 + v1 + v2

    def __find_outras_despesas(self, cutting: List) -> float:
        index = self.__locate_index('Total líquido da nota', cutting)
        v1 = self.parse_float(cutting[index + 1])  # outros
        index = self.__locate_index('Ajuste de posição', cutting)
        v2 = self.parse_float(cutting[index + 1])  # iss
        index = self.__locate_index('Ajuste de posição', cutting)
        v3 = self.parse_float(cutting[index])  # iss 2
        return v1 + v2 + v3
