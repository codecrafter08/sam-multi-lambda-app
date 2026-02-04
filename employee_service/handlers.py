from db_models import EmployeeMaster, SalesPersonAvailability, SalesPersonAvailabilitySlots, ConstantsEmployeeType
import json
from utils import api_response
from schema import EmployeeMasterSchema, SalesPersonAvailabilitySlotsSchema
from datetime import datetime




def getEmployees(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        query_params = kwargs.get('query_params', {}) or {}

        if not db_session:
            raise Exception("db_session not passed to handler")

        employee_id = kwargs.get('employee_id', None)
        constants_employee_type_names = query_params.get('constantsEmployeeTypeName', None)

        employee_query = db_session.query(EmployeeMaster)

        if employee_id:
            employee = employee_query.filter(EmployeeMaster.employeeID == employee_id).first()
            if not employee:
                raise Exception(f"Employee with ID '{employee_id}' not found.")
            
            schema = EmployeeMasterSchema()
            employees_data = schema.dump(employee)
            response_data.update({
                "success": True,
                "data": employees_data,
                "message": "Employee retrieved successfully."
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}

        elif constants_employee_type_names:
            # Handle multiple names passed as a comma-separated string
            if isinstance(constants_employee_type_names, str):
                constants_employee_type_names = [
                    name.strip() for name in constants_employee_type_names.split(",")
                ]

            # Query all matching employee types
            employee_types = db_session.query(ConstantsEmployeeType).filter(
                ConstantsEmployeeType.constantsEmployeeTypeName.in_(constants_employee_type_names)
            ).all()

            if not employee_types:
                raise Exception(f"Employee types '{constants_employee_type_names}' not found.")
            
            # Extract the IDs of matching employee types
            employee_type_ids = [et.constantsEmployeeTypeID for et in employee_types]

            # Filter employees by matching employee type IDs
            employee_query = employee_query.filter(
                EmployeeMaster.employeeTypeID.in_(employee_type_ids)
            )

        employees = employee_query.all()
        schema = EmployeeMasterSchema(many=True)
        employees_data = schema.dump(employees)

        response_data.update({
            "success": True,
            "data": employees_data,
            "message": "Employees retrieved successfully."
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}



def createEmployee(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        employee = EmployeeMaster(**{key: value for key, value in data.items() if hasattr(EmployeeMaster, key)})
        db_session.add(employee)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "Employee created successfully", 
        })
        return {'statusCode': 201, 'body': json.dumps(response_data) }
    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    

def createOrUpdateSalesPersonAvailabilitySlot(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        body = kwargs.get('body', None)
        if not body:
            raise Exception('Body required, not found')

        salesPersonAvailabilitySlotsDate_str = body.get('salesPersonAvailabilitySlotsDate')
        if not salesPersonAvailabilitySlotsDate_str:
            raise Exception("salesPersonAvailabilitySlotsDate is required and should be in ISO format")
        
        employee_id = body.get("salesPersonID")
        if not employee_id:
            raise Exception("Employee ID is required")
        
        existing_slot = db_session.query(SalesPersonAvailabilitySlots).join(SalesPersonAvailability).filter(
            SalesPersonAvailability.salesPersonID == employee_id,
            SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsDate == body.get('salesPersonAvailabilitySlotsDate')
        ).first()

        if existing_slot:
            for key, value in body.items():
                if hasattr(existing_slot, key):
                    setattr(existing_slot, key, value)

            db_session.commit()
            schema = SalesPersonAvailabilitySlotsSchema()
            data = schema.dump(existing_slot)

            response_data.update({
                "success": True,
                "data": data,
                "message": "SalesPerson Availability Slot updated successfully."
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}

        availability_slot = SalesPersonAvailabilitySlots(**{key: value for key, value in body.items() if hasattr(SalesPersonAvailabilitySlots, key)})
        db_session.add(availability_slot)
        db_session.commit()
        schema = SalesPersonAvailabilitySlotsSchema()
        data = schema.dump(availability_slot)

        availability = SalesPersonAvailability(
            salesPersonID=employee_id,
            salesPersonAvailabilitySlotsID=availability_slot.salesPersonAvailabilitySlotsID
        )
        db_session.add(availability)
        db_session.commit()

        response_data.update({
            "success": True,
            "data": data,
            "message": "SalesPerson Availability Slot created successfully."
        })
        return {'statusCode': 201, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def getSalesPersonAvailabilitySlots(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        # Query for joining SalesPersonAvailability and SalesPersonAvailabilitySlots
        availability_data = (
            db_session.query(
                SalesPersonAvailability.salesPersonID,
                SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsID,
                SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsDate,
                SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsIsMorningAvailable,
                SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsIsAfternoonAvailable,
                SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsIsEveningAvailable,
            )
            .join(
                SalesPersonAvailabilitySlots,
                SalesPersonAvailability.salesPersonAvailabilitySlotsID == SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsID
            )
            .all()
        )

        from collections import defaultdict

        grouped_data = defaultdict(list)
        for record in availability_data:
            grouped_data[record.salesPersonID].append({
                "salesPersonAvailabilitySlotsID": str(record.salesPersonAvailabilitySlotsID),
                "salesPersonAvailabilitySlotsDate": record.salesPersonAvailabilitySlotsDate.isoformat(),
                "isMorningAvailable": record.salesPersonAvailabilitySlotsIsMorningAvailable,
                "isAfternoonAvailable": record.salesPersonAvailabilitySlotsIsAfternoonAvailable,
                "isEveningAvailable": record.salesPersonAvailabilitySlotsIsEveningAvailable,
            })

        # Preparing response
        result = [
            {
                "salesPersonID": str(sales_person_id),
                "availabilitySlots": slots
            }
            for sales_person_id, slots in grouped_data.items()
        ]

        response_data.update({
            "success": True,
            "data": result,
            "message": "Sales person availability retrieved successfully."
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

    



