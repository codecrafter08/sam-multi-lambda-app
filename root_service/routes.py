from handlers import root_handler, deleteAllData
UUID_REGEX_PATTERN = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

available_methods = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
]

routes = {
    "GET": {
        "/": root_handler,
    },
    "DELETE" : {
        "/delete-all-data": deleteAllData,
    }
    
    
}