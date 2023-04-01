from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime, timedelta
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.storages.services import put_object, remove_object
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.modules.v1.program.queries import program_by_id
from src.modules.v1.profile.queries import profile_by_user_id
from .serializers import CreateProgramPersonalTrackerSerializer
from .models import ProgramPersonalTracker
from .queries import program_personal_tracker_not_finished_by_program_id
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateProgramPersonalTrackerSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        program_personal_tracker_uuid = uuid.uuid4()

        with transaction.atomic():
            program_personal_tracker_payload = {
                'id' : program_personal_tracker_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'program' : program_by_id(validated_payload.get('program')).first(),
                'child_program' : program_by_id(validated_payload.get('child_program')).first(),
                'profile_code' : profile_by_user_id(request.user.get('id')).first(),
                'is_finished' : False,
                'check_in_date' : datetime.now(),
            }
            ProgramPersonalTracker(**program_personal_tracker_payload).save()

        return output_response(success=RESPONSE_SUCCESS, data={'id': program_personal_tracker_payload.get('id')}, message=None, error=None, status_code=200)
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
        program_personal_tracker = program_personal_tracker_not_finished_by_program_id(program_id)

        with transaction.atomic():
            program_personal_tracker.update(
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