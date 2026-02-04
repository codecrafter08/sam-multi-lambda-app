from db_models import SalesJobAddendum, SalesJobCost, SalesJobPayment
import json
from utils import api_response
from schema import SalesJobAddendumSchema, SalesJobCostSchema, SalesJobPaymentSchema

def getSalesJobAddendum(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

       
        sales_job_addendums = db_session.query(SalesJobAddendum).all()
      
        schema = SalesJobAddendumSchema(many=True)
        sales_job_addendums_data = schema.dump(sales_job_addendums)

        response_data.update({
            "success": True,
            "data": sales_job_addendums_data,
            "message": "sales job addendums retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createSalesJobAddendum(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        sales_job_addendum = SalesJobAddendum(**{key: value for key, value in data.items() if hasattr(SalesJobAddendum, key)})
        db_session.add(sales_job_addendum)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "sales job addendum created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 
    

def getSalesJobCost(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

       
        sales_job_costs = db_session.query(SalesJobCost).all()
        schema = SalesJobCostSchema(many=True)
        sales_job_cost_data = schema.dump(sales_job_costs)

        response_data.update({
            "success": True,
            "data": sales_job_cost_data,
            "message": "sales job cost retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createSalesJobCost(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        
        sales_job_cost = SalesJobCost(**{key: value for key, value in data.items() if hasattr(SalesJobCost, key)})
        db_session.add(sales_job_cost)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "sales job cost created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 
    

def getSalesJobPayment(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

       
        sales_job_payments = db_session.query(SalesJobPayment).all()
        schema =SalesJobPaymentSchema(many=True)
        sales_job_payment_data = schema.dump(sales_job_payments)

        response_data.update({
            "success": True,
            "data": sales_job_payment_data,
            "message": "sales job payment retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createSalesJobPayment(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        
        sales_job_payment = SalesJobPayment(**{key: value for key, value in data.items() if hasattr(SalesJobPayment, key)})
        db_session.add(sales_job_payment)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "sales job payment created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 