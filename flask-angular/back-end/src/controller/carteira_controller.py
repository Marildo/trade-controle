# @author Marildo Cesar 17/10/2023

import threading

from webargs import fields
from flask import request
from webargs.flaskparser import parser

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from services import YFinanceService
from ..model import CarteiraRepository, Carteira, Dividendos, Historico, Operacao, HistoricoMensal, Movimentacao
from .schemas import CarteitaSchema, MovimentacaoSchema
from ..utils import str_util


class CarteiraController:
    repository = CarteiraRepository()

    @classmethod
    def carteiras(cls):
        data = cls.repository.get_carteiras()
        response = CarteitaSchema().dump(data, many=True)
        return response

    @classmethod
    def update_saldos(cls):
        cls.repository.totalize()

    @classmethod
    def update_saldos_async(cls):
        def task():
            cls.repository.totalize()

        thread = threading.Thread(target=task)
        thread.start()

    @classmethod
    def save(cls):
        input_schema = {
            'nome': fields.String(required=True),
            'tipo': fields.String(required=True),
            'daytrade': fields.Boolean(required=True),
            'dividendos': fields.Boolean(required=True),
            'buyhold': fields.Boolean(required=True),
            'descricao': fields.String(required=True),
        }
        args = parser.parse(input_schema, request, location='json')
        args.setdefault('saldo_ativos', 0)
        args.setdefault('saldo_caixa', 0)

        carteira = Carteira(**args)
        carteira.save()
        response = CarteitaSchema().dump(carteira)
        return response

    @classmethod
    def update(cls):
        input_schema = {
            'id': fields.Integer(required=True),
            'nome': fields.String(required=False),
            'tipo': fields.String(required=False),
            'daytrade': fields.Boolean(required=False),
            'dividendos': fields.Boolean(required=False),
            'buyhold': fields.Boolean(required=False),
            'descricao': fields.String(required=False)
        }
        args = parser.parse(input_schema, request, location='json')

        carteira = Carteira(**args)
        carteira.update()
        response = CarteitaSchema().dump(carteira)
        return response

    @classmethod
    def update_by_dividendos(cls, dividendo: Dividendos, codigo: str):
        if dividendo.total > 0:
            hist = Historico()
            hist.carteira_id = dividendo.carteira_id
            hist.dividendo_id = dividendo.id
            hist.data_referencia = dividendo.data_pgto
            hist.descricao = f'{"Juros sobre capital" if dividendo.jcp else "Dividendos"} de ({codigo})'
            hist.valor = dividendo.total
            hist.save()

    @classmethod
    def generate_historico(cls, start_date: date = None):
        if start_date is None:
            if not date.today().day == 1:
                return
            start_date = date.today()

        precos_ativos = {}
        carteiras = Carteira().read_by_params({})
        for carteira in carteiras:
            filters = dict(carteira_id=carteira.id)
            historicos = Historico().read_by_params(filters)
            operacoes = Operacao().read_by_params(filters)

            ref_month = start_date
            resultado_acc = 0
            while ref_month < date.today():
                ref_month = (ref_month + relativedelta(months=2)).replace(day=1) - timedelta(days=1)

                if ref_month > date.today():
                    continue

                saldo_caixa = sum([i.valor for i in historicos if i.data_referencia <= ref_month])

                resultado_total = sum([i.resultado - i.custos - i.irpf for i in operacoes if i.encerrada and
                                       i.data_encerramento <= ref_month])

                saldo_ativo = 0
                sales = [i for i in operacoes if
                         not i.daytrade and i.compra_venda.value == 'V' and i.data_venda <= ref_month and
                         (i.data_compra is None or i.data_compra > ref_month)]

                purchases = [i for i in operacoes if
                             not i.daytrade and i.compra_venda.value == 'C' and i.data_compra <= ref_month and
                             (i.data_venda is None or i.data_venda > ref_month)]

                opers = sales + purchases
                ativos = set([i.ativo for i in operacoes if opers])
                for a in ativos:
                    if a.codigo not in precos_ativos:
                        prices = YFinanceService.get_prices(a.codigo, start_date - timedelta(days=1))
                        precos_ativos[a.codigo] = prices

                    qtd_vendas = sum([i.qtd_venda for i in sales if i.ativo == a])
                    qtd_compras = sum([i.qtd_compra for i in purchases if i.ativo == a])
                    prices = [v for k, v in precos_ativos[a.codigo].items() if k >= ref_month]
                    if prices:
                        price_month = prices[0]
                    else:
                        op = opers[0]
                        price_month = op.pm_compra if op.compra_venda.value == 'C' else op.pm_venda

                    saldo_compras = price_month * qtd_compras
                    saldo_vendas = price_month * qtd_vendas
                    saldo_ativo += saldo_compras + saldo_vendas

                custos_compras = sum([i.qtd_compra * i.pm_compra for i in purchases])
                custos_vendas = sum([i.qtd_venda * i.pm_venda for i in sales])
                resultado_mes = saldo_ativo - (custos_compras + custos_vendas)

                hist_mensal = HistoricoMensal()
                hist_mensal.carteira_id = carteira.id
                hist_mensal.data_referencia = ref_month
                hist_mensal.saldo_ativo = saldo_ativo
                hist_mensal.saldo_caixa = saldo_caixa
                hist_mensal.resultado = resultado_total
                hist_mensal.resultado_mensal = resultado_mes - resultado_acc if carteira.id != 1 else (
                        resultado_total - resultado_acc)
                hist_mensal.save()
                resultado_acc = resultado_mes if carteira.id != 1 else resultado_total

    @classmethod
    def add_movimentacao(cls):
        input_schema = {
            'valor': fields.Float(required=False),
            'data_referencia': fields.Date(required=False),
            'descricao': fields.String(required=False),
            'tipo': fields.String(required=False),
            'carteira_id': fields.Integer(required=True)
        }
        args = parser.parse(input_schema, request, location='json')

        mov = Movimentacao(**args)
        mov.save()

        hist = Historico()
        hist.carteira_id = mov.carteira_id
        hist.movimento_id = mov.id
        hist.data_referencia = mov.data_referencia
        hist.descricao = f'{str_util.capitalize_plus(mov.tipo)} - {mov.descricao}'
        hist.valor = mov.valor
        hist.save()

        cls.update_saldos_async()

        return 201

    @classmethod
    def movimentacoes(cls):
        data = cls.repository.get_movimentacoes()
        response = MovimentacaoSchema().dump(data, many=True)
        return response
