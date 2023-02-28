from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed, ParseError
from src.modules.v1.user.models import User
from src.helpers import output_json
from src.constants import RESPONSE_FAILED, AUTHORIZATION_HEADER_DOES_NOT_EXISTS, INVALID_SIGNATURE, EXPIRED_SIGNATURE, USER_IDENTIFIER_NOT_FOUND_IN_JWT, USER_NOT_FOUND, AUTHORIZATION_PARSE_ERROR, USER_DOES_NOT_MATCH
import jwt

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            output = output_json(success=RESPONSE_FAILED, data=None, message=AUTHORIZATION_HEADER_DOES_NOT_EXISTS, error=None)
            raise exceptions.AuthenticationFailed(output)
        
        jwt_token = CustomJWTAuthentication.get_the_token_from_header(auth_header)
        try:
            payload = jwt.decode(jwt_token, settings.JWT_CONFIG['SIGNING_KEY'], algorithms=[settings.JWT_CONFIG['ALGORITHM']])
        except jwt.exceptions.InvalidSignatureError:
            output = output_json(success=RESPONSE_FAILED, data=None, message=INVALID_SIGNATURE, error=None)
            raise AuthenticationFailed(output)
        except jwt.exceptions.ExpiredSignatureError:
            output = output_json(success=RESPONSE_FAILED, data=None, message=EXPIRED_SIGNATURE, error=None)
            raise AuthenticationFailed(output)
        except:
            raise ParseError()

        user_identifier = payload.get('user_identifier')
        if user_identifier is None:
            output = output_json(success=RESPONSE_FAILED, data=None, message=USER_IDENTIFIER_NOT_FOUND_IN_JWT, error=None)
            raise AuthenticationFailed(output)

        user = User.objects.filter(id=user_identifier).first()
        if user is None:
            output = output_json(success=RESPONSE_FAILED, data=None, message=USER_NOT_FOUND, error=None)
            raise AuthenticationFailed(output)

        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'
    
    @classmethod
    def create_access_token(cls, user):
        payload = {
            'user_identifier': user.get('id'),
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONFIG['ACCESS_TOKEN_LIFETIME'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'username': user.get('username'),
            'email': user.get('email'),
            'phone_number': user.get('phone_number')
        }

        jwt_token = jwt.encode(payload, settings.JWT_CONFIG['SIGNING_KEY'], algorithm=settings.JWT_CONFIG['ALGORITHM'])

        return jwt_token
    
    @classmethod
    def create_refresh_token(cls, user):
        payload = {
            'user_identifier': user.get('id'),
            'exp': int((datetime.now() + timedelta(days=settings.JWT_CONFIG['REFRESH_TOKEN_LIFETIME'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'username': user.get('username'),
            'email': user.get('email'),
            'phone_number': user.get('phone_number')
        }

        jwt_token = jwt.encode(payload, settings.JWT_CONFIG['SIGNING_KEY'], algorithm=settings.JWT_CONFIG['ALGORITHM'])

        return jwt_token
    
    @classmethod
    def validate_refresh_token(cls, refresh_token, user_id):
        try:
            payload = jwt.decode(refresh_token, settings.JWT_CONFIG['SIGNING_KEY'], algorithms=[settings.JWT_CONFIG['ALGORITHM']])
        except jwt.exceptions.InvalidSignatureError:
            return False, INVALID_SIGNATURE
        except jwt.exceptions.ExpiredSignatureError:
            return False, EXPIRED_SIGNATURE
        except:
            return False, AUTHORIZATION_PARSE_ERROR

        user_identifier = payload.get('user_identifier')
        if user_identifier is None:
            return False, USER_IDENTIFIER_NOT_FOUND_IN_JWT

        if user_identifier != user_id:
            return False, USER_DOES_NOT_MATCH

        return True, user_id

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token