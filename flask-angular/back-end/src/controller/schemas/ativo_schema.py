"""
 @author Marildo Cesar 10/05/2023
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.model import Ativo


class AtivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ativo
