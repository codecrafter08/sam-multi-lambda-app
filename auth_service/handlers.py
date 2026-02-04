import boto3
import json
import os
from botocore.exceptions import ClientError
from utils import api_response, initiate_auth, get_secret_hash, provider_client,  CLIENT_ID








def login(**kwargs):
    try:
        response_data = api_response()
        body = kwargs.get('body', {})
        username = body.get('username')
        password = body.get('password')
        
        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")
       
            
        resp, msg = initiate_auth(provider_client, username, password)
        if msg != None:
            return {'message': msg,
                    "error": True, "success": False, "data": None}
        if resp.get("AuthenticationResult"):
            response_data.update({ 'message': "success",
                    "error": False,
                    "success": True,
                    "data": {
                        "id_token": resp["AuthenticationResult"]["IdToken"],
                        "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                        "access_token": resp["AuthenticationResult"]["AccessToken"],
                        "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                        "token_type": resp["AuthenticationResult"]["TokenType"]
                    }})
        
        return { 'statusCode': 200, 'body': json.dumps(response_data)}
    
    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong."
        })
        return {'statusCode': 500,'body': json.dumps(response_data) }
    

def refreshToken(**kwargs):
    try:
        response_data = api_response()
        body = kwargs.get('body', {})
        refresh_token = body.get('refresh_token')

        if not refresh_token:
            raise ValueError("Refresh token is required")

        # Perform token refresh using Cognito Initiate Auth
        auth_response = provider_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token
            }
        )

        
        access_token = auth_response['AuthenticationResult']['AccessToken']
        id_token = auth_response['AuthenticationResult']['IdToken']

        # Successful refresh token response
        response_data.update({
            "success": True,
            "message": "Token refreshed successfully",
            "data": {
                "access_token": access_token,
                "id_token": id_token
            }
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except ClientError as e:
        response_data.update({
            "error": str(e),
            "message": "Token refresh failed"
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "An error occurred during token refresh"
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
    

def forgotPassword(**kwargs):
    """
    This function initiates the forgot password process by sending a reset code to the user.
    """
    try:
        response_data = api_response()
        body = kwargs.get('body', {})
        username = body.get('username')

        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        provider_client.forgot_password(
            ClientId=CLIENT_ID,
            Username=username
        )

        response_data.update({
            "success": True,
            "message": "Password reset code sent successfully. Please check your email or phone.",
            "data": None
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except provider_client.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "error": True,
                "success": False,
                "message": "User not found",
                "data": None
            })
        }

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong during forgot password request."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}


def confirmPassword(**kwargs):
    """
    This function confirms the forgot password process by verifying the reset code
    and updating the password.
    """
    try:
        response_data = api_response()
        body = kwargs.get('body', {})
        username = body.get('username')
        confirmation_code = body.get('confirmation_code')
        new_password = body.get('new_password')

        db_session = kwargs.get('db_session', None)
        if not db_session:
            raise Exception("db_session not passed to handler")

        provider_client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code,
            Password=new_password
        )

        response_data.update({
            "success": True,
            "message": "Password reset successfully. You can now log in with your new password.",
            "data": None
        })
        return {'statusCode': 200, 'body': json.dumps(response_data)}

    except provider_client.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "error": True,
                "success": False,
                "message": "User not found",
                "data": None
            })
        }

    except provider_client.exceptions.CodeMismatchException:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "error": True,
                "success": False,
                "message": "Invalid confirmation code",
                "data": None
            })
        }

    except provider_client.exceptions.ExpiredCodeException:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "error": True,
                "success": False,
                "message": "The confirmation code has expired",
                "data": None
            })
        }

    except Exception as e:
        response_data.update({
            "error": str(e),
            "message": "Something went wrong during password reset confirmation."
        })
        return {'statusCode': 500, 'body': json.dumps(response_data)}
