import json
from db_models import Entity, EntityCall, EntitySecondaryContactDetails, EntityPropertyContact, EntityAppointments, EntityProperty, SubContractor, SamMultiLambdaAppBaseTable, EntityCallback, EntityPhone, EmployeeMaster, EntityAppointmentSelectedProduct, SalesPersonAvailabilitySlots, SalesPersonAvailability, EntityDispute, EntityCallback,EntityCall, CommissionReport, EntityCallCenterNotes, EmployeePayDetail, SalesJobAddendum, SalesJobCost, SalesJobPermits, SalesJobNotes, SalesJobPayment, SalesJobServiceTicketLogs, SalesJobMilestoneDate, SalesJobFinancingCompany, SalesJobFinancingParty, SalesJobFinancing, SalesJobDocuments, SalesJobDocumentCategory, SalesJobDocumentCategoryDocuments, SalesJobMaterialsOrdered, MaterialsVendor, SalesJobCommissions, ContractLineItem, EmployeePayrollBonus, PayrollNotes, SalesJobServiceTicket, SalesJob
from utils import api_response

def root_handler(**kwargs):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "success"
        }),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
    }


def deleteAllData(**kwargs):
    try:

        response_data = api_response()
        query_params = kwargs.get('query_params',{}) or {}
        db_session = kwargs.get('db_session', None)
        secret_key = query_params.get("secret_key", None)
        # expected_secret_key = os.environ.get("SECRET_KEY") # Recommended: Use environment variable
        expected_secret_key = "idpQTo4FuD8MQPx8qpWjKILAHwuVjXSm" # TODO: Move to Secrets Manager or Environment Variable
        if not secret_key or secret_key != expected_secret_key:
            raise Exception("Invalid secret key. Unauthorized access.")
        
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        models = [ SalesPersonAvailability, EntityPhone, EntityDispute, EntityCallback,EntityCall, EntityPropertyContact, 
                  EntitySecondaryContactDetails, EntityAppointmentSelectedProduct, EntityAppointments, EntityCallCenterNotes, 
                  EmployeePayDetail, SalesJobAddendum, SalesJobCost, SalesJobPermits, SalesJobNotes,
                  SalesJobPayment, SalesJobServiceTicketLogs, SalesJobServiceTicket, SalesJobMilestoneDate, SalesJobFinancingCompany,
                  SalesJobFinancingParty, SalesJobFinancing, SalesJobDocuments, SalesJobDocumentCategory, SalesJobDocumentCategoryDocuments, 
                  SalesJobMaterialsOrdered, MaterialsVendor, SalesJobCommissions, ContractLineItem, EmployeePayrollBonus, PayrollNotes, 
                  SalesPersonAvailabilitySlots, CommissionReport, SalesJob, SubContractor, EntityProperty, Entity, EmployeeMaster, SamMultiLambdaAppBaseTable ]
        for model in models:
            db_session.query(model).delete()

        db_session.commit()
        response_data.update({
            "success": True,
            "message": "All data deleted successfully",
        })
        return {'statusCode': 201, 'body': json.dumps(response_data)}
    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}