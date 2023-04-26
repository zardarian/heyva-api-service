from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime
from src.storages.services import put_object, remove_object
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.modules.v1.profile.queries import profile_by_user_id
from src.modules.v1.terms_privacy.queries import terms_privacy_by_id, terms_privacy_by_type
from .serializers import CreateTermsPrivacyPersonalSerializer, ReadTermsPrivacyPersonalByTypeSerializer, TermsPrivacyPersonalSerializer, CreateTermsPrivacyPersonalListSerializer
from .models import TermsPrivacyPersonal
from .queries import terms_privacy_personal_by_terms_privacy_id
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateTermsPrivacyPersonalSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        with transaction.atomic():
            terms_privacy_personal = terms_privacy_personal_by_terms_privacy_id(request.user.get('profile_code'), validated_payload.get('terms_privacy'))

            if not terms_privacy_personal:
                terms_privacy_personal_uuid = uuid.uuid4()

                terms_privacy_personal_payload = {
                    'id' : terms_privacy_personal_uuid,
                    'created_at' : datetime.now(),
                    'created_by' : request.user.get('id'),
                    'profile_code' : profile_by_user_id(request.user.get('id')).first(),
                    'terms_privacy' : terms_privacy_by_id(validated_payload.get('terms_privacy')).first(),
                    'is_agree' : validated_payload.get('is_agree'),
                }
                TermsPrivacyPersonal(**terms_privacy_personal_payload).save()
            else:
                terms_privacy_personal_uuid = terms_privacy_personal.values().first().get('id')

                terms_privacy_personal.update(
                    is_agree=validated_payload.get('is_agree'),
                    updated_at=datetime.now(),
                    updated_by=request.user.get('id')
                )
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': terms_privacy_personal_uuid}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create_list(request):
    payload = CreateTermsPrivacyPersonalListSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        with transaction.atomic():
            terms_privacy_personal_payload = []
            for index, terms_privacy in enumerate(validated_payload.get('terms_privacy')):
                terms_privacy_personal = terms_privacy_personal_by_terms_privacy_id(request.user.get('profile_code'), terms_privacy)

                if not terms_privacy_personal:
                    terms_privacy_personal_uuid = uuid.uuid4()
                    
                    payload = TermsPrivacyPersonal(
                        id=terms_privacy_personal_uuid,
                        created_at=datetime.now(),
                        created_by=request.user.get('id'),
                        profile_code=profile_by_user_id(request.user.get('id')).first(),
                        terms_privacy=terms_privacy_by_id(terms_privacy).first(),
                        is_agree=validated_payload.get('is_agree')[index]
                    )
                    terms_privacy_personal_payload.append(payload)
                else:
                    terms_privacy_personal.update(
                        is_agree=validated_payload.get('is_agree')[index],
                        updated_at=datetime.now(),
                        updated_by=request.user.get('id')
                    )

            if terms_privacy_personal_payload:
                TermsPrivacyPersonal.objects.bulk_create(terms_privacy_personal_payload)
        
        return output_response(success=RESPONSE_SUCCESS, data=None, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def read_by_type(request):
    try:
        payload = ReadTermsPrivacyPersonalByTypeSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        terms_privacy = terms_privacy_by_type(validated_payload.get('type'), None, None)
        if not terms_privacy:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)
        
        terms_privacy = terms_privacy.values().first()
        terms_privacy_personal = terms_privacy_personal_by_terms_privacy_id(request.user.get('profile_code'), terms_privacy.get('id'))
        if not terms_privacy_personal:
            return output_response(success=RESPONSE_FAILED, data=None, message=OBJECTS_NOT_FOUND, error=None, status_code=400)
        
        serializer = TermsPrivacyPersonalSerializer(terms_privacy_personal.first()).data

        return output_response(success=RESPONSE_SUCCESS, data=serializer, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)