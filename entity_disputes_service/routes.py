from handlers import getEntityDisputes

routes = {
    "GET": {
        "/entity-disputes/?$": getEntityDisputes,
    }
} 