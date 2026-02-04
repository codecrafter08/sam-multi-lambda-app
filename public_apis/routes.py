from handlers import getConstants, updateAppointmentStatus


available_methods = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
]

routes = {
    "GET": {
        "/public/constants/?$": getConstants,
        "/public/update-appointment-status/?$" : updateAppointmentStatus
    },
}
