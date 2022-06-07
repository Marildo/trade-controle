from services.corretagem.base_ativo import AtivoBase
from utils import StrUtil, str_date


class MiniIndice(AtivoBase):

    def calcule(self):
        for i in self.lines:
            print(i)

        operacao = {}

        value = self.__get_value_by_next('Total de negócios')
        resultado = StrUtil.str_to_float(value.replace('R$ ', ''))

        key = 'Quant. total de venda:'
        qtd = max([int(StrUtil.onnly_numbers(item)) for item in self.lines if item.startswith(key)])
        operacao['qtd_compra'] = qtd
        operacao['qtd_venda'] = qtd

        operacao['pm_compra'] = StrUtil.str_to_float(self.__get_value_by_next('Preço médio compra: R$ '))
        operacao['pm_venda'] = operacao['pm_compra'] + (resultado / qtd)

        value = StrUtil.onnly_numbers(self.__get_value_by_next('IRRF Day Trade (Projeção)'))
        operacao['irpf'] = StrUtil.str_to_float(value) * -0.01

        value = StrUtil.onnly_numbers(self.__get_value_by_next('Custos'))
        operacao['custos'] = StrUtil.str_to_float(value) * -0.01

        index = self.lines.index('Data de referência')
        operacao['data_compra'] = str_date(self.lines[index - 1])
        operacao['data_venda'] = operacao['data_compra']

        index = self.lines.index('Comprovante')
        operacao['comprovante'] = self.lines[index + 1]

        operacao['ativo'] = 'WINFUT'

        self._add_operacao(operacao)

    def __get_value_by_next(self, key):
        index = self.lines.index(key)
        return self.lines[index + 1]
