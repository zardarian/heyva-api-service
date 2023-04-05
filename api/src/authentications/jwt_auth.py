from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed, ParseError
from src.modules.v1.user.queries import user_by_id
from src.modules.v1.role.queries import role_by_user_id
from src.modules.v1.profile.queries import profile_by_user_id
from src.modules.v1.user.serializers import AuthenticateSerializer
from src.helpers import output_json
from src.constants import RESPONSE_FAILED, AUTHORIZATION_HEADER_DOES_NOT_EXISTS, INVALID_SIGNATURE, EXPIRED_SIGNATURE, USER_IDENTIFIER_NOT_FOUND_IN_JWT, USER_NOT_FOUND, AUTHORIZATION_PARSE_ERROR, USER_DOES_NOT_MATCH, JWT_ACCESS, JWT_REFRESH, JWT_REGISTRATION, JWT_REQUEST_RESET_PASSWORD, JWT_INVALID_SCOPE
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

        user = user_by_id(user_identifier).first()
        if user is None:
            output = output_json(success=RESPONSE_FAILED, data=None, message=USER_NOT_FOUND, error=None)
            raise AuthenticationFailed(output)
        
        if payload.get('scope') != JWT_ACCESS:
            output = output_json(success=RESPONSE_FAILED, data=None, message=JWT_INVALID_SCOPE, error=None)
            return AuthenticationFailed(output)
        
        serialized_user = AuthenticateSerializer(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'is_verified': user.is_verified,
                'last_login': user.last_login,
                'profile_code': payload.get('profile_code'),
                'roles': payload.get('roles'),
                'is_bearer': True
            }
        )
        
        return serialized_user.data, payload

    def authenticate_header(self, request):
        return 'Bearer'
    
    @classmethod
    def create_access_token(cls, user):
        profile = profile_by_user_id(user.get('id')).values().first()
        roles = role_by_user_id(user.get('id')).values_list('role', flat=True)
        payload = {
            'user_identifier': user.get('id'),
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONFIG['ACCESS_TOKEN_LIFETIME'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'scope': JWT_ACCESS,
            'username': user.get('username'),
            'email': user.get('email'),
            'phone_number': user.get('phone_number'),
            'profile_code': profile.get('code'),
            'roles': list(roles),
        }

        jwt_token = jwt.encode(payload, settings.JWT_CONFIG['SIGNING_KEY'], algorithm=settings.JWT_CONFIG['ALGORITHM'])

        return jwt_token
    
    @classmethod
    def create_refresh_token(cls, user):
        roles = role_by_user_id(user.get('id')).values_list('role', flat=True)
        payload = {
            'user_identifier': user.get('id'),
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONFIG['REFRESH_TOKEN_LIFETIME'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'scope': JWT_REFRESH,
            'username': user.get('username'),
            'email': user.get('email'),
            'phone_number': user.get('phone_number'),
            'roles': list(roles),
        }

        jwt_token = jwt.encode(payload, settings.JWT_CONFIG['SIGNING_KEY'], algorithm=settings.JWT_CONFIG['ALGORITHM'])

        return jwt_token
    
    @classmethod
    def create_registration_token(cls, user):
        payload = {
            'user_identifier': user.get('id'),
            'exp': int((datetime.now() + timedelta(minutes=settings.JWT_CONFIG['REGISTRATION_TOKEN_LIFETIME'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'scope': JWT_REGISTRATION,
            'username': user.get('username'),
            'email': user.get('email'),
            'phone_number': user.get('phone_number')
        }

        jwt_token = jwt.encode(payload, settings.JWT_CONFIG['SIGNING_KEY'], algorithm=settings.JWT_CONFIG['ALGORITHM'])

        return jwt_token
    
    @classmethod
    def create_request_reset_password_token(cls, user):
        payload = {
            'user_identifier': user.get('id'),
            'exp': int((datetime.now() + timedelta(minutes=settings.JWT_CONFIG['REQUEST_RESET_PASSWORD_TOKEN_LIFETIME'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'scope': JWT_REQUEST_RESET_PASSWORD,
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
        
        if payload.get('scope') != JWT_REFRESH:
            return False, JWT_INVALID_SCOPE

        return True, user_id
    
    @classmethod
    def validate_registration_token(cls, registration_token, user_id):
        try:
            payload = jwt.decode(registration_token, settings.JWT_CONFIG['SIGNING_KEY'], algorithms=[settings.JWT_CONFIG['ALGORITHM']])
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
        
        if payload.get('scope') != JWT_REGISTRATION:
            return False, JWT_INVALID_SCOPE

        return True, user_id
    
    @classmethod
    def validate_request_reset_password_token(cls, request_reset_password_token, user_id):
        try:
            payload = jwt.decode(request_reset_password_token, settings.JWT_CONFIG['SIGNING_KEY'], algorithms=[settings.JWT_CONFIG['ALGORITHM']])
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
        
        if payload.get('scope') != JWT_REQUEST_RESET_PASSWORD:
            return False, JWT_INVALID_SCOPE

        return True, user_id

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token