from handlers import getEmployees, createEmployee, createOrUpdateSalesPersonAvailabilitySlot, getSalesPersonAvailabilitySlots
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
        f"/employees/?(?P<employee_id>{INTEGER_REGEX_PATTERN})?/?$": getEmployees,
        "/sales-person-available-slot" : getSalesPersonAvailabilitySlots,
    },
    "POST": {
        "/employees": createEmployee,
        "/sales-person-available-slot" : createOrUpdateSalesPersonAvailabilitySlot,
    },


}
