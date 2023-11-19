# @author Marildo Cesar 24/09/2023
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from ...model import Dividendos

from .ativo_schema import AtivoSchema


class DividendosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dividendos

    ativo = Nested(AtivoSchema, only=['id', 'codigo'])
