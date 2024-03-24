"""
 @author Marildo Cesar 07/05/2023
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ...model import Carteira, Movimentacao, Historico


class CarteitaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Carteira


class MovimentacaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movimentacao

    carteira = fields.Nested(CarteitaSchema(), only=('id', 'nome'))
    tipo = fields.Function(lambda obj: str(obj.tipo.name).capitalize())
    valor = fields.Float()


class HistoricoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Historico

    carteira = fields.Nested(CarteitaSchema(), only=('id', 'nome'))

