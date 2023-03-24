from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.video_content_tag.models import VideoContentTag
from src.modules.v1.dictionary.queries import dictionary_by_id
from src.modules.v1.video_content_attachment.queries import video_content_attachment_by_multiple_id
from datetime import datetime
from .serializers import CreateVideoContentSerializer, VideoContentSerializer, ReadVideoContentSerializer, VideoContentByAuthSerializer
from .models import VideoContent
from .queries import video_content_active, video_content_by_id
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def create(request):
    payload = CreateVideoContentSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        video_content_uuid = uuid.uuid4()

        with transaction.atomic():
            video_content_payload = {
                'id' : video_content_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'is_active' : True,
                'title' : validated_payload.get('title'),
                'body' : validated_payload.get('body'),
                'creator': validated_payload.get('creator'),
            }
            VideoContent(**video_content_payload).save()

            tag_payload = []
            for tag in validated_payload.get('tag'):
                tag_uuid = uuid.uuid4()
                payload = VideoContentTag(
                    id=tag_uuid,
                    created_at=datetime.now(),
                    created_by=request.user.get('id'),
                    video_content=video_content_by_id(video_content_uuid).first(),
                    tag=dictionary_by_id(tag).first(),
                )
                tag_payload.append(payload)
            VideoContentTag.objects.bulk_create(tag_payload)

            if validated_payload.get('attachment'):
                video_content_attachment = video_content_attachment_by_multiple_id(validated_payload.get('attachment'))
                video_content_attachment.update(
                    video_content=video_content_uuid
                )
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': video_content_payload.get('id')}, message=None, error=None, status_code=200)
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
        payload = ReadVideoContentSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        paginator = CustomPageNumberPagination()
        video_content = video_content_active(validated_payload.get('search'), validated_payload.get('tag'))
        result_page = paginator.paginate_queryset(video_content, request)
        if request.user.get('is_bearer') == True:
            serializer = VideoContentByAuthSerializer(result_page, context={'request': request}, many=True)
        else:
            serializer = VideoContentSerializer(result_page, many=True)

        return paginator.get_paginated_response(success=RESPONSE_SUCCESS, data=serializer.data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['GET'])
@authentication_classes([CustomBasicAuthentication])
def read_by_id(request, id):
    try:
        video_content = video_content_by_id(id)
        if not video_content:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)

        return output_response(success=RESPONSE_SUCCESS, data=VideoContentSerializer(video_content, many=True).data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)