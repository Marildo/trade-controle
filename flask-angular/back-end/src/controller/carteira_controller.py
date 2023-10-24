# @author Marildo Cesar 17/10/2023
from webargs import fields, validate
from flask import request
from webargs.flaskparser import parser

from ..model import CarteiraRepository, Carteira, Dividendos, Historico
from .schemas import CarteitaSchema


class CarteiraController:
    repository = CarteiraRepository()

    @classmethod
    def carteiras(cls):
        data = cls.repository.get_carteiras()
        response = CarteitaSchema().dump(data, many=True)
        return response

    @classmethod
    def update_saldos(cls):
        cls.repository.totalize_saldo_caixa()
        cls.repository.totalize_saldo_ativos()

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
