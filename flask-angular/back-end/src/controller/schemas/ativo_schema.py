"""
 @author Marildo Cesar 10/05/2023
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested, fields
from ...model import Ativo, Setor, Segmento


class SetorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Setor

    id = fields.Int()
    nome = fields.Str()


class SegmentoSchema(SetorSchema):
    class Meta:
        model: Segmento


class AtivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ativo

    setor = Nested(SetorSchema())
    segmento = Nested(SegmentoSchema())
