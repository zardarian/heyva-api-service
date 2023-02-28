from django.http import JsonResponse
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

def output_response(success=None, data=None, message=None, error=None, status_code=None):
    output = {
        'success': success,
        'data': data,
        'message': message,
        'error': error
    }
    return JsonResponse(output, status=status_code)

def output_json(success=None, data=None, message=None, error=None):
    output = {
        'success': success,
        'data': data,
        'message': message,
        'error': error
    }
    return output

def encrypt(txt):
    try:
        if not txt:
            return None
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
    
def decrypt(txt):
    try:
        if not txt:
            return None
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")     
        return decoded_text
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None