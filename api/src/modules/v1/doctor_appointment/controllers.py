from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.modules.v1.profile.queries import profile_by_user_id
from src.modules.v1.doctor.queries import doctor_by_code
from src.modules.v1.dictionary.queries import dictionary_by_id
from .serializers import CreateDoctorAppointmentSerializer
from .models import DoctorAppointment
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateDoctorAppointmentSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        doctor_appointment_uuid = uuid.uuid4()

        with transaction.atomic():
            doctor_appointment_payload = {
                'id' : doctor_appointment_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'profile_code' : profile_by_user_id(request.user.get('id')).first(),
                'doctor_code' : doctor_by_code(validated_payload.get('doctor_code')).first(),
                'date' : validated_payload.get('date'),
                'hour' : validated_payload.get('hour'),
                'service' : dictionary_by_id(validated_payload.get('service')).first(),
            }
            DoctorAppointment(**doctor_appointment_payload).save()
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': doctor_appointment_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)