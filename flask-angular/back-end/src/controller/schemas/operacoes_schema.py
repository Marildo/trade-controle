"""
 @author Marildo Cesar 07/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from src.model import Operacao


class OperacaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Operacao
