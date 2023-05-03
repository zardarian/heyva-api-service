from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.super_admin_permission import IsSuperAdmin
from datetime import datetime
from .serializers import CreateDictionarySerializer, ReadByTypeDictionarySerializer, DictionarySerializer, UpdateDictionarySerializer
from .models import Dictionary
from .queries import dictionary_active_by_type_id, dictionary_by_id
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsSuperAdmin])
def create(request):
    payload = CreateDictionarySerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        dictionary_uuid = uuid.uuid4()
        
        with transaction.atomic():
            dictionary_payload = {
                'id' : str(dictionary_uuid),
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'type' : validated_payload.get('type'),
                'name' : validated_payload.get('name'),
                'parent' : validated_payload.get('parent'),
                'is_active' : True
            }
            Dictionary(**dictionary_payload).save()
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': dictionary_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['GET'])
@authentication_classes([CustomBasicAuthentication])
def read_by_type(request):
    try:
        payload = ReadByTypeDictionarySerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data
        dictionary = dictionary_active_by_type_id(validated_payload.get('type'), validated_payload.get('id'), validated_payload.get('search'))

        return output_response(success=RESPONSE_SUCCESS, data=DictionarySerializer(dictionary, many=True).data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsSuperAdmin])
def update(request, id):
    payload = UpdateDictionarySerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        dictionary = dictionary_by_id(id)
        if not dictionary:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)
        
        legacy = dictionary.values().first()
        
        with transaction.atomic():
            dictionary.update(
                updated_at=datetime.now(),
                updated_by=request.user.get('id'),
                type=validated_payload.get('type', legacy.get('type')),
                name=validated_payload.get('name', legacy.get('name')),
                parent=validated_payload.get('parent', legacy.get('parent')),
            )
        
        return output_response(success=RESPONSE_SUCCESS, data=validated_payload, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsSuperAdmin])
def delete(request, id):
    try:
        dictionary = dictionary_by_id(id)
        if not dictionary:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)
        
        with transaction.atomic():
            dictionary.update(
                deleted_at=datetime.now(),
                deleted_by=request.user.get('id')
            )
        
        return output_response(success=RESPONSE_SUCCESS, data=None, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsSuperAdmin])
def activate(request, id):
    try:
        dictionary = dictionary_by_id(id)
        if not dictionary:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)

        with transaction.atomic():
            dictionary.update(
                updated_at=datetime.now(),
                updated_by=request.user.get('id'),
                is_active=True,
            )
        
        return output_response(success=RESPONSE_SUCCESS, data=None, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsSuperAdmin])
def deactivate(request, id):
    try:
        dictionary = dictionary_by_id(id)
        if not dictionary:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)
        
        with transaction.atomic():
            dictionary.update(
                updated_at=datetime.now(),
                updated_by=request.user.get('id'),
                is_active=False,
            )
        
        return output_response(success=RESPONSE_SUCCESS, data=None, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
