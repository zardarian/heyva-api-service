from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes
from datetime import datetime
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, USER_DOES_NOT_EXISTS
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.storages.services import put_object, remove_object
from src.modules.v1.dictionary.queries import dictionary_by_id
from src.modules.v1.pregnancy.queries import pregnancy_by_profile_code
from src.modules.v1.interest.queries import interests_by_profile_code
from src.modules.v1.interest.models import Interest
from .serializers import ProfileSerializer, UpdateProfileSerializer
from .models import Profile
from .queries import profile_by_user_id, profile_by_code
import sys
import uuid

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def get_profile(request):
    try:
        profile = profile_by_user_id(request.user.get('id'))
        if not profile:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        profile = profile.first()
        serialize_user = ProfileSerializer(profile).data

        return output_response(success=RESPONSE_SUCCESS, data=serialize_user, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
def update(request):
    payload = UpdateProfileSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        profile = profile_by_user_id(request.user.get('id'))
        if not profile:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        legacy = profile.values().first()
        avatar = legacy.get('avatar')

        if validated_payload.get('avatar'):
            remove_object(legacy.get('avatar'))
            avatar = put_object('avatar', validated_payload.get('avatar'))

        with transaction.atomic():
            profile.update(
                updated_at=datetime.now(),
                updated_by=request.user.get('id'),
                full_name=validated_payload.get('full_name', legacy.get('full_name')),
                name_alias=validated_payload.get('name_alias', legacy.get('name_alias')),
                birth_date=validated_payload.get('birth_date', legacy.get('birth_date')),
                gender=dictionary_by_id(validated_payload.get('gender', legacy.get('gender'))).first(),
                avatar=avatar,
                slug_name=validated_payload.get('slug_name', legacy.get('slug_name')),
                about_me=validated_payload.get('about_me', legacy.get('about_me')),
            )

            if validated_payload.get('pregnancy_status') or validated_payload.get('estimated_due_date') or validated_payload.get('child_birth_date'):
                pregnancy = pregnancy_by_profile_code(legacy.get('code'))
                pregnancy_legacy = pregnancy.values().first()
                
                pregnancy.update(
                    updated_at=datetime.now(),
                    updated_by=request.user.get('id'),
                    status=dictionary_by_id(validated_payload.get('pregnancy_status', pregnancy_legacy.get('status'))).first(),
                    estimated_due_date=validated_payload.get('estimated_due_date', pregnancy_legacy.get('estimated_due_date')),
                    child_birth_date=validated_payload.get('child_birth_date', pregnancy_legacy.get('child_birth_date'))
                )

            if validated_payload.get('interests'):
                interests_by_profile_code(legacy.get('code')).delete()
                interest_payload = []

                for interest in validated_payload.get('interests'):
                    interest_uuid = uuid.uuid4()
                    payload = Interest(
                        id=interest_uuid,
                        created_at=datetime.now(),
                        created_by=request.user.get('id'),
                        profile_code=profile_by_code(legacy.get('code')).first(),
                        interests=dictionary_by_id(interest).first()
                    )
                    interest_payload.append(payload)
                Interest.objects.bulk_create(interest_payload)

        return output_response(success=RESPONSE_SUCCESS, data={'id': legacy.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
