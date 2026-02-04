from db_models import Entity, EntityCall, EntitySecondaryContactDetails, EntityPropertyContact, EntityAppointments, EntityProperty, SubContractor, SamMultiLambdaAppBaseTable, EntityCallback, EmployeeMaster, EntityAppointmentSelectedProduct, ConstantsAppointmentDisposition, ConstantsProductType, ConstantsMarketType, SubContractorInstaller, EntityPhone, ConstantsProductType, ConstantsPhoneType, ConstantsRelationType
import json
from utils import api_response, handle_phones, get_phone_data, handle_appointments, handle_calls, handle_phones_data, handle_properties, handle_secondary_contacts, send_email, encrypt_data, handle_property_update, handle_products, handle_entity_call_update, handle_secondary_contact_update
from sqlalchemy import and_, or_, func
from schema import EntitySchema, EntityCallSchema, EntitySecondaryContactDetailsSchema,EntityPropertyContactSchema, EntityAppointmentsSchema,EntityPropertySchema,SubContractorSchema, EntityCallbackSchema, SecondaryContactDetailsSchema, SubContractorInstallerSchema, EntityPhoneSchema
from sqlalchemy.orm import aliased
from uuid import UUID


def getEntity(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        query_params = kwargs.get('query_params', {}) or {}

        if not db_session:
            raise Exception("db_session not passed to handler")

        entity_id = kwargs.get('entity_id', None)
        search_query = query_params.get('searchQuery', None)
        sort_by = query_params.get('sort_by', None)
        page_type = query_params.get('pageType', None)

        page = int(query_params.get('page', 1))  
        per_page = 50  

        claims = kwargs.get('claims', {})
        employee_user_id = claims.get('sub', None)
        
        if not employee_user_id:
            raise Exception("Employee ID not found in token")
        
        employee = db_session.query(EmployeeMaster).filter(EmployeeMaster.userID == employee_user_id).first()
        if not employee:
            raise Exception("Employee not found.")

        entity_query = db_session.query(Entity)
        
        if entity_id:
            entity = entity_query.filter(Entity.entityID == entity_id).first()
            if not entity:
                raise Exception("Entity not found.")
            
            if entity.entityInboundRecordIsLocked:
                employee = db_session.query(EmployeeMaster).filter(EmployeeMaster.employeeID == entity.entityInboundRecordLockedByID).first()
                if not employee:
                    raise Exception("Employee not found.")
                data = {
                    "first_name": entity.entityFirstName,
                    "last_name": entity.entityLastName,
                    "locked_by": f"{employee.employeeFirstName} {employee.employeeLastName}"
                }
                response_data.update({
                    "success": True,
                    "data": data,
                    "error": "record_locked",
                    "message": f"Entity is already locked by {employee.employeeFirstName} {employee.employeeLastName}.",
                })
                return {'statusCode': 200, 'body': json.dumps(response_data)}
            else:
                entity.entityInboundRecordIsLocked = True
                entity.entityInboundRecordLockedByID = employee.employeeID
                db_session.commit()
                schema = EntitySchema()
                entity_data = schema.dump(entity)
                phones_data = get_phone_data(db_session, [entity.entityID]) 
                entity_data["phones"] = phones_data.get(entity.entityID, [])
                response_data.update({
                    "success": True,
                    "data": entity_data,
                    "message": "Entity is locked successfully.",
                })
                return {'statusCode': 200, 'body': json.dumps(response_data)}
        
        elif search_query:
            entity_query = entity_query.filter(
                (Entity.entityFirstName.ilike(f'%{search_query}%')) | 
                (Entity.entityLastName.ilike(f'%{search_query}%')) |
                (Entity.entityPhone.ilike(f"%{search_query}%")) |
                ((Entity.entityFirstName + " " + Entity.entityLastName).ilike(f"%{search_query}%")) |
                (Entity.entityCustomerRecordNumber.ilike(f"%{search_query}%"))
            )
        
        # Dynamic filtering based on other attributes in kwargs
        for key, value in query_params.items():
            if hasattr(Entity, key) and value is not None:
                entity_query = entity_query.filter(getattr(Entity, key) == value)

        # Sorting logic
        if sort_by == 'name':
            entity_query = entity_query.order_by(Entity.entityFirstName.asc(), Entity.entityLastName.asc())
        elif sort_by == 'id':
            entity_query = entity_query.order_by(Entity.entityCustomerRecordNumber.asc())
        elif sort_by == 'phone':
            entity_query = entity_query.order_by(Entity.entityPhone.asc())
        elif sort_by == 'created_at':
            entity_query = entity_query.order_by(Entity.created_at.asc())
        elif sort_by == '-name':
            entity_query = entity_query.order_by(Entity.entityFirstName.desc(), Entity.entityLastName.desc())
        elif sort_by == '-id':
            entity_query = entity_query.order_by(Entity.entityCustomerRecordNumber.desc())
        elif sort_by == '-phone':
            entity_query = entity_query.order_by(Entity.entityPhone.desc())
        elif sort_by == '-created_at':
            entity_query = entity_query.order_by(Entity.created_at.desc())
        else:
            entity_query = entity_query.order_by(Entity.entityInitialDataReceivedDate.desc())

        if page_type == 'IBQ':
            # Inbound Queue logic: Exclude duplicates and merged records
            filtered_query = entity_query.filter(
                and_(
                    Entity.entityIsInboundDuplicateRecord == False,
                    Entity.entityIsInboundRecordDeleted == False,
                    Entity.entityIsInboundRecordMerged == False
                )
            )
            has_inbound_record_query = filtered_query.filter(
            and_(
                func.coalesce(Entity.entityInboundRecordNumber, '') != '', 
                    or_(
                        Entity.entityCustomerRecordNumber.is_(None),  
                        func.coalesce(Entity.entityCustomerRecordNumber, '') == '' 
                    )
                )
            )
            no_inbound_record_query = filtered_query.filter(
                and_(
                    func.coalesce(Entity.entityInboundRecordNumber, '') != '',  
                    func.coalesce(Entity.entityCustomerRecordNumber, '') != ''  
                )
            ).order_by(Entity.entityInitialDataReceivedDate.desc())
            has_inbound_record_count = has_inbound_record_query.count()
            # Get total records count
            total_records = filtered_query.count()

            # Calculate total pages
            total_pages = (total_records + per_page - 1) // per_page 

            # Offset for pagination
            offset = (page - 1) * per_page

            # Fetch prioritized records
            inbound_records = has_inbound_record_query.offset(offset).limit(per_page).all()
            print(inbound_records, "records")
            remaining_count = per_page - len(inbound_records)

            if remaining_count > 0:
                remaining_offset = max(0, offset - has_inbound_record_count)
                customer_records = no_inbound_record_query.offset(remaining_offset).limit(remaining_count).all()
                inbound_records.extend(customer_records[:remaining_count])
            
            
            schema = EntitySchema(many=True)
            entities_data = schema.dump(inbound_records)
            entity_ids = [entity["entityID"] for entity in entities_data]
            phones_data = get_phone_data(db_session, entity_ids)
            for entity in entities_data:
                entity_id = UUID(entity["entityID"])
                phones = phones_data.get(entity_id, [])
                if not phones:
                    print(f"No phones found for entity ID: {entity_id}")
                entity["phones"] = phones
            response_data.update({
                "success": True,
                "data": entities_data,
                "pagination": {
                    "total_records": total_records,
                    "total_pages": total_pages,
                    "current_page": page,
                    "per_page": per_page,
                },
                "message": "Entities retrieved successfully.",
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}

        elif page_type == 'prospect_list':
            entity_query = entity_query.filter(Entity.entityCustomerRecordNumber != None)

        entities = entity_query.all()
        schema = EntitySchema(many=True)
        entities_data = schema.dump(entities)
        entity_ids = [entity["entityID"] for entity in entities_data]
        phones_data = get_phone_data(db_session, entity_ids)
        for entity in entities_data:
            entity_id = UUID(entity["entityID"])
            phones = phones_data.get(entity_id, [])
            if not phones:
                print(f"No phones found for entity ID: {entity_id}")
            entity["phones"] = phones
        response_data.update({
            "success": True,
            "data": entities_data,
            "message": "Entities retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}
    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

def createEntity(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        
        phones_data = data.pop('phones', None)
        
        entity = Entity(**{key: value for key, value in data.items() if hasattr(Entity, key)})
        db_session.add(entity)
        db_session.commit()
        handle_phones(db_session, entity, phones_data)
        response_data.update({
            "success" : True,
            "message": "entity created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }


def updateEntity(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        entityID = body.get('entityID', None)
        if not entityID:
            raise Exception("entityID not provided in the request body.")


        entity = db_session.query(Entity).filter_by(entityID=entityID).first()
        
        if not entity:
            raise Exception(f"entity with ID {entityID} not found.")
        
        if body.get('entityInboundRecordIsLocked') == False and entity.entityInboundRecordIsLocked == True:
            entity.entityInboundRecordIsLocked = False
            entity.entityInboundRecordLockedByID = None
            db_session.commit()
            response_data.update({
                "success": True,
                "message": "success",
            })
            return {'statusCode': 200, 'body': json.dumps(response_data)}

        if body.get('entityInboundRecordStatus') == 'MERGED':
            duplicate_entities = db_session.query(Entity).filter(
                Entity.entityPermanentAddressLine1 == entity.entityPermanentAddressLine1,
                Entity.entityID != entityID  
            ).all()

            for duplicate in duplicate_entities:
                # If both address and first name match
                if (duplicate.entityFirstName == entity.entityFirstName and duplicate.entityLastName == entity.entityLastName and duplicate.entityPhone == entity.entityPhone):
                    entity.entityIsInboundRecordMerged = True
                else:
                    entity_secondary_contact_detail = EntitySecondaryContactDetails(
                        entityID = duplicate.entityID,
                        entitySecondaryContactFirstName = duplicate.entityFirstName,
                        entitySecondaryContactLastName = duplicate.entityLastName,
                        entitySecondaryContactRelationshipType = "secondary_contact",
                        entitySecondaryContactDetailsPhone = duplicate.entityPhone,
                        entitySecondaryContactDetailsPhoneType =  duplicate.entityPhoneType,
                        entitySecondaryContactDetailsEmail =  duplicate.entityEmail,
                    )
                    db_session.add(entity_secondary_contact_detail)


        if body.get('entityInboundRecordStatus') == 'ACCEPTED' and body.get('confirm_data') == True:
            sam_multi_lambda_app_base_instance = db_session.query(SamMultiLambdaAppBaseTable).first()
    
            if not sam_multi_lambda_app_base_instance:
                raise Exception("No SamMultiLambdaAppBaseTable record found.")
            
            entity.entityCustomerRecordNumber = sam_multi_lambda_app_base_instance.increment_column('baseCustomerRecordNumber', db_session)
            entity.entityInboundRecordIsLocked = False
            entity.entityInboundRecordLockedByID = None
        elif body.get('entityInboundRecordStatus') == 'REJECTED':
            entity.entityIsInboundRecordMerged = False
            entity.entityIsInboundRecordDeleted = False

        phones_data = body.pop('phones', None)
        properties_data = body.pop('properties', None)
        calls_data = body.pop('calls', None)
        secondary_contacts_data = body.pop('secondary_contacts', None)

        for key, value in body.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        handle_phones(db_session, entity, phones_data)
        handle_secondary_contact_update(db_session, entity, secondary_contacts_data)
        handle_property_update(db_session, entity, properties_data)
        handle_entity_call_update(db_session, entity, calls_data)

        db_session.commit()
        schema = EntitySchema()
        data = schema.dump(entity)
        response_data.update({
            "success": True,
            "data": data,
            "message": "entity updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def getEntityCalls(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        entity_call_id = kwargs.get('entity_call_id', None)
        entity_calls = []

        if entity_call_id:
            entity_calls = db_session.query(EntityCall).filter(EntityCall.entityCallID == entity_call_id).all()
        else:
            entity_calls = db_session.query(EntityCall).all()

        schema = EntityCallSchema(many=True)
        entity_call_data = schema.dump(entity_calls)
        response_data.update({
            "success" : True,
            "data" : entity_call_data,
            "message": "entity calls retrieved successfully.",
        })
        return { 'statusCode': 200,'body': json.dumps(response_data)}
    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }


def createEntityCall(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        entity_call = EntityCall(**{key: value for key, value in data.items() if hasattr(EntityCall, key)})
        db_session.add(entity_call)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "entity call created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e: 
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }


def updateEntitycall(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        entityCallID = body.get('entityCallID', None)
        if not entityCallID:
            raise Exception("entityCallID not provided in the request body.")


        entity_call = db_session.query(EntityCall).filter_by(entityCallID=entityCallID).first()
        
        if not entity_call:
            raise Exception(f"entityPropertyContact with ID {entityCallID} not found.")

        for key, value in body.items():
            if hasattr(entity_call, key):
                setattr(entity_call, key, value)

        db_session.commit()
        schema = EntityCallSchema()
        data = schema.dump(entity_call)


        response_data.update({
            "success": True,
            "data": data,
            "message": "entity call updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
    
def getEntitySecondaryContactDetails(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        entity_secondary_contact_id = kwargs.get('entity_secondary_contact_id', None)

        schema = EntitySecondaryContactDetailsSchema(context={'db_session': db_session})
        
        if entity_secondary_contact_id:
            entity_secondary_contact = db_session.query(EntitySecondaryContactDetails).filter(
                EntitySecondaryContactDetails.customerSecondaryContactDetailsID == entity_secondary_contact_id
            ).first()
            if not entity_secondary_contact:
                raise Exception("Entity secondary contact not found.")
            
            entity_data = schema.dump(entity_secondary_contact)
        else:
            entity_secondary_contacts = db_session.query(EntitySecondaryContactDetails).all()
            
            schema = EntitySecondaryContactDetailsSchema(many=True, context={'db_session': db_session})
            entity_data = schema.dump(entity_secondary_contacts)

        response_data.update({
            "success": True,
            "data": entity_data,
            "message": "Entity secondary contact details retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        db_session.rollback()
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def createEntitySecondaryContactDetail(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        entity_secondary_contact_detail = EntitySecondaryContactDetails(**{key: value for key, value in data.items() if hasattr(EntitySecondaryContactDetails, key)})

        db_session.add(entity_secondary_contact_detail)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "entity secondary contact detail is created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e: 
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }


def updateEntitySecondaryContactDetail(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        customerSecondaryContactDetailsID = body.get('customerSecondaryContactDetailsID', None)
        if not customerSecondaryContactDetailsID:
            raise Exception("customerSecondaryContactDetailsID not provided in the request body.")


        entity_secondary_contact = db_session.query(EntitySecondaryContactDetails).filter_by(customerSecondaryContactDetailsID=customerSecondaryContactDetailsID).first()
        
        if not entity_secondary_contact:
            raise Exception(f"entityPropertyContact with ID {customerSecondaryContactDetailsID} not found.")

        
        for key, value in body.items():
            if hasattr(entity_secondary_contact, key):
                setattr(entity_secondary_contact, key, value)

        db_session.commit()
        schema = SecondaryContactDetailsSchema()
        data = schema.dump(entity_secondary_contact)

        response_data.update({
            "success": True,
            "data": data,
            "message": "entity secondary contact updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def getEntityPropertyContact(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        entity_property_contact_id = kwargs.get('entity_property_contact_id', None)
        schema = EntityPropertyContactSchema(many=True if not entity_property_contact_id else False)

        if entity_property_contact_id:
            entity_property_contacts = db_session.query(EntityPropertyContact).filter(EntityPropertyContact.entityPropertyContactID == entity_property_contact_id).first()

            if not entity_property_contacts:
                raise Exception("entity property contacts not found")
            
            data = schema.dump(entity_property_contacts)
            message = "entity property contacts retrieved successfully."
        else:
            entity_property_contacts = db_session.query(EntityPropertyContact).all()
            data = schema.dump(entity_property_contacts)
            message = "entity property contacts retrieved successfully."

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


def createEntityPropertyContact(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        entity_property_contact = EntityPropertyContact(**{key: value for key, value in data.items() if hasattr(EntityPropertyContact, key)})
        db_session.add(entity_property_contact)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "entity property contact is created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e: 
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }


def updateEntityPropertyContact(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        entityPropertyContactID = body.get('entityPropertyContactID', None)
        if not entityPropertyContactID:
            raise Exception("entityPropertyContactID not provided in the request body.")


        entity_property_contact = db_session.query(EntityPropertyContact).filter_by(entityPropertyContactID=entityPropertyContactID).first()
        
        if not entity_property_contact:
            raise Exception(f"entityPropertyContact with ID {entityPropertyContactID} not found.")

        for key, value in body.items():
            if hasattr(entity_property_contact, key):
                setattr(entity_property_contact, key, value)

        db_session.commit()
        schema = EntityPropertyContactSchema()
        data = schema.dump(entity_property_contact)
        

        response_data.update({
            "success": True,
            "data": data,
            "message": "entity property contact updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def getEntityAppointments(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        # Fixed typo and removed unnecessary tuple assignment
        entity_appointment_id = kwargs.get('entity_appointment_id', None)
        entity_appointments = []

        # Query the database based on whether the entity_appointment_id is provided
        if entity_appointment_id:
            entity_appointments = db_session.query(EntityAppointments).filter(
                EntityAppointments.entityAppointmentsID == entity_appointment_id
            ).all()
        else:
            entity_appointments = db_session.query(EntityAppointments).all()

        # Get all related products for the appointments
        appointment_ids = [appointment.entityAppointmentsID for appointment in entity_appointments]
        selected_products = db_session.query(
            EntityAppointmentSelectedProduct.entityAppointmentsID,
            EntityAppointmentSelectedProduct.constantsProductID,
            EntityAppointmentSelectedProduct.entityAppointmentSelectedProductQuanity,
            ConstantsProductType.constantsProductName
        ).join(
            ConstantsProductType,
            EntityAppointmentSelectedProduct.constantsProductID == ConstantsProductType.constantsProductID
        ).filter(
            EntityAppointmentSelectedProduct.entityAppointmentsID.in_(appointment_ids)
        ).all()

        # Organize products by appointment ID
        products_by_appointment = {}
        for product in selected_products:
            appointment_id = str(product.entityAppointmentsID)
            if appointment_id not in products_by_appointment:
                products_by_appointment[appointment_id] = []
            products_by_appointment[appointment_id].append({
                "constantsProductID": product.constantsProductID,
                "entityAppointmentSelectedProductQuanity": product.entityAppointmentSelectedProductQuanity
            })

        # Serialize the entity appointments and add the products to each
        if entity_appointment_id:
            schema = EntityAppointmentsSchema()
            entity_appointments_data = schema.dump(entity_appointments[0])  # Only get the first appointment (since it's a single object)
            entity_appointments_data["products"] = products_by_appointment.get(entity_appointment_id, [])
        else:
            schema = EntityAppointmentsSchema(many=True)
            entity_appointments_data = schema.dump(entity_appointments)
            for appointment in entity_appointments_data:
                appointment_id = str(appointment["entityAppointmentsID"])
                appointment["products"] = products_by_appointment.get(appointment_id, [])

        # Respond with success and data
        response_data.update({
            "success": True,
            "data": entity_appointments_data,
            "message": "Entity appointments retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getEntityAppointmentsList(**kwargs):
    try:
        response_data = api_response()

        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        query_params = kwargs.get('query_params', {}) or {}
        page = int(query_params.get('page', 1))
        per_page = int(query_params.get('per_page', 50))
        market_filter = query_params.get('market', None) 
        date_filter = query_params.get('appointmentDate', None)
        Employee1 = aliased(EmployeeMaster)
        Employee2 = aliased(EmployeeMaster)

        query = db_session.query(
            EntityAppointments.entityAppointmentsID,
            EntityAppointments.entityAppointmentsSalesRep1,
            EntityAppointments.entityAppointmentsSalesRep2,
            EntityAppointments.entityAppointmentsAppointmentDate.label("AppointmentDate"),
            EntityAppointments.entityAppointmentsNotes.label("Notes"),
            # EntityAppointments.status,
            Entity.entityFirstName,
            Entity.entityLastName,
            Entity.entityInitialDataReceivedSource.label("Source"),
            Entity.entityInitialDataReceivedSubSource.label("Sub_source"),
            EntityProperty.entityPropertyCity.label("City"),
            EntityProperty.entityPropertyState.label("State"),
            EntityProperty.entityPropertyZip.label("Zip"),
            EntityAppointments.entityAppointmentsMarketID,
            ConstantsMarketType.constantsMarketName.label("MarketValue"),
            ConstantsProductType.constantsProductName.label("Product"),
            EntityAppointments.entityAppointmentsAppointmentTime.label("AppointmentTime"),
            ConstantsAppointmentDisposition.constantsAppointmentDisposition.label("Dispo"),
            Employee1.employeeEmail.label("salesRep1_email"),  
            Employee2.employeeEmail.label("salesRep2_email"),
            Entity.entityID.label("entityID")  
        ).outerjoin(
            EntityProperty, EntityAppointments.entityPropertyID == EntityProperty.entityPropertyID
        ).outerjoin(
            Entity, EntityProperty.entityID == Entity.entityID
        ).outerjoin(
            EntityAppointmentSelectedProduct, EntityAppointments.entityAppointmentsID == EntityAppointmentSelectedProduct.entityAppointmentsID
        ).outerjoin(
            ConstantsProductType, EntityAppointmentSelectedProduct.constantsProductID == ConstantsProductType.constantsProductID
        ).outerjoin(
            ConstantsAppointmentDisposition, EntityAppointments.constantsAppointmentDispositionID == ConstantsAppointmentDisposition.constantsAppointmentDispositionID
        ).outerjoin(
            ConstantsMarketType, EntityAppointments.entityAppointmentsMarketID == ConstantsMarketType.constantsMarketID
        ).outerjoin(
            Employee1, EntityAppointments.entityAppointmentsSalesRep1 == Employee1.employeeID
        ).outerjoin(
            Employee2, EntityAppointments.entityAppointmentsSalesRep2 == Employee2.employeeID
        ).filter(
            EntityAppointments.constantsAppointmentDispositionID == 14,
            or_(
                Employee1.employeeTypeID.in_([2, 3]),
                Employee2.employeeTypeID.in_([2, 3])
            )
        )

        if market_filter:
            # Search for the market ID based on the case-insensitive filter
            market_id_result = db_session.query(
                ConstantsMarketType.constantsMarketID
            ).filter(
                ConstantsMarketType.constantsMarketName.ilike(market_filter)  # Using ilike for case-insensitive comparison
            ).first()

            if market_id_result:
                # Market ID found, apply the filter to the main query
                market_id = market_id_result.constantsMarketID
                query = query.filter(EntityAppointments.entityAppointmentsMarketID == market_id)
            else:
                # If no market ID is found, return an empty result with proper pagination
                response_data["data"] = []
                response_data.update({
                    "error": "null",
                    "message": "Entity appointments retrieved successfully.",
                    "pagination": {
                        "current_page": 1,
                        "per_page": per_page,
                        "total_count": 0,
                        "total_pages": 0
                    },
                    "success": True
                })
                return {'statusCode': 200, 'body': json.dumps(response_data)}

        # Apply Date Filter if provided (convert date from dd-mm-yyyy to datetime object)
        if date_filter:
            date_only = func.date(date_filter)
            query = query.filter(func.date(EntityAppointments.entityAppointmentsAppointmentDate) == date_only)
        query = query.distinct()
        total_count = query.count()
        query = query.offset((page - 1) * per_page).limit(per_page)

        entity_appointments = query.all()

        # Fetch phone numbers for each entity
        entity_ids = [appointment.entityID for appointment in entity_appointments]
        phone_numbers_query = db_session.query(
            EntityPhone.entityID,
            EntityPhone.entityPhoneNumber
        ).filter(EntityPhone.entityID.in_(entity_ids))

        phone_numbers = {}
        for phone in phone_numbers_query.all():
            phone_numbers.setdefault(phone.entityID, []).append(phone.entityPhoneNumber)

        response_data["data"] = [
            {
                "salesRep1_id": str(appointment.entityAppointmentsSalesRep1),
                "salesRep1_email": appointment.salesRep1_email,
                "salesRep2_id": str(appointment.entityAppointmentsSalesRep2),
                "salesRep2_email": appointment.salesRep2_email,
                "entityFirstName": appointment.entityFirstName,
                "entityLastName": appointment.entityLastName,
                "source": appointment.Source,
                "sub_source": appointment.Sub_source,
                "city": appointment.City,
                "state": appointment.State,
                "zip": appointment.Zip,
                "market": appointment.MarketValue,
                "product": appointment.Product,
                "appointmentTime": appointment.AppointmentTime.isoformat() if appointment.AppointmentTime else None,
                "appointmentDate": appointment.AppointmentDate.isoformat() if appointment.AppointmentDate else None,
                "dispo": appointment.Dispo,
                "phones": phone_numbers.get(appointment.entityID, []),
                "notes" : appointment.Notes ,
                # "status" : appointment.status,
            } for appointment in entity_appointments
        ]

        total_pages = (total_count + per_page - 1) // per_page

        response_data.update({
            "success": True,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_count": total_count,
                "per_page": per_page
            },
            "message": "Entity appointments retrieved successfully."
        })

        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

    

# def updateAppointment(**kwargs):
#     try:
#         response_data = api_response()
#         db_session = kwargs.get('db_session', None)
#         body = kwargs.get('body', None) 

#         if not db_session:
#             raise Exception("db_session not passed to handler")

#         if not body:
#             raise Exception("Request body is required for updating.")

      
#         entityAppointmentsID = body.get('entityAppointmentsID', None)
#         if not entityAppointmentsID:
#             raise Exception("entityAppointmentsID not provided in the request body.")

#         entity_type_cnf = db_session.query(ConstantsPropertyAppointmentState).filter(
#             ConstantsPropertyAppointmentState.constantsAppointmentState == "CNF"
#         ).first()

#         if not entity_type_cnf:
#             raise Exception("ConstantsPropertyAppointmentState with state 'CNF' not found")
        
#         # Fetch the appointment record to update
#         entity_Appointment = db_session.query(EntityAppointments).filter(
#             EntityAppointments.entityAppointmentsID == entityAppointmentsID
#         ).first()

#         if not entity_Appointment:
#             raise Exception("Appointment not found")
        
#         entity_Appointment.constantsPropertyAppointmentStateID = entity_type_cnf.constantsPropertyAppointmentStateID
#         db_session.commit()
#         schema = EntityAppointmentsSchema()
#         data = schema.dump(entity_Appointment)

    
#         response_data.update({
#             "success": True,
#             "data": data,
#             "message": "entity Appointment updated successfully.",
#         })
#         return {'statusCode': 200, 'body': json.dumps(response_data)}

#     except Exception as e:
#         response_data.update({
#             "error": str(e),
#             "message": "Something went wrong."
#         })
#         return {'statusCode': 500, 'body': json.dumps(response_data)}


def createEntityAppointment(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        products = data.pop('products', [])
        entity_appointment = EntityAppointments(**{key: value for key, value in data.items() if hasattr(EntityAppointments, key)})
        db_session.add(entity_appointment)
        db_session.commit()
        handle_products(db_session, entity_appointment,products)
        response_data.update({
            "success" : True,
            "message": "entity appointment is created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e: 
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    

def updateEntityAppointment(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

        products = body.pop('products', [])
        entityAppointmentsID = body.get('entityAppointmentsID', None)
        if not entityAppointmentsID:
            raise Exception("entityAppointmentsID not provided in the request body.")


        entity_Appointment = db_session.query(EntityAppointments).filter_by(entityAppointmentsID=entityAppointmentsID).first()
        
        if not entity_Appointment:
            raise Exception(f"entity property with ID {entityAppointmentsID} not found.")

        for key, value in body.items():
            if hasattr(entity_Appointment, key):
                setattr(entity_Appointment, key, value)

        db_session.commit()
        schema = EntityAppointmentsSchema()
        data = schema.dump(entity_Appointment)
        handle_products(db_session, entity_Appointment, products)
        response_data.update({
            "success": True,
            "data": data,
            "message": "entity Appointment updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def getEntityProperty(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        entity_property_id = kwargs.get('entity_property_id', None)
        entity_properties = []
        if entity_property_id:
            entity_properties = db_session.query(EntityProperty).filter(EntityProperty.entityPropertyID == entity_property_id).all()
        else:
            entity_properties = db_session.query(EntityProperty).all()

        schema = EntityPropertySchema(many=True)
        entity_property_data = schema.dump(entity_properties)
       

        response_data.update({
            "success": True,
            "data": entity_property_data,
            "message": "entity property retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def createEntityProperty(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')
        entity_property = EntityProperty(**{key: value for key, value in data.items() if hasattr(EntityProperty, key)})
        

        db_session.add(entity_property)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "entity property created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
       

    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) } 


def updateEntityProperty(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None) 

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

      
        entityPropertyID = body.get('entityPropertyID', None)
        if not entityPropertyID:
            raise Exception("entityPropertyID not provided in the request body.")


        entity_property = db_session.query(EntityProperty).filter_by(entityPropertyID=entityPropertyID).first()
        
        if not entity_property:
            raise Exception(f"entity property with ID {entityPropertyID} not found.")

        
        for key, value in body.items():
            if hasattr(entity_property, key):
                setattr(entity_property, key, value)

        db_session.commit()
        schema = EntityPropertySchema()
        data = schema.dump(entity_property)

        response_data.update({
            "success": True,
            "data": data,
            "message": "entity property updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def getSubContractor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

    
        sub_contractor_masters = db_session.query(SubContractor).filter(
            SubContractor.status == 'active'
        ).all()
        schema = SubContractorSchema(many=True)
        sub_contractor_master_data = schema.dump(sub_contractor_masters)
        

        response_data.update({
            "success": True,
            "data": sub_contractor_master_data,
            "message": "sub contractor retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getSubContractorInstaller(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        sub_contractor_id = kwargs.get('sub_contractor_id', None)
        sub_contractor_employee_id = kwargs.get('sub_contractor_installer_id', None)
        sub_contractor_master_employees = []
        if sub_contractor_id:
            sub_contractor_master_employees = db_session.query(SubContractorInstaller).filter(
                SubContractorInstaller.subContractorID == sub_contractor_id,
                SubContractorInstaller.status == 'active'
            ).all()
        elif sub_contractor_employee_id:
            sub_contractor_master_employees = db_session.query(SubContractorInstaller).filter(
                SubContractorInstaller.subContractorEmployeeID == sub_contractor_employee_id,
                SubContractorInstaller.status == 'active'
            ).all()
        else:
            sub_contractor_master_employees = db_session.query(SubContractorInstaller).filter(
                SubContractorInstaller.status == 'active'
            ).all()
        schema = SubContractorInstallerSchema(many=True)
        sub_contractor_master_employees_data = schema.dump(sub_contractor_master_employees)

        response_data.update({
            "success": True,
            "data": sub_contractor_master_employees_data,
            "message": "sub contractor Installer retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def createSubContractor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        sub_contractor = SubContractor(**{key: value for key, value in data.items() if hasattr(SubContractor, key)})

        db_session.add(sub_contractor)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "Subcontractor created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateSubContractor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

        subContractorID = body.get('subContractorID', None)
        if not subContractorID:
            raise Exception("subContractorID not provided in the request body.")

        # Fetch the subcontractor by ID
        sub_contractor = db_session.query(SubContractor).filter_by(subContractorID=subContractorID).first()
        if not sub_contractor:
            raise Exception(f"Subcontractor with ID {subContractorID} not found.")

        # Update the subcontractor fields dynamically from the request body
        for key, value in body.items():
            if hasattr(sub_contractor, key):
                setattr(sub_contractor, key, value)

        db_session.commit()
        schema = SubContractorSchema()
        data = schema.dump(sub_contractor)

        # Prepare response
        response_data.update({
            "success": True,
            "data": data,
            "message": "Subcontractor updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createSubContractorInstaller(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        Sub_Contractor_Installer = SubContractorInstaller(**{key: value for key, value in data.items() if hasattr(SubContractorInstaller, key)})

        db_session.add(Sub_Contractor_Installer)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "Sub Contractor Installer  created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    
def updateSubContractorInstaller(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        if not body:
            raise Exception("Request body is required for updating.")

        subContractorInstallerID = body.get('subContractorInstallerID', None)
        if not subContractorInstallerID:
            raise Exception("subContractorInstallerID not provided in the request body.")

        # Fetch the subcontractor employee by ID
        Sub_Contractor_Installer = (
            db_session.query(SubContractorInstaller)
            .filter_by(subContractorInstallerID=subContractorInstallerID)
            .first()
        )
        if not Sub_Contractor_Installer:
            raise Exception(f"sub Contractor Installer with ID {subContractorInstallerID} not found.")

        # Update the subcontractor employee fields dynamically from the request body
        for key, value in body.items():
            if hasattr(Sub_Contractor_Installer, key):
                setattr(Sub_Contractor_Installer, key, value)

        db_session.commit()
        schema = SubContractorInstallerSchema()
        data = schema.dump(Sub_Contractor_Installer)


        # Prepare response
        response_data.update({
            "success": True,
            "data": data,
            "message": "Sub Contractor Installer updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteSubContractor(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        sub_contractor_id = kwargs.get('sub_contractor_id', None)

        if not sub_contractor_id:
            raise Exception("sub_contractor_id is required for deletion.")

        sub_contractor = db_session.query(SubContractor).filter(
            SubContractor.subContractorID == sub_contractor_id
        ).first()

        if not sub_contractor_id:
            raise Exception(f"subContractor with ID {sub_contractor_id} not found.")

        sub_contractor.status = 'deleted'
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "Sub Contractor deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def deleteSubContractorInstaller(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)

        if not db_session:
            raise Exception("db_session not passed to handler")

        sub_contractor_installer_id = kwargs.get('sub_contractor_installer_id', None)
        if not sub_contractor_installer_id:
            raise Exception("sub_contractor_installer_id is required for deletion.")

        Sub_Contractor_Installer = db_session.query(SubContractorInstaller).filter(
            SubContractorInstaller.subContractorInstallerID == sub_contractor_installer_id
        ).first()

        if not Sub_Contractor_Installer:
            raise Exception(f"sub contractorinstaller with ID {sub_contractor_installer_id} not found.")

        Sub_Contractor_Installer.status = 'deleted'
        db_session.commit()

        response_data.update({
            "success": True,
            "message": "Sub Contractor Installer deleted successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "success": False,
            "message": "Something went wrong.",
            "error": str(e),
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def createCallback(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        data = kwargs.get('body', None)
        if not data:
            raise Exception('body required, not found')

        prospect_callback = EntityCallback(**{key: value for key, value in data.items() if hasattr(EntityCallback, key)})

        db_session.add(prospect_callback)
        db_session.commit()
        response_data.update({
            "success" : True,
            "message": "Entity Callback created successfully",
        })
        return { 'statusCode': 201,'body': json.dumps(response_data)}
    except Exception as e:  
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return { 'statusCode': 500, 'body': json.dumps(response_data) }
    

def getEntityCallback(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")

        # Query all EntityCallback records
        entity_callbacks = db_session.query(EntityCallback).all()

        schema = EntityCallbackSchema(many=True)
        entity_callbacks_data = schema.dump(entity_callbacks)

        # Update the response with data
        response_data.update({
            "success": True,
            "data": entity_callbacks_data,
            "message": "Entity callbacks retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def updateCallback(**kwargs):
    try:
        # Initialize response data and extract dependencies from kwargs
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None)

        if not db_session:
            raise Exception("db_session not passed to the handler.")

        if not body:
            raise Exception("Request body is required for updating.")

        entityCallbackID = body.get('entityCallbackID', None)
        if not entityCallbackID:
            raise Exception("entityCallbackID not provided in the request body.")

        # Fetch the EntityCallback record by ID
        entity_callback = (
            db_session.query(EntityCallback)
            .filter_by(entityCallbackID=entityCallbackID)
            .first()
        )
        if not entity_callback:
            raise Exception(f"EntityCallback with ID {entityCallbackID} not found.")

        for key, value in body.items():
            if hasattr(entity_callback, key):
                setattr(entity_callback, key, value)

        db_session.commit()
        schema = EntityCallbackSchema()
        data = schema.dump(entity_callback)

        # Prepare response data
        response_data.update({
            "success": True,
            "data": data,
            "message": "EntityCallback updated successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        # Handle exceptions and prepare the error response
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getEntityWithUnissuedAppointments(**kwargs):
    try:
        response_data = api_response()
        query_params = kwargs.get('query_params', {}) or {}
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        market_id = query_params.get('market_id', None)
        appointment_date = query_params.get('appointment_date', None)
        page = int(query_params.get('page', 1))
        per_page = int(query_params.get('per_page', 50))

        # Base query
        query = db_session.query(
            Entity,
            EntityProperty,
            EntityAppointments,
            ConstantsMarketType,
            ConstantsAppointmentDisposition
        ).join(
            EntityProperty, EntityAppointments.entityPropertyID == EntityProperty.entityPropertyID
        ).join(
            Entity, EntityProperty.entityID == Entity.entityID
        ).join(
            ConstantsMarketType, EntityProperty.constantsMarketID == ConstantsMarketType.constantsMarketID
        ).join(
            ConstantsAppointmentDisposition, EntityAppointments.constantsAppointmentDispositionID == ConstantsAppointmentDisposition.constantsAppointmentDispositionID
        ).filter(
            EntityAppointments.entityAppointmentsIssued == False,
            EntityAppointments.constantsAppointmentDispositionID == 14
        )

        if market_id:
            query = query.filter(EntityProperty.constantsMarketID == market_id)

        if appointment_date:
            date_only = func.date(appointment_date)
            query = query.filter(func.date(EntityAppointments.entityAppointmentsAppointmentDate) == date_only)

        query = query.limit(per_page).offset((page - 1) * per_page)

        results = query.all()

        # Prepare entity list with repeated entries for unique appointments
        entity_list = []
        for entity, entity_property, appointment, market, dispo in results:
            # Base entity data
            entity_entry = {
                "entityID": str(entity.entityID),
                "entityFirstName": entity.entityFirstName,
                "entityLastName": entity.entityLastName,
                "source": entity.entityInitialDataReceivedSource,
                "sub_source": entity.entityInitialDataReceivedSubSource,
                "market": market.constantsMarketName,
                "city": entity.entityPermanentCity,
                "state": entity.entityPermanentState,
                "zip": entity.entityPermanentZipcode,
                "phones": [],
                "secondary_phones": [],
                "appointment": {  # Single appointment object
                    "AppointmentDate": appointment.entityAppointmentsAppointmentDate.isoformat(),
                    "AppointmentTime": appointment.entityAppointmentsAppointmentTime.isoformat(),
                    "Dispo": dispo.constantsAppointmentDisposition,
                    "EntityAppointmentsID": str(appointment.entityAppointmentsID),
                    "entityAppointmentsIssued": appointment.entityAppointmentsIssued,
                    "product": []
                }
            }

            # Get phones associated with the entity
            phones = db_session.query(EntityPhone, ConstantsPhoneType).join(
                ConstantsPhoneType, EntityPhone.constantsPhoneTypeID == ConstantsPhoneType.constantsPhoneTypeID
            ).filter(EntityPhone.entityID == entity.entityID).all()

            for phone, phone_type in phones:
                entity_entry["phones"].append({
                    "entityPhoneID": str(phone.entityPhoneID),
                    "phoneType": phone_type.constantsPhoneTypeName,
                    "phoneNumber": phone.entityPhoneNumber
                })

            # Get secondary phones
            secondary_phones = db_session.query(EntitySecondaryContactDetails).filter(
                EntitySecondaryContactDetails.entityID == entity.entityID
            ).all()

            for secondary_contact in secondary_phones:
                entity_entry["secondary_phones"].append({
                    "customerSecondaryContactDetailsID": str(secondary_contact.customerSecondaryContactDetailsID),
                    "contactFirstName": secondary_contact.entitySecondaryContactFirstName,
                    "contactLastName": secondary_contact.entitySecondaryContactLastName,
                    "phone": secondary_contact.entitySecondaryContactDetailsPhone,
                    "email": secondary_contact.entitySecondaryContactDetailsEmail
                })

            # Get associated products for the appointment
            products = db_session.query(EntityAppointmentSelectedProduct, ConstantsProductType).join(
                ConstantsProductType, EntityAppointmentSelectedProduct.constantsProductID == ConstantsProductType.constantsProductID
            ).filter(
                EntityAppointmentSelectedProduct.entityAppointmentsID == appointment.entityAppointmentsID
            ).all()

            for product, product_type in products:
                entity_entry["appointment"]["product"].append({
                    "productID": str(product.constantsProductID),
                    "productName": product_type.constantsProductName,
                    "quantity": product.entityAppointmentSelectedProductQuanity
                })

            # Add the entity entry to the list
            entity_list.append(entity_entry)

        # Correct count query for pagination
        total_filtered_records = db_session.query(EntityAppointments).join(
            EntityProperty, EntityAppointments.entityPropertyID == EntityProperty.entityPropertyID
        ).filter(
            EntityAppointments.entityAppointmentsIssued == False,
            EntityAppointments.constantsAppointmentDispositionID == 14
        ).count()

        # Prepare the final response
        response_data.update({
            "success": True,
            "data": entity_list,  # Return as a flat list
            "message": "Entities with unissued appointments retrieved successfully.",
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_records": total_filtered_records,
                "total_pages": (total_filtered_records + per_page - 1) // per_page
            }
        })

        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def getEntityDetails(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        entity_id = kwargs.get('entity_id', None)
        if not entity_id:
            raise Exception("entity_id not provided")
        
        # Retrieve the main entity details
        entity = db_session.query(Entity).filter(Entity.entityID == entity_id).first()

        if not entity:
            raise Exception("Entity not found")
        
        # Retrieve phone details
        phones = (
            db_session.query(EntityPhone, ConstantsPhoneType.constantsPhoneTypeName)
            .join(ConstantsPhoneType, EntityPhone.constantsPhoneTypeID == ConstantsPhoneType.constantsPhoneTypeID)
            .filter(EntityPhone.entityID == entity_id)
            .all()
        )
        
        # Retrieve secondary contact details with relationship
        secondary_contacts = (
            db_session.query(
                EntitySecondaryContactDetails,
                ConstantsRelationType
            )
            .outerjoin(
                ConstantsRelationType,
                EntitySecondaryContactDetails.entitySecondaryContactRelationshipTypeID == ConstantsRelationType.constantsRelationTypeID
            )
            .filter(EntitySecondaryContactDetails.entityID == entity_id)
            .all()
        )

        # Use schemas to serialize data
        entity_schema = EntitySchema()
        secondary_contact_schema = EntitySecondaryContactDetailsSchema()

        entity_data = entity_schema.dump(entity)
        phones_data = [
            {
                **EntityPhoneSchema().dump(phone),
                "constantsPhoneTypeName": phoneType
            }
            for phone, phoneType in phones
        ]
        
        secondary_contacts_data = [
            {
                **secondary_contact_schema.dump(contact[0]),  # Secondary contact details
                "relationship": {
                    "entitySecondaryContactRelationshipTypeID": contact[1].constantsRelationTypeID if contact[1] else None,
                    "constantsRelationTypeName": contact[1].constantsRelationTypeName if contact[1] else None
                }
            }
            for contact in secondary_contacts
        ]

        # Combine the data
        entity_data["phones"] = phones_data
        entity_data["secondary_contacts"] = secondary_contacts_data

        # Return the response
        response_data.update({
            "success": True,
            "data": entity_data,
            "message": "Entity details retrieved successfully."
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

    

def getEntityPropertyDetails(**kwargs):
    try:
        response_data = api_response()

        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        entity_id = kwargs.get('entity_id', None)
        if not entity_id:
            raise Exception("entity_id not provided")

        properties = db_session.query(EntityProperty).filter(EntityProperty.entityID == entity_id).all()

        property_schema = EntityPropertySchema()
        property_contact_schema = EntityPropertyContactSchema()

        properties_contacts = []
        for property in properties:
          
            contacts = db_session.query(EntityPropertyContact).filter(
                EntityPropertyContact.entityPropertyID == property.entityPropertyID
            ).all()

            contact_data_with_relationship = []
            for contact in contacts:
                relationship = db_session.query(
                    ConstantsRelationType.constantsRelationTypeID,
                    ConstantsRelationType.constantsRelationTypeName
                ).filter(
                    ConstantsRelationType.constantsRelationTypeID == contact.entityPropertyContactRelationTypeID
                ).first()

               
                relationship_data = {
                    "entityPropertyContactRelationTypeID": relationship[0],
                    "constantsRelationTypeName": relationship[1]
                } if relationship else None

                contact_data = property_contact_schema.dump(contact)
                contact_data["relationship"] = relationship_data
                contact_data_with_relationship.append(contact_data)
            property_data = property_schema.dump(property)
            property_data["property_contacts"] = contact_data_with_relationship
            properties_contacts.append(property_data)

        response_data.update({
            "success": True,
            "data": properties_contacts,
            "message": "Entity properties and contacts retrieved successfully."
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    


def getEntityAppointmentDetails(**kwargs):
    try:
        response_data = api_response()

        
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        entity_id = kwargs.get('entity_id',None) 
        if not entity_id:
            raise Exception("entity_id not provided")

   
        entity_property_query = db_session.query(EntityProperty).filter(EntityProperty.entityID == entity_id).all()
        if not entity_property_query:
            raise Exception(f"No properties found for the entity ID {entity_id}")

    
        appointments_data = []
        for entity_property in entity_property_query:
            appointments = db_session.query(EntityAppointments).filter(EntityAppointments.entityPropertyID == entity_property.entityPropertyID).all()
            appointments_data.extend(appointments) 

 
        calls_data = []
        for entity_property in entity_property_query:
            entity_calls = db_session.query(EntityCall).filter(EntityCall.entityID == entity_id).all()
            for entity_call in entity_calls:
              
                callbacks = db_session.query(EntityCallback).filter(EntityCallback.entityCallID == entity_call.entityCallID).all()

                
                call_details = EntityCallSchema().dump(entity_call)  
                serialized_callbacks = [EntityCallbackSchema().dump(callback) for callback in callbacks]  # Serialize callbacks

                calls_data.append({
                    **call_details,  
                    "callbacks": serialized_callbacks  
                })

      
        response_data.update({
            "success": True,
            "data": {
                "Appointments": [EntityAppointmentsSchema().dump(appointment) for appointment in appointments_data],  # Serialize appointments
                "calls": calls_data  # Calls data with callbacks
            },
            "message": "Entity appointments, calls, and callbacks retrieved successfully."
        })

        # Return response with status code and body
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        # Handle any exceptions and update the response with the error
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def createProspectDetail(**kwargs):
    try:
        # Initialize response structure
        response_data = api_response()

        # Get database session
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        # Get and validate the request body
        data = kwargs.get('body', None)
        if not data or 'entity' not in data:
            raise Exception('entity data is required')

        entity_data = data['entity']
        
        # Extract nested data
        phones_data = entity_data.pop('phones', None)
        properties_data = entity_data.pop('properties', None)
        calls_data = entity_data.pop('calls', None)
        secondary_contacts_data = entity_data.pop('secondaryContacts', None)
        appointments_data = entity_data.pop('appointments', None)

        # Create the main Entity
        entity = Entity(**{key: value for key, value in entity_data.items() if hasattr(Entity, key)})
        db_session.add(entity)
        db_session.commit()

        # Handle nested relationships

        # Handle phones
        if phones_data:
            handle_phones_data(db_session, entity, phones_data)

        # Handle properties
        if properties_data:
            handle_properties(db_session, entity, properties_data)

        # Handle calls
        if calls_data:
            handle_calls(db_session, entity, calls_data)

        # Handle secondary contacts
        if secondary_contacts_data:
            handle_secondary_contacts(db_session, entity, secondary_contacts_data)

        # Handle appointments
        if appointments_data:
            handle_appointments(db_session, entity, appointments_data)

        # # Serialize the created entity
        # schema = EntitySchema()
        # serialized_data = schema.dump(entity)

        # Update and return the response
        response_data.update({
            "success": True,
            "message": "Entity created successfully",
        })
        return {'statusCode': 201, 'body': json.dumps(response_data)}

    except Exception as e:
        # Handle errors and rollback transaction
        if 'db_session' in locals() and db_session:
            db_session.rollback()
        response_data.update({
            "success": False,
            "message": str(e),
        })
        return {'statusCode': 400, 'body': json.dumps(response_data)}



def updateIssuedAppointments(**kwargs):
    try:
       
        response_data = api_response() 
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None)

        if not db_session:
            raise Exception("db_session not passed to the handler.")

        if not body:
            raise Exception("Request body is required for updating.")

       
        appointment_ids = body.get('appointment_ids', None)
        if not appointment_ids:
            raise Exception("appointment_ids not provided in the request body.")

        if not isinstance(appointment_ids, list) or not all(isinstance(id, str) for id in appointment_ids):
            raise Exception("appointment_ids must be a list of strings.")

       
        affected_rows = (
            db_session.query(EntityAppointments)
            .filter(EntityAppointments.entityAppointmentsID.in_(appointment_ids))
            .update({EntityAppointments.entityAppointmentsIssued: True}, synchronize_session=False)
        )

        if affected_rows == 0:
            raise Exception("No appointments were updated. Please check the appointment IDs.")

      
        db_session.commit()

       
        response_data.update({
            "success": True,
            "data": {
                "updated_record": affected_rows,
            },
            "message": f"Successfully updated {affected_rows} appointments."
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def updateLockedStatus(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None)

        if not db_session:
            raise Exception("db_session not passed to the handler.")

        if not body:
            raise Exception("Request body is required for updating.")

        entity_ids = body.get('entity_ids', None)
        if not entity_ids:
            raise Exception("entity_ids not provided in the request body.")

        if not isinstance(entity_ids, list) or not all(isinstance(id, str) for id in entity_ids):
            raise Exception("entity_ids must be a list of strings.")

        affected_rows = (
            db_session.query(Entity)
            .filter(Entity.entityID.in_(entity_ids))
            .update({
                Entity.entityInboundRecordIsLocked: False,
                Entity.entityInboundRecordLockedByID: None
            }, synchronize_session=False)
        )

        if affected_rows == 0:
            raise Exception("No entities were updated. Please check the entity IDs.")

        db_session.commit()
        response_data.update({
            "success": True,
            "data": {
                "updated_records": affected_rows,
            },
            "message": f"Successfully updated {affected_rows} entities."
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    
def getAllLockedEntity(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        
        entity_query = db_session.query(Entity).filter( Entity.entityInboundRecordIsLocked == True )

        entities = entity_query.all()
        schema = EntitySchema(many=True)
        entities_data = schema.dump(entities)
        entity_ids = [entity["entityID"] for entity in entities_data]
        phones_data = get_phone_data(db_session, entity_ids)
        for entity in entities_data:
            entity_id = entity["entityID"]
            entity["phones"] = phones_data.get(entity_id, [])
        response_data.update({
            "success": True,
            "data": entities_data,
            "message": "Entities with locked value retrieved successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

BASE_URL = "https://e98ab7h5da.execute-api.us-west-1.amazonaws.com/Prod/public/update-appointment-status"
def sendAppointmentEmail(**kwargs):
    try:
        response_data = api_response()
        db_session = kwargs.get('db_session', None)
        body = kwargs.get('body', None)
        
        if not db_session:
            raise Exception("db_session not passed to handler")
        
        if not body:
            raise Exception("Request body is required for updating.")

        appointment_id = body.get('appointment_id', None)
        sales_person1 = body.get('sales_person1', None)
        sales_person2 = body.get('sales_person2', None)
        email1 = body.get('email1', None)
        email2 = body.get('email2', None)

        if not all([appointment_id, email1, email2]):
            raise ValueError("Missing required query parameters")

        # Create tokens dictionary with sales person information
        tokens = {}

        for email, sales_person in [(email1, sales_person1), (email2, sales_person2)]:
            for status in ["accepted", "rejected"]:
                token_data = {
                    "appointment_id": appointment_id,
                    "email": email,
                    "action": status,
                    "sales_person": sales_person  # Add sales_person to the token data
                }
                token = encrypt_data(token_data)
                tokens[f"{email}_{status}"] = f"{BASE_URL}?token={token}"
                print(tokens, "tokens")

        # Send emails with URLs (simulated here)
        subject = "Appointment Confirmation"
        for email in [email1, email2]:
            body = (
                f"Hello,\n\nPlease use the following links to respond to the appointment:\n\n"
                f"Accept: {tokens[email + '_accepted']}\n"
                f"Reject: {tokens[email + '_rejected']}\n\n"
                "Thank you."
            )
            send_email(subject, body, email)

        response_data.update({
            "success": True,
            "message": "Emails sent successfully.",
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    



