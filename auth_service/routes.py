
from handlers import login, refreshToken, forgotPassword, confirmPassword
UUID_REGEX_PATTERN = "[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"

available_methods = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
]

routes = {
    
    "POST": {
        "/login": login,
        "/refresh-token": refreshToken,
        "/forgot-password": forgotPassword,
        "/confirm-password": confirmPassword
        
    },
    
}
