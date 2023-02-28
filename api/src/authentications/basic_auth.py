from rest_framework import authentication, exceptions
from django.conf import settings
from src.helpers import output_json
from src.constants import RESPONSE_FAILED, AUTHORIZATION_HEADER_DOES_NOT_EXISTS, AUTHORIZATION_HEADER_DOES_NOT_CONFIGURED_PROPERLY, AUTHORIZATION_HEADER_DOES_NOT_MATCH
import base64

class CustomBasicAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            output = output_json(success=RESPONSE_FAILED, data=None, message=AUTHORIZATION_HEADER_DOES_NOT_EXISTS, error=None)
            raise exceptions.AuthenticationFailed(output)
        if auth_header.split(' ')[0] != 'Basic':
            output = output_json(success=RESPONSE_FAILED, data=None, message=AUTHORIZATION_HEADER_DOES_NOT_CONFIGURED_PROPERLY, error=None)
            raise exceptions.AuthenticationFailed(output)
        
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        if not username or not password:
            output = output_json(success=RESPONSE_FAILED, data=None, message=AUTHORIZATION_HEADER_DOES_NOT_CONFIGURED_PROPERLY, error=None)
            raise exceptions.AuthenticationFailed(output)
        
        if username != settings.BASIC_AUTH_USERNAME or password != settings.BASIC_AUTH_PASSWORD:
            output = output_json(success=RESPONSE_FAILED, data=None, message=AUTHORIZATION_HEADER_DOES_NOT_MATCH, error=None)
            raise exceptions.AuthenticationFailed(output)
    
    def authenticate_header(self, request):
        return 'Basic'