from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime
from src.storages.services import put_object, remove_object
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.modules.v1.doctor_tag.models import DoctorTag
from src.modules.v1.profile.queries import profile_by_code
from src.modules.v1.dictionary.queries import dictionary_by_id
from .serializers import CreateDoctorSerializer, ReadDoctorSerializer, DoctorSerializer
from .models import Doctor
from .queries import get_latest_doctor_code_today, doctor_by_id, doctor_active
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def create(request):
    payload = CreateDoctorSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        today = datetime.today()
        doctor_uuid = uuid.uuid4()

        latest_doctor_code = get_latest_doctor_code_today()
        if not latest_doctor_code:
            doctor_code = "{}{}{}".format("DOC-", str(today.strftime("%Y%m%d")), str(1).zfill(4))
        else:
            extract_id = int(latest_doctor_code.first().code[-4:])
            next_id = extract_id + 1
            doctor_code = "{}{}{}".format("DOC-", str(today.strftime("%Y%m%d")), str(next_id).zfill(4))

        with transaction.atomic():
            avatar = put_object('doctor/avatar', validated_payload.get('avatar'))

            doctor_payload = {
                'id' : doctor_uuid,
                'created_at' : datetime.now(),
                'created_by' : request.user.get('id'),
                'is_active' : True,
                'code' : doctor_code,
                'profile_code' : profile_by_code(validated_payload.get('profile_code')).first(),
                'name' : validated_payload.get('name'),
                'specialist' : validated_payload.get('specialist'),
                'about' : validated_payload.get('about'),
                'rate' : validated_payload.get('rate'),
                'domicile' : validated_payload.get('domicile'),
                'phone_number' : validated_payload.get('phone_number'),
                'avatar': avatar
            }
            Doctor(**doctor_payload).save()

            tag_payload = []
            for tag in validated_payload.get('tag'):
                tag_uuid = uuid.uuid4()
                payload = DoctorTag(
                    id=tag_uuid,
                    created_at=datetime.now(),
                    created_by=request.user.get('id'),
                    doctor=doctor_by_id(doctor_uuid).first(),
                    tag=dictionary_by_id(tag).first(),
                )
                tag_payload.append(payload)
            DoctorTag.objects.bulk_create(tag_payload)
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': doctor_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        remove_object(doctor_payload.get('avatar'))
        
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['GET'])
@authentication_classes([CustomBasicAuthentication])
def read_list(request):
    try:
        payload = ReadDoctorSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        paginator = CustomPageNumberPagination()
        doctor = doctor_active(validated_payload.get('search'), validated_payload.get('tag'))
        result_page = paginator.paginate_queryset(doctor, request)
        serializer = DoctorSerializer(result_page, many=True)

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
        doctor = doctor_by_id(id)
        if not doctor:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)

        return output_response(success=RESPONSE_SUCCESS, data=DoctorSerializer(doctor, many=True).data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)