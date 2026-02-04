from db_models import ConstantsProductType, ConstantsMarketType, ConstantsEmployeeType, ConstantsEmployeePayType, ConstantsEntityCallType, ConstantsEntityCallResult, ConstantsEntityPropertyStructure, ConstantsEntitySubSource, ConstantsEntitySource, ConstantsPropertyLookUp, ConstantsPhoneType, ConstantsEntityEmploymentStatus, ConstantsEntityMaritalStatus, ConstantsSalesJobDispositon, ConstantsAppointmentDisposition, ConstantsRelationType, ConstantsUSAStates, ConstantsVoucherType, ConstantsDeliveryWarehouse, ConstantsMaterialsVendor
import json
from utils import api_response
from schema import ConstantsProductTypeSchema,ConstantsMarketTypeSchema, ConstantsEmployeeTypeSchema, ConstantsEmployeePayTypeSchema, ConstantsEntityCallResultSchema, ConstantsEntityCallTypeSchema, ConstantsEntityEmploymentStatusSchema, ConstantsEntityMaritalStatusSchema, ConstantsEntityPropertyStructureSchema, ConstantsEntitySubSourceSchema, ConstantsEntitySourceSchema, ConstantsPhoneTypeSchema, ConstantsPropertyLookUpSchema, ConstantsSalesJobDispositonSchema, ConstantsAppointmentDispositionSchema, ConstantsRelationTypeSchema, ConstantsUSAStatesSchema, ConstantsVoucherTypeSchema, ConstantsDeliveryWarehouseSchema, ConstantsMaterialsVendorSchema


def getConstantsProductType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_product_type_id = kwargs.get('constants_product_type_id', None)
        constants_product_types = []
        if constants_product_type_id:
            constants_product_types = db_session.query(ConstantsProductType).filter(ConstantsProductType.constantsProductID == constants_product_type_id).all()
        else:
            constants_product_types = db_session.query(ConstantsProductType).all()
        schema = ConstantsProductTypeSchema(many=True)
        constants_product_type_data = schema.dump(constants_product_types)
        

        response_data.update({
            "success": True,
            "data": constants_product_type_data,
            "message": "Cconstants product type retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createConstantsProductType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        constants_product_type = ConstantsProductType(**{key: value for key, value in data.items() if hasattr(ConstantsProductType, key)})
    
        db_session.add(constants_product_type)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "constants product type created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 

def updateConstantsProductType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsProductID = body.get('constantsProductID', None)
        if not constantsProductID:
            raise Exception("constantsProductID not provided in the request body.")


        constants_product_type = db_session.query(ConstantsProductType).filter_by(constantsProductID=constantsProductID).first()
        
        if not constants_product_type:
            raise Exception(f"constant Product Type with ID {constantsProductID} not found.")

        
        for key, value in body.items():
            if hasattr(constants_product_type, key):
                setattr(constants_product_type, key, value)

        db_session.commit()
        schema = ConstantsProductTypeSchema()
        data = schema.dump(constants_product_type)

        response_data.update({
            "success": True,
            "data":data,
            "message": "constants product type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def deleteConstantsProductType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        product_type_id = kwargs.get('constants_product_type_id', None)
        if not product_type_id:
            raise Exception("product_type_id is required for deletion.")

        product_type = db_session.query(ConstantsProductType).filter(
            ConstantsProductType.constantsProductID == product_type_id
        ).first()

        if not product_type:
            raise Exception(f"ConstantsProductType with ID {product_type_id} not found.")

        db_session.delete(product_type)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants product Type deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}  



def getConstantsMarketType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_market_type_id = kwargs.get('constants_market_type_id', None)
        constants_market_types = []
        if constants_market_type_id:
            constants_market_types = db_session.query(ConstantsMarketType).filter(ConstantsMarketType.constantsMarketID == constants_market_type_id).all()
        else:
            constants_market_types = db_session.query(ConstantsMarketType).all()
        schema = ConstantsMarketTypeSchema(many=True)
        constants_market_type_data = schema.dump(constants_market_types)
       

        response_data.update({
            "success": True,
            "data": constants_market_type_data,
            "message": "Cconstants market type retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def deleteConstantsMarketType(**kwargs):
    """
    Delete a ConstantsMarketType entry by ID.
    """
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        market_id = kwargs.get('constants_market_type_id', None)
        if not market_id:
            raise Exception("market_id is required for deletion.")

        market_type = db_session.query(ConstantsMarketType).filter(
            ConstantsMarketType.constantsMarketID == market_id
        ).first()

        if not market_type:
            raise Exception(f"ConstantsMarketType with ID {market_id} not found.")

        db_session.delete(market_type)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "Constants Market Type deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong.",
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createConstantsMarketType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        constants_market_type = ConstantsMarketType(**{key: value for key, value in data.items() if hasattr(ConstantsMarketType, key)})
    
        db_session.add(constants_market_type)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "constants market type created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 

def updateConstantsMarketType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsMarketID = body.get('constantsMarketID', None)
        if not constantsMarketID:
            raise Exception("constantsMarketID not provided in the request body.")


        constants_market_type = db_session.query(ConstantsMarketType).filter_by(constantsMarketID=constantsMarketID).first()
        
        if not constants_market_type:
            raise Exception(f"constant Market Type with ID {constantsMarketID} not found.")

        
        for key, value in body.items():
            if hasattr(constants_market_type, key):
                setattr(constants_market_type, key, value)

        db_session.commit()
        schema = ConstantsMarketTypeSchema()
        data = schema.dump(constants_market_type)

        response_data.update({
            "success": True,
            "data":data,
            "message": "constants market type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsEmployeeType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_employee_type_id = kwargs.get('constants_employee_type_id', None)
        constants_employee_types = []
        if constants_employee_type_id:
            constants_employee_types = db_session.query(ConstantsEmployeeType).filter(ConstantsEmployeeType.constantsEmployeeTypeID == constants_employee_type_id).all()
        else:
            constants_employee_types = db_session.query(ConstantsEmployeeType).all()
        schema = ConstantsEmployeeTypeSchema(many=True)
        constants_employee_type_data = schema.dump(constants_employee_types)

        response_data.update({
            "success": True,
            "data": constants_employee_type_data,
            "message": "constants employee type data retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsEmployeeType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        
        constants_employee_types = ConstantsEmployeeType(**{key: value for key, value in data.items() if hasattr(ConstantsEmployeeType, key)})
        db_session.add(constants_employee_types)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "constants employee type created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 
    
def updateConstantsEmployeeType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEmployeeTypeID = body.get('constantsEmployeeTypeID', None)
        if not constantsEmployeeTypeID:
            raise Exception("constantsEmployeeTypeID not provided in the request body.")


        constants_employee_types = db_session.query(ConstantsEmployeeType).filter_by(constantsEmployeeTypeID=constantsEmployeeTypeID).first()
        
        if not constants_employee_types:
            raise Exception(f"constants employee type with ID {constantsEmployeeTypeID} not found.")

        
        for key, value in body.items():
            if hasattr(constants_employee_types, key):
                setattr(constants_employee_types, key, value)

        db_session.commit()
        schema = ConstantsEmployeeTypeSchema()
        data = schema.dump(constants_employee_types)

        response_data.update({
            "success": True,
            "data": data,
            "message": "constants employee type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsEmployeeType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_employee_type_id = kwargs.get('constants_employee_type_id', None)
        if not constants_employee_type_id:
            raise Exception("constants_employee_type_id is required for deletion.")

        constants_employee_types = db_session.query(ConstantsEmployeeType).filter(
            ConstantsEmployeeType.constantsEmployeeTypeID == constants_employee_type_id
        ).first()

        if not constants_employee_types:
            raise Exception(f"ConstantsEmployeeType with ID {constants_employee_type_id} not found.")

        db_session.delete(constants_employee_types)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants employee type deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsEmployeePayType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        employee_pay_type_id = kwargs.get('employee_pay_type_id', None)
        constants_employee_pay_types = []
        if employee_pay_type_id:
            constants_employee_pay_types = db_session.query(ConstantsEmployeePayType).filter(ConstantsEmployeePayType.constantsEmployeePayTypeID == employee_pay_type_id).all()
        else:
            constants_employee_pay_types = db_session.query(ConstantsEmployeePayType).all()

        schema = ConstantsEmployeePayTypeSchema(many=True)
        constants_employee_type_data = schema.dump(constants_employee_pay_types)

        response_data.update({
            "success": True,
            "data": constants_employee_type_data,
            "message": "constants employee pay type data retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createConstantsEmployeePayType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        
        constants_employee_pay_types = ConstantsEmployeePayType(**{key: value for key, value in data.items() if hasattr(ConstantsEmployeePayType, key)})
        db_session.add(constants_employee_pay_types)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "constants employee pay types created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 

def updateConstantsEmployeePayType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEmployeePayTypeID = body.get('constantsEmployeePayTypeID', None)
        if not constantsEmployeePayTypeID:
            raise Exception("constantsEmployeePayTypeID not provided in the request body.")


        constants_employee_pay_types = db_session.query(ConstantsEmployeePayType).filter_by(constantsEmployeePayTypeID=constantsEmployeePayTypeID).first()
        
        if not constants_employee_pay_types:
            raise Exception(f"constants employee pay type with ID {constantsEmployeePayTypeID} not found.")

        
        for key, value in body.items():
            if hasattr(constants_employee_pay_types, key):
                setattr(constants_employee_pay_types, key, value)

        db_session.commit()
        schema = ConstantsEmployeePayTypeSchema()
        data = schema.dump(constants_employee_pay_types)

        response_data.update({
            "success": True,
            "data": data,
            "message": "constants employee pay types updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def deleteConstantsEmployeePayType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        employee_pay_type_id = kwargs.get('employee_pay_type_id', None)
        if not employee_pay_type_id:
            raise Exception("employee_pay_type_id is required for deletion.")

        constants_employee_pay_types = db_session.query(ConstantsEmployeePayType).filter(
            ConstantsEmployeePayType.constantsEmployeePayTypeID == employee_pay_type_id
        ).first()

        if not constants_employee_pay_types:
            raise Exception(f"ConstantsEmployeePayType with ID {constants_employee_pay_types} not found.")

        db_session.delete(constants_employee_pay_types)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants employee pay types deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getAllConstantsData(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        # Query all tables
        employee_types = db_session.query(ConstantsEmployeeType).all()
        employee_pay_types = db_session.query(ConstantsEmployeePayType).all()
        call_types = db_session.query(ConstantsEntityCallType).all()
        call_results = db_session.query(ConstantsEntityCallResult).all()
        property_structures = db_session.query(ConstantsEntityPropertyStructure).all()
        sources = db_session.query(ConstantsEntitySource).all()
        property_lookups = db_session.query(ConstantsPropertyLookUp).all()
        phone_types = db_session.query(ConstantsPhoneType).all()
        employment_statuses = db_session.query(ConstantsEntityEmploymentStatus).all()
        marital_statuses = db_session.query(ConstantsEntityMaritalStatus).all()
        product_types = db_session.query(ConstantsProductType).all()
        market_types = db_session.query(ConstantsMarketType).all()
        sales_job_dispositions = db_session.query(ConstantsSalesJobDispositon).all()
        appointment_dispositions = db_session.query(ConstantsAppointmentDisposition).all()
        states = db_session.query(ConstantsUSAStates).all()
        voucher_types = db_session.query(ConstantsVoucherType).all()
        relation_types = db_session.query(ConstantsRelationType).all()
        deliveryWare_house = db_session.query(ConstantsDeliveryWarehouse).all()
        materials_vendor = db_session.query(ConstantsMaterialsVendor).all()


        # Serialize the data using schemas
        employee_types_data = ConstantsEmployeeTypeSchema(many=True).dump(employee_types)
        employee_pay_types_data = ConstantsEmployeePayTypeSchema(many=True).dump(employee_pay_types)
        call_types_data = ConstantsEntityCallTypeSchema(many=True).dump(call_types)
        call_results_data = ConstantsEntityCallResultSchema(many=True).dump(call_results)
        property_structures_data = ConstantsEntityPropertyStructureSchema(many=True).dump(property_structures)
        sources_data = []
        for source in sources:
            sub_sources = db_session.query(ConstantsEntitySubSource).filter_by(constantsEntitySourceID=source.constantsEntitySourceID).all()
            sub_sources_data = ConstantsEntitySubSourceSchema(many=True).dump(sub_sources)
            source_data = ConstantsEntitySourceSchema().dump(source)
            source_data["sub_sources"] = sub_sources_data
            sources_data.append(source_data)
        
        property_lookups_data = ConstantsPropertyLookUpSchema(many=True).dump(property_lookups)
        phone_types_data = ConstantsPhoneTypeSchema(many=True).dump(phone_types)
        employment_statuses_data = ConstantsEntityEmploymentStatusSchema(many=True).dump(employment_statuses)
        marital_statuses_data = ConstantsEntityMaritalStatusSchema(many=True).dump(marital_statuses)
        product_types_data = ConstantsProductTypeSchema(many=True).dump(product_types)
        market_types_data = ConstantsMarketTypeSchema(many=True).dump(market_types)
        sales_job_dispositions_data = ConstantsSalesJobDispositonSchema(many=True).dump(sales_job_dispositions)
        appointment_dispositions_data = ConstantsAppointmentDispositionSchema(many=True).dump(appointment_dispositions)
        states_data = ConstantsUSAStatesSchema(many=True).dump(states)
        relation_types_data = ConstantsRelationTypeSchema(many=True).dump(relation_types)
        voucher_types_data = ConstantsVoucherTypeSchema(many=True).dump(voucher_types)
        deliveryWare_house_data = ConstantsDeliveryWarehouseSchema(many=True).dump(deliveryWare_house)
        materials_vendor_data = ConstantsMaterialsVendorSchema(many=True).dump(materials_vendor)

        # Combine all data into one response
        response_data.update({
            "success": True,
            "data": {
                "employee_types": employee_types_data,
                "employee_pay_types": employee_pay_types_data,
                "call_types": call_types_data,
                "call_results": call_results_data,
                "property_structures": property_structures_data,
                "sources": sources_data,
                "property_lookups": property_lookups_data,
                "phone_types": phone_types_data,
                "employment_status": employment_statuses_data,
                "marital_status": marital_statuses_data,
                "product_types": product_types_data,
                "market_types": market_types_data,
                "appointment_dispositions" : appointment_dispositions_data,
                "sales_job_dispositions" : sales_job_dispositions_data,
                "states" : states_data,
                "relation_types" : relation_types_data,
                "voucher_types" : voucher_types_data,
                "materials_vendor" : materials_vendor_data,
                "deliveryware_house" : deliveryWare_house_data
            },
            "message": "All constants data retrieved successfully.",
        })

        return {'statusCode': 201, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsPhoneType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_phone_type_id = kwargs.get('constants_phone_type_id', None)
        schema = ConstantsPhoneTypeSchema(many=True if not constants_phone_type_id else False)

        if constants_phone_type_id:
            constants_phone_type = db_session.query(ConstantsPhoneType).filter(ConstantsPhoneType.constantsPhoneTypeID == constants_phone_type_id).first()

            data = schema.dump(constants_phone_type)
            message = "constants phone type retrived successfully"
        else:
            constants_phone_types = db_session.query(ConstantsPhoneType).all()
            data = schema.dump(constants_phone_types)
            message = "constants phone types retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsPhoneType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_phone_type_id = kwargs.get('constants_phone_type_id', None)
        if not constants_phone_type_id:
            raise Exception("constants_entity_source_id is required for deletion.")

        constants_phone_type = db_session.query(ConstantsPhoneType).filter(
            ConstantsPhoneType.constantsPhoneTypeID == constants_phone_type_id
        ).first()

        if not constants_phone_type:
            raise Exception(f"ConstantsPhoneType with ID {constants_phone_type_id} not found.")

        db_session.delete(constants_phone_type)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants phone type deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsPhoneType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_phone_type = ConstantsPhoneType(**{key: value for key, value in data.items() if hasattr(ConstantsPhoneType, key)})

        db_session.add(constants_phone_type)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants phone type created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsPhoneType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsPhoneTypeID = body.get('constantsPhoneTypeID', None)

        if not constantsPhoneTypeID:
            raise Exception("constantsPhoneTypeID not provided in the request body.")


        constants_phone_type = db_session.query(ConstantsPhoneType).filter_by(constantsPhoneTypeID = constantsPhoneTypeID).first()
        
        if not constants_phone_type:
            raise Exception(f"constants phone type with ID {constantsPhoneTypeID} not found.")

        for key, value in body.items():
            if hasattr(constants_phone_type, key):
                setattr(constants_phone_type, key, value)

        db_session.commit()
        schema = ConstantsPhoneTypeSchema()
        data = schema.dump(constants_phone_type)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants phone type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsEntityEmploymentStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_employment_status_id = kwargs.get('constants_employment_status_id', None)
        schema = ConstantsEntityEmploymentStatusSchema(many=True if not constants_employment_status_id else False)

        if constants_employment_status_id:
            constants_employment_status = db_session.query(ConstantsEntityEmploymentStatus).filter(ConstantsEntityEmploymentStatus.constantsEntityEmploymentStatusID == constants_employment_status_id).first()

            data = schema.dump(constants_employment_status)
            message = "constants employment status retrived successfully"
        else:
            constants_employment_statuses = db_session.query(ConstantsEntityEmploymentStatus).all()
            data = schema.dump(constants_employment_statuses)
            message = "constants employmrnt status retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsEntityEmploymentStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_employment_status = ConstantsEntityEmploymentStatus(**{key: value for key, value in data.items() if hasattr(ConstantsEntityEmploymentStatus, key)})

        db_session.add(constants_employment_status)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants employment status created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsEntityEmploymentStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEntityEmploymentStatusID = body.get('constantsEntityEmploymentStatusID', None)

        if not constantsEntityEmploymentStatusID:
            raise Exception("constantsPhoneTypeID not provided in the request body.")


        constants_phone_type = db_session.query(ConstantsEntityEmploymentStatus).filter_by(constantsEntityEmploymentStatusID = constantsEntityEmploymentStatusID).first()
        
        if not constants_phone_type:
            raise Exception(f"constants employment status with ID {constantsEntityEmploymentStatusID} not found.")

        for key, value in body.items():
            if hasattr(constants_phone_type, key):
                setattr(constants_phone_type, key, value)

        db_session.commit()
        schema = ConstantsEntityEmploymentStatusSchema()
        data = schema.dump(constants_phone_type)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants employment status updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsEntityEmploymentStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_employment_status_id = kwargs.get('constants_employment_status_id', None)
        if not constants_employment_status_id:
            raise Exception("constants_employment_status_id is required for deletion.")

        constants_employment_status = db_session.query(ConstantsEntityEmploymentStatus).filter(
            ConstantsEntityEmploymentStatus.constantsEntityEmploymentStatusID == constants_employment_status_id
        ).first()

        if not constants_employment_status:
            raise Exception(f"ConstantsEntityCallType with ID {constants_employment_status_id} not found.")

        db_session.delete(constants_employment_status)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity employment status deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsAppointmentDisposition(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_appointment_disposition_id = kwargs.get('constants_appointment_disposition_id', None)
        schema = ConstantsAppointmentDispositionSchema(many=True if not constants_appointment_disposition_id else False)

        if constants_appointment_disposition_id:
            constants_appointment_disposition = db_session.query(ConstantsAppointmentDisposition).filter(ConstantsAppointmentDisposition.constantsAppointmentDispositionID == constants_appointment_disposition_id).first()

            data = schema.dump(constants_appointment_disposition)
            message = "constants appointment disposition retrived successfully"
        else:
            constants_appointment_dispositions = db_session.query(ConstantsAppointmentDisposition).all()
            data = schema.dump(constants_appointment_dispositions)
            message = "constants appointment disposition retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsAppointmentDisposition(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_appointment_disposition = ConstantsAppointmentDisposition(**{key: value for key, value in data.items() if hasattr(ConstantsAppointmentDisposition, key)})

        db_session.add(constants_appointment_disposition)
        db_session.commit()
        

        response_data.update({
            "success" : True,
            "message": "constants appointment disposition created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsAppointmentDisposition(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsAppointmentDispositionID = body.get('constantsAppointmentDispositionID', None)

        if not constantsAppointmentDispositionID:
            raise Exception("constantsAppointmentDispositionID not provided in the request body.")


        constants_appointment_disposition = db_session.query(ConstantsAppointmentDisposition).filter_by(constantsAppointmentDispositionID = constantsAppointmentDispositionID).first()
        
        if not constants_appointment_disposition:
            raise Exception(f"constants phone type with ID {constantsAppointmentDispositionID} not found.")

        for key, value in body.items():
            if hasattr(constants_appointment_disposition, key):
                setattr(constants_appointment_disposition, key, value)

        db_session.commit()
        schema = ConstantsAppointmentDispositionSchema()
        data = schema.dump(constants_appointment_disposition)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants appointment disposition updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsAppointmentDisposition(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_appointment_disposition_id = kwargs.get('constants_appointment_disposition_id', None)
        if not constants_appointment_disposition_id:
            raise Exception("constants_entity_call_type_id is required for deletion.")

        constants_appointment_disposition = db_session.query(ConstantsAppointmentDisposition).filter(
            ConstantsAppointmentDisposition.constantsAppointmentDispositionID == constants_appointment_disposition_id
        ).first()

        if not constants_appointment_disposition:
            raise Exception(f"constantsAppointmentDisposition with ID {constants_appointment_disposition_id} not found.")

        db_session.delete(constants_appointment_disposition)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants appointment disposition deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsEntityMaritalStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_marital_status_id = kwargs.get('constants_marital_status_id', None)
        schema = ConstantsEntityMaritalStatusSchema(many=True if not constants_marital_status_id else False)

        if constants_marital_status_id:
            constants_marital_status = db_session.query(ConstantsEntityMaritalStatus).filter(ConstantsEntityMaritalStatus.constantsEntityMaritalStatusID == constants_marital_status_id).first()

            data = schema.dump(constants_marital_status)
            message = "constants marital status retrived successfully"
        else:
            constants_marital_statuses = db_session.query(ConstantsEntityMaritalStatus).all()
            data = schema.dump(constants_marital_statuses)
            message = "constants marital status retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsEntityMaritalStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_phone_type = ConstantsEntityMaritalStatus(**{key: value for key, value in data.items() if hasattr(ConstantsEntityMaritalStatus, key)})

        db_session.add(constants_phone_type)
        db_session.commit()
        

        response_data.update({
            "success" : True,
            "message": "constants marital status created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsEntityMaritalStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        ConstantsEntityMaritalStatusID = body.get('constantsEntityMaritalStatusID', None)

        if not ConstantsEntityMaritalStatusID:
            raise Exception("constantsEntityMaritalStatusID not provided in the request body.")


        constants_marital_status = db_session.query(ConstantsEntityMaritalStatus).filter_by(constantsEntityMaritalStatusID = ConstantsEntityMaritalStatusID).first()
        
        if not constants_marital_status:
            raise Exception(f"constants phone type with ID {ConstantsEntityMaritalStatusID} not found.")

        for key, value in body.items():
            if hasattr(constants_marital_status, key):
                setattr(constants_marital_status, key, value)

        db_session.commit()
        schema = ConstantsEntityMaritalStatusSchema()
        data = schema.dump(constants_marital_status)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants marital status updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def deleteConstantsEntityMaritalStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_marital_status_id = kwargs.get('constants_marital_status_id', None)
        if not constants_marital_status_id:
            raise Exception("constants_marital_status_id is required for deletion.")

        constants_marital_status = db_session.query(ConstantsEntityMaritalStatus).filter(
            ConstantsEntityMaritalStatus.constantsEntityMaritalStatusID == constants_marital_status_id
        ).first()

        if not constants_marital_status:
            raise Exception(f"ConstantsEntityMaritalStatus with ID {constants_marital_status_id} not found.")

        db_session.delete(constants_marital_status)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity marital status deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsEntityPropertyStructure(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_property_structure_id = kwargs.get('constants_entity_property_structure_id', None)
        schema = ConstantsEntityPropertyStructureSchema(many=True if not constants_entity_property_structure_id else False)

        if constants_entity_property_structure_id:
            constants_entity_property_structure = db_session.query(ConstantsEntityPropertyStructure).filter(ConstantsEntityPropertyStructure.constantsEntityPropertyStructureID == constants_entity_property_structure_id).first()

            data = schema.dump(constants_entity_property_structure)
            message = "Constants Entity Property Structure retrived successfully"
        else:
            constants_entity_property_structures = db_session.query(ConstantsEntityPropertyStructure).all()
            data = schema.dump(constants_entity_property_structures)
            message = "Constants Entity Property Structure retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsEntityPropertyStructure(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_property_structure_id = kwargs.get('constants_entity_property_structure_id', None)
        if not constants_entity_property_structure_id:
            raise Exception("constants_entity_property_structure_id is required for deletion.")

        constants_entity_property_structure = db_session.query(ConstantsEntityPropertyStructure).filter(
            ConstantsEntityPropertyStructure.constantsEntityPropertyStructureID == constants_entity_property_structure_id
        ).first()

        if not constants_entity_property_structure:
            raise Exception(f"ConstantsEntityPropertyStructure with ID {constants_entity_property_structure_id} not found.")

        db_session.delete(constants_entity_property_structure)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity property structure deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createConstantsEntityPropertyStructure(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_entity_property_structure = ConstantsEntityPropertyStructure(**{key: value for key, value in data.items() if hasattr(ConstantsEntityPropertyStructure, key)})

        db_session.add(constants_entity_property_structure)
        db_session.commit()
        

        response_data.update({
            "success" : True,
            "message": "Constants Entity Property Structure created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsEntityPropertyStructure(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEntityPropertyStructureID = body.get('constantsEntityPropertyStructureID', None)

        if not constantsEntityPropertyStructureID:
            raise Exception("constantsEntityPropertyStructureID not provided in the request body.")


        constants_entity_property_structure = db_session.query(ConstantsEntityPropertyStructure).filter_by(constantsEntityPropertyStructureID = constantsEntityPropertyStructureID).first()
        
        if not constants_entity_property_structure:
            raise Exception(f"Constants Entity Property Structure with ID {constantsEntityPropertyStructureID} not found.")

        for key, value in body.items():
            if hasattr(constants_entity_property_structure, key):
                setattr(constants_entity_property_structure, key, value)

        db_session.commit()
        schema = ConstantsEntityPropertyStructureSchema()
        data = schema.dump(constants_entity_property_structure)
        response_data.update({
            "success": True,
            "data": data,
            "message": "Constants Entity Property Structure updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsEntitySource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_source_id = kwargs.get('constants_entity_source_id', None)
        schema = ConstantsEntitySourceSchema(many=True if not constants_entity_source_id else False)

        if constants_entity_source_id:
            constants_entity_source = db_session.query(ConstantsEntitySource).filter(ConstantsEntitySource.constantsEntitySourceID == constants_entity_source_id).first()

            data = schema.dump(constants_entity_source)
            message = "constants entity source retrived successfully"
        else:
            constants_entity_sources = db_session.query(ConstantsEntitySource).all()
            data = schema.dump(constants_entity_sources)
            message = "constants entity source retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsEntitySource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_source_id = kwargs.get('constants_entity_source_id', None)
        if not constants_entity_source_id:
            raise Exception("constants_entity_source_id is required for deletion.")

        constants_entity_source= db_session.query(ConstantsEntitySource).filter(
            ConstantsEntitySource.constantsEntitySourceID == constants_entity_source_id
        ).first()

        if not constants_entity_source:
            raise Exception(f"ConstantsEntitySource with ID {constants_entity_source_id} not found.")

        db_session.delete(constants_entity_source)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity source deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsEntitySource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_entity_source = ConstantsEntitySource(**{key: value for key, value in data.items() if hasattr(ConstantsEntitySource, key)})

        db_session.add(constants_entity_source)
        db_session.commit()
        

        response_data.update({
            "success" : True,
            "message": "constants entity source created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsEntitySource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEntitySourceID = body.get('constantsEntitySourceID', None)

        if not constantsEntitySourceID:
            raise Exception("constantsEntitySourceID not provided in the request body.")


        constants_entity_source = db_session.query(ConstantsEntitySource).filter_by(constantsEntitySourceID = constantsEntitySourceID).first()
        
        if not constants_entity_source:
            raise Exception(f"constants entity source result with ID {constantsEntitySourceID} not found.")

        for key, value in body.items():
            if hasattr(constants_entity_source, key):
                setattr(constants_entity_source, key, value)

        db_session.commit()
        schema = ConstantsEntitySourceSchema()
        data = schema.dump(constants_entity_source)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants entity source updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsEntitySubSource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_sub_source_id = kwargs.get('constants_entity_sub_source_id', None)
        schema = ConstantsEntitySubSourceSchema(many=True if not constants_entity_sub_source_id else False)

        if constants_entity_sub_source_id:
            constants_entity_sub_source = db_session.query(ConstantsEntitySubSource).filter(ConstantsEntitySubSource.constantsEntitySubSourceID == constants_entity_sub_source_id).first()

            data = schema.dump(constants_entity_sub_source)
            message = "constants entity sub source retrived successfully"
        else:
            constants_entity_sub_sources = db_session.query(ConstantsEntitySubSource).all()
            data = schema.dump(constants_entity_sub_sources)
            message = "constants entity sub source retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsEntitySubSource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_sub_source_id = kwargs.get('constants_entity_sub_source_id', None)
        if not constants_entity_sub_source_id:
            raise Exception("constants_entity_sub_source_id is required for deletion.")

        constants_entity_sub_source= db_session.query(ConstantsEntitySubSource).filter(
            ConstantsEntitySubSource.constantsEntitySubSourceID == constants_entity_sub_source_id
        ).first()

        if not constants_entity_sub_source:
            raise Exception(f"ConstantsEntitySubSource with ID {constants_entity_sub_source_id} not found.")

        db_session.delete(constants_entity_sub_source)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity sub source deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsEntitySubSource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_entity_sub_source = ConstantsEntitySubSource(**{key: value for key, value in data.items() if hasattr(ConstantsEntitySubSource, key)})

        db_session.add(constants_entity_sub_source)
        db_session.commit()
        response_data.update({
            "success" : True,
            "data" : data,
            "message": "constants entity sub source created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsEntitySubSource(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEntitySubSourceID = body.get('constantsEntitySubSourceID', None)

        if not constantsEntitySubSourceID:
            raise Exception("constantsEntitySubSourceID not provided in the request body.")


        constants_entity_sub_source = db_session.query(ConstantsEntitySubSource).filter_by(constantsEntitySubSourceID = constantsEntitySubSourceID).first()
        
        if not constants_entity_sub_source:
            raise Exception(f"constants entity call result with ID {constantsEntitySubSourceID} not found.")

        for key, value in body.items():
            if hasattr(constants_entity_sub_source, key):
                setattr(constants_entity_sub_source, key, value)

        db_session.commit()
        schema = ConstantsEntitySubSourceSchema()
        data = schema.dump(constants_entity_sub_source)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants entity sub source updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsPropertyLookUp(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_property_lookup_id = kwargs.get('constants_property_lookup_id', None)
        schema = ConstantsPropertyLookUpSchema(many=True if not constants_property_lookup_id else False)

        if constants_property_lookup_id:
            constants_property_lookup = db_session.query(ConstantsPropertyLookUp).filter(ConstantsPropertyLookUp.constantsPropertyLookUpID == constants_property_lookup_id).first()

            data = schema.dump(constants_property_lookup)
            message = "constants property lookup retrived successfully"
        else:
            constants_property_lookups = db_session.query(ConstantsPropertyLookUp).all()
            data = schema.dump(constants_property_lookups)
            message = "constants property lookup retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsPropertyLookUp(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_property_lookup_id = kwargs.get('constants_property_lookup_id', None)
        if not constants_property_lookup_id:
            raise Exception("constants_entity_source_id is required for deletion.")

        constants_property_lookup= db_session.query(ConstantsPropertyLookUp).filter(
            ConstantsPropertyLookUp.constantsPropertyLookUpID == constants_property_lookup_id
        ).first()

        if not constants_property_lookup:
            raise Exception(f"ConstantsPropertyLookUp with ID {constants_property_lookup_id} not found.")

        db_session.delete(constants_property_lookup)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants property lookup deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsPropertyLookUp(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_property_lookup = ConstantsPropertyLookUp(**{key: value for key, value in data.items() if hasattr(ConstantsPropertyLookUp, key)})

        db_session.add(constants_property_lookup)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants property lookup created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsPropertyLookUp(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsPropertyLookUpID = body.get('constantsPropertyLookUpID', None)

        if not constantsPropertyLookUpID:
            raise Exception("constantsPropertyLookUpID not provided in the request body.")


        constants_property_lookup = db_session.query(ConstantsPropertyLookUp).filter_by(constantsPropertyLookUpID = constantsPropertyLookUpID).first()
        
        if not constants_property_lookup:
            raise Exception(f"constants property lookup with ID {constantsPropertyLookUpID} not found.")

        for key, value in body.items():
            if hasattr(constants_property_lookup, key):
                setattr(constants_property_lookup, key, value)

        db_session.commit()
        schema = ConstantsPropertyLookUpSchema()
        data = schema.dump(constants_property_lookup)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants property lookup updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsUSAStates(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_usa_states_id = kwargs.get('constants_usa_states_id', None)
        schema = ConstantsUSAStatesSchema(many=True if not constants_usa_states_id else False)

        if constants_usa_states_id:
            constants_usa_states = db_session.query(ConstantsUSAStates).filter(ConstantsUSAStates.constantsUSAStatesID == constants_usa_states_id).first()

            data = schema.dump(constants_usa_states)
            message = "Constants USA States retrived successfully"
        else:
            consants_usa_states = db_session.query(ConstantsUSAStates).all()
            data = schema.dump(consants_usa_states)
            message = "Constants USA States retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsUSAStates(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_usa_states_id = kwargs.get('constants_usa_states_id', None)
        if not constants_usa_states_id:
            raise Exception("constants_usa_states_id is required for deletion.")

        constants_usa_states = db_session.query(ConstantsUSAStates).filter(
            ConstantsUSAStates.constantsUSAStatesID == constants_usa_states_id
        ).first()

        if not constants_usa_states:
            raise Exception(f"constants usa states with ID {constants_usa_states_id} not found.")

        db_session.delete(constants_usa_states)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants_usa_states deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createConstantsUSAStates(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_usa_states = ConstantsUSAStates(**{key: value for key, value in data.items() if hasattr(ConstantsUSAStates, key)})

        db_session.add(constants_usa_states)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants usa states created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsUSAStates(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsUSAStatesID = body.get('constantsUSAStatesID', None)

        if not constantsUSAStatesID:
            raise Exception("constantsUSAStatesID not provided in the request body.")


        constants_usa_states = db_session.query(ConstantsUSAStates).filter_by(constantsUSAStatesID = constantsUSAStatesID).first()
        
        if not constants_usa_states:
            raise Exception(f"constants usa states with ID {constantsUSAStatesID} not found.")

        for key, value in body.items():
            if hasattr(constants_usa_states, key):
                setattr(constants_usa_states, key, value)

        db_session.commit()
        schema = ConstantsUSAStatesSchema()
        data = schema.dump(constants_usa_states)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants usa states updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsRelationType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_relation_type_id = kwargs.get('constants_relation_type_id', None)
        schema = ConstantsRelationTypeSchema(many=True if not constants_relation_type_id else False)

        if constants_relation_type_id:
            constants_relation_type = db_session.query(ConstantsRelationType).filter(ConstantsRelationType.constantsRelationTypeID == constants_relation_type_id).first()

            data = schema.dump(constants_relation_type)
            message = "constants relation type retrived successfully"
        else:
            constants_relation_types = db_session.query(ConstantsRelationType).all()
            data = schema.dump(constants_relation_types)
            message = "constants relation type retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsRelationType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_relation_type_id = kwargs.get('constants_relation_type_id', None)
        if not constants_relation_type_id:
            raise Exception("constants_relation_type_id is required for deletion.")

        constants_relation_type = db_session.query(ConstantsRelationType).filter(
            ConstantsRelationType.constantsRelationTypeID == constants_relation_type_id
        ).first()

        if not constants_relation_type:
            raise Exception(f"constants relation type with ID {constants_relation_type_id} not found.")

        db_session.delete(constants_relation_type)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants relation type deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsRelationType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_relation_type = ConstantsRelationType(**{key: value for key, value in data.items() if hasattr(ConstantsRelationType, key)})

        db_session.add(constants_relation_type)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants relation type created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    
    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsRelationType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsRelationTypeID = body.get('constantsRelationTypeID', None)

        if not constantsRelationTypeID:
            raise Exception("constantsRelationTypeID not provided in the request body.")


        constants_relation_type = db_session.query(ConstantsRelationType).filter_by(constantsRelationTypeID = constantsRelationTypeID).first()
        
        if not constants_relation_type:
            raise Exception(f"Constants Relation Type with ID {ConstantsRelationType} not found.")

        for key, value in body.items():
            if hasattr(constants_relation_type, key):
                setattr(constants_relation_type, key, value)

        db_session.commit()
        schema = ConstantsRelationTypeSchema()
        data = schema.dump(constants_relation_type)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants relation type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsEntityCallType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_call_type_id = kwargs.get('constants_entity_call_type_id', None)
        schema = ConstantsEntityCallTypeSchema(mant=True if not constants_entity_call_type_id else False)

        if constants_entity_call_type_id:
            constants_entity_call_type = db_session.query(ConstantsEntityCallType).filter(ConstantsEntityCallType.constantsEntityCallTypeID == constants_entity_call_type_id).first()

            data = schema.dump(constants_entity_call_type)
            message = "Constants Entity Call Type retrived successfully"
        else:
            constants_entity_call_types = db_session.query(ConstantsEntityCallType).all()
            data = schema.dump(constants_entity_call_types)
            message = "Constants Entity Call Types retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsEntityCallType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_entity_call_type = ConstantsEntityCallType(**{key: value for key, value in data.items() if hasattr(ConstantsEntityCallType, key)})

        db_session.add(constants_entity_call_type)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "Constants Entity Call Type created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 
    
def updateConstantsEntityCallType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEntityCallTypeID = body.get('constantsEntityCallTypeID', None)

        if not constantsEntityCallTypeID:
            raise Exception("constantsEntityCallTypeID not provided in the request body.")


        constants_entity_call_type = db_session.query(ConstantsEntityCallType).filter_by(constantsEntityCallTypeID = constantsEntityCallTypeID).first()
        
        if not constants_entity_call_type:
            raise Exception(f"constants entity call type with ID {constantsEntityCallTypeID} not found.")

        for key, value in body.items():
            if hasattr(constants_entity_call_type, key):
                setattr(constants_entity_call_type, key, value)

        db_session.commit()
        schema = ConstantsEntityCallTypeSchema()
        data = schema.dump(constants_entity_call_type)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants entity call type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsEntityCallType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_call_type_id = kwargs.get('constants_entity_call_type_id', None)
        if not constants_entity_call_type_id:
            raise Exception("constants_entity_call_type_id is required for deletion.")

        constants_entity_call_type = db_session.query(ConstantsEntityCallType).filter(
            ConstantsEntityCallType.constantsEntityCallTypeID == constants_entity_call_type_id
        ).first()

        if not constants_entity_call_type:
            raise Exception(f"ConstantsEntityCallType with ID {constants_entity_call_type_id} not found.")

        db_session.delete(constants_entity_call_type)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity call type deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)} 
    

def getConstantsSalesJobDispositon(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_sales_job_disposition_id = kwargs.get('constants_sales_job_disposition_id', None)
        schema = ConstantsSalesJobDispositonSchema(many=True if not constants_sales_job_disposition_id else False)

        if constants_sales_job_disposition_id:
            constants_sales_job_disposition = db_session.query(ConstantsSalesJobDispositon).filter(ConstantsSalesJobDispositon.constantsSalesJobDispositonID == constants_sales_job_disposition_id).first()

            data = schema.dump(constants_sales_job_disposition)
            message = "constants sales job disposition retrived successfully"
        else:
            constants_sales_job_dispositions = db_session.query(ConstantsSalesJobDispositon).all()
            data = schema.dump(constants_sales_job_dispositions)
            message = "constants sales job disposition retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsSalesJobDispositon(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_sales_job_disposition = ConstantsSalesJobDispositon(**{key: value for key, value in data.items() if hasattr(ConstantsSalesJobDispositon, key)})

        db_session.add(constants_sales_job_disposition)
        db_session.commit()
        
        response_data.update({
            "success" : True,
            "message": "constants sales job disposition created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsSalesJobDispositon(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsSalesJobDispositonID = body.get('constantsSalesJobDispositonID', None)

        if not constantsSalesJobDispositonID:
            raise Exception("constantsSalesJobDispositonID not provided in the request body.")


        constants_sales_job_disposition = db_session.query(ConstantsSalesJobDispositon).filter_by(constantsSalesJobDispositonID = constantsSalesJobDispositonID).first()
        
        if not constants_sales_job_disposition:
            raise Exception(f"constants sales job disposition with ID {constantsSalesJobDispositonID} not found.")

        for key, value in body.items():
            if hasattr(constants_sales_job_disposition, key):
                setattr(constants_sales_job_disposition, key, value)

        db_session.commit()
        schema = ConstantsSalesJobDispositonSchema()
        data = schema.dump(constants_sales_job_disposition)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants sales job disposition updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsSalesJobDispositon(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_sales_job_disposition_id = kwargs.get('constants_sales_job_disposition_id', None)
        if not constants_sales_job_disposition_id:
            raise Exception("constants_sales_job_disposition_id is required for deletion.")

        constants_sales_job_disposition = db_session.query(ConstantsSalesJobDispositon).filter(
            ConstantsSalesJobDispositon.constantsSalesJobDispositonID == constants_sales_job_disposition_id
        ).first()

        if not constants_sales_job_disposition:
            raise Exception(f"ConstantsSalesJobDispositon with ID {constants_sales_job_disposition_id} not found.")

        db_session.delete(constants_sales_job_disposition)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants sales job disposition deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsEntityCallResult(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_call_result_id = kwargs.get('constants_entity_call_result_id', None)
        schema = ConstantsEntityCallResultSchema(many=True if not constants_entity_call_result_id else False)

        if constants_entity_call_result_id:
            constants_entity_call_result = db_session.query(ConstantsEntityCallResult).filter(ConstantsEntityCallResult.constantsEntityCallResultID == constants_entity_call_result_id).first()

            data = schema.dump(constants_entity_call_result)
            message = "Constants Entity Call Result retrived successfully"
        else:
            constants_entity_call_results = db_session.query(ConstantsEntityCallResult).all()
            data = schema.dump(constants_entity_call_results)
            message = "Constants Entity Call Result retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsEntityCallResult(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_entity_call_result_id = kwargs.get('constants_entity_call_result_id', None)
        if not constants_entity_call_result_id:
            raise Exception("constants_entity_call_result_id is required for deletion.")

        constants_entity_call_result = db_session.query(ConstantsEntityCallResult).filter(
            ConstantsEntityCallResult.constantsEntityCallResultID == constants_entity_call_result_id
        ).first()

        if not constants_entity_call_result:
            raise Exception(f"ConstantsEntityCallResult with ID {constants_entity_call_result_id} not found.")

        db_session.delete(constants_entity_call_result)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity call result deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}  
    
def createConstantsEntityCallResult(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_entity_call_result = ConstantsEntityCallResult(**{key: value for key, value in data.items() if hasattr(ConstantsEntityCallResult, key)})

        db_session.add(constants_entity_call_result)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "Constants Entity Call Result created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsEntityCallResult(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsEntityCallResultID = body.get('constantsEntityCallResultID', None)

        if not constantsEntityCallResultID:
            raise Exception("constantsEntityCallResultID not provided in the request body.")


        constants_entity_call_result = db_session.query(ConstantsEntityCallResult).filter_by(constantsEntityCallResultID = constantsEntityCallResultID).first()
        
        if not constants_entity_call_result:
            raise Exception(f"constants entity call result with ID {constantsEntityCallResultID} not found.")

        for key, value in body.items():
            if hasattr(constants_entity_call_result, key):
                setattr(constants_entity_call_result, key, value)

        db_session.commit()
        schema = ConstantsEntityCallResultSchema()
        data = schema.dump(constants_entity_call_result)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants entity call result updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsDeliveryWarehouse(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_delivery_warehouse_id = kwargs.get('constants_delivery_warehouse_id', None)
        schema = ConstantsDeliveryWarehouseSchema(many=True if not constants_delivery_warehouse_id else False)

        if constants_delivery_warehouse_id:
            constants_delivery_warehouse = db_session.query(ConstantsDeliveryWarehouse).filter(ConstantsDeliveryWarehouse.constantsDeliveryWarehouseID == constants_delivery_warehouse_id).first()

            data = schema.dump(constants_delivery_warehouse)
            message = "constants delivery warehouse retrived successfully"
        else:
            constants_delivery_warehouse = db_session.query(ConstantsDeliveryWarehouse).all()
            data = schema.dump(constants_delivery_warehouse)
            message = "constants delivery warehouse retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsDeliveryWarehouse(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_delivery_warehouse = ConstantsDeliveryWarehouse(**{key: value for key, value in data.items() if hasattr(ConstantsDeliveryWarehouse, key)})

        db_session.add(constants_delivery_warehouse)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants delivery warehouse created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }  

def updateConstantsDeliveryWarehouse(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsDeliveryWarehouseID = body.get('constantsDeliveryWarehouseID', None)

        if not constantsDeliveryWarehouseID:
            raise Exception("constantsDeliveryWarehouseID not provided in the request body.")


        constants_delivery_warehouse = db_session.query(ConstantsDeliveryWarehouse).filter_by(constantsDeliveryWarehouseID = constantsDeliveryWarehouseID).first()
        
        if not constants_delivery_warehouse:
            raise Exception(f"constants delivery warehouse with ID {constantsDeliveryWarehouseID} not found.")

        for key, value in body.items():
            if hasattr(constants_delivery_warehouse, key):
                setattr(constants_delivery_warehouse, key, value)

        db_session.commit()
        schema = ConstantsDeliveryWarehouseSchema()
        data = schema.dump(constants_delivery_warehouse)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants delivery warehouse updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsDeliveryWarehouse(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_delivery_warehouse_id = kwargs.get('constants_delivery_warehouse_id', None)
        if not constants_delivery_warehouse_id:
            raise Exception("constants_delivery_warehouse_id is required for deletion.")

        constants_delivery_warehouse = db_session.query(ConstantsDeliveryWarehouse).filter(
            ConstantsDeliveryWarehouse.constantsDeliveryWarehouseID == constants_delivery_warehouse_id
        ).first()

        if not constants_delivery_warehouse:
            raise Exception(f"constantsDeliveryWarehouse with ID {constants_delivery_warehouse_id} not found.")

        db_session.delete(constants_delivery_warehouse)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants entity call result deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getConstantsVoucherType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_voucher_type_id = kwargs.get('constants_voucher_type_id', None)
        schema = ConstantsVoucherTypeSchema(many=True if not constants_voucher_type_id else False)

        if constants_voucher_type_id:
            constants_voucher_type = db_session.query(ConstantsVoucherType).filter(ConstantsVoucherType.constantsVoucherTypeID == constants_voucher_type_id).first()

            data = schema.dump(constants_voucher_type)
            message = "constants voucher type retrived successfully"
        else:
            constants_voucher_type = db_session.query(ConstantsVoucherType).all()
            data = schema.dump(constants_voucher_type)
            message = "constants voucher type retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsVoucherType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_voucher_type_id = kwargs.get('constants_voucher_type_id', None)
        if not constants_voucher_type_id:
            raise Exception("constants_voucher_type_id is required for deletion.")

        constants_voucher_type = db_session.query(ConstantsVoucherType).filter(
            ConstantsVoucherType.constantsVoucherTypeID == constants_voucher_type_id
        ).first()

        if not constants_voucher_type:
            raise Exception(f"constantsVoucherType with ID {constants_voucher_type_id} not found.")

        db_session.delete(constants_voucher_type)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants voucher type deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createConstantsVoucherType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_voucher_type = ConstantsVoucherType(**{key: value for key, value in data.items() if hasattr(ConstantsVoucherType, key)})

        db_session.add(constants_voucher_type)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants voucher type created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 
    
def updateConstantsVoucherType(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsVoucherTypeID = body.get('constantsVoucherTypeID', None)

        if not constantsVoucherTypeID:
            raise Exception("constantsVoucherTypeID not provided in the request body.")


        constants_voucher_type = db_session.query(ConstantsVoucherType).filter_by(constantsVoucherTypeID = constantsVoucherTypeID).first()
        
        if not constants_voucher_type:
            raise Exception(f"constants voucher type with ID {constantsVoucherTypeID} not found.")

        for key, value in body.items():
            if hasattr(constants_voucher_type, key):
                setattr(constants_voucher_type, key, value)

        db_session.commit()
        schema = ConstantsVoucherTypeSchema()
        data = schema.dump(constants_voucher_type)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants voucher type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getConstantsMaterialsVendor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_materials_vendor_id = kwargs.get('constants_materials_vendor_id', None)
        schema = ConstantsMaterialsVendorSchema(many=True if not constants_materials_vendor_id else False)

        if constants_materials_vendor_id:
            constants_materials_vendor = db_session.query(ConstantsMaterialsVendor).filter(ConstantsMaterialsVendor.constantsMaterialsVendorID == constants_materials_vendor_id).first()

            data = schema.dump(constants_materials_vendor)
            message = "constants materials vendor retrived successfully"
        else:
            constants_materials_vendor = db_session.query(ConstantsMaterialsVendor).all()
            data = schema.dump(constants_materials_vendor)
            message = "constants materials vendor retrived successfully"
        

        response_data.update({
            "success": True,
            "data": data,
            "message": message,
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteConstantsMaterialsVendor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        constants_materials_vendor_id = kwargs.get('constants_materials_vendor_id', None)
        if not constants_materials_vendor_id:
            raise Exception("constants_materials_vendor_id is required for deletion.")

        constants_materials_vendor = db_session.query(ConstantsMaterialsVendor).filter(
            ConstantsMaterialsVendor.constantsMaterialsVendorID == constants_materials_vendor_id
        ).first()

        if not constants_materials_vendor:
            raise Exception(f"ConstantsMaterialsVendor with ID {constants_materials_vendor_id} not found.")

        db_session.delete(constants_materials_vendor)
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "constants materials vendor deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createConstantsMaterialsVendor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        constants_materials_vendor = ConstantsMaterialsVendor(**{key: value for key, value in data.items() if hasattr(ConstantsMaterialsVendor, key)})

        db_session.add(constants_materials_vendor)
        db_session.commit()

        response_data.update({
            "success" : True,
            "message": "constants materials vendor created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateConstantsMaterialsVendor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        constantsMaterialsVendorID = body.get('constantsMaterialsVendorID', None)

        if not constantsMaterialsVendorID:
            raise Exception("constantsMaterialsVendorID not provided in the request body.")


        constants_materials_vendor = db_session.query(ConstantsVoucherType).filter_by(constantsMaterialsVendorID = constantsMaterialsVendorID).first()
        
        if not constants_materials_vendor:
            raise Exception(f"constants Materials Vendor with ID {constantsMaterialsVendorID} not found.")

        for key, value in body.items():
            if hasattr(constants_materials_vendor, key):
                setattr(constants_materials_vendor, key, value)

        db_session.commit()
        schema = ConstantsMaterialsVendorSchema()
        data = schema.dump(constants_materials_vendor)
        response_data.update({
            "success": True,
            "data": data,
            "message": "constants voucher type updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}







 

    
