import json
from db_models import SalesJob, Entity, EntityProperty, ConstantsVoucherType, EmployeeMaster, SubContractor, SubContractorInstaller, SalesJobAddendum, EntityPhone
from schema import SalesJobSchema, EntitySchema, EntityPropertySchema, ConstantsVoucherTypeSchema, EmployeeSchema, SubContractorInstallerSchema, SalesJobAddendumSchema, PayrollAddendumSchema, EntityPhoneSchema
from utils import api_response

def getSalesJobs(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session')
        query_params = kwargs.get('query_params', {})
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        page = int(query_params.get('page', 1))
        page_size = 50
        offset = (page - 1) * page_size

        schema = SalesJobSchema(many=True)
        
        total_records = db_session.query(SalesJob).count()
        
        sales_jobs = db_session.query(SalesJob)\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        data = schema.dump(sales_jobs)
        
        total_pages = (total_records + page_size - 1) // page_size

        response_data.update({
            "success": True,
            "data": data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "page_size": page_size,
                "total_records": total_records
            },
            "message": "Sales jobs retrieved successfully"
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def getSalesJobById(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session')
        sales_job_id = kwargs.get('sales_job_id')
        
        if not db_session:
            raise Exception("db_session not passed to handler")
            
        if not sales_job_id:
            raise Exception("Sales job ID is required")

        # Get sales job information
        sales_job = db_session.query(SalesJob)\
            .filter(SalesJob.salesJobID == sales_job_id)\
            .first()
            
        if not sales_job:
            response_data.update({
                "success": False,
                "message": "Sales job not found"
            })
            return {'statusCode': 404, 'body': json.dumps(response_data)}

        # Get property information
        property_info = db_session.query(EntityProperty)\
            .filter(EntityProperty.entityPropertyID == sales_job.entityPropertyID)\
            .first()

        # Get customer information and phone numbers
        customer = None
        phone_numbers = []
        if property_info and property_info.entityID:
            customer = db_session.query(Entity)\
                .filter(Entity.entityID == property_info.entityID)\
                .first()
            
            # Get phone numbers for this entity
            if customer:
                phone_numbers = db_session.query(EntityPhone)\
                    .filter(EntityPhone.entityID == customer.entityID)\
                    .all()

        # Initialize schemas
        sales_job_schema = SalesJobSchema()
        entity_schema = EntitySchema()
        property_schema = EntityPropertySchema()
        phone_schema = EntityPhoneSchema(many=True)
        employee_schema = EmployeeSchema()
        installer_schema = SubContractorInstallerSchema()

        # Get voucher type information
        voucher_type = None
        if sales_job.salesJobVoucherTypeID:
            voucher_type = db_session.query(ConstantsVoucherType)\
                .filter(ConstantsVoucherType.constantsVoucherTypeID == sales_job.salesJobVoucherTypeID)\
                .first()

        # Get project managers information
        project_manager1 = None
        project_manager2 = None
        if sales_job.salesJobProjectManager1ID:
            project_manager1 = db_session.query(EmployeeMaster)\
                .filter(EmployeeMaster.employeeID == sales_job.salesJobProjectManager1ID)\
                .first()
        if sales_job.salesJobProjectManager2ID:
            project_manager2 = db_session.query(EmployeeMaster)\
                .filter(EmployeeMaster.employeeID == sales_job.salesJobProjectManager2ID)\
                .first()

        # Get installer information
        installer1 = None
        installer2 = None
        if sales_job.salesJobSubContractorInstaller1ID:
            installer1 = db_session.query(SubContractorInstaller)\
                .filter(SubContractorInstaller.subContractorInstallerID == sales_job.salesJobSubContractorInstaller1ID)\
                .first()
        if sales_job.salesJobSubContractorInstaller2ID:
            installer2 = db_session.query(SubContractorInstaller)\
                .filter(SubContractorInstaller.subContractorInstallerID == sales_job.salesJobSubContractorInstaller2ID)\
                .first()

        # Get sales rep information
        sales_rep = None
        if sales_job.salesJobSalesRepID:
            sales_rep = db_session.query(EmployeeMaster)\
                .filter(EmployeeMaster.employeeID == sales_job.salesJobSalesRepID)\
                .first()
            
            # Get previewer information
            previewed_by = None
            if sales_job.salesJobPreviewedByID:
                previewed_by = db_session.query(EmployeeMaster)\
                    .filter(EmployeeMaster.employeeID == sales_job.salesJobPreviewedByID)\
                    .first()
        # Prepare the response data
        overview_data = {
            "salesJob": sales_job_schema.dump(sales_job),
            "propertyInfo": property_schema.dump(property_info) if property_info else None,
            "customerInfo": {
                **(entity_schema.dump(customer) if customer else {}),
                "phoneNumbers": phone_schema.dump(phone_numbers) if phone_numbers else []
            },
            "contractDetails": {
                "salesJobContractAmount": sales_job.salesJobContractAmount,
                "salesJobFinancedAmount": sales_job.salesJobFinancedAmount,
                "salesJobDiscountPercentage": sales_job.salesJobDiscountPercentage,
                "salesJobAdjustedContractValue": sales_job.salesJobAdjustedContractValue,
                "salesJobContractDate": sales_job.salesJobContractDate.isoformat() if sales_job.salesJobContractDate else None,
                "salesJobNumber": sales_job.salesJobNumber,
                "salesJobEntityAppointmentNumber": sales_job.salesJobEntityAppointmentNumber,
                "salesJobEntityCustomerRecordNumber": sales_job.salesJobEntityCustomerRecordNumber,
                "salesJobSalesRepID": sales_job.salesJobSalesRepID,
                "salesJobSubContractorID": sales_job.salesJobSubContractorID,
            },
            "projectDetails": {
                "salesJobIsPermitRequired": sales_job.salesJobIsPermitRequired,
                "salesJobIsHOAAppRequired": sales_job.salesJobIsHOAAppRequired,
                "salesJobIsQualityControlled": sales_job.salesJobIsQualityControlled,
            },
            "voucherDetails": {
                "salesJobVoucherTypeID": sales_job.salesJobVoucherTypeID,
                "voucherType": ConstantsVoucherTypeSchema().dump(voucher_type) if voucher_type else None,
                "salesJobVoucherSentDate": sales_job.salesJobVoucherSentDate.isoformat() if sales_job.salesJobVoucherSentDate else None,
            },
            "teamDetails": {
                "salesRep": employee_schema.dump(sales_rep) if sales_rep else None,
                "projectManagers": {
                    "primary": employee_schema.dump(project_manager1) if project_manager1 else None,
                    "secondary": employee_schema.dump(project_manager2) if project_manager2 else None
                },
                "installers": {
                    "primary": {
                        "installerID": sales_job.salesJobSubContractorInstaller1ID,
                        "details": installer_schema.dump(installer1) if installer1 else None
                    },
                    "secondary": {
                        "installerID": sales_job.salesJobSubContractorInstaller2ID,
                        "details": installer_schema.dump(installer2) if installer2 else None
                    }
                },
                "subContractorID": sales_job.salesJobSubContractorID,
                "previewedBy": {
                    "previewerID": sales_job.salesJobPreviewedByID,
                    "details": employee_schema.dump(previewed_by) if previewed_by else None
                }
            },
        }

        response_data.update({
            "success": True,
            "data": overview_data,
            "message": "Sales job overview retrieved successfully"
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong while fetching sales job overview"
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def getSalesJobAddendumList(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session')
        query_params = kwargs.get('query_params', {})
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        page = int(query_params.get('page', 1))
        page_size = 50
        offset = (page - 1) * page_size

        # Initialize schemas
        addendum_schema = SalesJobAddendumSchema(many=True)
        employee_schema = EmployeeSchema()
        
        total_records = db_session.query(SalesJobAddendum).count()
        
        if total_records == 0:
            response_data.update({
                "success": True,
                "data": [],
                "pagination": {
                    "current_page": page,
                    "total_pages": 0,
                    "page_size": page_size,
                    "total_records": 0
                },
                "message": "No addendum records found"
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}

        addendums = db_session.query(SalesJobAddendum)\
            .order_by(SalesJobAddendum.salesJobAddendumDate.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        data = addendum_schema.dump(addendums)

        # Get employee details for each addendum
        for addendum in data:
            if addendum.get('salesJobAddendumSoldByID'):
                sold_by = db_session.query(EmployeeMaster)\
                    .filter(EmployeeMaster.employeeID == addendum['salesJobAddendumSoldByID'])\
                    .first()
                addendum['soldBy'] = employee_schema.dump(sold_by) if sold_by else None

        total_pages = (total_records + page_size - 1) // page_size

        response_data.update({
            "success": True,
            "data": data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "page_size": page_size,
                "total_records": total_records
            },
            "message": "Addendum records retrieved successfully"
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong while fetching addendum records"
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def getPayrollAddendumList(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session')
        query_params = kwargs.get('query_params', {})
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        page = int(query_params.get('page', 1))
        page_size = 50
        offset = (page - 1) * page_size

        # Initialize schemas
        payroll_schema = PayrollAddendumSchema(many=True)
        employee_schema = EmployeeSchema()
        
        total_records = db_session.query(SalesJobAddendum).count()
        
        if total_records == 0:
            response_data.update({
                "success": True,
                "data": [],
                "pagination": {
                    "current_page": page,
                    "total_pages": 0,
                    "page_size": page_size,
                    "total_records": 0
                },
                "message": "No payroll addendum records found"
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}

        payroll_addendums = db_session.query(SalesJobAddendum)\
            .order_by(SalesJobAddendum.salesJobAddendumDate.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        data = payroll_schema.dump(payroll_addendums)

        # Get employee details for each addendum
        for addendum in data:
            if addendum.get('salesJobAddendumSoldByID'):
                sold_by = db_session.query(EmployeeMaster)\
                    .filter(EmployeeMaster.employeeID == addendum['salesJobAddendumSoldByID'])\
                    .first()
                addendum['soldBy'] = employee_schema.dump(sold_by) if sold_by else None

        total_pages = (total_records + page_size - 1) // page_size

        response_data.update({
            "success": True,
            "data": data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "page_size": page_size,
                "total_records": total_records
            },
            "message": "Payroll addendum records retrieved successfully"
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong while fetching payroll addendum records"
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def rejectSalesJobAddendum(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session')
        addendum_id = kwargs.get('addendum_id')
        
        if not db_session:
            raise Exception("db_session not passed to handler")
            
        if not addendum_id:
            raise Exception("Addendum ID is required")

        # Get addendum record
        addendum = db_session.query(SalesJobAddendum)\
            .filter(SalesJobAddendum.salesJobAddendumID == addendum_id)\
            .first()
            
        if not addendum:
            response_data.update({
                "success": False,
                "message": "Addendum not found"
            })
            return {'statusCode': 404, 'body': json.dumps(response_data)}

        # Instead of deleting, update the isRejected flag
        addendum.salesJobAddendumIsRejected = True
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "Addendum marked as rejected successfully"
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        db_session.rollback()
        response_data.update({
            "error": str(e),
            "message": "Something went wrong while updating the addendum"
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}