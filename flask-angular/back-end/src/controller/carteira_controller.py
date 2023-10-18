# @author Marildo Cesar 17/10/2023
from webargs import fields, validate
from flask import request
from webargs.flaskparser import parser

from ..model import CarteiraRepository, Carteira
from .schemas import CarteitaSchema


class CarteiraController:

    @classmethod
    def carteiras(cls):
        data = CarteiraRepository.get_carteiras()
        response = CarteitaSchema().dump(data, many=True)
        return response

    @classmethod
    def save(cls):
        input_schema = {
            'nome': fields.String(required=True),
            'saldo_ativos': fields.Float(required=False, default=0),
            'saldo_caixa': fields.Float(required=False, default=0),
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
            'saldo_ativos': fields.Float(required=False),
            'saldo_caixa': fields.Float(required=False),
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
