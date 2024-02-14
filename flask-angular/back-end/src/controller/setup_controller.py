# @author Marildo Cesar 14/02/2024

from webargs.flaskparser import parser
from marshmallow import fields

from ..model import Setup
from .schemas import SetupSchema


class SetupController:

    @classmethod
    def load(cls, request):
        data = Setup().read_by_params({})
        result = SetupSchema().dump(data, many=True)
        return result

    @classmethod
    def save(cls, request):
        input_schema = {
            'nome': fields.Str(required=True),
            'descricao': fields.Str(required=True),
        }
        args = parser.parse(input_schema, request, location='json')
        setup = Setup(**args)
        setup.save()
        return SetupSchema().dump(setup)
