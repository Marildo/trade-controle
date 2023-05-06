"""
 @author Marildo Cesar 06/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from src.model import NotaCorretagem, NotaStatusProcess


class NotaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NotaCorretagem

    status = fields.Function(lambda obj: str(obj.status.name).capitalize())
    # data_upload = fields.DateTime(format='%d/%m/%Y')
