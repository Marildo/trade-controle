"""
 @author Marildo Cesar 07/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.model import NotaCorretagem


class NotaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotaCorretagem