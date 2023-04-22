from typing import List
from services.corretagem.base_ativo import AtivoBase
from utils import StrUtil, str_date


class BovespaAnual(AtivoBase):
    DATA_OPERACAO = 4
    COMPROVANTE = 6

    def calcule(self):
        for page in self.document:
            self._lines = page.get_text().split('\n')

            for i in self.lines:
                print(i)

            data_operacao = self.__data_operacao()
            comprovante = self.__find_comprovante()

            end = self.__locate_index('BOVESPA 1', self.lines)
            begin = end - 7

            while begin > 0:
                cutting = self.lines[begin - 1: end]

                ativo = self.__find_nome_ativo(cutting)
                qtd = self.__find_qtd(cutting)
                pm = self.__find_preco_medio(cutting)

                its_buy = cutting[-1] == 'C'

                qtd_compra = qtd if its_buy else 0
                pm_compra = pm if its_buy else 0

                qtd_venda = qtd if not its_buy else 0
                pm_venda = pm if not its_buy else 0

                operacao = dict(ativo=ativo, comprovante=comprovante,
                                qtd_compra=qtd_compra, qtd_venda=qtd_venda,
                                pm_compra=pm_compra, pm_venda=pm_venda,
                                data_compra=data_operacao, data_venda=data_operacao,
                                irpf=0, custos=0)

                self._add_operacao(operacao)

                end = self.__locate_index('BOVESPA 1', self.lines, end + 1)
                begin = end - 7

            self.__rateia_custos()
            self.__rateia_irrf()

    def __locate_index(self, value, cutting: List, start: int = 0) -> int:
        try:
            items = [item for item in cutting if item.startswith(value)]
            return cutting.index(items[0], start)
        except Exception as e:
            return 0

    def __data_operacao(self):
        return str_date(self.lines[self.DATA_OPERACAO])

    def __find_comprovante(self) -> int:
        return int(self.lines[self.COMPROVANTE])

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
        emulomentos = 0
        taxa_liquidacao = 0

        index = self.__locate_index('Emolumentos', self.lines)
        if index:
            value = self.lines[index - 1]
            emulomentos = round(StrUtil.str_to_float((StrUtil.onnly_numbers(value))) * 0.01, 2)

        index = self.__locate_index('Taxa de liquidação', self.lines)
        if index:
            value = self.lines[index - 1]
            taxa_liquidacao = round(StrUtil.str_to_float((StrUtil.onnly_numbers(value))) * 0.01, 2)

        custos_total = emulomentos + taxa_liquidacao
        if custos_total > 0:
            ops = [item for item in self.operacoes if item['qtd_compra'] > 0]
            total_compras = sum((item['pm_compra'] * item['qtd_compra'] for item in self.operacoes))
            for op in ops:
                rs = op['pm_compra'] * op['qtd_compra']
                percentual = rs * 100 / total_compras
                op['custos'] = round(custos_total * (percentual * 0.01), 2)

    def __find_nome_ativo(self, cutting: List) -> str:
        tipo = cutting[4].replace('N1', '').strip(' ')
        codigo = cutting[5].strip('')
        value = f'{codigo} / {tipo}'
        return value

    def __find_qtd(self, cutting: List) -> int:
        value = cutting[3]
        return int(value.strip(''))

    def __find_preco_medio(self, cutting: List) -> float:
        value = cutting[0]
        value = StrUtil.onnly_numbers(value)
        value = round(StrUtil.str_to_float(value) * 0.01, 2)
        return value
