"""
 @author Marildo Cesar 07/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ...model import Carteira


class CarteitaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Carteira
