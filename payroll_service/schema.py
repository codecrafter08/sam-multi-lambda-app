from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db_models import EmployeePayrollBonus, MasterPayrollPeriod, CommissionReport, SalesJobMilestoneDate

class EmployeePayrollBonusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeePayrollBonus
        include_fk = True
        load_instance = True

class MasterPayrollPeriodSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MasterPayrollPeriod
        load_instance = True

class CommissionReportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CommissionReport
        include_fk = True
        load_instance = True

class SalesJobMilestoneDateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesJobMilestoneDate
        include_fk = True
        load_instance = True
