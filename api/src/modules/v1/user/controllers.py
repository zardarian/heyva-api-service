from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, authentication_classes
from src.helpers import output_response, encrypt, decrypt
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, USER_ALREADY_EXISTS, USER_DOES_NOT_EXISTS, PASSWORD_DOES_NOT_MATCH, MULTIPLE_ROWS_RETURNED, AUTHENTICATION_FAILED
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from datetime import datetime
from .serializers import RegisterSerializer, LoginSerializer, LoginResponseSerializer, UserSerializer, RefreshTokenSerializer
from .models import User
from .queries import user_exists, user_by_id
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def register(request):
    payload = RegisterSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=list(payload.errors.keys()), status_code=400)
    
    validated_payload = payload.validated_data
    try:
        existed_user = user_exists(validated_payload.get('username'), validated_payload.get('email'), validated_payload.get('phone_number'))
        if existed_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_ALREADY_EXISTS, error=None, status_code=400)

        user_uuid = uuid.uuid4()
        encrypted_email = validated_payload.get('email')
        encrypted_phone_number = validated_payload.get('phone_number')
        
        with transaction.atomic():
            insert_payload = {
                'id' : str(user_uuid),
                'created_at' : datetime.now(),
                'created_by' : validated_payload.get('username', validated_payload.get('email', validated_payload.get('phone_number'))),
                'is_active' : True,
                'username' : validated_payload.get('username'),
                'email' : encrypted_email,
                'phone_number' : encrypted_phone_number,
                'password' : make_password(validated_payload.get('password'))
            }
            User(**insert_payload).save()
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': insert_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def login(request):
    payload = LoginSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=list(payload.errors.keys()), status_code=400)
    
    validated_payload = payload.validated_data
    try:
        existed_user = user_exists(validated_payload.get('username'), validated_payload.get('username'), validated_payload.get('username'))
        if not existed_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=401)
        if len(existed_user) > 1:
            return output_response(success=RESPONSE_FAILED, data=None, message=MULTIPLE_ROWS_RETURNED, error=None, status_code=400)

        user = existed_user.values().first()
        password_match = check_password(validated_payload.get('password'), user.get('password'))
        if not password_match:
            return output_response(success=RESPONSE_FAILED, data=None, message=PASSWORD_DOES_NOT_MATCH, error=None, status_code=401)
        
        access_token = CustomJWTAuthentication.create_access_token(user)
        refresh_token = CustomJWTAuthentication.create_refresh_token(user)
        response_data = LoginResponseSerializer(data={
            'id': user.get('id'),
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        if not response_data.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=AUTHENTICATION_FAILED, error=None, status_code=400)

        return output_response(success=RESPONSE_SUCCESS, data=response_data.validated_data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def refresh_token(request):
    payload = RefreshTokenSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=list(payload.errors.keys()), status_code=400)
    
    validated_payload = payload.validated_data
    try:
        user = user_by_id(validated_payload.get('id'))
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        validate_refresh_token = CustomJWTAuthentication.validate_refresh_token(validated_payload.get('refresh_token'), validated_payload.get('id'))
        
        if not validate_refresh_token[0]:
            return output_response(success=RESPONSE_FAILED, data=None, message=validate_refresh_token[1], error=None, status_code=404)

        user = user.values().first()
        access_token = CustomJWTAuthentication.create_access_token(user)
        refresh_token = CustomJWTAuthentication.create_refresh_token(user)
        response_data = LoginResponseSerializer(data={
            'id': user.get('id'),
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        if not response_data.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=AUTHENTICATION_FAILED, error=None, status_code=400)

        return output_response(success=RESPONSE_SUCCESS, data=response_data.validated_data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def get_user(request):
    try:
        user = user_by_id(request.user.id)
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        user = user.first()
        serialize_user = UserSerializer(user).data

        return output_response(success=RESPONSE_SUCCESS, data=serialize_user, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)