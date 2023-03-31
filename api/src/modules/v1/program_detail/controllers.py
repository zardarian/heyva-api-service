from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.storages.services import put_object, remove_object
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.program.queries import program_by_id
from datetime import datetime
from .serializers import CreateProgramDetailSerializer
from .models import ProgramDetail
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def create(request):
    payload = CreateProgramDetailSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        program_detail_uuid = uuid.uuid4()

        with transaction.atomic():
            image_path = put_object('program/detail', validated_payload.get('image_content'))
            video_path = put_object('program/detail', validated_payload.get('video_content'))

            program_detail_payload = {
                'id' : program_detail_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'program' : program_by_id(validated_payload.get('program')).first(),
                'content_type' : validated_payload.get('content_type'),
                'text_content' : validated_payload.get('text_content'),
                'image_content' : image_path,
                'video_content' : video_path,
                'json_content' : validated_payload.get('json_content'),
                'order' : validated_payload.get('order'),
            }
            ProgramDetail(**program_detail_payload).save()

        return output_response(success=RESPONSE_SUCCESS, data={'id': program_detail_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        remove_object(validated_payload.get('image_content'))
        remove_object(validated_payload.get('video_content'))
            
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)