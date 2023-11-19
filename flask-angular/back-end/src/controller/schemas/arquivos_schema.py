"""
 @author Marildo Cesar 06/05/2023
"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from ...utils.str_util import capitalize_plus
from ...model import FileCorretagem


class ArquivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FileCorretagem

    status = fields.Function(lambda obj: capitalize_plus(obj.status.name))
    tipo = fields.Function(lambda obj: capitalize_plus(obj.tipo.name))
    # data_upload = fields.DateTime(format='%d/%m/%Y')
