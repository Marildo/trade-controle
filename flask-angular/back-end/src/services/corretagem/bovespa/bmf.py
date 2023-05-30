"""
 @author Marildo Cesar 20/05/2023
"""
import uuid
from typing import List

from src.utils.date_util import str_date
from src.utils.str_util import str_to_float, onnly_numbers
from src.model import TipoNota

from ..investment import Investiment


class BMF(Investiment):
    DATA_OPERACAO = 5
    COMPROVANTE = 6

    def load(self):

        buffer = []

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

            _id = 0
            while begin > 0:
                cutting = self.lines[begin - 1: end]
                _id += 1
                ativo = self.__find_nome_ativo(cutting)
                qtd = self.__find_qtd(cutting)
                pm = self.__find_preco_medio(cutting)
                tipo = cutting[8]

                operacao = dict(id=_id, ativo=ativo, tipo=tipo, qtd=qtd, preco=pm, irpf=0, custos=0)
                # print(operacao)
                operacoes.append(operacao)

                begin = self.__locate_index('DAY TRADE', self.lines, end + 1) - 1
                end = begin + 8

            if 'C O N T I N U A . . .' in self.lines:
                buffer = operacoes
                continue
            else:
                buffer = []

            self.__rateia_custos(operacoes)
            self.__rateia_irrf(operacoes)
            self._add_notas(comprovante, data_operacao, tipo_nota, operacoes)

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

    def __rateia_irrf(self, operacoes: List) -> None:
        irrf_total = 0
        index = self.__locate_index('IRRF Day Trade ( Projeção )', self.lines)
        value = self.lines[index + 5]
        irrf_total = self.parse_float(value)

        self.__rateia_daytrade_irrf(operacoes, irrf_total)

    @staticmethod
    def __rateia_daytrade_irrf(operacoes: List, irrf: float):
        if irrf <= 0:
            return

        ops = [i for i in operacoes if i['tipo'] == 'V']
        total = sum((item['preco'] * item['qtd'] for item in ops))
        for item in ops:
            rs = item['preco'] * item['qtd']
            percentual = rs * 100 / total
            item['irpf'] = round(irrf * (percentual * 0.01), 4)

    def __rateia_custos(self, operacoes: List) -> None:
        taxa_liquidacao = self.__find_taxas(self.lines)
        iss = self.__find_iss(self.lines)
        outras = self.__find_outras_despesas(self.lines)
        custos_total = taxa_liquidacao + iss + outras
        if custos_total > 0:
            ops = [i for i in operacoes if i['tipo'] == 'V']
            total = sum((item['preco'] * item['qtd'] for item in ops))
            for op in ops:
                rs = op['preco'] * op['qtd']
                percentual = rs * 100 / total
                op['custos'] = round(custos_total * (percentual * 0.01), 2)

    @staticmethod
    def __find_nome_ativo(cutting: List) -> str:
        _map = {
            'WDO': 'WDO/900000',
            'WIN': 'WIN/800000'
        }
        return _map[cutting[7]]

    @staticmethod
    def __find_qtd(cutting: List) -> int:
        value = cutting[4]
        return int(value.strip(''))

    @staticmethod
    def __find_preco_medio(cutting: List) -> float:
        value = cutting[1]
        value = onnly_numbers(value)
        value = round(str_to_float(value) * 0.01, 2)
        return value

    def __find_taxas(self, cutting: List) -> float:
        index = self.__locate_index('Taxa registro BM&F', cutting)
        value = cutting[index + 5]
        v0 = self.parse_float(value)
        value = cutting[index + 6]
        v1 = self.parse_float(value)
        return v1 + v0

    def __find_iss(self, cutting: List) -> float:
        index = self.__locate_index('I.S.S', cutting)
        value = cutting[index + 17]
        return self.parse_float(value)

    def __find_outras_despesas(self, cutting: List) -> float:
        index = self.__locate_index('Outros', cutting)
        value = cutting[index + 6]
        return self.parse_float(value)
