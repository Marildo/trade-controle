"""
 @author Marildo Cesar 15/06/2023
"""
from typing import List

from src.utils.date_util import str_date
from src.utils.str_util import str_to_float, onnly_numbers
from src.model import TipoNota

from ..investment import Investiment


class BovespaDiaria(Investiment):

    def load(self):

        irfp = 0
        custos = 0
        tipo_nota = TipoNota.ACOES

        for page in self.document:
            self._lines = page.get_text().split('\n')
            if len(self._lines) == 1:
                continue

            operacoes = []

            # j = 0
            # for i in self.lines:
            #     print(j, i)
            #     j += 1

            data_operacao = self.__data_operacao()
            comprovante = self.__find_comprovante()

            # print(page.number, data_operacao, comprovante)

            if page.number == 0:
                custos = self.__get_custos(operacoes)
                irfp = self.__get_irrf(operacoes)

            begin = self.__locate_index('C/V', self.lines)
            end = self.__locate_index('C/V', self.lines, begin + 2) - 1

            _id = 0
            while begin > 0:
                cutting = self.lines[begin - 1: end]
                _id += 1
                ativo = self.__find_nome_ativo(cutting)

                begin_int = self.__locate_index('BOVESPA 1', cutting) - 1
                end_int = begin_int + 7
                while begin_int > 0:
                    cutting_item = cutting[begin_int: end_int]
                    qtd = self.__find_qtd(cutting_item)
                    pm = self.__find_preco_medio(cutting_item)
                    tipo = cutting_item[0][0]

                    operacao = dict(id=_id, ativo=ativo, tipo=tipo, qtd=qtd, preco=pm, daytrade=None)

                    find_pair = [item for item in operacoes if
                                 item['ativo'] == ativo and item['qtd'] == qtd
                                 and item['tipo'] != tipo and item['daytrade'] is None]

                    if find_pair:
                        operacao['daytrade'] = True
                        find_pair[0]['daytrade'] = True

                    operacoes.append(operacao)

                    begin_int = self.__locate_index('BOVESPA 1', cutting, begin_int + 2) - 1
                    end_int = begin_int + 7

                begin = self.__locate_index('C/V', self.lines, end + 1)
                end = self.__locate_index('C/V', self.lines, begin + 2) - 1

            self._add_notas(comprovante, data_operacao, tipo_nota, operacoes, irfp, custos)

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

    def __get_irrf(self, operacoes: List) -> float:
        result = 0
        index = self.__locate_index('IRRF Day Trade', self.lines)
        if index > 0:
            value = self.lines[index + 1]
            result += self.parse_float(value)

        index = self.__locate_index('IRRF Operação Comum', self.lines)
        if index > 0:
            value = self.lines[index + 1]
            result += self.parse_float(value)

        return result

    def __get_custos(self, operacoes: List) -> float:
        emulomentos = self.__find_emulumentos(self.lines)
        taxa_liquidacao = self.__find_taxa_liquidacao(self.lines)
        clearing = self.__find_clearing(self.lines)
        iss = self.__find_iss(self.lines)
        outras = self.__find_outras_despesas(self.lines)
        custos_total = emulomentos + taxa_liquidacao + clearing + iss + outras
        return custos_total

    @staticmethod
    def __find_nome_ativo(cutting: List) -> str:
        value = cutting[0]
        split = value.split('-')
        codigo = split[0].strip()
        codigo = codigo[:-1] if codigo[-1] == 'F' and len(codigo) == 6 else codigo
        #tipo = split[-1].split(' ')[0]
        value = f'{codigo}/ '
        return value

    @staticmethod
    def __find_qtd(cutting: List) -> int:
        value = cutting[2]
        return int(value.strip(''))

    @staticmethod
    def __find_preco_medio(cutting: List) -> float:
        value = cutting[3]
        value = onnly_numbers(value)
        value = round(str_to_float(value) * 0.01, 2)
        return value

    def __find_taxa_liquidacao(self, cutting: List) -> float:
        index = self.__locate_index('de Liquidação', cutting)
        if index < 0:
            return 0
        value = cutting[index + 1]
        return self.parse_float(value)

    def __find_emulumentos(self, cutting: List) -> float:
        index = self.__locate_index('Emolumentos', cutting)
        value = cutting[index + 1]
        return self.parse_float(value)

    def __find_clearing(self, cutting: List) -> float:
        index = self.__locate_index('Clearing', cutting)
        if index < 0:
            return 0
        sub = cutting[index + 1: len(cutting)]
        index = self.__locate_index('Clearing', sub)
        if index < 0:
            return 0
        value = sub[index + 2]
        return self.parse_float(value)

    def __find_iss(self, cutting: List) -> float:
        result = 0
        index = self.__locate_index('ISS', cutting)
        value = cutting[index + 1]
        result += self.parse_float(value)

        index = self.__locate_index('PIS', cutting)
        value = cutting[index + 1]
        result += self.parse_float(value)

        index = self.__locate_index('COFINS', cutting)
        value = cutting[index + 1]
        result += self.parse_float(value)

        return result

    def __find_outras_despesas(self, cutting: List) -> float:
        result = 0
        index = self.__locate_index('Outros', cutting)
        if index:
            value = cutting[index + 1]
            result += self.parse_float(value)

        index = self.__locate_index('Taxa Registro', cutting)
        if index:
            value = cutting[index + 1]
            result += self.parse_float(value)

        index = self.__locate_index('Taxa Operacional', cutting)
        if index:
            value = cutting[index + 1]
            result += self.parse_float(value)

        index = self.__locate_index('Taxa de termo/opções', cutting)
        if index:
            value = cutting[index + 1]
            result += self.parse_float(value)

        return result
