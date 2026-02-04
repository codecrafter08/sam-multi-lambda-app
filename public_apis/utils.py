import boto3
from botocore.config import Config
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os
import json

config = Config(
    region_name='us-west-1'
)

ssm_client = boto3.client('ssm', config=config) 

def get_all_parameters():
    parameters = []
    paginator = ssm_client.get_paginator('describe_parameters')
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for param in page['Parameters']:
            parameters.append(param['Name'])

    return parameters

def get_parameter_values_as_list(parameter_names):
    parameter_values_dict = {}
    
    for i in range(0, len(parameter_names), 10):
        response = ssm_client.get_parameters( Names=parameter_names[i:i+10], WithDecryption=True )
        for param in response['Parameters']:
            parameter_values_dict[param['Name']] = [param['Value']]

    return parameter_values_dict

def get_values(parameter_n):
        response = ssm_client.get_parameters( Names=parameter_n, WithDecryption=True )
        parameter_value = response['Parameters']
        return parameter_value

#api response
def api_response(success=False, data=None, message=None, error=None):
    response = {
        'success': success,
        'data': data if data is not None else {},
        'message': message if message is not None else 'something went wrong',
        'error': error if error is not None else 'null'
    }
    return response

AES_KEY = bytes.fromhex("0bb5e733a1976c2254fe6ffa2b33c67d90ced3e064d3c5588727b2bc23d900da")
AES_IV = bytes.fromhex("11c59f43ba75de3595f9363c8aa65cdf")

def decrypt_data(encrypted_data):
    try:
        # Decode from Base64
        encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data)
        iv = encrypted_data_bytes[:16]  # Extract the IV
        actual_encrypted_data = encrypted_data_bytes[16:]
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt and remove padding
        decrypted_padded_data = decryptor.update(actual_encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_bytes = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        # Convert bytes to dictionary
        return json.loads(decrypted_bytes.decode())
    except Exception as e:
        print(f"Error decrypting data: {e}")
        return None
