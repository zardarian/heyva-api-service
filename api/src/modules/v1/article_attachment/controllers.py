from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.paginations.page_number_pagination import CustomPageNumberPagination   
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.storages.services import put_object, remove_object
from src.modules.v1.article.queries import article_by_id
from datetime import datetime
from .serializers import CreateArticleAttachmentSerializer, ArticleAttachmentSerializer
from .models import ArticleAttachment
from .queries import article_attachment_unused
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def create(request):
    payload = CreateArticleAttachmentSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        with transaction.atomic():
            attachment_payload = []
            
            for attachment in validated_payload.get('attachment'):
                attachment_uuid = uuid.uuid4()
                attachment_path = put_object('article', attachment)

                payload = ArticleAttachment(
                    id=attachment_uuid,
                    created_at=datetime.now(),
                    created_by=request.user.get('id'),
                    article=article_by_id(validated_payload.get('article')).first(),
                    attachment=attachment_path
                )
                attachment_payload.append(payload)
            ArticleAttachment.objects.bulk_create(attachment_payload)
        
        return output_response(success=RESPONSE_SUCCESS, data=ArticleAttachmentSerializer(attachment_payload, many=True).data, message=None, error=None, status_code=200)
    except Exception as e:
        for payload in attachment_payload:
            remove_object(payload.attachment)

        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def read_unused(request):
    try:
        paginator = CustomPageNumberPagination()
        article = article_attachment_unused()
        result_page = paginator.paginate_queryset(article, request)
        serializer = ArticleAttachmentSerializer(result_page, many=True)

        return paginator.get_paginated_response(success=RESPONSE_SUCCESS, data=serializer.data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)