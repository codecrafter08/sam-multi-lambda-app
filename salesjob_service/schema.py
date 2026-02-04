from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db_models import SalesJobAddendum, SalesJobCost, SalesJobPayment

class SalesJobAddendumSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesJobAddendum
        include_fk = True
        load_instance = True

class SalesJobCostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesJobCost
        include_fk = True
        load_instance = True

class SalesJobPaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesJobPayment
        include_fk = True
        load_instance = True