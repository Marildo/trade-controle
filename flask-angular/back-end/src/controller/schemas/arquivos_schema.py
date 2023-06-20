"""
 @author Marildo Cesar 06/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from src.utils.str_util import capitalize_plus
from src.model import FileCorretagem, NotaStatusProcess
from .notas_schema import NotaSchema


class ArquivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FileCorretagem

    status = fields.Function(lambda obj: capitalize_plus(obj.status.name))
    tipo = fields.Function(lambda obj: capitalize_plus(obj.tipo.name))
    # data_upload = fields.DateTime(format='%d/%m/%Y')
