from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from db_models import Entity, EntityCall, EntitySecondaryContactDetails, EntityPropertyContact, EntityAppointments,EntityProperty, SubContractor, EntityCallback , EntityPhone, ConstantsRelationType,SubContractorInstaller

class EntitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entity
        include_fk = True
        load_instance = True

class EntityCallSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityCall
        include_fk = True
        load_instance = True

class EntitySecondaryContactDetailsSchema(SQLAlchemyAutoSchema):
    relationship = fields.Method("get_relationship")  

    class Meta:
        model = EntitySecondaryContactDetails
        include_fk = True  
        load_instance = True

    def get_relationship(self, obj):
        """
        Dynamically fetch the relationship details.
        """
        db_session = self.context.get('db_session')
        if obj.entitySecondaryContactRelationshipTypeID and db_session:
            relation = db_session.query(
                ConstantsRelationType.constantsRelationTypeID,
                ConstantsRelationType.constantsRelationTypeName
            ).filter(
                ConstantsRelationType.constantsRelationTypeID == obj.entitySecondaryContactRelationshipTypeID
            ).first()
            if relation:
                return {
                    "entitySecondaryContactRelationshipTypeID": relation[0],
                    "constantsRelationTypeName": relation[1]
                }
        return None


class EntityPropertyContactSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityPropertyContact
        include_fk = True
        load_instance = True


class EntityAppointmentsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityAppointments
        include_fk = True
        load_instance = True

class EntityPropertySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityProperty
        include_fk = True
        load_instance = True
   
class SubContractorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SubContractor
        include_fk = True
        load_instance = True
  


class EntityCallbackSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  EntityCallback
        include_fk = True
        load_instance = True

class EntityPhoneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  EntityPhone
        include_fk = True
        load_instance = True

class SecondaryContactDetailsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntitySecondaryContactDetails
        include_fk = True  # Include foreign keys if needed
        load_instance = True

        
class SubContractorInstallerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SubContractorInstaller
        include_fk = True  # Include foreign keys if needed
        load_instance = True

class EntityPhoneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  EntityPhone
        include_fk = True
        load_instance = True

