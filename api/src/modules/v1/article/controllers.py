from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.modules.v1.article_tag.models import ArticleTag
from src.modules.v1.dictionary.queries import dictionary_by_id
from src.modules.v1.article_attachment.queries import article_attachment_by_multiple_id
from datetime import datetime
from .serializers import CreateArticleSerializer, ArticleSerializer, ReadSerializer
from .models import Article
from .queries import article_active, article_by_id
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateArticleSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        article_uuid = uuid.uuid4()

        with transaction.atomic():
            insert_payload = {
                'id' : str(article_uuid),
                'created_at' : datetime.now(),
                'created_by' : request.user.id,
                'is_active' : True,
                'title' : validated_payload.get('title'),
                'body' : validated_payload.get('body'),
            }
            Article(**insert_payload).save()

            tag_payload = []
            for tag in validated_payload.get('tag'):
                tag_uuid = uuid.uuid4()
                payload = ArticleTag(
                    id=tag_uuid,
                    created_at=datetime.now(),
                    created_by=request.user.id,
                    article=article_by_id(article_uuid).first(),
                    tag=dictionary_by_id(tag).first(),
                )
                tag_payload.append(payload)
            ArticleTag.objects.bulk_create(tag_payload)

            article_attachment = article_attachment_by_multiple_id(validated_payload.get('attachment'))
            article_attachment.update(
                article=str(article_uuid)
            )
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': insert_payload.get('id')}, message=None, error=None, status_code=200)
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
        payload = ReadSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        paginator = CustomPageNumberPagination()
        article = article_active(validated_payload.get('search'), validated_payload.get('tag'))
        result_page = paginator.paginate_queryset(article, request)
        serializer = ArticleSerializer(result_page, many=True)

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
        article = article_by_id(id)
        if not article:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)

        return output_response(success=RESPONSE_SUCCESS, data=ArticleSerializer(article, many=True).data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)