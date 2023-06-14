"""
 @author Marildo Cesar 04/06/2023
"""
import uuid
from typing import List

from src.utils.date_util import str_date
from src.utils.str_util import str_to_float, onnly_numbers
from src.model import TipoNota

from services.corretagem.investment import Investiment


class BMFDiaria(Investiment):
    def load(self):

        tipo_nota = TipoNota.MERCADO_FUTURO
        irfp = 0
        custos = 0

        _id = 0
        operacoes = []
        for page in self.document:
            self._lines = page.get_text().split('\n')
            if len(self._lines) == 1:
                continue

            j = 0
            for y in self.lines:
                print(j, ';', y)
                j += 1

            data_operacao = self.__data_operacao()
            comprovante = self.__find_comprovante()

            print(page.number, data_operacao, comprovante)

            if page.number == 0:
                custos = self.__get_custos(operacoes)
                irfp = self.__get_irrf(operacoes)

            begin = self.__locate_index('DAY TRADE', self.lines) - 4
            end = begin + 7

            while begin > 0:
                cutting = self.lines[begin: end]
                _id += 1
                ativo = self.__find_nome_ativo(cutting)
                qtd = self.__find_qtd(cutting)
                pm = self.__find_preco_medio(cutting)
                tipo = cutting[0][0]

                operacao = dict(id=_id, ativo=ativo, tipo=tipo, qtd=qtd, preco=pm, irpf=0, custos=0, daytrade=True)
                # print(operacao)
                operacoes.append(operacao)

                begin = self.__locate_index('DAY TRADE', self.lines, end) - 4
                end = begin + 7

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
        index = self.__locate_index('Data de referência', self.lines) - 1
        return str_date(self.lines[index])

    def __find_comprovante(self) -> int:
        index = self.__locate_index('Comprovante', self.lines) + 1
        return int(onnly_numbers(self.lines[index]))

    def __get_custos(self, operacoes: List) -> float:
        taxa_liquidacao = self.__find_taxas(self.lines)
        outras = self.__find_outras_despesas(self.lines)
        custos_total = taxa_liquidacao + outras
        return custos_total

    @staticmethod
    def __find_nome_ativo(cutting: List) -> str:
        value = cutting[1][0]
        if value in ('G', 'J', 'M', 'Q', 'V', 'Z'):
            return Investiment.MINI_INDICE

        raise Exception('Nome de ativo não mapeado')

    @staticmethod
    def __find_qtd(cutting: List) -> int:
        value = cutting[2]
        return int(value.strip(''))

    @staticmethod
    def __find_preco_medio(cutting: List) -> float:
        value = cutting[3]
        value = onnly_numbers(value)
        value = str_to_float(value)
        value = value * 0.0001
        return round(value, 4)

    def __find_taxas(self, cutting: List) -> float:
        index = self.__locate_index('Taxa Registro BMF', cutting)
        value = cutting[index + 1]
        v0 = self.parse_float(value)

        index = self.__locate_index('Taxa Emolumentos BMF', cutting)
        value = cutting[index + 1]
        v1 = self.parse_float(value)

        index = self.__locate_index('Taxa Operacional', cutting)
        value = cutting[index + 1]
        v2 = self.parse_float(value)

        return v0 + v1 + v2

    def __find_outras_despesas(self, cutting: List) -> float:
        index = self.__locate_index('Outros', cutting)
        v1 = self.parse_float(cutting[index - 1])

        index = self.__locate_index('ISS', cutting)
        v2 = self.parse_float(cutting[index + 1])

        return v1 + v2

    def __get_irrf(self, operacoes: List) -> float:
        index = self.__locate_index('IRRF Day Trade (Projeção)', self.lines)
        value = self.lines[index + 1]
        irrf_total = self.parse_float(value)
        return irrf_total
