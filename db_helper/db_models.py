from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship



Base = declarative_base()

def create_db_schema(engine):
    Base.metadata.create_all(engine)

status_enum = ENUM('active', 'inactive', 'deleted', name='statusenum', create_type=True)
appointment_status_enum = ENUM('Completed', 'On Hold', 'In Progress', name='appointmentenum', create_type=True)

class ConstantsDeliveryWarehouse(Base):
    __tablename__ = 'ConstantsDeliveryWarehouse'
    constantsDeliveryWarehouseID = Column(Integer, primary_key=True, autoincrement=True)
    constantsDeliveryWarehouseName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsDeliveryWarehouse(constantsDeliveryWarehouseID={self.constantsDeliveryWarehouseID})>"
    

class ConstantsVoucherType(Base):
    __tablename__ = 'ConstantsVoucherType'
    constantsVoucherTypeID = Column(Integer, primary_key=True, autoincrement=True)
    constantsVoucherType = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsVoucherType(constantsVoucherTypeID={self.constantsVoucherTypeID})>"

class ConstantsUSAStates(Base):
    __tablename__ = 'ConstantsUSAStates'
    constantsUSAStatesID = Column(Integer, primary_key=True, autoincrement=True)
    constantsUSAStatesName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsUSAStates(constantsUSAStatesID={self.constantsUSAStatesID})>"

class ConstantsRelationType(Base):
    __tablename__ = 'ConstantsRelationType'
    constantsRelationTypeID = Column(Integer, primary_key=True, autoincrement=True)
    constantsRelationTypeName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsRelationType(constantsRelationTypeID={self.constantsRelationTypeID})>"

class ConstantsEmployeeType(Base):
    __tablename__ = 'ConstantsEmployeeType'
    constantsEmployeeTypeID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEmployeeTypeName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsEmployeeType(constantsEmployeeTypeID={self.constantsEmployeeTypeID})>"

class ConstantsEmployeePayType(Base):
    __tablename__ = 'ConstantsEmployeePayType'
    constantsEmployeePayTypeID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEmployeePayTypeName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEmployeePayType(constantsEmployeePayTypeID={self.constantsEmployeePayTypeID})>"
    

class ConstantsEntityCallType(Base):
    __tablename__ = 'ConstantsEntityCallType'
    constantsEntityCallTypeID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEntityCallTypeName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEntityCallType(constantsEntityCallTypeID={self.constantsEntityCallTypeID})>"
    
class ConstantsEntityCallResult(Base):
    __tablename__ = 'ConstantsEntityCallResult'
    constantsEntityCallResultID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEntityCallResultName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEntityCallResult(constantsEntityCallResultID={self.constantsEntityCallResultID})>"
    
class ConstantsEntityPropertyStructure(Base):
    __tablename__ = 'ConstantsEntityPropertyStructure'
    constantsEntityPropertyStructureID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEntityPropertyStructureName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEntityPropertyStructure(constantsEntityPropertyStructureID={self.constantsEntityPropertyStructureID})>"
    
class ConstantsEntitySource(Base):
    __tablename__ = 'ConstantsEntitySource'
    constantsEntitySourceID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEntitySourceName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEntitySource(constantsEntitySourceID={self.constantsEntitySourceID})>"
    
class ConstantsEntitySubSource(Base):
    __tablename__ = 'ConstantsEntitySubSource'
    constantsEntitySubSourceID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEntitySubSourceName = Column(String(255), nullable=False)
    constantsEntitySourceID = Column(Integer, ForeignKey('ConstantsEntitySource.constantsEntitySourceID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEntitySubSource(constantsEntitySubSourceID={self.constantsEntitySubSourceID})>"
    
class ConstantsPropertyLookUp(Base):
    __tablename__ = 'ConstantsPropertyLookUp'
    constantsPropertyLookUpID = Column(Integer, primary_key=True, autoincrement=True)
    constantsPropertyLookUpName = Column(String(255), nullable=False)
    constantsPropertyLookUpLink = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsPropertyLookUp(constantsPropertyLookUpID={self.constantsPropertyLookUpID})>"
    
class ConstantsPhoneType(Base):
    __tablename__ = 'ConstantsPhoneType'
    constantsPhoneTypeID = Column(Integer, primary_key=True, autoincrement=True)
    constantsPhoneTypeName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsPhoneType(constantsPhoneTypeID={self.constantsPhoneTypeID})>"
    
class ConstantsEntityEmploymentStatus(Base):
    __tablename__ = 'ConstantsEntityEmploymentStatus'
    constantsEntityEmploymentStatusID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEntityEmploymentStatusName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEntityEmploymentStatus(constantsEntityEmploymentStatusID={self.constantsEntityEmploymentStatusID})>"
    
class ConstantsEntityMaritalStatus(Base):
    __tablename__ = 'ConstantsEntityMaritalStatus'
    constantsEntityMaritalStatusID = Column(Integer, primary_key=True, autoincrement=True)
    constantsEntityMaritalStatusName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<ConstantsEntityMaritalStatus(constantsEntityMaritalStatusID={self.constantsEntityMaritalStatusID})>"
    

class EmployeeMaster(Base):
    __tablename__ = 'EmployeeMaster'
    employeeID = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=True)
    employeeBadgeID = Column(Integer, nullable=False)
    employeeFirstName = Column(String(255), nullable=False)
    employeeLastName = Column(String(255), nullable=False)
    employeeHireDate = Column(DateTime, nullable=False)
    employeeTerminationDate = Column(DateTime, nullable=False)
    employeeIsActive = Column(Boolean, nullable=False)
    employeeUserName = Column(String(255), nullable=False)
    employeePassword = Column(String(255), nullable=False)
    employeeEmail = Column(String(255), nullable=True)
    employeeTypeID = Column(Integer, ForeignKey('ConstantsEmployeeType.constantsEmployeeTypeID'), nullable=True)
    employeePayTypeID = Column(Integer, ForeignKey('ConstantsEmployeePayType.constantsEmployeePayTypeID'), nullable=True)
    employeeTitle = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmployeeMaster(employeeID={self.employeeID})>"
    

    
class ConstantsProductType(Base):
    __tablename__ = 'ConstantsProductType'
    constantsProductID = Column(Integer, primary_key=True, autoincrement=True)
    constantsProductName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsProductType(constantsProductID={self.constantsProductID})>"
    
class ConstantsMarketType(Base):
    __tablename__ = 'ConstantsMarketType'
    constantsMarketID = Column(Integer, primary_key=True, autoincrement=True)
    constantsMarketName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsMarketType(constantsMarketID={self.constantsMarketID})>"
    

class ConstantsSalesJobDispositon(Base):
    __tablename__ = 'ConstantsSalesJobDispositon'
    constantsSalesJobDispositonID = Column(Integer, primary_key=True, autoincrement=True)
    constantsSalesJobDispositionName = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsSalesJobDispositon(constantsSalesJobDispositonID={self.constantsSalesJobDispositonID})>"
    

class ConstantsAppointmentDisposition(Base):
    __tablename__ = 'ConstantsAppointmentDisposition'
    constantsAppointmentDispositionID = Column(Integer, primary_key=True, autoincrement=True)
    constantsAppointmentDisposition = Column(String(255), nullable=False)
    constantsAppointmentDispositionDescription = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsAppointmentDisposition(constantsAppointmentDispositionID={self.constantsAppointmentDispositionID})>"

    
class Entity(Base):
    __tablename__ = 'Entity'
    entityID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityInboundRecordNumber = Column(String(255), nullable=True)
    entityInboundRecordStatus = Column(String(255), nullable=True)
    entityCustomerRecordNumber = Column(String(255), nullable=True)
    entityIsInboundDuplicateRecord = Column(Boolean, nullable=True)
    entityIsInboundRecordMerged = Column(Boolean, nullable=True)
    entityIsInboundRecordDeleted = Column(Boolean, nullable=True)
    entityPrefix = Column(String(255), nullable=True) 
    entityFirstName = Column(String(255), nullable=False)
    entityLastName = Column(String(255), nullable=False)
    entityPermanentAddressLine1 = Column(String(255), nullable=True)
    entityPermanentAddressLine2 = Column(String(255), nullable=True) 
    entityPermanentCity = Column(String(255), nullable=True)
    entityPermanentState = Column(String(255), nullable=True)
    entityPermanentZipcode = Column(String(255), nullable=True)
    entityrIsTextPreferred = Column(Boolean, nullable=False, default=False)
    entityIsEmailPreferred = Column(Boolean, nullable=False, default=False)
    entityIsCallPreferred = Column(Boolean, nullable=False, default=False)
    entityDNCWaiver = Column(Boolean, nullable=False)
    entityEmail = Column(String(255), nullable=False)
    entityInitialDataReceivedDate = Column(DateTime, nullable=True)
    entityInitialDataReceivedSource = Column(String(255), nullable=False)
    entityInitialDataReceivedSubSource = Column(String(255), nullable=False)
    entityInitialDataReceivedProduct = Column(String(255), nullable=True)
    entityInitialDataReceivedNotes = Column(String(500), nullable=True) 
    entityInitialDataReceivedCheckoutDate = Column(DateTime, nullable=True) 
    entityInitialDataReceivedCheckedOutByID = Column(String(255), nullable=True) 
    entityInboundRecordIsLocked = Column(Boolean, nullable=True, default=True)
    entityInboundRecordLockedByID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True) 
    entityNotes = Column(String(255), nullable=True)  
    constantsMarketID = Column(Integer, ForeignKey('ConstantsMarketType.constantsMarketID'), nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Entity(entityID={self.entityID})>"
    
class EntityDispute(Base):
    __tablename__ = 'EntityDispute'
    entityDisputeID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityDisputeFirstName = Column(String((255)), nullable=False)
    entityDisputeLastName = Column(String((255)), nullable=False)
    parentEntityID = Column(UUID(as_uuid=True), ForeignKey('Entity.entityID'), nullable=True)
    parentEntityInboundRecordNumber = Column(Integer, nullable=False)
    entityDisputeOriginalSource = Column(String((255)), nullable=False)
    entityDisputeOriginalSubSource = Column(String((255)), nullable=False)
    entityDisputeSource = Column(String((255)), nullable=False)
    entityDisputeSubSource = Column(String((255)), nullable=False)
    entityDisputeProduct = Column(String((255)), nullable=False)
    entityDisputeInitialDataReceivedDate = Column(DateTime, nullable=False)
    entityDisputeIsProcessed= Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def ___repr___(self):
        return f"<EntityDispute(entityDisputeID={self.entityDisputeID})>"
    
class EntityPhone(Base):
    __tablename__ = 'EntityPhone'
    entityPhoneID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityID = Column(UUID(as_uuid=True), ForeignKey('Entity.entityID'), nullable=False)
    entityPhoneNumber = Column(String(255), nullable=False)
    constantsPhoneTypeID = Column(Integer, ForeignKey('ConstantsPhoneType.constantsPhoneTypeID'), nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityPhone(entityPhoneID={self.entityPhoneID})>"

class EntityProperty(Base):
    __tablename__ = 'EntityProperty'
    entityPropertyID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityID = Column(UUID(as_uuid=True), ForeignKey('Entity.entityID'), nullable=True) 
    entityPropertyAddressLine1 = Column(String(255), nullable=False)
    entityPropertyAddressLine2 = Column(String(255), nullable=True) 
    entityPropertyCity = Column(String(255), nullable=False)
    entityPropertyState = Column(String(255), nullable=False)
    entityPropertyZip = Column(String(255), nullable=False)
    entityPropertyDirections = Column(String(255), nullable=True) 
    constantsMarketID = Column(Integer, ForeignKey('ConstantsMarketType.constantsMarketID'), nullable=True) 
    entityPropertyStructure = Column(String(255), nullable=False)
    entityPropertyNotes = Column(String(255), nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityProperty(entityPropertyID={self.entityPropertyID})>"
    
class EntityCall(Base):
    __tablename__ = 'EntityCall'
    entityCallID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityID = Column(UUID(as_uuid=True), ForeignKey('Entity.entityID'), nullable=True) 
    entityCallCallResult = Column(String(255), nullable=False)
    entityCallPhone = Column(String(255), nullable=False)
    entityCallDate = Column(DateTime, nullable=False)
    entityCallCode = Column(String(255), nullable=False)
    entityCallCallerID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    entityCallCallType = Column(String(255), nullable=False)
    entityCallNotes = Column(String(255), nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityCall(entityCallID={self.entityCallID})>"
    
class EntityCallback(Base):
    __tablename__ = 'EntityCallback'
    entityCallbackID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityCallID = Column(UUID(as_uuid=True), ForeignKey('EntityCall.entityCallID'), nullable=True)
    entityCallbackDate = Column(DateTime, nullable=False)
    entityCallbackTime = Column(DateTime, nullable=False)
    entityCallbackAssignedTo = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    entityCallbackPhone = Column(String(255), nullable=False)
    entityCallbackIsComplete = Column(Boolean, nullable=False)
    entityCallbackNotes = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityCallback(entityCallbackID={self.entityCallbackID})>"


class EntityPropertyContact(Base):
    __tablename__ = 'EntityPropertyContact'
    entityPropertyContactID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityPropertyID = Column(UUID(as_uuid=True), ForeignKey('EntityProperty.entityPropertyID'), nullable=True)
    entityPropertyContactPrefix = Column(String(255), nullable=True)
    entityPropertyContactFirstName = Column(String(255), nullable=False)
    entityPropertyContactLastName = Column(String(255), nullable=False)
    entityPropertyContactRelationTypeID = Column(Integer, ForeignKey('ConstantsRelationType.constantsRelationTypeID'), nullable=True)
    entityPropertyContactPhone = Column(String(255), nullable=False)
    entityPropertyContactPhoneType = Column(String(255), nullable=False)
    entityPropertyContactEmail = Column(String(255), nullable=False)
    entityrIsTextPreferred = Column(Boolean, nullable=False,default=False)
    entityIsEmailPreferred = Column(Boolean, nullable=False, default=False)
    entityIsCallPreferred = Column(Boolean, nullable=False, default=False)
    entityDNCWaiver = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityPropertyContact(entityPropertyContactID={self.entityPropertyContactID})>"

class EntitySecondaryContactDetails(Base):
    __tablename__ = 'EntitySecondaryContactDetails'
    customerSecondaryContactDetailsID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityID = Column(UUID(as_uuid=True), ForeignKey('Entity.entityID'), nullable=True)
    entitySecondaryContactFirstName = Column(String(255), nullable=False)
    entitySecondaryContactLastName = Column(String(255), nullable=False)
    entitySecondaryContactRelationshipTypeID = Column(Integer, ForeignKey('ConstantsRelationType.constantsRelationTypeID'), nullable=True)
    entitySecondaryContactDetailsPhone = Column(String(255), nullable=False)
    entitySecondaryContactDetailsPhoneType = Column(String(255), nullable=False)
    entitySecondaryContactDetailsEmail = Column(String(255), nullable=False)
    entityrIsTextPreferred = Column(Boolean, nullable=False, default=False)
    entityIsEmailPreferred = Column(Boolean, nullable=False,default=False)
    entityIsCallPreferred = Column(Boolean, nullable=False,default=False)
    entityDNCWaiver = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntitySecondaryContactDetails(customerSecondaryContactDetailsID={self.customerSecondaryContactDetailsID})>"



class EntityAppointments(Base):
    __tablename__ = 'EntityAppointments'
    entityAppointmentsID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityAppointmentNumber = Column(Integer, nullable=True)
    entityPropertyID = Column(UUID(as_uuid=True), ForeignKey('EntityProperty.entityPropertyID'), nullable=True)
    constantsAppointmentDispositionID = Column(Integer, ForeignKey('ConstantsAppointmentDisposition.constantsAppointmentDispositionID'), nullable=True)
    entityAppointmentsIssued = Column(Boolean, nullable=True)
    entityAppointmentsLeadEntryDate = Column(DateTime, nullable=False)
    entityAppointmentsLeadTime = Column(DateTime, nullable=False)
    entityAppointmentsSalesRep1 = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    entityAppointmentsSalesRep2 = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    entityAppointmentsMarketID = Column(Integer, ForeignKey('ConstantsMarketType.constantsMarketID'), nullable=True)
    entityAppointmentsHDBadgeID = Column(String(255),nullable=True) 
    entityAppointmentsBCICallID = Column(String(255),nullable=True)
    entityAppointmentsAppointmentDate = Column(DateTime, nullable=False)
    entityAppointmentsAppointmentTime = Column(Time, nullable=False)
    entityAppointmentsLeadSetterID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    entityAppointmentsSOW = Column(String((255)), nullable=True) 
    entityAppointmentsGoodWith90Minutes = Column(Boolean, nullable=False)
    entityAppointmentsIsHOA = Column(Boolean, nullable=False)
    entityAppointmentsIsGoodWithPermits = Column(Boolean, nullable=False)
    entityAppointmentsIsRentalProperty = Column(Boolean, nullable=True)
    entityAppointmentsIsDecisionMakers = Column(Boolean, nullable=True)
    entityAppointmentsNotes = Column(String((255)), nullable=True) 
    entityAppointmentsSalesRep1IsAccepted = Column(Boolean, nullable=True) 
    entityAppointmentsSalesRep2IsAccepted  = Column(Boolean, nullable=True) 
    entityAppointmentsSalesRep1ResponseDate = Column(DateTime, nullable=True) 
    entityAppointmentsSalesRep2ResponseDate = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityAppointments(entityAppointmentsID={self.entityAppointmentsID})>"
    
class EntityAppointmentSelectedProduct(Base):
    __tablename__ = 'EntityAppointmentSelectedProduct'
    entityAppointmentSelectedProductID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityAppointmentsID = Column(UUID(as_uuid=True), ForeignKey('EntityAppointments.entityAppointmentsID'), nullable=True)
    constantsProductID = Column(Integer, ForeignKey('ConstantsProductType.constantsProductID'), nullable=True)
    entityAppointmentSelectedProductQuanity =  Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityAppointmentSelectedProduct(entityAppointmentSelectedProductID={self.entityAppointmentSelectedProductID})>"
    

    
class EntityCallCenterNotes(Base):
    __tablename__ = 'EntityCallCenterNotes'
    entityCallCenterNotesID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entityID = Column(UUID(as_uuid=True), ForeignKey('Entity.entityID'), nullable=True)
    entityCallCenterNotesNotes = Column(String((255)), nullable=False)
    entityCallCenterNotesDate = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EntityCallCenterNotes(entityCallCenterNotesID={self.entityCallCenterNotesID})>"
    
class SubContractor(Base):
    __tablename__ = 'SubContractor'
    subContractorID = Column(Integer, primary_key=True, autoincrement=True)
    subContractorCompanyName = Column(String(255), nullable=False)
    subContractorCompanyAddressLine1 = Column(String(255), nullable=False)
    subContractorCompanyAddressLine2 = Column(String(255), nullable=False)
    subContractorCompanyCity = Column(String(255), nullable=False)
    subContractorCompanyState = Column(String(255), nullable=False)
    subContractorCompanyZipCode = Column(String(255), nullable=False)
    subContractorCompanyPhone = Column(String(255), nullable=False)
    subContractorCompanyEmail = Column(String(255), nullable=False)
    subContractorCompanyLicenseNumber = Column(String(255), nullable=False)
    subContractorOwnerFirsttName = Column(String(255), nullable=False)
    subContractorOwnerLastName = Column(String(255), nullable=False)
    subContractorCompanyOwnerPhone = Column(String(255), nullable=False)
    subContractorCompanyOwnerEmail = Column(String(255), nullable=False)
    subContractorMarketID = Column(Integer, ForeignKey('ConstantsMarketType.constantsMarketID'), nullable=True)
    status = Column(status_enum, default='active', nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SubContractor(subContractorID={self.subContractorID})>"
    
class SubContractorInstaller(Base):
    __tablename__ = 'SubContractorInstaller'
    subContractorInstallerID = Column(Integer, primary_key=True, autoincrement=True)
    subContractorID = Column(Integer, ForeignKey('SubContractor.subContractorID'), nullable=True)
    subContractorInstallerFirstName = Column(String(255), nullable=False)
    subContractorInstallerLastName = Column(String(255), nullable=False)
    subContractorInstallerPhone = Column(String(255), nullable=False)
    subContractorInstallerEmail = Column(String(255), nullable=False)
    status = Column(status_enum, default='active', nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SubContractorInstaller(subContractorInstallerID={self.subContractorInstallerID})>"
    
class SalesJob(Base):
    __tablename__ = 'SalesJob'
    salesJobID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobNumber = Column(Integer, nullable=False)
    salesJobStatusDispositionID = Column(Integer, ForeignKey('ConstantsSalesJobDispositon.constantsSalesJobDispositonID'), nullable=True)
    salesJobEntityAppointmentNumber = Column(Integer, nullable=False)
    salesJobEntityCustomerRecordNumber = Column(Integer, nullable=False)
    entityPropertyID = Column(UUID(as_uuid=True), ForeignKey('EntityProperty.entityPropertyID'), nullable=True)
    salesJobContractDate = Column(DateTime, nullable=False)
    salesJobSalesRepID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobContractAmount = Column(String(255), nullable=False)
    salesJobFinancedAmount = Column(String(255), nullable=False)
    salesJobIsPermitRequired = Column(Boolean, nullable=False, default=False)
    salesJobDiscountPercentage = Column(String(255), nullable=True)
    salesJobAdjustedContractValue = Column(String(255), nullable=True)
    salesJobVoucherTypeID = Column(Integer, ForeignKey('ConstantsVoucherType.constantsVoucherTypeID'), nullable=True)
    salesJobVoucherSentDate = Column(DateTime, nullable=True)
    salesJobIsHOAAppRequired = Column(Boolean, nullable=False, default=False)
    salesJobIsQualityControlled = Column(Boolean, nullable=False, default=False)
    salesJobSubContractorID = Column(Integer, ForeignKey('SubContractor.subContractorID'), nullable=True)
    salesJobSubContractorInstaller1ID = Column(Integer, ForeignKey('SubContractorInstaller.subContractorInstallerID'), nullable=True)
    salesJobSubContractorInstaller2ID = Column(Integer, ForeignKey('SubContractorInstaller.subContractorInstallerID'), nullable=True)
    salesJobProjectManager1ID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobProjectManager2ID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobPreviewedByID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
       return f"<SalesJob(salesJobID={self.salesJobID})>"
    


class CommissionReport(Base):
    __tablename__ = 'CommissionReport'
    commissionReportID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    commissionReportDate = Column(DateTime, nullable=False)
    commissionReportSoldByID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    commissionReportRevisedContractPrice = Column(String(255), nullable=False)
    commissionReportTotalCommissionOnNonCommercialItemsPercent = Column(String(255), nullable=False)
    commissionReportTotalCommissionPrice = Column(String(255), nullable=False)
    commissionReportExpectedPrepayCommissionPrice = Column(String(255), nullable=False)
    commissionReportExpectedPrepayCommissionPriceIsProcessed = Column(Boolean, nullable=False, default=False)
    commissionReportExpectedFinalCommissionPrice = Column(String(255), nullable=False)
    commissionReportExpectedFinalCommissionPriceIsProcessed = Column(Boolean, nullable=False, default=False)
    commissionReportNotes = Column(String(255), nullable=True)
    commissionReportNotesToDesignConsultant = Column(String(255), nullable=False)
    commissionReportS3URL = Column(String(255), nullable=True)
    commissionReportIsDeleted = Column(Boolean, nullable=False, default=False)
    commissionReportIsRedFlagged = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CommissionReport(commissionReportID={self.commissionReportID})>"
    
class SalesJobAddendum(Base):
    __tablename__ = 'SalesJobAddendum'
    salesJobAddendumID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    salesJobAddendumDate = Column(DateTime, nullable=False)
    salesJobAddendumSoldByID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobAddendumOriginalContractValue = Column(String(255), nullable=False)
    salesJobAddendumIsIncrease = Column(Boolean, nullable=False, default=True)
    salesJobAddendumInvestmentAmount = Column(String(255), nullable=False)
    salesJobAddendumPositiveCommissionAmount = Column(String(255), nullable=False)
    salesJobAddendumNegativeCommissionAmount = Column(String(255), nullable=False)
    salesJobAddendumNewAdjustedContractValue = Column(String(255), nullable=False)
    salesJobAddendumSpecialInstructions = Column(String(255), nullable=False)
    salesJobAddendumIsApproved = Column(Boolean, nullable=False, default=False)
    salesJobAddendumIsRejected = Column(Boolean, nullable=False, default=False)
    salesJobAddendumS3URL = Column(String(255), nullable=False)

    def __repr__(self):
       return f"<SalesJobAddendum(salesJobAddendumID={self.salesJobAddendumID})>"

class EmployeePayDetail(Base):
    __tablename__ = 'EmployeePayDetail'
    employeePayDetailID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    commissionReportID = Column(UUID(as_uuid=True), ForeignKey('CommissionReport.commissionReportID'), nullable=True)
    employePayDetailEmployeeID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    employeePayDetailPayrollPeriodStartDate = Column(DateTime, nullable=False)
    employeePayDetailPayrollPeriodEndDate = Column(DateTime, nullable=False)
    employeePayDetailCustomerFullName = Column(String(255), nullable=False)
    employeePayDetailCustomerAddress = Column(String(255), nullable=False)
    employeePayDetailCommissionTypePrepay = Column(String(255), nullable=False)
    employeePayDetailCommissionTypeFinal = Column(String(255), nullable=False)
    employeePayDetailCommissionTypeAddendum = Column(String(255), nullable=False)
    salesJobAddendumID = Column(UUID(as_uuid=True), ForeignKey('SalesJobAddendum.salesJobAddendumID'), nullable=True)
    employeePayDetailTotalCommission = Column(String(255), nullable=False)
    payType = Column(String(225), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmployeePayDetail(employeePayDetailID={self.employeePayDetailID})>"

    

    
class SalesJobCost(Base):
    __tablename__ = 'SalesJobCost'
    salesJobCostID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    salesJobCostItemName = Column(String(255), nullable=False)
    salesJobCostInvoiceNumber = Column(String(255), nullable=False)
    salesJobCostInvoiceDate = Column(DateTime, nullable=False)
    salesJobCostAmount = Column(String(255), nullable=False)
    salesJobCostCommissionable = Column(Boolean, nullable=False)
    salesJobCostProcess = Column(Boolean, nullable=False)
    salesJobCostComments = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
       return f"<SalesJobCost(salesJobCostID={self.salesJobCostID})>"
    

class SalesJobPermits(Base):
    __tablename__ = 'SalesJobPermits'
    salesJobPermitsID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True) 
    salesJobPermitsStatus = Column(Boolean, nullable=False)
    salesJobPermitsType =Column(String(255), nullable=False)
    salesJobPermitsAssignedToID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobPermitsPermitNumber = Column(String(255), nullable=False)
    salesJobPermitsPermitDate = Column(DateTime, nullable=False)
    salesJobPermitsExpirationDate = Column(DateTime, nullable=False)
    salesJobPermitsInspectionSetDate1 = Column(DateTime, nullable=False)
    salesJobPermitsInspectionDate1Passed = Column(Boolean, nullable=False)
    salesJobPermitsInspectionSetDate2 = Column(DateTime, nullable=False)
    salesJobPermitsInspectionDate2Passed = Column(Boolean, nullable=False)
    salesJobPermitsInspectionSetDate3 = Column(DateTime, nullable=False)
    salesJobPermitsInspectionDate3Passed = Column(Boolean, nullable=False)
    salesJobPermitsCustomerAmountPaid = Column(String(255), nullable=False)
    salesJobPermitsCost = Column(String(255), nullable=False)
    salesJobPermitsCustomerTransactionNumber = Column(String(255), nullable=False)
    salesJobPermitsCustomerPaymentDate = Column(DateTime, nullable=False)
    salesJobPermitsEnteredByUserID = Column(String(255), nullable=False)
    salesJobPermitsEnteredByDate = Column(DateTime, nullable=False)
    salesJobPermitsUpdatedByDate = Column(DateTime, nullable=False)
    salesJobPermitsUpdatedByUserID = Column(String(255), nullable=False)
    salesJobPermitsNotes = Column(String(255), nullable=False)
    salesJobPermitsS3URL = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobPermits(salesJobPermitsID={self.salesJobPermitsID})>"
    
class SalesJobNotes(Base):
    __tablename__ = 'SalesJobNotes'
    salesJobNotesID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True) 
    salesJobNotesNotes = Column(String(255), nullable=False)
    salesJobNotesEnteredOnDate = Column(DateTime, nullable=False)
    salesJobNotesEnteredOnUserID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobNotesNotifyToID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobNotes(salesJobNotesID={self.salesJobNotesID})>"
    
    
class SalesJobPayment(Base):
    __tablename__ = 'SalesJobPayment'
    salesJobPaymentID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True) 
    salesJobPaymentInvoiceNumber = Column(String(255), nullable=False)
    salesJobPaymentDate = Column(DateTime, nullable=False)
    salesJobPaymentAmount = Column(String(255), nullable=False)
    salesJobPaymentComments = Column(String(255), nullable=False)
    salesJobPaymentEnteredByID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobPaymentEnteredDate = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f"<SalesJobPayment(salesJobPaymentID={self.salesJobPaymentID})>"


class SalesJobServiceTicket(Base):
    __tablename__ = 'SalesJobServiceTicket'
    salesJobServiceTicketID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobServiceTicketNumber = Column(Integer, nullable=False)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    salesJobServiceTicketDescription = Column(String(255), nullable=False)
    salesJobServiceTicketCategory = Column(String(255), nullable=False)
    salesJobServiceTicketStatus = Column(Boolean, nullable=False)
    salesJobServiceTicketStatusNotes = Column(String(255), nullable=False)
    salesJobServiceTicketBillable = Column(Boolean, nullable=False)
    salesJobServiceTicketWarranty = Column(Boolean, nullable=False)
    salesJobServiceTicketAmount = Column(String(255), nullable=False)
    salesJobServiceTicketAmountCustomerPaid = Column(String(255), nullable=False)
    salesJobServiceTicketAmountTransactionNumber = Column(String(255), nullable=False)
    salesJobServiceTicketAmountPaymentDate = Column(DateTime, nullable=False)
    salesJobServiceTicketPaid = Column(Boolean, nullable=False)
    salesJobServiceTicketAssignToID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesJobServiceTicketInstallerID =  Column(Integer, ForeignKey('SubContractor.subContractorID'), nullable=True)
    salesJobServiceTicketEnteredByID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobServiceTicket(salesJobServiceTicketID={self.salesJobServiceTicketID})>"
    
class SalesJobServiceTicketLogs(Base):
    __tablename__ = 'SalesJobServiceTicketLogs'
    salesJobServiceTicketLogsID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobServiceTicketID = Column(UUID(as_uuid=True), ForeignKey('SalesJobServiceTicket.salesJobServiceTicketID'), nullable=True)
    salesJobServiceTicketLogsLogTitle = Column(String(255), nullable=False)
    salesJobServiceTicketLogsLogDetails = Column(String(255), nullable=False)
    employeeID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobServiceTicketLogs(salesJobServiceTicketLogsID={self.salesJobServiceTicketLogsID})>"
    
class SalesJobMilestoneDate(Base):
    __tablename__ = 'SalesJobMilestoneDate'
    salesJobMilestoneDateID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    salesJobMilestoneContractDate = Column(DateTime, nullable=False)
    salesJobMilestoneMeasureEstimatedDate = Column(DateTime, nullable=False)
    salesJobMilestoneMeasureActualDate = Column(DateTime, nullable=False)
    salesJobMilestoneOrderEstimatedDate = Column(DateTime, nullable=False)
    salesJobMilestoneOrderActualDate = Column(DateTime, nullable=False)
    salesJobMilestoneShipEstimatedDate = Column(DateTime, nullable=False)
    salesJobMilestoneShipActualDate = Column(DateTime, nullable=False)
    salesJobMilestoneStartEstimatedDate = Column(DateTime, nullable=False)
    salesJobMilestoneStartActualDate = Column(DateTime, nullable=False)
    salesJobMilestonePartOrderEstimatedDate = Column(DateTime, nullable=False)
    salesJobMilestonePartOrderActualDate = Column(DateTime, nullable=False)
    salesJobMilestoneCompletionEstimatedDate = Column(DateTime, nullable=False)
    salesJobMilestoneCompletionActualDate = Column(DateTime, nullable=False)
    salesJobMilestoneCancellationDate = Column(DateTime, nullable=False)
    salesJobMilestoneHoldDate = Column(DateTime, nullable=False)
    salesJobMilestoneHoldReason = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobMilestoneDate(salesJobMilestoneDateID={self.salesJobMilestoneDateID})>"
    
class SalesJobFinancing(Base):
    __tablename__ = 'SalesJobFinancing'
    salesJobFinancingID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobFinancing(salesJobFinancingID={self.salesJobFinancingID})>"

class SalesJobFinancingCompany(Base):
    __tablename__ = 'SalesJobFinancingCompany'
    salesJobFinancingCompanyID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobFinancingID = Column(UUID(as_uuid=True), ForeignKey('SalesJobFinancing.salesJobFinancingID'), nullable=True)
    salesJobFinancingCompanyName = Column(String(255), nullable=False)
    salesJobFinancingCompanyAmount =Column(String(255), nullable=False)
    salesJobFinancingCompanyCreditLimit =Column(String(255), nullable=False)
    salesJobFinancingCompanyMonths = Column(String(255), nullable=False)
    salesJobFinancingCompanyFinancingPlan = Column(String(255), nullable=False)
    salesJobFinancingCompanyLoanApprovalDate = Column(DateTime, nullable=False)
    salesJobFinancingCompanyLoanExpirationDate = Column(DateTime, nullable=False)
    salesJobFinancingCompanyCreditApproved = Column(Boolean, nullable=False)
    salesJobFinancingCompanyCredit2ndLook = Column(Boolean, nullable=False)
    salesJobFinancingCompanyCreditRate = Column(String(255), nullable=False)
    salesJobFinancingCompanyCreditTerms = Column(String(225), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobFinancingCompany(salesJobFinancingCompanyID={self.salesJobFinancingCompanyID})>"
    
class SalesJobFinancingParty(Base):
    __tablename__ = 'SalesJobFinancingParty'
    salesJobFinancingPartyID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobFinancingID = Column(UUID(as_uuid=True), ForeignKey('SalesJobFinancing.salesJobFinancingID'),nullable=True)
    salesJobFinancingPartyName =  Column(String(255), nullable=False)
    salesJobFinancingPartyPhone =  Column(String(255), nullable=False)
    salesJobFinancingPartyEmployer = Column(String(255), nullable=False)
    salesJobFinancingPartyCreditScore = Column(String(255), nullable=False)
    salesJobFinancingPartyAnnualIncome = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobFinancingParty(salesJobFinancingPartyID={self.salesJobFinancingPartyID})>"

    
class ConstantsMaterialsVendor(Base):
    __tablename__ = 'ConstantsMaterialsVendor'
    constantsMaterialsVendorID = Column(Integer, primary_key=True, autoincrement=True)
    constantsMaterialsVendorName = Column(String(255), nullable=False)
    constantsMaterialsVendorActive = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ConstantsMaterialsVendor(constantsMaterialsVendorID={self.constantsMaterialsVendorID})>"


class SalesJobMaterials(Base):  
    __tablename__ = 'SalesJobMaterials'
    salesJobMaterialsID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    salesJobMaterialsItemsName = Column(String(225), nullable=False)
    salesJobMaterialsItemsQuantity = Column(Integer, nullable=False)
    salesJobMaterialsAllMaterialsIsReceived = Column(Boolean, nullable=False, default=False)
    salesJobMaterialsVendorID = Column(Integer, ForeignKey('ConstantsMaterialsVendor.constantsMaterialsVendorID'), nullable=True)
    salesJobMaterialsOrderNumber = Column(Integer, nullable=False)
    salesJobMaterialsDateOrdered = Column(DateTime, nullable=False)
    salesJobMaterialsEstimatedShipDate = Column(DateTime, nullable=False)
    salesJobMaterialsShippedDate = Column(DateTime, nullable=False)
    salesJobMaterialsShippingCarrier = Column(String(225), nullable=False)
    salesJobMaterialsTrackingNumber = Column(String(225), nullable=False)
    salesJobMaterialsDeliveryWarehouseID = Column(Integer, ForeignKey('ConstantsDeliveryWarehouse.constantsDeliveryWarehouseID'), nullable=True)
    salesJobMaterialsOrderedNotes = Column(String(225), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobMaterials(salesJobMaterialsID={self.salesJobMaterialsID})>"
    
class SalesJobCommissions(Base):
    __tablename__ = 'SalesJobCommissions'
    salesJobCommissionsID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesJobCommissions(salesJobCommissionsID={self.salesJobCommissionsID})>"


class ContractLineItem(Base):
    __tablename__ = 'ContractLineItem'
    contractLineItemID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    contractLineItemCategoryID = Column(String(255), nullable=False)
    contractLineItemCategoryName = Column(String(255), nullable=False)
    contractLineItemQuantiy = Column(String(255), nullable=False)
    contractLineItemUnit = Column(String(255), nullable=False)
    contractLineItemMeasure = Column(String(255), nullable=False)
    contractLineItemSelectedItem = Column(String(255), nullable=False)
    contractLineItemPriceAmount = Column(String(255), nullable=False)
    contractLineItemTotalAmount = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContractLineItem(contractLineItemID={self.contractLineItemID})>"



class EmployeePayrollBonus(Base):
    __tablename__ = 'EmployeePayrollBonus'
    employeePayrollBonusID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employeePayrollID = Column(String(255), nullable=False)
    salesJobID = Column(UUID(as_uuid=True), ForeignKey('SalesJob.salesJobID'), nullable=True)
    employeePayrollBonusDescription = Column(String(255), nullable=False)
    employeePayrollBonusQuantity = Column(String(255), nullable=False)
    employeePayrollBonusRate = Column(String(255), nullable=False)
    employeePayrollBonusTotal = Column(String(255), nullable=False)
    employeePayrollBonusStartDate = Column(DateTime, nullable=False)
    employeePayrollBonusEndDate = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmployeePayrollBonus(employeePayrollBonusID={self.employeePayrollBonusID})>"


    
class MasterPayrollPeriod(Base):
    __tablename__ = 'MasterPayrollPeriod'
    masterPayrollPeriodID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    masterPayrollPeriodYear = Column(String(255), nullable=False)
    masterPayrollPeriodPayDate = Column(DateTime, nullable=False)
    masterPayrollPeriodPayStartDate = Column(DateTime, nullable=False)
    masterPayrollPeriodPayEndDate = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<MasterPayrollPeriod(masterPayrollPeriodID={self.masterPayrollPeriodID})>"


class PayrollNotes(Base):
    __tablename__ = 'PayrollNotes'
    payrollNotesID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    masterPayrollPeriodID = Column(UUID(as_uuid=True), ForeignKey('MasterPayrollPeriod.masterPayrollPeriodID'), nullable=True)
    commissionReportID = Column(UUID(as_uuid=True), ForeignKey('CommissionReport.commissionReportID'), nullable=True)
    payrollNotesExcelCreatedDate = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PayrollNotes(payrollNotesID={self.payrollNotesID})>"
    
class SalesPersonAvailabilitySlots(Base):
    __tablename__ = 'SalesPersonAvailabilitySlots'
    salesPersonAvailabilitySlotsID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesPersonAvailabilitySlotsDate = Column(DateTime, nullable=False)
    salesPersonAvailabilitySlotsIsMorningAvailable = Column(Boolean, nullable=False)
    salesPersonAvailabilitySlotsIsAfternoonAvailable = Column(Boolean, nullable=False)
    salesPersonAvailabilitySlotsIsEveningAvailable = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesPersonAvailabilitySlots(salesPersonAvailabilitySlotsID={self.salesPersonAvailabilitySlotsID})>"
    
class SalesPersonAvailability(Base):
    __tablename__ = 'SalesPersonAvailability'
    salesPersonAvailabilityID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesPersonID = Column(Integer, ForeignKey('EmployeeMaster.employeeID'), nullable=True)
    salesPersonAvailabilitySlotsID = Column(UUID(as_uuid=True), ForeignKey('SalesPersonAvailabilitySlots.salesPersonAvailabilitySlotsID'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SalesPersonAvailability(salesPersonAvailabilityID={self.salesPersonAvailabilityID})>"
    
class SamMultiLambdaAppBaseTable(Base):
    __tablename__ = 'SamMultiLambdaAppBaseTable'
    samMultiLambdaAppBaseTableID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    baseSalesJobNumber = Column(Integer, nullable=False, default=100000)
    baseAppointmentNumber = Column(Integer, nullable=False, default=100000)
    baseInboundRecordNumber = Column(Integer, nullable=False, default=100000)
    baseCustomerRecordNumber = Column(Integer, nullable=False, default=100000)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SamMultiLambdaAppBaseTable(samMultiLambdaAppBaseTableID={self.samMultiLambdaAppBaseTableID})>"
    
    def increment_column(self, column_name, session):
        if not hasattr(self, column_name):
            raise ValueError(f"Column '{column_name}' does not exist in the table.")
        
        current_value = getattr(self, column_name)
        if current_value is None:
            raise ValueError(f"Column '{column_name}' has no initial value.")
        
        original_value = current_value
        setattr(self, column_name, current_value + 1)
        session.add(self)
        session.commit()
        
        return original_value
