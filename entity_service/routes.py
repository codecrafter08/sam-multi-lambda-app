from handlers import getEntity, createEntity, getEntityCalls, createEntityCall, getEntitySecondaryContactDetails, createEntitySecondaryContactDetail, updateEntitySecondaryContactDetail, getEntityPropertyContact, createEntityPropertyContact, updateEntityPropertyContact, updateEntity, getEntityAppointments, createEntityAppointment, updateEntityProperty, getEntityProperty, createEntityProperty, updateEntityAppointment, updateEntitycall, getSubContractor, getEntityCallback, createSubContractor, createCallback, updateSubContractor, updateCallback, deleteSubContractor, getEntityAppointmentsList, getSubContractorInstaller, createSubContractorInstaller, updateSubContractorInstaller, deleteSubContractorInstaller, getEntityWithUnissuedAppointments, getEntityDetails, getEntityAppointmentDetails, getEntityPropertyDetails, createProspectDetail, updateIssuedAppointments, updateLockedStatus, getAllLockedEntity, sendAppointmentEmail
UUID_REGEX_PATTERN = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
INTEGER_REGEX_PATTERN = "[0-9]{0,}"
available_methods = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
]

routes = {
    "GET": {
        f"/entity/?(?P<entity_id>{UUID_REGEX_PATTERN})?/?$": getEntity,
        f"/entity-call/?(?P<entity_call_id>{UUID_REGEX_PATTERN})?/?$": getEntityCalls,
        f"/entity-secondary-contact/?(?P<entity_secondary_contact_id>{UUID_REGEX_PATTERN})?/?$": getEntitySecondaryContactDetails,
        f"/entity-property-contact/?(?P<entity_property_contact_id>{UUID_REGEX_PATTERN})?/?$": getEntityPropertyContact,
        f"/entity-appointments/?(?P<entity_appointment_id>{UUID_REGEX_PATTERN})?/?$": getEntityAppointments,
        f"/entity-property/?(?P<entity_property_id>{UUID_REGEX_PATTERN})?/?$": getEntityProperty,
        f"/sub-contractor-installer-data/?(?P<sub_contractor_id>{INTEGER_REGEX_PATTERN})?/?$": getSubContractorInstaller,
        f"/sub-contractor-installer/?(?P<sub_contractor_installer_id>{INTEGER_REGEX_PATTERN})?/?$": getSubContractorInstaller,
        "/entity-appointment-list": getEntityAppointmentsList,
        "/sub-contractor": getSubContractor,
        f"/entity-callback": getEntityCallback,
        "/issued-appointments" : getEntityWithUnissuedAppointments,
        f"/entity-details/?(?P<entity_id>{UUID_REGEX_PATTERN})?/?$": getEntityDetails,
        f"/entity-property-details/?(?P<entity_id>{UUID_REGEX_PATTERN})?/?$": getEntityPropertyDetails,
        f"/entity-appointment-details/?(?P<entity_id>{UUID_REGEX_PATTERN})?/?$": getEntityAppointmentDetails,
        "/locked-entities" : getAllLockedEntity,


    },
    "POST": {
        "/entity": createEntity,
        "/entity-call": createEntityCall,
        "/entity-secondary-contact" : createEntitySecondaryContactDetail,
        "/entity-property-contact" : createEntityPropertyContact,
        "/entity-appointments": createEntityAppointment,
        "/entity-property": createEntityProperty,
        "/sub-contractor" :createSubContractor,
        "/entity-callback" : createCallback,
        "/sub-contractor-installer" : createSubContractorInstaller,
        "/prospect-details" : createProspectDetail,
        "/update-issued-appointmnets" : updateIssuedAppointments,
        "/update-locked-status" : updateLockedStatus,
        "/send-email" : sendAppointmentEmail

        
        
    },
    "PATCH" : {
        "/entity" : updateEntity,
        "/entity-secondary-contact" : updateEntitySecondaryContactDetail,
        "/entity-property-contact" : updateEntityPropertyContact,
        "/entity-property" : updateEntityProperty,
        "/entity-call" : updateEntitycall,
        "/entity-appointments" : updateEntityAppointment,
        # "/entity-appointment-list" : updateAppointment,
        "/sub-contractor" :updateSubContractor,
        "/entity-callback" : updateCallback,
        "/sub-contractor-installer" : updateSubContractorInstaller
    },

     "DELETE" : {
        f"/sub-contractor/?(?P<sub_contractor_id>{INTEGER_REGEX_PATTERN})?/?$": deleteSubContractor, 
        f"/sub-contractor-installer/?(?P<sub_contractor_installer_id>{INTEGER_REGEX_PATTERN})?/?$": deleteSubContractorInstaller,       
    }

}



