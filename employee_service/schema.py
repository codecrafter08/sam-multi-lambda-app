from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db_models import EmployeeMaster, SalesPersonAvailabilitySlots

class EmployeeMasterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeMaster
        include_fk = True
        load_instance = True

class SalesPersonAvailabilitySlotsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesPersonAvailabilitySlots
        include_fk = True
        load_instance = True

