from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from db_models import SalesJob, Entity, EntityProperty, ConstantsVoucherType, EmployeeMaster, SubContractorInstaller, SalesJobAddendum, EntityPhone

class EntitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entity
        fields = (
            "entityID",
            "entityFirstName",
            "entityLastName",
            "entityEmail",
            "entityPhone",
            "entityAddress",
            "entityCity",
            "entityState",
            "entityZipCode",
            "entityPhoneType",
            "entityrDoNotText",
            "entityDoNotEmail",
            "entityDoNotCall",
            "entityPermanentAddressLine1",
            "entityPermanentAddressLine2",
            "entityPermanentCity",
            "entityPermanentState",
            "entityPermanentZipcode",
            "entityInitialDataReceivedSource",
            "entityInitialDataReceivedSubSource"
        )
        include_fk = True
        load_instance = True

class EntityPropertySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityProperty
        fields = (
         "entityPropertyID",
            "entityID",
            "entityPropertyAddressLine1",
            "entityPropertyAddressLine2",
            "entityPropertyCity",
            "entityPropertyState",
            "entityPropertyZipCode",
            "entityPropertyDirections",
            "constantsMarketID",
            "entityPropertyStructure",
            "entityPropertyNotes"
        )
        include_fk = True
        load_instance = True

class SalesJobSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesJob
        fields = (
            "salesJobID",
            "salesJobNumber",
            "salesJobEntityAppointmentNumber",
            "salesJobEntityCustomerRecordNumber",
            "entityPropertyID",
            "salesJobContractDate",
            "salesJobSalesRepID",
            "salesJobContractAmount",
            "salesJobFinancedAmount",
            "salesJobIsPermitRequired",
            "salesJobDiscountPercentage",
            "salesJobAdjustedContractValue",
            "salesJobVoucherTypeID",
            "salesJobVoucherSentDate",
            "salesJobIsHOAAppRequired",
            "salesJobIsQualityControlled",
            "salesJobSubContractorID",
            "salesJobSubContractorInstaller1ID",
            "salesJobSubContractorInstaller2ID",
            "salesJobProjectManager1ID",
            "salesJobProjectManager2ID",
            "salesJobPreviewedByID",
            "created_at"
        )
        include_fk = True
        load_instance = True

class ConstantsVoucherTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConstantsVoucherType
        fields = (
            "constantsVoucherTypeID",
            "constantsVoucherType",
            "created_at"
        )
        include_fk = True
        load_instance = True

class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeMaster
        fields = (
            "employeeID",
            "employeeFirstName",
            "employeeLastName",
            "employeeEmail",
            "employeePhone",
            "employeeRole",
            "employeeStatus",
            "created_at"
        )
        include_fk = True
        load_instance = True

class SubContractorInstallerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SubContractorInstaller
        fields = (
            "subContractorInstallerID",
            "subContractorID",
            "subContractorInstallerFirstName",
            "subContractorInstallerLastName",
            "subContractorInstallerPhone",
            "subContractorInstallerEmail",
            "created_at"
        )
        include_fk = True
        load_instance = True

class SalesJobAddendumSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesJobAddendum
        fields = (
            "salesJobAddendumID",
            "salesJobID",
            "salesJobAddendumDate",
            "salesJobAddendumInvestmentAmount",
            "salesJobAddendumOriginalContractValue",
            "salesJobAddendumPositiveCommissionAmount",
            "salesJobAddendumNegativeCommissionAmount",
            "salesJobAddendumNewAdjustedContractValue",
            "salesJobAddendumSpecialInstructions",
            "salesJobAddendumIsApproved",
            "salesJobAddendumIsRejected",
            "salesJobAddendumSoldByID",
            "salesJobAddendumS3URL"
        )
        include_fk = True
        load_instance = True

class PayrollAddendumSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesJobAddendum
        fields = (
            "salesJobAddendumID",
            "salesJobID",
            "salesJobAddendumDate",
            "salesJobAddendumInvestmentAmount",
            "salesJobAddendumOriginalContractValue",
            "salesJobAddendumPositiveCommissionAmount",
            "salesJobAddendumNegativeCommissionAmount",
            "salesJobAddendumNewAdjustedContractValue",
            "salesJobAddendumSpecialInstructions",
            "salesJobAddendumIsApproved",
            "salesJobAddendumIsRejected",
            "salesJobAddendumSoldByID",
            "salesJobAddendumS3URL"
        )
        include_fk = True
        load_instance = True

class EntityPhoneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityPhone
        fields = (
            "entityPhoneID",
            "entityID",
            "entityPhoneNumber",
            "constantsPhoneTypeID",
            "created_at"
        )
        include_fk = True