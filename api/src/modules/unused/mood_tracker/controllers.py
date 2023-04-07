from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.paginations.page_number_pagination import CustomPageNumberPagination   
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.profile.queries import profile_by_code
from src.modules.v1.dictionary.queries import dictionary_by_id
from datetime import datetime
from .serializers import CreateMoodTrackerSerializer, ReadListMoodTrackerSerializer, MoodTrackerSerializer
from .models import MoodTracker
from .queries import mood_tracker_list
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateMoodTrackerSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        mood_tracker_uuid = uuid.uuid4()
        mood_value = 0
        mood_feel = dictionary_by_id(validated_payload.get('mood_feel')).values().first()
        if mood_feel:
            mood_value = mood_feel.get('value')

        with transaction.atomic():
            mood_tracker_payload = {
                'id' : mood_tracker_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'profile_code' : profile_by_code(request.user.get('profile_code')).first(),
                'mood_feel' : validated_payload.get('mood_feel'),
                'mood_source' : validated_payload.get('mood_source'),
                'more' : validated_payload.get('more'),
                'mood_value': mood_value,
            }
            MoodTracker(**mood_tracker_payload).save()
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': mood_tracker_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def read_list(request):
    try:
        payload = ReadListMoodTrackerSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        paginator = CustomPageNumberPagination()
        mood_tracker = mood_tracker_list(validated_payload.get('created_start'), validated_payload.get('created_end'), validated_payload.get('profile_code'), validated_payload.get('mood_feel'), validated_payload.get('mood_source'), validated_payload.get('search'))
        result_page = paginator.paginate_queryset(mood_tracker, request)
        serializer = MoodTrackerSerializer(result_page, many=True)

        return paginator.get_paginated_response(success=RESPONSE_SUCCESS, data=serializer.data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def read_list_by_auth(request):
    try:
        payload = ReadListMoodTrackerSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        paginator = CustomPageNumberPagination()
        mood_tracker = mood_tracker_list(validated_payload.get('created_start'), validated_payload.get('created_end'), request.user.get('profile_code'), validated_payload.get('mood_feel'), validated_payload.get('mood_source'), validated_payload.get('search'))
        result_page = paginator.paginate_queryset(mood_tracker, request)
        serializer = MoodTrackerSerializer(result_page, many=True)

        return paginator.get_paginated_response(success=RESPONSE_SUCCESS, data=serializer.data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)