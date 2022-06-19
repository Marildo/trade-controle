from typing import List
from services.corretagem.base_ativo import AtivoBase
from utils import StrUtil, str_date


class Bovespa(AtivoBase):
    DATA_OPERACAO = -5

    def calcule(self):
        for i in self.lines:
            print(i)

        begin = self.__locate_index('C/V', self.lines)
        end = self.__locate_index('PREÇO DE EXERCÍCIO', self.lines)

        data_operacao = self.__data_operacao()
        comprovante = self.__find_comprovante()

        operacao = dict(ativo='ativo', comprovante=comprovante,
                        qtd_compra=100, qtd_venda=100,
                        pm_compra=126, pm_venda=139,
                        data_compra=data_operacao, data_venda=data_operacao,
                        irpf=0, custos=0)
        self._add_operacao(operacao)

        while begin > 0:
            cutting = self.lines[begin - 1: end]

            ativo = self.__find_nome_ativo(cutting)
            qtd_compra = self.__find_qtd_compra(cutting)
            qtd_venda = self.__find_qtd_venda(cutting)
            pm_compra = self.__find_preco_medio_compra(cutting)
            pm_venda = self.__find_preco_medio_venda(cutting)

            operacao = dict(ativo=ativo, comprovante=comprovante,
                            qtd_compra=qtd_compra, qtd_venda=qtd_venda,
                            pm_compra=pm_compra, pm_venda=pm_venda,
                            data_compra=data_operacao, data_venda=data_operacao,
                            irpf=0, custos=0)

            self._add_operacao(operacao)

            begin = self.__locate_index('C/V', self.lines, end + 1)
            end = self.__locate_index('PREÇO DE EXERCÍCIO', self.lines, begin)

        self.__rateia_custos()
        self.__rateia_irrf()

    def __locate_index(self, value, cutting: List, start: int = 0) -> int:
        try:
            items = [item for item in cutting if item.startswith(value)]
            return cutting.index(items[0], start)
        except Exception as e:
            return 0

    def __locate_value(self, value, cutting: List) -> str:
        index = self.__locate_index(value, cutting)
        return None if index == 0 else cutting[index]

    def __data_operacao(self):
        return str_date(self.lines[self.DATA_OPERACAO])

    def __find_comprovante(self) -> int:
        return int(self.lines[self.__locate_index('Comprovante', self.lines) + 1])

    def __rateia_irrf(self) -> None:
        index = self.__locate_index('IRRF Day Trade', self.lines)
        if index:
            value = self.lines[index + 1]
            value = StrUtil.onnly_numbers(value)
            irrf_total = round(StrUtil.str_to_float(value) * 0.0001, 2)
            if irrf_total > 0:
                has_irrf = lambda item: item['qtd_compra'] == item['qtd_venda'] and item['pm_compra'] < item['pm_venda']
                ops = [item for item in self.operacoes if has_irrf(item)]
                if ops:
                    resultado_total = sum(((item['pm_venda'] - item['pm_compra']) * item['qtd_compra'] for item in ops))
                    for op in ops:
                        rs = (op['pm_venda'] - op['pm_compra']) * op['qtd_compra']
                        percentual = rs * 100 / resultado_total
                        op['irpf'] = round(irrf_total * (percentual * 0.01), 2)

    def __rateia_custos(self) -> None:
        index = self.__locate_index('Custos', self.lines)
        if index:
            value = self.lines[index + 1]
            value = StrUtil.onnly_numbers(value)
            custos_total = round(StrUtil.str_to_float(value) / 100, 2)
            if custos_total > 0:
                ops = [item for item in self.operacoes if item['qtd_venda'] > 0]
                total_vendas = sum((item['pm_venda'] * item['qtd_venda'] for item in ops))
                for op in ops:
                    rs = op['pm_venda'] * op['qtd_venda']
                    percentual = rs * 100 / total_vendas
                    op['custos'] = round(custos_total * (percentual * 0.01), 2)

    def __find_nome_ativo(self, cutting: List) -> str:
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
        key = f'Preço médio {tipo}: R$'
        index = self.__locate_index(key, cutting)
        index = index + 1 if key == cutting[index].strip(' ') else index
        if index > 1:
            value = cutting[index]
            value = StrUtil.onnly_numbers(value)
            value = round(StrUtil.str_to_float(value) * 0.0001, 2)
            return value
        return 0
