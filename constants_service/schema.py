from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db_models import ConstantsProductType,ConstantsMarketType, ConstantsEmployeeType, ConstantsEmployeePayType, ConstantsEntityCallType, ConstantsEntityCallResult, ConstantsEntityPropertyStructure, ConstantsEntitySubSource, ConstantsEntitySource, ConstantsPropertyLookUp, ConstantsPhoneType, ConstantsEmployeeType, ConstantsEmployeePayType, ConstantsEntityEmploymentStatus, ConstantsEntityMaritalStatus , ConstantsSalesJobDispositon, ConstantsAppointmentDisposition, ConstantsRelationType, ConstantsUSAStates, ConstantsVoucherType, ConstantsDeliveryWarehouse, ConstantsMaterialsVendor





class ConstantsEmployeeTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEmployeeType
        fields = ("constantsEmployeeTypeID", "constantsEmployeeTypeName")
        load_instance = True


class ConstantsEmployeePayTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEmployeePayType
        fields = ("constantsEmployeePayTypeID", "constantsEmployeePayTypeName")
        load_instance = True

class ConstantsEntityEmploymentStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEntityEmploymentStatus
        fields = ("constantsEntityEmploymentStatusID", "constantsEntityEmploymentStatusName")
        load_instance = True

class ConstantsEntityMaritalStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEntityMaritalStatus
        fields = ("constantsEntityMaritalStatusID", "constantsEntityMaritalStatusName")
        load_instance = True



class ConstantsEntityCallTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEntityCallType
        fields = ("constantsEntityCallTypeID", "constantsEntityCallTypeName")
        load_instance = True


class ConstantsEntityCallResultSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEntityCallResult
        fields = ("constantsEntityCallResultID", "constantsEntityCallResultName")
        load_instance = True


class ConstantsEntityPropertyStructureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEntityPropertyStructure       
        fields = ("constantsEntityPropertyStructureID", "constantsEntityPropertyStructureName")
        load_instance = True


class ConstantsEntitySubSourceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEntitySubSource
        fields = ("constantsEntitySubSourceID", "constantsEntitySubSourceName", "constantsEntitySourceID")
        load_instance = True
        include_fk = True


class ConstantsEntitySourceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsEntitySource
        fields = ("constantsEntitySourceID", "constantsEntitySourceName")
        load_instance = True
        

class ConstantsPropertyLookUpSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsPropertyLookUp
        fields = ("constantsPropertyLookUpID", "constantsPropertyLookUpName", "constantsPropertyLookUpLink")
        load_instance = True


class ConstantsPhoneTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsPhoneType
        fields = ("constantsPhoneTypeID", "constantsPhoneTypeName")
        load_instance = True


class ConstantsProductTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConstantsProductType
        fields = ("constantsProductID", "constantsProductName")
        include_relationships = True
        load_instance = True

class ConstantsMarketTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConstantsMarketType
        fields = ("constantsMarketID", "constantsMarketName")
        include_relationships = True
        load_instance = True

class ConstantsSalesJobDispositonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsSalesJobDispositon
        fields = ("constantsSalesJobDispositonID", "constantsSalesJobDispositionName")
        load_instance = True

class ConstantsAppointmentDispositionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsAppointmentDisposition
        fields = ("constantsAppointmentDispositionID", "constantsAppointmentDisposition")
        load_instance = True

        
class ConstantsUSAStatesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsUSAStates
        fields = ("constantsUSAStatesID", "constantsUSAStatesName")
        load_instance = True


class ConstantsRelationTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsRelationType
        fields = ("constantsRelationTypeID", "constantsRelationTypeName")
        load_instance = True

class ConstantsVoucherTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsVoucherType
        fields = ("constantsVoucherTypeID", "constantsVoucherType")
        load_instance = True


class ConstantsDeliveryWarehouseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsDeliveryWarehouse
        fields = ("constantsDeliveryWarehouseID", "constantsDeliveryWarehouseName")
        load_instance = True

class ConstantsMaterialsVendorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model =  ConstantsMaterialsVendor
        fields = ("constantsMaterialsVendorID", "constantsMaterialsVendorName", "constantsMaterialsVendorActive")
        load_instance = True

