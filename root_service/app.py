import json
import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routes import routes


DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv('DEBUG', 'False') == 'True'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def lambda_handler(event, context):
    session = Session()
    DEBUG and print(event)
    DEBUG and print(context)

    response = {}
    params = {
        "db_session": session,
        "query" : event.get('body',None)
    }

    try:
        authorizer_claims = event['requestContext'].get("authorizer", {}).get("claims", {})
        if len(authorizer_claims) > 0:
            params["claims"] = authorizer_claims

        body = event.get('body',None)
        if body:
            body = json.loads(body)
            if len(body)>0:
                params['body'] = body
        params['query_params'] = event.get('queryStringParameters',{})
        httpMethod = event['requestContext']['httpMethod']
        handlers = routes.get(httpMethod, {})
        if len(handlers) == 0:
            raise Exception(f"Could not find handler for method - {httpMethod}")

        # requestPath = event['requestContext']['resourcePath']
        requestPath = event['path']
        requestHandler = None

        allHandlers = handlers.keys()
        for handler in allHandlers:
            handlerPattern = re.compile(handler)
            if matchedHandler := handlerPattern.fullmatch(requestPath):
                requestHandler = handlers[handler]
                matchedGroups = matchedHandler.groupdict()
                DEBUG and print(f"matchedHandler: {matchedHandler}, matchedGroups: {matchedGroups}")
                for k,v in matchedGroups.items():
                    if v:
                        params[k] = v

                break

        DEBUG and print(f"requestPath: {requestPath}, requestHandler: {requestHandler}")

        if not requestHandler:
            raise Exception(f"Could not find handler for endpoint - {requestPath}")

        response = requestHandler(**params)
        response.update({'headers' : {
            'Content-Type' : 'application/json',
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods' : 'GET, POST, PUT, DELETE',
            'Access-Control-Allow-Headers' : 'Content-Type, Authorization, authorization'
        }})

    except Exception as e:
        print("Error: ", e)
        response = {
            'statusCode': 500,
            'body': json.dumps({'error' :str(e)}),
            'headers' : {
            'Content-Type' : 'application/json',
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods' : 'GET, POST, PUT, DELETE',
            'Access-Control-Allow-Headers' : 'Content-Type, Authorization, authorization'
        }
    }

    finally:
        session.close()

    print("response: ", response)
    return response