# @author Marildo Cesar 14/02/2024
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ...model import Setup


class SetupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Setup
