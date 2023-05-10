"""
 @author Marildo Cesar 06/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from src.model import FileCorretagem, NotaStatusProcess
from .notas_schema import NotaSchema


class ArquivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FileCorretagem

    status = fields.Function(lambda obj: str(obj.status.name).capitalize())
    # data_upload = fields.DateTime(format='%d/%m/%Y')
