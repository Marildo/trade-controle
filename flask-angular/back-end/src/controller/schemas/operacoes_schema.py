"""
 @author Marildo Cesar 07/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from ...model import Operacao

from .ativo_schema import AtivoSchema


class OperacaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Operacao

    compra_venda = fields.Function(lambda obj: str(obj.compra_venda.name).capitalize())
    qtd_aberta = fields.Float()
    resultado = fields.Float()

    ativo = fields.Nested(AtivoSchema(),
                          exclude=('descricao', 'parent_id', 'tipo_ativo', 'tipo_investimento', 'update_at'))
