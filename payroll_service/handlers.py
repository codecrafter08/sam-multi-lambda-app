from db_models import EmployeePayrollBonus, MasterPayrollPeriod, CommissionReport, SalesJobMilestoneDate
import json
from utils import api_response
from datetime import datetime
from sqlalchemy import and_
from schema import EmployeePayrollBonusSchema,MasterPayrollPeriodSchema, CommissionReportSchema, SalesJobMilestoneDateSchema

    
def createEmployeePayrollBonus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")
        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        payrollBonus = EmployeePayrollBonus(**{key: value for key, value in data.items() if hasattr(EmployeePayrollBonus, key)})
        db_session.add(payrollBonus)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "EmployeepayrollBonus created successfully",

        })
        return { 'statusCode': 201, 'body': json.dumps(response_data)}
    except Exception as e:
        db_session.rollback()  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }


def getEmployeePayrollBonus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        payrollBonus = db_session.query(EmployeePayrollBonus).all()
        schema = EmployeePayrollBonusSchema(many=True)
        payrollBonus_data = schema.dump(payrollBonus)
        response_data.update({
            "success": True,
            "data": payrollBonus_data, 
            "message": "PayrollBonus retrieved successfully."
        })
        return { 'statusCode': 200, 'body': json.dumps(response_data) }
    except Exception as e:
        db_session.rollback()  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    

def getMasterPayrollPeriod(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        query_params = kwargs.get('query_params',{}) or {}
        year = query_params.get('year', None)
        
        if year is None:
            year = str(datetime.now().year)

        master_payroll_period_id = kwargs.get('master_payroll_period_id', None)
        master_payroll_periods = []
        if master_payroll_period_id:
            master_payroll_periods = db_session.query(MasterPayrollPeriod).filter(MasterPayrollPeriod.masterPayrollPeriodID == master_payroll_period_id).all()
        else:
            master_payroll_periods = db_session.query(MasterPayrollPeriod).filter(MasterPayrollPeriod.masterPayrollPeriodYear == year).all()
      
        schema = MasterPayrollPeriodSchema(many=True)
        master_payroll_period_data = schema.dump(master_payroll_periods)
        response_data.update({
            "success": True,
            "data": master_payroll_period_data,
            "message": "master payroll period retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createMasterPayrollPeriod(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        master_payroll_period = MasterPayrollPeriod(**{key: value for key, value in data.items() if hasattr(MasterPayrollPeriod, key)})

        db_session.add(master_payroll_period)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "master payroll period created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 


def updateMasterPayrollPeriod(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        masterPayrollPeriodID = body.get('masterPayrollPeriodID', None)
        if not masterPayrollPeriodID:
            raise Exception("masterPayrollPeriodID not provided in the request body.")


        master_payroll_period = db_session.query(MasterPayrollPeriod).filter_by(masterPayrollPeriodID=masterPayrollPeriodID).first()
        
        if not master_payroll_period:
            raise Exception(f"Customer property with ID {masterPayrollPeriodID} not found.")

        for key, value in body.items():
            if hasattr(master_payroll_period, key):
                setattr(master_payroll_period, key, value)

        db_session.commit()
        schema = MasterPayrollPeriodSchema()
        data = schema.dump(master_payroll_period)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants entity type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def deleteMasterPayrollPeriod(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        payroll_period_id = kwargs.get('master_payroll_period_id', None)
        if not payroll_period_id:
            raise Exception("payroll_period_id is required for deletion.")

        payroll_period = db_session.query(MasterPayrollPeriod).filter(
            MasterPayrollPeriod.masterPayrollPeriodID == payroll_period_id
        ).first()

        if not payroll_period:
            raise Exception(f"MasterPayrollPeriod with ID {payroll_period_id} not found.")

        db_session.delete(payroll_period)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "Master payroll period deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getCommissionReports(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

       
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        query_params = kwargs.get('query_params',{}) or {}
        today = datetime.utcnow().date()

        start_date = query_params.get('start_date', None)
        end_date = query_params.get('end_date', None)

        if not start_date:
            start_date = today
        if not end_date:
            end_date = today

        # Convert to datetime if strings are provided
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            raise Exception("Invalid date format. Use 'YYYY-MM-DD'.")
        
        sales_job_id = kwargs.get('sales_job_id', None)
        reports = []
        filters = []  
    
        if sales_job_id:
            filters.append(CommissionReport.salesJobID == sales_job_id)
        
        if start_date and end_date:
            filters.append(CommissionReport.commissionReportDate.between(start_date, end_date))
        elif start_date:
            filters.append(CommissionReport.commissionReportDate >= start_date)
        elif end_date:
            filters.append(CommissionReport.commissionReportDate <= end_date)
        
        # Construct query with dynamic filters
        query = db_session.query(CommissionReport)
        if filters:
            query = query.filter(and_(*filters))
        
        # Optionally sort by commissionReportDate
        reports = query.order_by(CommissionReport.commissionReportDate).all()

        schema = CommissionReportSchema(many=True)
        reports_data = schema.dump(reports)

        # Prepare response
        response_data.update({
            "success": True,
            "data": reports_data,
            "message": "Commission reports retrieved successfully",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getSalesJobMilestoneDate(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        sales_job_milestone_date_id = kwargs.get('sales_job_milestone_date_id', None)
        milestone_dates = []

        if sales_job_milestone_date_id:
            milestone_dates = db_session.query(SalesJobMilestoneDate).filter(
                SalesJobMilestoneDate.salesJobMilestoneDateID == sales_job_milestone_date_id
            ).all()
        else:
            milestone_dates = db_session.query(SalesJobMilestoneDate).all()
        
        schema = SalesJobMilestoneDateSchema(many=True)
        milestone_date_data = schema.dump(milestone_dates)
        

        response_data.update({
            "success": True,
            "data": milestone_date_data,
            "message": "Milestone dates retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


