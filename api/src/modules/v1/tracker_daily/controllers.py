from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.storages.services import put_object, remove_object
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, EMPTY_DATA
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.program_tag.models import ProgramTag
from src.modules.v1.content.models import Content
from src.modules.v1.tracker_type.queries import tracker_type_by_id
from src.modules.v1.profile.queries import profile_by_user_id
from src.modules.v1.content.queries import content_active
from src.modules.v1.content.serializers import PreviewContentSerializer
from .queries import tracker_daily_today_by_profile_code, tracker_daily_insight, tracker_daily_recommendation
from .serializers import CreateTrackerDailySerializer, InsightSerializer, TrackerDailySerializer, RecommendationSerializer
from .models import TrackerDaily
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateTrackerDailySerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        tracker_daily_uuid = uuid.uuid4()

        with transaction.atomic():
            profile = profile_by_user_id(request.user.get('id')).first()
            tracker_daily = tracker_daily_today_by_profile_code(profile.code)

            if tracker_daily:
                tracker_daily.delete()

            tracker_daily_payload = {
                'id' : tracker_daily_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'profile_code' : profile,
                'type' : tracker_type_by_id(validated_payload.get('type')).first(),
                'response' : validated_payload.get('response'),
            }
            TrackerDaily(**tracker_daily_payload).save()

        return output_response(success=RESPONSE_SUCCESS, data={'id': tracker_daily_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def insight(request):
    try:
        payload = InsightSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        tracker_daily = tracker_daily_insight(request.user.get('profile_code'), validated_payload.get('type'), validated_payload.get('date'))
        serializer = TrackerDailySerializer(tracker_daily, many=True).data

        return output_response(success=RESPONSE_SUCCESS, data=serializer, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def recommendation(request):
    try:
        payload = RecommendationSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        tracker_daily = tracker_daily_recommendation(request.user.get('profile_code'), validated_payload.get('date'))
        tracker_daily_serializer = TrackerDailySerializer(tracker_daily, many=True).data

        tags = []
        for data in tracker_daily_serializer:
            for response in data.get('response'):
                tags = list(set(tags).union(set(response.get('answer').get('related_tag'))))

        if not tags:
            return output_response(success=RESPONSE_FAILED, data=None, message=EMPTY_DATA, error=None, status_code=400)

        paginator = CustomPageNumberPagination()
        contents = content_active(search=None, tag=tags)
        result_page = paginator.paginate_queryset(contents, request)
        contents_serializer = PreviewContentSerializer(result_page, many=True).data

        return paginator.get_paginated_response(success=RESPONSE_SUCCESS, data=contents_serializer, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)