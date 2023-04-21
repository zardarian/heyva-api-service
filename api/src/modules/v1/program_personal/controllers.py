from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime, timedelta
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.storages.services import put_object, remove_object
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND, OBJECTS_ALREADY_EXISTS
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.modules.v1.program.queries import program_by_id
from src.modules.v1.profile.queries import profile_by_user_id
from .serializers import CreateProgramPersonalSerializer, UpdateProgramPersonalSerializer
from .models import ProgramPersonal
from .queries import program_personal_not_finished_by_program_id
import uuid
import sys

program_days = 90

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateProgramPersonalSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        program_personal = program_personal_not_finished_by_program_id(request.user.get('profile_code'), validated_payload.get('program'))
        if program_personal:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_ALREADY_EXISTS, error=None, status_code=400)

        program_personal_uuid = uuid.uuid4()

        with transaction.atomic():
            program_personal_payload = {
                'id' : program_personal_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'profile_code' : profile_by_user_id(request.user.get('id')).first(),
                'program' : program_by_id(validated_payload.get('program')).first(),
                'is_finished' : False,
                'start_date' : datetime.now(),
                'end_date' : datetime.now() + timedelta(days=program_days)
            }
            ProgramPersonal(**program_personal_payload).save()

        return output_response(success=RESPONSE_SUCCESS, data={'id': program_personal_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
def finish_program(request, program_id):
    try:
        program_personal = program_personal_not_finished_by_program_id(program_id)

        with transaction.atomic():
            program_personal.update(
                updated_at = datetime.now(),
                updated_by = request.user.get('id'),
                is_finished = True
            )

        return output_response(success=RESPONSE_SUCCESS, data={'id': program_id}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)