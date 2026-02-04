from db_models import EntityPhone, EntityProperty, EntityPropertyContact, EntityCall, EntityCallback, EntitySecondaryContactDetails, EntityAppointments, ConstantsPhoneType, EntityAppointmentSelectedProduct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#api response
def api_response(success=False, data=None, message=None, error=None):
    response = {
        'success': success,
        'data': data if data is not None else {},
        'message': message if message is not None else 'something went wrong',
        'error': error if error is not None else 'null'
    }
    return response


def handle_phones(db_session, entity, phones_data):
    """
    Handle phone entries for an entity. Updates existing phones if the entity already exists.
    Deletes existing phones and creates new ones in case of an update operation.
    """
    if not phones_data:
        return

    if not isinstance(phones_data, list):
        raise ValueError("Phones data must be a list of phone records.")

    # Delete existing phone entries if entity already has phones (update case)
    if entity.entityID:
        db_session.query(EntityPhone).filter_by(entityID=entity.entityID).delete()

    # Add new phone entries
    for phone in phones_data:
        if not all(k in phone for k in ('entityPhoneNumber', 'constantsPhoneTypeID')):
            raise ValueError("Each phone record must include 'entityPhoneNumber' and 'constantsPhoneTypeID'.")

        new_phone = EntityPhone(
            entityID=entity.entityID,  # Explicitly assign the foreign key
            entityPhoneNumber=phone['entityPhoneNumber'],
            constantsPhoneTypeID=phone.get('constantsPhoneTypeID'),  # Handle optional nullable field
        )
        db_session.add(new_phone)

    db_session.commit()


def handle_phones_data(db_session, entity, phones_data):
    """
    Handle phone number creation for the entity.
    """
    if phones_data:
        for phone in phones_data:
            phone_record = EntityPhone(
                entityPhoneNumber=phone.get("entityPhoneNumber"),
                constantsPhoneTypeID=phone.get("constantsPhoneTypeID"),
                entityID=entity.entityID  # Using the correct entityID column
            )
            db_session.add(phone_record)
        db_session.commit()

def handle_calls(db_session, entity, calls_data):
    """
    Handle call record creation for the entity.
    """
    if calls_data:
        for call_data in calls_data:
            # Extract callbacks separately before passing to EntityCall constructor
            callbacks_data = call_data.pop("callbacks", [])
            call = EntityCall(**call_data)
            call.entityID = entity.entityID  # Link call to the entity
            db_session.add(call)
            db_session.commit()

            # Handle callbacks within the call
            for callback_data in callbacks_data:
                callback = EntityCallback(**callback_data)
                callback.entityCallID = call.entityCallID  # Link callback to call
                db_session.add(callback)
            db_session.commit()


def handle_secondary_contacts(db_session, entity, secondary_contacts_data):
    """
    Handle secondary contacts creation for the entity.
    """
    if secondary_contacts_data:
        for secondary_contact_data in secondary_contacts_data:
            secondary_contact = EntitySecondaryContactDetails(**secondary_contact_data)
            secondary_contact.entityID = entity.entityID  # Link secondary contact to the entity
            db_session.add(secondary_contact)
        db_session.commit()


def handle_properties(db_session, entity, properties_data):
    """
    Handle property creation for the entity, including appointments.
    """
    if properties_data:
        for property_data in properties_data:
            # Extract contacts and appointments separately before passing to EntityProperty constructor
            contacts_data = property_data.pop("contacts", [])
            appointments_data = property_data.pop("appointments", [])

            # Create the property
            entity_property = EntityProperty(**property_data)
            entity_property.entityID = entity.entityID  # Link property to the entity
            db_session.add(entity_property)
            db_session.commit()

            # Handle contacts within the property
            for contact_data in contacts_data:
                contact = EntityPropertyContact(**contact_data)
                contact.entityPropertyID = entity_property.entityPropertyID  # Link contact to property
                db_session.add(contact)
            db_session.commit()

            # Handle appointments for the property
            if appointments_data:
                handle_appointments(db_session, entity, entity_property, appointments_data)

def handle_appointments(db_session, entity, entity_property, appointments_data):
    """
    Handle appointment creation for the entity, linking appointments to properties.
    """
    if appointments_data:
        for appointment_data in appointments_data:
            products_data = appointment_data.pop("products", [])

            appointment = EntityAppointments(**appointment_data)
            appointment.entityPropertyID = entity_property.entityPropertyID  # Link appointment to the property
            db_session.add(appointment)

            if products_data:
                for product_data in products_data:
                    product = EntityAppointmentSelectedProduct(
                        entityAppointmentsID=appointment.entityAppointmentsID,
                        **product_data
                    )
                    db_session.add(product)
        db_session.commit()

def get_phone_data(db_session, entity_ids):
    """
    Function to retrieve phone data for a list of entity IDs or a single entity ID.
    Returns a dictionary where the key is the entityID and the value is a list of phone data.
    """
    # Ensure entity_ids is a list even if a single ID is passed
    if not isinstance(entity_ids, list):
        entity_ids = [entity_ids]

    phones_by_entity = {}
    
    # Fetch phone data for given entity IDs
    if entity_ids:
        phones_query = db_session.query(EntityPhone).filter(EntityPhone.entityID.in_(entity_ids))
        phones = phones_query.all()

        # Organize phone data by entity ID
        for phone in phones:
            phone_type = db_session.query(ConstantsPhoneType).filter(ConstantsPhoneType.constantsPhoneTypeID == phone.constantsPhoneTypeID).first()
            phone_data = {
                "phone_number_id": str(phone.entityPhoneID) if phone else None,
                "phone_number": phone.entityPhoneNumber if phone else None,
                "phone_type": phone_type.constantsPhoneTypeName if phone_type else "Unknown"
            }
            # Add phone data to the corresponding entity ID in the dictionary
            if phone.entityID not in phones_by_entity:
                phones_by_entity[phone.entityID] = []
            phones_by_entity[phone.entityID].append(phone_data)
    
    return phones_by_entity

AES_KEY = bytes.fromhex("0bb5e733a1976c2254fe6ffa2b33c67d90ced3e064d3c5588727b2bc23d900da")
AES_IV = bytes.fromhex("11c59f43ba75de3595f9363c8aa65cdf")

def encrypt_data(data_dict):
    try:
        # Convert dictionary to JSON bytes
        data_bytes = json.dumps(data_dict).encode()
        iv = os.urandom(16)  # Generate a random IV
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad data to be a multiple of AES block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data_bytes) + padder.finalize()

        # Encrypt the data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Combine IV and encrypted data, then encode in Base64
        return base64.urlsafe_b64encode(iv + encrypted_data).decode()
    except Exception as e:
        print(f"Error encrypting data: {e}")
        return None
    



def send_email(subject, body, receiver_email):
    smtp_host = 'email-smtp.us-west-1.amazonaws.com'  
    smtp_port = 587
    sender_email = 'prashant.tyagi.2307@gmail.com'
    receiver_email = receiver_email  


    smtp_user = ''
    smtp_password = ''

    # subject = 'Test Email from AWS SES'
    # body = 'This is a test email sent using AWS SES SMTP credentials.'

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
      
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls() 
        server.login(smtp_user, smtp_password) 
        text = msg.as_string() 
        server.sendmail(sender_email, receiver_email, text)  
        server.quit()  

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

def handle_secondary_contact_update(db_session, entity, secondary_contacts):
    try:
        if not secondary_contacts:
                return
            
        if not isinstance(secondary_contacts, list):
            raise Exception("appointmnets must be provided as a list of objects")
        
        for secondary_contact in secondary_contacts:
            secondary_contact_id = secondary_contact.get('customerSecondaryContactDetailsID')
            if secondary_contact_id:
                entity_secondary_contact = db_session.query(EntitySecondaryContactDetails).filter_by(customerSecondaryContactDetailsID=secondary_contact_id).first()
                if not entity_secondary_contact:
                        raise Exception(f"EntitySecondaryContactDetails with ID {secondary_contact_id} not found")
                
                for key, value in secondary_contact.items():
                    if hasattr(entity_secondary_contact, key):
                        setattr(entity_secondary_contact, key, value)
            else:
                entity_secondary_contact = EntitySecondaryContactDetails(
                    entityID=entity.entityID, 
                    **{key: value for key, value in secondary_contact.items() if hasattr(EntitySecondaryContactDetails, key)}
                )
                db_session.add(entity_secondary_contact)
            
            
        db_session.commit()
        print("entity secondary contact updated successfully")
    except Exception as e:
        raise Exception("Error while updating entity secondary contact data", str(e))
      
def handle_property_update(db_session, entity, properties):
    try:
        if not properties:
            return
        
        if not isinstance(properties, list):
            raise Exception("properties must be provided as a list of objects")
        
        for property in properties:
            entity_property_id = property.get('entityPropertyID')
            
            if entity_property_id:
                entity_property = db_session.query(EntityProperty).filter_by(entityPropertyID=entity_property_id).first()
                if not entity_property:
                    raise Exception(f"EntityProperty with ID {entity_property_id} not found")
                
                for key, value in property.items():
                    if hasattr(entity_property, key) and key != 'property_contact' and key != 'appointments':
                        setattr(entity_property, key, value)
            else:
                entity_property = EntityProperty(
                    entityID=entity.entityID, 
                    **{key: value for key, value in property.items() if hasattr(EntityProperty, key) and key != 'property_contact' and key != 'appointments'}
                )
                db_session.add(entity_property)
                db_session.flush()

            property_contacts = property.get('property_contact', [])
            if not isinstance(property_contacts, list):
                raise Exception("property_contact must be a list of objects")

            for contact in property_contacts:
                print("hello, contact")
                contact_id = contact.get('entityPropertyContactID')
                
                if contact_id:
                    existing_contact = db_session.query(EntityPropertyContact).filter_by(entityPropertyContactID=contact_id).first()
                    if not existing_contact:
                        raise Exception(f"EntityPropertyContact with ID {contact_id} not found")
                    for key, value in contact.items():
                        if hasattr(existing_contact, key):
                            setattr(existing_contact, key, value)
                else:
                    new_contact_data = {key: value for key, value in contact.items() if hasattr(EntityPropertyContact, key)}
                    new_contact_data['entityPropertyID'] = entity_property.entityPropertyID  # Assign parent ID
                    new_contact = EntityPropertyContact(**new_contact_data)
                    db_session.add(new_contact)

            # Handle appointments array
            appointments = property.get('appointments', [])
            print(appointments, "appointments")
            if not isinstance(appointments, list):
                raise Exception("appointments must be a list of objects")

            for appointment in appointments:
                appointment_id = appointment.get('entityAppointmentsID')

                if appointment_id:
                    # Update existing appointment
                    existing_appointment = db_session.query(EntityAppointments).filter_by(entityAppointmentsID=appointment_id).first()
                    if not existing_appointment:
                        raise Exception(f"EntityAppointments with ID {appointment_id} not found")
                    for key, value in appointment.items():
                        if hasattr(existing_appointment, key) and key != 'products':
                            setattr(existing_appointment, key, value)

                    # Handle products for existing appointment
                    product_data = appointment.get('products', [])
                    handle_products(db_session, existing_appointment, product_data)

                else:
                    # Create new appointment
                    new_appointment_data = {key: value for key, value in appointment.items() 
                                            if hasattr(EntityAppointments, key) and key != 'products'}
                    new_appointment_data['entityPropertyID'] = entity_property.entityPropertyID 
                    new_appointment = EntityAppointments(**new_appointment_data)
                    db_session.add(new_appointment)
                    db_session.flush()  # Flush to assign entityAppointmentsID

                    # Handle products for the new appointment
                    product_data = appointment.get('products', [])
                    handle_products(db_session, new_appointment, product_data)
        
        db_session.commit()
        print("Properties, contacts & appointments updated/created successfully")
    except Exception as e:
        db_session.rollback()
        raise Exception("Error while updating properties data: " + str(e))

def handle_products(db_session, appointment, product_data):

    if not product_data:
        return

    if not isinstance(product_data, list):
        raise ValueError("Phones data must be a list of phone records.")

    if appointment.entityAppointmentsID:
        db_session.query(EntityAppointmentSelectedProduct).filter_by(entityAppointmentsID=appointment.entityAppointmentsID).delete()

    for product in product_data:
        if not all(k in product for k in ('entityAppointmentSelectedProductQuanity', 'constantsProductID')):
            raise ValueError("Each product record must include 'entityAppointmentSelectedProductQuanity' and 'constantsProductID'.")

        new_product = EntityAppointmentSelectedProduct(
            entityAppointmentsID=appointment.entityAppointmentsID,  
            entityAppointmentSelectedProductQuanity=product['entityAppointmentSelectedProductQuanity'],
            constantsProductID=product.get('constantsProductID'),  
        )
        db_session.add(new_product)

    db_session.commit()

def handle_entity_call_update(db_session, entity, calls):
    try:
        if not calls:
            return
        
        if not isinstance(calls, list):
            raise Exception("calls must be provided as a list of objects")
        
        for call in calls:
            entity_call_id = call.get('entityCallID')
            
            # Check if the EntityCall exists or create a new one
            if entity_call_id:
                entity_call = db_session.query(EntityCall).filter_by(entityCallID=entity_call_id).first()
                if not entity_call:
                    raise Exception(f"EntityCall with ID {entity_call_id} not found")
                
                for key, value in call.items():
                    if hasattr(entity_call, key) and key != 'call_backs':
                        setattr(entity_call, key, value)
            else:
                entity_call = EntityCall(
                    entityID=entity.entityID,  
                    **{key: value for key, value in call.items() if hasattr(EntityCall, key) and key != 'call_backs'}
                )
                db_session.add(entity_call)
                db_session.flush()

            call_backs = call.get('call_backs', [])
            if not call_backs:
                continue
            
            if not isinstance(call_backs, list):
                raise Exception("call_backs must be a list of objects")

            for call_back in call_backs:
                entity_callback_id = call_back.get('entityCallbackID')
                
                if entity_callback_id:
                    # Update existing callback
                    entity_callback = db_session.query(EntityCallback).filter_by(entityCallbackID=entity_callback_id).first()
                    if not entity_callback:
                        raise Exception(f"EntityCallback with ID {entity_callback_id} not found")
                    for key, value in call_back.items():
                        if hasattr(entity_callback, key):
                            setattr(entity_callback, key, value)
                else:
                    # Create new callback
                    new_callback_data = {
                        key: value for key, value in call_back.items() if hasattr(EntityCallback, key)
                    }
                    new_callback_data['entityCallID'] = entity_call.entityCallID  # Use the generated ID
                    new_callback = EntityCallback(**new_callback_data)
                    db_session.add(new_callback)
        
        db_session.commit()
        print("calls and callbacks updated successfully")
    except Exception as e:
        db_session.rollback()  # Rollback on error
        raise Exception("Error while updating calls and callbacks data", str(e))

