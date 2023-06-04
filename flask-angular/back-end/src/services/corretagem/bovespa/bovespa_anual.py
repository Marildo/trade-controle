"""
 @author Marildo Cesar 23/04/2023
"""
import uuid
from typing import List

from src.utils.date_util import str_date
from src.utils.str_util import str_to_float, onnly_numbers
from src.model import TipoNota

from ..investment import Investiment


class BovespaAnual(Investiment):
    DATA_OPERACAO = 4
    COMPROVANTE = 6

    def load(self):

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
            tipo_nota = TipoNota.ACOES

            # print(page.number, data_operacao, comprovante)

            end = self.__locate_index('BOVESPA 1', self.lines)
            begin = end - 7

            _id = 0
            while begin > 0:
                cutting = self.lines[begin - 1: end]
                _id += 1
                ativo = self.__find_nome_ativo(cutting)
                qtd = self.__find_qtd(cutting)
                pm = self.__find_preco_medio(cutting)
                tipo = cutting[7][0]

                operacao = dict(id=_id, ativo=ativo, tipo=tipo, qtd=qtd, preco=pm, irpf=0, custos=0,  factor=5)
                # print(operacao)
                operacoes.append(operacao)

                end = self.__locate_index('BOVESPA 1', self.lines, end + 1)
                begin = end - 7

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
        return int(self.lines[self.COMPROVANTE])

    def __rateia_irrf(self, operacoes: List) -> None:
        irrf_total = 0
        index = self.__locate_index('IRRF Day Trade', self.lines)
        if index > 0:
            value = self.lines[index + 1]
            irrf_total = self.parse_float(value)

        index = self.__locate_index('IRRF Day-Trade', self.lines)
        if index > 0:
            value = self.lines[index]
            key = 'Projeção R$'
            value = value[value.find(key) + len(key): len(value)]
            irrf_total = self.parse_float(value)

        self.__rateia_daytrade_irrf(operacoes, irrf_total)

        index = self.__locate_index('I.R.R.F. s/ operações', self.lines)
        if index > 0:
            value = self.parse_float(self.lines[index + 1])
            op = [i for i in operacoes if [i['qtd'] * i['preco'] == value]][0]
            if op:
                value = self.parse_float(self.lines[index - 1])
                op['irpf'] = value

    @staticmethod
    def __rateia_daytrade_irrf(operacoes: List, irrf: float):
        if irrf <= 0:
            return

        compras = {i['ativo'] for i in operacoes if i['tipo'] == 'C'}
        vendas = {i['ativo'] for i in operacoes if i['tipo'] == 'V'}
        intersection = compras.intersection(vendas)
        ativos = set([i['ativo'] for i in operacoes if i['ativo'] in intersection])
        for item in ativos:
            ops = [i for i in operacoes if i['ativo'] == item]
            qtd_venda = sum([i['qtd'] for i in ops if i['tipo'] == 'V'])
            qtd_compra = sum([i['qtd'] for i in ops if i['tipo'] == 'C'])
            ops = [i for i in ops if i['tipo'] == 'V']
            if qtd_venda == qtd_compra:
                for op in ops:
                    percentual = (op['qtd'] * 100) / qtd_venda
                    op['irpf'] = round(irrf * (percentual * 0.01), 4)

    def __rateia_custos(self, operacoes: List) -> None:
        emulomentos = self.__find_emulumentos(self.lines)
        taxa_liquidacao = self.__find_taxa_liquidacao(self.lines)
        clearing = self.__find_clearing(self.lines)
        iss = self.__find_iss(self.lines)
        outras = self.__find_outras_despesas(self.lines)
        custos_total = emulomentos + taxa_liquidacao + clearing + iss + outras
        if custos_total > 0:
            ops = [item for item in operacoes if item['tipo'] == 'V']
            total_compras = sum((item['preco'] * item['qtd'] for item in ops))
            for op in ops:
                rs = op['preco'] * op['qtd']
                percentual = rs * 100 / total_compras
                op['custos'] = round(custos_total * (percentual * 0.01), 2)

    @staticmethod
    def __find_nome_ativo(cutting: List) -> str:
        tipo = cutting[5].replace('N1', '').replace('NM', '').strip(' ')
        codigo = cutting[6].strip('')
        value = f'{codigo}/{tipo}'
        return value

    @staticmethod
    def __find_qtd(cutting: List) -> int:
        value = cutting[4]
        return int(value.strip(''))

    @staticmethod
    def __find_preco_medio(cutting: List) -> float:
        value = cutting[2]
        value = onnly_numbers(value)
        value = round(str_to_float(value) * 0.01, 2)
        return value

    def __find_taxa_liquidacao(self, cutting: List) -> float:
        index = self.__locate_index('Taxa de liquidação', cutting)
        if index < 0:
            return 0
        value = cutting[index - 1]
        return self.parse_float(value)

    def __find_emulumentos(self, cutting: List) -> float:
        index = self.__locate_index('Emolumentos', cutting)
        value = cutting[index - 1]
        return self.parse_float(value)

    def __find_clearing(self, cutting: List) -> float:
        index = cutting.index('Clearing')
        sub = cutting[index + 1: len(cutting)]
        index = self.__locate_index('Clearing', sub)
        if index < 0:
            return 0
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
