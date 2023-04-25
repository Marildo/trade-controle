"""
 @author Marildo Cesar 23/04/2023
"""

from typing import List

from ..investment import Investiment
from src.utils.date_util import str_date
from src.utils.str_util import str_to_float, onnly_numbers


class BovespaAnual(Investiment):
    DATA_OPERACAO = 4
    COMPROVANTE = 6

    def load(self):
        page_count = 0
        for page in self.document.pages:
            page_count += 1
            print('page', page_count, '#' * 80)
            self._lines = page.extract_text().split('\n')

            j = 0
            for i in self.lines:
                print(j, i)
                j += 1

            data_operacao = self.__data_operacao()
            comprovante = self.__find_comprovante()

            end = self.__locate_index('BOVESPA 1', self.lines)
            begin = end - 7

            while begin > 0:
                cutting = self.lines[begin - 1: end]

                ativo = self.__find_nome_ativo(cutting)
                qtd = self.__find_qtd(cutting)
                pm = self.__find_preco_medio(cutting)

                its_buy = cutting[- 1] == 'C'

                operacao = dict(ativo=ativo, tipo=cutting[- 1], qtd=qtd, preco=pm,
                                data_operacao=data_operacao, comprovante=comprovante, irpf=0,
                                custos=0)

                self._add_operacao(operacao)

                end = self.__locate_index('BOVESPA 1', self.lines, end + 1)
                begin = end - 7

            self.__rateia_custos()
            self.__rateia_irrf()

    @staticmethod
    def __locate_index(value, cutting: List, start: int = 0) -> int:
        try:
            items = [item for item in cutting if item.startswith(value)]
            return cutting.index(items[0], start)
        except:
            return 0

    def __data_operacao(self):
        return str_date(self.lines[self.DATA_OPERACAO])

    def __find_comprovante(self) -> int:
        return int(self.lines[self.COMPROVANTE])

    def __rateia_irrf(self) -> None:
        index = self.__locate_index('IRRF Day Trade', self.lines)
        if index:
            value = self.lines[index + 1]
            value = onnly_numbers(value)
            irrf_total = round(str_to_float(value) * 0.0001, 2)
            if irrf_total > 0:
                has_irrf = lambda item: item['qtd_compra'] == item['qtd_venda'] and item['pm_compra'] < item['pm_venda']
                ops = [item for item in self.operacoes if has_irrf(item)]
                if ops:
                    resultado_total = sum(((item['pm_venda'] - item['pm_compra']) * item['qtd_compra'] for item in ops))
                    for op in ops:
                        rs = (op['pm_venda'] - op['pm_compra']) * op['qtd_compra']
                        percentual = rs * 100 / resultado_total
                        op['irpf'] = round(irrf_total * (percentual * 0.01), 2)

        index = self.__locate_index('I.R.R.F. s/ operações', self.lines)
        if index:
            value = self.parse_float(self.lines[index + 1])
            op = [i for i in self.operacoes if [i['qtd'] * i['preco'] == value]][0]
            if op:
                value = self.parse_float(self.lines[index - 1])
                op['irpf'] = value

    def __rateia_custos(self) -> None:
        emulomentos = self.__find_emulumentos(self.lines)
        taxa_liquidacao = self.__find_taxa_liquidacao(self.lines)
        clearing = self.__find_clearing(self.lines)
        iss = self.__find_iss(self.lines)
        outras = self.__find_outras_despesas(self.lines)
        custos_total = emulomentos + taxa_liquidacao + clearing + iss + outras
        if custos_total > 0:
            ops = [item for item in self.operacoes if item['tipo'] == 'V']
            total_compras = sum((item['preco'] * item['qtd'] for item in ops))
            for op in ops:
                rs = op['preco'] * op['qtd']
                percentual = rs * 100 / total_compras
                op['custos'] = round(custos_total * (percentual * 0.01), 2)

    @staticmethod
    def __find_nome_ativo(cutting: List) -> str:
        tipo = cutting[4].replace('N1', '').replace('NM', '').strip(' ')
        codigo = cutting[5].strip('')
        value = f'{codigo}/{tipo}'
        return value

    @staticmethod
    def __find_qtd(cutting: List) -> int:
        value = cutting[3]
        return int(value.strip(''))

    @staticmethod
    def __find_preco_medio(cutting: List) -> float:
        value = cutting[0]
        value = onnly_numbers(value)
        value = round(str_to_float(value) * 0.01, 2)
        return value

    def __find_taxa_liquidacao(self, cutting: List) -> float:
        index = self.__locate_index('Taxa de liquidação', cutting)
        value = cutting[index - 1]
        return self.parse_float(value)

    def __find_emulumentos(self, cutting: List) -> float:
        index = self.__locate_index('Emolumentos', cutting)
        value = cutting[index - 1]
        return self.parse_float(value)

    def __find_clearing(self, cutting: List) -> float:
        index = cutting.index('Clearing')
        sub = cutting[index + 1: len(cutting)]
        index = sub.index('Clearing')
        value = sub[index + 2]
        return self.parse_float(value)

    def __find_iss(self, cutting: List) -> float:
        index = self.__locate_index('ISS', cutting)
        value = cutting[index - 1]
        return self.parse_float(value)

    def __find_outras_despesas(self, cutting: List) -> float:
        index = self.__locate_index('Outras Despesas', cutting)
        value = cutting[index - 1]
        return self.parse_float(value)
