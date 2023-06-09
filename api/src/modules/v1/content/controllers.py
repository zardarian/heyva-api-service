from django.conf import settings
from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.article_tag.models import ArticleTag
from src.modules.v1.dictionary.queries import dictionary_by_id
from src.modules.v1.article_attachment.queries import article_attachment_by_multiple_id
from .queries import content_active, content_by_id
from .models import Content
from .serializers import ReadListContentSerializer, ContentSerializer, PreviewContentSerializer
import uuid
import sys

@api_view(['GET'])
@authentication_classes([CustomBasicAuthentication])
def read_list(request):
    try:
        payload = ReadListContentSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        paginator = CustomPageNumberPagination()
        content = content_active(validated_payload.get('search'), validated_payload.get('tag'), validated_payload.get('app_env', settings.APPLICATION_ENVIRONMENT))
        result_page = paginator.paginate_queryset(content, request)
        serializer = PreviewContentSerializer(result_page, many=True)

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
        content = content_by_id(id).first()
        if not content:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)

        return output_response(success=RESPONSE_SUCCESS, data=ContentSerializer(content).data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
