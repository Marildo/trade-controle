# @author Marildo Cesar 24/09/2023
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from model import Dividendos


class DividendosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dividendos
