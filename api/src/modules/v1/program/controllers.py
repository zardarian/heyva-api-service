from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.storages.services import put_object, remove_object
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.program_tag.models import ProgramTag
from src.modules.v1.dictionary.queries import dictionary_by_id
from datetime import datetime
from .serializers import CreateProgramSerializer
from .models import Program
from .queries import program_by_id
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def create(request):
    payload = CreateProgramSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        program_uuid = uuid.uuid4()

        with transaction.atomic():
            banner_path = put_object('program/banner', validated_payload.get('banner'))

            program_payload = {
                'id' : program_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'is_active' : True,
                'title' : validated_payload.get('title'),
                'body' : validated_payload.get('body'),
                'banner' : banner_path,
                'parent' : validated_payload.get('parent')
            }
            Program(**program_payload).save()

            tag_payload = []
            for tag in validated_payload.get('tag'):
                tag_uuid = uuid.uuid4()
                payload = ProgramTag(
                    id=tag_uuid,
                    created_at=datetime.now(),
                    created_by=request.user.get('id'),
                    program=program_by_id(program_uuid).first(),
                    tag=dictionary_by_id(tag).first(),
                )
                tag_payload.append(payload)
            ProgramTag.objects.bulk_create(tag_payload)

        return output_response(success=RESPONSE_SUCCESS, data={'id': program_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        remove_object(validated_payload.get('banner'))
            
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)