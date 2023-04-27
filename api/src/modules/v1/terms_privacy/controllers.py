from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime
from src.storages.services import put_object, remove_object
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.doctor_tag.models import DoctorTag
from src.modules.v1.profile.queries import profile_by_code
from src.modules.v1.dictionary.queries import dictionary_by_id
from .serializers import ReadTermsPrivacyByTypeSerializer, TermsPrivacySerializer, ReadListSerializer
from .models import TermsPrivacy
from .queries import terms_privacy_by_type, terms_privacy_active
import uuid
import sys

@api_view(['GET'])
@authentication_classes([CustomBasicAuthentication])
def read_by_type(request):
    try:
        payload = ReadTermsPrivacyByTypeSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        terms_privacy = terms_privacy_by_type(validated_payload.get('type'), validated_payload.get('platform'), validated_payload.get('version'))
        if not terms_privacy:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)
        
        serializer = TermsPrivacySerializer(terms_privacy.first(), context={'request': request}).data

        return output_response(success=RESPONSE_SUCCESS, data=serializer, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['GET'])
@authentication_classes([CustomBasicAuthentication])
def read_list(request):
    try:
        payload = ReadListSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        terms_privacy = terms_privacy_active(validated_payload.get('type'), validated_payload.get('platform'), validated_payload.get('version'))
        if not terms_privacy:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)
        
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(terms_privacy, request)
        serializer = TermsPrivacySerializer(result_page, context={'request': request}, many=True)

        return paginator.get_paginated_response(success=RESPONSE_SUCCESS, data=serializer.data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)