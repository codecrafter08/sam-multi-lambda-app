import random
import boto3
import base64, hmac, hashlib
import os
from botocore.exceptions import ClientError

USER_POOL_ID = os.environ.get('USER_POOL_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
region_name= os.environ.get('AWS_REGION', 'us-west-1')
AWS_ACCESS_KEY_ID= os.environ.get('AWS_ACCESS_KEY_ID')
CLIENT_SECRET= os.environ.get('CLIENT_SECRET')


provider_client = boto3.client('cognito-idp', region_name=region_name, aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#api response
def api_response(success=False, data=None, message=None, error=None):
    response = {
        'success': success,
        'data': data if data is not None else {},
        'message': message if message is not None else 'something went wrong',
        'error': error if error is not None else 'null'
    }
    return response


def generate_6_digit_number():
    return random.randint(100000, 999999)


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(
        str(CLIENT_SECRET).encode('utf-8'),
        msg=str(msg).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def initiate_auth(client, username, password):
    secret_hash = get_secret_hash(username)
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password, })
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None
