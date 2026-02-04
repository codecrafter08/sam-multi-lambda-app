import json
from utils import get_all_parameters, get_parameter_values_as_list, get_values, api_response, decrypt_data
from db_models import EntityAppointments
from datetime import datetime



def getConstants(**kwargs):
    try:
        response_data = api_response()
        query_params = kwargs.get('query_params',{}) or {}
        query = query_params.get('query', None) 
        if query:
            keys = query.strip('"').split(',')
            response = get_values(keys)
            values = {
                item.get('Name'): item.get('Value').replace('.', '').split(',') 
                if isinstance(item.get('Value'), str) else item.get('Value')
                for item in response
            }
            response_data.update({
                "success": True,
                "data": values,
                "message": "values retrieved successfully."
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}
        else:
            result = get_all_parameters()
            response = get_parameter_values_as_list(result)
            values = {
                key: [val.strip() for v in value for val in v.split(',')]
                for key, value in response.items()
            }
            response_data.update({
                "success": True,
                "data": values,
                "message": "values retrieved successfully."
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    



def updateAppointmentStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        query_params = kwargs.get('query_params', {}) or {}
        token = query_params.get('token', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        if token:
            decoded_data = decrypt_data(token)
            if decoded_data:
                sales_person = decoded_data.get('sales_person')
                appointment_id = decoded_data.get('appointment_id')
                action = decoded_data.get('action')
                sales_person = decoded_data.get('sales_person')
                
                appointment_with_sales_person1 = db_session.query(EntityAppointments).filter(
                    EntityAppointments.entityAppointmentsID == appointment_id,
                    EntityAppointments.entityAppointmentsSalesRep1 == sales_person
                ).first()
                
                if appointment_with_sales_person1:
                    if action == "accepted":
                        appointment_with_sales_person1.entityAppointmentsSalesRep1IsAccepted = True
                    else: 
                        appointment_with_sales_person1.entityAppointmentsSalesRep1IsAccepted = False
                    
                   
                    appointment_with_sales_person1.entityAppointmentsSalesRep1ResponseDate = datetime.now()
                    db_session.commit()  
                
                else:
                    
                    appointment_with_sales_person2 = db_session.query(EntityAppointments).filter(
                        EntityAppointments.entityAppointmentsID == appointment_id,
                        EntityAppointments.entityAppointmentsSalesRep2 == sales_person
                    ).first()
                    
                    if appointment_with_sales_person2:
                        if action == "accepted":
                            appointment_with_sales_person2.entityAppointmentsSalesRep2IsAccepted = True
                        else:  
                            appointment_with_sales_person2.entityAppointmentsSalesRep2IsAccepted = False
                        
                        appointment_with_sales_person2.entityAppointmentsSalesRep2ResponseDate = datetime.now()
                        db_session.commit()  
                    
                    else:
                        response_data.update({
                            "success": False,
                            "message": "Appointment not found for the given sales person."
                        })
                        return {'statusCode': 404, 'body': json.dumps(response_data)}
            
                response_data.update({
                    "success": True,
                    "message": f"Appointment {action} successfully.",
                    "data": {
                        "appointment_id": appointment_id,
                        "sales_person": sales_person,
                        "action": action
                    }
                })
                return {'statusCode': 200, 'body': json.dumps(response_data)}
            
            else:
                response_data.update({
                    "success": False,
                    "message": "Token is not valid."
                })
                return {'statusCode': 200, 'body': json.dumps(response_data)}
        
        else:
            response_data.update({
                "success": False,
                "message": "Token is required."
            })
            return {'statusCode': 400, 'body': json.dumps(response_data)}
        
    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}




